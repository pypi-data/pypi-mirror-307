"""Cross-platform command execution module."""

import subprocess
import threading
import os
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
    
    def __init__(self):
        self.platform_info = get_platform_info()
        self.command_mapping = CommandMapping()
        self.encoding = get_command_output_encoding(self.platform_info)
        self.current_process = None
        self._previous_dir = None
    
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
    
    def _sanitize_command(self, command: Command) -> List[str]:
        """
        Sanitize and prepare command for execution.
        
        Args:
            command: Command object to sanitize
            
        Returns:
            List[str]: Sanitized command and arguments
        """
        # Map command to platform-specific version
        executable = self.command_mapping.get_command(
            command.executable,
            self.platform_info
        )
        
        # Start with the shell and its argument
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
        while True:
            # Read stdout
            if process.stdout:
                line = process.stdout.readline()
                if not line and process.poll() is not None:
                    break
                if line:
                    decoded_line = line.decode(self.encoding).rstrip('\r\n')
                    output_lines.append(decoded_line)
                    console.print(decoded_line)

            # Read stderr
            if process.stderr:
                line = process.stderr.readline()
                if line:
                    decoded_line = line.decode(self.encoding).rstrip('\r\n')
                    error_lines.append(decoded_line)
                    console.print(f"[red]{decoded_line}[/red]")

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
                target_dir = command.args[0]
            
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
            
            # Sanitize and prepare command
            cmd_list = self._sanitize_command(command)
            
            # Execute command with real-time output streaming
            output_lines = []
            error_lines = []
            
            process = subprocess.Popen(
                cmd_list,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                bufsize=0,  # Unbuffered
                universal_newlines=False,  # Binary mode for proper encoding handling
                shell=False,  # More secure
                cwd=os.getcwd()  # Use current working directory
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
            
            # Wait for process to complete
            exit_code = process.wait()
            stream_thread.join()  # Wait for streaming to complete
            
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
