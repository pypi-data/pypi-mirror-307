"""Terminal user interface with history support."""

import platform
import os
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.prompt import Confirm
from rich.theme import Theme
from rich.table import Table

from .schemas import Command, CommandResult, TranslationResponse
from .history import HistoryManager
from .input_handler import InputHandler

# Create a custom theme for consistent styling
custom_theme = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "red",
    "success": "green",
    "history": "blue",
    "path": "yellow"
})

class CommandRexUI:
    """Handles all terminal UI interactions."""
    
    def __init__(self):
        self.os_type = platform.system()
        self.console = Console(theme=custom_theme)
        self.history_manager = HistoryManager()
        self.input_handler = InputHandler(self.history_manager)
        
    def show_welcome(self):
        """Display welcome message and basic instructions."""
        welcome_text = """
🦖 Welcome to CommandRex! 
Talk to your terminal in plain English.

Tips:
• Type your command in natural language
• Use ↑/↓ arrows to navigate command history
• Press Ctrl+R to search history
• Type 'history' to see command history
• Type 'stats' to see usage statistics
• Type 'exit' or 'quit' to leave
• Type 'help' for more information
        """
        self.console.print(Panel(welcome_text, title="CommandRex CLI", border_style="cyan"))
    
    def show_help(self):
        """Display help information."""
        help_text = """
Commands:
• [bold]Natural Language[/bold]: Just type what you want to do
• [bold]history[/bold]: Show command history
• [bold]stats[/bold]: Show usage statistics
• [bold]clear[/bold]: Clear the screen
• [bold]exit[/bold] or [bold]quit[/bold]: Exit CommandRex

Navigation:
• [bold]↑/↓ Arrows[/bold]: Navigate through command history
• [bold]Ctrl+R[/bold]: Search command history
• [bold]Tab[/bold]: Auto-complete (coming soon)

Examples:
• "Show all files in the current directory"
• "Create a new folder called projects"
• "What's my IP address"
        """
        self.console.print(Panel(help_text, title="Help", border_style="cyan"))
    
    def get_user_input(self, prompt_text: str = "CommandRex 🦖 > ") -> str:
        """
        Get input from user with proper formatting.
        
        Args:
            prompt_text: The prompt text to display
            
        Returns:
            str: User input
        """
        try:
            # Get current directory and format it
            current_dir = os.getcwd()
            # Create prompt with current directory
            full_prompt = f"[path]{current_dir}[/path]\nCommandRex 🦖 > "
            return self.input_handler.get_input(full_prompt)
        except (KeyboardInterrupt, EOFError):
            return "exit"
    
    def display_history(self, limit: int = 10):
        """
        Display command history.
        
        Args:
            limit: Maximum number of entries to show
        """
        if not self.history_manager.history:
            self.console.print("[yellow]No command history available.[/yellow]")
            return
            
        table = Table(title="Command History")
        table.add_column("Status", justify="center", style="bold")
        table.add_column("Natural Command")
        table.add_column("Translated Command", style="cyan")
        
        # Show most recent commands first
        for entry in reversed(self.history_manager.history[-limit:]):
            status = "✓" if entry['success'] else "✗"
            status_style = "green" if entry['success'] else "red"
            table.add_row(
                f"[{status_style}]{status}[/{status_style}]",
                entry['natural_command'],
                entry['translated_command']
            )
        
        self.console.print(table)
    
    def display_statistics(self):
        """Display command usage statistics."""
        stats = self.history_manager.get_statistics()
        
        table = Table(title="Usage Statistics", show_header=False)
        table.add_column("Metric")
        table.add_column("Value")
        
        table.add_row(
            "Total Commands",
            str(stats['total_commands'])
        )
        table.add_row(
            "Successful Commands",
            f"[green]{stats['successful_commands']}[/green]"
        )
        table.add_row(
            "Failed Commands",
            f"[red]{stats['failed_commands']}[/red]"
        )
        table.add_row(
            "Success Rate",
            f"{stats['success_rate']:.1f}%"
        )
        
        self.console.print(table)
    
    def display_translation(self, translation: TranslationResponse) -> bool:
        """
        Display the translated command and get user confirmation.
        
        Args:
            translation: The translated command response
            
        Returns:
            bool: True if user confirms execution
        """
        self.console.print("\n[info]Translated Command:[/info]")
        
        # Display the main command
        cmd_str = f"{translation.command.executable} {' '.join(translation.command.args)}"
        self.console.print(Syntax(cmd_str, "bash", theme="monokai"))
        
        # Show explanation
        self.console.print(f"\n[info]What it does:[/info] {translation.command.explanation}")
        
        # Show warning for dangerous commands
        if translation.command.is_dangerous:
            self.console.print("\n[warning]⚠️  This command could be dangerous![/warning]")
        
        # Show platform-specific warning
        if translation.command.platform_specific:
            self.console.print(
                f"\n[warning]Note: This command is optimized for {self.os_type}[/warning]"
            )
        
        # Show alternatives if available
        if translation.alternatives:
            self.console.print("\n[info]Alternative commands:[/info]")
            for i, alt in enumerate(translation.alternatives, 1):
                self.console.print(f"\n{i}. {alt.executable} {' '.join(alt.args)}")
                self.console.print(f"   {alt.explanation}")
        
        # Get user confirmation
        return Confirm.ask("\nDo you want to execute this command?", default=False)
    
    def display_result(self, result: CommandResult):
        """
        Display the result of command execution.
        
        Args:
            result: The command execution result
        """
        if result.success:
            if result.error:
                self.console.print("\n[warning]Command completed with warnings:[/warning]")
                self.console.print(result.error)
        else:
            self.console.print("\n[error]Command failed![/error]")
            if result.error:
                self.console.print(f"[error]Error: {result.error}[/error]")
    
    def display_error(self, message: str):
        """Display an error message."""
        self.console.print(f"\n[error]Error: {message}[/error]")
    
    def display_warning(self, message: str):
        """Display a warning message."""
        self.console.print(f"\n[warning]Warning: {message}[/warning]")
    
    def clear_screen(self):
        """Clear the terminal screen."""
        self.console.clear()

    def add_to_history(self, natural_command: str, translated_command: str, success: bool):
        """Add a command to history."""
        self.history_manager.add_command(natural_command, translated_command, success)

    def reset_prompt(self):
        """Reset the prompt state after command execution."""
        # Force a newline to ensure clean prompt display
        self.console.print("")

    def cleanup(self):
        """Cleanup resources before exit."""
        pass
