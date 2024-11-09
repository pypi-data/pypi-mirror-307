########
InsarViz
########

InsarViz is a project dedicated to the visualisation of InSar data. 

The ts_viz app is designed to visualize and interactively analyze time-series (datacubes) from InSAR data processing chains.

The full documentation is available here: 

https://deformvis.gricad-pages.univ-grenoble-alpes.fr/insarviz



Installation
************

If you would like to be able to **modify the code** or use a beta version, follow instead the **Developer installation** below.

Set up the environment
--------------------------

We recommend you to install the InsarViz tool in a *virtual environment* (an independent package installation, so that the package versions required by InsarViz do not mess up with your own installation).

* **With Anaconda**

If you have installed the `Anaconda distribution <https://docs.anaconda.com/anaconda/install/>`_ (for example Miniconda). If you are using Windows, open an *Anaconda Powershell Prompt*. Create a conda environment (InsarViz requires Python >= 3.9):

.. code-block :: bash

 conda create -n insarviz-env python=3.9

And then *activate* it:

.. code-block :: bash

 conda activate insarviz-env

* **Without Anaconda**

Without Anaconda, create a Python virtual environment (InsarViz requires Python >= 3.9):

.. code-block :: bash

 python3 -m venv path_to_venv

And then *activate* it:

.. code-block :: bash

 source path_to_venv/bin/activate

Install
-------

Installing InsarViz in a virtual environment (activate it first), or system-wide, is just a one-line command:

.. code-block :: bash

 pip install insarviz

If you already installed InsarViz before and only want to update it, run this command instead: 
.. code-block :: bash

 pip install insarviz -U

Check your installation
-----------------------

You can check your installation by doing (first activate the virtual environment if you used one):

.. code-block :: bash

 ts_viz --help

This should print the help message. If not, your install failed.

Run InsarViz
----------------

Simply run InsarViz from the following command line (first activate the virtual environment if you used one):

.. code-block :: bash

 ts_viz 

You can provide directly the path of a file to open (an Insar datacube or an InsarViz project) using the *-i* option:

.. code-block :: bash

 ts_viz -i path_to_file

Debug
*****
If the install prompts an error, try updating pip:

.. code-block :: bash

 python3 -m pip install --upgrade pip

If you get errors mentioning rasterio, try:

.. code-block :: bash

 python3
 >> import rasterio

If this fails with an error mentioning that rasterio cannot find libgdal.so.XX, you 
should try changing the version of GDAL you are using. InsarViz has rasterio 
(https://rasterio.readthedocs.io) as dependency. Rasterio depends upon the GDAL library 
(https://gdal.org) and assumes gdal is already installed. We recommend using version 
1.3.10 of rasterio which is compatible with GDAL >= 3.1 (on Linux, use the command 
gdalinfo --version to figure out which version of gdal you have).

Developer installation 
***********************

Follow this section instead of the **Installation** section if you would like to be able to **modify the code** or use a beta version.

Download source code
--------------------

Download the source code using git (first navigate to the destination folder):

* *Without a gitlab account*:

.. code-block :: bash

 git clone https://gricad-gitlab.univ-grenoble-alpes.fr/deformvis/insarviz

* *With a gitlab account (ssh)*:

.. code-block :: bash

 git clone git@gricad-gitlab.univ-grenoble-alpes.fr:deformvis/insarviz.git

Note that you can specify a branch using the option *-b*, for example the *beta* branch:
.. code-block :: bash

 git clone https://gricad-gitlab.univ-grenoble-alpes.fr/deformvis/insarviz -b beta

Use pdm to install
------------------

We recommend using pdm (https://pdm-project.org/) to manage the dependencies and install InsarViz for developers.
We provide lockfiles for Python versions 3.9 and 3.12, so you will create a virtual environment using one of those Python versions.
First navigate inside the root of the cloned folder, then:

* *With Anaconda*

.. code-block :: bash
 
 conda create -n insarviz-env-3-9 python=3.9.19
 conda activate insarviz-env-3-9
 pip install pdm
 pdm use -f "$(conda info --base)/envs/insarviz-env-3-9"
 pdm install --lockfile insarviz-py39.lock --frozen-lockfile

or

.. code-block :: bash
 
 conda create -n insarviz-env-3-12 python=3.12.3
 conda activate insarviz-env-3-12
 pip install pdm
 pdm use -f "$(conda info --base)/envs/insarviz-env-3-12"
 pdm install --lockfile insarviz-py312.lock --frozen-lockfile

* *Without Anaconda*

.. code-block :: bash
 
 python3 -m venv path_to_pdm_venv
 source path_to_pdm_venv/bin/activate
 pip install pdm
 pdm venv create 3.9.19 -n venv_3_9 
 pdm install --lockfile=insarviz-py39.lock --venv==venv_3_9 --frozen-lockfile

or

.. code-block :: bash
 
 python3 -m venv path_to_pdm_venv
 source path_to_pdm_venv/bin/activate
 pip install pdm
 pdm venv create 3.12.3 -n venv_31_2 
 pdm install --lockfile=insarviz-py312.lock --venv==venv_3_12 --frozen-lockfile

Run InsarViz
----------------

* *With Anaconda*

Simply activate the installation environment then:
.. code-block :: bash
 
 ts_viz

* *Without Anaconda*

To run InsarViz you will need the following command line (inside the pdm_venv):
.. code-block :: bash
 
 pdm run ts_viz

Update InsarViz after modifying the code
------------------------------------------

To ensure that your code changes are taken into account, run again the pdm install command line.

How to cite
***********
If you use InsarViz for your project, please consider citing `this paper <https://doi.org/10.21105/joss.06440>`_

How to cite
-----------
If you use InsarViz for your project, please consider citing `this paper <https://doi.org/10.21105/joss.06440>`_

Contact
*******
If you need help or have ideas for further developments, you can contact:
insarviz-sos@univ-grenoble-alpes.fr

