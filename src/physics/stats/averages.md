# Different Kinds of Averages

There are many more helpful and more detailed resources available.
Honestly, the [Wikipedia page on Average](https://en.wikipedia.org/wiki/Average)
is a great place to start.

### mean
The "arithmetic mean" (or "mean" for short, there are different kinds of means as well),
is the most common average. Simply add up all the values of the samples and divide by
the number of samples.

**Code**: [`np.mean`](https://numpy.org/doc/stable/reference/generated/numpy.mean.html)

How do we calculate the "error" on the mean? While the standard deviation shows the 
width of a normal distribution, what shows the "uncertainty" in how well we know what
the center of that distribution is? The value we use for this is "standard error of the
mean" (or just "standard error" for short). The 
[wikipedia page](https://en.wikipedia.org/wiki/Standard_error) gives a description 
in all its statistics glory, but for our purposes its helpful to remember that the
error of the mean is the standard deviation divided by the square root of the number
of samples.

### median
The middle number of the group of samples when ranked in order. If there are an even
number of samples, then take the arithmetic mean of the two samples in the middle.

**Code**: [`np.median`](https://numpy.org/doc/stable/reference/generated/numpy.median.html)

### weighted mean
Sometimes, the different samples should be weighted differently. In the arithmetic mean,
each sample carries the same weight (I think of it as importance). We can slightly augment
the arithmetic mean to consider weights by multipling each sample by its weight, adding these
up, and then dividing by the sum of weights. This is a nice definition since it simplifies
down to the regular arithmetic mean if all the weights are one.

Confusingly, NumPy has decided to implemented the weighted mean in their `average` function.
This is just due to a difference in vocabulary.

**Code**: [`np.average`](https://numpy.org/doc/stable/reference/generated/numpy.average.html)

### iterative mean
In a lot of the distributions we look at, there 
is a "core" distribution that is Gaussian, but the tails are distorted by other effects.
Sometimes, we only care about the core distribution and we want to intentionally cut away
the distorted tails so that we can study the "bulk" of the distribution. This is where
an iterative approach is helpful. We continue to take means and cut away outliers until
there are no outliers left. The main question then becomes: how do we define an outlier?
A simple definition that works well in our case since we usually have many samples is
to have any sample that is further from the mean by X standard deviations be considered
an outlier.

NumPy does not have a function for this type of mean to my knowledge, so we will construct
our own. The key aspect of NumPy I use is 
[boolean array indexing](https://numpy.org/doc/stable/user/basics.indexing.html#boolean-array-indexing)
which is one of many different ways NumPy allows you to access the contents of an array.
In this case, I access certain elements of an array by constructing another array of True/False
values (in the code below, this boolean array is called `selection`) and then when I use
that array as the "index" (the stuff between the square brackets), only the values of the
array that correspond to `True` values will be returned in the output array. I construct
this boolean array by [broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html)
a certain comparison against every element in the array. Using broadcasting shortens the
code by removing the manual `for` loop _and_ makes the code faster since NumPy can move that
`for` loop into it's under-the-hood, faster operations in C.

**Code**:
```python
import numpy as np

# first I write my own mean calculation that includes the possibility of weights
#   and returns the mean, standard deviation, and the error of the mean
def weightedmean(values, weights = None) :
    """calculate the weighted mean and standard deviation of the input values
    
    This function isn't /super/ necessary, but it is helpful for the itermean
    function below where the same code needs to be called in multiple times.
    """ 
    mean = np.average(values, weights=weights)
    stdd = np.sqrt(np.average((values-mean)**2, weights=weights))
    merr = stdd/np.sqrt(weights.sum())
    return mean, stdd, merr

# now I can write the iterative mean
def itermean(values, weights = None, *, sigma_cut = 3.0) :
    """calculate an iterative mean and standard deviation

    If no weights are provided, then we assume they are all one.
    The sigma_cut parameter is what defines what an outlier is.
    If a sample is further from the mean than the sigma_cut times
    the standard deviation, it is removed.
    """
    mean, stdd, merr = weightedmean(values, weights)
    num_included = len(values)+1 # just to get loop started
    # first selection is all non-zero weighted samples
    selection = (weights > 0) if weights is not None else np.full(len(values), True)
    while np.count_nonzero(selection) < num_included :
        # update number included for this mean
        num_included = np.count_nonzero(selection)
        # calculate mean and std dev
        mean, stdd, merr = weightedmean(values[selection], weights[selection] if weights is not None else None)
        # determine new selection, since this variable was defined outside
        #   the loop, we can use it in the `while` line and it will just be updated
        selection = (values > (mean - sigma_cut*stdd)) & (values < (mean + sigma_cut*stdd))

    # left loop, meaning we settled into a state where nothing is outside sigma_cut standard deviations
    #   from our mean
    return mean, stdd, merr
```

