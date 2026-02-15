"""Meta data service for fetching and caching TFT meta information"""

import requests
import json
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import os


class MetaDataService:
    """Handles fetching and caching of TFT meta data"""

    def __init__(self):
        self.cache_dir = "src/data/cache"
        self.cache_duration = timedelta(hours=6)  # Refresh every 6 hours
        self.meta_data: Optional[Dict] = None

        self._ensure_cache_dir()
        self._load_cached_data()

    def _ensure_cache_dir(self):
        """Ensure cache directory exists"""
        os.makedirs(self.cache_dir, exist_ok=True)

    def _load_cached_data(self):
        """Load cached meta data if available and fresh"""
        cache_file = os.path.join(self.cache_dir, "meta_data.json")

        if not os.path.exists(cache_file):
            return

        try:
            with open(cache_file, 'r') as f:
                cached = json.load(f)

            # Check if cache is still fresh
            cache_time = datetime.fromisoformat(cached.get("timestamp", ""))
            if datetime.now() - cache_time < self.cache_duration:
                self.meta_data = cached.get("data")
        except Exception as e:
            print(f"Error loading cached data: {e}")

    def _save_cache(self, data: Dict):
        """Save meta data to cache"""
        cache_file = os.path.join(self.cache_dir, "meta_data.json")

        try:
            cached = {
                "timestamp": datetime.now().isoformat(),
                "data": data
            }
            with open(cache_file, 'w') as f:
                json.dump(cached, f, indent=2)
        except Exception as e:
            print(f"Error saving cache: {e}")

    def get_top_comps(self) -> List[Dict]:
        """
        Get top meta team compositions

        Returns:
            List of composition dictionaries
        """
        if self.meta_data is None:
            self._fetch_meta_data()

        if self.meta_data:
            return self.meta_data.get("comps", [])

        # Fallback to hardcoded meta (for development/offline use)
        return self._get_fallback_comps()

    def get_champion_cost(self, champion_name: str) -> int:
        """Get the cost/tier of a champion"""
        # TODO: Implement champion cost lookup
        return 1

    def get_augment_tier(self, augment_name: str) -> str:
        """Get tier rating for an augment"""
        # TODO: Implement augment tier lookup
        return "A"

    def _fetch_meta_data(self):
        """Fetch fresh meta data from external sources"""
        try:
            # TODO: Implement actual API calls to meta sources
            # Examples:
            # - tactics.tools API
            # - MetaTFT API
            # - mobalytics API

            # For now, use fallback data
            self.meta_data = {
                "comps": self._get_fallback_comps(),
                "augments": self._get_fallback_augments(),
                "items": self._get_fallback_items()
            }

            self._save_cache(self.meta_data)

        except Exception as e:
            print(f"Error fetching meta data: {e}")

    def _get_fallback_comps(self) -> List[Dict]:
        """
        Fallback composition data for development

        TODO: Replace with real meta data fetch
        """
        return [
            {
                "name": "Reroll Tristana",
                "champions": ["Tristana", "Lulu", "Teemo", "Veigar", "Rumble", "Poppy", "Ziggs"],
                "traits": ["Yordle", "Gunner", "Mage"],
                "tier": "S",
                "win_rate": 54.2,
                "play_rate": 12.3,
                "items": {
                    "Tristana": ["Guinsoo's Rageblade", "Last Whisper", "Giant Slayer"]
                }
            },
            {
                "name": "Ahri Reroll",
                "champions": ["Ahri", "Syndra", "Annie", "Taric", "Lux", "Lulu", "Seraphine"],
                "traits": ["Arcanist", "Scholar", "Enchanter"],
                "tier": "S",
                "win_rate": 53.8,
                "play_rate": 10.1,
                "items": {
                    "Ahri": ["Blue Buff", "Jeweled Gauntlet", "Spear of Shojin"]
                }
            },
            {
                "name": "Bruiser Urgot",
                "champions": ["Urgot", "Vi", "Zac", "Jinx", "Vi", "Blitzcrank", "Ekko"],
                "traits": ["Bruiser", "Chemtech", "Twinshot"],
                "tier": "A",
                "win_rate": 52.1,
                "play_rate": 8.7,
                "items": {
                    "Urgot": ["Titan's Resolve", "Runaan's Hurricane", "Bloodthirster"]
                }
            },
            {
                "name": "Flex Kaisa",
                "champions": ["Kai'Sa", "Sivir", "Malzahar", "Cho'Gath", "Kassadin", "Rek'Sai"],
                "traits": ["Mutant", "Void"],
                "tier": "A",
                "win_rate": 51.5,
                "play_rate": 7.2,
                "items": {
                    "Kai'Sa": ["Guinsoo's Rageblade", "Titan's Resolve", "Runaan's Hurricane"]
                }
            },
            {
                "name": "Slow Roll Warwick",
                "champions": ["Warwick", "Trundle", "Mundo", "Vi", "Zac", "Tahm Kench"],
                "traits": ["Bruiser", "Chemtech"],
                "tier": "B",
                "win_rate": 50.2,
                "play_rate": 6.5,
                "items": {
                    "Warwick": ["Bloodthirster", "Titan's Resolve", "Bramble Vest"]
                }
            }
        ]

    def _get_fallback_augments(self) -> List[Dict]:
        """Fallback augment data"""
        return [
            {"name": "Cybernetic Uplink", "tier": "S"},
            {"name": "Portable Forge", "tier": "S"},
            {"name": "Combat Training", "tier": "A"},
            {"name": "Rich Get Richer", "tier": "A"},
            {"name": "Thrill of the Hunt", "tier": "B"}
        ]

    def _get_fallback_items(self) -> Dict:
        """Fallback item data"""
        return {
            "B.F. Sword": {"component": True},
            "Recurve Bow": {"component": True},
            "Chain Vest": {"component": True},
            "Guinsoo's Rageblade": {
                "component": False,
                "recipe": ["B.F. Sword", "Recurve Bow"]
            },
            "Last Whisper": {
                "component": False,
                "recipe": ["Recurve Bow", "Sparring Gloves"]
            }
        }
