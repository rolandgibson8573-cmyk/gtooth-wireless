# Mathematical Model

## Governed reference form — LOCKED

The master governor is the dimensionless scalar

\[
K_{\mathrm{MASTER}}=3.912023005428146=-\ln(0.02).
\]

This is a chosen model parameter, not a universal physical constant. The governed reference form is

\[
G_K(x)=e^{-K(1-x)},\qquad 0\leq x\leq1.
\]

Because the exponent ranges from \(-K\) to \(0\), the output range is

\[
G_K([0,1])=[e^{-K},1]=[0.02,1].
\]

The scalar map is strictly increasing, since \(G_K'(x)=K e^{-K(1-x)}>0\).

## Inverse — CONFIRMED algebraically

For \(a\in[0.02,1]\), solve \(a=e^{-K(1-x)}\):

\[
\ln(a)=-K(1-x),\quad \frac{\ln(a)}{K}=x-1,\quad
G_K^{-1}(a)=1+\frac{\ln(a)}{K}.
\]

Substitution gives \(G_K^{-1}(G_K(x))=x\) for \(x\in[0,1]\), and \(G_K(G_K^{-1}(a))=a\) for \(a\in[0.02,1]\), subject to floating-point rounding in software. The inverse is undefined for scores outside its stated domain in the reference implementation.

## Six-scalar wireless proposal

For normalized \(a_i\in[0,1]\) and weights \(w_i\geq0\) satisfying \(\sum_{i=1}^{6}w_i=1\):

\[
x=\sum_{i=1}^{6}w_i a_i\in[0,1],\qquad \alpha=G_K(x)\in[0.02,1].
\]

The six inputs are link quality, freshness, stability, interference/path quality, gateway/global-field contribution, and rheostat/resource score. Their meanings are proposed measurement features, not algebraically validated physical quantities.

Optional freshness half-life decay is

\[
f'=f\,e^{-(\ln2)t/h}=f\,2^{-t/h},
\]

where \(f\in[0,1]\), age \(t\geq0\), and half-life \(h>0\). This policy is optional and must not be treated as an empirical model absent measurements.

## Iteration and fixed points

Iteration means \(x_{n+1}=G_K(x_n)\), using the same K at every step. It is separate from the inverse/round-trip identity and has no physical interpretation by itself. The equation \(x=G_K(x)\) has the endpoint fixed point \(x=1\) and a lower fixed point near \(0.0218\). The derivative is \(G_K'(x)=K G_K(x)\); the lower fixed point is locally attracting, while the endpoint has derivative \(K>1\) and is repelling to perturbations from within `[0,1]`. Iterations from interior values approach the lower fixed point; the exact endpoint remains fixed. No claim about convergence of a radio, controller, or physical field follows.

## Numerical considerations

- Use `exp` and `log` from the standard numerical library and retain the inverse domain `[0.02,1]`; do not clamp invalid values silently.
- Validate all normalized inputs for finiteness and range before computing. Validate weights for finiteness, nonnegativity, and unit sum.
- `G_K(x)` stays bounded away from zero on its specified domain. The inverse uses the natural logarithm and is sensitive to invalid or rounded-below-floor values.
- Packet scalar quantization is lossy (8 bits per feature); it is not the exact scalar round-trip operation.
- In floating-point arithmetic, round-trip equality is approximate, not bitwise guaranteed.

## Algebraic round-trip is not hardware reversibility

The inverse recovers a scalar model input from a scalar model output. It does not restore information lost to quantization, noise, clipping, sampling, a changing channel, packet loss, or state estimation. No property in these equations establishes physical reversibility, radio transmission, compression, capacity gains, coherence-field physics, or a replacement for Shannon theory or established wireless standards.

`0.383` may be evaluated as a proposed/configurable score rejection threshold. It is not K and is not a mathematical consequence of the gate.
