# DFBA models in SBML
**version: 0.1-draft**
<!--
Please edit this file ONLY on hackmd.io for now and commit the file when finished with editing to the dfba git via Menu -> Download -> Markdown. Than we have the latest version available on github. Comments in this text via the comment syntax.
-->
* **[latest editable version](https://hackmd.io/IYUwDATAjAZgxiAtAZmFAJogLAdi8xUdJZMZAIyhDjnJzHSA?both)**
* **[github repository](https://github.com/matthiaskoenig/dfba)**

This document describes the rules and guidelines for encoding Dynamic Flux Balance Analysis (DFBA) models in the Systems Biology Markup Language (SBML), a free and open interchange format for computer models of biological processes.
* Section A) describes how to encode DFBA models in SBML.
* Section B) provides information on how simulators should execute models provided in the format of Section A). Example implementations can be found in `iBioSim` and `sbmlutils` implement the DFBA. 
* Section C) provides answers to frequently asked questions.

The following conventions are used in this document.
* Required rules are stated via **MUST**, i.e. DFBA models in SBML must implement these rules.
* Guidelines which should be followed are indicated by **SHOULD**, i.e. it is good practise to follow these guidelines, but they are not required for an executable DFBA model in SBML.

The example models in the [github repository](https://github.com/matthiaskoenig/dfba) in the `dfba/models` folder implement these rules and guidelines.

# A) Encoding DFBA models in SBML
This section describes how DFBA models can be 


The DFBA model in SBML consists of multiple SBML submodels.

* All SBML models for DFBA **MUST** be encoded in SBML L3V1 or higher.
* All SBML models **MUST** be valid SBML.
* The DFBA model **MUST** be encoded using the `comp` and `fbc` packages.
<!-- @Leandro: This is tricky because we don't support all packages. I think we should require the bare minimum to make a simulatable model for our tools.  
@Matthias: I think you misunderstood and we should clarify. This just says you should use comp & fbc to encode the DFBA, nothing more. We are doing this. It not even says that you have to support all of comp or fbc.
-->

* All SBML models **SHOULD** only use released SBML packages.


--@Leandro: This is ambiguous with the next requirement. This one says it should contain four and the next says it needs at least two. Maybe this should change to at most four submodels.
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
 
 **`TODO:`** Create figure showing linking between submodels

In the following sections the guidelines for the individual submodels are specified
  
### FBA submodel
* The `FBA` models **MUST** be encoded using the SBML package `fbc-v2` with `strict=false`. 
* The `FBA` submodel(s) **MUST** have the SBOTerm [SBO:0000624 (flux balance framework)](http://www.ebi.ac.uk/sbo/main/SBO:0000624) set as modeling framework on the `model` element.
* There **MUST** be exactely one submodel with `fbc` and [SBO:0000624](http://www.ebi.ac.uk/sbo/main/SBO:0000624) in the `comp` model. Multiple `fbc` submodels are not allowed.


- The fba submodel **MUST** be optimizable without any additional information as a stand-alone model, i.e. the model
**MUST** be importable in a FBA simulator like cobrapy and result in an optimal solution when optimized.

**Objective function**
* The FBA model **MUST** contain at least one objective function.
* The optimization objective for the DFBA model **MUST** be the active objective in the fba model, i.e. an active objective **MUST** exist and be the objective which is executed in every step of the DFBA.
* The objective **MUST** be `maximize`.
<!--
@Leandro: Will this always be the case?
@Matthias: Are you supporting minimize? If yes we can make this minimize or maximize (I am only supporting maximize right now, but could easily implement minimize as well)
-->

**Exchange reaction**

- The unbalanced species in the FBA, which correspond to the species which are changed in the kinetic model 
via the FBA solution **MUST NOT** be encoded via setting `boundaryCondition=True` on the species, 
 but **MUST** be encoded via creating an exchange reaction for the species. I.e. species which are 
 changed via the FBA fluxes have additional exchange reaction in the FBA model.
 -- @Leandro: This is not how I have done the FBA models but it seems it works in our tool. Would need to change my model and verify.
- The exchange reactions **MUST** have the Species with stoichiometry `1.0` as product and have no substrates (-> 1.0 S), 
i.e. point towards the species and be annotated with the SBOterm  
[SBO:0000627 exchange reaction](http://www.ebi.ac.uk/sbo/main/SBO:0000627)  
TODO: the definition of the direction is different in the SBO term, 
which would require to reverse all FBA exchange fluxes for the update of the metabolites.
--@Leandro: Tricky when we use reversible reaction in the FBA model and want to do DFBA with stochastic simulation. 
 
**Reaction bounds**
- SBML `Parameters` for upper and lower bounds **MUST** exist for all reactions and have numerical values, i.e. no `InitialAssignments` or
`AssignmentRules` for flux bound parameter are allowed.
-- @Leandro: In the FBA, only parameters, species, compartment(s), and reactions are allowed. Reactions should not have kinetic law.

- The following upper and lower bound default values **MUST** be set in fba models: If no flux bounds are specified the default upper flux bound is `1000`, 
and the default lower flux bound is `-1000` for reversible and `0` for irreversible reactions.
- The `Parameters` for the upper and lower bounds of reactions **SHOULD** have the ids `ub_{rid}` and `lb_{rid}` with `{rid}`
being the respective reaction id.
-- @Leandro: Can they use default values?
- SBML `Parameters` describing the flux bounds of exchange reactions **MUST** be `constant=False`. All exchange reactions
must have individual `Parameters` for the upper and lower bound which are not used by other reactions. 
- SBML `Parameters` describing the flux bounds of internal reactions where the **MUST** be `constant=False`.
--@Leandro: missing something at "where the ..."

**Ports**
- all exchange reactions `MUST` have a port
- all upper and lower bounds of the exchange reactions `MUST` have a port
- species used in exchange reactions `MUST` have a port
- compartments for species used in exchange reactions `MUST` have a port


## TOP model
* how related to `FBA` and `UPDATE` model ?
* dummy reaction & reactant.
* @Leandro: Do we need KISAO for DFBA?
* @Leandro: should we allow any SBML core? events, algebraic, delay, etc?
## UPDATE model
The update model?
* how to name things? 
* how related to the FBA and top model?

## BOUNDS model
* This should contain bound parameters for every reaction in the FBA that does not use default bounds. 
* Should have species values to compute how much reactions can be fired.

### Linking FBA and ode models
Two links must be defined between the FBA model and the kinetic models:
1. How are the species updated based on the FBA flux distributions:
After every FBA step the FBA fluxes are stored where ? in FBA model.

- Michaelis-Menten rule based on the species in the reaction (@Leandro: shouldn't this be in the update?)

2. How are the flux bounds updated before the FBA is run?
- The submodel handling the update of the bounds must contain a parameter `dt` which defines the step size of the FBA optimizations, i.e.
after which time interval the FBA is performed. During the time interval `dt` the FBA flux distribution
is assumed constant. The output time points of the complete simulation, i.e. at which timepoints outputs
are generated must be compatible to `dt`, i.e. the time between output points is `dt`.
- The parameter `dt` is used in calculating the upper and lower bounds based on the availability of the species
 used in the reaction. This ensures that the FBA solution cannot take more than the available species amounts
 in the timestep of duration `dt`
-- @Leandro: should dt be defined in the top? Can simulation time be updated using t = t + dt? Ambiguous with SED-ML?
$$r1: A + 2 B -> C+3D$$


### Modeling Framework

* The `TOP`,`UPDATE` and all other `NON-FBA` models **MUST** have the following SBOTerm for the modeling framework
on the model element [SBO:0000293 non-spatial continuous framework](http://www.ebi.ac.uk/sbo/main/SBO:0000293).


<!-- How to do ODE + SSA + Logical? -->
* @Leandro: does not support coupling of different frameworks. All submodels should be consistent.

## Ports
Objects which are linked via ports in the different submodels **MUST** have the same ids in the the different submodels.
The respective ports **MUST** have the same ids.

* All `comp:Port` elements **SHOULD** follow the following id schema: `{idRef}_port` for a port with `idRef={idRef}`.

* How to annotate (SBO) and how to name (we should have a simple naming convention which should be followed, so
it is clear which ports are belonging to what)?
* How to encode? 
* What must be coupled between the subnetworks?


## SBOTerm
This section gives an overview over the SBOterms used in DFBA models. 
* TODO: collect the SBOTerms


# B) Model Simulation
In this section we describe how simulators should simulate a model given in the DFBA SBML formalism described in section A. The described simulation and update strategy was implemented in the two simulators `iBioSim` and `sbmlutils`.

**`TODO:`** Create figure showing simulation workflow

The DFBA models are solved via a **Static Optimization Approach (SOA)**. The simulation time is divided into time intervals with the instantaneous optimization (FBA) solved at the beginning of every time interval. The dynamic equations are than integrated over the time interval assuming that the fluxes
are constant over the interval. 
Before every optimization of the FBA part optimization constraints have to be updated from the dynamic part, after every optimization the dynamic variables corresponding to the FBA fluxes have to be updated.

* what is the order of execution of the models ?? & when are the update steps performed ??
* how do we deal with the step sizes and tolerances?

# C) Frequently asked questions (FAQ)
## Are multiple kinetic models supported?
Yes, multiple kinetic submodels can exist in the DFBA. During the kinetic integrations the flattend kinetic model is integrated.

## Are multiple FBA submodels supported?
No, in the first version only a single FBA submodel is allowed.
<!-- 
@Leandro: Is it possible to have FBA models that depend on each other? Order of execution would matter.
@Matthias: I would say we keep it as simple as possible in the first version, i.e. only one FBA submodel. We have to think about what to do with multiple FBA models in the future. Things to consider are
* execution order
* resource allocation, i.e. boundary condition via species.
A possible solution could be merging of the FBA models and 
creating one overall optimization function. But we should not touch this in the first version.
-->


## Are stochastic & logical models supported?
It is possible to encode SBML models with additional modeling frameworks than FBA or deterministic ODE models. Examples are logical models encoded with the SBML package `qual` or stochastic models, i.e. stochastic ODE models. In the first version of the DFBA guidelines and implementation only deterministic kinetic models can be coupled to FBA models. In future versions the coupling of stochastic and/or logical models can be supported.

The coupling of either logical models ([SBO:0000234 logical](http://www.ebi.ac.uk/sbo/main/SBO:0000234)), 
discrete frameworks ([SBO:0000063 discrete framework](http://www.ebi.ac.uk/sbo/main/SBO:0000063)), or spatial continuous frameworks 
 ([SBO:0000292 spatial continuous framework](http://www.ebi.ac.uk/sbo/main/SBO:0000292)) is not yet supported.