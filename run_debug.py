#!/usr/bin/env python3
"""
Debug launcher for TFT Meta Guide with OCR visualization

This script runs the app in debug mode with:
- Screenshot saving enabled
- Verbose OCR output
- Performance monitoring
"""

import os
import sys
from pathlib import Path

# Enable debug mode
os.environ["DEBUG"] = "true"

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def main():
    """Main debug launcher"""
    print("=" * 60)
    print("TFT Meta Guide - DEBUG MODE")
    print("=" * 60)
    print()
    print("🔧 Debug features enabled:")
    print("  ✓ Screenshot saving (./debug/screenshots/)")
    print("  ✓ Verbose OCR output")
    print("  ✓ Detection logging")
    print()
    print("📺 Testing with YouTube:")
    print("  1. Open a TFT gameplay video on YouTube (fullscreen)")
    print("  2. Position the overlay to the side")
    print("  3. Watch the console for OCR detections")
    print()
    print("💡 Tips:")
    print("  - Use recent TFT gameplay videos")
    print("  - Pause on shop screens for best detection")
    print("  - Check ./debug/screenshots/ to see what's being captured")
    print("  - Look for '🛒 Detected in shop' messages")
    print()
    print("=" * 60)
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
