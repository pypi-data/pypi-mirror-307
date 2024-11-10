# DistVAE-Tabular

**DistVAE** is a novel approach to distributional learning in the VAE framework, focusing on accurately capturing the underlying distribution of the observed dataset through a nonparametric CDF estimation. 

We utilize the continuous ranked probability score (CRPS), a strictly proper scoring rule, as the reconstruction loss while preserving the mathematical derivation of the lower bound of the data log-likelihood. Additionally, we introduce a synthetic data generation mechanism that effectively preserves differential privacy.

> For a detailed method explanations, check our paper! [(link)](https://openreview.net/pdf?id=GxL6PrmEUw)

### 1. Installation
Install using pip:
```
pip install distvae-tabular
```

### 2. Usage
```python
from distvae_tabular import distvae
```
```python
distvae.DistVAE # DistVAE model
distvae.generate_data # generate synthetic data
```
- See [example.ipynb](example.ipynb) for detailed example and its results with `loan` dataset.
  - Link for download `loan` dataset: [https://www.kaggle.com/datasets/teertha/personal-loan-modeling](https://www.kaggle.com/datasets/teertha/personal-loan-modeling)

#### Example
```python
"""device setting"""
import torch
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

"""load dataset and specify column types"""
import pandas as pd
data = pd.read_csv('./loan.csv') 
continuous_features = [
    'Age',
    'Experience',
    'Income', 
    'CCAvg',
    'Mortgage',
]
categorical_features = [
    'Family',
    'Personal Loan',
    'Securities Account',
    'CD Account',
    'Online',
    'CreditCard'
]
integer_features = [
    'Age',
    'Experience',
    'Income', 
    'Mortgage'
]

"""DistVAE"""
from distvae_tabular import distvae

distvae = distvae.DistVAE(
    data=data,
    continuous_features=continuous_features,
    categorical_features=categorical_features,
    integer_features=integer_features,
    epochs=5 # for quick checking (default is 1000)
)

"""training"""
distvae.train()

"""generate synthetic data"""
syndata = distvae.generate_data(100)
syndata

"""generate synthetic data with Differential Privacy"""
syndata = distvae.generate_data(100, lambda_=0.1)
syndata
```

### Citation
If you use this code or package, please cite our associated paper:
```
@article{an2024distributional,
  title={Distributional learning of variational AutoEncoder: application to synthetic data generation},
  author={An, Seunghwan and Jeon, Jong-June},
  journal={Advances in Neural Information Processing Systems},
  volume={36},
  year={2024}
}
```