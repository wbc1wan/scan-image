import unittest
from unittest.mock import patch
from scan_image import config

class TestSetupTesseract(unittest.TestCase):

    @patch("scan_image.config.logging")
    @patch("scan_image.config.pytesseract.get_tesseract_version", return_value="5.4.0")
    @patch("scan_image.config.os.getenv", return_value="C:/Tesseract/tesseract.exe")
    def test_setup_tesseract_with_env_path(self, mock_getenv, mock_version, mock_logging):
        """TESSERACT_PATH is set → should assign tesseract_cmd and log version."""
        
        # Mock the internal pytesseract namespace
        with patch("scan_image.config.pytesseract.pytesseract") as mock_cmd:
            config.setup_tesseract()

            mock_getenv.assert_called_once_with("TESSERACT_PATH")
            self.assertEqual(
                mock_cmd.tesseract_cmd,
                "C:/Tesseract/tesseract.exe"
            )

            mock_version.assert_called_once()
            mock_logging.debug.assert_called()  # version log


    @patch("scan_image.config.logging")
    @patch("scan_image.config.pytesseract.get_tesseract_version",
           side_effect=Exception("not installed"))
    @patch("scan_image.config.os.getenv", return_value=None)
    def test_setup_tesseract_missing_binary(self, mock_getenv, mock_version, mock_logging):
        """Tesseract not installed → should log an error."""
        
        # Mock the exception type inside pytesseract
        with patch("scan_image.config.pytesseract.pytesseract.TesseractNotFoundError", Exception):

            config.setup_tesseract()

            mock_getenv.assert_called_once_with("TESSERACT_PATH")
            mock_logging.error.assert_called_once()
