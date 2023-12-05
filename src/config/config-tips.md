# Tips and Tricks

There are two simple and very helpful features of using a python script as our configuration file.
Firstly, python has a very easy-to-use [argument parsing library](https://docs.python.org/3/library/argparse.html). This library can be used within an ldmx-sw configuration script in order to change the parameters you are passing to the processors or even to change which processors you use.

Secondly, python has good libraries for working with your operating system: `os` and `sys`. These libraries can mainly be used to work with getting paths to files which is helpful for running over all the files in a given directory:
```python
p.inputFiles = [
    os.path.join(myDirectory, f) 
    for f in os.listdir(myDirectory) if os.path.isfile(os.path.join(myDirectory, f))
]
```
or formatting the output file name to correspond to the input with some prefix or suffix:
```python
p.outputFiles = [ 'myPrefix_' + p.inputFiles[0].replace( '.root' , '' ) + '_mySuffix' + '.root' ]
