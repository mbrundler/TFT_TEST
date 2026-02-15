"""Game state manager for analyzing and tracking TFT game state"""

from typing import Optional, Dict, List
from dataclasses import dataclass, field
import numpy as np


@dataclass
class GameState:
    """Represents the current state of a TFT game"""

    # Player state
    gold: int = 0
    level: int = 1
    hp: int = 100
    stage: str = "1-1"

    # Board state
    board_champions: List[str] = field(default_factory=list)
    bench_champions: List[str] = field(default_factory=list)
    items_on_board: Dict[str, List[str]] = field(default_factory=dict)
    items_on_bench: List[str] = field(default_factory=list)

    # Shop state
    shop_champions: List[str] = field(default_factory=list)
    shop_visible: bool = False

    # Augment state
    augments_available: List[str] = field(default_factory=list)
    augments_selected: List[str] = field(default_factory=list)
    augment_selection_active: bool = False

    # Carousel state
    carousel_items: List[str] = field(default_factory=list)
    carousel_active: bool = False

    # Opponent tracking
    opponent_boards: Dict[str, List[str]] = field(default_factory=dict)

    # Champion pool tracking
    champion_pool: Dict[str, int] = field(default_factory=dict)


class GameStateManager:
    """Manages game state detection and tracking"""

    def __init__(self):
        self.current_state: Optional[GameState] = None
        self.previous_state: Optional[GameState] = None

    def analyze_screen(self, screen: np.ndarray) -> Optional[GameState]:
        """
        Analyze screen capture and extract game state

        Args:
            screen: BGR image array from screen capture

        Returns:
            GameState object or None if analysis fails
        """
        # Save previous state
        self.previous_state = self.current_state

        # Create new state
        state = GameState()

        # Detect which screen/phase we're in
        screen_type = self.detect_screen_type(screen)

        if screen_type == "shop":
            state.shop_visible = True
            self.extract_shop_state(screen, state)
            self.extract_player_stats(screen, state)
            self.extract_board_state(screen, state)

        elif screen_type == "augment":
            state.augment_selection_active = True
            self.extract_augment_options(screen, state)

        elif screen_type == "carousel":
            state.carousel_active = True
            self.extract_carousel_items(screen, state)

        elif screen_type == "planning":
            self.extract_opponent_boards(screen, state)
            self.extract_player_stats(screen, state)

        # Update current state
        self.current_state = state

        return state

    def detect_screen_type(self, screen: np.ndarray) -> str:
        """
        Detect which game screen/phase is currently active

        Args:
            screen: BGR image array

        Returns:
            String indicating screen type: 'shop', 'augment', 'carousel', 'planning', 'combat'
        """
        # TODO: Implement screen detection using template matching or color detection
        # For now, default to shop
        return "shop"

    def extract_player_stats(self, screen: np.ndarray, state: GameState):
        """Extract player stats (gold, level, HP, stage)"""
        # TODO: Implement OCR for player stats
        # These are typically in fixed positions on screen
        pass

    def extract_shop_state(self, screen: np.ndarray, state: GameState):
        """Extract current shop champions"""
        # TODO: Implement champion detection in shop
        # Shop is typically at bottom center of screen
        # Use template matching or OCR to identify champions
        pass

    def extract_board_state(self, screen: np.ndarray, state: GameState):
        """Extract current board and bench state"""
        # TODO: Implement board detection
        # Board area is in lower portion of screen
        # Bench is at very bottom
        pass

    def extract_augment_options(self, screen: np.ndarray, state: GameState):
        """Extract available augment options"""
        # TODO: Implement augment detection
        # Augments appear as large icons in center of screen
        pass

    def extract_carousel_items(self, screen: np.ndarray, state: GameState):
        """Extract carousel item options"""
        # TODO: Implement carousel detection
        pass

    def extract_opponent_boards(self, screen: np.ndarray, state: GameState):
        """Extract visible opponent board compositions"""
        # TODO: Implement opponent board detection
        # During planning phase, opponent boards are visible
        pass

    def update_champion_pool(self, state: GameState):
        """
        Update champion pool tracking based on visible boards

        TFT has a shared champion pool. Track what's taken to calculate
        probabilities and contested units.
        """
        # TODO: Implement pool tracking
        # Each champion tier has specific pool sizes
        # Subtract visible champions from total pool
        pass
