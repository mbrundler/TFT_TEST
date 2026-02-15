# Testing TFT Meta Guide with YouTube Videos

This guide explains how to test the TFT Meta Guide app using YouTube gameplay videos instead of playing an actual game.

## Why Test with YouTube?

- ✅ No need to play a full TFT game
- ✅ Can pause/replay specific moments
- ✅ Test different game phases (shop, augments, carousel)
- ✅ Perfect for development and debugging

## Setup

### 1. Find a Good TFT Gameplay Video

Search YouTube for:
- "TFT gameplay 2024"
- "Teamfight Tactics ranked gameplay"
- "TFT full game"

**Recommended videos:**
- Full gameplay videos (15-30 minutes)
- Recent patches (Set 10+)
- High quality (1080p or 4K)
- Challenger/Master gameplay (cleaner UI)

### 2. Prepare Your Screen

```
┌─────────────────────────────────────────┬──────────┐
│                                         │          │
│         YouTube Video                   │  TFT     │
│         (TFT Gameplay)                  │  Meta    │
│                                         │  Guide   │
│                                         │  Overlay │
│                                         │          │
└─────────────────────────────────────────┴──────────┘
```

1. Open YouTube video in a browser
2. Make the video as large as possible (not necessarily fullscreen)
3. Position the TFT Meta Guide overlay to the side
4. The overlay will capture your entire screen

## Running in Debug Mode

### Windows (PowerShell):

```powershell
python run_debug.py
```

### Linux/Mac:

```bash
python3 run_debug.py
```

## What to Look For

### Console Output

When the app detects something, you'll see messages like:

```
🎮 Analyzing screen (type: shop)
  🛒 Detected in shop slot 1: Tristana
  🛒 Detected in shop slot 2: Ahri
  🛒 Detected in shop slot 4: Lulu
  📋 Total champions in shop: ['Tristana', 'Ahri', 'Lulu']
  💰 Detected gold: 45
  📊 Detected level: 7
  📸 Screenshot saved: debug/screenshots/capture_1234567890.png
```

### In the Overlay UI

- **Recommended Builds** - Should show builds from meta data
- **Shop Priority** - Should update when champions are detected in shop
- **Win rates** - Will show calculated probabilities

### Debug Screenshots

Check `./debug/screenshots/` folder to see what the app is capturing. This helps you understand:
- Is it capturing the right area?
- Is the text clear enough for OCR?
- Are shop regions visible?

## Best Moments to Test

### 1. Shop Phase (Easiest)
- Pause video when player is shopping
- Champion names are clearly visible
- Gold and level shown at bottom

### 2. Augment Selection
- When augment selection appears
- Large, clear text
- Good for testing augment recommendations

### 3. Carousel Round
- Beginning of game
- Clear item/champion visibility

## Troubleshooting

### "No champions detected"

**Possible issues:**
1. Video quality too low
2. Champion names not visible in captured region
3. OCR engine not initialized properly

**Solutions:**
- Try a higher quality video
- Check debug screenshots to see what's being captured
- Pause on shop screen for 2-3 seconds

### "OCR engine failed to initialize"

**For EasyOCR:**
```bash
pip install easyocr
```

**For Tesseract:**
- Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
- Mac: `brew install tesseract`
- Linux: `sudo apt-get install tesseract-ocr`

Then switch engine in `config.py`:
```python
OCR_ENGINE = "tesseract"  # or "easyocr"
```

### "App is too slow"

**EasyOCR is slower but more accurate**
- First run downloads models (~100MB)
- Subsequent runs are faster
- Each detection takes 2-5 seconds

**Switch to Tesseract for speed:**
1. Install Tesseract (see above)
2. Change `config.py`: `OCR_ENGINE = "tesseract"`
3. Restart app

## Understanding the Results

### Detection Accuracy

Current implementation:
- ✅ **Champion names**: Good accuracy with clear text
- ⚠️ **Gold/Level**: Moderate (numbers can be tricky)
- 🚧 **Board state**: Not yet implemented
- 🚧 **Augments**: Not yet implemented

### Recommendations

The app will:
1. Detect champions in shop
2. Match against meta compositions
3. Recommend which champions to buy
4. Show priority based on top builds

## Next Steps

Once shop detection works:
1. Implement board state detection
2. Add augment selection detection
3. Implement opponent tracking
4. Add real-time meta data from APIs

## Tips for Best Results

1. **Use recent videos** - Current set champions
2. **Pause frequently** - Give OCR time to process
3. **High quality videos** - 1080p minimum
4. **Check screenshots** - Verify capture regions
5. **Watch console** - See detection in real-time

## Example Test Session

1. Start app: `python run_debug.py`
2. Open YouTube: "TFT Set 10 Challenger Gameplay"
3. Skip to 5:00 (usually mid-game shop phase)
4. Pause video
5. Wait 2-3 seconds
6. Check console for detections
7. Check overlay for recommendations
8. Look at debug/screenshots/ to see capture

## Advanced: Custom Screen Regions

Edit `config.py` to adjust capture regions:

```python
SCREEN_REGIONS = {
    "shop": {
        "x_ratio": 0.2,    # Start 20% from left
        "y_ratio": 0.75,   # Start 75% from top
        "width_ratio": 0.6,  # 60% of screen width
        "height_ratio": 0.2  # 20% of screen height
    },
    # ... more regions
}
```

Adjust these values if the shop isn't being captured correctly for your video resolution.
