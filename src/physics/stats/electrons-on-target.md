# Electrons on Target
Generally, we find the equivalent electrons on target ($N_\text{EoT}^\text{equiv}$)
by multiplying the simulated number of electrons on target ($N_\mathrm{thrown}$)
by the biasing factor ($B$) increasing the rate of the process focused on for the sample.
If there is filtering in the simulation, the simulated number of electrons on target
_is not_ equal to the number of events in the output file.

Currently, the simulated number of electrons on target is stored as the "number of tries"
in the `RunHeader`.

~~~admonish note title="Caveat Depending on ldmx-sw Version" collapsible=true
Samples created with ldmx-sw verions newer than v3.3.4 ($\geq$ v3.3.5) have an update
to the processing framework to store this information more directly
(in the `numTries_` member of the RunHeader or $\leq$ v4.4.7 and the `num_tries_` member
for newer).
Samples created with ldmx-sw versions older than v3.1.12 ($\leq$ v3.1.11) have access
to the "Events Began" field of the `intParameters_` member of the RunHeader.

The easiest way to know for certain the number of tries is to just set the maximum
number of events to your desired number of tries $N_\mathrm{thrown}$ and limit the
number of tries per output event to one `p.maxTriesPerEvent = 1` and `p.maxEvents = Nthrown`
in the config script.
~~~

In the thin-target regime, this is satisfactory since the process we care about either
happens (with the biasing factor applied) or does not (and is filtered out).
In thicker target scenarios (like the Ecal), we need to account for events where
unbiased processes happen to a particle _before_ the biased process.
Geant4 accounts for this while stepping tracks through volumes with
biasing operators attached and we include the weights of all steps in the overall event
weight in our simulation.
We can then calculate an effective biasing factor by dividing the total number of events
in the output sample ($N_\mathrm{sampled}$) by the sum of their event weights ($\sum w$).
In the thin-target regime (where nothing happens to a biased particle besides the
biased process), this equation reduces to the simpler $B N_\mathrm{thrown}$ used in other
analyses since biased tracks in \textsc{Geant}4 begin with a weight of $1/B$.
$$
N_\text{EoT}^\text{equiv} = \frac{N_\mathrm{sampled}}{\sum w}N_\mathrm{thrown}
$$

## Event Yield Estimation
Each of the simulated events has a weight that accounts for the biasing that was applied.
This weight quantitatively estimates how many _unbiased_ events this single
_biased_ event represents.
Thus, if we want to estimate the total number of events produced for a desired EoT
(the "event yield"), we would sum the weights and then scale this weight sum by the ratio
between our desired EoT $N_\text{EoT}$ and our actual simulated EoT $N_\text{thrown}$.
$$
N_\text{yield} = \frac{N_\text{EoT}}{N_\text{thrown}}\sum w
$$
Notice that $N_\text{yield} = N_\text{sampled}$ if we use
$N_\text{EoT} = N_\text{EoT}^\text{equiv}$ from before.
Of particular importance, the scaling factor out front is constant across all events
for any single simulation sample, so (for example) we can apply it to the contents of a
histogram so that the bin heights represent the event yield within $N_\text{EoT}$ events
rather than just the weight sum (which is equivalent to $N_\text{EoT} = N_\text{thrown}$).

## More Complexity
Include Einar's notes here...
