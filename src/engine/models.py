"""Data models for TFT recommendation engine"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum


class Priority(Enum):
    """Priority levels for recommendations"""
    CRITICAL = 4
    HIGH = 3
    MEDIUM = 2
    LOW = 1
    AVOID = 0


class Stage(Enum):
    """TFT game stages"""
    STAGE_1 = "1"
    STAGE_2 = "2"
    STAGE_3 = "3"
    STAGE_4 = "4"
    STAGE_5 = "5"
    STAGE_6 = "6"
    STAGE_7 = "7"

    @property
    def is_early(self) -> bool:
        return self.value in ["1", "2", "3"]

    @property
    def is_mid(self) -> bool:
        return self.value in ["3", "4", "5"]

    @property
    def is_late(self) -> bool:
        return self.value in ["5", "6", "7"]


@dataclass
class Champion:
    """Represents a TFT champion"""
    name: str
    cost: int
    traits: List[str]
    is_carry: bool = False
    is_core: bool = False
    current_stars: int = 1
    count: int = 0  # How many owned

    @property
    def pool_size(self) -> int:
        """Total champions in pool by cost"""
        pool_sizes = {1: 29, 2: 22, 3: 18, 4: 12, 5: 10}
        return pool_sizes.get(self.cost, 10)

    def can_upgrade(self) -> bool:
        """Check if can upgrade to next star level"""
        required = {1: 3, 2: 9}  # 3 for 2-star, 9 for 3-star
        return self.count >= required.get(self.current_stars, 999)


@dataclass
class Item:
    """Represents a TFT item"""
    name: str
    components: List[str]
    stats: Dict[str, float]
    best_on: List[str] = field(default_factory=list)  # Champions


@dataclass
class Augment:
    """Represents a TFT augment"""
    name: str
    tier: str  # S, A, B, C, D
    boosts_trait: Optional[str] = None
    boosts_champions: List[str] = field(default_factory=list)
    effect_type: str = "general"  # general, trait, champion, economic

    def synergy_score(self, active_traits: List[str], champions: List[str]) -> float:
        """Calculate synergy with current board"""
        score = 0.0

        # Trait synergy
        if self.boosts_trait and self.boosts_trait in active_traits:
            score += 5.0

        # Champion synergy
        for champ in self.boosts_champions:
            if champ in champions:
                score += 3.0

        return min(score, 10.0)  # Cap at 10


@dataclass
class Composition:
    """Represents a TFT team composition"""
    name: str
    tier: str  # S, A, B, C, D
    champions: List[Champion]
    core_champions: List[str]  # Names of key units
    carry_units: List[str]  # Names of carry units
    items: Dict[str, List[str]]  # champion_name -> [item_names]
    traits: List[str]
    win_rate: float
    play_rate: float
    avg_placement: float
    patch: str
    best_stages: List[str] = field(default_factory=lambda: ["mid"])

    @property
    def is_early_comp(self) -> bool:
        return "early" in self.best_stages

    @property
    def is_mid_comp(self) -> bool:
        return "mid" in self.best_stages

    @property
    def is_late_comp(self) -> bool:
        return "late" in self.best_stages

    def tier_score(self) -> float:
        """Convert tier to numeric score"""
        tier_map = {"S": 100, "A": 80, "B": 60, "C": 40, "D": 20}
        return tier_map.get(self.tier, 40)

    def get_champion_by_name(self, name: str) -> Optional[Champion]:
        """Find champion in comp by name"""
        for champ in self.champions:
            if champ.name == name:
                return champ
        return None


@dataclass
class Board:
    """Represents current player board"""
    champions: List[Champion]
    bench: List[Champion]
    items: List[str]  # Held item components/completed items
    active_traits: Dict[str, int]  # trait_name -> tier (e.g., "Sniper": 2)

    def get_champion_count(self, champion_name: str) -> int:
        """Count total copies of a champion"""
        count = 0
        for champ in self.champions + self.bench:
            if champ.name == champion_name:
                count += champ.count
        return count

    def has_champion(self, champion_name: str) -> bool:
        """Check if board has champion"""
        return any(c.name == champion_name for c in self.champions + self.bench)

    def get_all_champion_names(self) -> List[str]:
        """Get list of all champion names on board"""
        return [c.name for c in self.champions + self.bench]

    @property
    def total_units(self) -> int:
        """Total units on board (not bench)"""
        return len(self.champions)


@dataclass
class GameState:
    """Represents current game state"""
    stage: Stage
    round_num: int  # e.g., 3 (for stage 3-2)
    level: int
    gold: int
    health: int
    board: Board
    opponent_boards: Dict[str, Board]  # opponent_name -> Board
    shop: List[Champion]  # Current shop champions
    available_augments: List[Augment] = field(default_factory=list)

    @property
    def can_afford_reroll(self) -> bool:
        """Check if player can afford to reroll"""
        return self.gold >= 2

    @property
    def should_save_gold(self) -> bool:
        """Check if player should save gold for interest"""
        return self.gold < 50 and (self.gold % 10) >= 8

    @property
    def can_level(self) -> bool:
        """Check if player can afford to level up"""
        level_costs = {4: 4, 5: 4, 6: 12, 7: 20, 8: 36, 9: 48}
        return self.gold >= level_costs.get(self.level, 999)

    def stage_progress(self) -> float:
        """Calculate game progress (0.0 to 1.0)"""
        stage_num = int(self.stage.value)
        return min((stage_num - 1) / 6, 1.0)


@dataclass
class Recommendation:
    """Represents a recommendation with reasoning"""
    item_name: str  # Champion, augment, or comp name
    item_type: str  # "champion", "augment", "composition"
    priority: Priority
    score: float
    reasoning: List[str]  # Human-readable reasons
    metadata: Dict = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert to dict for JSON serialization"""
        return {
            "name": self.item_name,
            "type": self.item_type,
            "priority": self.priority.name,
            "score": round(self.score, 2),
            "reasoning": self.reasoning,
            "metadata": self.metadata
        }


@dataclass
class BuildRecommendation:
    """Detailed build recommendation"""
    composition: Composition
    viability_score: float
    probability: float  # 0-100
    owned_champions: int  # How many champs already owned
    contest_count: int  # How many opponents running it
    reasoning: List[str]
    next_steps: List[str]  # What to do next

    def to_dict(self) -> Dict:
        """Convert to dict for JSON"""
        return {
            "name": self.composition.name,
            "tier": self.composition.tier,
            "viability_score": round(self.viability_score, 2),
            "probability": round(self.probability, 1),
            "owned_champions": self.owned_champions,
            "contest_count": self.contest_count,
            "reasoning": self.reasoning,
            "next_steps": self.next_steps,
            "champions": [c.name for c in self.composition.champions],
            "traits": self.composition.traits,
            "items": self.composition.items
        }
