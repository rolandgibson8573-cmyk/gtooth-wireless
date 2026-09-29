from gtooth.simulator import select_route, simulate_candidates


def test_synthetic_simulation_is_deterministic_and_selects_a_candidate() -> None:
    first = simulate_candidates()
    second = simulate_candidates()
    assert first == second
    assert len(first) == 3
    assert select_route(first, "baseline") in {result.name for result in first}
    assert select_route(first, "gtooth") in {result.name for result in first}


def test_gate_preserves_candidate_order_for_same_states() -> None:
    results = simulate_candidates()
    assert select_route(results, "baseline") == select_route(results, "gtooth")
