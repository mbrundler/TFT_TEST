"""Screen capture module for capturing TFT game window"""

import mss
import numpy as np
from PIL import Image
from typing import Optional, Tuple
import cv2


class ScreenCapture:
    """Handles screen capture operations for the TFT game window"""

    def __init__(self):
        self.sct = mss.mss()
        self.game_window_bounds: Optional[dict] = None
        self.target_window_title = "League of Legends"

    def find_game_window(self) -> bool:
        """
        Attempt to find the TFT game window

        Returns:
            bool: True if window found, False otherwise
        """
        # For cross-platform compatibility, we'll start with full screen
        # On Windows, this could be enhanced with win32gui to find specific window
        # For now, we'll capture the primary monitor
        monitors = self.sct.monitors
        if len(monitors) > 1:
            self.game_window_bounds = monitors[1]  # Primary monitor
            return True
        return False

    def capture_screen(self) -> Optional[np.ndarray]:
        """
        Capture the current game screen

        Returns:
            np.ndarray: BGR image array (OpenCV format) or None if capture fails
        """
        if not self.game_window_bounds:
            if not self.find_game_window():
                return None

        try:
            # Capture screenshot
            screenshot = self.sct.grab(self.game_window_bounds)

            # Convert to numpy array and then to OpenCV BGR format
            img = np.array(screenshot)
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

            return img
        except Exception as e:
            print(f"Error capturing screen: {e}")
            return None

    def capture_region(self, x: int, y: int, width: int, height: int) -> Optional[np.ndarray]:
        """
        Capture a specific region of the screen

        Args:
            x: X coordinate of top-left corner
            y: Y coordinate of top-left corner
            width: Width of region
            height: Height of region

        Returns:
            np.ndarray: BGR image array or None if capture fails
        """
        try:
            region = {"top": y, "left": x, "width": width, "height": height}
            screenshot = self.sct.grab(region)

            img = np.array(screenshot)
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

            return img
        except Exception as e:
            print(f"Error capturing region: {e}")
            return None

    def get_screen_size(self) -> Tuple[int, int]:
        """
        Get the current screen/window size

        Returns:
            Tuple[int, int]: (width, height)
        """
        if self.game_window_bounds:
            return (
                self.game_window_bounds["width"],
                self.game_window_bounds["height"]
            )
        return (1920, 1080)  # Default resolution

    def save_capture(self, image: np.ndarray, filename: str):
        """Save captured image for debugging"""
        cv2.imwrite(filename, image)
