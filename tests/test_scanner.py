import os
import sys
import unittest
from unittest.mock import patch, MagicMock, call
from scan_image import scanner as main
from scan_image.scanner import scan_images_for_phrase

class TestMain(unittest.TestCase):

    @patch("scan_image.scanner.os.path.isdir", return_value=True)
    @patch("scan_image.scanner.scan_images_for_phrase", return_value=["/images/img1.png", "/images/img2.png"])
    @patch("scan_image.scanner.logging")
    def test_main_with_arguments(self, mock_logging, mock_scan, mock_isdir):
        """Ensure main() behaves correctly with CLI args."""
        test_args = ["scanner.py", "-f", "/test/path", "-p", "hello"]
        with patch.object(sys, "argv", test_args):
            main.main()

        expected_path = os.path.normpath("/test/path")
        mock_isdir.assert_called_once_with(expected_path)
        mock_scan.assert_called_once_with(expected_path, "hello")
        self.assertTrue(mock_logging.success.called)

    @patch("scan_image.scanner.os.path.isdir", return_value=True)
    @patch("scan_image.scanner.scan_images_for_phrase", return_value=[])
    @patch("scan_image.scanner.logging")
    def test_main_no_results(self, mock_logging, mock_scan, mock_isdir):
        """Should warn when no images match."""
        test_args = ["scanner.py", "-f", "/folder", "-p", "test"]
        with patch.object(sys, "argv", test_args):
            main.main()

        mock_logging.warning.assert_called_with("No images contain the phrase.")

    @patch("scan_image.scanner.os.path.isdir", return_value=False)
    @patch("scan_image.scanner.logging")
    def test_main_invalid_folder(self, mock_logging, mock_isdir):
        """Should exit when a bad folder is provided."""
        test_args = ["scanner.py", "-f", "/bad/path", "-p", "phrase"]
        with patch.object(sys, "argv", test_args):
            with self.assertRaises(SystemExit):
                main.main()

        mock_logging.error.assert_called_once()

    @patch("scan_image.scanner.input", side_effect=["/folder/interactive", "search phrase"])
    @patch("scan_image.scanner.os.path.isdir", return_value=True)
    @patch("scan_image.scanner.scan_images_for_phrase", return_value=["/images/a.png"])
    @patch("scan_image.scanner.logging")
    def test_main_interactive(self, mock_logging, mock_scan, mock_isdir, mock_input):
        """Should prompt user for folder + phrase when args missing."""
        test_args = ["scanner.py"]  # no CLI args
        with patch.object(sys, "argv", test_args):
            main.main()

        mock_input.assert_has_calls([
            call("Enter the folder path to scan: "),
            call("Enter the phrase to search for: ")
        ])
        mock_scan.assert_called_once_with("/folder/interactive", "search phrase")

    @patch("scan_image.scanner.os.walk")
    @patch("scan_image.scanner.cpu_count", return_value=4)
    @patch("scan_image.scanner.Pool")
    @patch("scan_image.scanner.logging")
    def test_scan_images_for_phrase(self, mock_logging, mock_pool, mock_cpu, mock_walk):
        """Test scan_images_for_phrase logic (without OCR)."""

        # Fake directory listing
        mock_walk.return_value = [
            ("/folder", [], ["a.jpg", "b.jpg", "c.txt"])  # only jpg processed
        ]

        # Fake multiprocessing pool
        pool_instance = MagicMock()
        mock_pool.return_value.__enter__.return_value = pool_instance

        # imap_unordered simulated behavior
        pool_instance.imap_unordered.return_value = [
            ("/folder/a.jpg", "hash1"),
            ("/folder/b.jpg", "hash1"),  # duplicate
            None
        ]

        result = scan_images_for_phrase("/folder", "hello")

        self.assertEqual(result, ["/folder/a.jpg"])
        mock_walk.assert_called_once()
        mock_pool.assert_called_once()


if __name__ == "__main__":
    unittest.main()
