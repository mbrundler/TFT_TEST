"""
TFT Meta Guide - Flask API Backend
Connects React UI with Python recommendation engine
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os

# Add parent directory to path to import engine
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.engine.recommendation_engine import RecommendationEngine
from src.engine.models import GameState, Board, Champion, Stage, Composition, Augment

app = Flask(__name__)
CORS(app)  # Enable CORS for React development

# Initialize engine
engine = RecommendationEngine()


def parse_game_state(data):
    """Convert JSON payload to GameState object"""

    # Parse board
    board_data = data.get('board', {})
    champions = [
        Champion(
            name=champ['name'],
            cost=champ['cost'],
            level=champ.get('level', 1),
            items=champ.get('items', [])
        )
        for champ in board_data.get('champions', [])
    ]

    board = Board(
        champions=champions,
        traits=board_data.get('traits', [])
    )

    # Parse bench
    bench = [
        Champion(
            name=champ['name'],
            cost=champ['cost'],
            level=champ.get('level', 1)
        )
        for champ in data.get('bench', [])
    ]

    # Parse stage
    stage_str = data.get('stage', 'STAGE_2_1')
    stage = Stage[stage_str] if stage_str in Stage.__members__ else Stage.STAGE_2_1

    # Create game state
    game_state = GameState(
        stage=stage,
        level=data.get('level', 2),
        gold=data.get('gold', 0),
        health=data.get('health', 100),
        board=board,
        bench=bench,
        item_components=data.get('item_components', []),
        completed_items=data.get('completed_items', [])
    )

    return game_state


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'TFT Meta Guide API is running'})


@app.route('/api/recommend-all', methods=['POST'])
def recommend_all():
    """
    Get all recommendations (builds, shop, augments, action)

    Payload:
    {
        "stage": "STAGE_2_1",
        "level": 4,
        "gold": 32,
        "health": 100,
        "board": {
            "champions": [{"name": "Caitlyn", "cost": 1, "level": 1, "items": []}],
            "traits": ["Sniper", "Enforcer"]
        },
        "bench": [],
        "item_components": ["Sword", "Rod"],
        "completed_items": [],
        "shop": ["Jinx", "Vi", "Jayce", "Ekko", "Caitlyn"],
        "augment_choices": ["Sniper Emblem", "Hedge Fund", "Combat Training"]
    }
    """
    try:
        data = request.json
        game_state = parse_game_state(data)

        # Get all recommendations
        recommendations = engine.recommend_all(game_state)

        # Convert to JSON-serializable format
        result = {
            'builds': [
                {
                    'name': rec.composition.name,
                    'viability': rec.viability_score,
                    'traits': rec.composition.core_traits,
                    'champions': [
                        {'name': c.name, 'cost': c.cost}
                        for c in rec.composition.core_champions
                    ],
                    'reason': rec.reason,
                    'next_steps': rec.next_steps,
                    'contested': rec.is_contested,
                    'num_opponents': rec.num_opponents,
                    'owned_champions': rec.owned_champions
                }
                for rec in recommendations['builds']
            ],
            'shop': [],
            'augments': [],
            'action': {
                'recommendation': recommendations['action']['recommendation'],
                'reason': recommendations['action']['reason'],
                'board_strength': recommendations['action']['board_strength']
            }
        }

        # Shop recommendations (if shop provided)
        if 'shop' in data and data['shop']:
            shop_recs = engine.shop_recommender.recommend_shop_purchases(
                game_state,
                [
                    Champion(name=name, cost=1, level=1)  # Cost determined by engine
                    for name in data['shop']
                ],
                recommendations['builds']
            )

            result['shop'] = [
                {
                    'champion': rec.champion.name,
                    'priority': rec.priority.value,
                    'priority_color': {
                        'CRITICAL': 'red',
                        'HIGH': 'orange',
                        'MEDIUM': 'yellow',
                        'LOW': 'gray'
                    }.get(rec.priority.value, 'gray'),
                    'score': rec.score,
                    'reason': rec.reason,
                    'can_afford': rec.can_afford,
                    'is_upgrade': rec.is_upgrade
                }
                for rec in shop_recs
            ]

        # Augment recommendations (if augments provided)
        if 'augment_choices' in data and data['augment_choices']:
            augments = [
                Augment(name=name, tier='Gold')  # Tier can be refined
                for name in data['augment_choices']
            ]

            augment_recs = engine.augment_recommender.score_augments(
                game_state,
                augments,
                recommendations['builds']
            )

            result['augments'] = [
                {
                    'name': rec.augment.name,
                    'score': rec.score,
                    'tier': rec.tier,
                    'synergies': rec.synergies,
                    'reason': rec.reason
                }
                for rec in augment_recs
            ]

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/recommend-builds', methods=['POST'])
def recommend_builds():
    """Get build recommendations only"""
    try:
        data = request.json
        game_state = parse_game_state(data)

        recommendations = engine.recommend_all(game_state)

        builds = [
            {
                'name': rec.composition.name,
                'viability': rec.viability_score,
                'traits': rec.composition.core_traits,
                'champions': [
                    {'name': c.name, 'cost': c.cost}
                    for c in rec.composition.core_champions
                ],
                'reason': rec.reason,
                'next_steps': rec.next_steps,
                'contested': rec.is_contested,
                'num_opponents': rec.num_opponents
            }
            for rec in recommendations['builds']
        ]

        return jsonify({'builds': builds})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("🚀 TFT Meta Guide API starting...")
    print("📍 Running on http://localhost:5000")
    print("🔗 CORS enabled for React development")
    app.run(debug=True, port=5000)
