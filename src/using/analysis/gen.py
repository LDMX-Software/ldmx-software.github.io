from LDMX.Framework import ldmxcfg
p = ldmxcfg.Process('test')
from LDMX.SimCore import simulator as sim
mySim = sim.Simulator( "mySim" )
mySim.set_detector( 'ldmx-det-v15-8gev', True )
from LDMX.SimCore import generators as gen
mySim.generators = [ gen.single_8gev_e_upstream_tagger() ]
mySim.description = 'Basic test Simulation'
p.sequence = [ mySim ]
p.run = 1
p.max_events = 10000
p.output_files = [ 'events.root' ]

import LDMX.Ecal.ecal_geometry
import LDMX.Ecal.ecal_hardcoded_conditions
import LDMX.Hcal.hcal_geometry
import LDMX.Ecal.digi as ecal_digi

p.sequence = [
    mySim,
    ecal_digi.EcalDigiProducer(),
    ecal_digi.EcalRecProducer()
]
