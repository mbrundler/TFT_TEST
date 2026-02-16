"""Meta data fetcher for TFT - pulls data from various sources"""

import requests
from typing import List, Dict, Optional
from dataclasses import dataclass
import json
from pathlib import Path
import time
from datetime import datetime, timedelta


@dataclass
class Composition:
    """Represents a TFT team composition"""
    name: str
    tier: str  # S, A, B, C, D
    champions: List[str]
    core_champions: List[str]
    carry_units: List[str]
    items: Dict[str, List[str]]
    traits: List[str]
    win_rate: float
    play_rate: float
    avg_placement: float
    patch: str


class CacheManager:
    """Manages caching of meta data"""

    def __init__(self, cache_dir: Path = Path("data/cache")):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def get_cache_path(self, key: str) -> Path:
        """Get cache file path for a key"""
        return self.cache_dir / f"{key}.json"

    def is_cache_valid(self, key: str, ttl_seconds: int) -> bool:
        """Check if cache is still valid"""
        cache_path = self.get_cache_path(key)

        if not cache_path.exists():
            return False

        # Check age
        cache_age = time.time() - cache_path.stat().st_mtime
        return cache_age < ttl_seconds

    def get_cached(self, key: str, ttl_seconds: int) -> Optional[Dict]:
        """Get cached data if valid"""
        if not self.is_cache_valid(key, ttl_seconds):
            return None

        cache_path = self.get_cache_path(key)
        with open(cache_path, 'r') as f:
            return json.load(f)

    def set_cache(self, key: str, data: Dict):
        """Save data to cache"""
        cache_path = self.get_cache_path(key)
        with open(cache_path, 'w') as f:
            json.dump(data, f, indent=2)


class TacticsToolsFetcher:
    """Fetches meta data from tactics.tools"""

    BASE_URL = "https://tactics.tools"
    CACHE_TTL = 21600  # 6 hours

    def __init__(self, cache_manager: CacheManager):
        self.cache = cache_manager
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'TFT-Meta-Guide/1.0'
        })

    def get_top_comps(self, patch: str = "current", rank: str = "master+") -> List[Composition]:
        """
        Fetch top compositions from tactics.tools

        Args:
            patch: Patch version (e.g., "13.24" or "current")
            rank: Rank filter (e.g., "master+", "diamond+")

        Returns:
            List of top compositions
        """
        cache_key = f"tactics_comps_{patch}_{rank}"

        # Try cache first
        cached = self.cache.get_cached(cache_key, self.CACHE_TTL)
        if cached:
            print("📦 Using cached tactics.tools data")
            return self._parse_compositions(cached)

        # Fetch fresh data
        print("🌐 Fetching fresh data from tactics.tools...")

        try:
            # Example endpoint - adjust based on actual API
            # Note: This is pseudocode - you'll need to inspect their actual API
            url = f"{self.BASE_URL}/api/compositions"
            params = {
                "patch": patch,
                "rank": rank,
                "limit": 20
            }

            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            # Cache the result
            self.cache.set_cache(cache_key, data)

            return self._parse_compositions(data)

        except Exception as e:
            print(f"❌ Error fetching from tactics.tools: {e}")

            # Fallback to cache even if expired
            cached = self.cache.get_cached(cache_key, ttl_seconds=999999)
            if cached:
                print("📦 Using stale cache as fallback")
                return self._parse_compositions(cached)

            return []

    def _parse_compositions(self, data: Dict) -> List[Composition]:
        """Parse API response into Composition objects"""
        compositions = []

        # Parse based on actual API structure
        # This is pseudocode - adjust to actual format
        for comp_data in data.get("compositions", []):
            comp = Composition(
                name=comp_data["name"],
                tier=comp_data.get("tier", "C"),
                champions=comp_data["champions"],
                core_champions=comp_data.get("core_units", []),
                carry_units=comp_data.get("carry_units", []),
                items=comp_data.get("items", {}),
                traits=comp_data.get("traits", []),
                win_rate=comp_data.get("win_rate", 0.0),
                play_rate=comp_data.get("play_rate", 0.0),
                avg_placement=comp_data.get("avg_placement", 4.5),
                patch=comp_data.get("patch", "current")
            )
            compositions.append(comp)

        return compositions

    def get_augment_tiers(self, patch: str = "current") -> Dict[str, str]:
        """
        Fetch augment tier list

        Returns:
            Dict mapping augment name to tier (S/A/B/C/D)
        """
        cache_key = f"tactics_augments_{patch}"

        cached = self.cache.get_cached(cache_key, self.CACHE_TTL)
        if cached:
            return cached

        try:
            # Fetch augment data
            url = f"{self.BASE_URL}/api/augments/tiers"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            data = response.json()
            self.cache.set_cache(cache_key, data)

            return data

        except Exception as e:
            print(f"❌ Error fetching augment tiers: {e}")
            return {}


class MetaTFTFetcher:
    """Fetches detailed comp guides from MetaTFT.com"""

    BASE_URL = "https://www.metatft.com"
    CACHE_TTL = 86400  # 24 hours

    def __init__(self, cache_manager: CacheManager):
        self.cache = cache_manager
        self.session = requests.Session()

    def get_comp_guide(self, comp_name: str) -> Optional[Dict]:
        """
        Fetch detailed guide for a specific composition

        Args:
            comp_name: Name of the composition

        Returns:
            Dict with positioning, items, augments, etc.
        """
        cache_key = f"metatft_{comp_name.lower().replace(' ', '_')}"

        cached = self.cache.get_cached(cache_key, self.CACHE_TTL)
        if cached:
            return cached

        try:
            # Example: scrape or API call
            # You might need BeautifulSoup for scraping
            print(f"🌐 Fetching {comp_name} guide from MetaTFT...")

            # Pseudocode - implement actual scraping/API
            data = self._scrape_comp_guide(comp_name)

            self.cache.set_cache(cache_key, data)
            return data

        except Exception as e:
            print(f"❌ Error fetching MetaTFT guide: {e}")
            return None

    def _scrape_comp_guide(self, comp_name: str) -> Dict:
        """Scrape comp guide from MetaTFT (implement with BeautifulSoup)"""
        # Placeholder - implement actual scraping
        return {
            "name": comp_name,
            "positioning": {},
            "item_priority": [],
            "recommended_augments": [],
            "stage_guide": {}
        }


class CommunityDragonFetcher:
    """Fetches static game data from Community Dragon"""

    BASE_URL = "https://raw.communitydragon.org/latest/cdragon/tft"
    CACHE_TTL = 1209600  # 2 weeks

    def __init__(self, cache_manager: CacheManager):
        self.cache = cache_manager
        self.session = requests.Session()

    def get_champions(self) -> Dict[str, Dict]:
        """
        Fetch champion database

        Returns:
            Dict mapping champion name to data (cost, traits)
        """
        cache_key = "cdragon_champions"

        cached = self.cache.get_cached(cache_key, self.CACHE_TTL)
        if cached:
            return cached

        try:
            print("🌐 Fetching champion data from Community Dragon...")

            url = f"{self.BASE_URL}/en_us.json"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            data = response.json()

            # Parse and structure the data
            champions = self._parse_champion_data(data)

            self.cache.set_cache(cache_key, champions)
            return champions

        except Exception as e:
            print(f"❌ Error fetching champion data: {e}")
            return {}

    def _parse_champion_data(self, raw_data: Dict) -> Dict[str, Dict]:
        """Parse Community Dragon format into usable structure"""
        champions = {}

        # Adjust parsing based on actual API structure
        for champ_data in raw_data.get("sets", {}).get("champions", []):
            name = champ_data["name"]
            champions[name] = {
                "cost": champ_data.get("cost", 1),
                "traits": champ_data.get("traits", []),
                "ability": champ_data.get("ability", {}),
                "stats": champ_data.get("stats", {})
            }

        return champions

    def get_traits(self) -> Dict[str, Dict]:
        """Fetch trait database"""
        cache_key = "cdragon_traits"

        cached = self.cache.get_cached(cache_key, self.CACHE_TTL)
        if cached:
            return cached

        try:
            # Fetch and parse trait data
            # Similar to get_champions()
            return {}

        except Exception as e:
            print(f"❌ Error fetching trait data: {e}")
            return {}

    def get_items(self) -> Dict[str, Dict]:
        """Fetch item database"""
        cache_key = "cdragon_items"

        cached = self.cache.get_cached(cache_key, self.CACHE_TTL)
        if cached:
            return cached

        try:
            # Fetch and parse item data
            return {}

        except Exception as e:
            print(f"❌ Error fetching item data: {e}")
            return {}


class MetaDataAggregator:
    """Aggregates data from multiple sources"""

    def __init__(self):
        self.cache = CacheManager()
        self.tactics_tools = TacticsToolsFetcher(self.cache)
        self.metatft = MetaTFTFetcher(self.cache)
        self.cdragon = CommunityDragonFetcher(self.cache)

    def get_top_comps(self, limit: int = 10) -> List[Composition]:
        """
        Get top compositions from all sources

        Args:
            limit: Number of compositions to return

        Returns:
            Aggregated and ranked list of compositions
        """
        # Primary source: tactics.tools
        comps = self.tactics_tools.get_top_comps()

        if not comps:
            print("⚠️  No data available from primary source")
            return []

        # Enrich with data from MetaTFT
        for comp in comps[:limit]:
            guide = self.metatft.get_comp_guide(comp.name)
            if guide:
                # Merge additional details
                comp.items.update(guide.get("item_priority", {}))

        return comps[:limit]

    def get_champion_data(self, champion_name: str) -> Optional[Dict]:
        """Get static data for a champion"""
        all_champions = self.cdragon.get_champions()
        return all_champions.get(champion_name)

    def get_champion_cost(self, champion_name: str) -> int:
        """Get champion cost (tier)"""
        champ_data = self.get_champion_data(champion_name)
        return champ_data.get("cost", 1) if champ_data else 1

    def get_augment_tier(self, augment_name: str) -> str:
        """Get augment tier (S/A/B/C/D)"""
        augment_tiers = self.tactics_tools.get_augment_tiers()
        return augment_tiers.get(augment_name, "C")


# Example usage
if __name__ == "__main__":
    aggregator = MetaDataAggregator()

    # Fetch top comps
    print("Fetching top compositions...")
    top_comps = aggregator.get_top_comps(limit=10)

    for i, comp in enumerate(top_comps, 1):
        print(f"\n{i}. {comp.name} ({comp.tier} tier)")
        print(f"   Champions: {', '.join(comp.champions)}")
        print(f"   Win Rate: {comp.win_rate:.1%}")
        print(f"   Play Rate: {comp.play_rate:.1%}")

    # Get champion data
    print("\n" + "="*50)
    print("Champion data example:")
    champ_data = aggregator.get_champion_data("Jinx")
    print(f"Jinx - Cost: {champ_data.get('cost')}, Traits: {champ_data.get('traits')}")
