from LDMX.Framework import ldmxcfg
p = ldmxcfg.Process('test')
from LDMX.SimCore import simulator as sim
mySim = sim.simulator( "mySim" )
mySim.setDetector( 'ldmx-det-v14-8gev', True )
from LDMX.SimCore import generators as gen
mySim.generators = [ gen.single_8gev_e_upstream_tagger() ]
mySim.beamSpotSmear = [20.,80.,0.]
mySim.description = 'Basic test Simulation'
p.sequence = [ mySim ]
p.run = 1
p.maxEvents = 10000
p.outputFiles = [ 'events.root' ]

import LDMX.Ecal.EcalGeometry
import LDMX.Ecal.ecal_hardcoded_conditions
import LDMX.Hcal.HcalGeometry
import LDMX.Ecal.digi as ecal_digi

p.sequence = [
    mySim,
    ecal_digi.EcalDigiProducer(),
    ecal_digi.EcalRecProducer()
]
