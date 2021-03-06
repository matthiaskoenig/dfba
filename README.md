# Dynamic Flux Balance Analysis in SBML
[![DOI](https://www.zenodo.org/badge/71236313.svg)](https://www.zenodo.org/badge/latestdoi/71236313)
[![GitHub version](https://badge.fury.io/gh/matthiaskoenig%2Fdfba.svg)](https://badge.fury.io/gh/matthiaskoenig%2Fdfba)
[![License (LGPL version 3)](https://img.shields.io/badge/license-LGPLv3.0-blue.svg?style=flat-square)](http://opensource.org/licenses/LGPL-3.0)

<b><a href="https://orcid.org/0000-0003-1725-179X" title="orcid id"><img src="./docs/images/logos/orcid.png" height="15"/></a> Matthias König,
 Leandro Watanabe, Chris Myers
</b>

This repository provides guidelines and rules for the encoding of dynamic flux balance analysis (DFBA) models in SBML. The latest guidelines and rules are available from this repository at [latest schema](./schema/DFBA_models_in_SBML.md). 

As part of this project DFBA implementations based on these guidelines have been implemented in 
[iBioSim](http://www.async.ece.utah.edu/ibiosim) and [sbmlutils](https://github.com/matthiaskoenig/sbmlutils/).
 

<a href="http://www.async.ece.utah.edu/ibiosim" title="iBioSim" target="_blank"><img src="./docs/images/logos/ibiosim.png" height="35"/></a>&nbsp;
<a href="https://github.com/matthiaskoenig/sbmlutils/" title="sbmlutils" target="_blank"><img src="./docs/images/logos/sbmlutils.jpg" height="35"/></a>&nbsp;

This repository contains the following content
* [`./docs/`](./docs/): documentation, presentation, tutorial
* [`./schema/`](./schema/): guidelines for encoding DFBA in SBML
* [`./models/`](./models/): examples models with simulation results, cytoscape visualizations, jupyter notebooks
* [`./README.md`](./README.md): this document

Detailed instructions on how to run the example models are provided [below](#running-example-models).

## Standardization
This effort builds on existing standards, i.e., [SBML](http://sbml.org), [SED-ML](http://sed-ml.org), and the [COMBINE archive](http://co.mbine.org/documents/archive).

<a href="http://sbml.org" title="SBML" target="_blank"><img src="./docs/images/logos/sbml.png" height="35"/></a>&nbsp;
<a href="http://sed-ml.org" title="SED-ML" target="_blank"><img src="./docs/images/logos/sedml.png" height="35"/></a>&nbsp;
<a href="http://co.mbine.org/documents/archive" title="CombineArchive" target="_blank"><img src="./docs/images/logos/omex.png" height="35"/></a>&nbsp;

##  How to cite
If you use these schema and guidelines and/or the provided examples, or want to reference the information within,  
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

<a href="http://www.lisym.org/" alt="LiSyM" target="_blank"><img src="./docs/images/logos/lisym.png" height="35"></a> &nbsp;&nbsp;
<a href="http://www.bmbf.de/" alt="BMBF" target="_blank"><img src="./docs/images/logos/bmbf.png" height="35"></a> &nbsp;&nbsp;

The development of iBioSim is supported by the National Science Foundation under Grants CCF-1218095 and CCF-1748200. Any opinions, findings, and conclusions or recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of the National Science Foundation.

<a href="http://www.lisym.org/" alt="NSF" target="_blank"><img src="./docs/images/logos/nsf.jpg" height="50"></a> 

# Example models
Model examples encoded in the proposed dynamic FBA scheme in the [`./models/`](./models/) folder. 
Example models contain
* SBML model(s) according to guidelines and rules
* SED-ML file encoding example simulation experiments
* Simulation results for [iBioSim](http://www.async.ece.utah.edu/ibiosim) and [sbmlutils](https://github.com/matthiaskoenig/sbmlutils/)
* Jupyter notebooks
* Cytoscape visualization

The model examples are provided as COMBINE archives for exchange.


## sbmlutils 
<a href="https://github.com/matthiaskoenig/sbmlutils/" title="sbmlutils"><img src="./docs/images/logos/sbmlutils.jpg" height="35"/></a> 

Example jupyter notebooks reproducing the results are available for the individual DFBA models. 
Installation instructions and the entry point is available at [`./models/index.ipynb`](./models/index.ipynb)

* [`./models/toy_wholecell/toy_wholecell.ipynb`](./models/toy_wholecell/toy_wholecell.ipynb)
* [`./models/toy_atp/toy_atp.ipynb`](./models/toy_atp/toy_atp.ipynb)
* [`./models/diauxic_growth/diauxic_growth.ipynb`](./models/diauxic_growth/diauxic_growth.ipynb)
* [`./models/ecoli/ecoli.ipynb`](./models/ecoli/ecoli.ipynb)

## iBioSim
<a href="http://www.async.ece.utah.edu/ibiosim" title="iBioSim"><img src="./docs/images/logos/ibiosim.png" height="35"/></a>

To use iBioSim, you can follow the instructions available [here](./models/iBioSim_Tutorial.md).

## Tool reproducibility
The numerical identity of the results was checked with results available in the
following notebook  
[`./models/compare.ipynb`](./models/compare.ipynb)
