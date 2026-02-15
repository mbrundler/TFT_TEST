"""Recommendation engine for TFT builds, champions, and augments"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from game_state.state_manager import GameState
from recommendation.meta_data import MetaDataService


@dataclass
class BuildRecommendation:
    """Represents a recommended team composition"""
    name: str
    champions: List[str]
    traits: List[str]
    carry_items: Dict[str, List[str]]
    tier: str  # S, A, B, C, D
    win_rate: float
    play_rate: float
    probability: float  # How achievable based on current state
    contested: int  # Number of opponents running similar comp


@dataclass
class ChampionRecommendation:
    """Represents a champion purchase recommendation"""
    name: str
    priority: str  # critical, high, medium, low
    reason: str
    cost: int
    builds: List[str]  # Which builds this champion fits


@dataclass
class AugmentRecommendation:
    """Represents an augment selection recommendation"""
    name: str
    score: float  # 0-10 rating for current situation
    synergy: str  # How it synergizes with current board
    tier: str


class RecommendationEngine:
    """Generates recommendations based on game state and meta data"""

    def __init__(self):
        self.meta_service = MetaDataService()
        self.current_build_path: Optional[str] = None

    def get_recommendations(self, game_state: GameState) -> Dict:
        """
        Generate all recommendations for current game state

        Args:
            game_state: Current game state

        Returns:
            Dict containing builds, shop, augments, carousel recommendations
        """
        recommendations = {
            "builds": self.recommend_builds(game_state),
            "shop": self.recommend_shop_purchases(game_state),
            "augments": self.recommend_augments(game_state),
            "carousel": self.recommend_carousel_item(game_state)
        }

        return recommendations

    def recommend_builds(self, game_state: GameState) -> List[Dict]:
        """
        Recommend possible team compositions

        Args:
            game_state: Current game state

        Returns:
            List of build recommendations sorted by probability
        """
        meta_comps = self.meta_service.get_top_comps()

        recommendations = []

        for comp in meta_comps[:10]:
            # Calculate probability based on:
            # 1. Current champions owned
            # 2. Items available
            # 3. Stage of game
            # 4. Champion pool availability
            probability = self.calculate_build_probability(comp, game_state)

            # Check if build is contested
            contested = self.count_contested(comp, game_state)

            # Adjust probability based on contest level
            adjusted_probability = probability * (1 - (contested * 0.15))

            recommendations.append({
                "name": comp["name"],
                "champions": comp["champions"],
                "tier": comp["tier"],
                "probability": adjusted_probability,
                "contested": contested,
                "items": comp.get("items", {}),
                "traits": comp.get("traits", [])
            })

        # Sort by adjusted probability
        recommendations.sort(key=lambda x: x["probability"], reverse=True)

        return recommendations

    def recommend_shop_purchases(self, game_state: GameState) -> List[Dict]:
        """
        Recommend which champions to buy from shop

        Args:
            game_state: Current game state

        Returns:
            List of champion recommendations sorted by priority
        """
        if not game_state.shop_visible or not game_state.shop_champions:
            return []

        recommendations = []
        top_builds = self.recommend_builds(game_state)

        if not top_builds:
            return []

        # Focus on top 3 most probable builds
        for champ in game_state.shop_champions:
            priority = "low"
            reason = ""
            builds_for_champ = []

            # Check if champion is needed for any top builds
            for build in top_builds[:3]:
                if champ in build["champions"]:
                    builds_for_champ.append(build["name"])

                    # Check current board state
                    current_count = game_state.board_champions.count(champ)
                    current_count += game_state.bench_champions.count(champ)

                    # Determine priority based on how core the unit is
                    if current_count == 0:
                        priority = "high"
                        reason = f"Core unit for {build['name']}"
                    elif current_count == 1:
                        priority = "high"
                        reason = f"1-star upgrade for {build['name']}"
                    elif current_count == 2:
                        priority = "critical"
                        reason = f"⭐⭐ 2-star upgrade!"

            if builds_for_champ:
                recommendations.append({
                    "name": champ,
                    "priority": priority,
                    "reason": reason,
                    "builds": builds_for_champ,
                    "cost": self.meta_service.get_champion_cost(champ)
                })

        # Sort by priority
        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        recommendations.sort(key=lambda x: priority_order[x["priority"]])

        return recommendations

    def recommend_augments(self, game_state: GameState) -> List[Dict]:
        """
        Recommend augment selections

        Args:
            game_state: Current game state

        Returns:
            List of augment recommendations sorted by score
        """
        if not game_state.augment_selection_active:
            return []

        recommendations = []
        top_builds = self.recommend_builds(game_state)

        for augment in game_state.augments_available:
            score = self.calculate_augment_score(
                augment,
                game_state,
                top_builds
            )

            synergy = self.get_augment_synergy(augment, game_state, top_builds)

            recommendations.append({
                "name": augment,
                "score": score,
                "synergy": synergy,
                "tier": self.meta_service.get_augment_tier(augment)
            })

        recommendations.sort(key=lambda x: x["score"], reverse=True)

        return recommendations

    def recommend_carousel_item(self, game_state: GameState) -> Optional[Dict]:
        """
        Recommend which carousel item to pick

        Args:
            game_state: Current game state

        Returns:
            Item recommendation or None
        """
        if not game_state.carousel_active:
            return None

        top_builds = self.recommend_builds(game_state)

        if not top_builds:
            return None

        # Get priority items for top build
        target_build = top_builds[0]
        needed_items = self.get_needed_items(target_build, game_state)

        # Find best carousel option
        for item in game_state.carousel_items:
            if item in needed_items:
                return {
                    "item": item,
                    "reason": f"Needed for {target_build['name']}",
                    "priority": "high"
                }

        return None

    def calculate_build_probability(
        self,
        comp: Dict,
        game_state: GameState
    ) -> float:
        """Calculate probability of successfully pivoting to a composition"""
        # TODO: Implement sophisticated probability calculation
        # Consider:
        # - Champions already owned
        # - Stage of game
        # - Gold available
        # - Items available vs. needed
        # - Champion pool availability

        return 50.0  # Placeholder

    def count_contested(self, comp: Dict, game_state: GameState) -> int:
        """Count how many opponents are running similar composition"""
        # TODO: Implement contest detection
        # Compare opponent boards to this comp's core units
        return 0  # Placeholder

    def calculate_augment_score(
        self,
        augment: str,
        game_state: GameState,
        top_builds: List[Dict]
    ) -> float:
        """Score an augment for the current situation"""
        # TODO: Implement augment scoring
        # Consider synergy with:
        # - Current board
        # - Target builds
        # - Items available
        return 5.0  # Placeholder

    def get_augment_synergy(
        self,
        augment: str,
        game_state: GameState,
        top_builds: List[Dict]
    ) -> str:
        """Describe how augment synergizes with current state"""
        # TODO: Implement synergy description
        return "Good with current board"

    def get_needed_items(
        self,
        build: Dict,
        game_state: GameState
    ) -> List[str]:
        """Get list of items still needed for a build"""
        # TODO: Implement item tracking
        return []
