#!/usr/bin/env python3

import socket
import argparse
import sys
from colorama import init, Fore, Style

init()

def validate_port(port):
    try:
        port_num = int(port)
        if 1 <= port_num <= 65535:
            return port_num
        else:
            raise ValueError(f"Port must be between 1 and 65535, got {port_num}")
    except ValueError:
        raise ValueError(f"Port must be a valid integer, got {port}")

def check_port(host, port, timeout=3):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    
    try:
        sock.connect((host, port))
        sock.close()
        return True
    except socket.timeout:
        return False, "Connection timed out"
    except ConnectionRefusedError:
        return False, "Connection refused"
    except socket.gaierror:
        return False, "Could not resolve hostname"
    except OSError as e:
        return False, str(e)
    except Exception as e:
        return False, f"An unexpected error occurred: {e}"

def main():
    parser = argparse.ArgumentParser(description='Check if a port is open on a specified host.')
    parser.add_argument('host', help='Host address (IP or domain name)')
    parser.add_argument('port', help='Port number (1-65535)')
    parser.add_argument('-t', '--timeout', type=float, default=3.0, 
                        help='Connection timeout in seconds (default: 3.0)')
    
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    
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