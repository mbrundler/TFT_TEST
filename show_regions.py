#!/usr/bin/env python3
"""
Visual region debugger - shows what areas the app is capturing
"""

import sys
from pathlib import Path
import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).parent / "src"))

import config
from capture.screen_capture import ScreenCapture

def draw_regions():
    """Capture screen and draw rectangles showing detection regions"""

    print("=" * 60)
    print("Region Visualization Tool")
    print("=" * 60)

    # Capture screen
    capture = ScreenCapture()
    screen = capture.capture_screen()

    if screen is None:
        print("❌ Failed to capture screen")
        return

    height, width = screen.shape[:2]
    print(f"\n📺 Screen resolution: {width}x{height}")

    # Create a copy to draw on
    annotated = screen.copy()

    # Draw each region
    regions_to_draw = {
        "shop": (0, 255, 0),      # Green
        "gold": (255, 0, 0),      # Blue
        "level": (0, 255, 255),   # Yellow
        "board": (255, 0, 255),   # Magenta
        "bench": (0, 165, 255)    # Orange
    }

    print("\n🎨 Drawing regions:")

    for region_name, color in regions_to_draw.items():
        if region_name not in config.SCREEN_REGIONS:
            continue

        region_config = config.SCREEN_REGIONS[region_name]

        x = int(width * region_config["x_ratio"])
        y = int(height * region_config["y_ratio"])
        w = int(width * region_config["width_ratio"])
        h = int(height * region_config["height_ratio"])

        # Draw rectangle
        cv2.rectangle(annotated, (x, y), (x+w, y+h), color, 3)

        # Add label
        label = f"{region_name.upper()}"
        cv2.putText(annotated, label, (x, y-10),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        print(f"  {region_name:10s}: x={x:4d}, y={y:4d}, w={w:4d}, h={h:4d} - {color}")

    # Save annotated image
    output_path = "region_visualization.png"
    cv2.imwrite(output_path, annotated)

    print(f"\n✅ Saved visualization: {output_path}")
    print(f"\n📝 Legend:")
    print(f"  🟢 Green  = Shop region")
    print(f"  🔵 Blue   = Gold region")
    print(f"  🟡 Yellow = Level region")
    print(f"  🟣 Magenta= Board region")
    print(f"  🟠 Orange = Bench region")
    print(f"\nOpen '{output_path}' to see if regions are correct!")

    # Also save just the shop region
    shop_config = config.SCREEN_REGIONS["shop"]
    x = int(width * shop_config["x_ratio"])
    y = int(height * shop_config["y_ratio"])
    w = int(width * shop_config["width_ratio"])
    h = int(height * shop_config["height_ratio"])

    shop_region = screen[y:y+h, x:x+w]
    cv2.imwrite("shop_region_extracted.png", shop_region)
    print(f"✅ Saved shop region: shop_region_extracted.png")

if __name__ == "__main__":
    draw_regions()
