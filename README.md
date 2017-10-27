# Dynamic Flux Balance Analysis in SBML
<a href="http://sbml.org" title="SBML"><img src="./docs/images/sbml.png" height="35"/></a>&nbsp;
<a href="http://sed-ml.org" title="SED-ML"><img src="./docs/images/sedml.png" height="35"/></a>&nbsp;
<a href="http://co.mbine.org/documents/archive" title="CombineArchive"><img src="./docs/images/omex.png" height="35"/></a>&nbsp;


Model examples encoded in the proposed dynamic FBA scheme. the models are listed in the `/models/*` folders. Every model provides
* SBML model
* SED-ML file 
* Results for `iBioSim` and `sbmlutils`
* Combine archive for the exchange

The models can be simulated either with [iBioSim](http://www.async.ece.utah.edu/ibiosim) or [sbmlutils](https://github.com/matthiaskoenig/sbmlutils/).

## Manuscript
https://www.overleaf.com/6382003zbbpfy#/21488847/

## DFBA SBML Encoding Guidelines
[DFBA models in SBML](./guidelines/DFBA_models_in_SBML.md)

## Setup
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


