# TFT Meta Guide

AI-powered companion app for League of Legends: Teamfight Tactics that provides real-time recommendations for champion purchases, augment selections, and optimal builds based on current meta and game state.

## Features

- **Real-time Screen Analysis**: Captures and analyzes TFT game window without memory injection
- **Build Recommendations**: Shows top meta builds with probability scores based on your current state
- **Smart Shop Priorities**: Highlights which champions to buy with color-coded priorities
- **Augment Analysis**: Ranks augments based on synergy with your board and target builds
- **Carousel Item Suggestions**: Recommends optimal carousel picks
- **Contest Detection**: Tracks opponent boards to identify contested compositions
- **Champion Pool Tracking**: Monitors shared champion pool to calculate availability

## Safety & Riot Compliance

✅ **100% Safe & Allowed**
- Uses screen capture only (no memory reading)
- No automation or scripting
- No code injection into game process
- Similar to existing approved tools (MetaTFT, Blitz.gg)
- Provides informational assistance only

## Technology Stack

- **Python 3.9+**
- **PyQt6**: Transparent overlay UI
- **OpenCV**: Computer vision and image processing
- **EasyOCR**: Text recognition for champion names and stats
- **MSS**: Fast screen capture
- **Requests**: Meta data fetching

## Installation

### Prerequisites

- Python 3.9 or higher
- Windows 10/11 (Linux/Mac support coming soon)
- League of Legends with TFT installed

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/tft-meta-guide.git
cd tft-meta-guide
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. (Optional) Install Tesseract OCR:
   - Download from: https://github.com/tesseract-ocr/tesseract
   - Add to system PATH

## Usage

### Quick Start (No Game Required!)

Test the app with YouTube gameplay videos:

```bash
python run_debug.py
```

Then open a [TFT gameplay video on YouTube](https://www.youtube.com/results?search_query=tft+gameplay). See [TESTING.md](TESTING.md) for detailed testing instructions.

### Normal Usage

1. Launch League of Legends and enter a TFT game

2. Run the TFT Meta Guide:
```bash
python run.py
```

3. The overlay will appear on your screen with real-time recommendations

### Controls

- **Drag**: Click and drag the overlay to reposition
- **Minimize**: Click the minimize button
- **Close**: Click the X button or press Alt+F4

## Project Structure

```
tft-meta-guide/
├── src/
│   ├── capture/           # Screen capture module
│   ├── ui/                # Overlay interface
│   ├── game_state/        # Game state detection
│   ├── recommendation/    # Recommendation engine
│   ├── utils/             # Utility functions
│   └── data/              # Data and cache storage
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
└── README.md
```

## Development Roadmap

### Phase 1: Core Functionality ✅
- [x] Project structure
- [x] Screen capture system
- [x] Overlay UI framework
- [x] Basic recommendation engine
- [ ] OCR implementation
- [ ] Game state detection

### Phase 2: Advanced Features
- [ ] Opponent board tracking
- [ ] Champion pool calculations
- [ ] Real-time meta data integration
- [ ] Build probability calculations
- [ ] Contest detection algorithm

### Phase 3: Polish & Optimization
- [ ] Performance optimization
- [ ] Multi-resolution support
- [ ] User settings panel
- [ ] Hotkey support
- [ ] Statistics tracking

### Phase 4: Community
- [ ] User feedback system
- [ ] Community build sharing
- [ ] Auto-update functionality
- [ ] Multi-language support

## Configuration

Edit `config.py` to customize:
- Overlay position and size
- Update intervals
- OCR engine preferences
- Debug settings

## Troubleshooting

**Overlay not appearing?**
- Ensure TFT is running
- Check if overlay is behind game window
- Try adjusting window mode (windowed/borderless)

**Recommendations not updating?**
- Verify screen capture is working
- Check debug logs
- Ensure adequate system resources

**Poor OCR accuracy?**
- Run game in windowed mode
- Increase game resolution
- Install Tesseract for better accuracy

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - See LICENSE file for details

## Disclaimer

This project is not affiliated with, endorsed by, or connected to Riot Games. League of Legends and Teamfight Tactics are trademarks or registered trademarks of Riot Games, Inc.

This tool is provided for educational and informational purposes. Use at your own discretion.