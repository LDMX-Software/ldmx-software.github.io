# Multi-Bin Exclusion Limit with Combine

These notes were written while using Combine v9.2.1.
Please reference [Combine's own documentation](https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/latest/)
when replicating this work and extending it to more
complicated situations.
In addition, these are *not* meant to be a full introduction
to the statistical procedures within Combine (again, refer to
its documentation), instead these notes are just meant as an example
guide on how one could use Combine.

## Set Up
Fortunately, [Combine distributes a container image](https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/latest/#oustide-of-cmssw-recommended-for-non-cms-users) distinct from CMSSW.
This enables us to choose a version of Combine and (almost) immediately begin.
In order to pin the version, avoid typing longer commands, and have the same command across
multiple runners, I use this image `denv`.
```
# initialize with combine version, may change version tag at end if desired
denv init --clean-env gitlab-registry.cern.ch/cms-cloud/combine-standalone:v9.2.1
# --clean-env is necessary for denv currently due to sharing of the LD_LIBRARY_PATH variable
# https://github.com/tomeichlersmith/denv/issues/110
```

## Usage
Roughly, we can partition using Combine into three steps.
1. Preparing the inputs to Combine
2. Running Combine
3. Interpreting the results from Combine

I've done the first and last steps within Python in a Jupyter notebook;
however, one could easily use Python scripts, ROOT macros, or
some other form of text file creation and TTree reading and plotting.

### Input Preparation
The main input to Combine is a text file called a "datacard" where we
specify the observed event counts, the expected event counts for the
different processes and the uncertainties on these event counts for
these different processes.
Again, I refer you to [the Combine documentation](https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/latest/part2/settinguptheanalysis/)
for some tutorials on writing these datacards.
Below, I include an example datacard where I have a 3-bin analysis
with only two processes (signal and background).

~~~admonish note title="Example 3-bin 2-process Data Card" collapsible=true
```
# counting experiment with multiple channels
# combine datacard generated on 2024-05-16 17:21:40
imax 3  number of channels
jmax 1  number of backgrounds
kmax 5  number of nuisance parameters
------------
# number of observed events in each channel
bin low med high
observation  1 10 100
------------
# list the expectation for signal and background processes in each of the channels
bin           low low med med high high 
process       ap bkg ap bkg ap bkg 
process       0 1 0 1 0 1 
rate          0.400000 1.000000 0.300000 10.000000 0.200000 100.000000 
------------
# list the sources of systematic uncertainty
sigrate lnN   1.200000 - 1.200000 - 1.200000 - 
lowstat lnN   - 2.000000 - - - - 
medstat lnN   - - - 1.316228 - - 
highstat lnN  - - - - - 1.100000 
bkgdsyst lnN  - 1.050000 - 1.050000 - 1.050000 
```
~~~

A few personal notes on the datacards.
- The datacard syntax is a custom space-separated syntax that is somewhat difficult
  to edit manually. As such, there are many tools that write datacards to be subsequently
  read by `combine` (The above example was actually written by just some Python I wrote
  to convert my histograms into this textual format.)
- When uncertainties appear on the same line, they are treated as correlated by `combine`
  (the `bkgdsyst` uncertainty in the example). Simiarly, appearing on separate lines means
  they are uncorrelated (the `*stat` uncertainties in the example).
- The total signal process rate (the sum over the `ap` process across all bins) is
  normalized to one so that interpreting the result is easier.

### Running
There are a plethora of command line options for `combine` that I
will not go into here. Instead, I just have two comments.
1. In a low-background scenario, the asymptotic limits are not as trustworthy,
  so it is better to use the `--method HybridNew` rather than the default.
  This method does the full CLs technique with toy experiment generation.
  We can use the suggested settings for this method using the `--LHCmode LHC-limits`
  argument.
2. One can label different runs within the output TTree with `--mass` and
  `--keyword-value` such that the resulting ROOT files can be `hadd`ed together
  into a single file containing all of the limits for the different runs
  of `combine`.

For a single datacard example,
```
denv combine --datacard datacard.txt --method HybridNew --LHCmode LHC-limits
```
Often, we want to estimate an exclusion for our different mass points as well.
The brute-force way to do this is to simply write a datacard for each masspoint
(if the mass point changes the signal rate fraction in each bin for example)
and then run `combine` for each of these datacards while changing the `--mass` label.
```
for m in 1 10 100 1000; do
  denv combine \
    --datacard datacard-${m}.txt \
    --method HybridNew \
    --LHCmode LHC-limits \
    --mass ${m} || break
done
denv hadd higgsCombineTest.HybridNew.root higgsCombineTest.HybridNew.mH*.root
```
~~~admonish warning title="Without Mass Argument"
Without the `--mass` argument (or another `--keyword-value` arugment) that
allows separation of the resulting limits in the ROOT files, the merged
ROOT file will have several limit values but no way for you to determine
which corresponds to the different inputs.
~~~

~~~admonish tip title="Parallelize Combine"
With GNU parallel installed, it is pretty easy to parallelize
this running of combine since none of the runs depend on each other.
```
parallel \
  --joblog combine.log \
  denv combine \
    --method HybridNew \
    --mass {} \
    --datacard datacard-{}.txt \
  ::: 1 10 100 1000
```
And then `hadd` the same was as above.
~~~

### Result Interpretation
The output from Combine is stored into a TTree within a ROOT file
[with a simple and well-defined schema](https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/latest/part3/runningthetool/#output-from-combine).
For the `HybridNew` method, the `limit` branch of the TTree is
the upper limit on \\(r = N_\text{sig}/N_\text{sig}^\text{exp}\\)
where \\(N_\text{sig}^\text{exp}\\) is the total number of expected
signal events across all bins (hence, why we set this number to one
when creating the datacard above).

Again, here I used Python within a Jupyter notebook to access this
TTree (via `uproot`) and plot the results (via `matplotlib` and `mplhep`).
Since we normalized the expected signal to one, the resulting limit
can be interpreted as the maximum number of signal events allowed.
This can then be converted into a limit on the dark sector mixing
strength \\(\epsilon\\) with knowledge of the total signal production
rate \\(R_{\epsilon=1}\\) and the signal efficiency \\(E\\).
\\[
N_\text{sig} = \epsilon^2 E R_{\epsilon=1}
\quad\Rightarrow\quad
\epsilon_\text{up}^2 = \frac{E R_{\epsilon=1}}{r}
\\]
where \\(r\\) is a stand-in for the value of the `limit` branch from
the Combine output ROOT file. Futher conversion of this mixing strength
into an effective interaction strength \\(y\\) is commonly done using
the dark sector interaction strength \\(\alpha_D\\) and the ratio of
the dark fermion mass to the dark photon mass \\(m_\chi/m_{A'}\\).
\\[
y_\text{up}
= \alpha_D\left(m_\chi/m_{A'}\right)^4\epsilon_\text{up}^2
= \alpha_D\left(m_\chi/m_{A'}\right)^4\frac{E R_{\epsilon=1}}{r}
\\]
