#!/usr/bin/env python3
# The line above allows this to run as an executable on Linux/Mac

import re
import os
import platform
import subprocess
import sys
from datetime import datetime

# Configuration
INVENTORY_FILE = 'inventory.txt'
LOG_FILE = 'network_log.txt'

def get_ping_param():
    """
    Determines the correct ping flag based on the OS.
    Returns '-n' for Windows, '-c' for Linux/Mac.
    """
    return '-n' if platform.system().lower() == 'windows' else '-c'

def ping_ip(ip):
    """
    Pings an IP address once and returns status (is_success, latency_ms)
    """
    param = get_ping_param()
    command = ['ping', param, '1', '-w', '1000', ip]  # Added -w 1000 (1 sec timeout)
    
    try:
        # Run the command and CAPTURE the text output
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if result.returncode != 0:
            return False, 0

        # REGEX: Look for "time=" followed by digits
        match = re.search(r'time[=<]([\d.]+)', result.stdout)
        
        if match:
            return True, float(match.group(1))
        else:
            return True, 0
            
    except Exception:
        return False, 0

def main():
    
    # Enable ANSI escape codes on Windows
    if platform.system().lower() == 'windows':
        os.system('')  
    
    # Record start time
    start_time = datetime.now()
    start_timestamp = f"{start_time.strftime('%Y-%m-%d %H:%M:%S')}.{start_time.microsecond // 1000:03d}"
    
    print("-" * 40)
    print(f"Starting Network Health Check at {start_timestamp}")
    print("-" * 40)

    # Load Inventory
    try:
        with open(INVENTORY_FILE, 'r') as file:
            ip_list = file.read().splitlines()
    except FileNotFoundError:
        print(f"\033[91mERROR: '{INVENTORY_FILE}' not found.\033[0m")
        print("Please create the file and add one IP address per line.")
        sys.exit(1)

    # Initialize counters
    up_count = 0
    down_count = 0
    total_hosts = 0   

    # Start Scan
    try:
        with open(LOG_FILE, 'a') as log:
            for ip in ip_list:
                if not ip.strip():  
                    continue

                total_hosts += 1
                
                # Refresh time for each host
                now = datetime.now()
                current_timestamp = f"{now.strftime('%Y-%m-%d %H:%M:%S')}.{now.microsecond // 1000:03d}"

                is_alive, latency = ping_ip(ip)

                # Logic Tree
                if is_alive:
                    up_count += 1
                    if latency > 100:
                        status = f"SLOW ({latency}ms)"
                        color = "\033[93m" # Yellow
                    else:
                        status = f"UP ({latency}ms)"
                        color = "\033[92m" # Green
                else:
                    down_count += 1
                    status = "DOWN"
                    color = "\033[91m" # Red

                # Output to Screen and Log
                print(f"[{current_timestamp}] {ip}: {color}{status}\033[0m")
                log.write(f"[{current_timestamp}] {ip} is {status}\n")
                
    except IOError as e:
        print(f"\033[91mERROR: Could not open log file '{LOG_FILE}': {e}\033[0m")

    # Record end time
    end_time = datetime.now()
    end_timestamp = f"{end_time.strftime('%Y-%m-%d %H:%M:%S')}.{end_time.microsecond // 1000:03d}"

    # Summary Report
    print("-" * 40)
    print("SUMMARY REPORT")
    print("-" * 40)
    print(f"Total Hosts Scanned: {total_hosts}")
    print(f"Hosts UP:   \033[92m{up_count}\033[0m")
    print(f"Hosts DOWN: \033[91m{down_count}\033[0m")
    
    success_rate = (up_count / total_hosts * 100) if total_hosts > 0 else 0
    print(f"Success Rate: {success_rate:.2f}%")
    print(f"Scan completed at {end_timestamp}")
    print("-" * 40)
    
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
