"""Deterministic synthetic link examples; not a wireless channel simulator."""

from __future__ import annotations

from dataclasses import dataclass

from .core import LinkState, governed_score, weighted_composite


@dataclass(frozen=True)
class CandidateResult:
    """Synthetic candidate scores for one named route."""

    name: str
    state: LinkState
    baseline_score: float
    gtooth_score: float


def simulate_candidates() -> tuple[CandidateResult, ...]:
    """Return a fixed set of illustrative wireless link states."""
    candidates = (
        ("direct", LinkState(0.78, 0.88, 0.74, 0.72, 0.35, 0.82)),
        ("relay", LinkState(0.70, 0.93, 0.87, 0.91, 0.80, 0.66)),
        ("congested", LinkState(0.91, 0.42, 0.48, 0.39, 0.25, 0.54)),
    )
    return tuple(
        CandidateResult(name, state, weighted_composite(state), governed_score(weighted_composite(state)))
        for name, state in candidates
    )


def select_route(results: tuple[CandidateResult, ...], score_kind: str = "gtooth") -> str:
    """Choose the highest-scoring candidate using a named illustrative score."""
    if not results:
        raise ValueError("at least one candidate is required")
    if score_kind not in {"baseline", "gtooth"}:
        raise ValueError("score_kind must be 'baseline' or 'gtooth'")
    score_attribute = "baseline_score" if score_kind == "baseline" else "gtooth_score"
    return max(results, key=lambda result: getattr(result, score_attribute)).name
