# Params Storage

ParamsStorage is key-value storage to store hyperparameters for machine learning models as a key. The value of a key
can be anything, e.g. cross-validation score of the hyperparameters. All floating-point hyperparameters will store
with given desired precision. This can be useful for pruning optuna params suggestions.

Example:

```python
from params_storage import ParamsStorage

ps = ParamsStorage(precision=3)

ps.add(params=dict(tree_number=128, learning_rate=0.015, c="Bayesian"))
ps.add(params=dict(tree_number=128, learning_rate=0.0154, c="Bayesian"))
ps.add(params=dict(learning_rate=0.1, batch_size=32), value=0.95)

print(ps.size())  # 2
print(ps.exist(dict(tree_number=128, learning_rate=0.015, c="Bayesian")))  # True
print(ps.get(dict(learning_rate=0.1, batch_size=32)))  # 0.95
```