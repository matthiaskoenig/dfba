# Dynamic Flux Balance Analysis in SBML
[![DOI](https://www.zenodo.org/badge/71236313.svg)](https://www.zenodo.org/badge/latestdoi/71236313)
[![GitHub version](https://badge.fury.io/gh/matthiaskoenig%2Fdfba.svg)](https://badge.fury.io/gh/matthiaskoenig%2Fdfba)
[![License (LGPL version 3)](https://img.shields.io/badge/license-LGPLv3.0-blue.svg?style=flat-square)](http://opensource.org/licenses/LGPL-3.0)

**Matthias König, Leandro Watanabe, Chris Myers**

This repository provides guidelines and rules for the encoding of dynamic flux balance analysis (DFBA) models in SBML. The latest guidelines and rules are available from this repository at  
[latest guidelines](./guidelines/DFBA_models_in_SBML.md). 

Example models are provided with instructions on how to run the simulations below

This effort builds on existing standards, i.e., [SBML](http://sbml.org), [SED-ML](http://sed-ml.org), and the [COMBINE archive](http://co.mbine.org/documents/archive).

<a href="http://sbml.org" title="SBML"><img src="./docs/images/sbml.png" height="35"/></a>&nbsp;
<a href="http://sed-ml.org" title="SED-ML"><img src="./docs/images/sedml.png" height="35"/></a>&nbsp;
<a href="http://co.mbine.org/documents/archive" title="CombineArchive"><img src="./docs/images/omex.png" height="35"/></a>&nbsp;

##  How to cite
If you use these guidelines and/or the provided examples, or want to reference the information within,  
please cite corresponding manuscript and this repository via its DOI

[![DOI](https://www.zenodo.org/badge/71236313.svg)](https://www.zenodo.org/badge/latestdoi/71236313)

The latest manuscript is available from
[https://www.overleaf.com/6382003zbbpfy#/21488847/](https://www.overleaf.com/6382003zbbpfy#/21488847/).

  
## License
* Source Code: [LGPLv3](http://opensource.org/licenses/LGPL-3.0)
* Documentation: [CC BY-SA 4.0](http://creativecommons.org/licenses/by-sa/4.0/)

## Funding
Matthias König is supported by the Federal Ministry of Education and Research (BMBF, Germany) 
within the research network Systems Medicine of the Liver (LiSyM, grant number 031L0054).

<a href="http://www.lisym.org/" alt="LiSyM" target="_blank"><img src="./docs/images/lisym.png" height="35"></a> &nbsp;&nbsp;
<a href="http://www.bmbf.de/" alt="BMBF" target="_blank"><img src="./docs/images/bmbf.png" height="35"></a> &nbsp;&nbsp;


# Running example models
Model examples encoded in the proposed dynamic FBA scheme. the models are listed in the `/models/*` folders. Example models consist of
* SBML model(s) according to guidelines and rules
* SED-ML file encoding example simulation experiments
* Simulation results for `iBioSim` and `sbmlutils`

The model examples are provided as COMBINE archives for exchange.

As part of this project DFBA implementations based on these guidelines have been implemented. 
The models can be simulated either with [iBioSim](http://www.async.ece.utah.edu/ibiosim) or [sbmlutils](https://github.com/matthiaskoenig/sbmlutils/)
with detailed instructions below.


## sbmlutils
To run the ipython notebooks setup a virtual environment via
```
# clone repository
git clone https://github.com/matthiaskoenig/dfba.git
cd dfba

# setup virtual environment
mkvirtualenv dfba
(dfba) pip install -r requirements.txt

# install kernel for ipython
(dfba) python -m ipykernel install --user --name=dfba

# start jupyter notbook
jupyter notebook

# select notebook for model (dfba/models/*/*.ipynb) and run notbook with the dfba kernel
Kernel -> Change kernel -> dfba
Kernel -> Restart & Run All
```

## iBioSim
The tutorial on running the models in iBioSim is available from
[Tutorial_iBioSim](./docs/Tutorial_iBioSim.pdf)



