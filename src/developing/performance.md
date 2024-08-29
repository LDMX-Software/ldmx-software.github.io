# Tracking the Performance of ldmx-sw

With v1.4.0 of Framework, rudimentary performance tracking is available to all users of Framework.
This first release only tracks the time of various components leaving more complicated measurements
(e.g. memory consumption) for later.

Performance is tracked in an opt-in basis and is stored within the output histogram file underneath
a directory named "performance". In order to track performance, you must update your config file
with the following data.

```python
# p is the ldmxcfg.Process object already constructed
p.histogramFile = 'performance.root' # only necessary if not already being used
p.logPerformance = True
```

The performance measurements are measuring how long a specific callback took as well as some
additional timing measurements.
- `absolute`: timing how long the entire process took to run (ignoring the configuration time)
- `onProcessStart`: how long `onProcessStart` took
- `onProcessEnd`: how long `onProcessEnd` took
- `onFileOpen`: how long the _last_ `onFileOpen` took
- `onFileClose`: how long the _last_ `onFileClose` took
- `beforeNewRun`: how long the _last_ `beforeNewRun` took
- `onNewRun`: how long the _last_ `onNewRun` took
- `by_event`: timing of each processing call took for each event

```admonish warning
Some callbacks (the `File` and `Run` ones) can be called multiple times during
reconstruction mode. The performance tracking software only stores the last
measurement since it is focused on measuring production runs.

Future developments to measure every call to these functions would not be difficult,
but would require some complication of the data schema.
```

Each of these measurements are further separated into the different processors in the sequence
by the name given to the processor in the configuration. A special name "\_\_ALL\_\_" is used
for a measurement that times how long all of the processors in the sequence took for that callback.
The performance measurements are stored in the output histogram file under the following schema.
All timing measurements use the framework::performance::Timer class.

```
- performance/      # TDirectory holding all performance data
  - absolute        # Timer for all 
  - onProcessStart/ # TDirectory holding onProcessStart data
    - <processor>   # Timer for processor named <processor>
    - ...
    - __ALL__       # Timer wrapping all processor's onProcessStart calls
  - ... other non-by-event call-backs follow same structure
  - by_event/
    - <processor>   # branch holding instances of Timer for processor named <processor>
    - ...
    - __ALL__       # wrapping all processor's producer or analyze calls
    - completed     # boolean signalling if event was completed (true) or aborted (false)
```

Accessing this schema is not too difficult, but as an example, I've included some python
snippets below using `uproot` that just prints the performance data from the input
file to the terminal.

```python
"""load a file and print the performance data"""

import uproot
import sys
import json

class ReprEncoder(json.JSONEncoder):
    """if JSON can't serialize it, just use its repr string"""
    def default(self, obj):
        try:
            return super().default(obj)
        except TypeError:
            return repr(obj)


with uproot.open(sys.argv[1]) as f:
    print('absolute')
    t = f['performance/absolute'].members
    print(t['duration_'], t['start_time_'])
    for callback in [
        'onProcessStart', 'onProcessEnd',
        'onFileOpen','onFileClose',
        'beforeNewRun', 'onNewRun'
    ]:
        print(callback)
        for name, timer in f[f'performance/{callback}'].items():
            print('  ', f'{name:10s}', f'{timer.members["duration_"]:.3e}', timer.members['start_time_'])

    t = f['performance/by_event']
    # use recursive=False so that the branches remain structured into their Timers
    # you can also remove the expressions argument which will just return an unstructured set of data
    events = t.arrays(expressions=t.keys(recursive=False), library='np')
    print(json.dumps(events, cls=ReprEncoder, indent=2))
```
