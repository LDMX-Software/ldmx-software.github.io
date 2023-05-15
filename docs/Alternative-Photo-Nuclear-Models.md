---
layout: default
---

This page details the options in LDMX-sw that allow you to change the default model used in Geant4 for modelling photo nuclear interactions. 

Example use cases:

- Replacing PN products with known complicated PN topologies for comparing different detector geometries
- Replacing the Bertini with other hadronic models 
- Instrumenting a model to extend it in some way, e.g. to run the event generator until you produce an event topology that you are interested in, but could in principle be used to do anything you need (e.g. debugging)


A photonuclear model in ldmx-sw is a class that provides Geant4 with an appropriate hadronic interaction to use for $\gamma A$ interactions. With the standard LDMX version of Geant4, the hadronic model is a modified version of [The Bertini Cascade](https://doi.org/10.1016/j.nima.2015.09.058) (for details, see sec D and appendix A of [arxiv:1808.04219v1](https://arxiv.org/abs/1808.05219v1)). 


To load a different model than the default, you change the `photonuclear_model` parameter of your simulation processor. A couple such models are bundled with ldmx-sw and adding new ones either within or from outside ldmx-sw is a relatively straigh-forward task. 

## Models generating rare but challenging final states


With all of these models, when a photonuclear interaction occurs the model will rerun the interaction until a particular condition is met for the final state particles. If it took $N$ attempts to produce that final state, the weight of the event will be multiplied with $\frac{1}{N}$. You can access the event weight with the event header. This can produce much faster simulations (>10x faster) than a full simulation + skim would do. However, you may need to be careful so that you don't introduce any significant bias to your results. Consider producing a smaller sample first with a regular simulation and comparing it to a sample of the same size made with one of these models. See the Validation module for a good starting point for such comparisons. 


### Events with one hard neutron 

  This model will rerun the event generator until we get an event where one neutron is the only particle with kinetic energy above some threshold. By default, this model is applied for interactions with any nucleus and for photons with at least 2.5 GeV of energy. With these settings and a configuration like the standard ECal PN simulation, you could in principle skip the filter but unless you have e.g. a performance reason to do so consider keeping it.
    
```python
# Assuming your simulator is called mySim 
from LDMX.Simcore import photonuclear_models as pn 
from LDMX.Biasing import particle_filter 


myModel = pn.BertiniSingleNeutronModel()
# These are the default values of the parameters
myModel.hard_particle_threshold=200. # Count particles with >= 200 MeV as "hard"
myModel.zmin = 0 # Apply the model for any nucleus
myModel.emin = 2500. # Apply the model for photonuclear reactions with > 2500 MeV photons
myModel.count_light_ions=True # Don't disregard deutrons, tritons, 3He, or 4He ions when counting hard particles 

# Change the default model to the single neutron model
mySim.photonuclear_model = myModel


myFilter = particle_filter.PhotoNuclearTopologyFilter().SingleNeutron()
# Default values 
myFilter.hard_particle_threshold = 200. # MeV, use the same as for the model 
myFilter.count_light_ions = True # As above

# Add the filter at the end of the current list of user actions. 
mySim.actions.extend([myFilter])
```
### Events with no particles with high kinetic energy 

  This model is very similar to the previous one with one big exception, it is only applied for interactions with tungsten (the `zmin` parameter is set to 74). Since the ECal consists of more material than just tungsten, this means that some ECal PN-events will not produce the desired final state. If you don't combine the model with a particle filter, you will have $\approx 50\%$ of your events being regular photonuclear reactions. The reason for this cut on the proton number of the target nucleus is that nothing hard events, which generally include very high product multiplicity, are extremely rare for nuclei with few nucleons. These interactions would therefore receive an extremely small event weight or even get stuck repeating the event generation infinitely for e.g. hydrogen. 
  
 ```python
from LDMX.Simcore import photonuclear_models as pn 
from LDMX.Biasing import particle_filter 


myModel = pn.BertiniNothingHardModel()
# These are the default values of the parameters
myModel.hard_particle_threshold=200. # Count particles with >= 200 MeV as "hard"
myModel.zmin = 74 # Apply the model tungsten only
myModel.emin = 2500. # Apply the model for photonuclear reactions with > 2500 MeV photons
myModel.count_light_ions=True # Don't disregard deutrons, tritons, 3He, or 4He ions when counting hard particles 

# Change the default model to the single neutron model
mySim.photonuclear_model = myModel

myFilter = particle_filter.PhotoNuclearTopologyFilter().NothingHard()
# Default values 
myFilter.hard_particle_threshold = 200. # MeV, use the same as for the model 
myFilter.count_light_ions = True # As above

# Add the filter at the end of the current list of user actions. 
mySim.actions.extend([myFilter])
 ``` 

### Events with hard kaons (or similar particle selections)

The last of the default models in ldmx-sw works similar to the other two but
rather than requiring an exact number of hard particles, it requires at least N
hard particles of any of a set of particles that you are interested in. The
setup comes with a preconfigured version that requries at least one hard kaon in
the final state. 

```python
from LDMX.Simcore import photonuclear_models as pn 
from LDMX.Biasing import particle_filter 


myModel = pn.BertiniAtLeastNProductsModel().kaon() 
# These are the default values of the parameters
myModel.hard_particle_threshold=200. # Count particles with >= 200 MeV as "hard"
myModel.zmin = 0 # Apply the model to any nucleus
myModel.emin = 2500. # Apply the model for photonuclear reactions with > 2500 MeV photons
myModel.pdg_ids = [130, 310, 311, 321, -321] # PDG ids for K^0_L, K^0_S, K^0, K^+, and K^- respectively
myModel.min_products = 1 # Require at least 1 hard particle from the list above


# Change the default model to the single neutron model
mySim.photonuclear_model = myModel

myFilter = particle_filter.PhotoNuclearProductsFilter().kaon()

# Add the filter at the end of the current list of user actions. 
mySim.actions.extend([myFilter])
```
   
Details
---

## Adding a new model 

To add a new model within a library, you need to add a class that inherits from `SimCore/PhotoNuclearModel` and registering it with the `DECLARE_PHOTONUCLEAR_MODEL` macro at the end of your source file. This base class has one pure virtual function that you have to implement called `ConstructGammaProcess(G4ProcessManager*)` with some other virtual functions you can override if you need some other behaviour than the defaults. If you are adding a photonuclear model from outside of SimCore, you need to register `SimCore::PhotoNuclearModels` as a dependency when setting up your library. 


```CMake
setup_library(module ModuleName 
    dependencies 
    # Any other dependencies your module has 
    SimCore::PhotoNuclearModels
    sources 
    # Your source files
)
```

Finally, you'll need to add a new mocel to your python configuration and register it as the as the photonuclear model of your simulation processor. 

```python
from LDMX.SimCore import simcfg 

class MyModel(simcfg.PhotoNuclearModel): 
    """
       Documentation 
    """
    def __init__(self):
    super().__init__('MyModel', 'ClassName', 'ModuleName')
    
    
    
mySim.photonuclear_model = MyModel()
```

Where `'ClassName'` matches the namespace and type name that you registered with `DECLARE_PHOTONUCLEAR_MODEL` and `'ModuleName'` is the name of your module (same as you used in the CMake configuration).

### ConstructGammaProcess 

This is the only member function of `simcore::PhotoNuclearModel` you have to implement yourself. 
It takes a `G4ProcessManager`. This function is responsible for creating a `G4HadronInelasticProcess` with the name `"photonNuclear"` (the name matters since other parts of ldmx-sw relies on this being the name of the PN process). The process needs to have one `G4HadronicInteraction` registered with valid energy range and a cross section dataset. For the latter, there is a default implementation you can use in the `PhotoNuclearModel` class called `addPNCrossSectionData(G4HadronInelasticProcess*) const`;

A typical implementation would look like the following 

```C++

namespace mynamespace {
void MyModel::ConstructGammaProcess(G4ProcessManager* processManager) {
    auto photoNuclearProcess{new G4HadronInelasticProcess("photonNuclear", G4Gamma::Definition())};
    auto myInteraction {new MyHadronicInteraction{ // any parameters
    }}; 
    myInteraction->SetMaxEnergy(15*CLHEP::GeV);
    addPNCrossSectionData(photoNuclearProcess); // If you forget this line, the simulation won't run. 
    photoNuclearProcess->RegisterMe(myInteraction); 
    processManager->AddDiscreteProcess(photoNuclearProcess);
} // namespace mynamespace
}
DECLARE_PHOTONUCLEAR_MODEL(mynamespace::MyModel);
```

You can see how the model is used in `GammaPhysics.cxx` in `SimCore` but in short the order of operations is the following

- Create a `PhotoNuclearModel` depending on the configuration 
- Call `removeExistingModel` to remove the default model
- Call `ConstructGammaProcess` to build the `photonNuclear` process
- Set the `photonNuclear` process to be first in the list of processes for
  photons. Necessary for the bias operator to work. 
- Add the $\gamma \rightarrow \mu\mu$ process

## Instrumenting the photonuclear 


## Models forcing particular final states 

One use case for customizing the process used for photonuclear reaction is to study particular rare final states like single hard neutron events without having to generate a complete simulation set or as an alternative to biasing schemes like the kaon enhancement setup. There is a abstract base class, `BertiniEventTopologyProcess`, available that makes implementing such models relatively straight-forward with the Bertini cascade. It handles all of the things underneath the hood like cleaning up the memory from unused secondaries automatically. 

The process will run the Bertini cascade over and over until some condition is met for the final state. Once an attempt has been succesful, the event weight is incremented based on the number of attempts made. In the example with `MyModel` above, you would have a `G4HadronicInteraction` that is derived from `BertiniEventTopologyProcess` as `myInteraction`. Typically you want to combine this kind of process with a corresponding filter.

## Included models in LDMX-sw 

LDMX-sw comes with a couple of these models included that both cover important final states and illustrate how to extend it with new ones. 
- `BertiniNothingHardModel` 
  - Runs the event generator until we find an event where no individual particle has more than some threshold energy. 
  - By default only applied for nuclei with `Z >= 74` since these events are much less likely to occur for lighter nuclei. 
  - By default, light ions with kinetic energy above the threshold are counted so that e.g. an event with a 1 GeV deutron isn't considered "Nothing hard". 
  - Should be paired with a product filter from `LDMX.Biasing`. 
```python 
from LDMX.SimCore import photonuclear_models as pn
model = pn.BertiniNothingHardModel()
model.hard_particle_threshold = 500. # MeV, Default is 200. 
model.zmin = 29 # Include Copper, Default is 74 (W)
model.count_light_ions = False # Default is to include 
from LDMX.Biasing import particle_filter 
mySim.actions.extend([
    particle_filter.PhotoNuclearTopologyFilter().NothingHard()
])
mySim.photonuclear_model = model
```

- `BertiniSingleNeutronModel` 
  - Similar to the nothing hard model but requires exactly one particle with kinetic energy above the threshold and that the particle in question is a neutron. 
  - Default applied for any nucleus
  - Has a similar corresponding filter in `LDMX.Biasing.PhotoNuclearTopologyFilter`
- `BertiniAtLeastNProductsModel` 
  - Takes a list of PDG particle-ids, an energy threshold, and a particle count and requires that at there are at least N particles with ids matching that in the list with kinetic energy above the threshold 
  - A version suitable for producing events with at least one kaon in the final state can be obtained from `BertiniAtLeastNProductsModel.kaon()`
  - Should be used together with a corresponding filter such as `LDMX.Biasing.PhotoNuclearProductsFilter`
  



### Adding your own model for other final states than those that are included with LDMX-sw


An implementation needs to override three functions, `acceptProjectile`, `acceptTarget`, and `acceptEvent`. The first two allow you to define what types of photons and target  nuclei you are interested in. If either `acceptProjectile` or `acceptTarget` return `false`, the event generator will only be called once. The choice of what target nuclei to apply the model to requires some care. Since different final states are more or less likely depending on what nucleus the photon interacts with, you can end up producing events with very low event weight or even get stuck trying to repeat the event generation for a final state that is impossible (e.g. producing a single hard neutron from a photonuclear reaction with hydrogen). On the other hand, if you limit your reactions to only occur for tungsten you might be biasing the kinds of final states that are possible to study. To build an understanding for these kinds of issues, you can add a model that does the corresponding bookkeeping for you. For example, if you keep a count of what the target nucleus is for an ECal PN sample, you would find that ~50% of all PN interactions are with other nuclei than tungsten in the v14 detector.


Once you are sure that you are accepting the right kinds of projectiles and targets, the only thing left to add is the `acceptEvent` function. This function has access to the secondaries that was produced by the event generator through the `theParticleChange` member variable. See an example below.

```C++
bool MyProcess::acceptEvent() const {
    int secondaries{theParticleChange.GetNumberOfSecondaries()}; 
    for (int i{0}; i < secondaries; ++i) {
        // Grab the ith secondary G4Track*  
        auto secondary {theParticleChange.GetSecondary(i)->GetParticle()};
        auto kinetic_energy {secondary->GetKineticEnergy()};
        auto pdg_code {secondary->GetDefinition()->GetPDGEncoding()};
        if (my_condition(pdg_code, kinetic_energy)) {
            return true;
        }
    }
    return false;
}
```

Finally, you want to add a filter that rejects events that don't have the topology you are interested in. This is next to trivial to add if you make use of the `PhotoNuclearTopologyFilter` base class. Similar to how you implemented an `acceptEvent` function for the model, this filter has an `rejectEvent` function to be added. The filter needs to be registered with LDMX-sw similar to any other user action with the `DECLARE_ACTION` macro as well as with a python object added to the `actions` of your simulation processor. If you don't need to do anything custom, you can use the `PhotoNuclearTopologyFilter` as a starting point.

An example implementation would have the following form

```C++
namespace MyNamespace {
class MyFilter : public PhotoNuclearTopologyFilter {
    public: 
    bool rejectEvent(const std::vector<G4Track*>& secondaries) const override {
       for (auto secondary : secondaries) {
           // Check your condition
       } 
    }
};
} // namespace MyNamespace

DECLARE_ACTION(MyNamespace, MyFilter)
```

```python
mySim.photonuclear_model = myModel 
from LDMX.Biasing import particle_filter 

myFilter = particle_filter.PhotoNuclearTopologyFilter(
                name='MyFilter', 
                filter_class='MyNamespace::MyFilter')

mySim.actions.extend([myFilter])

```


