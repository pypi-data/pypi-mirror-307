from datetime import date
from enum import Enum

class PlotColors(Enum):
    ORANGE = 'orange'
    TEAL = 'teal'
    CRIMSON = 'crimson'
    MAGENTA = 'magenta'
    SKYBLUE = 'skyblue'
    GREEN = 'green'
    PURPLE = 'purple'
    GOLD = 'gold'
    NAVY = 'navy'
    LIME = 'lime'
    CYAN = 'cyan'
    PINK = 'pink'
    BROWN = 'brown'
    CHOCOLATE = 'chocolate'
    SALMON = 'salmon'
    SLATEBLUE = 'slateblue'
    OLIVE = 'olive'
    MAROON = 'maroon'
    DARKORANGE = 'darkorange'
    CORNFLOWERBLUE = 'cornflowerblue'

class PlotStyleConfig:
    BACKGROUND_COLOR = '#121212'
    AXIS_FACE_COLOR = '#080808'
    GRID_COLOR = '#303030'
    LINE_WIDTH = 1
    STYLE = 'dark_background'

DEFAULT_TIMEFRAME = f'2004-01-01 {date.today().strftime("%Y-%m-%d")}'
DEFAULT_CATEGORY = 31  # programming
DEFAULT_GEO = '' # worldwide

COLOR_LIST = [color.value for color in PlotColors]
