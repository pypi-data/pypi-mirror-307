import typing as tp

TParams = tp.Dict[str, tp.Union[str, int, float]]


class ParamsStorage:
    """
    ParamsStorage is key-value storage to store hyperparameters for machine learning models as a key. The value of a key
    can be anything, e.g. cross-validation score of the hyperparameters. All floating-point hyperparameters will store
    with given desired precision. This can be useful for pruning optuna params suggestions.

    Example:
        ps = ParamsStorage(precision=2)

        ps.add(dict(a=1, b=3.141, c="Bayesian"))
        ps.add(dict(a=1, b=3.142, c="Bayesian"))

        print(ps.size())  # 1
    """

    def __init__(self, precision: int):
        self.precision = precision
        self._memory: tp.Dict[tuple, tp.Optional[tp.Any]] = dict()

    @staticmethod
    def _round_dict(params: TParams, digits: int) -> TParams:
        rounded_dict: TParams = dict()
        for k, v in params.items():
            if isinstance(v, float):
                rounded_dict[k] = round(v, digits)
            else:
                rounded_dict[k] = v
        return rounded_dict

    def _get_key(self, params: TParams) -> tuple:
        key = sorted(list(zip(self._round_dict(params, self.precision).items())))
        return tuple(key)

    def add(self, params: TParams, value: tp.Optional[tp.Any] = None):
        key = self._get_key(params)
        if key not in self._memory:
            self._memory[key] = value

    def get(self, params: TParams) -> tp.Any:
        key = self._get_key(params)
        return self._memory[key]

    def exist(self, params: TParams) -> bool:
        key = self._get_key(params)
        return key in self._memory

    def size(self) -> int:
        return len(self._memory)
