# Given a set of data, compute and plot confidence intervals
# for the corresponding CDF.

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from scipy.stats import binom, beta
from scipy.special import loggamma
from scipy import interpolate

# The beta distribution is the correct (pointwise) distribution
# across *quantiles* for a given *data point*; if you're not
# sure, this is probably the estimator you want to use.


def cdf_CI_marginal_quick(a=None, N=None, confidence=None, **kwargs):
    # The marginal distribution is beta-distributed, and this calculates a
    # (marginal) confidence interval exactly.  This interval is guaranteed
    # to contain the mode, but is not necessarily the smallest possible
    # confidence interval.

    b = N + 1 - a

    if a == 1:
        lower = 0
        upper = beta.ppf(confidence, a, b)
        return (lower, upper)
    if a == N:
        lower = beta.ppf(1 - confidence, a, b)
        upper = 1
        return (lower, upper)

    mode = (a - 1) / (a + b - 2)
    mode_cumu_prob = beta.cdf(mode, a, b)
    lower_prob = max(mode_cumu_prob - confidence * mode_cumu_prob, 0.0)
    # upper_prob = min(mode_cumu_prob + confidence * (1 - mode_cumu_prob),1.0)
    upper_prob = lower_prob + confidence
    lower = beta.ppf(lower_prob, a, b)
    upper = beta.ppf(upper_prob, a, b)

    return (lower, upper)


def cdf_CI_marginal_opt(a=None, N=None, confidence=None, max_steps=6, **kwargs):
    # The marginal distribution is beta-distributed, and this calculates a
    # (marginal) confidence interval exactly.  There are different choices
    # for the confidence interval.  If N>1, then there is a unique shortest
    # confidence interval; because the beta distribution is (usually)
    # asymmetric, computing this interval requires a little work.  (We use
    # Newton's method to optimize.)

    b = N + 1 - a

    if a == 1:
        lower = 0
        upper = beta.ppf(confidence, a, b)
        return (lower, upper)
    if a == N:
        lower = beta.ppf(1 - confidence, a, b)
        upper = 1
        return (lower, upper)

    # Choose a reasonable starting guess
    lower, upper = cdf_CI_marginal_quick(a=a, N=N, confidence=confidence, **kwargs)

    # We want a relatively small step size in the context of our
    # distribution
    delta = min(0.1 / (N ** 2), 0.0001)

    B_norm = np.exp(loggamma(a + b) - loggamma(a) - loggamma(b))

    # lower_guess should always be in [0, max_lower_guess]
    max_lower = beta.ppf(1 - confidence, a, b)

    def recover_upper(lower):
        prob = min(beta.cdf(lower, a, b) + confidence, 1.0)
        return beta.ppf(prob, a, b)

    def f_0(lower):
        # f_0 should be monotonically increasing for a,b>=2
        upper = recover_upper(lower)
        b_lower = beta.pdf(lower, a, b)
        b_upper = beta.pdf(upper, a, b)
        return b_lower - b_upper

    def f_1(lower, f_left=None):
        if f_left is None:
            f_left = f_0(lower)
        f_right = f_0(lower + delta)
        return (f_right - f_left) / delta

    for step_count in range(max_steps):
        f_0_val = f_0(lower)
        f_1_val = f_1(lower, f_left=f_0_val)
        step_size = f_0_val / f_1_val
        lower = lower - step_size
        # delta = min(delta, np.abs(step) / 100)
        if np.abs(step_size) < delta:
            break

    upper = recover_upper(lower)

    return (lower, upper)


# Compute Dvoretzky-Kiefer-Wolfowitz confidence bands.
def cdf_CI_DKW(a=None, N=None, confidence=None, **kwargs):
    # See, e.g.,
    # https://en.wikipedia.org/wiki/Dvoretzky%E2%80%93Kiefer%E2%80%93Wolfowitz_inequality
    epsilon = np.sqrt(np.log(2.0 / (1 - confidence)) / (2.0 * float(N)))

    y = ecdf_value(a, N, ecdf_type="classical")
    return (y - epsilon, y + epsilon)


def confidence_interval_bounds(**kwargs):
    bound = kwargs["bound"]
    confidence = kwargs["confidence"]

    if confidence == 0:
        v = ecdf_value(**kwargs)
        return (v, v)
    if confidence == 1:
        return (0, 1)

    if bound == "DKW":
        fn = cdf_CI_DKW
    elif bound == "marginal_quick":
        fn = cdf_CI_marginal_quick
    elif bound == "marginal_opt":
        fn = cdf_CI_marginal_opt
    else:
        raise ValueError(f"Unknown bound {bound}")

    lower, upper = fn(**kwargs)
    if lower < 0:
        lower = 0
    if upper > 1:
        upper = 1

    return (lower, upper)


def ecdf_value(a=None, N=None, ecdf_type=None, bound=None, **kwargs):
    assert a <= N

    # Note that the DKW inequality assumes the "classic"
    # definition of the empirical CDF, namely
    #
    #  ecdf(x) = (# samples <= x) / (# samples)
    #
    # However, we compute marginal CIs by minimizing
    # the size of the CI for the beta distribution; for
    # small confidence values, ecdf(x) may not
    # lie within the CI.  If, instead, we use the mode of the
    # beta distribution, we are guaranteed to fall within
    # the CI.
    #
    # So, we select the type of ecdf based on the estimator.
    if ecdf_type is None:
        if bound == "marginal_quick" or "marginal_opt":
            ecdf_type = "mode"
        elif bound == "DKW":
            ecdf_type = "classical"
        else:
            raise ValueError(f"Unknown bound {bound}")

    if ecdf_type == "classical":
        return a / N
    elif ecdf_type == "mean":
        return a / (N + 1)
    elif ecdf_type == "mode":
        return (a - 1) / (N - 1)
    else:
        ValueError(f"Unknown cdf_type {ecdf_type}")


def cdf_plot(
    # Key arguments
    data=None,
    confidence=0.9,  # How wide is the confidence interval/band?
    # Statistical and control parameters
    presorted=False,  # Is the data already sorted?
    bound="marginal_opt",  # What kind of CI? (E.g., DKW or marginal?)
    ecdf_type=None,  # Exactly how do we define the empirical CDF?
    max_points=128,  # How many points to compute?
    # Plotting parameters
    plot_figure=True,  # Should we plot the data (or only return the results?)
    color=None,
    ax=None,
    plot_central_kw=None,  # Arguments to pass to plot(CDF)
    plot_confidence_kw=None,  # Arguments to pass to plot(confidence band)
    seaborn=True,
):
    """
    Given a collection of real-valued observations, plot a CDF with a
    confidence band around the values.
    """

    # Check input arguments
    assert confidence >= 0 and confidence <= 1
    assert bound in {"marginal_quick", "marginal_opt", "DKW"}
    assert ecdf_type in {"classical", "mode", "mean", None}

    # Clean up data types
    if isinstance(data, pd.core.series.Series):
        # Extract data from PANDAS data frame
        data = data.values
    if not isinstance(data, np.ndarray):
        # Try to convert, e.g., list to Numpy array
        data = np.array(data)

    N = len(data)
    if N == 0:
        raise ValueError("Data length is zero!")

    # Make sure we have numbers...
    assert np.issubdtype(data.dtype, np.number)
    # Make sure no NaNs or Infs...
    if not np.isfinite(data).all():
        bad_index = np.min(np.where(~np.isfinite(data)))
        msg = f"Nonfinite values!  data[{bad_index}] = {data[bad_index]}"
        raise ValueError(msg)

    # Sort data if necessary
    if presorted == False:
        # We can't risk overwriting the original data, so we
        # make a copy.  (If data is presorted, we can skip this
        # and save the memory).
        data = np.sort(data)

    # If we have a lot of data, then we neither want nor need to
    # plot every point-- it would be very slow to compute, memory
    # intensive to plot, and uninformative (because the envelope
    # won't change much).  Instead, we plot only "max_points".
    # If you really want to plot everything, set that value to 0 or None.
    if max_points is None or max_points < 1:
        N_plot = N
    N_plot = min(N, max_points)
    # Choose N_plot numbers evenly spread between 0 and N-1 (inclusive)
    index_list = np.linspace(0, N - 1, N_plot).round().astype(int)

    # Compute estimates
    x = []
    y = []
    y_lower = []
    y_upper = []
    for i in index_list:
        a = i + 1
        x.append(data[i])  # i-th largest value
        y.append(ecdf_value(a=a, N=N, ecdf_type=ecdf_type, bound=bound))
        if N == 1:
            # Special case N==1 to avoid possible edge cases
            tail = (1.0 - confidence) / 2
            y_lower.append(tail)
            y_upper.append(1 - tail)
            break

        lower, upper = confidence_interval_bounds(
            a=a, N=N, confidence=confidence, bound=bound, ecdf_type=ecdf_type
        )
        y_lower.append(lower)
        y_upper.append(upper)
    x = np.array(x)
    y = np.array(y)
    y_upper = np.array(y_upper)
    y_lower = np.array(y_lower)

    if plot_figure:
        # Use Seaborn defaults if desired
        if seaborn:
            sns.set_theme()

        # Use specified or default Matplotlib axis
        if ax is None:
            ax = plt.gca()

        if plot_central_kw is None:
            plot_central_kw = {}
        if plot_confidence_kw is None:
            plot_confidence_kw = {}

        default_plot_confidence_kw = dict(alpha=0.3)
        default_plot_confidence_kw.update(plot_confidence_kw)
        plot_confidence_kw = default_plot_confidence_kw
        if color is not None:
            plot_central_kw.update({"color": color})
            plot_confidence_kw.update({"color": color})

        plt.plot(x, y, **plot_central_kw)
        plt.fill_between(x, y_lower, y_upper, **plot_confidence_kw)

    DKW_epsilon_bound = None
    if bound == "DKW":
        DKW_epsilon_bound = 1 - y_lower[-1]

    results = dict(
        x=x,
        y=y,
        y_lower=y_lower,
        y_upper=y_upper,
        index_list=index_list,
        DKW_epsilon_bound=DKW_epsilon_bound,
    )
    return results
