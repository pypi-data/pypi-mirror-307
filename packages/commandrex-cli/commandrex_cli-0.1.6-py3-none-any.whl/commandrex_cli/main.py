"""Main entry point for CommandRex CLI."""

import sys
import os
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

def reset_terminal():
    """Reset terminal state."""
    try:
        # Force two newlines and flush
        sys.stdout.write('\n\n')
        sys.stdout.flush()
        
        # On Windows, try to reset console mode
        if os.name == 'nt':
            try:
                import msvcrt
                import ctypes
                kernel32 = ctypes.WinDLL('kernel32')
                kernel32.SetConsoleMode(msvcrt.get_osfhandle(1), 7)
            except:
                pass
                
        # Move cursor to start of line and clear it
        if sys.stdout.isatty():
            sys.stdout.write('\r\033[K')
            sys.stdout.flush()
    except Exception:
        # Fallback for terminals that don't support ANSI
        print("\n")

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
    try:
        # Handle special commands
        cmd_lower = user_input.lower()
        if not cmd_lower:
            return True
        elif cmd_lower in ['exit', 'quit']:
            ui.console.print("[info]Goodbye! 👋[/info]")
            return False
        elif cmd_lower == 'help':
            ui.show_help()
            reset_terminal()  # Add explicit reset
            return True
        elif cmd_lower == 'clear':
            ui.clear_screen()
            return True
        elif cmd_lower == 'history':
            ui.display_history()
            reset_terminal()  # Add explicit reset
            return True
        elif cmd_lower == 'stats':
            ui.display_statistics()
            reset_terminal()  # Add explicit reset
            return True
        elif cmd_lower == 'reset-key':
            Config.remove_api_key()
            if not setup_api_key():
                ui.display_error("Failed to set up new API key")
            reset_terminal()  # Add explicit reset
            return True
        
        # Translate command
        translation = translator.translate(user_input)
        if not translation:
            ui.display_error("Failed to translate command. Please try again.")
            reset_terminal()  # Add explicit reset
            return True
        
        # Display translation and get confirmation
        if ui.display_translation(translation):
            # Execute command
            translated_cmd = f"{translation.command.executable} {' '.join(translation.command.args)}"
            result = executor.execute(translation.command)
            ui.display_result(result)
            
            # Add to history
            ui.add_to_history(user_input, translated_cmd, result.success)
            
            # Reset terminal state after command execution
            reset_terminal()
            
            # Force display of new prompt
            ui.reset_prompt()
        else:
            reset_terminal()  # Add reset for cancelled commands
        
        return True
        
    except Exception as e:
        ui.display_error(f"Error handling command: {str(e)}")
        reset_terminal()  # Add explicit reset
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
            try:
                # Get user input using the input handler
                user_input = ui.input_handler.get_input(
                    f"[path]{os.getcwd()}[/path]\nCommandRex 🦖 > "
                ).strip()
                
                # Handle the command
                if not handle_command(ui, translator, executor, user_input):
                    break
                
            except KeyboardInterrupt:
                ui.console.print("\n[info]Command interrupted.[/info]")
                continue
            except Exception as e:
                ui.display_error(f"Unexpected error: {str(e)}")
                continue
    
    except KeyboardInterrupt:
        ui.console.print("\n[info]Interrupted by user. Goodbye! 👋[/info]")
    except Exception as e:
        ui.display_error(f"Unexpected error: {str(e)}")
        sys.exit(1)
    finally:
        # Cleanup resources
        ui.cleanup()

if __name__ == "__main__":
    main()