# Diauxic Growth Model
Model of diauxic growth in E.coli.

The model is based on the publication

Biophys J. 2002 Sep;83(3):1331-40.  
Dynamic flux balance analysis of diauxic growth in Escherichia coli.  
Mahadevan R1, Edwards JS, Doyle FJ 3rd.  
https://www.ncbi.nlm.nih.gov/pubmed/12202358  

and simulates the diauxic growth on glucose and acetate as substrates.

# Model feedback

Feedback to the model created with iBioSim.

The first step of validation is to check that your models don't have any validation errors.

## General
* the relative change in upper bounds is handled incorrectly (maximal allowed change, 
provides new upper and lower bounds)
* update of concentrations not correct ? (should be done by reactions via their respective fluxes)

## growth_fba
* fbc strict attribute missing
* don't write array information in the SBML, i.e. remove `arrays:required="true"`. 
Especially because no array information is in the model.
* reaction v2 has wrong upper bound: "max_v4" -> max_v2 (which is currently not used)
* value for max_v2 is wrong, should be 0.3 !

```
file: growth_fba.xml
read time (ms): 0.016786
validation error(s): 4

line 2: (99107 [Error]) Every SBML Level 3 package is identified uniquely by an XML namespace URI and defines the attribute named 'required'. A value of required=true indicates that interpreting the package is necessary for complete mathematical interpretation of the model. (L3V1 Section 4.1.2) This instance of libSBML version 5 cannot find the code necessary to interpret the package information.
 Package 'arrays' is a required package and the model cannot be properly interpreted.

line 3: (fbc-20209 [Error]) A <model> object must have the required attributes 'strict'. No other attributes from the Flux Balance Constraints namespace are permitted on a <model> object. 
Reference: L3V1 Fbc V2 Section 3.3
 Fbc attribute 'strict' is missing from <Model> object.

line 1: (comp-90106 [Warning]) Due to the need to instantiate models, modelDefinitions, submodels etc. for the purposes of validation it is problematic to reliably report line numbers when performing validation on models using the Hierarchical Model Composition package.

line 1: (comp-90107 [Warning]) The CompFlatteningConverter has encountered a required package for which libSBML does not recognize the information.
 The CompFlatteningConverter has the 'abortIfUnflattenable' option set to 'requiredOnly'  and thus flattening will not be attempted.
```

## growth_update
* same things like growth_fba (i.e. add fbc strict, remove array info, rename species)
* errors in model, because the fbc parameters are not part of the model
```

file: growth_update.xml
read time (ms): 0.018547
validation error(s): 12

line 2: (99107 [Error]) Every SBML Level 3 package is identified uniquely by an XML namespace URI and defines the attribute named 'required'. A value of required=true indicates that interpreting the package is necessary for complete mathematical interpretation of the model. (L3V1 Section 4.1.2) This instance of libSBML version 5 cannot find the code necessary to interpret the package information.
 Package 'arrays' is a required package and the model cannot be properly interpreted.

line 3: (fbc-20209 [Error]) A <model> object must have the required attributes 'strict'. No other attributes from the Flux Balance Constraints namespace are permitted on a <model> object. 
Reference: L3V1 Fbc V2 Section 3.3
 Fbc attribute 'strict' is missing from <Model> object.

line 1: (comp-90106 [Warning]) Due to the need to instantiate models, modelDefinitions, submodels etc. for the purposes of validation it is problematic to reliably report line numbers when performing validation on models using the Hierarchical Model Composition package.

line 1: (comp-90107 [Warning]) The CompFlatteningConverter has encountered a required package for which libSBML does not recognize the information.
 The CompFlatteningConverter has the 'abortIfUnflattenable' option set to 'requiredOnly'  and thus flattening will not be attempted.

line 480: (fbc-20705 [Error]) The attribute 'fbc:lowerFluxBound' of a <Reaction> must point to an existing <Parameter> in the model. 
Reference: L3V1 Fbc V2 Section 3.8
 <Reaction> 'v1' refers to lowerBound with id 'v1_min' that does not exist within the <model>.

line 480: (fbc-20706 [Error]) The attribute 'fbc:upperFluxBound' of a <Reaction> must point to an existing <Parameter> in the model. 
Reference: L3V1 Fbc V2 Section 3.8
 <Reaction> 'v1' refers to upperBound with id 'v1_max' that does not exist within the <model>.

line 524: (fbc-20705 [Error]) The attribute 'fbc:lowerFluxBound' of a <Reaction> must point to an existing <Parameter> in the model. 
Reference: L3V1 Fbc V2 Section 3.8
 <Reaction> 'v3' refers to lowerBound with id 'v3_min' that does not exist within the <model>.

line 524: (fbc-20706 [Error]) The attribute 'fbc:upperFluxBound' of a <Reaction> must point to an existing <Parameter> in the model. 
Reference: L3V1 Fbc V2 Section 3.8
 <Reaction> 'v3' refers to upperBound with id 'v3_max' that does not exist within the <model>.

line 543: (fbc-20705 [Error]) The attribute 'fbc:lowerFluxBound' of a <Reaction> must point to an existing <Parameter> in the model. 
Reference: L3V1 Fbc V2 Section 3.8
 <Reaction> 'v4' refers to lowerBound with id 'v4_min' that does not exist within the <model>.

line 543: (fbc-20706 [Error]) The attribute 'fbc:upperFluxBound' of a <Reaction> must point to an existing <Parameter> in the model. 
Reference: L3V1 Fbc V2 Section 3.8
 <Reaction> 'v4' refers to upperBound with id 'v4_max' that does not exist within the <model>.

line 561: (fbc-20705 [Error]) The attribute 'fbc:lowerFluxBound' of a <Reaction> must point to an existing <Parameter> in the model. 
Reference: L3V1 Fbc V2 Section 3.8
 <Reaction> 'v2' refers to lowerBound with id 'v2_min' that does not exist within the <model>.

line 561: (fbc-20706 [Error]) The attribute 'fbc:upperFluxBound' of a <Reaction> must point to an existing <Parameter> in the model. 
Reference: L3V1 Fbc V2 Section 3.8
 <Reaction> 'v2' refers to upperBound with id 'v2_max' that does not exist within the <model>.
```

## growth_top
* same things like above, i.e. fbc strict, remove array info, rename species, missing flux bound parameters.
* in addition you have some layout error on a text glyph
```
line 1967: (10103 [Error]) An SBML XML document must conform to the XML Schema for the corresponding SBML Level, Version and Release. The XML Schema for SBML defines the basic SBML object structure, the data types used by those objects, and the order in which the objects may appear in an SBML document.
 Attribute '' on an <TextGlyph> must not be an empty string.
```
* and missing ids in layout
```
line 1123: (layout-21111 [Error]) The value of the 'layout:glyph' attribute of a <referenceGlyph> must be of the 'id' of an existing <graphicalObject> (or derived) element in the <layout>.
Reference: L3V1 Layout V1 Section 3.11.1
 The <referenceGlyph> with the id 'Glyph__rateOfV1__product__R0' has a glyph 'Glyph__R0' which is not the id of any <graphicalObject> in the model.

line 1141: (layout-21111 [Error]) The value of the 'layout:glyph' attribute of a <referenceGlyph> must be of the 'id' of an existing <graphicalObject> (or derived) element in the <layout>.
Reference: L3V1 Layout V1 Section 3.11.1
 The <referenceGlyph> with the id 'Glyph__rateOfV2__product__R0' has a glyph 'Glyph__R0' which is not the id of any <graphicalObject> in the model.

line 1159: (layout-21111 [Error]) The value of the 'layout:glyph' attribute of a <referenceGlyph> must be of the 'id' of an existing <graphicalObject> (or derived) element in the <layout>.
Reference: L3V1 Layout V1 Section 3.11.1
 The <referenceGlyph> with the id 'Glyph__rateOfV3__product__R0' has a glyph 'Glyph__R0' which is not the id of any <graphicalObject> in the model.

line 1177: (layout-21111 [Error]) The value of the 'layout:glyph' attribute of a <referenceGlyph> must be of the 'id' of an existing <graphicalObject> (or derived) element in the <layout>.
Reference: L3V1 Layout V1 Section 3.11.1
 The <referenceGlyph> with the id 'Glyph__rateOfV4__product__R0' has a glyph 'Glyph__R0' which is not the id of any <graphicalObject> in the model.
```
* rest of warnings/errors related to point one of the list
```
file: growth_top.xml
read time (ms): 0.163716
validation error(s): 18

line 2: (99107 [Error]) Every SBML Level 3 package is identified uniquely by an XML namespace URI and defines the attribute named 'required'. A value of required=true indicates that interpreting the package is necessary for complete mathematical interpretation of the model. (L3V1 Section 4.1.2) This instance of libSBML version 5 cannot find the code necessary to interpret the package information.
 Package 'arrays' is a required package and the model cannot be properly interpreted.

line 4: (fbc-20209 [Error]) A <model> object must have the required attributes 'strict'. No other attributes from the Flux Balance Constraints namespace are permitted on a <model> object. 
Reference: L3V1 Fbc V2 Section 3.3
 Fbc attribute 'strict' is missing from <Model> object.

line 500: (fbc-20209 [Error]) A <model> object must have the required attributes 'strict'. No other attributes from the Flux Balance Constraints namespace are permitted on a <model> object. 
Reference: L3V1 Fbc V2 Section 3.3
 Fbc attribute 'strict' is missing from <Model> object.

line 1079: (fbc-20209 [Error]) A <model> object must have the required attributes 'strict'. No other attributes from the Flux Balance Constraints namespace are permitted on a <model> object. 
Reference: L3V1 Fbc V2 Section 3.3
 Fbc attribute 'strict' is missing from <Model> object.

line 1967: (10103 [Error]) An SBML XML document must conform to the XML Schema for the corresponding SBML Level, Version and Release. The XML Schema for SBML defines the basic SBML object structure, the data types used by those objects, and the order in which the objects may appear in an SBML document.
 Attribute '' on an <TextGlyph> must not be an empty string.

line 1: (comp-90106 [Warning]) Due to the need to instantiate models, modelDefinitions, submodels etc. for the purposes of validation it is problematic to reliably report line numbers when performing validation on models using the Hierarchical Model Composition package.

line 977: (fbc-20705 [Error]) The attribute 'fbc:lowerFluxBound' of a <Reaction> must point to an existing <Parameter> in the model. 
Reference: L3V1 Fbc V2 Section 3.8
 <Reaction> 'v1' refers to lowerBound with id 'v1_min' that does not exist within the <model>.

line 977: (fbc-20706 [Error]) The attribute 'fbc:upperFluxBound' of a <Reaction> must point to an existing <Parameter> in the model. 
Reference: L3V1 Fbc V2 Section 3.8
 <Reaction> 'v1' refers to upperBound with id 'v1_max' that does not exist within the <model>.

line 1021: (fbc-20705 [Error]) The attribute 'fbc:lowerFluxBound' of a <Reaction> must point to an existing <Parameter> in the model. 
Reference: L3V1 Fbc V2 Section 3.8
 <Reaction> 'v3' refers to lowerBound with id 'v3_min' that does not exist within the <model>.

line 1021: (fbc-20706 [Error]) The attribute 'fbc:upperFluxBound' of a <Reaction> must point to an existing <Parameter> in the model. 
Reference: L3V1 Fbc V2 Section 3.8
 <Reaction> 'v3' refers to upperBound with id 'v3_max' that does not exist within the <model>.

line 1040: (fbc-20705 [Error]) The attribute 'fbc:lowerFluxBound' of a <Reaction> must point to an existing <Parameter> in the model. 
Reference: L3V1 Fbc V2 Section 3.8
 <Reaction> 'v4' refers to lowerBound with id 'v4_min' that does not exist within the <model>.

line 1040: (fbc-20706 [Error]) The attribute 'fbc:upperFluxBound' of a <Reaction> must point to an existing <Parameter> in the model. 
Reference: L3V1 Fbc V2 Section 3.8
 <Reaction> 'v4' refers to upperBound with id 'v4_max' that does not exist within the <model>.

line 1058: (fbc-20705 [Error]) The attribute 'fbc:lowerFluxBound' of a <Reaction> must point to an existing <Parameter> in the model. 
Reference: L3V1 Fbc V2 Section 3.8
 <Reaction> 'v2' refers to lowerBound with id 'v2_min' that does not exist within the <model>.

line 1058: (fbc-20706 [Error]) The attribute 'fbc:upperFluxBound' of a <Reaction> must point to an existing <Parameter> in the model. 
Reference: L3V1 Fbc V2 Section 3.8
 <Reaction> 'v2' refers to upperBound with id 'v2_max' that does not exist within the <model>.
```

## General
* The top model contains the complete `growth_update` and `growth_fba` models within its `<comp:listOfModelDefinitions>` (??).
 In addition these files are provided as separate SBML files. The Top model should only link the FBA and update model, not
 define them, i.e. use ExternalModelDefinitions.
 
* The handling via the events in the `top` model is extremely ugly. This must be handled differently (for instance by calculating
what is the upper bound in the FBA depending on the availability of substrates)

* what are p2, ..., p7 and why annotated with SBO:0000593 : petri net place ??? (does not make sense)