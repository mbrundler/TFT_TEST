"""Game state analyzer - analyzes current board and game state"""

from typing import List, Dict, Tuple
from .models import GameState, Board, Composition, Champion


class GameStateAnalyzer:
    """Analyzes game state and calculates various metrics"""

    def analyze_board_strength(self, game_state: GameState) -> float:
        """
        Calculate current board strength (0-100 scale)

        Factors:
        - Champion stars and costs
        - Active trait synergies
        - Item completion
        """
        score = 0.0

        # Factor 1: Champion value (40% weight)
        champion_value = self._calculate_champion_value(game_state.board)
        score += champion_value * 0.40

        # Factor 2: Trait synergies (35% weight)
        trait_value = self._calculate_trait_value(game_state.board)
        score += trait_value * 0.35

        # Factor 3: Item value (25% weight)
        item_value = self._calculate_item_value(game_state.board)
        score += item_value * 0.25

        return min(score, 100)

    def _calculate_champion_value(self, board: Board) -> float:
        """Calculate value from champions (0-100)"""
        total_value = 0.0

        for champ in board.champions:
            # Base value by cost
            base_value = champ.cost * 10

            # Multiply by stars
            star_multiplier = {1: 1.0, 2: 2.5, 3: 5.0}
            value = base_value * star_multiplier.get(champ.current_stars, 1.0)

            total_value += value

        # Normalize to 0-100 (assuming ~8 units, avg cost 3, 2-star)
        max_expected = 8 * 30 * 2.5  # 600
        return min((total_value / max_expected) * 100, 100)

    def _calculate_trait_value(self, board: Board) -> float:
        """Calculate value from trait synergies (0-100)"""
        if not board.active_traits:
            return 0.0

        total_value = 0.0

        # Trait tier values
        tier_values = {1: 10, 2: 20, 3: 35, 4: 50, 5: 65}

        for trait, tier in board.active_traits.items():
            total_value += tier_values.get(tier, 0)

        # Normalize (assuming ~3 active traits at tier 2-3)
        max_expected = 3 * 35  # 105
        return min((total_value / max_expected) * 100, 100)

    def _calculate_item_value(self, board: Board) -> float:
        """Calculate value from items (0-100)"""
        # Count completed items (not components)
        completed_items = [item for item in board.items if len(item) > 15]

        # Ideal: 3 items per carry, 2 carries = 6 items
        ideal_items = 6
        return min((len(completed_items) / ideal_items) * 100, 100)

    def identify_pivot_potential(
        self,
        game_state: GameState,
        target_comp: Composition
    ) -> float:
        """
        Calculate how easily player can pivot to target comp (0-100)

        Factors:
        - Champions already owned
        - Gold available
        - Stage timing
        - Items alignment
        - Bench space
        """
        score = 0.0

        # Factor 1: Owned champions (30% weight)
        owned_score = self._calculate_owned_champions_score(
            game_state.board,
            target_comp
        )
        score += owned_score * 0.30

        # Factor 2: Gold availability (25% weight)
        gold_score = self._calculate_gold_score(game_state, target_comp)
        score += gold_score * 0.25

        # Factor 3: Stage timing (20% weight)
        stage_score = self._calculate_stage_score(game_state, target_comp)
        score += stage_score * 0.20

        # Factor 4: Items alignment (15% weight)
        item_score = self._calculate_item_alignment(game_state, target_comp)
        score += item_score * 0.15

        # Factor 5: Bench space (10% weight)
        bench_score = self._calculate_bench_score(game_state)
        score += bench_score * 0.10

        return min(score, 100)

    def _calculate_owned_champions_score(
        self,
        board: Board,
        target_comp: Composition
    ) -> float:
        """Score based on how many comp champions already owned"""
        owned_count = 0
        core_owned = 0

        owned_names = board.get_all_champion_names()

        for champ in target_comp.champions:
            if champ.name in owned_names:
                owned_count += 1
                if champ.name in target_comp.core_champions:
                    core_owned += 1

        # Weight core champions more heavily
        total_champs = len(target_comp.champions)
        core_champs = len(target_comp.core_champions)

        if total_champs == 0:
            return 0

        # 60% weight on core, 40% on total
        core_pct = (core_owned / core_champs * 100) if core_champs > 0 else 0
        total_pct = (owned_count / total_champs * 100)

        return (core_pct * 0.6) + (total_pct * 0.4)

    def _calculate_gold_score(self, game_state: GameState, target_comp: Composition) -> float:
        """Score based on gold available"""
        # Estimate cost to complete comp
        owned_names = game_state.board.get_all_champion_names()
        needed_champs = [
            c for c in target_comp.champions
            if c.name not in owned_names
        ]

        # Rough estimate: 10 gold per missing unit
        estimated_cost = len(needed_champs) * 10

        # Plus rolling cost
        estimated_cost += 20  # ~10 rerolls

        if game_state.gold >= estimated_cost:
            return 100
        else:
            return (game_state.gold / estimated_cost) * 100

    def _calculate_stage_score(self, game_state: GameState, target_comp: Composition) -> float:
        """Score based on stage timing"""
        stage_num = int(game_state.stage.value)

        # Early comps good in stages 1-3
        if target_comp.is_early_comp:
            if stage_num <= 3:
                return 100
            else:
                return max(0, 100 - (stage_num - 3) * 30)

        # Mid comps good in stages 3-5
        if target_comp.is_mid_comp:
            if 3 <= stage_num <= 5:
                return 100
            elif stage_num < 3:
                return 70  # A bit early but okay
            else:
                return max(0, 100 - (stage_num - 5) * 20)

        # Late comps good in stages 5+
        if target_comp.is_late_comp:
            if stage_num >= 5:
                return 100
            else:
                return max(0, (stage_num / 5) * 100)

        return 50  # Default

    def _calculate_item_alignment(self, game_state: GameState, target_comp: Composition) -> float:
        """Score based on having correct items"""
        # Get items needed for comp
        needed_items = set()
        for items in target_comp.items.values():
            needed_items.update(items)

        if not needed_items:
            return 50  # No specific items needed

        # Check how many we have
        owned_items = set(game_state.board.items)
        matching_items = needed_items.intersection(owned_items)

        return (len(matching_items) / len(needed_items)) * 100

    def _calculate_bench_score(self, game_state: GameState) -> float:
        """Score based on bench space"""
        bench_size = len(game_state.board.bench)
        max_bench = 9

        # More space = better for pivoting
        available_space = max_bench - bench_size
        return (available_space / max_bench) * 100

    def detect_current_traits(self, board: Board) -> Dict[str, int]:
        """
        Identify active traits on board

        Returns:
            Dict mapping trait name to tier level
        """
        trait_counts = {}

        # Count champions per trait
        for champ in board.champions:
            for trait in champ.traits:
                trait_counts[trait] = trait_counts.get(trait, 0) + 1

        # Convert counts to tiers (simplified - would need actual breakpoints)
        active_traits = {}
        for trait, count in trait_counts.items():
            tier = self._count_to_tier(count)
            if tier > 0:
                active_traits[trait] = tier

        return active_traits

    def _count_to_tier(self, count: int) -> int:
        """Convert champion count to trait tier (simplified)"""
        if count >= 7:
            return 5
        elif count >= 5:
            return 4
        elif count >= 4:
            return 3
        elif count >= 3:
            return 2
        elif count >= 2:
            return 1
        else:
            return 0

    def calculate_champion_overlap(
        self,
        board1: Board,
        board2: Board,
        core_champions: List[str] = None
    ) -> float:
        """
        Calculate overlap between two boards (0.0 to 1.0)

        Args:
            board1: First board
            board2: Second board
            core_champions: If provided, only check these champions

        Returns:
            Overlap ratio (1.0 = identical, 0.0 = no overlap)
        """
        champs1 = set(board1.get_all_champion_names())
        champs2 = set(board2.get_all_champion_names())

        if core_champions:
            champs1 = champs1.intersection(set(core_champions))
            champs2 = champs2.intersection(set(core_champions))

        if not champs1 and not champs2:
            return 0.0

        overlap = champs1.intersection(champs2)
        total_unique = champs1.union(champs2)

        return len(overlap) / len(total_unique) if total_unique else 0.0

    def count_contested(
        self,
        game_state: GameState,
        target_comp: Composition,
        threshold: float = 0.6
    ) -> int:
        """
        Count how many opponents are contesting the comp

        Args:
            game_state: Current game state
            target_comp: Composition to check
            threshold: Overlap threshold to consider "contested" (default 60%)

        Returns:
            Number of opponents running similar comp
        """
        contest_count = 0

        for opponent_board in game_state.opponent_boards.values():
            overlap = self.calculate_champion_overlap(
                game_state.board,
                opponent_board,
                core_champions=target_comp.core_champions
            )

            if overlap >= threshold:
                contest_count += 1

        return contest_count

    def should_eco_or_roll(self, game_state: GameState) -> Tuple[str, str]:
        """
        Decide whether to eco (save gold) or roll (reroll shop)

        Returns:
            Tuple of (decision, reasoning)
        """
        # Critical health - must roll to stabilize
        if game_state.health <= 30:
            return ("roll", "Critical health - need to stabilize board")

        # Strong board + good economy - eco
        board_strength = self.analyze_board_strength(game_state)
        if board_strength >= 70 and game_state.gold < 50:
            return ("eco", "Strong board - save for interest")

        # Late game - roll to find upgrades
        stage_num = int(game_state.stage.value)
        if stage_num >= 5 and game_state.level >= 7:
            return ("roll", "Late game - roll for upgrades")

        # Weak board - roll to improve
        if board_strength < 50:
            return ("roll", "Weak board - roll to improve")

        # Default: eco
        return ("eco", "Save gold for interest")
