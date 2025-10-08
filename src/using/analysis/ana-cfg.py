from LDMX.Framework import ldmxcfg
p = ldmxcfg.Process('ana')
p.sequence = [ ldmxcfg.Analyzer.from_file('MyAnalyzer.cxx', needs=['Ecal_Event']) ]
p.inputFiles = [ 'events.root' ]
p.histogramFile = 'hist.root'
