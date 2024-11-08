"""Enhanced input handling with history navigation."""

import os
from typing import Optional

from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from rich.console import Console

from .history import HistoryManager

console = Console()

class InputHandler:
    """Handles user input with history navigation and search."""
    
    def __init__(self, history_manager: HistoryManager):
        self.history_manager = history_manager
        self.prompt_history = InMemoryHistory()
        self.session = self._create_session()
        
    def _create_session(self) -> PromptSession:
        """Create a prompt session with custom keybindings."""
        kb = KeyBindings()
        
        @kb.add(Keys.Up)
        def _(event):
            """Handle up arrow key."""
            prev_cmd = self.history_manager.get_previous_command()
            if prev_cmd:
                event.current_buffer.text = prev_cmd
        
        @kb.add(Keys.Down)
        def _(event):
            """Handle down arrow key."""
            next_cmd = self.history_manager.get_next_command()
            if next_cmd:
                event.current_buffer.text = next_cmd
            else:
                event.current_buffer.text = ""
        
        @kb.add('c-r')
        def _(event):
            """Handle Ctrl+R for history search."""
            # Get current text as search term
            search_term = event.current_buffer.text
            results = self.history_manager.search_history(search_term)
            
            if results:
                # Show search results
                console.print("\nMatching commands:")
                for i, entry in enumerate(results, 1):
                    success_marker = "✓" if entry['success'] else "✗"
                    console.print(
                        f"{i}. [{entry['success'] and 'green' or 'red'}]{success_marker}[/] "
                        f"{entry['natural_command']} → {entry['translated_command']}"
                    )
        
        return PromptSession(
            history=self.prompt_history,
            key_bindings=kb,
            enable_history_search=True,
            search_ignore_case=True
        )
    
    def get_input(self, prompt_text: str = "") -> str:
        """
        Get user input with history support.
        
        Args:
            prompt_text: Text to show in the prompt
            
        Returns:
            str: User input
        """
        try:
            return self.session.prompt(prompt_text)
        except (KeyboardInterrupt, EOFError):
            return "exit"
