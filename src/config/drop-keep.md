# Drop Keep Rules

```admonish warning title="Bugs with Drop Keep Rules" collapsible=true
Some issues with the drop keep rules have been reported on GitHub:
[Framework Issue #91](https://github.com/LDMX-Software/Framework/issues/91).
Check there if you are having issues to see if you need to update or if there
is a work-around.
```

By default, all data that is added to an event (via `event.add` within a `produce` function)
is written to the output data file. This is a helpful default because it allows users to
quickly and write a new config and see everything that was produced by it.

Nevertheless, it is often helpful to avoid storing specific event objects within the output file
mostly because the output file is getting too large and removing certain objects can save disk
space without sacrificing too much usability for physics analyses. For this purpose, our processing
framework has a method for configuring which objects should be stored in the output file. This
configuration is colloquially called "drop keep rules" since some objects can be "dropped" during
processing (generated in memory but not written to the output file) while others can be explicitly
kept (i.e. written to the output file).

The drop keep rules are written in the config as a python list of strings
```python
# p is the ldmxcfg.Process object created earlier
p.keep = [ '<rule0>', '<rule1>', ... ]
```
the implementation of these rules is done in the
[framework::EventFile class](https://ldmx-software.github.io/ldmx-sw/classframework_1_1EventFile.html)
specifically the `addDrop` function handles the deduction of these rules.

## Rule Format
Each rule in the list should be a string with a single space.
```
decision expression
```
- `decision` is one of three strings: `drop`, `keep`, and `ignore`.
- `expression` is a regular expression that will be compared against the event object names

### decision
As the name implies, this first string is the definition of what should happen to
an event object that this rule applies to. It must exactly match one of the strings below.

- `drop` : event objects matching `expression` should not be written to the output file
- `keep` : event objects matching `expression` should be written to the output file
- `ignore` : event objects matching `expression` should not even be read in from the input file

```admonish note title='Legacy Note'
The "ignore" decision is leftover from earlier versions of the processing framework that
would load all event objects from the input file into memory for processing. Current versions
of framework do not do this and so this decision is largely not needed.

Perhaps a future version of framework will fully remove this as an option after testing
confirms that this behavior is not needed.
```

### expression
This regular expression hasn't been fully tested against all the powers of regular expressions.
What has been tested is basic sub-string matching and so it is advised to stay within the realm of
sub-string matching.

Since we append the pass name of a process to the end of these event objects created within that
process, we expect this expression to be focused on matching the prefix of the full object name.
Thus, if an expression _emph_ does not end in a `*` character, one is appended.

~~~admonish example
The expression `"EcalSimHits"` in the python configuration will be updated to
`"EcalSimHits*"`.
~~~

### Ordering
The rules are applied in order and can override one another. This allows for more complicated
decisions to be made. In essence, the _last_ rule in the list whose expression matches the
event object's name, that is the decision that will be applied.

~~~admonish example
I can drop all of the scoring plane hit collections except the one for the ECal.
```python
p.keep = [
    'drop .*ScoringPlane.*',
    'keep EcalScoringPlane.*'
]
```
~~~

~~~admonish warning title="Dangerous Example"
In a very tight disk space environment, you can drop all event objects and then only keep
ones you specifically require. In general, this is _not_ recommended (and to be honest,
I'm not sure if it works).
```python
p.keep = [
    'drop .*',
    'keep HcalHits.*',
    'keep EcalHits.*',
]
```
The above would then have a file with only the Hcal and Ecal hits.
Make sure to thoroughly test run your config with the setting of `p.keep` to make sure that
everything you need is in the output file. It is very easy to mis-type one of these patterns
and prevent anything from being written to the output file.
~~~
