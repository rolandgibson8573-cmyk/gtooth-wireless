# Status Register

Status labels distinguish algebra from proposed architecture and empirical claims. A LOCKED formula is the project's governed reference form; it does not imply physical validation.

| Claim or component | Status | Basis / evidence needed |
| --- | --- | --- |
| \(K=3.912023005428146=-\ln(0.02)\) | **LOCKED / CONFIRMED** | Algebraic definition and scalar unit test |
| \(G_K(x)=e^{-K(1-x)}\), \(x\in[0,1]\) | **LOCKED / CONFIRMED** | Specified reference function and output bound |
| \(G_K^{-1}(a)=1+\ln(a)/K\), \(a\in[0.02,1]\) | **LOCKED / CONFIRMED** | Algebraic derivation and scalar round-trip test |
| Fixed-point iteration behavior | **CONFIRMED** (mathematical property only) | Scalar iteration; not a physical convergence claim |
| Six normalized wireless state values | **PROPOSED** | Requires operational measurement definitions |
| Weight selection and composite scoring policy | **PROPOSED** | Reference defaults are illustrative; empirical tuning open |
| Optional freshness decay | **PROPOSED** | Needs clock/age handling and measured policy evaluation |
| `0.383` rejection threshold | **PROPOSED / OPEN** | Configurable candidate only; needs independent calibration |
| Packet metadata layout and 8-bit scalar quantization | **PROPOSED** | Requires interoperability and overhead evaluation |
| G99 constrained route/scheduler utility | **PROPOSED** | Objective/constraints require explicit implementation and testing |
| Route stability, hysteresis, dwell-time settings | **PROPOSED** | No calibrated operational settings |
| Synthetic simulation values | **CONFIRMED** as deterministic software output only | Generated from fixed source constants; not radio observations |
| Live hardware measurements | **NOT YET TESTED** | No live hardware results are present |
| Comparative wireless-performance claims | **OPEN / NOT YET TESTED** | Requires controlled baseline experiments and reproducible traces |
| Cross-domain validation | **NOT YET TESTED** | None is claimed or included |
| Replacement of Shannon theory or wireless standards | **NOT CLAIMED** | Outside project scope |
