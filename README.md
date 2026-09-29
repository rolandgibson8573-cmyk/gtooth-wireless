# G-Tooth Wireless

**A proposed, experimental wireless link-control reference architecture.** This repository provides a small, deterministic scalar model and synthetic example—not a radio implementation or evidence of improved wireless performance.

| Area | Status |
| --- | --- |
| Master K-gate and inverse algebra | **LOCKED / CONFIRMED** (mathematical identities) |
| Six-scalar link state and scoring policy | **PROPOSED** |
| Packet metadata and G99 route objective | **PROPOSED** |
| Hardware measurements and comparative performance | **OPEN / NOT YET TESTED** |

The master governance rule is: **the K-gate form is the governed reference form; empirical values and wireless thresholds require independent measurement.** The value `0.383` is an optional proposed/configurable rejection threshold, not K and not a universal constant.

## Quick start

Requires Python 3.10 or later. Runtime code uses only the Python standard library; tests use pytest.

```sh
python -m examples.basic_simulation
python -m pytest
```

Example output (fixed synthetic inputs; not measured links):

```text
Synthetic demonstration only; values are not radio measurements.
Route          Baseline    G-Tooth
direct           0.7380     0.3588
relay            0.8080     0.4718
congested        0.5650     0.1824
Selected route (proposed G99 utility): relay
```

Small floating-point formatting differences are possible across Python/platform versions. The demonstration illustrates the scalar mapping and selection flow only.

## Mathematical model

The master governor is

\[
K = 3.912023005428146 = -\ln(0.02).
\]

For normalized input \(x\in[0,1]\), the governed reference map and its inverse are

\[
G_K(x)=\exp[-K(1-x)]\in[0.02,1],\qquad
G_K^{-1}(a)=1+\frac{\ln(a)}{K},\quad a\in[0.02,1].
\]

The scalar inverse is algebraically exact (up to floating-point rounding). Repeated application is a mathematical fixed-point iteration; neither property implies physical reversibility, radio behavior, or measured performance.

The proposed link state consists of six normalized real values in `[0, 1]`: link/spot quality, temporal freshness, stability, interference/path quality, gateway/global-field contribution, and rheostat/resource score. A nonnegative weight vector summing to one forms \(x=\sum_i w_i a_i\); the governed link utility is \(\alpha=G_K(x)\). Defaults in the reference code are illustrative policy, not calibrated coefficients. Optional freshness decay and rejection are policy choices; a rejection threshold can be configured and must be independently justified for its deployment.

**G99** is a proposed scheduler/route-selection objective: maximize an application-defined link utility subject to operational constraints (for example, resource budget, availability, and minimum dwell time). It is not an established physical field equation.

## What this project is—and is not

- **Is:** an openly inspectable reference definition, packet-metadata sketch, and reproducible deterministic synthetic demonstration.
- **Is not:** experimentally validated, a replacement for Shannon theory or established wireless standards, a claim of compression or increased channel capacity, or evidence for coherence-field physics.
- **Out of scope:** audio, DAW, DSP, preamp, and emotional-enhancement integrations. Such systems, if ever pursued, would be separate future adapters and are not part of this wireless/link-control project.
- **Security:** metadata is not encryption, authentication, or a security protocol. See [SECURITY.md](SECURITY.md).

## Project map

- [Wireless architecture specification](docs/GTOOTH_WIRELESS_SPEC.md)
- [Mathematical model and numerical notes](docs/MATHEMATICAL_MODEL.md)
- [Status register](docs/STATUS_REGISTER.md)
- [Reproducible experiment plan](docs/EXPERIMENT_PLAN.md)
- [Packet metadata proposal](protocol/packet_format.md)
- [Reference implementation](gtooth/)
- [Contributing and evidence standards](CONTRIBUTING.md)

## Roadmap

1. Review the proposed terminology, interfaces, and synthetic tests.
2. Build reproducible synthetic traces and compare policies against explicit baselines.
3. Only after defining controls and falsification criteria, evaluate on compatible SDR/ESP32-class hardware.
4. Publish independently reproducible measurements before making performance claims.

No live hardware results or cross-domain validation are included. See the status register and experiment plan; do not infer results from roadmap items.

## Citation

Use the repository metadata in [CITATION.cff](CITATION.cff). Cite a specific release or commit and identify the work as a proposed experimental architecture. Do not cite the reference implementation as evidence of validated wireless performance.
