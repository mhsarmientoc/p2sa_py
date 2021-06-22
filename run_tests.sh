#!/bin/bash

#conda env create --name test --file environment.yml
#conda activate test

pytest --junitxml=junit.xml --cov-report xml:coverage.xml --cov-report term --cov-branch --cov

#conda deactivate
#conda remove --yes -n test --all
