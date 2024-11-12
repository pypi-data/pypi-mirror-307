# Some unit tests (to be run through "pytest") to validate
# "cdf_tools.cdf_plot()". We focus less on code edge cases
# and more on checking statistical correctness.

import numpy as np
import sys
import os
import matplotlib.pyplot as plt
from scipy.stats import beta

# Get parent directory on import path
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

# Import "cdf_plot" (from parent directory)
from cdf_tools import cdf_plot


def wassert(x, warning):
    if not x:
        print(warning)
        assert x


def vec_assert(x, warning):
    for i in range(len(x)):
        if not x[i]:
            print(warning + f":  x[{i}]={x[i]}")
            assert x[i]


def test_minimal():
    # Make sure it runs without crashing and quantiles are in [0,1].
    # Low bar to success :)
    N = 100
    unsorted_data = np.random.randn(N)
    sorted_data = np.sort(unsorted_data)
    for presorted in [True, False]:
        if presorted:
            data = sorted_data
        else:
            data = unsorted_data
        for bound in ["marginal_quick", "marginal_opt", "DKW"]:
            warning1 = f"ERROR MESSAGE: sorted={sorted}, N={N}, bound={bound}"
            for confidence in [0, 0.5, 0.95, 1.0]:
                warning2 = warning1 + f", conf={confidence}"
                for plot_figure in [True, False]:
                    results = cdf_plot(
                        data=data,
                        bound=bound,
                        confidence=confidence,
                        plot_figure=plot_figure,
                        presorted=presorted,
                    )
                    if plot_figure:
                        plt.close(plt.gcf())
                for k in ["y", "y_lower", "y_upper"]:
                    warning3 = warning2 + f", k={k}"
                    r = results[k]
                    # Check that the quantiles actually lie in [0, 1]
                    vec_assert(np.isfinite(r), warning3)
                    vec_assert(r <= 1.0, warning3)
                    vec_assert(r >= 0.0, warning3)


def test_statistical():
    # Let's check that the statistics work correctly.

    num_trials = 10000
    N_list = [3, 4, 15, 512]
    confidence_list = [0.5, 0.95]

    for N in N_list:
        data = np.random.randn(N)
        for confidence in confidence_list:
            warning1 = f"ERROR: N={N}, conf={confidence}"
            # Test marginals (pointwise CI)
            for bound in ["marginal_quick", "marginal_opt"]:
                warning2 = warning1 + f", bound={bound}"
                results = cdf_plot(
                    data=data, bound=bound, confidence=confidence, plot_figure=False
                )
                i_len = len(results["index_list"])
                i_list = np.unique([0, 1, i_len // 2, i_len - 1])
                a_list = results["index_list"][i_list] + 1
                for a, i in zip(a_list, i_list):
                    warning3 = warning2 + f", x={i}"
                    b = N + 1 - a
                    # The following check presupposes that (1) beta() in scipy
                    # works correctly, and (2) we are interpreting the math
                    # correctly.  But if so, it's fast and exact
                    prob = beta.cdf(results["y_upper"][i], a, b) - beta.cdf(
                        results["y_lower"][i], a, b
                    )
                    warning3 += f", conf={confidence}, prob={prob}"
                    wassert(np.isclose(prob, confidence), warning3)

            # Test envelope (DKW)
            bound = "DKW"
            success_count = 0
            for trial in range(num_trials):
                results = cdf_plot(
                    data=np.random.uniform(size=N),
                    bound=bound,
                    confidence=confidence,
                    plot_figure=False,
                )
                if (results["x"] >= results["y_lower"]).all() and (
                    results["x"] <= results["y_upper"]
                ).all():
                    success_count += 1
            success_prob = success_count / num_trials

            # The DKW bound guarantees that, in expectation,
            #    success_prob >= confidence
            # If we are "lucky", it may be tighter and
            #    success_prob ~= confidence
            # In the latter case, if we take a Monte Carlo
            # estimate of "success_prob", we may still observe
            #    sampled(success_prob) < confidence
            # (say) half the time.  To avoid this, we add a few
            # standard deviations (a "fudge factor") to account
            # for the risk of sampling noise.  (Since the underlying
            # samples are Bernoulli, that's easy to compute.)
            fudge_sigmas = 6
            fudge_factor = np.sqrt(success_prob * (1 - success_prob) / num_trials)
            fudged_success_prob = success_prob + fudge_sigmas * fudge_factor

            check = fudged_success_prob > confidence
            assert check
