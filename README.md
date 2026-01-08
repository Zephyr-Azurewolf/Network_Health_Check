# Network_Health_Check
# Python Network Health Monitor

A lightweight, cross-platform CLI tool for automated network status checks. 
This script reads from a local inventory file, checks connectivity via ICMP (Ping), and generates timestamped logs.

## Features
- **Cross-Platform:** Automatically detects OS (Windows/Linux) to adjust system commands.
- **Latency Detection:** Flags connections as "SLOW" (Yellow) if latency exceeds 100ms.
- **Visual Feedback:** Uses ANSI escape codes for real-time color-coded terminal output.
- **Audit Logging:** Appends all results to `network_log.txt` for historical analysis.
- **Regex Parsing:** Utilizes regular expressions to parse raw system output.

## Usage

1. **Create Inventory File:**
   Create a file named `inventory.txt` in the same directory. Add one IP address or hostname per line.
   ```text
   8.8.8.8
   192.168.1.1
   10.0.0.50
