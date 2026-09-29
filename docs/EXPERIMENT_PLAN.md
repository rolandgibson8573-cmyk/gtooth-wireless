# Reproducible Experiment Plan

**Status: planned only. No results are reported here.** The reference simulator is deterministic arithmetic over fixed synthetic inputs; it is not a wireless channel model.

## Questions and hypotheses

1. **Decision quality:** Under explicitly defined link observations and constraints, does a six-scalar governed-score policy select routes that meet or improve predeclared service metrics relative to a specified baseline?
2. **Freshness:** Does optional age decay improve behavior with stale measurements without creating avoidable route churn?
3. **Stability:** Do predeclared hysteresis and dwell-time settings reduce unnecessary switching while keeping outage/latency within target bounds?
4. **Overhead:** What airtime and processing overhead does the metadata format add on the chosen transport?

These are questions, not expected or established outcomes. Treat any hypothesis as falsified if the preregistered primary metric fails its acceptance criterion, or if performance regressions exceed the stated tolerance.

## Stage 1: synthetic traces

1. Publish a trace generator with a fixed seed, versioned parameters, and documented units. Include stationary, fading, interference-burst, stale-observation, missing-data, and route-switch scenarios.
2. Preserve raw synthetic inputs and configuration alongside outputs; do not describe generated traces as field data.
3. Compare at least: (a) a conventional baseline defined before evaluation (for example, strongest measured link), (b) six-scalar weighted composite without the gate, and (c) the governed-score policy with the same inputs and constraints.
4. Evaluate threshold and weight sensitivity without selecting a favorable setting on the final evaluation traces.
5. Report per-scenario availability, packet delivery ratio, latency distribution, outage duration, route switches, resource use, and threshold rejection counts. Mark not-applicable metrics explicitly.

Because the K-gate is monotonic, baseline and governed scores over an identical single composite should yield the same ranking absent thresholds or other policy effects. Any route differences must be traced to explicit additional constraints or policy, not attributed to the map alone.

## Stage 2: SDR/ESP32-compatible measurements

Only proceed after documenting the board/radio, firmware, antenna, channel/band, legal operating constraints, transport, clock source/synchronization, measurement units, and exact normalization procedure. Store machine-readable raw traces and configuration; publish hashes and replay tooling where practical. A simulator or desktop unit test is not a substitute for this stage.

Use fixed positions and controlled traffic/channel conditions first, then preregistered variations in distance, interference, mobility, and competing traffic. Randomize policy run order where feasible. Use identical hardware, payload workload, power, and channel conditions for baseline and candidate runs. Record losses, retransmissions, timestamps, resource load, and all scoring inputs at a declared sampling rate. Repeat enough runs to report uncertainty and device-to-device variability; state exclusions before analysis.

Do not transmit on unauthorized frequencies or exceed local power limits. Use shielded/conducted tests or appropriately authorized spectrum where needed.

## Baselines, controls, and analysis

- Freeze and version the baseline policy, candidate weights, threshold, freshness half-life, hysteresis, and dwell time before held-out tests.
- Include an ablation without the gate and an ablation without freshness decay; preserve the same underlying state and constraints.
- Compare identical route candidates and measurement windows. Separate calibration from held-out evaluation.
- Define a primary outcome and acceptance margin before collecting data. Report all planned outcomes, including negative results and uncertainty intervals.
- Log software revision, firmware, configuration, trace IDs, and environment. Do not invent, omit, or retrospectively relabel measurements.

## Falsification and publication

The performance hypothesis is not supported if held-out results fail the preregistered criterion, are indistinguishable within uncertainty where improvement was required, or show unacceptable regressions in outage, latency, loss, or resource cost. Repeated instability, irreproducibility, or inability to beat the stated baseline should be published as such. Publish raw/derived data when lawful and safe, the analysis procedure, limitations, and enough detail for independent replay.
