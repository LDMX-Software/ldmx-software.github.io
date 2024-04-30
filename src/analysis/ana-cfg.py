from LDMX.Framework import ldmxcfg
p = ldmxcfg.Process('ana')
import os
# needs to match path to where compiled library is
# deduced automatically if built and installed alongside ldmx-sw
ldmxcfg.Process.addLibrary(f'{os.getcwd()}/libMyAnalysis.so')
class MyAnalysis:
    def __init__(self):
        self.instanceName = 'my-ana'
        self.className = 'MyAnalyzer' # match class name in source file
        self.histograms = []
p.sequence = [ MyAnalysis() ]
p.inputFiles = [ 'events.root' ]
p.histogramFile = 'hist.root'
