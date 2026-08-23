# ADR-004 Gate B — Mathematical Consistency Audit

- **ADR:** ADR-004 — Validation, Reproducibility, and Scientific Evidence
- **Phase:** 0C — Scientific Foundations
- **Gate:** B — Mathematical Consistency
- **Gate result:** **PASS**
- **Governing draft:** `ADR-004-validation-reproducibility-scientific-evidence.md`
- **Reviewed governing content SHA:** `8cca2e3ac514cd031bee1d8c9e4c0347694ecb53`
- **Pre-Gate review:** PASS
- **Gate A:** PASS
- **Gates C–F:** Not evaluated by this audit
- **ADR-004 acceptance:** NOT ACCEPTED

> Gate B evaluates signs, definitions, transformations, invariances, probability/event semantics, rank statements, and mathematical consistency of the ADR-004 evidence contract. Gate B does not establish unit consistency, software semantics, formal Golden Reference PASS, or boundary/failure acceptance.

---

## 1. Gate B Criterion

The Phase 0C roadmap defines Gate B as:

> Signs, dimensions, transformations, invariances, rank statements, and approximation boundaries must be internally consistent.

For ADR-004 the main mathematical objects are not only propagation formulas inherited from earlier ADRs. They also include stochastic estimators, assignment rules, event indicators, denominators, bias/variance decompositions, projective manifold metrics, covariance/eigenspace diagnostics, and paired-comparison semantics.

---

## 2. Audit Scope

Gate B checks:

```text
B1   scalar error / bias / variance / MSE / RMSE identities
B2   finite-sample empirical MSE decomposition
B3   divisor-N versus divisor-(N-1) variance roles
B4   multi-source assignment semantics
B5   cardinality mismatch / unmatched-output consistency
B6   detection and resolution event probability denominators
B7   Bernoulli probability-estimator bounds
B8   covariance / second-moment algebra
B9   source-count / rank / model-order distinctions
B10  manifold correlation / projective distance identities
B11  gauge invariance and subspace-basis invariance
B12  eigenvalue/eigenspace metric semantics
B13  CRN / paired-comparison mathematical meaning
B14  fixed/floating/hardware equivalence semantics
B15  approximation/profile boundaries inherited from ADR-001/002/003
```

---

## 3. Real-Valued Scalar Error Domain

ADR-004 F6 defines

\[
e=\hat q-q.
\]

The bias/variance/MSE identities in F6 are mathematically the ordinary real-valued scalar formulas used for DOA angle/direction-coordinate localization metrics.

For fixed real truth `q_0`,

\[
\operatorname{Bias}=E[e]
\]

and

\[
\operatorname{Var}(\hat q)
=E[(\hat q-E\hat q)^2]
=E[(e-Ee)^2].
\]

Then

\[
\operatorname{MSE}=E[e^2]
=\operatorname{Var}(\hat q)+\operatorname{Bias}^2.
\]

### Domain clarification

These formulas are mathematically exact for the intended **real-valued scalar localization quantity**. If a future profile defines MSE for a complex-valued quantity, the appropriate complex squared-error object is generally `|e|^2` rather than `e^2`, and that future metric must receive its own definition.

This is a domain condition, not a contradiction in VP-001.

### Gate-B finding

**PASS.** The F6 identities are correct for the declared localization-metric role.

---

## 4. Finite-Sample MSE Decomposition

For finite errors `e_i`, ADR-004 defines

\[
\bar e=\frac{1}{N}\sum_{i=1}^N e_i,
\]

\[
\widehat{MSE}=\frac{1}{N}\sum_{i=1}^N e_i^2,
\]

and

\[
v_N=\frac{1}{N}\sum_{i=1}^N(e_i-\bar e)^2.
\]

Expand:

\[
(e_i-\bar e)^2=e_i^2-2e_i\bar e+\bar e^2.
\]

Averaging,

\[
v_N
=\frac1N\sum_i e_i^2
-2\bar e\left(\frac1N\sum_i e_i\right)
+\bar e^2
\]

so

\[
v_N=\widehat{MSE}-\bar e^2.
\]

Therefore

\[
\boxed{\widehat{MSE}=v_N+\bar e^2}.
\]

### Gate-B finding

**PASS.** The finite empirical decomposition is exact.

---

## 5. `v_N` versus Unbiased Sample Variance `s^2`

ADR-004 separately defines

\[
s^2=\frac{1}{N-1}\sum_i(e_i-\bar e)^2.
\]

Hence

\[
s^2=\frac{N}{N-1}v_N
\]

for `N>1`.

Thus `s^2` is not the exact term in

\[
\widehat{MSE}=v_N+\bar e^2.
\]

### Gate-B finding

**PASS.** The governing draft correctly separates the divisor-`N` empirical decomposition quantity from the divisor-`N-1` statistical variance estimator.

---

## 6. GRP-018 Arithmetic Cross-Check

The reserved hand example is:

```text
truth = 10 deg
estimates = {9, 10, 12, 13} deg
errors = {-1, 0, 2, 3} deg
```

Then

\[
\bar e=\frac{-1+0+2+3}{4}=1\ \mathrm{deg}.
\]

The squared-error mean is

\[
\widehat{MSE}
=\frac{1+0+4+9}{4}
=3.5\ \mathrm{deg}^2.
\]

Therefore

\[
\widehat{RMSE}=\sqrt{3.5}=1.870828693\ldots\ \mathrm{deg}.
\]

The centered deviations are

```text
{-2, -1, 1, 2} deg
```

so

\[
v_N=\frac{4+1+1+4}{4}=2.5\ \mathrm{deg}^2,
\]

and

\[
2.5+1^2=3.5\ \mathrm{deg}^2.
\]

The unbiased sample variance is

\[
s^2=\frac{10}{3}\ \mathrm{deg}^2,
\]

which correctly does **not** replace `v_N` in the exact empirical decomposition.

### Gate-B finding

**PASS at audit arithmetic level.** Formal GRP-018 acceptance remains Gate E and is not claimed here.

---

## 7. Random-Truth Conditioning

The fixed-truth identity

\[
\operatorname{MSE}=\operatorname{Var}(\hat q)+\operatorname{Bias}^2
\]

is not silently generalized to every random-truth population. ADR-004 requires the averaging distribution and conditioning to be declared when truth itself varies.

This prevents ambiguity between, for example,

\[
E[(\hat q-q_0)^2\mid q_0]
\]

and

\[
E_{q,\hat q}[(\hat q-q)^2].
\]

### Gate-B finding

**PASS.** Conditional and unconditional estimands are not mathematically conflated.

---

## 8. Multi-Source Assignment Mathematics

For equal cardinality `K`, ADR-004 uses

\[
\pi^*=\arg\min_{\pi\in S_K}\sum_i C_{i,\pi(i)}.
\]

This is a finite one-to-one assignment problem when the declared costs are finite/admissible. Source permutation is treated as a nuisance symmetry for unordered truth sets.

For unequal cardinality, the ADR does not force an invalid permutation of unequal sets; unmatched truth and unmatched estimates remain explicit.

Association gating is mathematically separate from the assignment optimization. The gate defines admissible edges/pairs; the assignment determines the one-to-one mapping among admissible possibilities under the declared cost semantics.

### Gate-B finding

**PASS.** No cardinality or permutation inconsistency was found.

---

## 9. Association Is Not Resolution

A one-to-one matched pair is only an association result. A designated two-source resolution event additionally requires distinct admissible matches for both truth members under the declared resolution event.

Therefore a single collapsed estimate cannot satisfy two truth members under the standard one-to-one event.

Mathematically:

```text
one estimate index cannot be assigned to two different truth indices
```

under the one-to-one assignment constraint.

### Gate-B finding

**PASS.** Association and resolution event semantics are mathematically compatible.

---

## 10. Resolution Probability Estimator

ADR-004 defines for a fixed condition/trial law

\[
P_{res}=P(R=1\mid C,P_{trial}),
\]

with binary event indicator `R`.

For VP-001,

\[
\widehat P_{res}
=\frac{N_{resolved}}{N_{eligible,compatible}}.
\]

Because every resolved trial is an eligible compatible trial,

\[
0\le N_{resolved}\le N_{eligible,compatible},
\]

hence

\[
0\le\widehat P_{res}\le1.
\]

Numerical/algorithm failures on otherwise eligible compatible trials remain in the denominator as event failures, so failure filtering cannot mathematically inflate the baseline end-to-end estimator by reducing the denominator silently.

### Gate-B finding

**PASS.** The numerator/denominator relation is mathematically coherent.

---

## 11. Detection Probability Estimator

ADR-004 defines VP-001 source-level detection as

\[
\widehat P_D
=\frac{N_{detected\ truth\ opportunities}}
{N_{eligible\ truth\ opportunities\ in\ compatible\ trials}}.
\]

Each detected truth opportunity belongs to the eligible truth-opportunity universe, therefore

\[
0\le\widehat P_D\le1.
\]

A numerical failure on an otherwise eligible compatible trial contributes non-detections for affected eligible truth opportunities while retaining the failure type.

This preserves the mathematical denominator for an end-to-end probability rather than conditionally estimating only successful executions.

### Gate-B finding

**PASS.** Detection-probability counting is internally consistent.

---

## 12. Conditional versus End-to-End Probability Metrics

ADR-004 permits a valid-output conditional metric only under a distinct metric identity.

In general,

\[
P(R=1\mid \mathrm{valid})
\neq
P(R=1)
\]

when validity/failure is stochastic and associated with condition difficulty.

Therefore replacing the end-to-end probability with a successful-output conditional probability would change the estimand.

### Gate-B finding

**PASS.** Conditioning is mathematically explicit rather than silently changing the target probability.

---

## 13. Wilson Interval Scope

The VP-001 Wilson score interval default is restricted to ordinary IID fixed-`N` Bernoulli event evidence.

This is mathematically compatible with `P_D` / `P_res` only when the declared event opportunities satisfy the corresponding IID Bernoulli model at the interval-analysis level.

ADR-004 explicitly does not promote Wilson as a universal interval for clustered, sequential, weighted, hierarchical, or importance-sampled evidence.

### Gate-B finding

**PASS.** The interval method is correctly scoped and does not contradict the general dependence rules.

---

## 14. Uncentered Sample Second Moment Algebra

For snapshot matrix

\[
X\in\mathbb C^{M\times L},
\]

VP-001 uses

\[
\hat R^{(2)}=\frac1LXX^H.
\]

This matrix satisfies

\[
(XX^H)^H=XX^H,
\]

so it is Hermitian, and for any `z`,

\[
z^H\hat R^{(2)}z
=\frac1L\|X^Hz\|_2^2\ge0,
\]

so it is positive semidefinite in exact arithmetic.

Also,

\[
\operatorname{rank}(\hat R^{(2)})
=\operatorname{rank}(X)
\le\min(M,L).
\]

This does not conflict with ADR-002's centered-sample-covariance ceiling

\[
\operatorname{rank}(\hat C)\le\min(M,L-1),
\]

because the two matrix objects are explicitly different.

### Gate-B finding

**PASS.** Matrix algebra and rank semantics are consistent.

---

## 15. Source Count versus Rank and Model Order

The governing draft distinguishes

```text
K
rank(R_s)
observed signal-subspace rank
estimator model order
K_hat
```

and makes no invalid equality claim among them.

The accepted general relationship inherited from the upstream model is compatible with

\[
\operatorname{rank}(A R_s A^H)
\le
\min(\operatorname{rank}(A),\operatorname{rank}(R_s)).
\]

Thus `K` sources need not imply observed rank `K`, particularly under source coherence, manifold degeneracy, or rank-deficient transforms.

### Gate-B finding

**PASS.** No mathematically invalid `source count = rank = model order` identity is introduced.

---

## 16. Manifold Correlation Metric

For nonzero complex vectors `a,b`, ADR-004 uses

\[
\rho(a,b)=\frac{|a^Hb|}{\|a\|_2\|b\|_2}.
\]

By Cauchy–Schwarz,

\[
|a^Hb|\le\|a\|_2\|b\|_2,
\]

so

\[
0\le\rho\le1.
\]

Hence

\[
\alpha=\cos^{-1}\rho
\]

is real and lies in

\[
0\le\alpha\le\frac\pi2.
\]

And

\[
d_{proj}^2=1-\rho^2
\]

satisfies

\[
0\le d_{proj}^2\le1.
\]

### Domain clarification

The normalized correlation is undefined if `a=0` or `b=0`. VP-001 ideal steering vectors have unit-modulus entries and are therefore nonzero. A future zero/invalid-manifold case must be typed as ineligible/invalid for this metric or use another declared metric.

### Gate-B finding

**PASS.** The metric is mathematically bounded on its valid domain.

---

## 17. Complex-Scale / Phase Invariance

For nonzero complex scalars `c_1,c_2`,

\[
\rho(c_1a,c_2b)
=
\frac{|c_1^*c_2|\,|a^Hb|}
{|c_1|\|a\|\,|c_2|\|b\|}
=\rho(a,b).
\]

Therefore `rho`, `alpha`, and `d_proj^2` are invariant to nonzero common complex scaling of either vector.

This is mathematically compatible with their projective/gauge-aware role, while raw vector norms remain scale/phase sensitive.

### Gate-B finding

**PASS.** Gauge-aware and raw metrics answer mathematically distinct questions.

---

## 18. Rank-One Projector Identity

For unit vectors

\[
u=\frac{a}{\|a\|},
\qquad
v=\frac{b}{\|b\|},
\]

with orthogonal projector

\[
P_u^{\perp}=I-uu^H,
\]

we have

\[
\|P_u^{\perp}v\|_2^2
=v^H(I-uu^H)v
=1-|u^Hv|^2
=1-\rho^2.
\]

Thus the ADR-004 projective distance is consistent with the rank-one orthogonal leakage interpretation inherited from ADR-003.

### Gate-B finding

**PASS.** The projective metric identity is exact under the declared normalization.

---

## 19. Subspace Basis Invariance

If `U_s` spans a signal subspace and `Q` is unitary, then

\[
(U_sQ)(U_sQ)^H
=U_sQQ^HU_s^H
=U_sU_s^H.
\]

Therefore the projector

\[
P_s=U_sU_s^H
\]

is invariant to basis rotation.

This mathematically justifies the ADR-004 rule that projector/principal-angle metrics are preferred over raw eigenvector-entry equality when eigenspaces are the scientific object.

### Gate-B finding

**PASS.** Subspace comparison semantics respect basis nonuniqueness.

---

## 20. Eigenvector Phase Nonuniqueness

If

\[
Av=\lambda v,
\]

then for any scalar `c != 0`,

\[
A(cv)=\lambda(cv).
\]

For normalized complex eigenvectors, arbitrary unit-modulus phase remains. Therefore raw elementwise eigenvector equality is not a universal mathematical correctness criterion.

Repeated eigenvalues additionally allow arbitrary unitary basis rotations within the eigenspace.

### Gate-B finding

**PASS.** The governing draft's eigenstructure comparison rule is mathematically necessary.

---

## 21. Eigengap Role

The governing draft treats eigengap as a separate diagnostic rather than an error metric itself. This is mathematically coherent because eigenspace perturbation sensitivity depends on spectral separation; a small matrix perturbation may produce a large subspace rotation when the relevant eigengap is small.

ADR-004 does not claim one universal linear perturbation formula or threshold without theorem assumptions.

### Gate-B finding

**PASS.** No unjustified perturbation bound is universalized.

---

## 22. MUSIC Leakage and Final DOA

The draft distinguishes:

```text
noise-subspace leakage at truth
spectrum error
peak-location error
resolution event
final associated DOA error
```

These quantities are mathematically related under specific assumptions but are not identical.

For the rank-one normalized case, the accepted projector relation can reduce a MUSIC denominator to a `1-rho^2` form, but ADR-004 correctly does not generalize this identity to arbitrary multi-source/subspace/configuration cases.

### Gate-B finding

**PASS.** No invalid equivalence between spectrum and final-estimator error is asserted.

---

## 23. Common Random Numbers and Paired Effects

Let paired method metrics on the same exogenous trial be

\[
M_t^{(A)},\qquad M_t^{(B)},
\]

and define

\[
D_t=M_t^{(A)}-M_t^{(B)}.
\]

Then

\[
\operatorname{Var}(D)
=\operatorname{Var}(M_A)+\operatorname{Var}(M_B)
-2\operatorname{Cov}(M_A,M_B).
\]

CRN can reduce comparison variance when it induces useful positive covariance between paired outcomes. It changes the joint coupling used for comparison precision; it does not redefine the marginal scientific methods or justify uncontrolled sharing of method-internal randomness.

### Gate-B finding

**PASS.** The fair-comparison rationale for CRN is mathematically sound.

---

## 24. Geometry-Comparison Randomness Mapping

ADR-004 does not require unequal-dimensional geometries to consume numerically identical noise arrays. It requires scientifically common latent randomness to be paired under a declared mapping.

This avoids an impossible identity requirement such as equating random vectors in different-dimensional sample spaces while preserving the intent of paired experimental conditions.

### Gate-B finding

**PASS.** CRN semantics remain mathematically well-defined across geometry changes.

---

## 25. Equivalence versus Failure to Reject Difference

The governing draft states that `not significantly different` does not imply equivalence.

Mathematically, a failure to reject a point null does not establish that the true effect lies inside a declared engineering equivalence interval

\[
[-\Delta,+\Delta].
\]

Noninferiority/equivalence claims require explicit margins and corresponding inference.

### Gate-B finding

**PASS.** Inferential logic is correct.

---

## 26. Fixed-Point / Floating-Point Equivalence

ADR-004 distinguishes:

```text
bit-exact equality
bounded numerical equivalence
scientific/task-level equivalence
```

Finite-precision arithmetic is not associative in general, so

\[
(a+b)+c
\]

and

\[
a+(b+c)
\]

may differ numerically after rounding/reassociation even if they are algebraically identical over exact real arithmetic.

Therefore pipelining, unrolling, tree reduction, FMA use, or HLS scheduling need not imply bit-exact floating equality; the declared equivalence target must match the representation/architecture.

### Gate-B finding

**PASS.** The implementation-equivalence contract is mathematically compatible with finite-precision arithmetic.

---

## 27. Quantization Error Is Not Linearly Equivalent to DOA Error

The governing draft intentionally avoids a universal additive chain such as

\[
\Delta\theta = c\,e_q
\]

for arbitrary fixed-point quantization error `e_q`.

The actual map can pass through nonlinear and conditioning-sensitive stages:

\[
e_q
\rightarrow \Delta R
\rightarrow \Delta P_s
\rightarrow \Delta P(\theta)
\rightarrow \Delta\hat\theta.
\]

### Gate-B finding

**PASS.** No unsupported linear propagation identity is asserted.

---

## 28. Metric versus Acceptance Threshold

The governing ADR distinguishes a mathematical quantity from a decision threshold.

For example,

\[
\widehat P_{res}=0.91
\]

is a metric estimate. A rule such as

\[
P_{res}\ge0.90
\]

is an application/profile acceptance criterion.

The second does not follow mathematically from the definition of the first and therefore requires separate justification.

### Gate-B finding

**PASS.** Mathematical definitions are not contaminated by arbitrary universal thresholds.

---

## 29. Approximation Boundaries

ADR-004 inherits rather than redefines the mathematical approximation contracts of ADR-001/002/003.

In particular:

```text
far-field approximation != narrowband approximation
ordinary covariance/subspace != augmented improper-signal processing
ideal Phase-1 sensor != nonideal calibrated sensor model
```

A benchmark metric cannot mathematically repair an incompatible model assumption merely by producing a finite numeric value.

### Gate-B finding

**PASS.** Approximation and compatibility boundaries remain mathematically distinct.

---

## 30. Gate-B Boundary Conditions Carried Forward

The following are not contradictions but are explicit mathematical domains to be rechecked in Gate F and software semantics:

1. scalar `e^2` bias/MSE formulas are the real-valued localization-metric formulas; complex-valued future metrics require an explicit complex error definition;
2. normalized manifold correlation/projective metrics require nonzero vectors;
3. relative errors require nonzero or explicitly floored denominators;
4. assignment costs must be finite/declared on admissible edges;
5. principal angles/projector comparisons require declared subspace dimensions and handling of unequal dimensions;
6. Wilson intervals require the stated IID fixed-`N` Bernoulli scope;
7. sample-variance formulas require `N>1` where divisor `N-1` is used;
8. inverse/whitening metrics require the declared matrix to be nonsingular/regularized as governed by the profile.

No Gate-B blocker remains from these domain conditions.

---

## 31. Gate B Checklist

```text
Real scalar bias/variance/MSE identities                  PASS
Finite empirical MSE decomposition                       PASS
v_N versus s^2                                            PASS
GRP-018 arithmetic consistency                           PASS (audit only; formal Gate E pending)
Random-truth conditioning                                PASS
Equal-cardinality assignment semantics                   PASS
Unequal-cardinality handling                             PASS
Association versus resolution                            PASS
P_res estimator / denominator                            PASS
P_D estimator / denominator                              PASS
Conditional-vs-end-to-end probability distinction        PASS
Wilson scope                                              PASS
XX^H/L Hermitian / PSD / rank semantics                  PASS
Source count / rank / model order                        PASS
rho / alpha / d_proj bounds                              PASS
Complex-scale / phase invariance                         PASS
Rank-one projector identity                              PASS
Subspace basis invariance                                PASS
Eigenvector phase/nonuniqueness                          PASS
Eigengap interpretation                                  PASS
MUSIC diagnostic distinctions                            PASS
CRN paired-effect mathematics                            PASS
Geometry CRN dimensional semantics                       PASS
Equivalence / noninferiority logic                       PASS
Finite-precision equivalence semantics                   PASS
Quantization-to-DOA nonlinearity                         PASS
Metric versus threshold                                  PASS
Approximation/profile boundaries                         PASS
Blocking mathematical contradiction                      NONE
```

---

## 32. Gate B Decision

### **Gate B — Mathematical Consistency: PASS**

ADR-004 is mathematically coherent at the governing-contract level.

The bias/variance/MSE/RMSE definitions and finite-sample decomposition are consistent; association and event-probability denominators are well-defined; covariance and rank semantics do not conflict; projective/eigenspace metrics respect their invariances; CRN and paired-comparison logic are sound; and the finite-precision/hardware equivalence hierarchy does not assume exact-real arithmetic properties that do not hold numerically.

No correction to the governing ADR is required for a Gate-B PASS. The domain conditions listed in Section 30 are explicit audit interpretations of the intended metrics and shall be checked again at Gate F and during software-semantic implementation.

---

## 33. Status after Gate B

```text
Pre-Gate consistency review                PASS
Gate A — Physical Consistency              PASS
Gate B — Mathematical Consistency          PASS
Gate C — Dimensional / Unit Consistency     NEXT
Gate D — Software Semantic Consistency      NOT STARTED
Gate E — Hand Reference Evidence            NOT STARTED
Gate F — Boundary / Failure Analysis         NOT STARTED
ADR-004 acceptance                          NOT ACCEPTED
Authoritative Phase-1 implementation        NOT YET AUTHORIZED
```

The next work item is:

```text
ADR-004 Gate C — Dimensional and Unit Consistency Audit
```
