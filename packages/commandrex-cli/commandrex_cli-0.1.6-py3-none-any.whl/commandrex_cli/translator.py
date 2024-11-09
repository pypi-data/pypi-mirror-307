"""Cross-platform command translation module using OpenAI API."""

import json
from typing import Optional

from openai import OpenAI, APITimeoutError, APIError, APIConnectionError
from rich.console import Console

from .config import Config
from .schemas import TranslationResponse, Command
from .platform_utils import get_platform_info, PlatformInfo

console = Console()

class CommandTranslator:
    """Translates natural language to platform-specific shell commands."""
    
    def __init__(self):
        api_key = Config.get_api_key()
        if not api_key:
            raise ValueError("OpenAI API key not found. Please set it up first.")
        
        self.client = OpenAI(api_key=api_key)
        self.platform_info = get_platform_info()
        
    def _get_platform_examples(self) -> str:
        """Get platform-specific command examples."""
        if self.platform_info.os_type == 'windows':
            return """
Examples for Windows:
1. List files:
{
  "executable": "dir",
  "args": [],
  "is_dangerous": false,
  "explanation": "Lists files and directories in the current directory",
  "platform_specific": true
}

2. Create directory:
{
  "executable": "md",
  "args": ["new_folder"],
  "is_dangerous": false,
  "explanation": "Creates a new directory named 'new_folder'",
  "platform_specific": true
}
"""
        else:
            return """
Examples for Unix-like systems:
1. List files:
{
  "executable": "ls",
  "args": ["-la"],
  "is_dangerous": false,
  "explanation": "Lists all files with detailed information",
  "platform_specific": true
}

2. Create directory:
{
  "executable": "mkdir",
  "args": ["new_folder"],
  "is_dangerous": false,
  "explanation": "Creates a new directory named 'new_folder'",
  "platform_specific": true
}
"""

    def _get_shell_context(self) -> str:
        """Get shell-specific context information."""
        if self.platform_info.is_powershell:
            return "Using PowerShell. Use PowerShell commands and syntax."
        elif self.platform_info.os_type == 'windows':
            return "Using Windows Command Prompt (cmd.exe). Use CMD commands and syntax."
        else:
            shell_name = self.platform_info.shell_path.split('/')[-1]
            return f"Using {shell_name}. Use appropriate Unix commands and syntax."

    def _create_prompt(self, user_input: str) -> list[dict]:
        """Create the chat messages for the API call."""
        shell_context = self._get_shell_context()
        platform_examples = self._get_platform_examples()
        
        return [
            {
                "role": "system",
                "content": (
                    "You are a command-line interface translator that outputs JSON. "
                    f"Current environment: {self.platform_info.os_type.upper()}. "
                    f"{shell_context}\n\n"
                    "Convert natural language into appropriate terminal commands. "
                    "Format your response as JSON with the following structure:\n"
                    "{\n"
                    '  "executable": "command_name",\n'
                    '  "args": ["arg1", "arg2"],\n'
                    '  "is_dangerous": false,\n'
                    '  "explanation": "What the command does",\n'
                    '  "platform_specific": true\n'
                    "}\n\n"
                    f"{platform_examples}\n"
                    "Important rules:\n"
                    "1. Always use commands native to the current platform\n"
                    "2. Set platform_specific to true for platform-specific commands\n"
                    "3. Flag dangerous commands that could modify or delete data\n"
                    "4. Provide clear, concise explanations\n"
                    "5. Use appropriate command flags for the current shell\n"
                )
            },
            {"role": "user", "content": user_input}
        ]

    def translate(self, user_input: str) -> Optional[TranslationResponse]:
        """
        Translate natural language input to a platform-appropriate command.
        
        Args:
            user_input: The natural language command description
            
        Returns:
            TranslationResponse object or None if translation fails
        """
        try:
            response = self.client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=self._create_prompt(user_input),
                temperature=0.2  # Lower temperature for more consistent outputs
            )
            
            # Parse and structure the response manually
            content = response.choices[0].message.content
            try:
                command_data = json.loads(content)
                # Format the response to match our schema
                structured_response = {
                    "command": {
                        "executable": command_data.get("executable", ""),
                        "args": command_data.get("args", []),
                        "is_dangerous": command_data.get("is_dangerous", False),
                        "explanation": command_data.get("explanation", ""),
                        "platform_specific": command_data.get("platform_specific", False)
                    },
                    "confidence": 1.0,  # Default confidence
                    "alternatives": []  # Empty alternatives list
                }
                return TranslationResponse(**structured_response)
                
            except json.JSONDecodeError as e:
                console.print("[red]Error parsing API response.[/red]")
                console.print(f"[yellow]Response content: {content}[/yellow]")
                return None

        except (APITimeoutError, APIConnectionError) as e:
            console.print("[red]Error connecting to OpenAI API.[/red]")
            console.print(f"[yellow]Details: {str(e)}[/yellow]")
            return None
            
        except APIError as e:
            console.print("[red]Error with OpenAI API request.[/red]")
            console.print(f"[yellow]Details: {str(e)}[/yellow]")
            return None
            
        except Exception as e:
            console.print("[red]Unexpected error during translation.[/red]")
            console.print(f"[yellow]Details: {str(e)}[/yellow]")
            return None

__all__ = ['CommandTranslator']
