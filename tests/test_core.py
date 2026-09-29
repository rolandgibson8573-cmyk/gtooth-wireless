import math

import pytest

from gtooth.core import (
    DEFAULT_WEIGHTS,
    GATE_FLOOR,
    MASTER_K,
    LinkState,
    decay_freshness,
    governed_score,
    inverse_governed_score,
    is_acceptable,
    iterate_gate,
    normalize,
    route_score,
    weighted_composite,
)


def test_master_gate_bounds_and_exact_scalar_round_trip() -> None:
    assert MASTER_K == pytest.approx(-math.log(0.02))
    assert governed_score(0.0) == pytest.approx(GATE_FLOOR)
    assert governed_score(1.0) == 1.0
    for value in (0.0, 0.02, 0.25, 0.5, 0.999, 1.0):
        assert inverse_governed_score(governed_score(value)) == pytest.approx(value)


def test_weighted_composite_and_optional_freshness_decay() -> None:
    state = LinkState(1, 1, 1, 1, 1, 1)
    assert weighted_composite(state) == pytest.approx(1.0)
    assert weighted_composite(state, (0.3, 0.15, 0.15, 0.2, 0.1, 0.1000000000005)) == 1.0
    assert decay_freshness(0.8, 10, 10) == pytest.approx(0.4)
    fresh_score = route_score(state)
    aged_score = route_score(state, age_seconds=10, freshness_half_life_seconds=10)
    assert aged_score < fresh_score
    assert sum(DEFAULT_WEIGHTS) == pytest.approx(1.0)


def test_fixed_point_iteration_is_scalar_and_converges_from_interior() -> None:
    estimate = iterate_gate(0.5, 40)
    assert estimate == pytest.approx(0.0218, abs=0.0001)
    assert iterate_gate(1.0, 20) == 1.0
    assert iterate_gate(0.5, 0) == 0.5


@pytest.mark.parametrize("value", [-0.1, 1.1, math.nan, math.inf, -math.inf, True])
def test_link_state_rejects_invalid_normalized_values(value: float) -> None:
    with pytest.raises(ValueError):
        LinkState(value, 0.5, 0.5, 0.5, 0.5, 0.5)


def test_link_state_rejects_integer_overflow_as_invalid() -> None:
    with pytest.raises(ValueError):
        LinkState(10**10000, 0.5, 0.5, 0.5, 0.5, 0.5)


def test_inputs_and_weights_are_validated() -> None:
    assert normalize(5, 0, 10) == pytest.approx(0.5)
    with pytest.raises(ValueError):
        normalize(11, 0, 10)
    with pytest.raises(ValueError):
        governed_score(math.nan)
    with pytest.raises(ValueError):
        inverse_governed_score(0.019)
    assert is_acceptable(0.383)
    assert not is_acceptable(0.382, threshold=0.383)
    with pytest.raises(ValueError):
        is_acceptable(0.5, threshold=0.01)
    with pytest.raises(ValueError):
        weighted_composite(LinkState(0.5, 0.5, 0.5, 0.5, 0.5, 0.5), (1, 1, 1, 1, 1, 1))
    with pytest.raises(ValueError):
        decay_freshness(0.5, -1, 5)
