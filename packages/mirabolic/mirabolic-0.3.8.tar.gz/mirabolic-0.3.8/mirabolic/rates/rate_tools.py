import numpy as np
import pandas as pd
from scipy.stats import beta as beta_dist
from scipy.optimize import minimize_scalar
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Rectangle, Ellipse

sns.set()
# If you don't like Seaborn's look, switch back to vanilla
# graphing aesthetics by running:
#   sns.reset_orig()


def num_to_list(x):
    if isinstance(x, (int, float, np.int32, np.int64, np.float32, np.float64)):
        return [x]
    else:
        return x


def str_to_series(x, df):
    return ()


def highest_density_interval(alpha, beta, prob):
    """
    Find the shortest confidence/credibility interval of the beta(A,B) distribution
    containing probability "prob"
    """
    dist = beta_dist(alpha, beta)

    # Function to find the interval
    def interval_func(low_tail_prob):
        low_tail = dist.ppf(low_tail_prob)
        high_tail_prob = low_tail_prob + prob
        high_tail = dist.ppf(high_tail_prob)
        return high_tail - low_tail

    # Find the low tail probability that minimizes the interval width
    low_tail_prob = minimize_scalar(
        interval_func, bounds=(0, 1 - prob), method="bounded"
    ).x

    # Compute the interval
    low_tail = dist.ppf(low_tail_prob)
    high_tail_prob = low_tail_prob + prob
    high_tail = dist.ppf(high_tail_prob)

    return low_tail, high_tail


def rate_comparison(
    num_successes_A=None,
    num_successes_B=None,
    num_trials_A=None,
    num_trials_B=None,
    # Optional arguments
    labels=None,
    confidence=0.9,  # How big is our confidence/credibility interval?
    df=None,
    ax=None,
    plot_kwargs=None,
    plot=True,
    patch_type="rectangle",
    patch_alpha=0.3,
    label_font_size=8,
    xlabel="A arm",
    ylabel="B arm",
    title="Response Rate Correlation",
):
    """
    We run a series of A/B experiments.  In each experiment, we run a number of trials of
    the A arm and the B arm, recording the number of successes.  We're trying to estimate
    the probability that each arm succeeds.  The probability may differ between different
    experiments.

    This function computes the expected success rate and uncertainty for each experiment
    and (optionally) plots the results.
    """

    if plot_kwargs is None:
        plot_kwargs = {}
    if ax is None:
        ax = plt.gca()
    assert patch_type in ["ellipse", "rectangle"]

    num_successes = dict(A=num_successes_A, B=num_successes_B)
    num_trials = dict(A=num_trials_A, B=num_trials_B)
    arms = ["A", "B"]

    ###########################
    # Standardize input formats
    ###########################

    ## If input specified a single experiment by listing four numbers, convert to 4 singleton lists
    for arm in arms:
        num_successes[arm] = num_to_list(num_successes[arm])
        num_trials[arm] = num_to_list(num_trials[arm])

    ## If dataframe is specified, we assume arguments are the names of columns, not the
    ## columns themselves.
    if df is not None:
        for arm in arms:
            num_successes[arm] = df[num_successes[arm]].values
            num_trials[arm] = df[num_trials[arm]].values
        if labels is not None:
            labels = df[labels].values

    # Make sure consistent number of experiments
    num_experiments = len(num_successes["A"])
    if num_experiments == 0:
        raise ValueError("Must have at least 1 experiment!")
    for arm in arms:
        assert num_experiments == len(num_successes[arm])
        assert num_experiments == len(num_trials[arm])
        for i in range(num_experiments):
            assert num_trials[arm][i] >= 1
    if labels is not None:
        assert num_experiments == len(labels)

    assert confidence > 0
    assert confidence < 1

    #########################
    # Compute statistics
    #########################

    results = dict(num_experiments=num_experiments, confidence=confidence)
    for arm in arms:
        results[arm] = dict(rate=[], std_dev=[], low=[], high=[])

        for i in range(num_experiments):
            results[arm]["rate"].append(num_successes[arm][i] / num_trials[arm][i])
            # Beta distribution computations
            ## Set Beta parameters
            alpha = num_successes[arm][i] + 1
            ## Sigh.  The "Beta distribution" has a parameter traditionally called "beta".
            beta = num_trials[arm][i] + 1 - alpha
            ## Compute variance and thence standard deviation
            var = alpha * beta / ((alpha + beta) ** 2 * (alpha + beta + 1))
            results[arm]["std_dev"].append(np.sqrt(var))
            lower_bound, upper_bound = highest_density_interval(alpha, beta, confidence)
            results[arm]["low"].append(lower_bound)
            results[arm]["high"].append(upper_bound)

    if plot:
        # Draw a dotted line along the main diagonal
        mm, MM = np.inf, -np.inf
        for rate_A, rate_B in zip(results["A"]["low"], results["B"]["low"]):
            mm = min(mm, min(rate_A, rate_B))
        for rate_A, rate_B in zip(results["A"]["high"], results["B"]["high"]):
            MM = max(MM, max(rate_A, rate_B))
        ax.plot([mm, MM], [mm, MM], ":", color="black")

        color_list = sns.color_palette("deep", 8)
        legend_proxy, legend_label = [], []
        for i in range(num_experiments):
            facecolor = color_list[i % len(color_list)]
            edgecolor = color_list[i // len(color_list)]
            x_low, x_high = results["A"]["low"][i], results["A"]["high"][i]
            y_low, y_high = results["B"]["low"][i], results["B"]["high"][i]
            width = x_high - x_low
            height = y_high - y_low
            if patch_type == "ellipse":
                center_x = (x_low + x_high) / 2
                center_y = (y_low + y_high) / 2
                angle = 0
                patch = Ellipse(
                    (center_x, center_y),
                    width,
                    height,
                    edgecolor=edgecolor,
                    facecolor=facecolor,
                    alpha=patch_alpha,
                )
            elif patch_type == "rectangle":
                patch = Rectangle(
                    (x_low, y_low),
                    width,
                    height,
                    edgecolor=edgecolor,
                    facecolor=facecolor,
                    alpha=patch_alpha,
                )
            else:
                raise ValueError(f"Unknown path type {patch_type}")
            ax.add_patch(patch)
            if labels is not None:
                legend_proxy.append(
                    plt.Line2D(
                        [0],
                        [0],
                        linestyle="none",
                        marker="o",
                        markerfacecolor=facecolor,
                        markeredgecolor=edgecolor,
                        markersize=label_font_size,
                    )
                )
                legend_label.append(labels[i])
        if labels is not None:
            plt.legend(legend_proxy, legend_label, prop={"size": label_font_size})

        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.scatter(
            results["A"]["rate"], results["B"]["rate"], marker=".", color="black"
        )
        ax.set_aspect("equal")

    return results


if __name__ == "__main__":

    # Some synthetic data
    num_experiments = 8
    num_trials = 2000
    num_conversions_A = np.random.binomial(num_trials, 0.03, size=num_experiments)
    num_conversions_B = np.random.binomial(num_trials, 0.035, size=num_experiments)
    num_emails_A = num_experiments * [num_trials]
    num_emails_B = num_experiments * [num_trials]

    # Plot the figure
    plt.figure(figsize=(6, 6))
    results = rate_comparison(
        num_successes_A=num_conversions_A,
        num_successes_B=num_conversions_B,
        num_trials_A=num_emails_A,
        num_trials_B=num_emails_B,
    )
    plt.show()
