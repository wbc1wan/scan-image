import os
import cv2
import pytesseract
import imagehash
from PIL import Image
from .config import IMAGE_EXTENSIONS, MIN_WIDTH, MIN_HEIGHT
import logging

def is_valid_image(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext not in IMAGE_EXTENSIONS:
        return False
    try:
        img = Image.open(file_path)
        img.verify()
    except Exception:
        return False
    with Image.open(file_path) as img_check:
        if img_check.width < MIN_WIDTH or img_check.height < MIN_HEIGHT:
            return False
    return True

def has_text_heuristic(image_path, edge_thresh=0.02):
    try:
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            return False
        edges = cv2.Canny(img, 100, 200)
        edge_density = edges.sum() / (edges.shape[0] * edges.shape[1])
        return edge_density > edge_thresh
    except Exception as e:
        logging.error((f"Text heuristic failed for {image_path}: {e}"))
        return False

def compute_perceptual_hash(image_path):
    with Image.open(image_path) as img:
        return imagehash.phash(img)

def contains_phrase(image_path, phrase):
    try:
        text = pytesseract.image_to_string(Image.open(image_path))
        logging.debug(f"OCR text for {image_path}: {text[:100]}...")
        return phrase.lower() in text.lower()
    except Exception as e:
        logging.error((f"OCR failed for {image_path}: {e}"))
        return False
