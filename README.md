# aqua-sdk

SDK to generate data that can be used by the Aqua Predict platform. 

The Aqua Predict application and the Aqua Predict Water Intelligence data hub can work with foreign data, i.e. data that is not controlled by Aqua Predict (servers) but is only available on local servers controlled by third parties.

To work with provided foreign data Aqua Predict provides this toolkit / SDK that computes local aggregates based on the provided data sets directly on the local servers. These computations will employ Differential Privacy enabled algorithms which mathematically guarantees maximum data protection and privacy. The aggregated results of these computations which are completely free of sensitive information can be safely transferred to Aqua Predict systems. There the Aqua Predict Water Intelligence Data & AI system will use these results to re-compute the Aqua Predict Machine Learning models to predict global and local water availability scores and similar predictions.

## Setup

The library is designed to run with Python 3.12. The Python packages required 
can be installed by using the requirement.txt file:

```
pip install -r requirements.txt
```

## Getting started

Examples of use are provided in the notebook:
```
notebook/usage_example.ipynb.
```

