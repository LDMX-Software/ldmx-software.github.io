# Electrons on Target
The number of "Electrons on Target" (EoT) of a simulated or collected data sample
is an important measure on the quantity of data the sample represents.
Estimating this number depends on how the sample was constructed.

## Real Data Collection
For real data, the accelerator folks at SLAC construct a beam that has a few parameters we can
measure (or they can measure and then tell us).
- duty cycle \\(d\\): the fraction of time that the beam is delivering bunches
- rate \\(r\\): how quickly bunches are delivered
- multiplicity \\(\mu\\): the Poisson average number of electrons per bunch

The first two parameters can be used to estimate the number of bunches the beam delivered to LDMX
given the amount of time we collected data \\(t\\).
\\[
  N_\text{bunch} = d \times r \times t
\\]

For an analysis that only inspects single-electron events, we can use the Poisson fraction of these
bunches that corresponds to one-electron to estimate the number of EoT the analysis is inspecting.
\\[
  N_\text{EoT} \approx e^{-\mu} N_\text{bunch}
\\]
If we are able to include all bunches (regardless on the number of electrons), then we can replace
the Poisson fraction with the Poisson average.
\\[
  N_\text{EoT} \approx \mu N_\text{bunch}
\\]
A more precise estimate is certainly possible, but has not been investigated or written down
to my knowledge.

## Simulation
For the simulation, we configure the sample generation with a certain number of electrons
per event (usually one) and we decide how many events to run for.
Complexity is introduced when we do more complicated generation procedures in order to
access rarer processes.

~~~admonish warning title="Single Electron Events"
All of the discussion below is for single-electron events.
Multiple-electron events are more complicated and have not been studied in as much detail.
~~~

In general, a good first estimate for the number of EoT a simulation sample represents is
\\[
N_\text{EoT}^\text{equiv} = \frac{N_\text{sampled}}{\sum w} N_\text{attempt}
\\]
where
- \\(N_\text{sampled}\\) is the number of events in the file(s) that constitute the sample
- \\(\sum w\\) is the sum of the event weights of those same events
- \\(N_\text{attempt}\\) is the number of events that were attempted when simulating

~~~admonish note title="Finding Number of Attempted Events"
Currently, the number of attempted events is stored as the `num_tries_` member of
the `RunHeader`

Samples created with ldmx-sw verions newer than v3.3.4 (>= v3.3.5) have an update
to the processing framework to store this information more directly
(in the `numTries_` member of the RunHeader or <= v4.4.7 and the `num_tries_` member
for newer).
Samples created with ldmx-sw versions older than v3.1.12 (<= v3.1.11) have access
to the "Events Began" field of the `intParameters_` member of the RunHeader.

The easiest way to know for certain the number of tries is to just set the maximum
number of events to your desired number of tries \\(N_\mathrm{attempt}\\) and limit the
number of tries per output event to one (`p.maxTriesPerEvent = 1` and `p.maxEvents = Nthrown`
in the config script).
~~~

### Inclusive
The number of EoT of an inclusive sample (a sample that has neither biasing or filtering)
is just the number of events in the file(s) that constitute the sample.

The general equation above still works for this case.
Since there is no biasing, the weights for all of the events are one \\(w=1\\) so the sum
of the weights is equal to the number of events sampled \\(N_\text{sampled}\\).
Since there is no filtering, the number of events attempted \\(N_\text{attempt}\\) is also equal
to the number of events sampled.
\\[
  N_\text{EoT}^\text{inclusive} = N_\text{sampled}
\\]

### Filtered
Often, we filter out "uninteresting" events, but that should not change the EoT the sample
represents since the "uninteresting" events still represent data volume that was processed.
This is the motivation behind using number of events attempted \\(N_\text{attempt}\\) instead
of just using the number in the file(s).
Without any biasing, the weights for all of the events are one so the sum of the weights
is again equal to the number of events sampled and the general equation simplifies to
just the total number of attempts.
\\[
  N_\text{EoT}^\text{filtered} = N_\text{attempt}
\\]


### Biased
Generally, we find the equivalent electrons on target (\\(N_\text{EoT}^\text{equiv}\\))
by multiplying the attempted number of electrons on target (\\(N_\mathrm{attempt}\\))
by the biasing factor (\\(B\\)) increasing the rate of the process focused on for the sample.

In the thin-target regime, this is satisfactory since the process we care about either
happens (with the biasing factor applied) or does not (and is filtered out).
In thicker target scenarios (like the Ecal), we need to account for events where
unbiased processes happen to a particle _before_ the biased process.
Geant4 accounts for this while stepping tracks through volumes with
biasing operators attached and we include the weights of all steps in the overall event
weight in our simulation.
We can then calculate an effective biasing factor by dividing the total number of events
in the output sample (\\(N_\mathrm{sampled}\\)) by the sum of their event weights (\\(\sum w\\)).
In the thin-target regime (where nothing happens to a biased particle besides the
biased process), this equation reduces to the simpler \\(B N_\mathrm{thrown}\\) used in other
analyses since biased tracks in Geant4 begin with a weight of \\(1/B\\).
\\[
N_\text{EoT}^\text{equiv} = \frac{N_\mathrm{sampled}}{\sum w}N_\mathrm{thrown}
\\]

## Event Yield Estimation
Each of the simulated events has a weight that accounts for the biasing that was applied.
This weight quantitatively estimates how many _unbiased_ events this single
_biased_ event represents.
Thus, if we want to estimate the total number of events produced for a desired EoT
(the "event yield"), we would sum the weights and then scale this weight sum by the ratio
between our desired EoT \\(N_\text{EoT}\\) and our actual simulated EoT \\(N_\text{thrown}\\).
\\[
N_\text{yield} = \frac{N_\text{EoT}}{N_\text{thrown}}\sum w
\\]
Notice that \\(N_\text{yield} = N_\text{sampled}\\) if we use
\\(N_\text{EoT} = N_\text{EoT}^\text{equiv}\\) from before.
Of particular importance, the scaling factor out front is constant across all events
for any single simulation sample, so (for example) we can apply it to the contents of a
histogram so that the bin heights represent the event yield within \\(N_\text{EoT}\\) events
rather than just the weight sum (which is equivalent to \\(N_\text{EoT} = N_\text{thrown}\\)).

## More Complexity
Include Einar's notes here...
