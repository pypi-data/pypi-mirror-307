import matplotlib.pyplot as plt
from .config import COLOR_LIST, PlotStyleConfig

def plot_interest_over_time(data, keywords):
    plt.style.use(PlotStyleConfig.STYLE)
    plt.figure().patch.set_facecolor(PlotStyleConfig.BACKGROUND_COLOR)
    ax = plt.axes()
    ax.set_facecolor(PlotStyleConfig.AXIS_FACE_COLOR)

    for i, keyword in enumerate(keywords):
        color = COLOR_LIST[i % len(COLOR_LIST)]  # handles cases with more keywords than available colors
        plt.plot(data[keyword], color=color, label=keyword, linewidth=PlotStyleConfig.LINE_WIDTH)

    plt.legend()
    plt.grid(color=PlotStyleConfig.GRID_COLOR)
    # saves png in current directory
    # plt.savefig(f'{"_".join(keywords)}.png', dpi=120)
    plt.show()
