#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: ESDC team
@contact: esdc_proba2_tech@sciops.esa.int
European Space Astronomy Centre (ESAC)
European Space Agency (ESA)
Created on 5 Aug. 2019
"""
import os
import shutil
from os.path import isfile, join
from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install

import re
import ast
import sys
import fileinput

folder = "esa_p2sa"
packages = []
for dirname, dirnames, filenames in os.walk(folder):
    if '__init__.py' in filenames:
        packages.append(dirname.replace('/', '.'))
# Filter test packages
toFilter = []
for package in packages:
    if 'test' in package:
        toFilter.append(package)
for filter in toFilter:
    packages.remove(filter)

############################
# Parse the profile argument
############################
profile = 'dev'  # default value
for argument in sys.argv[1:]:
    print(argument)
    if argument.startswith('-P'):
        profile = argument[2:]
        sys.argv.remove(argument)
print('Profile:', profile)


def copyFolder(src, dest):
    directory = os.path.dirname(dest)
    if not os.path.exists(directory):
        os.makedirs(directory)
    src_files = os.listdir(src)
    for file_name in src_files:
        full_file_name = os.path.join(src, file_name)
        if os.path.isfile(full_file_name):
            print('Copying %s into %s ... ' % (full_file_name, dest))
            shutil.copy(full_file_name, dest)

def loadReplaceDictionary():
    propsfile = 'conf/%s.properties' % profile
    print('Loading %s ... ' % propsfile)
    return reading(propsfile)


def reading(propsfile):
    props = {}
    with open(propsfile, 'r') as f:
        for line in f:
            line = re.sub('\s+', '', line)  # remove whitespace and '\n' chars
            if "=" not in line:
                continue  # skips blanks and comments w/o =
            if line.startswith("#"):
                continue  # skips comments which contain =
            k, v = line.split("=", 1)
            props[k] = v
    return props

def replacePython(file):
    print('Processing file:', file)
    replaced = []
    replaceDictionary = loadReplaceDictionary()
    REGEX = re.compile(r'[=]\s*\S*$', re.IGNORECASE)
    # Variable substitution in python code
    for line in fileinput.input(file, inplace=True):
        l = re.sub('\s+', '', line)  # Remove all the spaces from the line
        for key in replaceDictionary:
            pattern = '%s=' % key
            if l.startswith(pattern):
                line = REGEX.sub('= "%s"' % replaceDictionary[key], line)
                replaced.append(line.strip())
        print(line, end='')
    for line in replaced:
        print('Replaced:', line)

def replaceNotebooks(file):
    print('Processing file:', file)
    replaceDictionary = loadReplaceDictionary()
    for line in fileinput.input(file, inplace=True):
        for key in replaceDictionary:
            value = "'%s'" % replaceDictionary[key]
            line = line.replace(key, value)
        print(line, end='')


# https://stackoverflow.com/questions/20288711/post-install-script-with-python-setuptools


class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        print("*********** POST INSTALL COMMAND ***************")
        # Copy demos into the build folder
        copyFolder('demo/', 'build/demo/')
        # Variable substitution
        # Python code
        FILES2UPDATE = [ 'build/lib/esa_p2sa/__init__.py' ]
        for file in FILES2UPDATE:
            replacePython(file)
        # Notebook demos
        folder = './build/demo/'
        FILES2UPDATE = [join(folder, filename) for filename in os.listdir(folder) if os.path.splitext(filename)[1] == '.ipynb' ]
        for file in FILES2UPDATE:
            replaceNotebooks(file)
        print("*********** POST INSTALL COMMAND END ***********")
        install.run(self)


setup(name='esa_p2sa',
      version='1.1',
      description='First version of p2sa_core to access the data stored in PROBA2 archive',
      url='https://repos.cosmos.esa.int/socci/scm/esdc_ptwosa/p2sa-python.git',
      author='ESDC',
      author_email='esdc_proba2_tech@sciops.esa.int',
      license='ESDC',
      packages=packages,
      zip_safe=False,
      install_requires=['astroquery', 'astropy', 'pytest', 'IPython', 'requests', 'six', 'python-dateutil'],
      cmdclass={
          'install': PostInstallCommand,
      })
