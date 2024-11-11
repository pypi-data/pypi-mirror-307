import typing as tp

import pytest

from params_storage import ParamsStorage


@pytest.mark.parametrize("case", [
    dict(
        params=dict(a=1, b=1.23, c="Bayesian"),
        digits=1,
        expected=dict(a=1, b=1.2, c="Bayesian"),
    ),
])
def test_round_dict(case: tp.Dict) -> None:
    assert ParamsStorage._round_dict(case["params"], case["digits"]) == case["expected"]


@pytest.mark.parametrize("case", [
    dict(
        params=[
            dict(a=1, b=3.1415, c="Bayesian"),
            dict(b=3.1417, a=1, c="Bayesian"),
            dict(a=1, b=6.7123, c="Bayesian"),
            dict(a=2, b=6.7123, c="Bayesian"),
            dict(a=2, b=6.7125, c="Bayesian"),
        ],
        count=[1, 1, 2, 3, 3]
    ),
])
def test_params_storage(case: tp.Dict) -> None:
    ps = ParamsStorage(precision=2)
    for params, count in zip(case["params"], case["count"]):
        ps.add(params)
        assert count == ps.size()
        assert ps.exist(params)
