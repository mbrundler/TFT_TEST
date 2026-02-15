#!/usr/bin/env python3
"""
Launcher script for TFT Meta Guide

This script provides a simple way to launch the application with proper error handling.
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = [
        "PyQt6",
        "cv2",
        "numpy",
        "PIL",
        "mss",
        "requests"
    ]

    missing = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)

    if missing:
        print("❌ Missing required packages:")
        for pkg in missing:
            print(f"   - {pkg}")
        print("\nPlease install dependencies with:")
        print("   pip install -r requirements.txt")
        return False

    return True


def main():
    """Main launcher function"""
    print("=" * 50)
    print("TFT Meta Guide - Starting...")
    print("=" * 50)

    # Check dependencies
    if not check_dependencies():
        sys.exit(1)

    print("✅ All dependencies found")
    print("🚀 Launching overlay...")
    print()
    print("Tips:")
    print("  - Make sure TFT is running")
    print("  - Drag the overlay to reposition it")
    print("  - Press minimize to hide temporarily")
    print()

    # Import and run main application
    try:
        from main import main as app_main
        app_main()
    except Exception as e:
        print(f"\n❌ Error launching application: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
