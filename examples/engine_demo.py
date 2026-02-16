"""
Demo of the TFT Recommendation Engine

This example shows how the engine makes recommendations based on:
- Current meta compositions
- Game state (stage, gold, board)
- Shop champions
- Augment choices
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.engine import (
    RecommendationEngine,
    GameState,
    Board,
    Champion,
    Composition,
    Augment,
    Stage
)


def create_sample_meta_comps():
    """Create sample meta compositions"""
    comps = []

    # 1. Sniper Comp (S-tier)
    sniper_comp = Composition(
        name="Sniper Reroll",
        tier="S",
        champions=[
            Champion("Caitlyn", 2, ["Sniper", "Enforcer"], is_carry=True),
            Champion("Jinx", 3, ["Sniper", "Rebel"], is_carry=True),
            Champion("Miss Fortune", 5, ["Sniper", "Mercenary"]),
            Champion("Urgot", 5, ["Sniper", "Bruiser"]),
            Champion("Vi", 3, ["Enforcer", "Bruiser"], is_core=True),
            Champion("Jayce", 3, ["Enforcer", "Inventor"]),
            Champion("Ekko", 4, ["Rebel", "Assassin"]),
        ],
        core_champions=["Caitlyn", "Jinx", "Vi"],
        carry_units=["Caitlyn", "Jinx"],
        items={
            "Caitlyn": ["Giant Slayer", "Last Whisper", "Runaan's Hurricane"],
            "Jinx": ["Giant Slayer", "Runaan's Hurricane", "Infinity Edge"]
        },
        traits=["Sniper", "Enforcer", "Rebel"],
        win_rate=0.54,
        play_rate=0.12,
        avg_placement=3.8,
        patch="14.2",
        best_stages=["mid", "late"]
    )
    comps.append(sniper_comp)

    # 2. Bruiser Comp (A-tier)
    bruiser_comp = Composition(
        name="Bruiser Frontline",
        tier="A",
        champions=[
            Champion("Sett", 4, ["Bruiser", "Boss"], is_carry=True),
            Champion("Vi", 3, ["Enforcer", "Bruiser"], is_core=True),
            Champion("Urgot", 5, ["Sniper", "Bruiser"]),
            Champion("Warwick", 2, ["Bruiser", "Chemtech"]),
            Champion("Darius", 1, ["Bruiser", "Conqueror"]),
            Champion("Illaoi", 3, ["Bruiser", "Watcher"]),
        ],
        core_champions=["Sett", "Vi", "Urgot"],
        carry_units=["Sett"],
        items={
            "Sett": ["Sunfire Cape", "Warmog's Armor", "Titan's Resolve"],
        },
        traits=["Bruiser", "Enforcer"],
        win_rate=0.52,
        play_rate=0.15,
        avg_placement=4.0,
        patch="14.2",
        best_stages=["mid"]
    )
    comps.append(bruiser_comp)

    # 3. Fast 8 Comp (B-tier)
    fast8_comp = Composition(
        name="Fast 8 Legendaries",
        tier="B",
        champions=[
            Champion("Miss Fortune", 5, ["Sniper", "Mercenary"], is_carry=True),
            Champion("Urgot", 5, ["Sniper", "Bruiser"]),
            Champion("Ekko", 4, ["Rebel", "Assassin"]),
            Champion("Viktor", 4, ["Arcanist", "Chemtech"]),
        ],
        core_champions=["Miss Fortune", "Urgot"],
        carry_units=["Miss Fortune"],
        items={
            "Miss Fortune": ["Giant Slayer", "Last Whisper", "Infinity Edge"],
        },
        traits=["Sniper", "Mercenary"],
        win_rate=0.48,
        play_rate=0.08,
        avg_placement=4.3,
        patch="14.2",
        best_stages=["late"]
    )
    comps.append(fast8_comp)

    return comps


def create_sample_game_state_early():
    """Create sample game state - Early game scenario"""

    # Current board - starting to build sniper
    board = Board(
        champions=[
            Champion("Caitlyn", 2, ["Sniper", "Enforcer"], count=1),
            Champion("Vi", 3, ["Enforcer", "Bruiser"], count=1),
            Champion("Darius", 1, ["Bruiser", "Conqueror"], count=2),
            Champion("Warwick", 2, ["Bruiser", "Chemtech"], count=1),
        ],
        bench=[
            Champion("Caitlyn", 2, ["Sniper", "Enforcer"], count=1),
        ],
        items=["B.F. Sword", "Recurve Bow", "Giant's Belt"],
        active_traits={
            "Sniper": 1,
            "Enforcer": 2,
            "Bruiser": 2
        }
    )

    # Shop - has good options
    shop = [
        Champion("Caitlyn", 2, ["Sniper", "Enforcer"]),  # UPGRADE!
        Champion("Jinx", 3, ["Sniper", "Rebel"]),
        Champion("Ezreal", 1, ["Sniper", "Scrap"]),
        Champion("Blitzcrank", 2, ["Brawler", "Rival"]),
        Champion("Jayce", 3, ["Enforcer", "Inventor"]),
    ]

    # Opponent boards (2 opponents)
    opponent_boards = {
        "Opponent1": Board(
            champions=[
                Champion("Jinx", 3, ["Sniper", "Rebel"], count=2),
                Champion("Vi", 3, ["Enforcer", "Bruiser"], count=1),
            ],
            bench=[],
            items=["B.F. Sword"],
            active_traits={"Sniper": 1, "Enforcer": 1}
        ),
        "Opponent2": Board(
            champions=[
                Champion("Sett", 4, ["Bruiser", "Boss"], count=1),
                Champion("Warwick", 2, ["Bruiser", "Chemtech"], count=2),
            ],
            bench=[],
            items=[],
            active_traits={"Bruiser": 2}
        ),
    }

    game_state = GameState(
        stage=Stage.STAGE_3,
        round_num=2,
        level=5,
        gold=32,
        health=78,
        board=board,
        opponent_boards=opponent_boards,
        shop=shop
    )

    return game_state


def create_sample_augments():
    """Create sample augment choices"""
    return [
        Augment(
            name="Sniper Emblem",
            tier="A",
            boosts_trait="Sniper",
            effect_type="trait"
        ),
        Augment(
            name="Combat Training",
            tier="B",
            effect_type="general"
        ),
        Augment(
            name="Rich Get Richer",
            tier="S",
            effect_type="economic"
        ),
    ]


def main():
    """Run the demo"""
    print("=" * 70)
    print("🎮 TFT RECOMMENDATION ENGINE DEMO")
    print("=" * 70)

    # Initialize engine
    engine = RecommendationEngine()

    # Create sample data
    meta_comps = create_sample_meta_comps()
    game_state = create_sample_game_state_early()
    game_state.available_augments = create_sample_augments()

    print("\n📊 GAME STATE")
    print(f"  Stage: {game_state.stage.value}-{game_state.round_num}")
    print(f"  Level: {game_state.level}")
    print(f"  Gold: {game_state.gold}")
    print(f"  Health: {game_state.health}")
    print(f"  Board: {[c.name for c in game_state.board.champions]}")
    print(f"  Active Traits: {game_state.board.active_traits}")

    print("\n" + "=" * 70)
    print("🎯 BUILD RECOMMENDATIONS")
    print("=" * 70)

    build_recs = engine.recommend_builds(meta_comps, game_state, limit=3)

    for i, rec in enumerate(build_recs, 1):
        print(f"\n{i}. {rec.composition.name} ({rec.composition.tier}-tier)")
        print(f"   Viability: {rec.viability_score:.1f}/100")
        print(f"   Probability: {rec.probability:.1f}%")
        print(f"\n   Reasoning:")
        for reason in rec.reasoning:
            print(f"     • {reason}")
        print(f"\n   Next Steps:")
        for step in rec.next_steps:
            print(f"     → {step}")

    print("\n" + "=" * 70)
    print("🛒 SHOP RECOMMENDATIONS")
    print("=" * 70)

    shop_recs = engine.recommend_shop_purchases(game_state, build_recs)

    print(f"\nCurrent shop: {[c.name for c in game_state.shop]}")
    print("\nPriority order:")

    for i, rec in enumerate(shop_recs, 1):
        priority_emoji = {
            "CRITICAL": "🔴",
            "HIGH": "🟠",
            "MEDIUM": "🟡",
            "LOW": "⚪"
        }
        emoji = priority_emoji.get(rec.priority.name, "⚪")

        print(f"\n{i}. {emoji} {rec.item_name} - {rec.priority.name} (Score: {rec.score:.0f})")
        for reason in rec.reasoning:
            print(f"     • {reason}")

    print("\n" + "=" * 70)
    print("✨ AUGMENT RECOMMENDATIONS")
    print("=" * 70)

    augment_recs = engine.recommend_augments(game_state, build_recs)

    print("\nAvailable augments:")
    for i, rec in enumerate(augment_recs, 1):
        print(f"\n{i}. {rec.item_name} ({rec.metadata['tier']}-tier)")
        print(f"   Score: {rec.score:.1f}/100 - {rec.priority.name}")
        for reason in rec.reasoning:
            print(f"     • {reason}")

    print("\n" + "=" * 70)
    print("💰 ACTION RECOMMENDATION")
    print("=" * 70)

    action_rec = engine.recommend_action(game_state)
    print(f"\nRecommended action: {action_rec['action'].upper()}")
    print(f"Reasoning: {action_rec['reasoning']}")
    print(f"Board strength: {action_rec['board_strength']}/100")

    print("\n" + "=" * 70)
    print("✅ DEMO COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
