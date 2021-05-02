import logging
from colorama import Fore, Style, init
init()  # For Window system


DEFAULT_FG_COLORS = {
    'WARNING': Fore.YELLOW,
    'INFO': Fore.WHITE,
    'DEBUG': Fore.BLUE,
    'CRITICAL': Fore.RED,
    'ERROR': Fore.RED
}

DEFAULT_STYLES = {
    'WARNING': Style.NORMAL,
    'INFO': Style.NORMAL,
    'DEBUG': Style.NORMAL,
    'CRITICAL': Style.BRIGHT,
    'ERROR': Style.NORMAL
}


class ColoredFormatter(logging.Formatter):
    """A formatter that can colour the levelname.
    It's a subclass of logging.Formatter.

    Attributes
    ----------
    level_colored : bool
        Specify if the level must be colored.
    fg_colors : Dict[str, str], format: {levelname: colorama.Fore constant}
        A dictionary with the color constant for each levelname
    styles : Dict[str, str], format: {levelname: colorama.Style constant}
        A dictionary with the style for each levelname
    """
    def __init__(self, fmt, level_colored = True, fg_colors: dict = DEFAULT_FG_COLORS, styles: dict = DEFAULT_STYLES, **kwargs):
        """Initialize an instance of Formatter

        Parameters
        ----------
        fmt : str
            The format passed to the logger
        OPTIONAL[level_colored] : bool
            Specify if the level must be colored.
            Default: True
        OPTIONAL[fg_colors] : Dict[str, str], format: {levelname: colorama.Fore constant}
            A dictionary with the color constant for each levelname
            Default: DEFAULT_FG_COLORS
        OPTIONAL[styles] : Dict[str, str], format: {levelname: colorama.Style constant}
            A dictionary with the style for each levelname
            Default: DEFAULT_STYLES
        """
        logging.Formatter.__init__(self, fmt, **kwargs)
        self.level_colored = level_colored
        self.fg_colors = fg_colors
        self.styles = styles

    def format(self, record):
        levelname = record.levelname
        if self.level_colored:
            style = self.styles[levelname] if levelname in self.styles else ""
            fg_color = self.fg_colors[levelname] if levelname in self.fg_colors else ""
            record.levelname = style + fg_color + levelname + Style.RESET_ALL
        return logging.Formatter.format(self, record)
