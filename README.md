# aqua-sdk

SDK to generate data that can be used by the aqua-predict platform. 

## Setup

The library is designed to run with Python 3. The Python packages required 
can be installed by using the requirement.txt file:

```bash
pip install -r requirements.txt
```

## Getting started

Examples of use are provided in the notebook: notebook/usage_example.ipynb.
In order to generate differentially-private aggregate statistics, it is 
recommended to provide bounds for the data values. A warning is thrown if the
bounds are not specified. The parameter epsilon in [0.0, 1.0] controls the 
privacy level.
