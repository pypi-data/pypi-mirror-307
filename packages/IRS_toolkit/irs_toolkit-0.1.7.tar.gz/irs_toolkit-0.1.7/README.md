# IRS Toolkit

[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![Linting - Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Code style - Black](https://img.shields.io/badge/Code%20Style-Black-000000.svg)](https://github.com/psf/black)

### Installation

This library is published in the PyPI directory. To install, users can run pip install 'IRS_toolkit' command.

The IRS Toolkit is a Python-based project designed to provide a comprehensive solution for valuing interest rate swaps and bonds. This toolkit aims to assist Risk team in the monitoring of the Qonto's investements.

## Features

- **Interest Rate Swap Valuation:** The toolkit facilitates the valuation of interest rate swaps, allowing users to input various parameters and swap terms.
The toolkit then calculates the present value of future cash flows and estimates the fair value of the swap. [IR SWAP](/Test_Swap.ipynb).

- **Basket Swap Valuation:** The toolkit facilitates the valuation of Basket swaps, allowing the user to give the informations required.
The toolkit then calculates Mark to Market of the Basket swap.

- **Bond Valuation:** With the bond valuation module, users can evaluate the current value of bonds based on different inputs .
The toolkit employs interpolation techniques to generate yield curves from provided data or market rates, enabling accurate valuation.[BONDS](/Tuto_Bonds.ipynb)

## Getting started

You will need `poetry`. Here's the easiest way to install it:

1. Install [pipx](https://pypa.github.io/pipx/#install-pipx)
2. Install [poetry with pipx](https://python-poetry.org/docs/#installing-with-pipx)

Then you can do the following command to install the dependencies:

```bash
poetry install
```

Once everything is installed, you will have to spawn a shell inside the virtual environment of your project with:

```bash
poetry shell
```

After that, you will be able to launch the streamlit using the command:

```bash
streamlit run Swap_Pricing_interface.py
```

or for QLF Reco interface

```bash
streamlit run QLF_Reconciliation_interface.py
```

```bash
streamlit run QTF_Rec.py
```

## Best practices

Before each push, run the following command, in order to fix formatting and linting issues:

```bash
make -i lint-fix
```

## Dependencies management

Based on [Poetry](https://python-poetry.org/docs/cli/).

## Basic GitHub Commands

To clone the IRS toolkit project:
```bash
git clone git@gitlab.qonto.co:risk/financial-toolkit.git
```

To change branch:
```bash
git checkout <Branch-Name>
```

To create your branch:
```bash
git checkout -b <New-Branch-Name>
```

To get latest branch data:
```bash
git pull
```

To add all your file to the git:
```bash
git add .
```

To commit your change to the git:
```bash
git commit -m "commit description"
```

To push your change to the git:
```bash
git push
```

## Quick Overview

- 📁 notebook_analysis

        Contains all the jupyter notebook for ad-hoc analysis, including the data_for_dashboard.ipynb notebook allowing to populate the snowflake table

- 📁 connector

        Contains the python file to communicate with Snowflake SQL, Refinitiv API (still requires Refinitiv to be open) and AWS SFTP S3 to get the inventory files.
        Also contains python script that get data from refinitiv, it uses the Refinitiv_connection.py file from 📁 connector, note that refinit workspace needs to be open to get the data.

- 📁 script

        Folder that contains all the backend with all the functions being called by the GUI and the notebook

- 📁 streamlit

        Folder containing the streamkit GUI, use "streamlit run filename.py" to run the streamlit app

- 📁 output

        Folder containing all the output generated, some output are used as input by some python file, notably the hard_inout folder which contains the IRS characteristics of each split and schedule and the Composition of each basket swap. Please note that .xlsx file are exluding in the .gitignore so the file wont be uploaded to gitlab.

- 📁 airflow_dags

        Basic structure for maybe upcoming automation of data insertion with airflow

        

- 📁 documentation

        folder containing .mdj which contains uml graph of the databse and of the project can be opened with the free software StarUML

#