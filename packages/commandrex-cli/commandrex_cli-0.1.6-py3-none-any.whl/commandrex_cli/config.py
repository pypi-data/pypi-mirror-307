"""Configuration management for CommandRex."""

import os
from pathlib import Path
from typing import Optional

import keyring
from rich.console import Console
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

console = Console()

class Config:
    """Configuration management for CommandRex."""
    
    # Service name for keyring
    SERVICE_NAME = "commandrex-cli"
    
    # OpenAI API configuration
    OPENAI_API_KEY_USERNAME = "openai-api-key"
    OPENAI_MODEL = "gpt-4o-mini"
    
    @classmethod
    def get_api_key(cls) -> Optional[str]:
        """Get the OpenAI API key from keyring or environment."""
        # First try to get from environment
        api_key = os.getenv("OPENAI_API_KEY")
        
        # If not in environment, try keyring
        if not api_key:
            api_key = keyring.get_password(cls.SERVICE_NAME, cls.OPENAI_API_KEY_USERNAME)
            
            # If found in keyring, save to environment for this session
            if api_key:
                os.environ["OPENAI_API_KEY"] = api_key
        
        return api_key

    @classmethod
    def save_api_key(cls, api_key: str) -> None:
        """Save the OpenAI API key to keyring and environment."""
        # Save to keyring
        keyring.set_password(cls.SERVICE_NAME, cls.OPENAI_API_KEY_USERNAME, api_key)
        
        # Also save to environment for current session
        os.environ["OPENAI_API_KEY"] = api_key
        console.print("[green]API key saved successfully![/green]")

    @classmethod
    def remove_api_key(cls) -> None:
        """Remove the API key from keyring."""
        try:
            keyring.delete_password(cls.SERVICE_NAME, cls.OPENAI_API_KEY_USERNAME)
            if "OPENAI_API_KEY" in os.environ:
                del os.environ["OPENAI_API_KEY"]
            console.print("[yellow]API key removed.[/yellow]")
        except keyring.errors.PasswordDeleteError:
            pass  # Key doesn't exist

    @classmethod
    def validate_api_key(cls, api_key: str) -> bool:
        """
        Basic validation of API key format.
        
        Args:
            api_key: The API key to validate
            
        Returns:
            bool: True if the key format is valid
        """
        if not api_key:
            return False
        
        # Basic format validation - OpenAI API keys typically start with 'sk-'
        if not api_key.startswith('sk-'):
            console.print("[yellow]Warning: API key should start with 'sk-'[/yellow]")
            return False
            
        # Check minimum length
        if len(api_key) < 20:
            console.print("[yellow]Warning: API key seems too short[/yellow]")
            return False
            
        return True
