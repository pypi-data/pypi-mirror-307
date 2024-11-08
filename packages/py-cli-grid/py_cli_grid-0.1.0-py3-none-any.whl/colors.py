class Color:
    """New class to manage TRUE COLOR in terminals"""

    @staticmethod
    def rgb_to_color_scape(r, g, b, background=False):
        """Transforms RGB code to terminal scape color"""
        return '\033[{};2;{};{};{}m'.format(48 if background else 38, r, g, b)

    @staticmethod
    def bold(text: str, reset: bool = True):
        return Color.BOLD + text + Color.RESET if reset else None

    @staticmethod
    def italic(text: str, reset: bool = True):
        return Color.ITALIC + text + Color.RESET if reset else None

    @staticmethod
    def blink(text: str, reset: bool = True):
        return Color.BLINK + text + Color.RESET if reset else None

    @staticmethod
    def blink_alt(text: str, reset: bool = True):
        return Color.BLINK2 + text + Color.RESET if reset else None

    @staticmethod
    def selected(text: str, reset: bool = True):
        return Color.SELECTED + text + Color.RESET if reset else None
    
    # Predefined styles
    RESET = '\33[0m'
    BOLD = '\33[1m'
    BOLD = '\33[1m'
    ITALIC = '\33[3m'
    URL = '\33[4m'
    BLINK = '\33[5m'
    BLINK2 = '\33[6m'
    SELECTED = '\33[7m'
