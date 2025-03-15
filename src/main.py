#!/usr/bin/env python3

import argparse
import sys
from colorama import init, Fore, Style
from .utils import check_port, validate_port

init()

def main():
    if len(sys.argv) == 1:
        from .tui import main as tui_main
        tui_main()
        return

    parser = argparse.ArgumentParser(description='Check if a port is open on a specified host.')
    parser.add_argument('host', help='Host address (IP or domain name)')
    parser.add_argument('port', help='Port number (1-65535)')
    parser.add_argument('-t', '--timeout', type=float, default=3.0, 
                        help='Connection timeout in seconds (default: 3.0)')
    
    args = parser.parse_args()
    
    try:
        port = validate_port(args.port)
    except ValueError as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        sys.exit(1)
    
    result = check_port(args.host, port, args.timeout)
    
    if isinstance(result, tuple):
        is_open, error_msg = False, result[1]
        print(f"{Fore.RED}Port {port} on {args.host} is CLOSED: {error_msg}.{Style.RESET_ALL}")
    elif result:
        print(f"{Fore.GREEN}Port {port} on {args.host} is OPEN.{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Port {port} on {args.host} is CLOSED.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()