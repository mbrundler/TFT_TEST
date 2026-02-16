# TFT Meta Guide - Decision Tree & Data Pipeline Plan

## Overview
This document outlines the strategy for building the recommendation decision tree and integrating meta data sources.

---

## Data Sources

### Primary Sources (Live Meta Data)

#### 1. tactics.tools
- **Priority**: HIGH
- **URL**: `https://tactics.tools/`
- **Data Needed**:
  - Top compositions (tier, win rate, play rate)
  - Champion tier lists by cost
  - Augment tier lists
  - Item priority rankings
- **Access Method**: Web scraping or API inspection
- **Update Frequency**: Every 6 hours
- **Implementation**:
  ```python
  class TacticsToolsAPI:
      def get_top_comps(self, patch: str, rank: str = "master+"):
          # Fetch composition data
          # Return: List[Composition]

      def get_augment_tiers(self, patch: str):
          # Fetch augment tier list
          # Return: Dict[augment_name, tier]
  ```

#### 2. MetaTFT.com
- **Priority**: HIGH
- **URL**: `https://www.metatft.com/`
- **Data Needed**:
  - Detailed build guides (champions, items, positioning)
  - S/A/B/C tier categorization
  - Augment recommendations per comp
- **Access Method**: Web scraping
- **Update Frequency**: Daily
- **Implementation**:
  ```python
  class MetaTFTAPI:
      def get_comp_details(self, comp_name: str):
          # Fetch detailed guide
          # Return: CompGuide (items, positioning, augments)
  ```

#### 3. lolchess.gg
- **Priority**: MEDIUM
- **URL**: `https://lolchess.gg/`
- **Data Needed**:
  - High ELO trending builds
  - Champion popularity by rank
- **Access Method**: Public API
- **Update Frequency**: Daily

### Static Data Sources

#### 4. Community Dragon
- **Priority**: HIGH
- **URL**: `https://raw.communitydragon.org/`
- **Data Needed**:
  - Champion database (name, cost, traits)
  - Trait database (tiers, effects)
  - Item database (recipes, stats)
- **Access Method**: Direct JSON fetch
- **Update Frequency**: Per patch (every 2 weeks)
- **Implementation**:
  ```python
  class GameDataService:
      def load_champions(self, patch: str):
          # Fetch champion data
          # Return: Dict[champion_name, ChampionData]

      def load_traits(self, patch: str):
          # Fetch trait data
          # Return: Dict[trait_name, TraitData]

      def load_items(self, patch: str):
          # Fetch item data
          # Return: Dict[item_name, ItemData]
  ```

---

## Decision Tree Architecture

### Layer 1: Meta Data Layer
**Purpose**: Understand what's strong in the current patch

```python
class MetaDataService:
    def __init__(self):
        self.tactics_api = TacticsToolsAPI()
        self.metatft_api = MetaTFTAPI()
        self.game_data = GameDataService()
        self.cache_ttl = 21600  # 6 hours

    def get_top_comps(self, limit=20):
        """Fetch top comps from multiple sources and aggregate"""
        # Combine data from tactics.tools + MetaTFT
        # Weight by recency and reliability
        # Return consolidated tier list

    def get_augment_tiers(self):
        """Get augment tier list"""
        # S/A/B/C/D tiers from tactics.tools

    def get_item_priority(self, comp_name):
        """Get item priority for specific comp"""
        # From MetaTFT comp guides
```

### Layer 2: Game State Analysis
**Purpose**: Analyze current game state and player resources

```python
class GameStateAnalyzer:
    def analyze_board_strength(self, game_state):
        """Calculate current board strength"""
        # Sum up champion values + trait synergies
        # Return: 0-100 score

    def identify_pivot_potential(self, game_state, target_comp):
        """Calculate how easily player can pivot to comp"""
        factors = {
            "owned_champions": 0.30,  # Already have key units
            "gold_available": 0.25,   # Can afford to roll/buy
            "stage": 0.20,            # Time remaining
            "items": 0.15,            # Have right items
            "bench_space": 0.10       # Room to hold units
        }
        # Return: 0-100 probability score

    def detect_current_traits(self, game_state):
        """Identify active traits on board"""
        # Count champions per trait
        # Return: Dict[trait, tier_active]
```

### Layer 3: Probability Calculation
**Purpose**: Calculate likelihood of successfully executing each strategy

```python
class ProbabilityEngine:
    def calculate_build_probability(self, comp, game_state):
        """Multi-factor probability calculation"""

        # Factor 1: Meta Strength (30%)
        meta_score = comp.tier_to_score()  # S=100, A=80, B=60, C=40

        # Factor 2: Board Synergy (25%)
        owned_pct = count_owned_champions(comp) / len(comp.champions)
        synergy_score = owned_pct * 100

        # Factor 3: Stage Appropriateness (20%)
        stage_score = self._stage_multiplier(game_state.stage, comp)

        # Factor 4: Resource Availability (15%)
        resource_score = self._can_afford(comp, game_state)

        # Factor 5: Item Alignment (10%)
        item_score = self._have_items(comp, game_state)

        final_score = (
            meta_score * 0.30 +
            synergy_score * 0.25 +
            stage_score * 0.20 +
            resource_score * 0.15 +
            item_score * 0.10
        )

        return final_score

    def _stage_multiplier(self, current_stage, comp):
        """Adjust probability based on game stage"""
        # Early game (1-3): Favor flexible comps
        # Mid game (3-5): Peak pivot time
        # Late game (5+): Hard to pivot, favor current board

        stage_num = int(current_stage.split('-')[0])

        if comp.is_early_comp and stage_num <= 3:
            return 100
        elif comp.is_mid_game_spike and 3 <= stage_num <= 5:
            return 100
        elif comp.is_late_game_comp and stage_num >= 5:
            return 80  # Harder to pivot late
        else:
            return 50
```

### Layer 4: Contest Detection
**Purpose**: Adjust recommendations based on opponents

```python
class ContestDetector:
    def count_contested(self, comp, game_state):
        """Count opponents running similar comp"""
        contest_count = 0

        for opponent_board in game_state.opponent_boards.values():
            # Check overlap in key champions
            overlap = self._calculate_overlap(
                comp.core_champions,
                opponent_board
            )

            if overlap >= 0.6:  # 60% overlap = contested
                contest_count += 1

        return contest_count

    def adjust_for_contest(self, probability, contest_count):
        """Reduce probability based on contest"""
        # Each contester reduces probability by 15%
        penalty = contest_count * 0.15
        return max(0, probability - penalty)
```

### Layer 5: Champion Purchase Logic
**Purpose**: Decide which champions to buy from shop

```python
class ShopRecommender:
    def prioritize_champions(self, shop_champions, game_state, top_builds):
        """Create priority list for shop champions"""

        recommendations = []

        for champ in shop_champions:
            priority = self._calculate_priority(champ, game_state, top_builds)
            recommendations.append({
                "champion": champ,
                "priority": priority.level,  # CRITICAL/HIGH/MEDIUM/LOW
                "reason": priority.reason,
                "builds": priority.builds_for
            })

        return sorted(recommendations, key=lambda x: x["priority"])

    def _calculate_priority(self, champ, game_state, top_builds):
        """Decision tree for champion priority"""

        # Check if champion is in any top 3 builds
        relevant_builds = []
        for build in top_builds[:3]:
            if champ in build.champions:
                relevant_builds.append(build)

        if not relevant_builds:
            return Priority.LOW("Not in target builds")

        # How many do we have?
        current_count = self._count_owned(champ, game_state)

        # Is it a carry?
        is_carry = any(champ in b.carry_units for b in relevant_builds)

        # Decision tree
        if current_count == 2:
            return Priority.CRITICAL("2-star upgrade available!")

        if current_count == 1:
            if is_carry:
                return Priority.HIGH("Upgrade main carry", relevant_builds)
            else:
                return Priority.MEDIUM("Upgrade support", relevant_builds)

        if current_count == 0:
            if is_carry:
                return Priority.HIGH("Main carry unit", relevant_builds)
            elif any(champ in b.core_units for b in relevant_builds):
                return Priority.MEDIUM("Core unit for comp", relevant_builds)
            else:
                return Priority.LOW("Filler unit", relevant_builds)
```

### Layer 6: Augment Selection
**Purpose**: Score and rank augment choices

```python
class AugmentRecommender:
    def score_augments(self, available_augments, game_state, top_builds):
        """Score each augment option"""

        scores = []

        for augment in available_augments:
            score = self._calculate_augment_score(
                augment,
                game_state,
                top_builds
            )
            scores.append({
                "augment": augment,
                "score": score.total,
                "breakdown": score.breakdown,
                "synergy": score.explanation
            })

        return sorted(scores, key=lambda x: x["score"], reverse=True)

    def _calculate_augment_score(self, augment, game_state, top_builds):
        """Multi-factor augment scoring"""

        # Factor 1: Meta Tier (40%)
        tier = self.meta_service.get_augment_tier(augment)
        tier_scores = {"S": 10, "A": 8, "B": 6, "C": 4, "D": 2}
        tier_score = tier_scores.get(tier, 3) * 0.40

        # Factor 2: Current Board Synergy (30%)
        current_traits = game_state.get_active_traits()
        board_score = 0
        if augment.boosts_trait and augment.trait in current_traits:
            board_score = 10 * 0.30

        # Factor 3: Target Build Synergy (30%)
        build_score = 0
        target_build = top_builds[0] if top_builds else None
        if target_build and augment.benefits_comp(target_build):
            build_score = 10 * 0.30

        total = tier_score + board_score + build_score

        return AugmentScore(
            total=total,
            breakdown={
                "tier": tier_score,
                "board": board_score,
                "build": build_score
            },
            explanation=self._explain_synergy(augment, game_state, target_build)
        )
```

---

## Caching Strategy

```python
class CacheManager:
    def __init__(self):
        self.meta_cache_ttl = 21600  # 6 hours
        self.game_data_cache_ttl = 1209600  # 2 weeks (patch cycle)

    def cache_meta_data(self):
        """Cache meta comps, augments, tier lists"""
        # Store in local SQLite or JSON
        # Include timestamp for invalidation

    def cache_game_data(self):
        """Cache static champion/trait/item data"""
        # Only update on new patch
```

---

## API Rate Limiting

```python
class RateLimiter:
    def __init__(self):
        self.max_requests_per_hour = 100
        self.request_timestamps = []

    def can_make_request(self):
        """Check if we're within rate limits"""
        # Implement token bucket or sliding window

    def wait_if_needed(self):
        """Sleep if rate limited"""
```

---

## Data Models

```python
@dataclass
class Composition:
    name: str
    tier: str  # S, A, B, C, D
    champions: List[str]
    core_champions: List[str]  # Key units
    carry_units: List[str]
    items: Dict[str, List[str]]  # champion -> item list
    traits: List[str]
    win_rate: float
    play_rate: float
    avg_placement: float
    best_stages: List[str]  # e.g., ["early", "mid"]
    is_early_comp: bool
    is_mid_game_spike: bool
    is_late_game_comp: bool

@dataclass
class Champion:
    name: str
    cost: int
    traits: List[str]
    pool_size: int  # How many exist at this cost

@dataclass
class Augment:
    name: str
    tier: str
    boosts_trait: Optional[str]
    effect: str

    def benefits_comp(self, comp: Composition) -> bool:
        """Check if augment synergizes with comp"""
        # Logic to determine synergy
```

---

## Implementation Priority

### Phase 1: Static Data (Week 1)
- [ ] Implement Community Dragon integration
- [ ] Load champion/trait/item databases
- [ ] Create local cache

### Phase 2: Meta Data (Week 2)
- [ ] Implement tactics.tools scraper
- [ ] Implement MetaTFT scraper
- [ ] Build caching layer with 6-hour TTL
- [ ] Create aggregation logic

### Phase 3: Decision Engine (Week 3)
- [ ] Implement probability calculator
- [ ] Build contest detector
- [ ] Create shop recommender
- [ ] Build augment scorer

### Phase 4: Testing & Tuning (Week 4)
- [ ] Test with real game data
- [ ] Tune weights and thresholds
- [ ] Validate recommendations against high ELO plays

---

## Error Handling

```python
class DataService:
    def fetch_with_fallback(self, primary_source, fallback_sources):
        """Try primary source, fall back if it fails"""
        try:
            return primary_source.fetch()
        except Exception as e:
            logging.warning(f"Primary source failed: {e}")
            for fallback in fallback_sources:
                try:
                    return fallback.fetch()
                except:
                    continue

            # If all fail, use cached data
            return self.get_cached_data()
```

---

## Metrics & Validation

### Success Metrics
1. **Recommendation Accuracy**: Compare to high ELO player decisions
2. **Build Win Rate**: Track win rate of recommended builds
3. **Champion Purchase Accuracy**: % of purchases that match recommendations

### A/B Testing
- Compare different weight configurations
- Validate decision tree logic against actual outcomes
