# Guideline for encoding DFBA models in SBML
In this document the guidelines for encoding DFBA models in SBML are described.
The example models in `models` follow this guidelines.

## Validity
* All SBML models **MUST** be valid SBML.
* All SBML models **MUST** be encoded in SBML L3V1 or higher.
* ALL SBML models **SHOULD** only use released SBML packages.



## SBO terms

### Modeling Framework
* The FBA submodel **MUST** have the following SBOTerm on the model element  
[SBO:0000624 flux balance framework](http://www.ebi.ac.uk/sbo/main/SBO:0000624)  
```<id="growth_fba" sboTerm="SBO:0000624" ... >```


## Ports
