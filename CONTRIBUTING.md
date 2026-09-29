# Contributing

Contributions should keep this repository focused on wireless link-control. Audio, DAW, DSP, preamp, and emotional-enhancement integrations are out of scope.

## Formulas, scalars, and status

- Preserve the governed reference K-gate form unless a change is explicitly proposed and reviewed. Do not describe K as a universal physical constant.
- Every new scalar or formula must define units, domain, normalization, assumptions, role, and relationship to existing parameters. Do not conflate `0.383` with K.
- Label claims/components **LOCKED**, **CONFIRMED**, **PROPOSED**, **OPEN**, or **NOT YET TESTED** accurately. Algebraic verification is not empirical validation.
- Document missing-data behavior, parameter provenance, and whether values are illustrative, synthetic, or measured.

## Evidence and implementation

- Never fabricate measurements, datasets, hardware results, citations, or performance claims.
- Separate synthetic tests from traces and measurements. For empirical claims include reproducible hardware, firmware, configuration, controls, baseline, metrics, and analysis details; follow the experiment plan.
- Keep the reference implementation deterministic, small, and dependency-free at runtime. Validate finite normalized inputs and test domains, boundaries, invalid data, and serialization.
- Preserve compatibility deliberately: version wire-format changes and include tests for both supported behavior and rejection paths.
- Run `python -m pytest` and `python -m examples.basic_simulation` before submitting. Include actual command outcomes; do not claim unrun checks passed.

## Review

Explain the motivation and scope of a change, link any relevant evidence, describe limitations, and state whether results are synthetic or empirical. A proposed architecture feature should not be described as validated behavior.
