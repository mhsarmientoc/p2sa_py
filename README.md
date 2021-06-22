# pyP2SAExample

Welcome to the P2SA Jupyter notebook widget page. 

# Requirements

`Jupyter` and `node.js`

`Jupyter` comes together with anaconda. Anaconda can be downloaded from here:

- Anaconda (Python 3.7 Version): https://www.anaconda.com/distribution/

For `node.js`:
If you use conda, you can get it with:

```bash
conda install -c conda-forge nodejs
```

If you use Homebrew on Mac OS X:
```bash
brew install node
```
You can also download `Node.js` from the Node.js website https://nodejs.org/ and install it directly.

# Installation

For a development installation (requires npm),

Once that everything it is installed, open a console and install the following Python packages (If they haven't been installed already:

Astroquery:

```bash
pip install astroquery
```
   For some methods is necessary to have the last version available of TapPlus. This library 'TapPlus' is provided as part of the package "Astroquery".
   In order to upgrade 'Astroquery' to the latest version, please execute the following command:

``` bash
conda install -c astropy astroquery
```

Pytest:

```bash
pip install pytest
pip install pytest-cov
```
Ipywidgets:

```bash
pip install ipywidgets
```
IPython: (Jupyter Notebook library that provides access to widgets like 'Image' to display images or 'Video' to play videos in the Notebook as for the example the SWAP Carrington Movies.

```bash
pip install ipython
````

# Running Tests

```bash
./run_tests.sh
````


## Installing P2SA python wrapper

We can install the P2SA wrapper in two ways. The first one is the most simple and requires no permissions. The second one requires access to our internal git repository

### Downloading the package from the P2SA web page

- **Optional** - If there is already a previous version installed in the system, execute this command to uninstall it:

```
pip uninstall esa_p2sa
```

- Download the python wheel package from [here](http://p2sa.esac.esa.int/p2sa-py/esa_p2sa-1.1-py3-none-any.whl) or generate it as described below.
- Install the package in your system:

```
pip install esa_p2sa-1.1-py3-none-any.whl
```

### Clonning the project from the git repository

- Go to the root folder of the project download from Bitbucket

```
git clone https://repos.cosmos.esa.int/socci/scm/esdc_ptwosa/p2sa-python.git
```
- Run the following command to install the environment for the wrapper in python 

```bash
python setup.py install
```

# How to execute the Jupyter Notebook in local

In order to run this Jupyter Notebook in your local environment, please do the following steps:


- Run Jupyter Notebooks

```bash
jupyter-notebook
```
It is also possible to launch Jupyter Notebooks directly from the Anaconda UI. 

Once Jupyter Notebook is running, a new tab will be opened in your browser showing the contents of the current directory.
Navigate inside the "demo" directory and select "pyP2SA.ipynb" where '.ipynb' is the extension for the Jupyter Notebooks. 


# pyP2SA in Jupyter lab

In order to be able to run pyP2SA in Jupyter lab it is necessary to install the labextension ivywidgets by the following command:

```bash
$ jupyter labextension install @jupyter-widgets/jupyterlab-manager
```

NOTE that this requires `node.js` to be installed. 

# Creating a wheel package

Referenced links:  

- https://docs.python.org/3/distributing/index.html  
- https://packaging.python.org/tutorials/packaging-projects/#packaging-your-project  
- https://stackoverflow.com/questions/21222114/how-do-i-install-python-libraries-in-wheel-format  
- https://stackoverflow.com/questions/36014334/how-to-install-python-packages-from-the-tar-gz-file-without-using-pip-install  

Create a setup.py file:

```
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: ESDC team
@contact: esdc_proba2_tech@sciops.esa.int
European Space Astronomy Centre (ESAC)
European Space Agency (ESA)
Created on 23 Aug. 2019
"""
import os
from setuptools import setup

name = "esa_p2sa"
packages = []
for dirname, dirnames, filenames in os.walk(name):
    if '__init__.py' in filenames:
        packages.append(dirname.replace('/', '.'))

setup(name='esa_p2sa',
      version='0.1',
      description='First version of p2sa_core.py to access the data stored in P2SA archive',
      url='',
      author='ESDC team',
      author_email='esdc_proba2_tech@sciops.esa.int',
      license='ESDC',
      packages=packages,
      zip_safe=False,
      install_requires=['astroquery', 'astropy', 'pytest', 'IPython'])
```

Once the setup.py is in the project, creating a package is as simple as run a python script:

```bash
$ python3 setup.py bdist bdist_wheel [-Pprofile]
```

**Note**: Latest parameter does not actually belong to the setuptools package and was added to the script to determine the target environment. Code was included to parse this parameter and configure the package according the property files included in the 'conf' folder. Possible values for the profile are: _dev_, _beta_ and _oper_. Once processed, the parameter is removed from the sys.argv to avoid problems with the setuptools.

The command should output a lot of text and once completed should generate two files in the dist directory:

```
dist/
  esa_p2sa-1.0.2-py3-none-any.whl
  esa_p2sa-1.0.2.macosx-10.7-x86_64.tar.gz
```

The tar.gz file is a source archive whereas the .whl file is a built distribution. Newer pip versions preferentially install built distributions, but will fall back to source archives if needed. You should always upload a source archive and provide built archives for the platforms your project is compatible with. In this case, our example package is compatible with Python on any platform so only one built distribution is needed.
