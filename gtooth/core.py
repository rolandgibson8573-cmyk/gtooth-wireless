"""Small scalar reference model for proposed wireless link scoring."""

from __future__ import annotations

from dataclasses import dataclass, replace
import math
from typing import Sequence

MASTER_K = 3.912023005428146
GATE_FLOOR = 0.02
DEFAULT_REJECTION_THRESHOLD = 0.383
DEFAULT_WEIGHTS = (0.30, 0.15, 0.15, 0.20, 0.10, 0.10)
SCALAR_NAMES = (
    "link_quality",
    "freshness",
    "stability",
    "path_quality",
    "gateway_contribution",
    "resource_score",
)


def validate_normalized(value: float, name: str = "value") -> float:
    """Return a finite normalized scalar or raise ``ValueError``."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a finite number in [0, 1]")
    try:
        result = float(value)
    except OverflowError as error:
        raise ValueError(f"{name} must be a finite number in [0, 1]") from error
    if not math.isfinite(result) or not 0.0 <= result <= 1.0:
        raise ValueError(f"{name} must be a finite number in [0, 1]")
    return result


def normalize(value: float, minimum: float, maximum: float) -> float:
    """Map a finite value within [minimum, maximum] to [0, 1]."""
    for candidate, name in ((value, "value"), (minimum, "minimum"), (maximum, "maximum")):
        if isinstance(candidate, bool) or not isinstance(candidate, (int, float)):
            raise ValueError(f"{name} must be finite")
        try:
            numeric_candidate = float(candidate)
        except OverflowError as error:
            raise ValueError(f"{name} must be finite") from error
        if not math.isfinite(numeric_candidate):
            raise ValueError(f"{name} must be finite")
    if minimum >= maximum:
        raise ValueError("minimum must be less than maximum")
    if not minimum <= value <= maximum:
        raise ValueError("value must be within [minimum, maximum]")
    return (float(value) - float(minimum)) / (float(maximum) - float(minimum))


@dataclass(frozen=True)
class LinkState:
    """Six normalized wireless link-control inputs."""

    link_quality: float
    freshness: float
    stability: float
    path_quality: float
    gateway_contribution: float
    resource_score: float

    def __post_init__(self) -> None:
        for name in SCALAR_NAMES:
            object.__setattr__(self, name, validate_normalized(getattr(self, name), name))

    def as_tuple(self) -> tuple[float, ...]:
        """Return scalar values in the documented scoring order."""
        return tuple(getattr(self, name) for name in SCALAR_NAMES)


def weighted_composite(
    state: LinkState, weights: Sequence[float] = DEFAULT_WEIGHTS
) -> float:
    """Compute the normalized weighted sum for a six-scalar link state."""
    if not isinstance(state, LinkState):
        raise ValueError("state must be a LinkState")
    if len(weights) != len(SCALAR_NAMES):
        raise ValueError(f"exactly {len(SCALAR_NAMES)} weights are required")
    checked_weights = []
    for weight in weights:
        if isinstance(weight, bool) or not isinstance(weight, (int, float)):
            raise ValueError("weights must be finite, nonnegative numbers")
        try:
            numeric_weight = float(weight)
        except OverflowError as error:
            raise ValueError("weights must be finite, nonnegative numbers") from error
        if not math.isfinite(numeric_weight) or numeric_weight < 0.0:
            raise ValueError("weights must be finite, nonnegative numbers")
        checked_weights.append(numeric_weight)
    weight_total = math.fsum(checked_weights)
    if not math.isclose(weight_total, 1.0, rel_tol=0.0, abs_tol=1e-12):
        raise ValueError("weights must sum to 1")
    normalized_weights = (weight / weight_total for weight in checked_weights)
    composite = math.fsum(
        value * weight for value, weight in zip(state.as_tuple(), normalized_weights)
    )
    return min(1.0, max(0.0, composite))


def governed_score(value: float) -> float:
    """Apply the governed K-gate to a normalized scalar."""
    normalized = validate_normalized(value)
    return math.exp(-MASTER_K * (1.0 - normalized))


def inverse_governed_score(score: float) -> float:
    """Invert the locked-K gate for a score in [0.02, 1]."""
    if isinstance(score, bool) or not isinstance(score, (int, float)):
        raise ValueError("score must be a finite number in [0.02, 1]")
    try:
        score = float(score)
    except OverflowError as error:
        raise ValueError("score must be a finite number in [0.02, 1]") from error
    if not math.isfinite(score) or not GATE_FLOOR <= score <= 1.0:
        raise ValueError("score must be a finite number in [0.02, 1]")
    return 1.0 + math.log(score) / MASTER_K


def is_acceptable(score: float, threshold: float = DEFAULT_REJECTION_THRESHOLD) -> bool:
    """Return whether a governed score meets a configurable rejection threshold."""
    if isinstance(score, bool) or not isinstance(score, (int, float)):
        raise ValueError("score must be a finite number in [0.02, 1]")
    try:
        numeric_score = float(score)
    except OverflowError as error:
        raise ValueError("score must be a finite number in [0.02, 1]") from error
    if not math.isfinite(numeric_score) or not GATE_FLOOR <= numeric_score <= 1.0:
        raise ValueError("score must be a finite number in [0.02, 1]")
    numeric_threshold = validate_normalized(threshold, "threshold")
    if numeric_threshold < GATE_FLOOR:
        raise ValueError("threshold must be in [0.02, 1]")
    return numeric_score >= numeric_threshold


def iterate_gate(value: float, iterations: int) -> float:
    """Apply the scalar gate repeatedly; this is a mathematical iteration only."""
    result = validate_normalized(value)
    if isinstance(iterations, bool) or not isinstance(iterations, int) or iterations < 0:
        raise ValueError("iterations must be a nonnegative integer")
    for _ in range(iterations):
        result = governed_score(result)
    return result


def decay_freshness(freshness: float, age_seconds: float, half_life_seconds: float) -> float:
    """Apply exponential half-life decay to a normalized freshness value."""
    normalized = validate_normalized(freshness, "freshness")
    for candidate, name in ((age_seconds, "age_seconds"), (half_life_seconds, "half_life_seconds")):
        if isinstance(candidate, bool) or not isinstance(candidate, (int, float)):
            raise ValueError(f"{name} must be finite")
        try:
            numeric_candidate = float(candidate)
        except OverflowError as error:
            raise ValueError(f"{name} must be finite") from error
        if not math.isfinite(numeric_candidate):
            raise ValueError(f"{name} must be finite")
    if age_seconds < 0.0:
        raise ValueError("age_seconds must be nonnegative")
    if half_life_seconds <= 0.0:
        raise ValueError("half_life_seconds must be positive")
    return normalized * math.exp(-math.log(2.0) * age_seconds / half_life_seconds)


def route_score(
    state: LinkState,
    weights: Sequence[float] = DEFAULT_WEIGHTS,
    *,
    age_seconds: float = 0.0,
    freshness_half_life_seconds: float | None = None,
) -> float:
    """Score a link, optionally decaying freshness from its measured age."""
    if freshness_half_life_seconds is not None:
        state = replace(
            state,
            freshness=decay_freshness(
                state.freshness, age_seconds, freshness_half_life_seconds
            ),
        )
    elif age_seconds != 0.0:
        raise ValueError("freshness_half_life_seconds is required when age_seconds is nonzero")
    return governed_score(weighted_composite(state, weights))
