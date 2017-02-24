# Encoding Dynamic Flux Balance Analysis (DFBA) models in SBML
This document describes the rules and guidelines for encoding DFBA models in SBML.
Required rules are stated via **MUST**, guidelines which should be followed are indicated
by **SHOULD**.

The provided example models in the `models` folder follow the rules & guidelines below.

## Models
The DFBA model in SBML consists of multiple SBML submodels.
* All SBML models for DFBA **MUST** be encoded in SBML L3V1 or higher.
* All SBML models **MUST** be valid SBML.
* The DFBA model **MUST** be encoded using the `comp` and `fbc` packages.
* All SBML models **SHOULD** only use released SBML packages.
* The **MUST** at least consist of three submodels:
    * the `TOP` model, which is the SBML top model including the other models, 
    * the `FBA` model, which defines the FBA submodel using the `fbc` package,
    * the `UPDATE` model, which defines the update between the `TOP` and `FBA` model. 
  
  Models and model filenames **SHOULD** contain the word `TOP`, `FBA` and `UPDATE`, respectively to 
  make clear what part of the DFBA model is encoded by the submodel.  
  The different submodels **SHOULD** be stored in separate files.
  
## TOP model
* how related to `FBA` and `UPDATE` model ?
* dummy reaction & respective assignments ?
  
## FBA model
- The `FBA` models **MUST** be encoded using the SBML package `fbc v2`. Variables for all upper and lower bounds **MUST** exist.
The selected objective function in the `FBA` models will be optimized.
- The fba submodel **MUST** be optimizable without any additional information as a stand-alone model, i.e. the model
must be importable in a FBA simulator like cobrapy and result in an optimal solution when optimized.
- The `FBA` submodel(s) **MUST** have the SBOTerm [SBO:0000624 flux balance framework](http://www.ebi.ac.uk/sbo/main/SBO:0000624)  
set as modeling framework on the model element  
```<id="growth_fba" sboTerm="SBO:0000624" ... >```

**Objective function**

- The FBA model **MUST** contain at least one objective function. The optimization objective for the DFBA model 
**MUST** be the active objective in the fba model.
- The objective **MUST** be `maximize`.

**Exchange reaction**

- The unbalanced species in the FBA, which correspond to the species which are changed in the kinetic model 
via the FBA solution **MUST NOT** be encoded via setting `boundaryCondition=True` on the species, 
 but **MUST** be encoded via creating an exchange reaction for the species. I.e. species which are 
 changed via the FBA fluxes have additional exchange reaction in the FBA model.
- The exchange reactions **MUST** have the Species with stoichiometry `1.0` as product and have no substrates (-> 1.0 S), 
i.e. point towards the species and be annotated with the SBOterm  
[SBO:0000627 exchange reaction](http://www.ebi.ac.uk/sbo/main/SBO:0000627)  
TODO: the definition of the direction is different in the SBO term, 
which would require to reverse all FBA exchange fluxes for the update of the metabolites.
 
**Reaction bounds**

The following upper and lower bound default values are set in models: If no flux bounds are specified the default upper flux bound is `1000`, 
and the default lower flux bound is `-1000` for reversible and `0` for irreversible reactions.

The parameters for all flux bounds in the FBA submodel **MUST** be set to numerical values.

### UPDATE
The update model?
* how to name things? 
* how related to the FBA and top model?

### Linking FBA and ode models
Two links must be defined between the FBA model and the kinetic models:
1. How are the species updated based on the FBA flux distributions:
After every FBA step the FBA fluxes are stored where ? in FBA model.

- Michaelis-Menten rule based on the species in the reaction 

2. How are the flux bounds updated before the FBA is run?
- The submodel handling the update of the bounds must contain a parameter `dt` which defines the step size of the FBA optimizations, i.e.
after which time interval the FBA is performed. During the time interval `dt` the FBA flux distribution
is assumed constant. The output time points of the complete simulation, i.e. at which timepoints outputs
are generated must be compatible to `dt`, i.e. the time between output points is `dt`.
- The parameter `dt` is used in calculating the upper and lower bounds based on the availability of the species
 used in the reaction. This ensures that the FBA solution cannot take more than the available species amounts
 in the timestep of duration `dt`

$$r1: A + 2 B -> C+3D$$




### Modeling Framework


* The `TOP`,`UPDATE` and all other `NON-FBA` models **MUST** have the following SBOTerm for the modeling framework
on the model element  
[SBO:0000293 non-spatial continuous framework](http://www.ebi.ac.uk/sbo/main/SBO:0000293)  
```<id="growth_fba" sboTerm="SBO:0000624" ... >```

The coupling of either logical models ([SBO:0000234 logical](http://www.ebi.ac.uk/sbo/main/SBO:0000234)), 
discrete frameworks ([SBO:0000063 discrete framework](http://www.ebi.ac.uk/sbo/main/SBO:0000063)), or spatial continuous frameworks 
 ([SBO:0000292 spatial continuous framework](http://www.ebi.ac.uk/sbo/main/SBO:0000292)) is not yet supported.

? How stochastic or deterministic simulation ? (which SBOTerm)

* The `dt` parameter must be annotated with the SBOTerm ?


## Ports
Objects which are linked via ports in the different submodels **MUST** have the same ids in the the different submodels.
The respective ports **MUST** have the same ids.

* How to annotate (SBO) and how to name (we should have a simple naming convention which should be followed, so
it is clear which ports are belonging to what)?
* How to encode? 
* What must be coupled between the subnetworks?

## Multiple FBA and kinetic models
* How to handle multiple FBA models and kinetic models ?

* How to deal with stochastic models ?
In this first version of the guidlines and implementation no stochastic models are supported. 

# Model Simulation
In this section we describe how simulators should simulate a model given in the DFBA SBML formalism.
The described simulation and update strategy was herby implemented in `iBioSim` and `sbmlutils`.

The DFBA models are solved via a **Static Optimization Approach (SOA)**. The simulation time is
divided into time intervals with the instantaneous optimization (FBA) solved at the beginning
of every time interval. The dynamic equations are than integrated over the time interval assuming that the fluxes
are constant over the interval. 
Before every optimization of the FBA part optimization constraints have to be updated from the dynamic part, after 
every optimization the dynamic variables corresponding to the FBA fluxes have to be updated.


* what is the order of execution of the models ?? & when are the update steps performed ??
* how do we deal with the step sizes and tolerances?


# Questions?
* should we allow stochastic models in this first version? If we say yes, we also need an example for the coupling of 
stochastic to fba models. If we only allow deterministic to FBA coupling in the first version things will be easier.


