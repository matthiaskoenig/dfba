# DFBA models in SBML
**version: 0.1-draft**
<!--
Please edit this file ONLY on hackmd.io for now and commit the file when finished with editing to the dfba git via Menu -> Download -> Markdown. Than we have the latest version available on github. Comments in this text via the comment syntax.
-->
* **[latest editable version](https://hackmd.io/IYUwDATAjAZgxiAtAZmFAJogLAdi8xUdJZMZAIyhDjnJzHSA?both)**
* **[github repository](https://github.com/matthiaskoenig/dfba)**

This document describes the rules and guidelines for encoding Dynamic Flux Balance Analysis (DFBA) models in the Systems Biology Markup Language ([SBML](http://sbml.org/Main_Page)), a free and open interchange format for computer models of biological processes.

The document is structured in
* **Section A**: describes how to encode DFBA models in SBML.
* **Section B**: provides information on how simulators should execute models provided in the format of Section A). DFBA Implementation are provided by [iBioSim](http://www.async.ece.utah.edu/ibiosim) or [sbmlutils](https://github.com/matthiaskoenig/sbmlutils/).
* **Section C**: provides answers to frequently asked questions.

The following conventions are used throughout this document.
* Required rules are stated via **MUST**, i.e. DFBA models in SBML must implement these rules.
* Guidelines which should be followed are indicated by **SHOULD**, i.e. it is good practice to follow these guidelines, but they are not required for an executable DFBA model in SBML. [iBioSim](http://www.async.ece.utah.edu/ibiosim) and [sbmlutils](https://github.com/matthiaskoenig/sbmlutils/) will run the DFBA even if these recommendations are not followed.
* Curly brackets function as place holders. For instance the reaction id `{rid}` means that `{rid}` is replaced with the actual id of the reaction.

Example models implementing the rules and guidelines of this document are provided in the `dfba/models` folder of the [github repository](https://github.com/matthiaskoenig/dfba).

The following abbreviations are used in this document
* DFBA : Dynamic Flux Balance Analysis
* FBA : Flux Balance Analysis
* SBML : Systems Biology Markup Language


<!------------------------------------------------------------------->
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
* All DFBA model and submodels **SHOULD** only use released SBML packages.
<!-- 
Leandro: This is tricky because we don't support all packages. I think we should require the bare minimum to make a simulatable model for our tools.  

Matthias: I think you misunderstood and we should clarify. This just says you should only use released packages to encode the DFBA, nothing more. It does not say anything about what you have to support.
-->

The DFBA models consists of different units performing parts of the DFBA task. These tasks are
* `TOP` : DFBA comp model that includes all submodels and their corresponding connections
* `KINETIC` : kinetic part of the DFBA model
* `FBA` : FBA part of the DFBA model
* `BOUNDS` : calculation of the upper and lower bounds for the `FBA` model
* `UPDATE` : calculation of the updated `KINETIC` part from the `FBA` solution

 **`TODO:`** Create figure showing linking between submodels (this section is unclear, figure will help. Show the different alternatives)

* The DFBA model **MUST** consist of the `comp` model and at least one `comp:SubModel`
    * a `TOP` kinetic model (main DFBA `comp` model)
    * a `FBA` FBA submodel, which defines the FBA submodel using the `fbc` package
    * In the case of a single `FBA` submodel, the `TOP` model performs multiple functions, i.e. the `KINETIC` part of the model, the calculation of the flux bounds (`BOUNDS`) and the update of the kinetic model from the FBA solution (`UPDATE`)

* The DFBA model **SHOULD** consist of the `comp` model and three `comp:SubModels`
    * the `TOP` ode model, which is the SBML top model containing the other submodels, and includes the `KINETIC` part of the DFBA
    * the `FBA` fba model, which defines the FBA submodel using the `fbc` package,
    * the `BOUNDS` ode model, which defines the calculation of the FBA bounds
    * the `UPDATE` ode model, which defines the update of the `TOP` model from the `FBA` model.

### Modeling Frameworks
* Every model other than `FBA` **MUST** have the SBOTerm [`SBO:0000293` (non-spatial continuous framework)](http://www.ebi.ac.uk/sbo/main/SBO:0000293) defining the modeling framework on the model element .

### Ports
Objects in the different submodels are linked via `comp:Ports`.
* Objects which are linked via ports in the different submodels **MUST** have the same ids in the the different submodels. 
* In addition, the respective ports of the linked objects **MUST** have the same ids.
* All `comp:Port` elements **SHOULD** hereby follow the id schema: id of the port is `{idRef}_port` for an object with `idRef={idRef}`.

### Units
* All models **SHOULD** include units.

In the following sections the guidelines for the individual submodels are specified.
  
## FBA submodel
* The `FBA` models **MUST** be encoded using the SBML package `fbc-v2` with `strict=false`. 
* The `FBA` submodel(s) **MUST** have the SBOTerm [`SBO:0000624` (flux balance framework)](http://www.ebi.ac.uk/sbo/main/SBO:0000624) set as modeling framework on the `model` element.
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

* The exchange reactions **MUST** have the Species with stoichiometry `1.0` as product and have no substrates (-> 1.0 S), i.e. point towards the species and be annotated with the SBOterm [`SBO:0000627` (exchange reaction)](http://www.ebi.ac.uk/sbo/main/SBO:0000627).  
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
* Species used in exchange reactions `MUST` have a port.
* Compartments for species used in exchange reactions `MUST` have a port.


## TOP model

### dt
* The `TOP` DFBA model **MUST** contain a parameter `dt` which defines the step size of the FBA optimizations, i.e. after which time interval the FBA is performed. 
* The `dt` parameter **MUST** be annotated with the SBOTerm [`SBO:0000346` (temporal measure)](http://www.ebi.ac.uk/sbo/main/SBO:0000346).
<!--
Matthias: what is the correct SBOTerm for dt. I used the temporal measurement for now.
-->

### Dummy reactions
* The top model **MUST** include a dummy species with `id="dummy_S"` with the SBOTerm [`SBO:0000291` (empty set)](http://www.ebi.ac.uk/sbo/main/SBO:0000291). This species is required for the definition of the dummy reactions in SBML L3V1.
<!--
Matthias: We should move to L3V2, where there is no more
requirement for the dummy species. This would simplify and clarify things, i.e. remove the dummy species rules.
I have to check if roadrunner is supporting this, if yes we can go to L3V2.
Also no real SBOTerm fitting for dummy species or reaction. Using empty set for now.
-->
* For every exchange reaction in the `FBA` submodel, there **MUST** be exist a dummy reaction in the `TOP`. The id of the dummy reaction **MUST** be `id="dummy_{rid}"` for the respective exchange reaction with `id="{rid}"` in the `FBA` submodel.
* Each dummy reaction **MUST** include the dummy species `dummy_S` as product with stochiometry `1.0`. No other reactants, products or modifiers are allowed on the dummy reactions. 
* The dummy reactions **MUST** have the SBOTerm [`SBO:0000631` (pseudoreaction)](http://www.ebi.ac.uk/sbo/main/SBO:0000631).

### Flux AssignmentRules
For every exchange reaction in the `FBA` with `id="{rid}"` and the corresponding dummy reaction in the `TOP` model with `id="dummy_{rid}"` an `AssignmentRule` in the `TOP` model **MUST** exist of form
```
{rid} = {dummy_rid}
```
### ReplacedBy
For every dummy reaction in the `TOP` model with `id="dummy_{rid}"` must be replaced via a `comp:ReplacedBy` with the corresponding exchange reaction with `id={rid}` from the `FBA` submodel. The `comp:ReplacedBy` uses the `portRef` of the exchange reaction `{rid}_port`.
<!--
Matthias: Not sure if this part is needed. This is how I am encoding my models right now. I am using this ReplacedBy for the update of kinetic modek based on the FBA solution
-->

## UPDATE submodel
The `UPDATE` model can be part of the `TOP` model or a separate submodel.
* All species and reactions in the UPDATE submodel **MUST** be named as the species and reactions in the FBA submodel.
* The UPDATE submodel **MUST** be structurely equivalent to the FBA submodel. The only difference should be reactions in the UPDATE submodel should use kinetic law and the FBA submodel should use flux bounds.
* All reactions in the UPDATE submodel **MUST** have a kinetic law that depends on a parameter being replaced by another parameter in the TOP model. 
* The parameters that appear in the reactions kinetic law **SHOULD** be a function of the computed fluxes of the FBA submodel.
<!--how to name things? -->
<!--how related to the FBA and top model?-->

## BOUNDS submodel
The `BOUNDS` submodel is used for the calculation of the upper and lower bounds for the `FBA` model. For the calculation the species changed by FBA and the time step `dt` are required. The `BOUNDS` model can be part of the `TOP` model or a separate submodel.
* The submodel handling the update of the bounds **MUST** contain a parameter `dt` which defines the step size of the FBA optimizations, i.e. after which time interval the FBA is performed. The `BOUNDS` submodel `dt` must be linked via a port to the `TOP` model `dt`. The `dt` parameter **MUST** be annotated with the SBOTerm [`SBO:0000346` (temporal measure)](http://www.ebi.ac.uk/sbo/main/SBO:0000346).  
If the `BOUNDS` model is part of the `TOP` model this rule is obsolete.
<!-- 
@Leandro: should dt be defined in the top? Can simulation time be updated using t = t + dt?
Ambiguous with SED-ML?
@Matthias: Yes dt should be in top. But if there is separate model for bounds calculation dt must be mirrored there.
Yes, t(i+1) = t(i) + dt, but this only defines when the FBA is executed. I updated the rules above accordingly and added the info to the simulation section.
-->

* This **MUST** contain bound parameters for every reaction in the FBA that does not use default bounds. 
* **MUST** have species values to compute how much reactions can be fired.


## Linking FBA with ODE model
<!-- 
Matthias: this section should be removed and the infromation merged with the `BOUNDS`, `UPDATE` model parts and the simulation section
-->

Two links are required between the FBA model and the kinetic models: 
* Update of flux bounds in the FBA model from the kinetic model. 
* Update of species in kinetic model which are changed by FBA boundary reactions.

### Update of flux bounds
* The parameter `dt` is used in calculating the upper and lower bounds based on the availability of the species used in the reaction. This ensures that the FBA solution cannot take more than the available species amounts in the timestep of duration `dt`

$$r1: A + 2 B -> C+3D$$

`TODO:` fill in the rules/math which must be added for bounds update

### Update of species from FBA solutions
* After every FBA step the fluxes of the optimal FBA solution **MUST** be stored in the respective dummy reactions in the `TOP` model.
<!--
Matthias: this is more simulation section than model definition section.
-->
* Michaelis-Menten rule based on the species in the reaction kinetic law. This ensures the species will not go negative.

`TODO:` fill in the Michaelis menten rules. Which form? How does this work?


<!------------------------------------------------------------------->
# B) Model Simulation
In this section we describe how simulators should simulate a model given in the DFBA SBML formalism described in section A. The described simulation and update strategy was implemented in the two simulators `iBioSim` and `sbmlutils`.

Currently, all SBML core constructs are supported in the kinetic models with the exception of `Delay` and `AlgebraicRule`.

**`TODO:`** Create figure showing simulation workflow

The DFBA models are solved via a **Static Optimization Approach (SOA)**. The simulation time is divided into time intervals with the instantaneous optimization (FBA) solved at the beginning of every time interval. The dynamic equations are than integrated over the time interval assuming that the fluxes
are constant over the interval. 
Before every optimization of the FBA part optimization constraints have to be updated from the dynamic part, after every optimization the dynamic variables corresponding to the FBA fluxes have to be updated.

The simulation algorithm starts off by computing the reaction fluxes in the FBA submodel. The reaction fluxes updates the reaction values in the TOP model, which are used to compute the reaction rates in the UPDATE submodel. Once the reaction fluxes are computed by FBA, all NON-FBA submodels are updated concurrently.

* The output time points **MUST** be in agreement with the `dt` parameter, i.e. the interval between subsequent time points **MUST** be `dt`. This does not affect the internal steps of the kinetic solver.
* If the FBA optimization encounters an infeasible solution the simulation **MUST** stop.
* If the kinetic simulation encounters problems like unfulfilled tolerances the simulation **MUST** stop.
* The flux bounds **MUST** be updated from the kinetic model before the FBA optimization is run.
* The fluxes in the kinetic model **MUST** be set before the kinetic simulation is run.

* For the execution of the kinetic models the comp model is flattend and the flattened model is simulated.

* what is the order of execution of the models ?? & when are the update steps performed ??
* how do we deal with the step sizes and tolerances?


<!------------------------------------------------------------------->
# C) Frequently asked questions (FAQ)
## Are multiple kinetic models supported?
Yes, multiple kinetic submodels can exist in the DFBA. During the kinetic integrations the flattend kinetic model is integrated. However, kinetic submodels **SHOULD** be kept inside the KINETIC submodel. 

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
No, in the first version of the DFBA guidelines and implementation only deterministic kinetic models can be coupled to FBA models. In future versions the coupling of stochastic and/or logical models can be supported.
It is possible to encode SBML models with additional modeling frameworks than FBA or deterministic ODE models. Examples are logical models encoded with the SBML package `qual` or stochastic models, i.e. stochastic ODE models. Such models will be considered in future versions. 

## Are variable step sizes supported?
No, currently only fixed step sizes are supported. The simulation steps must be in agreement with the `dt` parameter for bound updates.
