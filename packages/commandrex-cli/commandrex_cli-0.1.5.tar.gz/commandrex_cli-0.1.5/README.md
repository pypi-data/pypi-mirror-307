# CommandRex 🦖

A natural language interface for terminal commands. Talk to your terminal in plain English!

## Features

- 🗣️ Use natural language to run terminal commands
- 🔍 Preview commands before execution
- 🔒 Built-in safety checks for dangerous commands
- 💻 Cross-platform support (Windows, Linux, macOS)
- 📝 Command history with search
- ⌨️ Arrow key navigation
- 📊 Usage statistics

## Installation

```bash
pip install commandrex-cli
```

## Requirements

- Python 3.9 or higher
- OpenAI API key (get one at https://platform.openai.com)

## Quick Start

1. Install CommandRex:
```bash
pip install commandrex-cli
```

2. Run CommandRex:
```bash
commandrex
```

3. On first run, you'll be prompted to enter your OpenAI API key.

4. Start typing commands in plain English:
```
Show me all files in the current directory
Create a new folder called projects
What's my current directory
```

5. Update-
```
pip install --upgrade commandrex-cli
```

## Usage Tips

- Use arrow keys (↑/↓) to navigate command history
- Press Ctrl+R to search command history
- Type 'help' for more information
- Type 'history' to see command history
- Type 'stats' to see usage statistics
- Type 'exit' or 'quit' to leave

## Common Commands

Here are some example commands you can try:

- "Show all files"
- "Create a new folder called test"
- "What's my IP address"
- "Show system information"
- "Create a file called notes.txt"

## Safety Features

- Commands are shown and explained before execution
- Dangerous commands are flagged with warnings
- Confirmation required before execution
- Platform-specific command adaptation

## Special Commands

- `help` - Show help information
- `history` - Show command history
- `stats` - Show usage statistics
- `clear` - Clear the screen
- `reset-key` - Reset OpenAI API key
- `exit` or `quit` - Exit CommandRex

## Configuration

The OpenAI API key is stored securely using your system's keyring. You can:

1. Set it via environment variable:
```bash
export OPENAI_API_KEY=your-key-here
```

2. Let CommandRex prompt you for it on first run

3. Reset it anytime with:
```bash
commandrex reset-key
```

## License

MIT License - see LICENSE file for details.