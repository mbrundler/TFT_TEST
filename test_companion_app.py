#!/usr/bin/env python3
"""
Test script for Companion App
Simulates a game state and gets recommendations from the API
"""

import requests
import json

API_URL = "http://localhost:5000"

def test_api():
    print("🧪 Testing TFT Meta Guide Companion App")
    print("=" * 50)

    # Test payload (Stage 2-1, early game)
    payload = {
        "stage": "STAGE_2_1",
        "level": 4,
        "gold": 32,
        "health": 100,
        "board": {
            "champions": [
                {"name": "Caitlyn", "cost": 1, "level": 1, "items": []}
            ],
            "traits": ["Sniper", "Enforcer"]
        },
        "bench": [],
        "item_components": ["Sword", "Rod"],
        "completed_items": [],
        "shop": ["Jinx", "Vi", "Jayce", "Ekko", "Caitlyn"],
        "augment_choices": []
    }

    print("\n📊 Game State:")
    print(f"   Stage: {payload['stage']}")
    print(f"   Level: {payload['level']}")
    print(f"   Gold: {payload['gold']}")
    print(f"   Board: {[c['name'] for c in payload['board']['champions']]}")
    print(f"   Shop: {payload['shop']}")

    print("\n🚀 Calling API...")

    try:
        response = requests.post(
            f"{API_URL}/api/recommend-all",
            json=payload,
            headers={"Content-Type": "application/json"}
        )

        if response.status_code != 200:
            print(f"❌ API returned status {response.status_code}")
            print(response.text)
            return False

        data = response.json()

        print("\n✅ Success! Got recommendations:")
        print("\n" + "=" * 50)

        # Action recommendation
        print("\n⚡ ACTION RECOMMENDATION:")
        print(f"   {data['action']['recommendation']}")
        print(f"   Reason: {data['action']['reason']}")
        print(f"   Board Strength: {data['action']['board_strength']}/100")

        # Build recommendations
        print("\n🏆 BUILD RECOMMENDATIONS:")
        for i, build in enumerate(data['builds'][:3], 1):
            print(f"\n   #{i} {build['name']} - {build['viability']:.1f}/100")
            print(f"      Traits: {', '.join(build['traits'])}")
            print(f"      Champions: {', '.join([c['name'] for c in build['champions']])}")
            print(f"      Reason: {build['reason']}")
            if build['contested']:
                print(f"      ⚠️  Contested by {build['num_opponents']} opponent(s)")

        # Shop recommendations
        if data['shop']:
            print("\n🛒 SHOP RECOMMENDATIONS:")
            for rec in data['shop'][:5]:
                priority_icon = {
                    'CRITICAL': '🔴',
                    'HIGH': '🟠',
                    'MEDIUM': '🟡',
                    'LOW': '⚪'
                }.get(rec['priority'], '⚪')

                print(f"   {priority_icon} {rec['champion']} - {rec['score']:.0f}/100")
                print(f"      {rec['reason']}")
                if rec['is_upgrade']:
                    print(f"      ⭐⭐ 2-STAR UPGRADE AVAILABLE!")

        print("\n" + "=" * 50)
        print("✅ All tests passed!")
        return True

    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API server")
        print("   Make sure the server is running: python backend/api.py")
        return False

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("\n⚠️  Make sure the API server is running in another terminal:")
    print("   python backend/api.py\n")
    input("Press Enter when ready to test...")

    success = test_api()

    if success:
        print("\n🎉 Companion App is working!")
        print("\n📖 Next steps:")
        print("   1. Keep the API server running")
        print("   2. Open companion_app/index.html in your browser")
        print("   3. Enter game state and get recommendations!")
    else:
        print("\n❌ Test failed. Check the errors above.")
