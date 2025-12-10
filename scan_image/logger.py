import logging

try:
    from colorama import Fore, Style, init as colorama_init
    colorama_init(autoreset=True)
    COLOR_ENABLED = True
except Exception:
    COLOR_ENABLED = False
    class Dummy:
        def __getattr__(self, _): return ""
    Fore = Style = Dummy()

# Custom SUCCESS level
SUCCESS_LEVEL_NUM = 25
logging.addLevelName(SUCCESS_LEVEL_NUM, "SUCCESS")

def _success(self, message, *args, **kwargs):
    if self.isEnabledFor(SUCCESS_LEVEL_NUM):
        self._log(SUCCESS_LEVEL_NUM, message, args, **kwargs)

logging.Logger.success = _success
def success(message, *args, **kwargs):
    logging.getLogger().success(message, *args, **kwargs)
setattr(logging, "success", success)

class ColorFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: Fore.CYAN,
        SUCCESS_LEVEL_NUM: Fore.LIGHTGREEN_EX + (Style.BRIGHT if COLOR_ENABLED else ""),
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.MAGENTA + (Style.BRIGHT if COLOR_ENABLED else ""),
    }
    def format(self, record):
        base = super().format(record)
        if not COLOR_ENABLED:
            return base
        color = self.COLORS.get(record.levelno, "")
        return f"{color}{base}{Style.RESET_ALL}"

def setup_logging():
    handler = logging.StreamHandler()
    formatter = ColorFormatter("%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")
    handler.setFormatter(formatter)
    logging.basicConfig(level=logging.INFO, handlers=[handler])
