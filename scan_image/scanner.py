import os
import time
import logging
from . import __version__
from .config import setup_tesseract
from .logger import setup_logging

setup_logging()
setup_tesseract()

import argparse
from multiprocessing import Pool, cpu_count
from .utils import is_valid_image, has_text_heuristic, compute_perceptual_hash, contains_phrase

def process_file(args):
    image_path, phrase = args
    if not is_valid_image(image_path):
        return None
    if not has_text_heuristic(image_path):
        return None
    img_hash = compute_perceptual_hash(image_path)
    if contains_phrase(image_path, phrase):
        return (image_path, img_hash)
    return None

def scan_images_for_phrase(folder, phrase):
    all_files = []
    for root, _, files in os.walk(folder):
        for file in files:
            all_files.append((os.path.join(root, file), phrase))

    found_images = []
    seen_hashes = set()

    logging.info(f"Starting scan of {len(all_files)} files using {cpu_count()} cores")

    with Pool(processes=cpu_count()) as pool:
        for result in pool.imap_unordered(process_file, all_files):
            if result is None:
                continue
            image_path, img_hash = result
            if img_hash in seen_hashes:
                continue
            seen_hashes.add(img_hash)
            found_images.append(image_path)

    return found_images

def main():
    parser = argparse.ArgumentParser(description="Scan a folder of images and detect a specific text phrase using OCR (Tesseract).")
    parser.add_argument("--version", action="version", version=f"scan-image {__version__}")
    parser.add_argument("-f", "--folder", help="Folder path to scan")
    parser.add_argument("-p", "--phrase", help="Phrase to search for")
    args = parser.parse_args()

    # If not provided, ask interactively
    folder_path = os.path.normpath(args.folder) if args.folder else input("Enter the folder path to scan: ").strip()
    target_phrase = args.phrase if args.phrase else input("Enter the phrase to search for: ").strip()

    if not os.path.isdir(folder_path):
        logging.error(f"The folder '{folder_path}' does not exist.")
        exit(1)

    logging.info(f"Scanning images in '{folder_path}' for phrase '{target_phrase}'...")

    start_time = time.time()
    found_images = scan_images_for_phrase(folder_path, target_phrase)
    elapsed = time.time() - start_time

    if found_images:
        count = len(found_images)
        word = "image" if count == 1 else "images"
        paths_str = "\n".join(f"- {img}" for img in found_images)
        logging.success(f"Scan complete: The phrase was found in {count} {word}:\n{paths_str}")
    else:
        logging.warning("No images contain the phrase.")

    logging.info(f"Time taken: {elapsed:.2f} seconds")
    time.sleep(5)

if __name__ == "__main__":
    main()
