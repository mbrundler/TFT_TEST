"""OCR utilities for text recognition in TFT screen captures"""

import cv2
import numpy as np
from typing import List, Tuple, Optional, Dict
import config


class OCREngine:
    """Base class for OCR engines"""

    def __init__(self):
        self.confidence_threshold = config.OCR_CONFIDENCE_THRESHOLD

    def read_text(self, image: np.ndarray) -> List[Tuple[str, float]]:
        """
        Extract text from image

        Args:
            image: Input image (BGR or grayscale)

        Returns:
            List of (text, confidence) tuples
        """
        raise NotImplementedError


class EasyOCREngine(OCREngine):
    """EasyOCR implementation for text recognition"""

    def __init__(self):
        super().__init__()
        self.reader = None
        self._initialize()

    def _initialize(self):
        """Initialize EasyOCR reader"""
        try:
            import easyocr
            self.reader = easyocr.Reader(
                config.OCR_LANGUAGES,
                gpu=False  # Set to True if CUDA available
            )
            print("✅ EasyOCR initialized successfully")
        except Exception as e:
            print(f"❌ Failed to initialize EasyOCR: {e}")
            self.reader = None

    def read_text(self, image: np.ndarray) -> List[Tuple[str, float]]:
        """Extract text using EasyOCR"""
        if self.reader is None:
            return []

        try:
            results = self.reader.readtext(image)

            # Filter by confidence and format output
            filtered_results = [
                (text, confidence)
                for (bbox, text, confidence) in results
                if confidence >= self.confidence_threshold
            ]

            return filtered_results
        except Exception as e:
            print(f"Error in EasyOCR text recognition: {e}")
            return []

    def read_text_regions(
        self,
        image: np.ndarray
    ) -> List[Dict[str, any]]:
        """
        Extract text with bounding box information

        Args:
            image: Input image

        Returns:
            List of dicts with text, confidence, and bbox
        """
        if self.reader is None:
            return []

        try:
            results = self.reader.readtext(image)

            formatted_results = []
            for (bbox, text, confidence) in results:
                if confidence >= self.confidence_threshold:
                    formatted_results.append({
                        "text": text,
                        "confidence": confidence,
                        "bbox": bbox
                    })

            return formatted_results
        except Exception as e:
            print(f"Error in EasyOCR region detection: {e}")
            return []


class TesseractEngine(OCREngine):
    """Tesseract OCR implementation"""

    def __init__(self):
        super().__init__()
        self.available = self._check_availability()

    def _check_availability(self) -> bool:
        """Check if Tesseract is installed"""
        try:
            import pytesseract
            pytesseract.get_tesseract_version()
            print("✅ Tesseract OCR initialized successfully")
            return True
        except Exception as e:
            print(f"⚠️ Tesseract not available: {e}")
            return False

    def read_text(self, image: np.ndarray) -> List[Tuple[str, float]]:
        """Extract text using Tesseract"""
        if not self.available:
            return []

        try:
            import pytesseract

            # Get detailed data with confidence scores
            data = pytesseract.image_to_data(
                image,
                output_type=pytesseract.Output.DICT
            )

            results = []
            for i, text in enumerate(data["text"]):
                if text.strip():
                    confidence = float(data["conf"][i]) / 100.0
                    if confidence >= self.confidence_threshold:
                        results.append((text, confidence))

            return results
        except Exception as e:
            print(f"Error in Tesseract text recognition: {e}")
            return []

    def read_single_line(self, image: np.ndarray) -> Optional[str]:
        """
        Extract single line of text (optimized for numbers/stats)

        Args:
            image: Input image

        Returns:
            Extracted text or None
        """
        if not self.available:
            return None

        try:
            import pytesseract

            # Configure for single line
            custom_config = r'--oem 3 --psm 7'
            text = pytesseract.image_to_string(image, config=custom_config)

            return text.strip() if text else None
        except Exception as e:
            print(f"Error in Tesseract single line reading: {e}")
            return None


class ChampionNameRecognizer:
    """Specialized recognizer for TFT champion names"""

    def __init__(self, ocr_engine: OCREngine):
        self.ocr = ocr_engine
        self.champion_names = self._load_champion_names()

    def _load_champion_names(self) -> List[str]:
        """
        Load list of valid champion names

        TODO: Load from data file or API
        """
        return [
            "Ahri", "Akali", "Amumu", "Annie", "Ashe",
            "Blitzcrank", "Brand", "Braum", "Caitlyn", "Camille",
            "Cassiopeia", "Cho'Gath", "Darius", "Diana", "Draven",
            "Ekko", "Elise", "Ezreal", "Fiora", "Fizz",
            "Gangplank", "Garen", "Gnar", "Graves", "Hecarim",
            "Heimerdinger", "Irelia", "Janna", "Jarvan IV", "Jayce",
            "Jhin", "Jinx", "Kai'Sa", "Kalista", "Kassadin",
            "Katarina", "Kayle", "Kennen", "Kha'Zix", "Kindred",
            "Kog'Maw", "LeBlanc", "Lee Sin", "Leona", "Lissandra",
            "Lucian", "Lulu", "Lux", "Malphite", "Malzahar",
            "Miss Fortune", "Mordekaiser", "Morgana", "Nami", "Nasus",
            "Nautilus", "Neeko", "Nocturne", "Nunu", "Olaf",
            "Orianna", "Pantheon", "Poppy", "Pyke", "Qiyana",
            "Quinn", "Rakan", "Rammus", "Rek'Sai", "Renekton",
            "Riven", "Rumble", "Ryze", "Sejuani", "Senna",
            "Seraphine", "Sett", "Shen", "Shyvana", "Singed",
            "Sion", "Sivir", "Skarner", "Sona", "Soraka",
            "Swain", "Syndra", "Tahm Kench", "Taliyah", "Talon",
            "Taric", "Teemo", "Thresh", "Tristana", "Trundle",
            "Tryndamere", "Twisted Fate", "Twitch", "Udyr", "Urgot",
            "Varus", "Vayne", "Veigar", "Vel'Koz", "Vi",
            "Viego", "Viktor", "Vladimir", "Volibear", "Warwick",
            "Wukong", "Xayah", "Xerath", "Xin Zhao", "Yasuo",
            "Yorick", "Yuumi", "Zac", "Zed", "Ziggs",
            "Zilean", "Zoe", "Zyra"
        ]

    def recognize_champion(self, image: np.ndarray) -> Optional[str]:
        """
        Recognize champion name from image region

        Args:
            image: Image region containing champion name

        Returns:
            Champion name or None
        """
        results = self.ocr.read_text(image)

        if not results:
            return None

        # Get best match
        for text, confidence in sorted(results, key=lambda x: x[1], reverse=True):
            # Try to match with known champion names
            matched = self._fuzzy_match(text, self.champion_names)
            if matched:
                return matched

        return None

    def _fuzzy_match(self, text: str, candidates: List[str]) -> Optional[str]:
        """
        Find best fuzzy match for text in candidates

        Args:
            text: Input text
            candidates: List of valid options

        Returns:
            Best match or None
        """
        text = text.lower().strip()

        # Exact match
        for candidate in candidates:
            if text == candidate.lower():
                return candidate

        # Partial match
        for candidate in candidates:
            if text in candidate.lower() or candidate.lower() in text:
                return candidate

        # Levenshtein distance (simplified)
        best_match = None
        best_score = float('inf')

        for candidate in candidates:
            score = self._levenshtein_distance(text, candidate.lower())
            if score < best_score and score <= 3:  # Allow up to 3 character differences
                best_score = score
                best_match = candidate

        return best_match

    def _levenshtein_distance(self, s1: str, s2: str) -> int:
        """Calculate Levenshtein distance between two strings"""
        if len(s1) < len(s2):
            return self._levenshtein_distance(s2, s1)

        if len(s2) == 0:
            return len(s1)

        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]


def get_ocr_engine() -> OCREngine:
    """
    Get configured OCR engine

    Returns:
        OCREngine instance
    """
    engine_type = config.OCR_ENGINE.lower()

    if engine_type == "easyocr":
        return EasyOCREngine()
    elif engine_type == "tesseract":
        return TesseractEngine()
    else:
        print(f"Unknown OCR engine: {engine_type}, defaulting to EasyOCR")
        return EasyOCREngine()
