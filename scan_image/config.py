import os
import pytesseract
import logging

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".tiff"}
MIN_WIDTH = 50
MIN_HEIGHT = 50

def setup_tesseract():
    """Configure Tesseract path from environment variable and log version once."""
    tesseract_path = os.getenv("TESSERACT_PATH")
    if tesseract_path:
        pytesseract.pytesseract.tesseract_cmd = tesseract_path

    try:
        version = pytesseract.get_tesseract_version()
        logging.debug(f"Tesseract version {version} from binary: {pytesseract.pytesseract.tesseract_cmd}")
    except pytesseract.pytesseract.TesseractNotFoundError:
        logging.error("Tesseract not found. Ensure TESSERACT_PATH points to the full executable path.")
