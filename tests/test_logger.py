import unittest
import logging
from unittest.mock import patch, MagicMock
from scan_image import logger

class TestLogger(unittest.TestCase):

    def test_success_level(self):
        """Custom SUCCESS level should log correctly."""
        log = logging.getLogger("test_success")
        with patch.object(log, "_log") as mock_log:
            log.success("Test success message")
            mock_log.assert_called_once()
            args, kwargs = mock_log.call_args
            self.assertEqual(args[0], logger.SUCCESS_LEVEL_NUM)  # Level
            self.assertEqual(args[1], "Test success message")    # Message

    def test_logger_success_function(self):
        """Global logger.success() should call logger._log correctly."""
        with patch("logging.getLogger") as mock_get_logger:
            mock_instance = MagicMock()
            mock_get_logger.return_value = mock_instance
            logger.success("Hello")
            mock_instance.success.assert_called_once_with("Hello")

    def test_color_formatter_output(self):
        """Formatter should return a string (with or without colors)."""
        log_record = logging.LogRecord(
            name="test", level=logging.INFO, pathname="", lineno=1,
            msg="Hello World", args=(), exc_info=None
        )
        formatter = logger.ColorFormatter("%(levelname)s: %(message)s")
        formatted = formatter.format(log_record)
        self.assertIn("Hello World", formatted)

    def test_setup_logging_adds_handler(self):
        """Ensure setup_logging adds at least one handler."""
        logger.setup_logging()
        root_logger = logging.getLogger()
        self.assertTrue(any(isinstance(h, logging.StreamHandler) for h in root_logger.handlers))


if __name__ == "__main__":
    unittest.main()
