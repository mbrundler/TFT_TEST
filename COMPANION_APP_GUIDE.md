# 🎮 TFT Companion App - Quick Start Guide

**You now have a working companion app!** 🎉

---

## 🚀 How to Run (2 Steps)

### Step 1: Start the API Server

Open a terminal and run:

```bash
python backend/api.py
```

You should see:
```
🚀 TFT Meta Guide API starting...
📍 Running on http://localhost:5000
```

**Keep this terminal open!**

---

### Step 2: Open the Companion App

Just **double-click** this file in your file explorer:
```
companion_app/index.html
```

Or use command line:
```bash
# macOS
open companion_app/index.html

# Linux
xdg-open companion_app/index.html

# Windows
start companion_app\index.html
```

---

## 🎯 How to Use While Playing TFT

### During a Game:

1. **Position the browser window** next to TFT
2. **Enter your game state:**
   - Select stage (2-1, 3-2, 4-1, etc.)
   - Update gold, health, level
   - Type your board champions (e.g., "Caitlyn, Jinx, Vi")
   - Type shop champions (e.g., "Jinx, Vi, Jayce, Ekko, Caitlyn")
3. **Click "Get Recommendations"**
4. **Check the tabs:**
   - ⚡ **Action**: Roll or Eco?
   - 🏆 **Builds**: Top 5 comps to aim for
   - 🛒 **Shop**: Which champions to buy (priority order)
   - ⭐ **Augments**: Best augment choice

### Quick Buttons:

- **⬆️ Level Up**: Auto-deducts gold and increases level
- **🎲 Roll**: Deducts 2 gold
- **💰 Buy**: Deduct gold when buying champs
- **💵 Sell**: Add 1 gold when selling

---

## 📸 Example Usage

### Early Game (Stage 2-1)

**Game State:**
- Stage: 2-1
- Level: 4
- Gold: 32
- Health: 100
- Board: Caitlyn
- Shop: Jinx, Vi, Jayce, Ekko, Caitlyn

**Recommendations:**
```
⚡ ACTION: ECO (Save gold for interest)
   Board Strength: 22/100

🏆 BUILDS:
   #1 Sniper Reroll - 70.8/100
      → Find core units: Jinx
      → Roll for upgrades after level 6

🛒 SHOP:
   🔴 Caitlyn - 100/100
      ⭐⭐ 2-STAR UPGRADE AVAILABLE!

   🟠 Jinx - 75/100
      Main carry unit for Sniper comp
```

### Mid Game (Stage 3-2 Augment)

**Game State:**
- Stage: 3-2
- Level: 6
- Gold: 45
- Board: Caitlyn⭐⭐, Jinx, Vi
- Augments: Sniper Emblem, Hedge Fund, Combat Training

**Recommendations:**
```
⭐ AUGMENTS:
   S-Tier: Sniper Emblem - 100/100
      Perfect synergy with your board

   A-Tier: Hedge Fund - 75/100
      Extra gold for faster upgrades

   B-Tier: Combat Training - 60/100
      Generic stat boost
```

---

## 🎨 What You'll See

### Beautiful UI with:
- **Dark, gaming-focused design**
- **Color-coded priorities:**
  - 🔴 CRITICAL = must buy/do
  - 🟠 HIGH = important
  - 🟡 MEDIUM = if you have resources
  - ⚪ LOW = filler
- **Viability scores** (0-100) for each build
- **Tier badges** (S/A/B/C)
- **Contest warnings** if opponents are playing same comp
- **2-star alerts** when upgrades are available

---

## 🐛 Troubleshooting

### "Cannot connect to API server"

**Fix:** Make sure the API is running:
```bash
python backend/api.py
```

### "Error: API error: 500"

**Fix:** Check the API terminal for Python errors. Usually a typo in champion names.

### Recommendations seem wrong

**Fix:** Make sure you entered:
- Correct stage
- All champions on your board
- Shop champions exactly as shown in game

---

## 💡 Tips for Best Results

1. **Update frequently**: Every round, update gold/stage/shop
2. **Trust the priorities**: 🔴 means MUST do, 🟡 means optional
3. **Check builds early**: By Stage 3, you should know your target comp
4. **Watch for contests**: Avoid builds with multiple opponents
5. **Follow the action**: If it says ROLL, you need upgrades now

---

## 🔮 What's Next (Future Features)

Later we'll add:
- **Overlay mode**: Highlights on the actual game!
- **OCR**: Auto-read game state from screenshots
- **Hotkeys**: Press keys to quick-update
- **Item recommendations**: Which items to build
- **Positioning guide**: Where to place units

---

## 📊 Tech Details

### Stack:
- **Backend**: Flask API (Python)
- **Engine**: Multi-factor recommendation algorithm
- **Frontend**: Pure HTML/CSS/JavaScript (no build needed!)
- **Data**: Real TFT compositions and meta data

### How it works:
1. You enter game state in UI
2. UI sends JSON to Flask API (`POST /api/recommend-all`)
3. API converts JSON to `GameState` object
4. Python engine calculates recommendations
5. API returns JSON with builds/shop/augments
6. UI displays color-coded recommendations

---

## 🎓 Understanding the Recommendations

### Build Viability Score:
```
Score = Meta Strength (30%)
      + Board Synergy (25%)
      + Stage Timing (20%)
      + Resources (15%)
      + Items (10%)
      - Contest Penalty (15% per opponent)
```

### Shop Priority:
- **CRITICAL**: 2-star upgrades, key carries
- **HIGH**: Core units for top build
- **MEDIUM**: Supporting units
- **LOW**: Filler/flex units

### Augment Tiers:
- **S-Tier**: Perfect synergy with your board (90-100)
- **A-Tier**: Strong choice (75-89)
- **B-Tier**: Decent option (60-74)
- **C-Tier**: Mediocre (45-59)
- **D-Tier**: Avoid (0-44)

---

## ✅ You're Ready!

**Start playing TFT with the companion app and watch your LP climb! 🚀**

Questions? Check:
- `companion_app/README.md` - Detailed docs
- `examples/engine_demo.py` - Engine examples
- `PROJECT_STATUS.md` - Project overview

---

**Built for TFT players who want to make smarter decisions! 🏆**

*Good luck and have fun!*
