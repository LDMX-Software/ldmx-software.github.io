from LDMX.Framework import ldmxcfg
p = ldmxcfg.Process('ana')
p.sequence = [ ldmxcfg.processor_from_file('MyAnalyzer.cxx', needs=['SimCore_Event', 'Ecal_Event']) ]
p.input_files = [ 'events.root' ]
p.histogram_file = 'hist.root'
p.pause()
