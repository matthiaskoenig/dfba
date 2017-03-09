# DFBA models in SBML
**version: 0.1-draft**
<!--
Please edit this file ONLY on hackmd.io for now and commit the file when finished with editing to the dfba git via Menu -> Download -> Markdown. Than we have the latest version available on github. Comments in this text via the comment syntax.
-->
<!-- Discuss this during the next Harmony meeting -->
* **[latest editable version](https://hackmd.io/IYUwDATAjAZgxiAtAZmFAJogLAdi8xUdJZMZAIyhDjnJzHSA?both)**
* **[github repository](https://github.com/matthiaskoenig/dfba)**

This document describes the rules and guidelines for encoding Dynamic Flux Balance Analysis (DFBA) models in the Systems Biology Markup Language ([SBML](http://sbml.org/Main_Page)), a free and open interchange format for computer models of biological processes.

Note that the guidelines have been proposed by [iBioSim](http://www.async.ece.utah.edu/ibiosim) or [sbmlutils](https://github.com/matthiaskoenig/sbmlutils/) as ground rules to simulate DFBA models in these tools. It is by no means a community agreement. However, we highly encourage everyone who wants to encode DFBA models and tool developers to follow these rules.

The document is structured in
* **Section A**: describes how to encode DFBA models in SBML.
* **Section B**: provides information on how simulators should execute models provided in the format of Section A). DFBA Implementation are provided by [iBioSim](http://www.async.ece.utah.edu/ibiosim) or [sbmlutils](https://github.com/matthiaskoenig/sbmlutils/).
* **Section C**: provides answers to frequently asked questions.

The following conventions are used throughout this document.
* Required rules are stated via **MUST**, i.e. DFBA models in SBML must implement these rules.
* Guidelines which are recommended to be followed are indicated by **SHOULD**, i.e. it is good practice to follow these guidelines, but they are not required for an executable DFBA model in SBML. [iBioSim](http://www.async.ece.utah.edu/ibiosim) and [sbmlutils](https://github.com/matthiaskoenig/sbmlutils/) will run the DFBA even if these recommendations are not followed.
* Additional information for clarification is provided by **CAN**, i.e. it is clarified that this is allowed.
* Curly brackets function as place holders. For instance the reaction id `{rid}` means that `{rid}` is replaced with the actual id of the reaction.

Example models implementing the rules and guidelines of this document are provided in the `dfba/models` folder of the [github repository](https://github.com/matthiaskoenig/dfba).

The following abbreviations are used in this document
* DFBA : Dynamic Flux Balance Analysis
* FBA : Flux Balance Analysis
* SBML : Systems Biology Markup Language


<!------------------------------------------------------------------->
# A) Encoding DFBA models in SBML
This section describes how DFBA models can be encoded in SBML. Two main links are hereby required between the FBA model and the kinetic models: 
* Update of flux bounds in the FBA model from the kinetic model. 
* Update of reaction fluxes in the kinetic model from the FBA solution.

The DFBA models consists of different components performing parts of the DFBA task:
* `TOP` : DFBA comp model that includes all submodels and their corresponding connections
* `KINETIC` : kinetic part of the DFBA model
* `FBA` : FBA part of the DFBA model
* `BOUNDS` : calculation of the upper and lower bounds for the `FBA` model
* `UPDATE` : calculation of the updated `KINETIC` part from the `FBA` solution

 **`TODO:`** Create figure showing linking between submodels (this section is unclear, figure will help. Show the different alternatives)

## DFBA model
* The DFBA SBML model **MUST** be a single SBML `comp` model.
* The DFBA submodels **MUST** be encoded in the DFBA model via `comp:SubModels`. 
* The DFBA submodels **CAN** be encoded via `comp:ModelDefinition` or `comp:ExternalModelDefinition`, with each submodel being defined in a separate file.
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
Units are especially helpful when connecting `FBA` and kinetic model in DFBA models, because they can ensure that the updates of `Species` via `FBA` fluxes have compatible units.
* All models **SHOULD** contain units. The units of the submodel **SHOULD** be identical and be replaced by the top model.
  
## FBA submodel
* The `Model` element of the `FBA` submodel **MUST** have the SBOTerm [`SBO:0000624` (flux balance framework)](http://www.ebi.ac.uk/sbo/main/SBO:0000624).

* The `FBA` models **MUST** be encoded using the SBML package `fbc-v2` with `strict=true`.
<!-- 
Matthias: change to strict=true
-->

<!--
* The fba submodel **MUST** be optimizable without any additional information as a stand-alone model, i.e. the model **MUST** be importable in a FBA simulator like cobrapy and result in an optimal solution when optimized.

Matthias: This is not really a model encoding rule, it makes the differce between an encoded and simulatable model, i.e. a model which produces useable results.
-->

* The `reactions` in the FBA model **MUST NOT** have any `KineticLaw`.
<!--
Leandro: The FBA model **MUST** consist only of `parameters`, `species`, `compartments`, and `reactions` are allowed. Reactions should not have kinetic law.
Matthias: I think this is too restrictive. We should allow valid FBA models encoded in fbc-v2.
I added the no KineticLaw as rule above.
-->

### Objective function
* The FBA model **MUST** contain at least one objective function.
* The optimization objective for the DFBA model **MUST** be the active objective in the fba model, i.e. an active objective **MUST** exist and be the objective which is executed in every step of the DFBA.
* The objective **CAN** be `maximize` or `minimize`.

### Exchange reaction
* Unbalanced species in the FBA **MUST** be encoded by creating an exchange reaction for the respective species. The unbalanced species correspond to species in the kinetic model which are changed via the FBA solution fluxes.
<!--
Leandro: This is not how I have done the FBA models but it seems it works in our tool. Would need to change my model and verify.
Matthias: This would be great because it simplifies many things for me. Also we could easily use FBA models which are encoded in this way, like the BiGG models. 
-->
* The exchange `Reactions` **MUST** have the `Species` which is changed by the reaction (unbalanced `Species` in FBA) as substrate with stoichiometry `1.0` and have no products, i.e. have the form `1.0 {sid} ->` with `{sid}` being the `Species` id.
* The exchange `Reactions` **SHOULD** have the SBOterm [`SBO:0000627` (exchange reaction)](http://www.ebi.ac.uk/sbo/main/SBO:0000627).
* The exchange `Reactions` **SHOULD** be named `EX_{sid}`, i.e. consist of the prefix `EX_` and the `Species` id `{sid}`.
<!--
Matthias: !! directionality changed to be in agreement with SBO, cobra(py) and BiGG models. Also naming adapted. This allows to directly use BiGG models for DFBA simulations. See for instance
http://bigg.ucsd.edu/models/e_coli_core/reactions/EX_ac_e

--@Leandro: Tricky when we use reversible reaction in the FBA model and want to do DFBA with stochastic simulation. 
Matthias: no stochastic simulations for now, but we have to plan for this.
-->
### BoundaryCondition
* The FBA model **MUST NOT** have `species` with `boundaryCondition=True`. Such models can easily be converted in supported `FBA` models by setting `boundaryCondition=False` and adding a exchange `Reaction` for the corresponding `Species`.
 
### Reaction flux bounds
<!-- REMOVE
* SBML `Parameters` for upper and lower bounds **MUST** exist for all reactions and have numerical values, i.e. no `InitialAssignments` or `AssignmentRules` for flux bound parameter are allowed.
Matthias: This is covered by fbc strict=true
-->
* All exchange reactions **MUST** have individual `Parameters` for the upper and lower bound which are not used by other reactions. 

<!-- REMOVE
* The following upper and lower bound default values **MUST** be set in fba models: If no flux bounds are specified the default upper flux bound is `1000`, and the default lower flux bound is `-1000` for reversible and `0` for irreversible reactions. 

Matthias: we should agree that we use -1000, 1000 for all unspecified upper and lower bounds when we encode the models for us. All reactions have flux bounds due to fbc strict=true.
-->

* The `Parameters` for the upper and lower bounds of reactions **SHOULD** have the ids `ub_{rid}` and `lb_{rid}` with `{rid}` being the respective reaction id.
* The `Parameters` describing the flux bounds **SHOULD** have the SBOTerm [`SBO:0000625` (flux bound)](http://www.ebi.ac.uk/sbo/main/SBO:0000625). 


### Ports
* All exchange reactions **MUST** have a port.
* All upper and lower bounds of exchange reactions **MUST** have a port.

## TOP model
* The `TOP` model **MUST** have the SBOTerm [`SBO:0000293` (non-spatial continuous framework)](http://www.ebi.ac.uk/sbo/main/SBO:0000293) on the `Model` element.
* The `TOP` model **MUST** have exactly one submodel with the SBOTerm [`SBO:0000624` (flux balance framework)](http://www.ebi.ac.uk/sbo/main/SBO:0000624) on the `Model` element, i.e. multiple `fbc` submodels are currently not supported.

### dt
* The `TOP` DFBA model **MUST** contain a parameter `dt` which defines the step size of the FBA optimizations, i.e. after which time interval the FBA is performed. 
* The `dt` parameter **MUST** be annotated with the SBOTerm [`SBO:0000346` (temporal measure)](http://www.ebi.ac.uk/sbo/main/SBO:0000346).
<!--
Matthias: what is the correct SBOTerm for dt. I used the temporal measurement for now.
-->

### Dummy reactions
* The top model **MUST** include a dummy species with `id="dummy_S"`. The dummy species are required for the definition of the dummy reactions in SBML L3V1.
<!--
Matthias: We should think about moving to L3V2, where there is no more
requirement for the dummy species. This would simplify and clarify things, i.e. remove the dummy species rules.
I have to check if roadrunner is supporting this, if yes we can go to L3V2.
Also no real SBOTerm fitting for dummy species or reaction. Using empty set for now.
Leandro: can have separate guidelines for L3V1 and L3V2
-->
* For every exchange reaction in the `FBA` submodel, there **MUST** exist a dummy reaction in the `TOP`. Each dummy reaction **MUST** include the dummy species `dummy_S` as product with stochiometry `1.0`. No other reactants, products or modifiers are allowed on the dummy reactions `(-> dummy_S)`. 
* The id of the dummy reaction **SHOULD** be `id="dummy_{rid}"` for the respective exchange reaction with `id="{rid}"` in the `FBA` submodel.
* The dummy species **SHOULD** have the SBOTerm [`SBO:0000291` (empty set)](http://www.ebi.ac.uk/sbo/main/SBO:0000291). 
* The dummy reactions **SHOULD** have the SBOTerm [`SBO:0000631` (pseudoreaction)](http://www.ebi.ac.uk/sbo/main/SBO:0000631).

###  Flux parameters & Flux AssignmentRules
* For every dummy `Reaction` in the `TOP` model with id a corresponding flux `Parameter` **MUST** exist in the `TOP` model which is `constant=true`.
* For every dummy `Reaction` and corresponding flux `Parameter` in the top model an `AssignmentRule` in the `TOP` model **MUST** exist of form `{rid} = {dummy_rid}`.
* The flux parameter **SHOULD** have the id with `{rid}` for dummy reactions `{dummy_rid}`.
* The flux `Parameters` **SHOULD** have the SBOTerm [`SBO:0000612` (rate of reaction)](http://www.ebi.ac.uk/sbo/main/SBO:0000612).
* The flux `AssignmentRules` **SHOULD** have the SBOTerm [`SBO:0000391` (steady state expression)](http://www.ebi.ac.uk/sbo/main/SBO:0000391).
<!-- What SBOTerm? -->

### ReplacedBy
For every dummy reaction in the `TOP` model with `id="dummy_{rid}"` must be replaced via a `comp:ReplacedBy` with the corresponding exchange reaction with `id={rid}` from the `FBA` submodel. The `comp:ReplacedBy` uses the `portRef` of the exchange reaction `{rid}_port`.
These replacements update the ODE fluxes in the `TOP` model by replacing the dummy `Reactions` by the `FBA` reactions.


### Replacements
The following replacements are part of the model:
`TODO:` what are the replacements exactely, list all of them
- For every parameter that is used to as a flux bound for a reaction in the FBA submodel, there **MUST** be a replacing reaction from the `TOP`.
- For every species that affect any bound calculation, there **MUST** be a replacing species from the `TOP`.
- For every species that appear in both the `UPDATE` and `KINETIC` submodels, there **MUST** be a species on the `TOP` model that replaces the corresponding species in each submodel.

<!-- 
Try to do all replacements in the top model.
-->

## BOUNDS submodel
The `BOUNDS` submodel calculates the upper and lower bounds for the `FBA` model. For this calculation the `Species` changed via exchange `Reactions` in the FBA and the time step `dt` are required. The `BOUNDS` model can be part of the `TOP` model or a separate submodel (in this case some of the rules are obsolete)

The parameter `dt` is used in calculating the upper and lower bounds based on the availability of the species in the exchange `Reactions`. This ensures that the FBA solution cannot take more than the available species amounts in the timestep of duration `dt` and is consistent for the timestep with the available resources.

* The `BOUNDS` model **MUST** have the SBOTerm [`SBO:0000293` (non-spatial continuous framework)](http://www.ebi.ac.uk/sbo/main/SBO:0000293) on the `Model` element.
* The `BOUNDS` model **MUST** contain the parameter `dt` which defines the step size of the FBA optimizations. The `dt` `Parameter` **MUST** be linked via a port to the `TOP` model `dt`. The `dt` parameter **MUST** be annotated with the SBOTerm [`SBO:0000346` (temporal measure)](http://www.ebi.ac.uk/sbo/main/SBO:0000346).  
* The `BOUNDS` model **MUST** contain all `Species` which are used in `FBA` exchange `Reactions`.
* The `BOUNDS` model **MUST** contain `Parameters` for all upper and lower flux bounds of exchange `Reactions`.
* The `BOUNDS` model **MUST** contain `FunctionDefinitions` for `min` and `max` of the form  
`min=lambda( x,y, piecewise(x,lt(x,y),y) )`  
and  
`max=lambda( x,y, piecewise(x,gt(x,y),y) )`.

* The `BOUNDS` model **MUST** contain `AssignmentRules` for the update of all upper and lower bounds of the exchange reactions of the form
`lb_EX_{sid}=max(lb_default, -{sid}*{cid}/dt)`  
and  
`ub_EX_{sid}=min(ub_default, {sid}*{cid}/dt)`
with `{cid}` being the compartment of the species `{sid}`. This ensures that in the time step `dt` not more than the available amounts of the species are used in the `FBA` solution.
<!--
Matthias: The bound must be the most restrictive bound via min/max function. Probably good to use L3V2 where there exist min and max functions for the calculation.
-->
* The `BOUNDS` model **MUST** contain the necessary parameter and assignment rules for the update of additional upper and lower bounds of reactions in the FBA which are not exchange reactions. E.g. if there is a time dependent change in an upper bound of an FBA reaction this belongs in the `BOUNDS` model.
### ReplacedElements
* The `TOP` model **MUST** contain parameters with `ReplacedElements` for all upper and lower bounds which are changed via the `BOUNDS` submodel. Every parameter in the `TOP` model contains hereby a `ReplacedElement` for the respective parameter from the `BOUNDS` model and `FBA` model.


## UPDATE submodel
The `UPDATE` model can be part of the `TOP` model or a separate submodel. The update submodel performs the update of the species which are changed by the FBA, i.e. the species which have exchange reactions.
* The `UPDATE` model **MUST** have the SBOTerm [`SBO:0000293` (non-spatial continuous framework)](http://www.ebi.ac.uk/sbo/main/SBO:0000293) on the `Model` element.
* For every `FBA` exchange reaction with id `{rid}` the `UPDATE` model **MUST** contain a parameter with id `{pid}={rid}` to store the flux from the FBA solution.

* For every `FBA` exchange `Reaction` the `UPDATE` model **MUST** contain an update `reaction` with identical reaction equation than the corresponding exchange reaction, i.e. `S ->`.

* The `UPDATE` model **MUST** contain all `Species` which are used in `FBA` exchange `Reactions`.
* The species in the `UPDATE` submodel **SHOULD** be named identical to the species in the `FBA` submodel.
* The update `Reactions` **SHOULD** have ids of the form `update_{sid}` with `{sid}` being the id of the `Species` which is updated.
* The update reaction **MUST** have a `KineticLaw` of the form 
$$update_S = v_S\cdot\frac{S}{Km + S}$$
for the `Species` S being updated. The Michaelis Menten Term assures that the update of the `Species` by the `FBA` flux does not result in negative concentrations. 

* The update reactions **SHOULD** have the SBOTerm [`SBO:0000631` (pseudoreaction)](http://www.ebi.ac.uk/sbo/main/SBO:0000631).
<!--
Matthias: The flux units must fit to the species. This is currently a problem in the diauxic growth because things are always normalized with X. I must update the model structure that fluxes and species are compatible, but still have the normalization. Not sure how to handle this best.
-->
### ReplacedElements
- The `UPDATE` submodel **MUST** have `Species` with `ReplacedElements` that appear in the `FBA` submodel.

<!------------------------------------------------------------------->
# B) Model Simulation
In this section we describe how models in the DFBA SBML formalism described in section A should be simulated by software. The described simulation and update strategy was implemented in two DFBA simulators: `iBioSim` and `sbmlutils`.

## Static Optimization Approach (SOA)
The DFBA models are solved via a **Static Optimization Approach (SOA)**. The total simulation time is divided into time intervals of length `dt` with the instantaneous optimization (FBA) solved at the beginning of every time interval. The dynamic equations are than integrated over the time interval assuming that the fluxes are constant over the interval. 
Before every optimization of the FBA part optimization constraints have to be updated from the dynamic part, after every optimization the dynamic variables corresponding to the FBA fluxes have to be updated.

## Simulation Algorithm
The simulation algorithm starts off by computing the reaction fluxes in the FBA submodel. The reaction fluxes updates the reaction values in the TOP model, which are used to compute the reaction rates in the UPDATE submodel. Once the reaction fluxes are computed by FBA, all NON-FBA submodels are updated concurrently.

```
time = 0
# necessary to calculate the initial flux bounds
calculate_bounds()
## Leandro: calculate_initial_conditions instead?
while (time <= tend){
    # FBA
    set_bounds_fba()
    v_optimal = optimize_fba()
    
    # ODE
    update_fluxes_ode(v_optimal)
    integrate_ode(start=time, end=time+dt, steps=1)
    
    # Next time step
    time = time + dt
}
```
* The output time points **MUST** be in agreement with the `dt` parameter, i.e. the interval between subsequent time points **MUST** be `dt`. This does not affect the internal steps of the kinetic solver.
* The model simulation **MUST** abort if the FBA LP probelm is infeasible.
* If the kinetic simulation encounters problems like unfulfilled tolerances the simulation **MUST** stop.
* The flux bounds **MUST** be updated from the kinetic model before the FBA optimization is run.
* The fluxes in the kinetic model **MUST** be set before the kinetic simulation is run.

* For the execution of the kinetic models the comp model is flattend and the flattened model is simulated.

## Tolerances
For the DFBA simulation absolute tolerances `absTol` and `relTol` are defined. These tolerances are used for the kinetic integration. 
In addition `absTol` is used in the update of the bounds. If the updated bounds are smaller than the absolute tolerance the bounds are set to zero (this avoids infeasible LP problems due to very small negative upper bounds or positive lower bounds). 
```
if abs(bound_updated)<= absTol:
    bound_updated = 0
```

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

## What SBML constructs are supported by the simulators?
Currently, in `iBioSim` and `sbmlutils` all SBML core constructs are supported in the kinetic models with the exception of `Delay` and `AlgebraicRule`.

## I am a tool developer and have different ideas about DFBA encoding in SBML. How can I contribute?
You can make suggestions on the [Github Issue Tracker](https://github.com/matthiaskoenig/dfba/issues). Note this does not guarantee that your suggestions will be adopted. However, we welcome good ideas that would improve our proposed data model idea.
