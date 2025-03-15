import socket

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
