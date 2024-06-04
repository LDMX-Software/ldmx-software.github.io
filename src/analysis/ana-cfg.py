from LDMX.Framework import ldmxcfg
p = ldmxcfg.Process('ana')
p.sequence = [ ldmxcfg.Analyzer.from_file('MyAnalysis.cxx') ]
p.inputFiles = [ 'events.root' ]
p.histogramFile = 'hist.root'
