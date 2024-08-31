# Event Skimming

Another feature of our event processing framework is selecting out only certain events to be written
into the output file. This is colloquially called "skimming" and is helpful for many reasons, primarily
for users to be able to not waste disk space on events that are not interesting for an analysis.

Since not writing events into the output file is an inherently destructive feature, event skimming
will only operate if _both_ the config and the processors being run by the config support it.
Both play a part in how the choice to keep an event is made and so they are described below.

~~~admonish note title="More Info"
The
[StorageControl](https://ldmx-software.github.io/ldmx-sw/classframework_1_1StorageControl.html)
class in the processing framework is what handles the event skimming
decisions and the input from the config and processors.
~~~

## Processor 
On the C++ side of things, processors can use their protected member function `setStorageHint`
to "hint" to the framework what that processor wants to happen to the event. The argument
to this function is a `framework::StorageControl::Hint` value as well as a string that can
be used to give a more detailed "purpose".

Hints are then used to algorithmically decide if an event should be written to the output file
(kept) or not (dropped). Only hints passing the "listening rules" (see below) are included in
this algorithm.

- `Must*`: "must"-style hints are dominant. If any processor provides a "must" hint, 
  then that decision is made. `MustDrop` takes precendence over `MustKeep` if both are provided.
- `Should*`: "should"-style hints are less forceful and are just used to tally votes.
  A simple majority of should hints is used to make the decision if no must hints are provided.
- If there is a tie (including if no hints are provided), then the default decision is made.

## Config
The config script can alter which processors the framework will "listen" to when deciding
what to do with an event by checking for specific processor names and (optionally) only
specific "purpose" strings from that processor. In addition, the config script defines
what the default decision is in the case of no hints or a tie in voting.

### Listening Rules
The format of the string representing a listening rule is a bit complicated, so it is best
to just use the `p.skimConsider` function when defining which processors you wish to "listen"
to (or "consider") when making a skimming decision. Most commonly, a user just has one processor
that they want to make the skimming decision and in this case you can just provide the processors
name.
```python
p.skimConsider(my_processor.instanceName)
```
Technically, the listening rules use regular expressions for both the processor name and the
purpose, so one could get quite fancy about which processors (and purposes) are selected.
This more intricate skimming method has not been well tested.

### Default Decision
The default storage decision is what will be used if no processors that are being listened
to provide a hint during processing. Since the default configuration is to listen to no
processors at all, the default configuration of the default decision is to keep i.e. without
any config changes, we keep all events that are processed. Without changing this,
you could have a processor that explicity "drops" events and update the config to consider
this processor in order to run over events and drop the "uninteresting" ones
(using `p.skimConsider` like above).

On the other hand, we could set the default decision to drop all the events and instead
have a processor specifically "keep" events that are interesting. In this case, you would
want to add the following to your config.
```python
p.skimDefaultIsDrop()
```
**along with a `p.skimConsider`** so that something ends up in your output event file.

~~~admonish warning title="Another Form of Event Dropping"
This style of event dropping is geared more towards readout, reconstruction, and analysis
decisions where the event is already fully created in memory and we just want to make
a decision about it.

In the simulation, we also allow for events to be "aborted" in the middle of creating
it so that we can end the event early and save computing resources from being wasted
on an event we've decided is not interesting (for whatever reason). This style of "dropping"
events is more commonly called "filtering" the simulation and is more complicated than
what is described here since it operates _during_ the Geant4 simulation.
~~~
