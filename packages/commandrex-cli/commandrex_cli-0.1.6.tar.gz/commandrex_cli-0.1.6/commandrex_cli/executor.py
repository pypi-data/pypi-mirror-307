"""Cross-platform command execution module."""

import subprocess
import threading
import os
import signal
import time
from typing import List, Optional

from rich.console import Console

from .platform_utils import (
    get_platform_info,
    get_command_output_encoding,
    is_dangerous_command,
    CommandMapping,
    PlatformInfo
)
from .schemas import Command, CommandResult

console = Console()

class CommandExecutor:
    """Safely executes translated commands across different platforms."""
    
    # Commands that should be executed directly without shell wrapping
    DIRECT_EXECUTE_COMMANDS = {
        'ps', 'ls', 'dir', 'ping', 'netstat', 'top', 'htop',
        'df', 'du', 'free', 'who', 'w', 'uptime'
    }

    # Commands that are typically continuous and need special handling
    CONTINUOUS_COMMANDS = {
        'ping': {'max_packets': 4},  # Stop ping after 4 packets
        'top': {'timeout': 10},      # Run top for 10 seconds
        'htop': {'timeout': 10},     # Run htop for 10 seconds
    }
    
    def __init__(self):
        self.platform_info = get_platform_info()
        self.command_mapping = CommandMapping()
        self.encoding = get_command_output_encoding(self.platform_info)
        self.current_process = None
        self._previous_dir = None
        self._stop_streaming = False
    
    def is_dangerous(self, command: Command) -> bool:
        """
        Check if a command is potentially dangerous.
        
        Args:
            command: Command object to check
            
        Returns:
            bool: True if command is considered dangerous
        """
        # Check if already flagged as dangerous
        if command.is_dangerous:
            return True
            
        # Check against platform-specific dangerous commands
        if is_dangerous_command(command.executable, self.platform_info):
            return True
            
        # Check for dangerous patterns in arguments
        dangerous_patterns = {
            'windows': {'/q', '/f', '/s', '/y', '-y', '--force'},
            'unix': {'/*', '-rf', '-r', '--force', '-f'}
        }.get(self.platform_info.os_type, set())
        
        return any(pattern in arg.lower() for arg in command.args
                  for pattern in dangerous_patterns)
    
    def _prepare_command(self, command: Command) -> List[str]:
        """
        Prepare command for execution.
        
        Args:
            command: Command object to prepare
            
        Returns:
            List[str]: Command and arguments ready for execution
        """
        # Map command to platform-specific version
        executable = self.command_mapping.get_command(
            command.executable,
            self.platform_info
        )

        # Handle continuous commands like ping
        if executable == 'ping':
            # Add count parameter based on platform
            if self.platform_info.os_type == 'windows':
                return [executable, '-n', '4', *command.args]  # Windows uses -n
            else:
                return [executable, '-c', '4', *command.args]  # Unix uses -c
        
        # For direct execute commands, return the command and args directly
        if command.executable.lower() in self.DIRECT_EXECUTE_COMMANDS:
            return [executable, *command.args]
        
        # For other commands, wrap in shell
        cmd_list = [
            self.platform_info.shell_path,
            *self.platform_info.shell_args
        ]
        
        # Create the command string
        if self.platform_info.is_powershell:
            # PowerShell needs special handling for some commands
            cmd_str = f"& {executable} {' '.join(command.args)}"
        else:
            cmd_str = f"{executable} {' '.join(command.args)}"
        
        cmd_list.append(cmd_str)
        return cmd_list

    def _stream_output(self, process: subprocess.Popen, output_lines: list, error_lines: list):
        """Stream output from process in real-time."""
        self._stop_streaming = False
        
        def read_stream(stream, lines, is_error=False):
            """Read from a stream and process lines."""
            try:
                while not self._stop_streaming:
                    chunk = stream.read(4096)  # Changed from read1 to read
                    if not chunk and process.poll() is not None:
                        break
                    if chunk:
                        try:
                            decoded_text = chunk.decode(self.encoding)
                            lines_text = decoded_text.splitlines()
                            
                            for line in lines_text:
                                if line:
                                    lines.append(line)
                                    if is_error:
                                        console.print(f"[red]{line}[/red]")
                                    else:
                                        console.print(line)
                        except UnicodeDecodeError:
                            try:
                                decoded_text = chunk.decode('utf-8', errors='replace')
                                lines_text = decoded_text.splitlines()
                                
                                for line in lines_text:
                                    if line:
                                        lines.append(line)
                                        if is_error:
                                            console.print(f"[red]{line}[/red]")
                                        else:
                                            console.print(line)
                            except:
                                continue
            except (OSError, IOError):
                pass  # Handle pipe errors gracefully
        
        # Create separate threads for stdout and stderr
        if process.stdout:
            stdout_thread = threading.Thread(
                target=read_stream,
                args=(process.stdout, output_lines)
            )
            stdout_thread.daemon = True
            stdout_thread.start()
        
        if process.stderr:
            stderr_thread = threading.Thread(
                target=read_stream,
                args=(process.stderr, error_lines, True)
            )
            stderr_thread.daemon = True
            stderr_thread.start()
        
        # Wait for both streams to complete
        if process.stdout:
            stdout_thread.join()
        if process.stderr:
            stderr_thread.join()

    def _handle_cd_command(self, command: Command) -> CommandResult:
        """
        Special handling for cd command to make directory changes persist.
        
        Args:
            command: Command object containing cd command
            
        Returns:
            CommandResult: Result of directory change
        """
        try:
            # Get the target directory from command args
            if not command.args:
                # cd without args should go to home directory
                target_dir = os.path.expanduser("~")
            else:
                # Expand any ~ in the path first
                target_dir = os.path.expanduser(command.args[0])
            
            # Handle special cases
            if target_dir == "-":
                # cd - to go to previous directory
                if not self._previous_dir:
                    return CommandResult(
                        success=False,
                        output="",
                        error="No previous directory",
                        exit_code=1
                    )
                target_dir = self._previous_dir
            
            # Store current directory before changing
            self._previous_dir = os.getcwd()
            
            # Handle relative paths
            if not os.path.isabs(target_dir):
                target_dir = os.path.abspath(os.path.join(os.getcwd(), target_dir))
            
            # Change directory in the main process
            os.chdir(target_dir)
            
            # Get and display new working directory
            new_dir = os.getcwd()
            return CommandResult(
                success=True,
                output=f"Current directory: {new_dir}",
                error=None,
                exit_code=0
            )
            
        except Exception as e:
            return CommandResult(
                success=False,
                output="",
                error=str(e),
                exit_code=1
            )

    def stop_current_process(self):
        """Stop the currently running process if any."""
        if self.current_process:
            self._stop_streaming = True
            if self.platform_info.os_type == 'windows':
                self.current_process.terminate()
            else:
                os.killpg(os.getpgid(self.current_process.pid), signal.SIGINT)

    def execute(self, command: Command) -> CommandResult:
        """
        Execute a command safely with real-time output streaming.
        
        Args:
            command: Command object to execute
            
        Returns:
            CommandResult: Result of command execution
        """
        try:
            # Special handling for directory change commands
            if command.executable.lower() in ['cd', 'chdir'] or (
                self.platform_info.is_powershell and 
                command.executable.lower() == 'set-location'
            ):
                # If it's Set-Location, modify the command to use the directory argument
                if command.executable.lower() == 'set-location':
                    modified_command = Command(
                        executable='cd',
                        args=command.args,
                        is_dangerous=command.is_dangerous
                    )
                    return self._handle_cd_command(modified_command)
                return self._handle_cd_command(command)
            
            # Additional safety check
            if self.is_dangerous(command):
                confirm = console.input(
                    "[yellow]This command may be dangerous. "
                    "Are you sure you want to proceed? (y/N): [/yellow]"
                ).lower()
                
                if confirm != 'y':
                    return CommandResult(
                        success=False,
                        output="Command cancelled by user.",
                        error=None,
                        exit_code=1
                    )
            
            # Prepare command
            cmd_list = self._prepare_command(command)
            
            # Execute command with real-time output streaming
            output_lines = []
            error_lines = []
            
            # Determine if we should use shell
            use_shell = command.executable.lower() not in self.DIRECT_EXECUTE_COMMANDS
            
            # Set up process with proper group handling for Unix-like systems
            if self.platform_info.os_type != 'windows':
                process = subprocess.Popen(
                    cmd_list,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    bufsize=0,  # Unbuffered output
                    shell=use_shell,
                    cwd=os.getcwd(),
                    preexec_fn=os.setsid  # Create new process group
                )
            else:
                process = subprocess.Popen(
                    cmd_list,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    bufsize=0,  # Unbuffered output
                    shell=use_shell,
                    cwd=os.getcwd()
                )
            
            # Store current process
            self.current_process = process
            
            # Create and start output streaming thread
            stream_thread = threading.Thread(
                target=self._stream_output,
                args=(process, output_lines, error_lines)
            )
            stream_thread.daemon = True  # Thread will be terminated when main thread exits
            stream_thread.start()
            
            try:
                # For continuous commands, wait with timeout
                if command.executable.lower() in self.CONTINUOUS_COMMANDS:
                    config = self.CONTINUOUS_COMMANDS[command.executable.lower()]
                    timeout = config.get('timeout', 10)  # Default timeout of 10 seconds
                    try:
                        exit_code = process.wait(timeout=timeout)
                    except subprocess.TimeoutExpired:
                        self.stop_current_process()
                        exit_code = 0  # Consider timeout as normal completion
                else:
                    # Wait for process to complete or user interrupt
                    exit_code = process.wait()
            except KeyboardInterrupt:
                self.stop_current_process()
                exit_code = 0  # Consider interrupt as normal termination
            finally:
                self._stop_streaming = True
                stream_thread.join(timeout=1.0)  # Wait for streaming to complete with timeout
                
                # Clear current process
                self.current_process = None
            
            # Combine output and error lines
            output = '\n'.join(output_lines)
            error = '\n'.join(error_lines) if error_lines else None
            
            return CommandResult(
                success=exit_code == 0,
                output=output,
                error=error,
                exit_code=exit_code
            )
            
        except subprocess.SubprocessError as e:
            return CommandResult(
                success=False,
                output="",
                error=str(e),
                exit_code=1
            )
        except Exception as e:
            return CommandResult(
                success=False,
                output="",
                error=f"Unexpected error: {str(e)}",
                exit_code=1
            )

__all__ = ['CommandExecutor']
