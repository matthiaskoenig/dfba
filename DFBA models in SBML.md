# DFBA models in SBML
**version: 0.1-draft**
<!--
Please edit this file ONLY on hackmd.io for now and commit the file when finished with editing to the dfba git via Menu -> Download -> Markdown. Than we have the latest version available on github. Comments in this text via the comment syntax.
-->
* **[latest editable version](https://hackmd.io/IYUwDATAjAZgxiAtAZmFAJogLAdi8xUdJZMZAIyhDjnJzHSA?both)**
* **[github repository](https://github.com/matthiaskoenig/dfba)**

This document describes the rules and guidelines for encoding Dynamic Flux Balance Analysis (DFBA) models in the Systems Biology Markup Language ([SBML](http://sbml.org/Main_Page)), a free and open interchange format for computer models of biological processes.

The document is structured in
* Section A) describes how to encode DFBA models in SBML.
* Section B) provides information on how simulators should execute models provided in the format of Section A). DFBA Implementation are provided by [iBioSim](http://www.async.ece.utah.edu/ibiosim) or [sbmlutils](https://github.com/matthiaskoenig/sbmlutils/).
* Section C) provides answers to frequently asked questions.

The following conventions are used in throughout this document.
* Required rules are stated via **MUST**, i.e. DFBA models in SBML must implement these rules.
* Guidelines which should be followed are indicated by **SHOULD**, i.e. it is good practise to follow these guidelines, but they are not required for an executable DFBA model in SBML.

Example models implementing the rules and guidelines of this document are provided in the `dfba/models` folder of the [github repository](https://github.com/matthiaskoenig/dfba).

The following abbreviations are used in this document
* DFBA : Dynamic Flux Balance Analysis
* FBA : Flux Balance Analysis
* SBML : Systems Biology Markup Language

# A) Encoding DFBA models in SBML
This section describes how DFBA models can be encoded in SBML.
## DFBA model
* The DFBA SBML model **MUST** be a single `comp` model.
* The DFBA submodel **MUST** be encoded in the DFBA model via `comp:SubModel`. The individual submodels **MUST** be encoded via `comp:ExternalModelDefinition` with each submodel being a separate file.
<!-- 
Matthias: I am currently only supporting ExternalModelDefinitions. I can implement the additional direct definition of submodels. Than we can change this rule from **MUST** to **SHOULD** .
-->

* All SBML submodels of the DFBA model **MUST** be encoded in SBML L3V1 or higher.
* The DFBA SBML model and all SBML submodels **MUST** be valid SBML.
* The DFBA model **MUST** be encoded using SBML `core` and the SBML packages `comp` and `fbc`.
* All DFB model and all submodels **SHOULD** only use released SBML packages.
<!-- 
Leandro: This is tricky because we don't support all packages. I think we should require the bare minimum to make a simulatable model for our tools.  

Matthias: I think you misunderstood and we should clarify. This just says you should only use released packages to encode the DFBA, nothing more. It does not say anything about what you have to support.
-->

The DFBA models consists of different units performing part of the DFBA task. These tasks are
* `TOP` : DFBA comp model
* `KINETIC` : kinetic part of the DFBA model
* `FBA` : FBA part of the DFBA model
* `BOUNDS` : calculation of the upper and lower bounds for the `FBA` model
* `UPDATE` : calculation of the updated `KINETIC` part from the `FBA` solution

 **`TODO:`** Create figure showing linking between submodels (this section is unclear, figure will help)

* The DFBA model **MUST** consist of the `comp` model and at least one `comp:SubModel`
    * a `TOP` kinetic model (main DFBA `comp` model)
    * a `FBA` FBA submodel, which defines the FBA submodel using the `fbc` package
    * In the case of a single `FBA` submodel, the `TOP` model performs multiple functions, i.e. the `KINETIC` part of the model, the calculation of the flux bounds (`BOUNDS`) and the update of the kinetic model from the FBA solution (`UPDATE`)

* The DFBA model **SHOULD** consist of the `comp` model and three `comp:SubModels`
    * the `TOP` ode model, which is the SBML top model containing the other submodels, and includes the `KINETIC` part of the DFBA
    * the `FBA` fba model, which defines the FBA submodel using the `fbc` package,
    * the `BOUNDS` ode model, which defines the calculation of the FBA bounds
    * the `UPDATE` ode model, which defines the update of the `TOP` model from the `FBA` model.

* The `TOP`,`UPDATE` and all other `NON-FBA` models **MUST** have the SBOTerm [SBO:0000293 non-spatial continuous framework](http://www.ebi.ac.uk/sbo/main/SBO:0000293) defining the modeling framework on the model element .

In the following sections the guidelines for the individual submodels are specified
  
## FBA submodel
* The `FBA` models **MUST** be encoded using the SBML package `fbc-v2` with `strict=false`. 
* The `FBA` submodel(s) **MUST** have the SBOTerm [SBO:0000624 (flux balance framework)](http://www.ebi.ac.uk/sbo/main/SBO:0000624) set as modeling framework on the `model` element.
* Exactly one `fbc` submodel **MUST** exist in the DFBA model, i.e. multiple `fbc` submodels are currently not supported.
* The fba submodel **MUST** be optimizable without any additional information as a stand-alone model, i.e. the model **MUST** be importable in a FBA simulator like cobrapy and result in an optimal solution when optimized.
* The `reactions` in the FBA model `MUST NOT` have any `KineticLaw`.
<!--
Leandro: The FBA model **MUST** consist only of `parameters`, `species`, `compartments`, and `reactions` are allowed. Reactions should not have kinetic law.
Matthias: I think this is too restrictive. We should allow valid FBA models encoded in fbc-v2.
I added the no KineticLaw as rule above.
-->

### Objective function
* The FBA model **MUST** contain at least one objective function.
* The optimization objective for the DFBA model **MUST** be the active objective in the fba model, i.e. an active objective **MUST** exist and be the objective which is executed in every step of the DFBA.
* The objective **MUST** be `maximize`.
<!--
@Leandro: Will this always be the case?
@Matthias: Are you supporting minimize? If yes we can make this minimize or maximize (I am only supporting maximize right now, but could easily implement minimize as well)
-->

### Exchange reaction
* The unbalanced species in the FBA, which correspond to the species which are changed in the kinetic model via the FBA solution **MUST NOT** be encoded via setting `boundaryCondition=True` on the species, but **MUST** be encoded via creating an exchange reaction for the species. I.e. species which are changed via the FBA fluxes have additional exchange reaction in the FBA model.
<!--
Leandro: This is not how I have done the FBA models but it seems it works in our tool. Would need to change my model and verify.
Matthias: This would be great because it simplifies many things for me. Also we could easily use FBA models which are encoded in this way, like the BiGG models. 
-->

* * The exchange reactions **MUST** have the Species with stoichiometry `1.0` as product and have no substrates (-> 1.0 S), i.e. point towards the species and be annotated with the SBOterm [SBO:0000627 exchange reaction](http://www.ebi.ac.uk/sbo/main/SBO:0000627)  
`TODO:` the definition of the direction is different in the SBO term, which would require to reverse all FBA exchange fluxes for the update of the metabolites.
<!--
--@Leandro: Tricky when we use reversible reaction in the FBA model and want to do DFBA with stochastic simulation. 
Matthias: no stochastic simulations for now, but we have to plan for this.
-->
 
### Reaction bounds
* SBML `Parameters` for upper and lower bounds **MUST** exist for all reactions and have numerical values, i.e. no `InitialAssignments` or `AssignmentRules` for flux bound parameter are allowed.
* The following upper and lower bound default values **MUST** be set in fba models: If no flux bounds are specified the default upper flux bound is `1000`, and the default lower flux bound is `-1000` for reversible and `0` for irreversible reactions.
<!-- 
Matthias: not sure about that. We probably should change that to: All reactions **MUST** have upper and lower flux bounds defined. This would make things more consistent.
-->

* The `Parameters` for the upper and lower bounds of reactions **SHOULD** have the ids `ub_{rid}` and `lb_{rid}` with `{rid}` being the respective reaction id.
<!--
Leandro: Can they use default values?
Matthias: I don't understand that? What do you mean?
-->

* SBML `Parameters` describing the flux bounds of exchange reactions **MUST** be `constant=False`. All exchange reactions must have individual `Parameters` for the upper and lower bound which are not used by other reactions. 
* SBML `Parameters` describing the flux bounds of internal reactions **MUST** be `constant=False`.

### Ports
* All exchange reactions `MUST` have a port.
* All upper and lower bounds of the exchange reactions `MUST` have a port.
* Apecies used in exchange reactions `MUST` have a port.
* Compartments for species used in exchange reactions `MUST` have a port.


## TOP model
* how related to `FBA` and `UPDATE` model ?
* dummy reaction & reactant.
* @Leandro: Do we need KISAO for DFBA?
* @Leandro: should we allow any SBML core? events, algebraic, delay, etc?  
@Matthias: yes, everything but delays and algebraic rules

## UPDATE model
* how to name things? 
* how related to the FBA and top model?

## BOUNDS model
* This should contain bound parameters for every reaction in the FBA that does not use default bounds. 
* Should have species values to compute how much reactions can be fired.

## Linking FBA and ode models
Two links must be defined between the FBA model and the kinetic models:
1. How are the species updated based on the FBA flux distributions:
After every FBA step the FBA fluxes are stored where ? in FBA model.

* Michaelis-Menten rule based on the species in the reaction (@Leandro: shouldn't this be in the update?)

2. How are the flux bounds updated before the FBA is run?
* The submodel handling the update of the bounds must contain a parameter `dt` which defines the step size of the FBA optimizations, i.e. after which time interval the FBA is performed. During the time interval `dt` the FBA flux distribution is assumed constant. The output time points of the complete simulation, i.e. at which timepoints outputs are generated must be compatible to `dt`, i.e. the time between output points is `dt`.
* The parameter `dt` is used in calculating the upper and lower bounds based on the availability of the species used in the reaction. This ensures that the FBA solution cannot take more than the available species amounts in the timestep of duration `dt`

@Leandro: should dt be defined in the top? Can simulation time be updated using t = t + dt?
Ambiguous with SED-ML?
@Matthias: Yes dt should be in top. Yes, t(i+1) = t(i) + dt, but this only defines when the FBA is executed.

$$r1: A + 2 B -> C+3D$$

## Ports
* Objects which are linked via ports in the different submodels **MUST** have the same ids in the the different submodels. * The respective ports **MUST** have the same ids.
* All `comp:Port` elements **SHOULD** follow the following id schema: `{idRef}_port` for a port with `idRef={idRef}`.
* How to annotate (SBO) and how to name (we should have a simple naming convention which should be followed, so it is clear which ports are belonging to what)?
* How to encode? 
* What must be coupled between the subnetworks?

## SBOTerms
This section gives an overview over the SBOterms used in DFBA models. 
* `TODO:` collect and list all SBOTerms we use


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