"""Configuration settings for TFT Meta Guide"""

import os
from pathlib import Path

# Application Settings
APP_NAME = "TFT Meta Guide"
VERSION = "0.1.0"

# Paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "src" / "data"
CACHE_DIR = DATA_DIR / "cache"
TEMPLATES_DIR = DATA_DIR / "templates"

# Screen Capture Settings
CAPTURE_FPS = 1  # Captures per second
SCREEN_CAPTURE_DELAY = 1000  # Milliseconds between captures

# UI Settings
OVERLAY_WIDTH = 500
OVERLAY_HEIGHT = 800
OVERLAY_OPACITY = 0.9
OVERLAY_DEFAULT_POSITION = (1400, 50)

# Game Detection Settings
GAME_WINDOW_TITLE = "League of Legends"
SCREEN_REGIONS = {
    "shop": {
        "x_ratio": 0.2,
        "y_ratio": 0.75,
        "width_ratio": 0.6,
        "height_ratio": 0.2
    },
    "gold": {
        "x_ratio": 0.05,
        "y_ratio": 0.92,
        "width_ratio": 0.1,
        "height_ratio": 0.05
    },
    "level": {
        "x_ratio": 0.15,
        "y_ratio": 0.92,
        "width_ratio": 0.05,
        "height_ratio": 0.05
    },
    "board": {
        "x_ratio": 0.25,
        "y_ratio": 0.45,
        "width_ratio": 0.5,
        "height_ratio": 0.25
    },
    "bench": {
        "x_ratio": 0.25,
        "y_ratio": 0.7,
        "width_ratio": 0.5,
        "height_ratio": 0.08
    }
}

# OCR Settings
OCR_ENGINE = "easyocr"  # or "tesseract"
OCR_LANGUAGES = ["en"]
OCR_CONFIDENCE_THRESHOLD = 0.1  # Lowered for EasyOCR (0.1-0.3 is normal for game text)

# Meta Data Settings
META_UPDATE_INTERVAL = 21600  # 6 hours in seconds
META_API_ENDPOINTS = {
    "tactics_tools": "https://tactics.tools/api",
    "metatft": "https://www.metatft.com/api"
}

# Champion Pool Sizes (per tier)
CHAMPION_POOL_SIZES = {
    1: 29,  # 29 copies of each 1-cost
    2: 22,  # 22 copies of each 2-cost
    3: 18,  # 18 copies of each 3-cost
    4: 12,  # 12 copies of each 4-cost
    5: 10   # 10 copies of each 5-cost
}

# Recommendation Settings
MAX_BUILD_RECOMMENDATIONS = 5
MAX_SHOP_RECOMMENDATIONS = 5
MAX_AUGMENT_RECOMMENDATIONS = 3

# Debug Settings
DEBUG_MODE = os.getenv("DEBUG", "false").lower() in ("true", "1", "yes")
SAVE_SCREENSHOTS = DEBUG_MODE
SCREENSHOT_DIR = BASE_DIR / "debug" / "screenshots"

# Print debug status on import
if DEBUG_MODE:
    print(f"🔧 DEBUG MODE ENABLED")

# Create directories
for directory in [DATA_DIR, CACHE_DIR, TEMPLATES_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

if SAVE_SCREENSHOTS:
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
