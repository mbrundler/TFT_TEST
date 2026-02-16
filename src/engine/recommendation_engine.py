"""Main recommendation engine - combines all analyzers to make recommendations"""

from typing import List, Dict
from .models import (
    GameState, Composition, Champion, Augment,
    Recommendation, BuildRecommendation, Priority
)
from .game_analyzer import GameStateAnalyzer


class ProbabilityEngine:
    """Calculates probability of successfully executing strategies"""

    def __init__(self):
        self.analyzer = GameStateAnalyzer()

    def calculate_build_probability(
        self,
        comp: Composition,
        game_state: GameState
    ) -> float:
        """
        Multi-factor probability calculation (0-100 scale)

        Factors:
        - Meta strength (30%)
        - Board synergy (25%)
        - Stage appropriateness (20%)
        - Resource availability (15%)
        - Item alignment (10%)
        """
        # Factor 1: Meta Strength (30%)
        meta_score = comp.tier_score()  # S=100, A=80, B=60, C=40, D=20

        # Factor 2: Board Synergy (25%)
        synergy_score = self.analyzer.identify_pivot_potential(game_state, comp)

        # Factor 3: Stage Appropriateness (20%)
        stage_score = self._stage_multiplier(game_state, comp)

        # Factor 4: Resource Availability (15%)
        resource_score = self._resource_score(game_state, comp)

        # Factor 5: Item Alignment (10%)
        item_score = self.analyzer._calculate_item_alignment(game_state, comp)

        final_score = (
            meta_score * 0.30 +
            synergy_score * 0.25 +
            stage_score * 0.20 +
            resource_score * 0.15 +
            item_score * 0.10
        )

        return min(final_score, 100)

    def _stage_multiplier(self, game_state: GameState, comp: Composition) -> float:
        """Calculate stage appropriateness score"""
        return self.analyzer._calculate_stage_score(game_state, comp)

    def _resource_score(self, game_state: GameState, comp: Composition) -> float:
        """Calculate resource availability score"""
        return self.analyzer._calculate_gold_score(game_state, comp)

    def adjust_for_contest(self, probability: float, contest_count: int) -> float:
        """Reduce probability based on contest"""
        penalty = contest_count * 15  # 15% per contester
        return max(0, probability - penalty)


class ShopRecommender:
    """Recommends which champions to buy from shop"""

    def __init__(self):
        self.analyzer = GameStateAnalyzer()

    def prioritize_champions(
        self,
        shop_champions: List[Champion],
        game_state: GameState,
        top_builds: List[Composition]
    ) -> List[Recommendation]:
        """
        Create priority list for shop champions

        Args:
            shop_champions: Champions in current shop
            game_state: Current game state
            top_builds: Top recommended builds

        Returns:
            List of recommendations sorted by priority
        """
        recommendations = []

        for champ in shop_champions:
            rec = self._calculate_champion_priority(
                champ,
                game_state,
                top_builds
            )
            recommendations.append(rec)

        # Sort by priority (CRITICAL first) then score
        recommendations.sort(
            key=lambda x: (x.priority.value, x.score),
            reverse=True
        )

        return recommendations

    def _calculate_champion_priority(
        self,
        champ: Champion,
        game_state: GameState,
        top_builds: List[Composition]
    ) -> Recommendation:
        """Decision tree for champion priority"""

        reasoning = []
        score = 0.0

        # Check if champion is in any top 3 builds
        relevant_builds = []
        for build in top_builds[:3]:
            if any(c.name == champ.name for c in build.champions):
                relevant_builds.append(build)

        if not relevant_builds:
            return Recommendation(
                item_name=champ.name,
                item_type="champion",
                priority=Priority.LOW,
                score=10.0,
                reasoning=["Not in target builds"],
                metadata={"cost": champ.cost}
            )

        # How many do we have?
        current_count = game_state.board.get_champion_count(champ.name)

        # Is it a carry?
        is_carry = any(
            champ.name in build.carry_units
            for build in relevant_builds
        )

        # Is it core?
        is_core = any(
            champ.name in build.core_champions
            for build in relevant_builds
        )

        # Decision tree
        if current_count == 2:
            # 2-STAR UPGRADE AVAILABLE!
            return Recommendation(
                item_name=champ.name,
                item_type="champion",
                priority=Priority.CRITICAL,
                score=100.0,
                reasoning=["⭐⭐ 2-star upgrade available!"],
                metadata={
                    "cost": champ.cost,
                    "builds": [b.name for b in relevant_builds]
                }
            )

        if current_count == 5:
            # Potential 3-star
            return Recommendation(
                item_name=champ.name,
                item_type="champion",
                priority=Priority.HIGH,
                score=90.0,
                reasoning=["⭐⭐⭐ Working towards 3-star"],
                metadata={
                    "cost": champ.cost,
                    "builds": [b.name for b in relevant_builds]
                }
            )

        if current_count == 1:
            if is_carry:
                score = 80.0
                reasoning.append("Upgrade main carry unit")
                priority = Priority.HIGH
            else:
                score = 60.0
                reasoning.append("Upgrade support unit")
                priority = Priority.MEDIUM

        elif current_count == 0:
            if is_carry:
                score = 75.0
                reasoning.append("Main carry unit for comp")
                priority = Priority.HIGH
            elif is_core:
                score = 55.0
                reasoning.append("Core unit for comp")
                priority = Priority.MEDIUM
            else:
                score = 30.0
                reasoning.append("Filler unit for comp")
                priority = Priority.LOW

        # Add build info
        build_names = [b.name for b in relevant_builds]
        reasoning.append(f"Used in: {', '.join(build_names[:2])}")

        return Recommendation(
            item_name=champ.name,
            item_type="champion",
            priority=priority,
            score=score,
            reasoning=reasoning,
            metadata={
                "cost": champ.cost,
                "is_carry": is_carry,
                "is_core": is_core,
                "builds": build_names
            }
        )


class AugmentRecommender:
    """Scores and ranks augment choices"""

    def __init__(self):
        self.analyzer = GameStateAnalyzer()

    def score_augments(
        self,
        available_augments: List[Augment],
        game_state: GameState,
        top_builds: List[Composition]
    ) -> List[Recommendation]:
        """
        Score each augment option

        Args:
            available_augments: Augments offered
            game_state: Current game state
            top_builds: Top recommended builds

        Returns:
            List of recommendations sorted by score
        """
        recommendations = []

        for augment in available_augments:
            rec = self._score_augment(augment, game_state, top_builds)
            recommendations.append(rec)

        # Sort by score
        recommendations.sort(key=lambda x: x.score, reverse=True)

        return recommendations

    def _score_augment(
        self,
        augment: Augment,
        game_state: GameState,
        top_builds: List[Composition]
    ) -> Recommendation:
        """Multi-factor augment scoring"""

        reasoning = []
        breakdown = {}

        # Factor 1: Meta Tier (40%)
        tier_scores = {"S": 10, "A": 8, "B": 6, "C": 4, "D": 2}
        tier_score = tier_scores.get(augment.tier, 3) * 0.40
        breakdown["tier"] = tier_score
        reasoning.append(f"{augment.tier}-tier augment")

        # Factor 2: Current Board Synergy (30%)
        current_traits = list(game_state.board.active_traits.keys())
        current_champs = game_state.board.get_all_champion_names()

        board_synergy = augment.synergy_score(current_traits, current_champs)
        board_score = board_synergy * 0.30
        breakdown["board_synergy"] = board_score

        if board_score > 2:
            reasoning.append(f"Strong synergy with current board")

        # Factor 3: Target Build Synergy (30%)
        build_score = 0
        if top_builds:
            target_build = top_builds[0]
            target_traits = target_build.traits
            target_champs = [c.name for c in target_build.champions]

            build_synergy = augment.synergy_score(target_traits, target_champs)
            build_score = build_synergy * 0.30
            breakdown["build_synergy"] = build_score

            if build_score > 2:
                reasoning.append(f"Synergizes with {target_build.name}")

        # Calculate total
        total = tier_score + board_score + build_score

        # Convert to 0-100 scale
        final_score = (total / 10) * 100

        # Determine priority
        if final_score >= 80:
            priority = Priority.HIGH
        elif final_score >= 60:
            priority = Priority.MEDIUM
        else:
            priority = Priority.LOW

        return Recommendation(
            item_name=augment.name,
            item_type="augment",
            priority=priority,
            score=final_score,
            reasoning=reasoning,
            metadata={
                "tier": augment.tier,
                "breakdown": breakdown
            }
        )


class RecommendationEngine:
    """Main recommendation engine - combines all systems"""

    def __init__(self):
        self.analyzer = GameStateAnalyzer()
        self.probability_engine = ProbabilityEngine()
        self.shop_recommender = ShopRecommender()
        self.augment_recommender = AugmentRecommender()

    def recommend_builds(
        self,
        meta_comps: List[Composition],
        game_state: GameState,
        limit: int = 5
    ) -> List[BuildRecommendation]:
        """
        Recommend top builds based on meta and game state

        Args:
            meta_comps: Available meta compositions
            game_state: Current game state
            limit: Max number of recommendations

        Returns:
            List of build recommendations sorted by viability
        """
        recommendations = []

        for comp in meta_comps:
            # Calculate base probability
            probability = self.probability_engine.calculate_build_probability(
                comp,
                game_state
            )

            # Count contest
            contest_count = self.analyzer.count_contested(game_state, comp)

            # Adjust for contest
            adjusted_probability = self.probability_engine.adjust_for_contest(
                probability,
                contest_count
            )

            # Count owned champions
            owned_names = game_state.board.get_all_champion_names()
            owned_count = sum(
                1 for c in comp.champions
                if c.name in owned_names
            )

            # Generate reasoning
            reasoning = self._generate_build_reasoning(
                comp,
                adjusted_probability,
                contest_count,
                owned_count,
                game_state
            )

            # Generate next steps
            next_steps = self._generate_next_steps(
                comp,
                game_state,
                owned_count
            )

            rec = BuildRecommendation(
                composition=comp,
                viability_score=adjusted_probability,
                probability=adjusted_probability,
                owned_champions=owned_count,
                contest_count=contest_count,
                reasoning=reasoning,
                next_steps=next_steps
            )

            recommendations.append(rec)

        # Sort by viability score
        recommendations.sort(key=lambda x: x.viability_score, reverse=True)

        return recommendations[:limit]

    def _generate_build_reasoning(
        self,
        comp: Composition,
        probability: float,
        contest_count: int,
        owned_count: int,
        game_state: GameState
    ) -> List[str]:
        """Generate human-readable reasoning for build recommendation"""
        reasoning = []

        # Meta strength
        reasoning.append(f"{comp.tier}-tier composition (WR: {comp.win_rate:.1%})")

        # Ownership
        total_champs = len(comp.champions)
        owned_pct = (owned_count / total_champs) * 100 if total_champs > 0 else 0
        reasoning.append(f"You own {owned_count}/{total_champs} champions ({owned_pct:.0f}%)")

        # Contest
        if contest_count == 0:
            reasoning.append("✓ Uncontested")
        elif contest_count == 1:
            reasoning.append("⚠️ 1 opponent contesting")
        else:
            reasoning.append(f"⚠️ {contest_count} opponents contesting")

        # Stage appropriateness
        stage_num = int(game_state.stage.value)
        if comp.is_early_comp and stage_num <= 3:
            reasoning.append("✓ Good for current stage")
        elif comp.is_mid_comp and 3 <= stage_num <= 5:
            reasoning.append("✓ Perfect timing for this comp")
        elif comp.is_late_comp and stage_num >= 5:
            reasoning.append("✓ Late game power spike")
        elif stage_num > 5 and not comp.is_late_comp:
            reasoning.append("⚠️ Difficult to pivot this late")

        return reasoning

    def _generate_next_steps(
        self,
        comp: Composition,
        game_state: GameState,
        owned_count: int
    ) -> List[str]:
        """Generate actionable next steps"""
        steps = []

        owned_names = game_state.board.get_all_champion_names()

        # Identify missing core units
        missing_core = [
            name for name in comp.core_champions
            if name not in owned_names
        ]

        if missing_core:
            steps.append(f"Find core units: {', '.join(missing_core[:3])}")

        # Identify missing carry
        missing_carry = [
            name for name in comp.carry_units
            if name not in owned_names
        ]

        if missing_carry:
            steps.append(f"Find carry: {', '.join(missing_carry)}")

        # Level recommendation
        if game_state.level < 7:
            steps.append(f"Level to 7+ for better odds")

        # Item building
        if comp.items:
            carry_name = comp.carry_units[0] if comp.carry_units else None
            if carry_name and carry_name in comp.items:
                items = comp.items[carry_name]
                steps.append(f"Build items on {carry_name}: {', '.join(items[:2])}")

        # Rolling strategy
        if owned_count < 4:
            steps.append("Roll to find key units")
        else:
            steps.append("Roll for upgrades")

        return steps[:4]  # Limit to 4 steps

    def recommend_shop_purchases(
        self,
        game_state: GameState,
        top_builds: List
    ) -> List[Recommendation]:
        """
        Recommend which champions to buy from shop

        Args:
            game_state: Current game state
            top_builds: List of BuildRecommendation or Composition objects
        """
        # Extract compositions if BuildRecommendations were passed
        if top_builds and hasattr(top_builds[0], 'composition'):
            comps = [b.composition for b in top_builds]
        else:
            comps = top_builds

        return self.shop_recommender.prioritize_champions(
            game_state.shop,
            game_state,
            comps
        )

    def recommend_augments(
        self,
        game_state: GameState,
        top_builds: List
    ) -> List[Recommendation]:
        """
        Recommend which augment to choose

        Args:
            game_state: Current game state
            top_builds: List of BuildRecommendation or Composition objects
        """
        # Extract compositions if BuildRecommendations were passed
        if top_builds and hasattr(top_builds[0], 'composition'):
            comps = [b.composition for b in top_builds]
        else:
            comps = top_builds

        return self.augment_recommender.score_augments(
            game_state.available_augments,
            game_state,
            comps
        )

    def recommend_action(self, game_state: GameState) -> Dict[str, str]:
        """
        Recommend high-level action (roll, eco, level)

        Returns:
            Dict with action and reasoning
        """
        decision, reason = self.analyzer.should_eco_or_roll(game_state)

        return {
            "action": decision,
            "reasoning": reason,
            "board_strength": round(
                self.analyzer.analyze_board_strength(game_state),
                1
            )
        }
