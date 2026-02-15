# Contributing to TFT Meta Guide

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the project.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in Issues
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - Your system info (OS, Python version, etc.)

### Suggesting Features

1. Check if the feature has been suggested before
2. Open an issue with:
   - Clear description of the feature
   - Use cases and benefits
   - Potential implementation approach

### Submitting Code

1. Fork the repository
2. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes following our code style
4. Test thoroughly
5. Commit with clear messages:
   ```bash
   git commit -m "Add feature: description"
   ```
6. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
7. Open a Pull Request with:
   - Description of changes
   - Related issue numbers
   - Testing done

## Development Setup

1. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/tft-meta-guide.git
   cd tft-meta-guide
   ```

2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Enable debug mode:
   ```bash
   export DEBUG=True
   ```

## Code Style

- Follow PEP 8 style guide
- Use type hints where appropriate
- Add docstrings to functions and classes
- Keep functions focused and concise
- Comment complex logic

### Example:

```python
def calculate_probability(comp: Dict, state: GameState) -> float:
    """
    Calculate probability of achieving a composition

    Args:
        comp: Composition dictionary with champions and items
        state: Current game state

    Returns:
        Probability score between 0-100
    """
    # Implementation
    pass
```

## Project Structure

- `src/capture/`: Screen capture and image processing
- `src/ui/`: Overlay interface components
- `src/game_state/`: Game state detection and tracking
- `src/recommendation/`: Recommendation algorithms
- `src/utils/`: Shared utility functions
- `src/data/`: Data storage and caching

## Testing

Before submitting:

1. Test your changes manually
2. Ensure no regressions in existing features
3. Test on different resolutions if UI-related
4. Verify performance (should not impact game FPS)

## Areas Needing Help

- **OCR Accuracy**: Improving champion/item recognition
- **Game State Detection**: Better screen analysis
- **Meta Data Integration**: Adding more data sources
- **UI/UX**: Making overlay more intuitive
- **Performance**: Optimization opportunities
- **Documentation**: Tutorials and guides

## Questions?

Feel free to open an issue with the "question" label or reach out to maintainers.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the best solution, not ego
- Help others learn and grow

Thank you for contributing! 🎉
