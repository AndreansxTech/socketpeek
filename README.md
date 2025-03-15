# SocketPeek

A little something made for the Terminalcraft event from Hackclub. Made using Python

## Installation

### Development Installation

1. Clone this repository:
```
git clone https://github.com/AndreansxTech/socketpeek.git
cd socketpeek
```

2. Install in development mode:
```
pip install -e .
```

### Regular Installation

You can install directly from the repository:
```
pip install git+https://github.com/AndreansxTech/socketpeek.git
```

## Usage

### Text User Interface (TUI)

Simply run the command without arguments to launch the interactive interface:
```
socketpeek
```

The TUI provides a user-friendly interface where you can:
- Enter the host (IP or domain name)
- Specify the port number
- Set the connection timeout
- Check the connection with a button press

### Command Line Interface (CLI)

You can also use the tool from the command line:
```
socketpeek <host> <port> [options]
```

Examples:
```
socketpeek google.com 80
socketpeek 192.168.1.1 22
socketpeek example.com 443 --timeout 5
```

### Options

- `<host>`: The host address (IP or domain name)
- `<port>`: The port number (1-65535)
- `-t, --timeout`: Optional. Connection timeout in seconds (default: 3.0)
- `-h, --help`: Show help message

## Features

- Text-based user interface for interactive use
- Command-line interface for scripting and quick checks
- Color-coded output for better readability
- Detailed error messages
- Configurable connection timeout

## Requirements

- Python 3.6+
- colorama
- textual
