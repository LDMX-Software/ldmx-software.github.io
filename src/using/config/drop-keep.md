# Drop Keep Rules

By default, all data that is added to an event (via `event.add` within a `produce` function)
is written to the output data file. This is a helpful default because it allows users to
quickly write a new config and see everything that was produced by it.

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
- `expression` is a regular expression that will be compared against the branch names

### decision
As the name implies, this first string is the definition of what should happen to
an event object that this rule applies to. It must exactly match one of the strings below
**and must appear at the start of the rule string**.

- `drop` : event objects matching `expression` are readable during processing but not written to the output file
- `keep` : event objects matching `expression` are written to the output file (the default for all objects)
- `ignore` : event objects matching `expression` are not read from the input file at all and are invisible to processors

```admonish note title='Difference between drop and ignore'
`drop` lets processors still read the collection during processing — it just will not appear in the
output file. `ignore` goes further: the branch is not registered in the event product list at all,
so processors cannot access it even if they try. Use `ignore` when you want to completely hide
collections from a previous pass (e.g. intermediate "test" pass data) while reprocessing with a
new pass.
```

```admonish warning title='EventHeader is protected'
A `drop` or `ignore` rule that would match `EventHeader` will raise an error at startup.
The EventHeader is required by the framework and cannot be removed.
```

### expression
This regular expression has been tested against basic sub-string matching and it is advised
to stay within the realm of sub-string matching.

Since we append the pass name of a process to the end of event objects created within that
process, we expect this expression to be focused on matching the prefix of the full branch name.
Thus, if an expression does not end in a `*` character, one is appended automatically.

~~~admonish example
The expression `"EcalSimHits"` in the python configuration will be updated to
`"EcalSimHits*"`.
~~~

### Ordering
The rules are applied in order and can override one another. This allows for more complicated
decisions to be made. In essence, the _last_ rule in the list whose expression matches the
event object's name is the decision that will be applied.

~~~admonish example
Drop all scoring plane hit collections except the one for the ECal.
```python
p.keep = [
    'drop .*ScoringPlane.*',
    'keep EcalScoringPlane.*'
]
```
~~~

~~~admonish example title='Ignoring a previous pass'
When reprocessing data, you can hide all collections from a previous pass so that processors
cannot accidentally read old data. New collections with the current pass name will still be
created normally.
```python
p.keep = [
    'ignore test',  # hide all branches with pass name "test"
]
```
~~~

~~~admonish warning title="Dangerous Example"
In a very tight disk space environment, you can drop all event objects and then only keep
ones you specifically require. In general, this is _not_ recommended.
```python
p.keep = [
    'drop .*',
    'keep HcalHits.*',
    'keep EcalHits.*',
]
```
The above would produce a file with only the Hcal and Ecal hits. A warning will be printed
at startup when an all-matching drop or ignore rule is detected.
Make sure to thoroughly test your config with `p.keep` set to confirm that
everything you need is in the output file. It is very easy to mis-type one of these patterns
and prevent anything from being written to the output file.
~~~
