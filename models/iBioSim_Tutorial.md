To run DFBA models in iBioSim tool, you need to:
* Download [iBioSim 3.0](https://github.com/MyersResearchGroup/iBioSim/releases)
* Install from [source](https://github.com/MyersResearchGroup/iBioSim/)
* Open up the tool as instructed [here](https://github.com/MyersResearchGroup/iBioSim/).
* Create a project by clicking on File->New->Project and specify the location and name of the project.

To create DFBA models, you need to follow these steps:
* Create a model by clicking on File->New->Model and the name of the model.
* Create a model for each required module as described in the [guidelines](../docs/manuscript/supplement/S1_DFBA_models_in_SBML.pdf)
* Specify the SBO term of each module by clicking on the Model button in the toolbar.
* Once all the submodels have been created, you click on Tools->Analysis Tool and specify a name for the analysis. You can leave it empty for a default value.
* In the analysis view, select Monte Carlo as the Analysis Type and select Mixed-Hierarchical as the simulator.
* Click on the run button in the toolbar.
* Navigate to the TSD Graph to view the simulation results.

To run DFBA models from COMBINE Archives, you need to follow these steps:
* Once a project is created, you can import our examples.
* Click on File->Import->Archive and selecting the appropriate omex file.
