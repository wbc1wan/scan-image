import unittest
import numpy as np
from unittest.mock import patch, MagicMock
from scan_image import utils

class TestUtils(unittest.TestCase):

    @patch("scan_image.utils.IMAGE_EXTENSIONS", [".jpg", ".png"])
    @patch("scan_image.utils.Image.open")
    def test_is_valid_image_valid(self, mock_open):
        """Valid image with correct size returns True."""
        mock_img = MagicMock()
        mock_img.width = 300
        mock_img.height = 300

        # Image.open first call for verify(), second for size check
        mock_open.return_value.__enter__.return_value = mock_img

        self.assertTrue(utils.is_valid_image("file.jpg"))

    @patch("scan_image.utils.IMAGE_EXTENSIONS", [".jpg"])
    def test_is_valid_image_invalid_extension(self):
        """Unsupported extension returns False."""
        self.assertFalse(utils.is_valid_image("file.gif"))

    @patch("scan_image.utils.IMAGE_EXTENSIONS", [".jpg"])
    @patch("scan_image.utils.Image.open", side_effect=Exception("cannot open"))
    def test_is_valid_image_corrupted(self, mock_open):
        """Corrupted or unreadable file returns False."""
        self.assertFalse(utils.is_valid_image("file.jpg"))

    @patch("scan_image.utils.IMAGE_EXTENSIONS", [".jpg"])
    @patch("scan_image.utils.MIN_WIDTH", 100)
    @patch("scan_image.utils.MIN_HEIGHT", 100)
    @patch("scan_image.utils.Image.open")
    def test_is_valid_image_too_small(self, mock_open):
        """Image smaller than min size returns False."""
        img_mock = MagicMock()
        img_mock.width = 50
        img_mock.height = 50
        mock_open.return_value.__enter__.return_value = img_mock

        self.assertFalse(utils.is_valid_image("file.jpg"))

    @patch("scan_image.utils.cv2.imread")
    @patch("scan_image.utils.cv2.Canny")
    def test_has_text_heuristic_detects_text(self, mock_canny, mock_read):
        fake_img = np.ones((100, 100), dtype=np.uint8)
        fake_edges = np.ones((100, 100), dtype=np.uint8) * 255

        mock_read.return_value = fake_img
        mock_canny.return_value = fake_edges

        self.assertTrue(utils.has_text_heuristic("file.jpg"))

    @patch("scan_image.utils.cv2.imread", return_value=None)
    def test_has_text_heuristic_invalid_image(self, mock_read):
        self.assertFalse(utils.has_text_heuristic("no_image.png"))

    @patch("scan_image.utils.logging")
    @patch("scan_image.utils.cv2.imread", side_effect=Exception("cv2 error"))
    def test_has_text_heuristic_exception(self, mock_read, mock_log):
        """Exceptions should log an error and return False."""
        self.assertFalse(utils.has_text_heuristic("crash.png"))
        mock_log.error.assert_called()

    @patch("scan_image.utils.cv2.imread")
    @patch("scan_image.utils.cv2.Canny")
    def test_has_text_heuristic_no_edges(self, mock_canny, mock_read):
        fake_img = np.ones((100, 100), dtype=np.uint8)
        zero_edges = np.zeros((100, 100), dtype=np.uint8)

        mock_read.return_value = fake_img
        mock_canny.return_value = zero_edges

        self.assertFalse(utils.has_text_heuristic("empty.png"))

    @patch("scan_image.utils.imagehash.phash", return_value="hash123")
    @patch("scan_image.utils.Image.open")
    def test_compute_perceptual_hash(self, mock_open, mock_hash):
        """phash() should be called properly."""
        result = utils.compute_perceptual_hash("file.jpg")
        self.assertEqual(result, "hash123")
        mock_hash.assert_called_once()

    @patch("scan_image.utils.pytesseract.image_to_string", return_value="Hello THIS is a Test!")
    @patch("scan_image.utils.Image.open")
    @patch("scan_image.utils.logging")
    def test_contains_phrase_found(self, mock_log, mock_open, mock_ocr):
        """Phrase detection is case-insensitive."""
        result = utils.contains_phrase("img.png", "test")
        self.assertTrue(result)
        mock_log.debug.assert_called()  # logs OCR snippet

    @patch("scan_image.utils.pytesseract.image_to_string", return_value="No match here")
    @patch("scan_image.utils.Image.open")
    def test_contains_phrase_not_found(self, mock_open, mock_ocr):
        result = utils.contains_phrase("img.png", "missing")
        self.assertFalse(result)

    @patch("scan_image.utils.logging")
    @patch("scan_image.utils.Image.open", side_effect=Exception("OCR crash"))
    def test_contains_phrase_exception(self, mock_open, mock_log):
        """OCR errors should log and return False."""
        result = utils.contains_phrase("file.jpg", "test")
        self.assertFalse(result)
        mock_log.error.assert_called()


if __name__ == "__main__":
    unittest.main()
