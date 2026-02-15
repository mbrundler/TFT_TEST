"""Main overlay window for TFT Meta Guide"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QPalette, QColor
from typing import Optional, List, Dict
from capture.screen_capture import ScreenCapture
from game_state.state_manager import GameStateManager
from recommendation.engine import RecommendationEngine


class TFTOverlay(QMainWindow):
    """Transparent overlay window for displaying TFT recommendations"""

    def __init__(
        self,
        screen_capture: ScreenCapture,
        state_manager: GameStateManager,
        recommendation_engine: RecommendationEngine
    ):
        super().__init__()

        self.screen_capture = screen_capture
        self.state_manager = state_manager
        self.recommendation_engine = recommendation_engine

        self.init_ui()
        self.setup_update_timer()

    def init_ui(self):
        """Initialize the overlay UI"""

        # Window setup - transparent overlay
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Set window size and position (top-right corner)
        self.setGeometry(1400, 50, 500, 800)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Create header
        self.header = self.create_header()
        main_layout.addWidget(self.header)

        # Create build recommendations panel
        self.build_panel = self.create_build_panel()
        main_layout.addWidget(self.build_panel)

        # Create shop recommendations panel
        self.shop_panel = self.create_shop_panel()
        main_layout.addWidget(self.shop_panel)

        # Create augment recommendations panel
        self.augment_panel = self.create_augment_panel()
        main_layout.addWidget(self.augment_panel)

        # Add spacer
        main_layout.addStretch()

    def create_header(self) -> QFrame:
        """Create header with app title and controls"""
        frame = self.create_panel_frame()
        layout = QHBoxLayout(frame)

        title = QLabel("TFT Meta Guide")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: #f0e6d2;")

        minimize_btn = QPushButton("_")
        minimize_btn.setFixedSize(30, 30)
        minimize_btn.clicked.connect(self.showMinimized)
        minimize_btn.setStyleSheet("""
            QPushButton {
                background-color: #1e2328;
                color: #f0e6d2;
                border: 1px solid #c89b3c;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #c89b3c;
            }
        """)

        close_btn = QPushButton("X")
        close_btn.setFixedSize(30, 30)
        close_btn.clicked.connect(self.close)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #1e2328;
                color: #f0e6d2;
                border: 1px solid #c89b3c;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #c84034;
            }
        """)

        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(minimize_btn)
        layout.addWidget(close_btn)

        return frame

    def create_build_panel(self) -> QFrame:
        """Create panel showing recommended builds and probabilities"""
        frame = self.create_panel_frame()
        layout = QVBoxLayout(frame)

        title = QLabel("Recommended Builds")
        title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        title.setStyleSheet("color: #c89b3c;")
        layout.addWidget(title)

        # Build list placeholder
        self.build_list_label = QLabel("Analyzing game state...")
        self.build_list_label.setWordWrap(True)
        self.build_list_label.setStyleSheet("color: #a09b8c; padding: 10px;")
        layout.addWidget(self.build_list_label)

        return frame

    def create_shop_panel(self) -> QFrame:
        """Create panel showing which champions to buy"""
        frame = self.create_panel_frame()
        layout = QVBoxLayout(frame)

        title = QLabel("Shop Priority")
        title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        title.setStyleSheet("color: #c89b3c;")
        layout.addWidget(title)

        self.shop_list_label = QLabel("Waiting for shop data...")
        self.shop_list_label.setWordWrap(True)
        self.shop_list_label.setStyleSheet("color: #a09b8c; padding: 10px;")
        layout.addWidget(self.shop_list_label)

        return frame

    def create_augment_panel(self) -> QFrame:
        """Create panel showing augment recommendations"""
        frame = self.create_panel_frame()
        layout = QVBoxLayout(frame)

        title = QLabel("Augment Priority")
        title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        title.setStyleSheet("color: #c89b3c;")
        layout.addWidget(title)

        self.augment_list_label = QLabel("Waiting for augment selection...")
        self.augment_list_label.setWordWrap(True)
        self.augment_list_label.setStyleSheet("color: #a09b8c; padding: 10px;")
        layout.addWidget(self.augment_list_label)

        return frame

    def create_panel_frame(self) -> QFrame:
        """Create a styled panel frame"""
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: rgba(16, 26, 33, 230);
                border: 2px solid #c89b3c;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        return frame

    def setup_update_timer(self):
        """Setup timer for periodic screen capture and analysis"""
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_recommendations)
        self.update_timer.start(1000)  # Update every second

    def update_recommendations(self):
        """Update recommendations based on current game state"""
        # Capture screen
        screen = self.screen_capture.capture_screen()

        if screen is None:
            return

        # Analyze game state
        game_state = self.state_manager.analyze_screen(screen)

        if game_state is None:
            return

        # Get recommendations
        recommendations = self.recommendation_engine.get_recommendations(game_state)

        # Update UI
        self.update_build_display(recommendations.get("builds", []))
        self.update_shop_display(recommendations.get("shop", []))
        self.update_augment_display(recommendations.get("augments", []))

    def update_build_display(self, builds: List[Dict]):
        """Update build recommendations display"""
        if not builds:
            self.build_list_label.setText("Analyzing possible builds...")
            return

        build_text = ""
        for i, build in enumerate(builds[:3], 1):
            name = build.get("name", "Unknown")
            probability = build.get("probability", 0)
            tier = build.get("tier", "?")
            contested = build.get("contested", 0)

            color = self.get_tier_color(tier)
            build_text += f"{i}. <span style='color: {color};'>{name}</span><br>"
            build_text += f"   Win Rate: {probability:.1f}% | Tier: {tier}"
            if contested > 0:
                build_text += f" | ⚠️ {contested} contesting"
            build_text += "<br><br>"

        self.build_list_label.setText(build_text)

    def update_shop_display(self, shop_recommendations: List[Dict]):
        """Update shop recommendations display"""
        if not shop_recommendations:
            self.shop_list_label.setText("No shop recommendations")
            return

        shop_text = ""
        for i, champ in enumerate(shop_recommendations[:5], 1):
            name = champ.get("name", "Unknown")
            priority = champ.get("priority", "medium")
            reason = champ.get("reason", "")

            color = self.get_priority_color(priority)
            shop_text += f"<span style='color: {color};'>{'★' * self.priority_to_stars(priority)}</span> "
            shop_text += f"{name}"
            if reason:
                shop_text += f"<br>   <span style='color: #7f7f7f; font-size: 10px;'>{reason}</span>"
            shop_text += "<br>"

        self.shop_list_label.setText(shop_text)

    def update_augment_display(self, augment_recommendations: List[Dict]):
        """Update augment recommendations display"""
        if not augment_recommendations:
            self.augment_list_label.setText("No augment selection available")
            return

        augment_text = ""
        for i, augment in enumerate(augment_recommendations[:3], 1):
            name = augment.get("name", "Unknown")
            score = augment.get("score", 0)
            synergy = augment.get("synergy", "")

            augment_text += f"{i}. {name} ({score:.1f}/10)<br>"
            if synergy:
                augment_text += f"   <span style='color: #a09b8c; font-size: 10px;'>{synergy}</span><br>"
            augment_text += "<br>"

        self.augment_list_label.setText(augment_text)

    def get_tier_color(self, tier: str) -> str:
        """Get color for tier rating"""
        colors = {
            "S": "#ff7eb3",
            "A": "#00d4ff",
            "B": "#00ff9f",
            "C": "#f0e6d2",
            "D": "#7f7f7f"
        }
        return colors.get(tier, "#f0e6d2")

    def get_priority_color(self, priority: str) -> str:
        """Get color for priority level"""
        colors = {
            "critical": "#ff4655",
            "high": "#ff7eb3",
            "medium": "#00d4ff",
            "low": "#a09b8c"
        }
        return colors.get(priority, "#f0e6d2")

    def priority_to_stars(self, priority: str) -> int:
        """Convert priority to star count"""
        stars = {
            "critical": 5,
            "high": 4,
            "medium": 3,
            "low": 2
        }
        return stars.get(priority, 3)

    def mousePressEvent(self, event):
        """Enable dragging the window"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        """Handle window dragging"""
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()
