"""Game state manager for analyzing and tracking TFT game state"""

from typing import Optional, Dict, List
from dataclasses import dataclass, field
import numpy as np
import cv2
import config
from utils.ocr import get_ocr_engine, ChampionNameRecognizer


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

        # Initialize OCR engine
        print("🔍 Initializing OCR engine...")
        self.ocr_engine = get_ocr_engine()
        self.champion_recognizer = ChampionNameRecognizer(self.ocr_engine)
        print("✅ OCR engine ready")

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

        print(f"\n🎮 Analyzing screen (type: {screen_type})")

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

        # Save debug screenshot if enabled
        if config.SAVE_SCREENSHOTS:
            import time
            timestamp = int(time.time())
            screenshot_path = config.SCREENSHOT_DIR / f"capture_{timestamp}.png"
            cv2.imwrite(str(screenshot_path), screen)
            print(f"  📸 Screenshot saved: {screenshot_path}")

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
        try:
            height, width = screen.shape[:2]

            # Extract gold (bottom left area)
            gold_config = config.SCREEN_REGIONS.get("gold")
            if gold_config:
                x = int(width * gold_config["x_ratio"])
                y = int(height * gold_config["y_ratio"])
                w = int(width * gold_config["width_ratio"])
                h = int(height * gold_config["height_ratio"])

                gold_region = screen[y:y+h, x:x+w]

                # Use OCR to detect gold amount
                gold_text = self.ocr_engine.read_text(gold_region)
                if gold_text:
                    # Try to extract number from text
                    for text, confidence in gold_text:
                        # Look for digits
                        import re
                        numbers = re.findall(r'\d+', text)
                        if numbers:
                            state.gold = int(numbers[0])
                            print(f"  💰 Detected gold: {state.gold}")
                            break

            # Extract level
            level_config = config.SCREEN_REGIONS.get("level")
            if level_config:
                x = int(width * level_config["x_ratio"])
                y = int(height * level_config["y_ratio"])
                w = int(width * level_config["width_ratio"])
                h = int(height * level_config["height_ratio"])

                level_region = screen[y:y+h, x:x+w]

                level_text = self.ocr_engine.read_text(level_region)
                if level_text:
                    import re
                    for text, confidence in level_text:
                        numbers = re.findall(r'\d+', text)
                        if numbers:
                            state.level = int(numbers[0])
                            print(f"  📊 Detected level: {state.level}")
                            break

        except Exception as e:
            print(f"Error extracting player stats: {e}")

    def extract_shop_state(self, screen: np.ndarray, state: GameState):
        """Extract current shop champions"""
        try:
            # Get shop region based on screen size
            height, width = screen.shape[:2]
            shop_config = config.SCREEN_REGIONS["shop"]

            # Calculate actual coordinates
            x = int(width * shop_config["x_ratio"])
            y = int(height * shop_config["y_ratio"])
            w = int(width * shop_config["width_ratio"])
            h = int(height * shop_config["height_ratio"])

            # Extract shop region
            shop_region = screen[y:y+h, x:x+w]

            # Divide shop into 5 champion slots (TFT shop has 5 slots)
            slot_width = w // 5
            champions = []

            for i in range(5):
                slot_x = i * slot_width
                champion_slot = shop_region[:, slot_x:slot_x+slot_width]

                # Use OCR to detect champion name
                champion_name = self.champion_recognizer.recognize_champion(champion_slot)

                if champion_name:
                    champions.append(champion_name)
                    print(f"  🛒 Detected in shop slot {i+1}: {champion_name}")

            state.shop_champions = champions

            if config.DEBUG_MODE and champions:
                print(f"  📋 Total champions in shop: {champions}")

        except Exception as e:
            print(f"Error extracting shop state: {e}")
            import traceback
            traceback.print_exc()

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
