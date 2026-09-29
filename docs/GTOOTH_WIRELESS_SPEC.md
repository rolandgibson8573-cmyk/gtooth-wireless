# G-Tooth Wireless Architecture Specification

**Status:** proposed reference architecture; not an adopted wireless standard.

## 1. Scope and terminology

This document specifies a wireless-only link-control proposal. A *candidate link* is a direct or relayed path for which a controller has normalized observations. A *link state* is the six-value vector defined below. A *governed score* is a scalar produced by applying the locked reference K-gate to a weighted composite. A *gateway/global-field contribution* is a proposed input feature supplied by a system's own estimator; the term does not assert a physical field.

Audio, DAW, DSP, preamp, and emotional-enhancement systems are out of scope.

## 2. Data flow

1. A platform-specific adapter gathers link and resource observations and converts them to finite normalized values.
2. An optional receiver-side age estimate adjusts freshness using a configured half-life. Clock and rollover handling are adapter responsibilities.
3. The policy validates the six scalars and combines them using nonnegative weights summing to one.
4. The governed map produces a score in `[0.02, 1]`. A configured acceptance threshold, if used, rejects below-threshold candidates.
5. A scheduler ranks eligible routes, then applies constraints, hysteresis, and minimum dwell time before switching.
6. Observations, policy version, decision, and relevant timing should be logged so another implementation can reproduce the decision.

The reference Python implementation defines scalar operations only. It does not read a radio, estimate a channel, transmit, or implement a scheduler.

## 3. Proposed six-scalar state

The order in `gtooth.core.LinkState` and in version-1 packet metadata is:

| Name | Proposed meaning |
| --- | --- |
| `link_quality` | Local link/spot quality estimate from a specified measurement procedure |
| `freshness` | Recency/relevance of the observation |
| `stability` | Short-window consistency estimate |
| `path_quality` | Interference and path-quality estimate |
| `gateway_contribution` | Contribution from gateway/global coordination inputs |
| `resource_score` | Rheostat/resource availability or cost preference |

Each value is a finite real number in `[0,1]`. Implementations must document raw measurement units, normalization bounds, missing-value handling, and observation window. Missing data must not silently be encoded as a favorable value. Reference defaults are illustrative only; deployments must choose and justify their own weights.

## 4. Scoring and rejection

For state values \(a_i\) and weights \(w_i\):

\[
x=\sum_{i=1}^{6}w_i a_i,\quad w_i\geq0,\quad\sum_iw_i=1,\qquad
\alpha=G_K(x)=\exp[-K(1-x)].
\]

Use `K = -ln(0.02)` in the governed reference form. An optional freshness decay is \(f'=f\,2^{-t/h}\), for nonnegative age \(t\) and positive half-life \(h\). It is a policy transform, not a radio law. A rejection threshold \(r\) may be configured on the score domain `[0.02,1]`; `0.383` is one proposed/configurable value and has no universal status or relationship to K.

Since \(G_K\) is strictly increasing, applying it to a single composite preserves its ranking. Any claim of a better route outcome must therefore come from separately stated policy choices, constraints, robustness, or measured system effects—not from a ranking change caused by the monotonic mapping alone.

## 5. Proposed G99 scheduling objective

G99 names a proposed route/scheduler objective, not an established physical field equation. A deployment can choose utility \(U\) based on governed link scores and solve, for example,

\[
\max_{r\in\mathcal{R}} U(r)
\quad\text{subject to availability, resource, latency, and policy constraints.}
\]

The objective, constraints, tie-breaking, sampling interval, and missing-observation behavior must be versioned and reported. Do not call this physical law or infer wireless capacity from it.

## 6. Stability and switching guidance

To avoid route flapping, implementations should consider:

- a configurable hysteresis margin: switch only when a challenger exceeds the current route by the margin for a defined number of observations;
- a minimum dwell time after a switch, except for an explicit safety/availability override;
- separate thresholds for entering and leaving an eligible state when appropriate;
- deterministic tie-breaking and a defined fallback when no route is eligible.

These are recommendations, not calibrated defaults. Report each setting in experiments and test edge cases such as stale observations and rapid alternating scores.

## 7. Packet metadata

The companion packet format proposes an 18-byte, big-endian metadata record containing a magic value, version, reserved flags, sequence, node identifier, millisecond timestamp, and six quantized scalar values. It is not a complete wireless packet. See [packet_format.md](../protocol/packet_format.md) for field semantics, wraparound, and compatibility guidance. Payload framing, addressing, retransmission, authentication, and encryption remain the responsibility of an established transport/link layer.

## 8. Limitations

There are no live hardware results, dataset results, or cross-domain validation in this repository. The model does not claim radio transmission, compression, coherence-field physics, capacity improvement, or replacement of Shannon theory or existing standards. Empirical values, thresholds, weights, and useful operating regimes remain open until measured independently and reproducibly.
