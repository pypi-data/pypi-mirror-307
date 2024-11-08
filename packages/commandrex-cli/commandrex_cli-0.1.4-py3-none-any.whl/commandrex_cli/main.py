"""Main entry point for CommandRex CLI."""

import sys
from typing import Optional

from .config import Config
from .translator import CommandTranslator
from .executor import CommandExecutor
from .ui import CommandRexUI

def setup_api_key() -> bool:
    """
    Setup OpenAI API key if not already configured.
    
    Returns:
        bool: True if setup was successful
    """
    api_key = Config.get_api_key()
    if not api_key:
        ui = CommandRexUI()
        ui.display_warning("OpenAI API key not found!")
        
        try:
            while True:
                api_key = ui.get_user_input("\n[cyan]Please enter your OpenAI API key: [/cyan]").strip()
                
                if not api_key:
                    ui.display_error("API key cannot be empty")
                    continue
                    
                if Config.validate_api_key(api_key):
                    Config.save_api_key(api_key)
                    return True
                else:
                    retry = ui.get_user_input(
                        "\n[yellow]API key format seems invalid. "
                        "Do you want to try again? (y/N): [/yellow]"
                    ).lower()
                    if retry != 'y':
                        return False
                    
        except (KeyboardInterrupt, EOFError):
            return False
    return True

def handle_command(ui: CommandRexUI, translator: CommandTranslator, 
                  executor: CommandExecutor, user_input: str) -> bool:
    """
    Handle a single command.
    
    Args:
        ui: UI instance
        translator: Translator instance
        executor: Executor instance
        user_input: User's command
        
    Returns:
        bool: True if should continue, False if should exit
    """
    # Handle special commands
    cmd_lower = user_input.lower()
    if not cmd_lower:
        return True
    elif cmd_lower in ['exit', 'quit']:
        ui.console.print("[info]Goodbye! 👋[/info]")
        return False
    elif cmd_lower == 'help':
        ui.show_help()
        return True
    elif cmd_lower == 'clear':
        ui.clear_screen()
        return True
    elif cmd_lower == 'history':
        ui.display_history()
        return True
    elif cmd_lower == 'stats':
        ui.display_statistics()
        return True
    elif cmd_lower == 'reset-key':
        Config.remove_api_key()
        if not setup_api_key():
            ui.display_error("Failed to set up new API key")
        return True
    
    # Translate command
    translation = translator.translate(user_input)
    if not translation:
        ui.display_error("Failed to translate command. Please try again.")
        return True
    
    # Display translation and get confirmation
    if ui.display_translation(translation):
        # Execute command
        translated_cmd = f"{translation.command.executable} {' '.join(translation.command.args)}"
        result = executor.execute(translation.command)
        ui.display_result(result)
        
        # Add to history
        ui.add_to_history(user_input, translated_cmd, result.success)
    
    return True

def main():
    """Main entry point for CommandRex CLI."""
    ui = CommandRexUI()
    
    # Show welcome message
    ui.clear_screen()
    ui.show_welcome()
    
    # Check for API key
    if not setup_api_key():
        ui.display_error("Failed to set up API key. Please try again.")
        sys.exit(1)
    
    try:
        # Initialize components
        translator = CommandTranslator()
        executor = CommandExecutor()
        
        while True:
            # Get user input
            user_input = ui.get_user_input().strip()
            
            # Handle the command
            if not handle_command(ui, translator, executor, user_input):
                break
    
    except KeyboardInterrupt:
        ui.console.print("\n[info]Interrupted by user. Goodbye! 👋[/info]")
    except Exception as e:
        ui.display_error(f"Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()