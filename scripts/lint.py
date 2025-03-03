#!/usr/bin/env python
"""
Lint script for Netgsm Python SDK.
"""

import sys
import subprocess
from pathlib import Path

def run_command(cmd):
    """Run a command and return its exit code."""
    try:
        if cmd[0] == 'black' or cmd[0] == 'flake8':
            # Run tools as Python modules
            subprocess.run([sys.executable, '-m'] + cmd, check=True)
        else:
            subprocess.run(cmd, check=True)
        return 0
    except subprocess.CalledProcessError as e:
        print(f"Error running command {' '.join(cmd)}: {e}")
        return e.returncode

def lint_directory(directory):
    """Run flake8 and black on a directory."""
    print(f"\nLinting {directory}...")
    
    # Run flake8
    flake8_result = run_command(['flake8', directory])
    if flake8_result != 0:
        return flake8_result
        
    # Run black
    black_result = run_command(['black', '--check', directory])
    return black_result

def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: python lint.py [directory]")
        return 1
        
    directory = sys.argv[1]
    if not Path(directory).exists():
        print(f"Directory {directory} does not exist")
        return 1
        
    return lint_directory(directory)

if __name__ == '__main__':
    sys.exit(main()) 