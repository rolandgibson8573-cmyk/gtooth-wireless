"""Experimental, wireless-only G-Tooth link-control reference package."""

from .core import (
    DEFAULT_WEIGHTS,
    DEFAULT_REJECTION_THRESHOLD,
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

__all__ = [
    "DEFAULT_WEIGHTS",
    "DEFAULT_REJECTION_THRESHOLD",
    "MASTER_K",
    "LinkState",
    "decay_freshness",
    "governed_score",
    "inverse_governed_score",
    "is_acceptable",
    "iterate_gate",
    "normalize",
    "route_score",
    "weighted_composite",
]
