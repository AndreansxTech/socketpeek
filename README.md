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

After installation, you can use the command directly:
```
socketpeek <host> <port>
```

If you prefer to run it without installation:
```
python src/main.py <host> <port>
```

Examples:
```
socketpeek google.com 80
socketpeek 192.168.1.1 22
socketpeek example.com 443 --timeout 5
```

### Options

- `<host>`: Required. The host address (IP or domain name)
- `<port>`: Required. The port number (1-65535)
- `-t, --timeout`: Optional. Connection timeout in seconds (default: 3.0)
- `-h, --help`: Show help message

## Features

- Simple command-line interface
- Color-coded output (green for open ports, red for closed ports)
- Detailed error messages
- Configurable connection timeout

## Requirements

- Python 3.6+
- colorama
