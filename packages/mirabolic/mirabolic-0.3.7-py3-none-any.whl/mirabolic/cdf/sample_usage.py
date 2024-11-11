import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

import mirabolic

# We provide examples of plotting a CDF with a confidence
# envelope using mirabolic.cdf_plot()

# Make some data to plot
data = np.random.randn(120)


##############
# A basic plot
#
# By default, we use a "90% marginal credible interval",
# which means that if take any data point, there is a 90%
# probability that it falls within the shaded region above
# it (so, we should think of a vertical interval).  Note
# that the chance that *all* the data points jointly fall
# in their credible interval is less than 90%; if you
# want a joint bound, see the next example.
plt.figure()
mirabolic.cdf_plot(data=data, seaborn=True)
plt.title("Figure 1: Default behavior\n90% Marginal CI")


################################################################
# The DKW Inequality gives us a bound that *all* the data points
# will *simultaneously* fall within the confidence envelope.
plt.figure()
mirabolic.cdf_plot(data=data, bound="DKW", confidence=0.75, color="purple")
plt.title("Figure 2: Joint bound (DKW)\nProbability all data lies envelope is >=75% ")


##################
# Fancier plotting
f, (ax1, ax2) = plt.subplots(1, 2)

plot_central_kw = {"color": "green", "linestyle": "dotted", "marker": "o"}
plot_confidence_kw = {"color": "blue", "alpha": 0.1}
mirabolic.cdf_plot(
    data=data,
    bound="DKW",
    ax=ax2,
    plot_central_kw=plot_central_kw,
    plot_confidence_kw=plot_confidence_kw,
)
f.suptitle("Figure 3: Fancier Plotting")
ax1.set_title("Histogram")
ax1.hist(data)

ax2.set_title("CDF")
ax2.plot([0, 1], [0, 0.8], color="red")
plt.tight_layout()


###########################
# Cut corners to run faster
sorted_data = np.sort(data)

plt.figure()
plt.title("Figure 4: Speed up compute & rendering")
mirabolic.cdf_plot(
    data=sorted_data, presorted=True, bound="marginal_quick", max_points=64
)


plt.show()
