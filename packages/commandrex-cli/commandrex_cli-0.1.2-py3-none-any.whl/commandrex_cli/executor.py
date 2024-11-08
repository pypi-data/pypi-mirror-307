"""Cross-platform command execution module."""

import subprocess
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
    
    def execute(self, command: Command) -> CommandResult:
        """
        Execute a command safely.
        
        Args:
            command: Command object to execute
            
        Returns:
            CommandResult: Result of command execution
        """
        try:
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
            
            # Execute command with proper encoding
            process = subprocess.run(
                cmd_list,
                capture_output=True,
                text=True,
                encoding=self.encoding,
                shell=False  # More secure
            )
            
            # Process output
            output = process.stdout if process.stdout else ""
            error = process.stderr if process.stderr else None
            
            # Clean up output based on platform
            if self.platform_info.os_type == 'windows':
                output = output.replace('\r\n', '\n')
                if error:
                    error = error.replace('\r\n', '\n')
            
            return CommandResult(
                success=process.returncode == 0,
                output=output,
                error=error,
                exit_code=process.returncode
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