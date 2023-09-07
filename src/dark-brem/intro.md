# Dark Brem Signal Samples

The Dark Brem (short for Dark Bremsstrahlung, acronym DB) process is one of the most complicated processes we need to simulate for LDMX. This is due in large part to two factors (1) it is not implemented in Geant4 already and (2) it interacts with a nucleus, making the analytic cross section difficult to compute and program into a simulation. For these two reasons (and a few others), DB is supported by doing two stages.

1. Generate DB Events with MadGraph -- MadGraph handles the complicated process of generating outgoing kinematics for the particles involved in the interaction. Using MadGraph at this stage also leaves the door open for trying different models of DB in MadGraph and seeing how LDMX is sensitive to them.
2. Simulate DB Events in the LDMX Detector with Geant4 -- Geant4 handles the process of particles interacting with materials. We use the previously generated DB events in order to inform Geant4 how it should simulated DB when it occurs within a material in LDMX.

Following conventions done by collider experiments, I usually call stage one "generation" (or "gen" for short) and stage two "simulation" (or "sim" for short). Just remember that they are two different program executions.

To make this even more complicated, LDMX has two different methods to perform the DB simulation. This has led to some confusion within the collaboration and so this document explains both (even though only one is suggested for future use).

### Historical Method
The "historical" method is the one that was first done and is a valid approximation for the O(90%) of electrons that arrive at the target undisturbed by the upstream detector components (tagger tracker and trigger scintillator). Generation is done by using MadGraph at a _single_ beam energy such that a _single_ LHE file is output. This LHE file is then given to the [LHEPrimaryGenerator](Configuring-the-Simulation.md) to setup the electron and A' as primaries. The vertex of the primaries imported from the LHE files would be smeared around the target, but the electron's energy would stay fixed at the energy simulated for the LHE files.

As mentioned, this is a good approximation for a vast majority of electrons when looking a DB _in the target_. It is not a helpful method if we wish to include the complexities of the tagger tracker and trigger scintilator or if we wish to look for DB in other parts of the LDMX detector (like in the ECal).

### G4DarkBreM
Geant4 Dark Bremsstrahlung from Madgraph (G4DarkBreM) is a package that grew out of this desire to expand the regions where LDMX could search for DB. Between ldmx-sw v2.3.0 and v3.2.1 it was a part of ldmx-sw's SimCore module directly and was used to produce signal samples for the LDMX ECal-as-Target analysis. As it matured (being used in parallel in CMS for a similar DB search with muons), it was pulled out of ldmx-sw into its own package where it was improved, tested, validated, and published. Below, I've included links related to G4DarkBreM where you can learn more information.

How is G4DarkBreM different from the above method? In essence, as the paper shows, it is able to produce DB events within a _continuous_ range of lepton energies using a reference library consisting of a set of _discrete_ energy points. The discrete-ness of the energy points is helpful for interacting with MadGraph - this way the reference library can be generated at a finite set of incident energies which is simple for MadGraph to do, loaded into the Geant4 DB process, and then used as data during the simulation when MadGraph is unavailable.

### References
- [ArXiV of Paper about G4DarkBreM](https://arxiv.org/abs/2211.03873)
- [G4DarkBreM Package Documentation](https://tomeichlersmith.github.io/G4DarkBreM/)
- [G4DarkBreM on GitHub](https://github.com/tomeichlersmith/G4DarkBreM)

