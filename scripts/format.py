#!/usr/bin/env python
"""
Format script for Netgsm Python SDK.
"""

import sys
import subprocess
from pathlib import Path

def run_command(cmd):
    """Run a command and return its exit code."""
    try:
        if cmd[0] == 'black':
            # Run black as a Python module
            subprocess.run([sys.executable, '-m'] + cmd, check=True)
        else:
            subprocess.run(cmd, check=True)
        return 0
    except subprocess.CalledProcessError as e:
        print(f"Error running command {' '.join(cmd)}: {e}")
        return e.returncode

def format_directory(directory):
    """Run black on a directory."""
    print(f"\nFormatting {directory}...")
    return run_command(['black', directory])

def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: python format.py [directory]")
        return 1
        
    directory = sys.argv[1]
    if not Path(directory).exists():
        print(f"Directory {directory} does not exist")
        return 1
        
    return format_directory(directory)

if __name__ == '__main__':
    sys.exit(main()) 