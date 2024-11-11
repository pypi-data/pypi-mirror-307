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

## Cite us

If you use ENKIE in a scientific publication, please cite our paper: 

Gollub, M.G., Backes, T., Kaltenbach, H.M., Stelling, J., 2023. "ENKIE: A package for
predicting enzyme kinetic parameter values and their uncertainties". *Bioinformatics*. -
[DOI](https://doi.org/10.1093/bioinformatics/btae652)