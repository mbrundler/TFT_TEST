#!/usr/bin/env python3
"""
Diagnostic script to check OCR setup and screen capture
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

def check_ocr():
    """Check if OCR engines are available"""
    print("=" * 60)
    print("OCR Engine Diagnostics")
    print("=" * 60)

    # Check EasyOCR
    print("\n1. Checking EasyOCR...")
    try:
        import easyocr
        print("   ✅ EasyOCR package installed")
        try:
            reader = easyocr.Reader(['en'], gpu=False)
            print("   ✅ EasyOCR reader initialized successfully")

            # Test with simple text
            import numpy as np
            from PIL import Image, ImageDraw, ImageFont

            # Create test image with text
            img = Image.new('RGB', (200, 50), color='white')
            draw = ImageDraw.Draw(img)
            draw.text((10, 10), "Tristana", fill='black')

            test_img = np.array(img)
            results = reader.readtext(test_img)

            if results:
                print(f"   ✅ EasyOCR test successful: {results}")
            else:
                print("   ⚠️  EasyOCR returned no results")

        except Exception as e:
            print(f"   ❌ EasyOCR initialization failed: {e}")
    except ImportError:
        print("   ❌ EasyOCR not installed")

    # Check Tesseract
    print("\n2. Checking Tesseract...")
    try:
        import pytesseract
        version = pytesseract.get_tesseract_version()
        print(f"   ✅ Tesseract installed (version: {version})")
    except Exception as e:
        print(f"   ❌ Tesseract not available: {e}")

    # Check config
    print("\n3. Checking config...")
    try:
        import config
        print(f"   OCR Engine: {config.OCR_ENGINE}")
        print(f"   OCR Languages: {config.OCR_LANGUAGES}")
        print(f"   Confidence Threshold: {config.OCR_CONFIDENCE_THRESHOLD}")
        print(f"   Debug Mode: {config.DEBUG_MODE}")
        print(f"   Save Screenshots: {config.SAVE_SCREENSHOTS}")
    except Exception as e:
        print(f"   ❌ Error loading config: {e}")

def check_screen_capture():
    """Test screen capture"""
    print("\n" + "=" * 60)
    print("Screen Capture Test")
    print("=" * 60)

    try:
        from capture.screen_capture import ScreenCapture

        capture = ScreenCapture()
        print("\n✅ ScreenCapture initialized")

        screen = capture.capture_screen()
        if screen is not None:
            print(f"✅ Screen captured: {screen.shape}")

            # Save test capture
            import cv2
            cv2.imwrite("debug_capture.png", screen)
            print(f"✅ Test screenshot saved: debug_capture.png")
        else:
            print("❌ Screen capture failed")

    except Exception as e:
        print(f"❌ Screen capture error: {e}")
        import traceback
        traceback.print_exc()

def check_game_state_manager():
    """Test game state manager"""
    print("\n" + "=" * 60)
    print("Game State Manager Test")
    print("=" * 60)

    try:
        from game_state.state_manager import GameStateManager

        print("\nInitializing GameStateManager...")
        manager = GameStateManager()
        print("✅ GameStateManager initialized")

        # Check if OCR engine is initialized
        if hasattr(manager, 'ocr_engine'):
            print(f"✅ OCR engine: {type(manager.ocr_engine).__name__}")
        else:
            print("❌ OCR engine not initialized")

        if hasattr(manager, 'champion_recognizer'):
            print(f"✅ Champion recognizer: {type(manager.champion_recognizer).__name__}")
        else:
            print("❌ Champion recognizer not initialized")

    except Exception as e:
        print(f"❌ GameStateManager error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_ocr()
    check_screen_capture()
    check_game_state_manager()

    print("\n" + "=" * 60)
    print("Diagnostic Complete")
    print("=" * 60)
