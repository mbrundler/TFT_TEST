# 🎮 TFT Meta Guide - Companion App

**Simple side-by-side companion app for Teamfight Tactics**

Run this app alongside TFT to get real-time recommendations based on your game state.

---

## 🚀 Quick Start

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the API Server

```bash
python backend/api.py
```

You should see:
```
🚀 TFT Meta Guide API starting...
📍 Running on http://localhost:5000
🔗 CORS enabled for React development
```

### 3. Open the Companion App

Simply open `companion_app/index.html` in your browser:

```bash
# macOS
open companion_app/index.html

# Linux
xdg-open companion_app/index.html

# Windows
start companion_app/index.html
```

Or just double-click `index.html` in your file explorer.

---

## 📖 How to Use

### During a TFT Game:

1. **Position the window** next to your TFT game
2. **Update game state** as you play:
   - Enter your stage (2-1, 3-2, 4-1, etc.)
   - Update gold and health
   - Add champions on your board
   - Enter shop champions (what's available to buy)
   - Enter augment choices when offered
3. **Click "Get Recommendations"**
4. **View results** in the tabs:
   - ⚡ **Action**: Should you roll or eco?
   - 🏆 **Builds**: Top 5 comps you can pivot to
   - 🛒 **Shop**: Which champions to buy (priority order)
   - ⭐ **Augments**: Best augment to pick

### Quick Buttons:

- **⬆️ Level Up**: Increases level and deducts gold
- **🎲 Roll**: Deducts 2 gold
- **💰 Buy**: Deducts gold (for buying champions)
- **💵 Sell**: Adds 1 gold (for selling champions)

---

## 🎯 Example Workflow

### Stage 2-1 (Early Game)

```
1. You're at Stage 2-1, Level 4, 32 gold
2. Board: Caitlyn
3. Shop: Jinx, Vi, Jayce, Ekko, Caitlyn

👉 Click "Get Recommendations"

Results:
- 🔴 CRITICAL: Buy Caitlyn (2-star upgrade!)
- 🟠 HIGH: Buy Jinx (main carry for Sniper comp)
- 💰 Recommendation: ECO (save gold for interest)
- 🏆 Top Build: Sniper Reroll (70.8% viability)
```

### Stage 3-2 (Augment Selection)

```
1. Stage 3-2, Level 6, 45 gold
2. Board: Caitlyn⭐⭐, Jinx, Vi
3. Augments: Sniper Emblem, Hedge Fund, Combat Training

👉 Click "Get Recommendations"

Results:
- ⭐ S-Tier: Sniper Emblem (100/100)
- ⭐ A-Tier: Hedge Fund (75/100)
- ⭐ B-Tier: Combat Training (60/100)
```

---

## 🎨 Features

### ✅ What's Working:

- **Manual Input**: Easy form to update game state
- **Quick Actions**: Fast buttons for common actions
- **Multi-Tab Interface**: Organized recommendations
- **Real-Time Updates**: Instant recommendations from engine
- **Color-Coded Priorities**: 🔴 Critical, 🟠 High, 🟡 Medium, ⚪ Low
- **Viability Scores**: Shows how strong each build is (0-100)
- **Contest Detection**: Warns if opponents are playing same comp
- **2-Star Alerts**: Highlights when you can upgrade units
- **Board Strength**: Shows how strong your current board is

### 🎨 Beautiful UI:

- Dark, modern design (easy on the eyes during long games)
- Gradient backgrounds
- Smooth animations
- Responsive layout
- Color-coded recommendations

---

## 🛠️ Tech Stack

- **Backend**: Flask + Python recommendation engine
- **Frontend**: Pure HTML/CSS/JavaScript (no build step!)
- **API**: REST API with JSON
- **Engine**: Multi-factor probability calculator

---

## 📊 How It Works

```
┌─────────────────────┐
│  Companion App UI   │  ← You enter game state
│  (HTML/JS)          │
└──────────┬──────────┘
           │
           │ POST /api/recommend-all
           ▼
┌─────────────────────┐
│  Flask API Server   │  ← Converts JSON to GameState
│  (backend/api.py)   │
└──────────┬──────────┘
           │
           │ engine.recommend_all()
           ▼
┌─────────────────────┐
│  Python Engine      │  ← Calculates recommendations
│  (src/engine/)      │
└──────────┬──────────┘
           │
           │ Returns recommendations
           ▼
┌─────────────────────┐
│  Companion App UI   │  ← Displays results
│  (HTML/JS)          │
└─────────────────────┘
```

---

## 🐛 Troubleshooting

### "Error: API error: 500"

**Solution**: Check the API server terminal for errors. Make sure all dependencies are installed:

```bash
pip install flask flask-cors
```

### "Cannot connect to API server"

**Solution**: Make sure the API server is running:

```bash
python backend/api.py
```

You should see "Running on http://localhost:5000"

### Recommendations seem wrong

**Solution**: Make sure you entered:
- Correct stage (2-1, 3-2, etc.)
- Current gold and level
- All champions on your board
- Shop champions accurately

---

## 🔮 Future Enhancements

Later we'll add:
- **OCR Integration**: Auto-detect game state from screenshots
- **Overlay Mode**: Transparent window on top of game
- **Hotkeys**: Press keys to quick-update state
- **Game History**: Track your decisions over time
- **Win Rate Tracking**: See which recommendations work best

---

## 🎓 Tips

1. **Keep it open**: Position next to TFT and update every round
2. **Trust the priorities**: 🔴 CRITICAL = must buy, 🟡 MEDIUM = if you have gold
3. **Check builds early**: Know which comp you're pivoting to by Stage 3
4. **Watch contest warnings**: Avoid builds with multiple opponents
5. **Follow the action**: If it says ROLL, you need upgrades fast

---

## 📝 Notes

- This is a **companion app**, not an overlay (yet!)
- You manually input your game state (no automation)
- 100% safe and Riot-compliant (no memory reading, no injection)
- Similar to using MetaTFT or tactics.tools while playing

---

**Built for TFT players who want to improve their decision-making! 🏆**

*Have fun climbing!*
