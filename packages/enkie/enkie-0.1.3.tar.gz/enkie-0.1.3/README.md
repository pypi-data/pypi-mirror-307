# ENKIE - The ENzyme KInetics Estimator
[![Documentation Status](https://readthedocs.org/projects/enkie/badge/?version=latest)](https://enkie.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/enkie.svg)](https://badge.fury.io/py/enkie)

ENKIE is a python package for the prediction of kinetic parameter values and
uncertainties in metabolic networks. The package uses Bayesian Multilevel Models to
predict values and uncertainties from reaction, protein and metabolite identifiers. The
predictions are then combined with standard free energy estimates to ensure
thermodynamic consistency.

## Installation
ENKIE is available as a Python package on the [Python Package
Index](https://pypi.org/project/enkie/), see the
[documentation](https://enkie.readthedocs.io/en/latest/getting_started.html)
for the installation instructions.

## Repository structure
This repository is structured as follows:
- `benchmarks`: R scripts and Jupyter notebooks for comparing ENKIE's performance to
  previous methods. 
- `docs`: Input files for the [readthedocs
  documentation](https://enkie.readthedocs.io/en/latest/getting_started.html).
- `enkie`: Source code of the ENKIE python package.
- `examples`: Examples for using ENKIE from the command line and for accessing the API.
- `tests`: Unit tests for the ENKIE python package.
- `training`: Python scripts for constructing the training datasets from SABIO-RK and
  BRENDA, and R Scripts for training the models.

## Training the models (optional).
ENKIE comes with pre-trained models, which are available on
[Zenodo](https://doi.org/10.5281/zenodo.7664120) and are automatically downloaded during
the first usage. If you want to reproduce the training process or train your own models, you can:
1. Retrieve the BRENDA and SABIO-RK data using the scripts in `training/data/brenda/` and
   `training/data/sabio-rk/`.
2. Merge, annotate and clean up the data using the scripts in `training/data/`.
3. Train the models using the `training/train_models.R` script.

## Cite us

If you use ENKIE in a scientific publication, please cite our paper: 

Gollub, M.G., Backes, T., Kaltenbach, H.M., Stelling, J., 2024. "ENKIE: A package for
predicting enzyme kinetic parameter values and their uncertainties". *Bioinformatics*. -
[DOI](https://doi.org/10.1093/bioinformatics/btae652)
