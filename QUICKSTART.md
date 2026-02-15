# Quick Start Guide

Get up and running with TFT Meta Guide in 5 minutes!

## Installation

### 1. Prerequisites

- **Python 3.9+**: Download from [python.org](https://www.python.org/downloads/)
- **Git**: Download from [git-scm.com](https://git-scm.com/downloads/)
- **League of Legends**: With TFT installed

### 2. Clone & Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/tft-meta-guide.git
cd tft-meta-guide

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Run the App

```bash
python run.py
```

The overlay will appear on your screen!

## First-Time Setup

### Configure Position

1. Launch TFT in windowed or borderless mode
2. Run TFT Meta Guide
3. Drag the overlay to your preferred position
4. Position is saved automatically

### Verify Detection

The overlay should show:
- ✅ "Analyzing game state..." when working
- ✅ Build recommendations when in game
- ⚠️ "Waiting for..." when not in relevant game phase

## Usage Tips

### During Champion Select
- Check "Shop Priority" panel
- Stars indicate importance (5 stars = critical)
- Buy champions highlighted in pink/red first

### During Augment Selection
- Top 3 augments ranked by synergy
- Score out of 10 shown
- Synergy explanation provided

### During Carousel
- Recommended item shown
- Based on your current build path

### Build Panel
- Shows top 3 achievable builds
- Probability % = how likely you can pivot to it
- ⚠️ Warning shown if build is contested

## Troubleshooting

### "Analyzing game state..." stuck?

**Solution**: Run TFT in windowed or borderless mode

### Overlay not visible?

**Solutions**:
1. Check if it's behind the game window
2. Try Alt+Tab to bring it forward
3. Restart the app

### Poor champion recognition?

**Solutions**:
1. Increase game resolution
2. Install Tesseract OCR:
   ```bash
   # Windows: Download installer from
   # https://github.com/tesseract-ocr/tesseract
   # Add to PATH

   # Mac:
   brew install tesseract

   # Linux:
   sudo apt-get install tesseract-ocr
   ```
3. Set `OCR_ENGINE=tesseract` in config

### Recommendations seem off?

The app is analyzing:
- Your current champions
- Items available
- Stage of game
- What others are playing

Give it a few seconds to update!

## Keyboard Shortcuts

Currently, manual controls only:
- **Drag**: Reposition overlay
- **Minimize button**: Hide temporarily
- **X button**: Close app

## Next Steps

- Read the full [README.md](README.md)
- Check out [CONTRIBUTING.md](CONTRIBUTING.md) to help improve the app
- Join our community (coming soon!)

## Support

Having issues? Check:
1. This guide first
2. [README.md](README.md) troubleshooting section
3. Open an issue on GitHub

## Tips for Best Results

1. **Resolution**: 1920x1080 or higher recommended
2. **Window Mode**: Borderless or windowed
3. **Performance**: Close unnecessary background apps
4. **Meta Data**: App auto-updates meta data every 6 hours

Enjoy climbing with TFT Meta Guide! 🚀
