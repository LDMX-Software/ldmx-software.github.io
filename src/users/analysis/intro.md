# Analyzing ldmx-sw Event Files

Often when first starting on LDMX, people are given a `.root` file produced by ldmx-sw
(or some method for producing their own file). This then leads to the very next
and reasonable question -- how to analyze the data in this file?

Many answers to this question have been said and many of them are functional.
In subsequent sections of this chapter of the website, I choose to focus
on highlighting two possible analysis workflows that I personally
like (for different reasons).

I am not able to fully cover all of the possible different types of analysis,
so I am writing this guide in the context of one of the most common analyses:
looking at a histogram. This type of analysis can be broken into four steps.
1. Load data: from a data file, load the information in that file into memory.
2. Data Manipulation: from the data already present, calculate the variable
    that you would like to put into the histogram.
3. Histogram Filling: define how the histogram should be binned and fill
    the histogram with the variable that you calculated.
4. Plotting: from the definition of the histogram and its content,
    draw the histogram in a visual manner for inspection.

The software that is used to do each of these steps is what mainly separates
the different analysis workflows, so I am first going to mention various
software tools that are helpful for one or more of these steps. I have separated
these tools into two "ecosystems", both of which are popularly used within
HEP.

Purpose | ROOT | scikit-hep
---|---|---
Load Data | `TFile`,`TTree` | `uproot`
Manipulate Data | `C++` Code | Vectorized Python with `awkward`
Fill Histograms | `TH1*` | `hist`,`boost_histogram`
Plot Histograms | `TBrowser`, `TCanvas` | `matplotlib`,`mplhep`

How one mixes and matches these tools is a personal choice,
especially since the LDMX collaboration has not landed on a
widely agreed-upon method for analysis. With this in mind,
I find it important to emphasize that the following subsections
are **examples** of analysis workflows -- a specific analyzer
can choose to mix and match the tools however they like.

### Caveat
While I (Tom Eichlersmith) have focused on two potential analysis
workflows, I do not mean to claim that I have tried all of them
and these two are "the best". I just mean to say that I have
drifted to these two analysis workflows over time as I've looked
for easier and better methods of analyzing data. If you have
an analysis workflow that you would like to share, add another
subsection to this chapter of the website!
