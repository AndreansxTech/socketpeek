import socket
import time
import subprocess
import platform
import re
import sys

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

def traceroute(host, max_hops=30, timeout=1):
    """
    Perform a traceroute to the specified host.
    
    Args:
        host (str): The target hostname or IP address
        max_hops (int): Maximum number of hops to trace
        timeout (float): Timeout in seconds for each hop
        
    Returns:
        list: List of dictionaries with hop information
    """
    os_name = platform.system().lower()
    
    try:
        socket.gethostbyname(host)
        
        if os_name == "windows":
            return _traceroute_windows(host, max_hops, timeout)
        elif os_name in ["linux", "darwin"]: 
            return _traceroute_unix(host, max_hops, timeout)
        else:
            return [{"hop": 0, "ip": None, "hostname": None, "time": None, 
                    "error": f"Unsupported operating system: {os_name}"}]
    except socket.gaierror:
        return [{"hop": 0, "ip": None, "hostname": None, "time": None, 
                "error": f"Could not resolve hostname: {host}"}]
    except Exception as e:
        return [{"hop": 0, "ip": None, "hostname": None, "time": None, 
                "error": f"Error during traceroute: {str(e)}"}]

def _traceroute_windows(host, max_hops, timeout):
    timeout_ms = int(timeout * 1000)
    result = []
    
    try:
        cmd = ['tracert', '-d', '-h', str(max_hops), '-w', str(timeout_ms), host]
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        
        skip_count = 0
        for line in process.stdout:
            skip_count += 1
            if "Tracing route" in line:
                break
            if skip_count > 5: 
                break
        
        hop_num = 0
        for line in process.stdout:
            line = line.strip()
            
            if not line:
                continue
            
            if line[0].isdigit():
                hop_num = int(line.split()[0])
                

                if "Request timed out" in line:
                    result.append({
                        "hop": hop_num,
                        "ip": None,
                        "hostname": None,
                        "time": None,
                        "error": "Request timed out"
                    })
                    continue
                
                ip_match = re.search(r'(\d+\.\d+\.\d+\.\d+)', line)
                ip = ip_match.group(1) if ip_match else None
                
                times = re.findall(r'(\d+) ms', line)
                avg_time = sum(int(t) for t in times) / len(times) if times else None
                
                hostname = None
                if ip:
                    try:
                        hostname = socket.gethostbyaddr(ip)[0]
                    except:
                        hostname = ip
                
                result.append({
                    "hop": hop_num,
                    "ip": ip,
                    "hostname": hostname,
                    "time": avg_time,
                    "error": None if ip else "No response"
                })
        
        process.terminate()
        return result
    except subprocess.SubprocessError as e:
        return [{"hop": 0, "ip": None, "hostname": None, "time": None, 
                "error": f"Error running tracert: {str(e)}"}]

def _traceroute_unix(host, max_hops, timeout):
    result = []
    
    try:
        cmd = ['traceroute', '-n', '-m', str(max_hops), '-w', str(timeout), host]
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        
        next(process.stdout)
        
        for line in process.stdout:
            line = line.strip()
            match = re.search(r'^\s*(\d+)\s+(?:(\d+\.\d+\.\d+\.\d+)|(\*))', line)
            
            if not match:
                continue
                
            hop = int(match.group(1))
            ip = match.group(2) if match.group(2) else None
            
            times = re.findall(r'(\d+\.\d+) ms', line)
            avg_time = sum(float(t) for t in times) / len(times) if times else None
            
            hostname = None
            if ip:
                try:
                    hostname = socket.gethostbyaddr(ip)[0]
                except:
                    hostname = ip
            
            result.append({
                "hop": hop,
                "ip": ip,
                "hostname": hostname,
                "time": avg_time,
                "error": "No response" if not ip else None
            })
        
        process.terminate()
        return result
    except FileNotFoundError:
        return _traceroute_ping_fallback(host, max_hops, timeout)
    except subprocess.SubprocessError as e:
        return [{"hop": 0, "ip": None, "hostname": None, "time": None, 
                "error": f"Error running traceroute: {str(e)}"}]

def _traceroute_ping_fallback(host, max_hops, timeout):
    result = []
    
    for ttl in range(1, max_hops + 1):
        if platform.system().lower() == "darwin":
            cmd = ['ping', '-c', '1', '-t', str(ttl), '-W', str(int(timeout * 1000)), host]
        else:
            cmd = ['ping', '-c', '1', '-t', str(ttl), '-W', str(int(timeout)), host]
        
        try:
            output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, universal_newlines=True)
            
            dest_reached = False
            ip = None
            time_ms = None
            
            ip_match = re.search(r'from (\d+\.\d+\.\d+\.\d+)', output)
            if ip_match:
                ip = ip_match.group(1)
                
                time_match = re.search(r'time=(\d+\.\d+) ms', output)
                if time_match:
                    time_ms = float(time_match.group(1))
                
                if ip == socket.gethostbyname(host):
                    dest_reached = True
            
            hostname = None
            if ip:
                try:
                    hostname = socket.gethostbyaddr(ip)[0]
                except:
                    hostname = ip
            
            result.append({
                "hop": ttl,
                "ip": ip,
                "hostname": hostname,
                "time": time_ms,
                "error": None
            })
            
            if dest_reached:
                break
                
        except subprocess.CalledProcessError as e:
            if "Time to live exceeded" in e.output:
                ip_match = re.search(r'from (\d+\.\d+\.\d+\.\d+)', e.output)
                ip = ip_match.group(1) if ip_match else None
                
                hostname = None
                if ip:
                    try:
                        hostname = socket.gethostbyaddr(ip)[0]
                    except:
                        hostname = ip
                
                result.append({
                    "hop": ttl,
                    "ip": ip,
                    "hostname": hostname,
                    "time": None,
                    "error": None
                })
            else:
                result.append({
                    "hop": ttl,
                    "ip": None,
                    "hostname": None,
                    "time": None,
                    "error": "Request timed out"
                })
    
    return result
