# DFBA models in SBML
* **[Latest editable version](https://hackmd.io/IYUwDATAjAZgxiAtAZmFAJogLAdi8xUdJZMZAIyhDjnJzHSA?both)**
* **[github repository](https://github.com/matthiaskoenig/dfba)**

<!--
Please edit this file ONLY on hackmd.io for now and commit the file when finished with editing to the dfba git via Menu -> Download -> Markdown. Than we have the latest version available on github. Comments in this text via the comment syntax.
-->
This document describes the rules and guidelines for encoding Dynamic Flux Balance Analysis (DFBA) models in SBML in section A. In addition information is provided on how the simulators `iBioSim` and `sbmlutils` implement the DFBA. The following conventions are used in this document.
* required rules are stated via **MUST**. DFBA models in SBML must implement this rules.
* guidelines which should be followed are indicated by **SHOULD**.

The example models in the [github repository](https://github.com/matthiaskoenig/dfba) in the `dfba/models` folder implement these rules & guidelines.

# A) Encoding DFBA models in SBML
## Models
The DFBA model in SBML consists of multiple SBML submodels.
* All SBML models for DFBA **MUST** be encoded in SBML L3V1 or higher.
* All SBML models **MUST** be valid SBML.
* The DFBA model **MUST** be encoded using the `comp` and `fbc` packages.
* All SBML models **SHOULD** only use released SBML packages.
* The DFBA model **SHOULD** consist of four submodels:
    * the `TOP` ode model, which is the SBML top model including the other submodels via `comp:ExternalModelDefinitions` 
    * the `FBA` fba model, which defines the FBA submodel using the `fbc` package,
    * the `BOUNDS` ode model, which defines the calculation of the FBA bounds
    * the `UPDATE` ode model, which defines the update of the `TOP` model from the `FBA` model.
    
  Models and model filenames **SHOULD** contain the word `TOP`, `FBA`, `BOUNDS` and `UPDATE`, respectively to 
  make clear what part of the DFBA model is encoded by the submodel.  
  The different submodels **SHOULD** be stored in separate files.
* The DFBA model **MUST** consist of at least two models:
    * the `TOP` model, which in this case includes the `BOUNDS` and `UPDATE` logic
    * the `FBA` fba model, which defines the FBA submodel using the `fbc` package
  
**Ports**
- All `comp:Port` elements **SHOULD** follow the following id schema: `{idRef}_port` for a port with `idRef={idRef}`.
  
## FBA model
- The `FBA` models **MUST** be encoded using the SBML package `fbc v2` with `strict=false`. 
- The `FBA` submodel(s) **MUST** have the SBOTerm [SBO:0000624 flux balance framework](http://www.ebi.ac.uk/sbo/main/SBO:0000624) set as modeling framework on the `model` element.

The selected objective function in the `FBA` models will be optimized.
- The fba submodel **MUST** be optimizable without any additional information as a stand-alone model, i.e. the model
**MUST** be importable in a FBA simulator like cobrapy and result in an optimal solution when optimized.

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
- SBML `Parameters` for upper and lower bounds **MUST** exist for all reactions and have numerical values, i.e. no `InitialAssignments` or
`AssignmentRules` for flux bound parameter are allowed.
- The following upper and lower bound default values **MUST** be set in fba models: If no flux bounds are specified the default upper flux bound is `1000`, 
and the default lower flux bound is `-1000` for reversible and `0` for irreversible reactions.
- The `Parameters` for the upper and lower bounds of reactions **SHOULD** have the ids `ub_{rid}` and `lb_{rid}` with `{rid}`
being the respective reaction id.
- SBML `Parameters` describing the flux bounds of exchange reactions **MUST** be `constant=False`. All exchange reactions
must have individual `Parameters` for the upper and lower bound which are not used by other reactions.

- SBML `Parameters` describing the flux bounds of internal reactions where the **MUST** be `constant=False`.

**Ports**
- all exchange reactions `MUST` have a port
- all upper and lower bounds of the exchange reactions `MUST` have a port
- species used in exchange reactions `MUST` have a port
- compartments for species used in exchange reactions `MUST` have a port


## TOP model
* how related to `FBA` and `UPDATE` model ?
* dummy reaction & respective assignments ?

## UPDATE model
The update model?
* how to name things? 
* how related to the FBA and top model?

## BOUNDS model

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
on the model element [SBO:0000293 non-spatial continuous framework](http://www.ebi.ac.uk/sbo/main/SBO:0000293).

The coupling of either logical models ([SBO:0000234 logical](http://www.ebi.ac.uk/sbo/main/SBO:0000234)), 
discrete frameworks ([SBO:0000063 discrete framework](http://www.ebi.ac.uk/sbo/main/SBO:0000063)), or spatial continuous frameworks 
 ([SBO:0000292 spatial continuous framework](http://www.ebi.ac.uk/sbo/main/SBO:0000292)) is not yet supported.


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

## SBOTerm
This section gives an overview over the SBOterms used in DFBA models. 
* TODO: collect the SBOTerms


# B) Model Simulation
In this section we describe how simulators should simulate a model given in the DFBA SBML formalism described in section A. The described simulation and update strategy was implemented in the two simulators `iBioSim` and `sbmlutils`.

The DFBA models are solved via a **Static Optimization Approach (SOA)**. The simulation time is divided into time intervals with the instantaneous optimization (FBA) solved at the beginning of every time interval. The dynamic equations are than integrated over the time interval assuming that the fluxes
are constant over the interval. 
Before every optimization of the FBA part optimization constraints have to be updated from the dynamic part, after every optimization the dynamic variables corresponding to the FBA fluxes have to be updated.


* what is the order of execution of the models ?? & when are the update steps performed ??
* how do we deal with the step sizes and tolerances?


# C) Open Questions
* should we allow stochastic models in this first version? If we say yes, we also need an example for the coupling of 
stochastic to fba models. If we only allow deterministic to FBA coupling in the first version things will be easier.


