# Params Storage

ParamsStorage is key-value storage to store hyperparameters for machine learning models as a key. The value of a key
can be anything, e.g. cross-validation score of the hyperparameters. All floating-point hyperparameters will store
with given desired precision. This can be useful for pruning optuna params suggestions.

Example:

```python
from params_storage import ParamsStorage

ps = ParamsStorage(precision=2)

ps.add(dict(a=1, b=3.141, c="Bayesian"))
ps.add(dict(a=1, b=3.142, c="Bayesian"))

print(ps.size())  # 1
```