# Tips and Tricks

~~~admonish info collapsible=true title="Command Line Arguments"
Python has an easy-to-use [argument parsing library](https://docs.python.org/3/library/argparse.html). This library can be used within an ldmx-sw configuration script in order to change the parameters you are passing to the processors or even to change which processors you use.

For example, I use the code snippet often to pass inputs to the process.

```python
import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('run_number',type=int,help='run number for this simulation run')
parser.add_argument('-o','--out-dir',type=Path,help='output directory to write event data to')
args = parser.parse_args()

from LDMX.Framework import ldmxcfg
p = ldmxcfg.Process('example')
p.run = args.run_number
p.outputFile = [
  str(args.out_dir / f'my_special_simulation_run_{p.run:04d}.root')
]

# rest of configuration
```

Looking at the argparse library linked above is highly recommended since it has a lot
of flexibility and can make passing arguments into your config very easy.
~~~

~~~admonish info collapsible=true title="Manipulating File Paths"
Python's [pathlib](https://docs.python.org/3/library/pathlib.html) library is helpful for doing the common tasks of finding files, listing files, and making a new file path.

For example, if `input_dir` is a `pathlib.Path` for an input directory of ROOT files.
```python
p.inputFiles = [ str(f) for f in input_dir.iterdir() if f.suffix == '.root' ]
```

We can also use an input file `input_file` to get an output file name and an output directory `output_dir`
to place this file in the directory we want.
```python
p.outputFiles = [ str(output_dir / (input_file.stem + '_with_my_analyzer.root')) ]
```
~~~
