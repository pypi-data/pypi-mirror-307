# Produce a Q-Q plot.  For details, see:
# https://en.wikipedia.org/wiki/Q%E2%80%93Q_plot

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set()


def qq_plot(
    x,
    y,
    N=300,  # How many points to plot? 300 is probably plenty.
    outlier_q=0.1,  # Restrict plot to inliers. "0.0" plots all.
    plot=True,
    ax=None,
    color=None,
    marker=None,  # e.g.: "o", ".", "x"
    linestyle=None,  # e.g.: "-", "--", or no line: ""
    alpha=None,
    label=None,
):
    """
    Construct a Q-Q plot between data sets "x" and "y".
    Plots N equally-spaced quantiles.  Returns the matched
    quantiles.
    """
    assert outlier_q < 0.5
    if len(x) == len(y):
        # If |x| == |y| and the data sets are relatively
        # small, then just plot the matching points.
        N = min(N, len(x))
    x = np.sort(x)
    y = np.sort(y)
    q = np.linspace(0, 1, N)
    x_q = np.interp(q, np.linspace(0, 1, len(x)), x)
    y_q = np.interp(q, np.linspace(0, 1, len(y)), y)
    if plot:
        if ax is None:
            ax = plt.gca()
        plt.plot(
            x_q,
            y_q,
            color=color,
            marker=marker,
            linestyle=linestyle,
            alpha=alpha,
            label=label,
        )
        if outlier_q > 0:
            low_x_q = np.interp(outlier_q, np.linspace(0, 1, len(x)), x)
            high_x_q = np.interp(1 - outlier_q, np.linspace(0, 1, len(x)), x)
            estimated_extra = outlier_q * (high_x_q - low_x_q) / (1 - 2 * outlier_q)
            ax.set_xlim([low_x_q - estimated_extra, high_x_q + estimated_extra])

            low_y_q = np.interp(outlier_q, np.linspace(0, 1, len(y)), y)
            high_y_q = np.interp(1 - outlier_q, np.linspace(0, 1, len(y)), y)
            estimated_extra = outlier_q * (high_y_q - low_y_q) / (1 - 2 * outlier_q)
            ax.set_ylim([low_y_q - 2 * estimated_extra, high_y_q + 2 * estimated_extra])
    return (x_q, y_q)
