"""Main entry point for TFT Meta Guide application"""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from ui.overlay import TFTOverlay
from capture.screen_capture import ScreenCapture
from game_state.state_manager import GameStateManager
from recommendation.engine import RecommendationEngine


def main():
    """Initialize and run the TFT Meta Guide application"""

    # Enable high DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(sys.argv)
    app.setApplicationName("TFT Meta Guide")

    # Initialize core components
    screen_capture = ScreenCapture()
    game_state_manager = GameStateManager()
    recommendation_engine = RecommendationEngine()

    # Create and show overlay
    overlay = TFTOverlay(
        screen_capture=screen_capture,
        state_manager=game_state_manager,
        recommendation_engine=recommendation_engine
    )
    overlay.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
