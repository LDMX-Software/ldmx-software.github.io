# Resolution
What I (Tom Eichlersmith) mean when I say "resolution".

Many of the measurements we take form distributions that are 
[normal](https://en.wikipedia.org/wiki/Normal_distribution)
(a.k.a. Gaussian, a.k.a. bell).

A normal distribution is completely characterized by its mean and
its standard deviation. In order to compare several different normal
distributions with different means and get an idea about which is "wider"
than another, we can divide the standard deviation by the mean to get
(what I call) the _resolution_. [^1]

[^1]: The technical term for this value is the 
[Coefficent of Variation](https://en.wikipedia.org/wiki/Coefficient_of_variation)

For our purposes, a lower value for the resolution is better since that
means our measurement is more precise. Additionally, in simulations we
know what the true measurement value _should_ be and so we can compare
the mean to the true value to see how accurate our measurement is.

## Calculation
Calculating the mean and standard deviation are fairly common tasks,
so they are available from numpy:
[mean](https://numpy.org/doc/stable/reference/generated/numpy.mean.html)
and
[std](https://numpy.org/doc/stable/reference/generated/numpy.std.html).

So if I have a set of measurements, the following python code snippet
calculates the mean, std, resolution, and accuracy.
```python
import numpy as np
# below, I randomly generate "measurements" from a normal distribution
#   in our work with the ECal, these measurements will actually be
#   taken from the output of the simulation using uproot
true_value = 10
true_width = 5
measurements = np.random.normal(true_value, true_width, 10000)
mean = measurements.mean()
stdd = measurements.std()
resolution = stdd/mean
accuracy   = mean/true_value
```

Oftentimes, it is helpful to display the distribution of the data compared
to an _actual_ normal distribution to confirm that the data is _actually_
normal and our analysis makes sense. In this case, the following code
snippet is very helpful.
```python
import matplotlib.pyplot as plt
from scipy.stats import norm
import numpy as np
measurements = np.random.normal(true_value, true_width, 10000)

# plot the raw data has a histogram
bin_values, bin_edges, art = plt.hist(measurements, bins='auto', label='data')
bin_centers = (bin_edges[1:]+bin_edges[:-1])/2
# plot an actual normal distribution on top to see if the histogram follows that shape
plt.plot(bin_centers, norm.pdf(bin_centers, measurements.mean(), meansurements.std(), label='real normal')
```

**Brief Aside**:
Sometimes, we do not have access to the full list of actual measurements because
there are too many of them, so we only have access to the binned-data. In this case,
we can calculate an approximate mean and standard deviation using the center of the 
bins as the "measurements" and the values in the bins as the "weights".
```python
approx_mean = np.average(bin_centers, weights=bin_values)
approx_stdd = np.sqrt(np.average((bin_centers-approx_mean)**2, weights=bin_values))
```

## Plotting
There are several plots that are commonly made when studying the resolution of things.
I'm listing them here just as reference.

#### Symbols
Not necessarily standard but helpful to be on the same page.
- \\(E_{meas}\\) the reconstructed total energy measured by the ECal
- \\(E_{true}\\) the known energy of the particle entering the ECal
- \\(\\langle X \\rangle\\) the mean of samples of \\(X\\)
- \\(\\sigma_X\\) the standard deviation of samples of \\(X\\)

#### Plots
- Histogram of \\(E_{meas}/E_{true}\\): this helps us see the shap of the distributions and
  dividing by the known beam energy allows us to overlay several different beam energies
  and compare their shapes.
- Plot of \\(\\langle E_{meas} \\rangle/E_{true}\\) vs \\(\\langle E_{meas} \\rangle\\) shows how the mean changes with beam energy
- Plot of \\(\\sigma_E / \\langle E_{meas} \\rangle\\) vs \\(\\langle E_{meas} \\rangle\\) shows how the variation changes with beam energy
