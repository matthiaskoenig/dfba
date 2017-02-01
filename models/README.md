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

## SBO terms

### Modeling Framework
* The `FBA` submodel **MUST** have the following SBOTerm on the model element  
[SBO:0000624 flux balance framework](http://www.ebi.ac.uk/sbo/main/SBO:0000624)  
```<id="growth_fba" sboTerm="SBO:0000624" ... >```


## Ports
?

## Multiple FBA and kinetic models
* ? How to handle multiple FBA models and kinetic models.

* ? How to deal with stochastic models.
In this first version 

# Model Simulation
* mix of stochastic & deterministic models ?
In this first version all kinetic models **MUST** be executed with the same algorithm and method, 
i.e. all kinetic submodels **MUST** be either deterministic or stochastic 

* what is the order of execution of the models ?? & when are the update steps performed ??



