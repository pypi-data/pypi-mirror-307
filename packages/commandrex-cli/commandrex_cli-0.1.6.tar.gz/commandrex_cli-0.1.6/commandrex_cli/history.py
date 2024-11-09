"""Command history management module."""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from rich.console import Console

console = Console()

class HistoryManager:
    """Manages command history with persistent storage."""
    
    def __init__(self, max_entries: int = 1000):
        self.max_entries = max_entries
        self.history: List[dict] = []
        self.current_index = 0
        
        # Set up history file path
        self.history_dir = Path.home() / '.commandrex'
        self.history_file = self.history_dir / 'history.json'
        
        # Create directory if it doesn't exist
        self.history_dir.mkdir(parents=True, exist_ok=True)
        
        # Load existing history
        self.load_history()
    
    def load_history(self):
        """Load command history from file."""
        try:
            if self.history_file.exists():
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
                    # Keep only the last max_entries
                    self.history = self.history[-self.max_entries:]
        except Exception as e:
            console.print(f"[yellow]Warning: Could not load history: {e}[/yellow]")
            self.history = []
    
    def save_history(self):
        """Save command history to file."""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, indent=2)
        except Exception as e:
            console.print(f"[yellow]Warning: Could not save history: {e}[/yellow]")
    
    def add_command(self, natural_command: str, translated_command: str, success: bool):
        """
        Add a command to history.
        
        Args:
            natural_command: The original natural language command
            translated_command: The translated shell command
            success: Whether the command executed successfully
        """
        entry = {
            'timestamp': datetime.now().isoformat(),
            'natural_command': natural_command,
            'translated_command': translated_command,
            'success': success
        }
        
        self.history.append(entry)
        
        # Trim history if it exceeds max entries
        if len(self.history) > self.max_entries:
            self.history = self.history[-self.max_entries:]
        
        self.save_history()
        self.current_index = len(self.history)
    
    def get_previous_command(self) -> Optional[str]:
        """Get the previous command in history."""
        if not self.history:
            return None
            
        self.current_index = max(0, self.current_index - 1)
        if self.current_index < len(self.history):
            return self.history[self.current_index]['natural_command']
        return None
    
    def get_next_command(self) -> Optional[str]:
        """Get the next command in history."""
        if not self.history:
            return None
            
        self.current_index = min(len(self.history), self.current_index + 1)
        if self.current_index < len(self.history):
            return self.history[self.current_index]['natural_command']
        return None
    
    def search_history(self, search_term: str) -> List[dict]:
        """
        Search command history.
        
        Args:
            search_term: Term to search for
            
        Returns:
            List of matching history entries
        """
        search_term = search_term.lower()
        return [
            entry for entry in self.history
            if search_term in entry['natural_command'].lower() or
               search_term in entry['translated_command'].lower()
        ]
    
    def clear_history(self):
        """Clear all command history."""
        self.history = []
        self.save_history()
    
    def get_statistics(self) -> dict:
        """Get history statistics."""
        if not self.history:
            return {
                'total_commands': 0,
                'successful_commands': 0,
                'failed_commands': 0,
                'success_rate': 0.0
            }
        
        total = len(self.history)
        successful = sum(1 for entry in self.history if entry['success'])
        
        return {
            'total_commands': total,
            'successful_commands': successful,
            'failed_commands': total - successful,
            'success_rate': (successful / total) * 100
        }
