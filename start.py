#!/usr/bin/env python
"""Cross-platform startup script for Django server."""
import os
import sys
import platform
import subprocess
from pathlib import Path

def is_windows():
    """Check if running on Windows."""
    return platform.system() == 'Windows'

def venv_exists():
    """Check if virtual environment exists."""
    venv_path = Path('venv')
    if is_windows():
        return (venv_path / 'Scripts' / 'python.exe').exists()
    else:
        return (venv_path / 'bin' / 'python').exists()

def create_venv():
    """Create virtual environment if it doesn't exist."""
    print("Creating virtual environment...")
    subprocess.run([sys.executable, '-m', 'venv', 'venv'], check=True)
    print("Virtual environment created successfully!")

def get_venv_python():
    """Get the path to the venv Python interpreter."""
    venv_path = Path('venv')
    if is_windows():
        return venv_path / 'Scripts' / 'python.exe'
    else:
        return venv_path / 'bin' / 'python'

def run_server():
    """Run the Django development server."""
    # Check/create venv
    if not venv_exists():
        create_venv()
    else:
        print("Virtual environment found!")
    
    # Get venv Python
    venv_python = get_venv_python()
    
    # Build command
    if is_windows():
        cmd = [str(venv_python), 'manage.py', 'runserver', '192.168.1.7:8000']
        print("Starting server on Windows at 192.168.1.7:8000...")
    else:
        cmd = [str(venv_python), 'manage.py', 'runserver']
        print("Starting server on Linux...")
    
    # Run the server
    subprocess.run(cmd)

if __name__ == '__main__':
    run_server()

