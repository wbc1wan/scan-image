import os
import unittest
from unittest.mock import patch
from scan_image import utils, scanner
from PIL import Image, ImageDraw
import shutil  # for checking system executables

class TestIntegrationOCR(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_dir = os.path.dirname(__file__)
        cls.sample_image_name = "sample_ocr_test.png"
        cls.sample_image_path = os.path.join(cls.test_dir, cls.sample_image_name)

        # Create a test image
        img = Image.new("RGB", (400, 150), color="white")
        draw = ImageDraw.Draw(img)
        draw.text((20, 60), "HELLO_TEST", fill="black")
        img.save(cls.sample_image_path)

        # Small image (should be skipped)
        cls.small_image_path = os.path.join(cls.test_dir, "small.png")
        small_img = Image.new("RGB", (10, 10), color="white")
        small_img.save(cls.small_image_path)

        # Non-image file (should be ignored)
        cls.text_file_path = os.path.join(cls.test_dir, "file.txt")
        with open(cls.text_file_path, "w") as f:
            f.write("HELLO_TEST")

        # Robust check for Tesseract: either env var or system PATH
        cls.tesseract_path = os.getenv("TESSERACT_PATH") or shutil.which("tesseract")
        if not cls.tesseract_path:
            raise unittest.SkipTest(
                "Tesseract not installed or not found in PATH — skipping full scan test"
            )
        # Optionally set environment variable for code that uses TESSERACT_PATH
        os.environ["TESSERACT_PATH"] = cls.tesseract_path

    @classmethod
    def tearDownClass(cls):
        for path in [cls.sample_image_path, cls.small_image_path, cls.text_file_path]:
            try:
                os.remove(path)
            except OSError:
                pass

    @patch("scan_image.scanner.logging")
    def test_scan_finds_correct_images(self, mock_logging):
        # Scan for phrase
        found = scanner.scan_images_for_phrase(self.test_dir, "HELLO_TEST")

        # Check that the sample OCR image is found
        self.assertIn(self.sample_image_path, found, "OCR image should be detected")

        # Check small image is ignored
        self.assertNotIn(self.small_image_path, found, "Small images below min size should be skipped")

        # Check non-image file is ignored
        self.assertNotIn(self.text_file_path, found, "Non-image files should be ignored")

        # Check all found images actually contain the phrase
        for img_path in found:
            self.assertTrue(utils.contains_phrase(img_path, "HELLO_TEST"), f"{img_path} does not contain phrase")

        # Check duplicates are removed (simulate by copying the same image)
        duplicate_path = os.path.join(self.test_dir, "duplicate.png")
        Image.open(self.sample_image_path).save(duplicate_path)
        found_with_duplicate = scanner.scan_images_for_phrase(self.test_dir, "HELLO_TEST")
        # Ensure only 1 image is returned for the hash
        self.assertEqual(len(found_with_duplicate), 1, "Duplicates should be removed")

        # Ensure that this image contains the phrase
        self.assertTrue(utils.contains_phrase(found_with_duplicate[0], "HELLO_TEST"),
                        "Returned image should contain the phrase")

        # Accept either path (original or duplicate)
        self.assertIn(os.path.basename(found_with_duplicate[0]),
              [os.path.basename(self.sample_image_path), os.path.basename(duplicate_path)],
              "Returned image should be either the original or the duplicate")
        try:
            os.remove(duplicate_path)
        except OSError:
            pass

    @patch("scan_image.scanner.logging")
    def test_scan_phrase_not_found(self, mock_logging):
        # Scan for a phrase that doesn't exist
        found = scanner.scan_images_for_phrase(self.test_dir, "NON_EXISTENT_PHRASE")
        self.assertEqual(found, [], "No images should be found for a phrase that doesn't exist")
