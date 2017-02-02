# Encoding DFBA models in SBML
In this document the guidelines for encoding DFBA models in SBML are described.


The example models in the `models` folder follow these guidelines.
Strict rules which have to be followed are indicated via **MUST**, guidlines which should be followed are indicated
by **SHOULD**.

## Model Validity
* All SBML models **MUST** be valid SBML.
* All SBML models **MUST** be encoded in SBML L3V1 or higher.

## SBML Packages
* ALL SBML models **SHOULD** only use released SBML packages.

## Models
* The DFBA model **MUST** be encoded using the `comp` package.  
* The **MUST** at least consist of three submodels:
    * the `TOP` model, which is the SBML top model including the other models, 
    * the `FBA` model, which defines the FBA submodel using the `fbc` package,
    * the `UPDATE` model, which defines the update between the `TOP` and `FBA` model. 
  
  Models and model filenames **SHOULD** contain the word `TOP`, `FBA` and `UPDATE`, respectively to 
  make clear what part of the DFBA model is encoded by the submodel.  
  The different submodels **SHOULD** be stored in separate files.
  
### TOP
* how related to `FBA` and `UPDATE` model ?
  
### FBA
The `FBA` models **MUST** be encoded using the SBML package `fbc v2`. Variables for all upper and lower bounds **MUST** exist.
The selected objective function in the `FBA` models will be optimized.

* How the bounds?
* How the objective functions?
* What is optimized / maximization/minimization?

### UPDATE
The update model?
* how to name things? 
* how related to the FBA and top model?


## SBO terms

### Modeling Framework
* The `FBA` submodel(s) **MUST** have the following SBOTerm for the modeling framework on the model element  
[SBO:0000624 flux balance framework](http://www.ebi.ac.uk/sbo/main/SBO:0000624)  
```<id="growth_fba" sboTerm="SBO:0000624" ... >```

* The `TOP`,`UPDATE` and all other `NON-FBA` models **MUST** have the following SBOTerm for the modeling framework
on the model element  
[SBO:0000293 non-spatial continuous framework](http://www.ebi.ac.uk/sbo/main/SBO:0000293)  
```<id="growth_fba" sboTerm="SBO:0000624" ... >```

The coupling of either logical models ([SBO:0000234 logical](http://www.ebi.ac.uk/sbo/main/SBO:0000234)), 
discrete frameworks ([SBO:0000063 discrete framework](http://www.ebi.ac.uk/sbo/main/SBO:0000063)), or spatial continuous frameworks 
 ([SBO:0000292 spatial continuous framework](http://www.ebi.ac.uk/sbo/main/SBO:0000292)) is not yet supported.

? How stochastic or deterministic simulation ? (which SBOTerm)


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


