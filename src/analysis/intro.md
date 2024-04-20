# Analyzing ldmx-sw Event Files

Often when first starting on LDMX, people are given a `.root` file produced by ldmx-sw
(or some method for producing their own file). This then leads to the very next
and reasonable question -- how to analyze the data in this file?

Many answers to this question have been said and many of them are functional.
In subsequent sections of this chapter of the website, I choose to focus
on highlighting two possible analysis workflows that I personally
like (for different reasons). Below, I describe the various software tools of
which I am aware and the upsides and downsides of them from my point of view.

I am not able to fully cover all of the possible different types of analysis,
so I am writing this guide in the context of one of the most common analyses:
looking at a histogram. This type of analysis can be broken into three steps.
1. Data Manipulation: from the data already present, calculate the variable
    that you would like to put into the histogram.
2. Histogram Filling: define how the histogram should be binned and fill
    the histogram with the variable that you calculated.
3. Plotting: from the definition of the histogram and its content,
    draw the histogram in a visual manner for inspection.

The software that is used to do each of these steps is what mainly separates
the different analysis workflows, so I am first going to mention various
software tools that are helpful for one or more of these steps.

### ldmx-sw Analyzer
Data Manipulation and Histogram Filling

### Write a ROOT Macro

### PyROOT within a Python Script

### scikit-hep
