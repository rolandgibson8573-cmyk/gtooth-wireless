"""Print deterministic synthetic candidate scores and the selected route."""

from gtooth.simulator import select_route, simulate_candidates


def main() -> None:
    results = simulate_candidates()
    print("Synthetic demonstration only; values are not radio measurements.")
    print(f"{'Route':<12} {'Baseline':>10} {'G-Tooth':>10}")
    for result in results:
        print(f"{result.name:<12} {result.baseline_score:>10.4f} {result.gtooth_score:>10.4f}")
    print(f"Selected route (proposed G99 utility): {select_route(results, 'gtooth')}")


if __name__ == "__main__":
    main()
