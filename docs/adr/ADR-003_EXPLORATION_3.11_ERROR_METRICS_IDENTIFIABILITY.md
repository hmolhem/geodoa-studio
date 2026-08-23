# ADR-003 Exploration 3.11 — Error Metrics and Identifiability

- **Phase:** 0C — Scientific Foundations
- **Status:** EXPLORATION COMPLETE — CANDIDATE CONTRACT, NOT ACCEPTED
- **Parent ADR:** ADR-003 — Sensor Imperfections, Mutual Coupling, and Calibration
- **Branch:** `docs/phase0c-scientific-conventions`
- **Depends on:** ADR-001, ADR-002, ADR-003 Explorations 3.1–3.10
- **Acceptance gates:** Not started

> This is the dedicated exploration record for ADR-003 Section 3.11. It is not an accepted governing ADR. Candidate decisions remain subject to 3.12–3.14 reconciliation, Gates A–F, Golden Reference evidence, boundary/failure analysis, and final acceptance.

---

## 1. Primary question

Explorations 3.1–3.10 established multiple sensor-imperfection families, calibration strategies, direct measured/EM manifolds, gauge/reference-plane semantics, uncertainty, interpolation, and provenance.

Exploration 3.11 answers:

> How shall GeoDOA measure error and mismatch without erasing physically meaningful distinctions, and how shall it distinguish an error that is numerically small from a parameter that is scientifically identifiable, observable, or well-conditioned?

The governing principles are

\[
\boxed{
\text{No single scalar error metric is sufficient for every sensor/calibration question.}
}
\]

and

\[
\boxed{
\text{Identifiability, observability, conditioning, uncertainty, and numerical fit are distinct scientific concepts.}
}
\]

---

## 2. Error taxonomy

GeoDOA shall distinguish at least the following error levels.

### 2.1 Parameter error

For a physically meaningful parameter vector,

\[
\boxed{
\Delta\boldsymbol\theta
=\hat{\boldsymbol\theta}-\boldsymbol\theta_{\rm ref}.
}
\]

Examples include position error, gain error, phase error, delay error, coupling-parameter error, sample-clock error, or I/Q coefficient error.

### 2.2 Operator error

For compatible linear operators,

\[
\boxed{
\Delta\mathbf H
=\mathbf H_{\rm test}-\mathbf H_{\rm ref}.
}
\]

Operator error is not meaningful unless input/output reference planes, channel basis, state, and included-effects semantics match.

### 2.3 Manifold error

At source/scene state \(\xi\),

\[
\boxed{
\Delta\mathbf a(\xi)
=\mathbf a_{\rm test}(\xi)-\mathbf a_{\rm ref}(\xi).
}
\]

This raw difference is representation dependent and may contain a common phase/scale that is irrelevant to some DOA observables.

### 2.4 Statistical error

Examples include covariance, pseudocovariance, eigenvalue, eigenspace, subspace, or noise-statistics error.

These are developed primarily in 3.12.

### 2.5 Estimator-output error

Examples include DOA bias, RMSE, resolution probability, missed detections, false peaks, or estimator failure state.

ADR-004 governs formal validation statistics, but ADR-003 must preserve the chain from physical mismatch to estimator output.

---

## 3. Error reference must be explicit

An error requires a reference object.

The following are different comparisons:

```text
physical vs nominal
measured vs physical truth in simulation
EM vs measured
calibrated vs physical
calibrated vs nominal
corrected vs target identity response
interpolated vs held-out measured response
estimated parameter vs realized parameter
```

GeoDOA shall not report `manifold_error = x` without declaring which two scientific objects were compared.

---

## 4. Raw Euclidean manifold error

For two registered complex vectors \(\mathbf a\) and \(\mathbf b\), define

\[
\boxed{
d_{\rm raw}(\mathbf a,\mathbf b)
=\|\mathbf b-\mathbf a\|_2.
}
\]

A relative form may be

\[
\boxed{
\varepsilon_{\rm raw,rel}
=\frac{\|\mathbf b-\mathbf a\|_2}{\|\mathbf a\|_2}
}
\]

provided \(\|\mathbf a\|_2>0\).

This metric preserves common phase and scale differences. It is appropriate only when those differences are physically meaningful for the comparison.

---

## 5. Phase-only aligned manifold error

When common phase is considered an equivalence but common amplitude is not, define

\[
\boxed{
\varepsilon_{\phi}
=\min_{\phi\in\mathbb R}
\frac{\|\mathbf b-e^{j\phi}\mathbf a\|_2}{\|\mathbf a\|_2}.
}
\]

The optimum phase satisfies, when \(\mathbf a^H\mathbf b\neq0\),

\[
\boxed{
\phi^*
=\arg(\mathbf a^H\mathbf b).
}
\]

The sign/order convention in the alignment expression shall be preserved consistently.

If \(\mathbf a^H\mathbf b=0\), the optimum phase is not unique even though the minimum residual is well-defined.

---

## 6. Common-complex-scale aligned manifold error

When common complex scale is considered irrelevant, define

\[
\boxed{
\varepsilon_{c}
=\min_{c\in\mathbb C}
\frac{\|\mathbf b-c\mathbf a\|_2}{\|\mathbf b\|_2}
}
\]

or another explicitly declared normalization.

For the unweighted least-squares problem

\[
\min_c\|\mathbf b-c\mathbf a\|_2^2,
\]

with \(\|\mathbf a\|_2>0\),

\[
\boxed{
c^*
=\frac{\mathbf a^H\mathbf b}{\mathbf a^H\mathbf a}.
}
\]

GeoDOA shall record which vector is treated as the scale-adjustable reference because the normalized residual definition can otherwise appear symmetric when it is not.

---

## 7. Normalized complex coherence / projective alignment

For nonzero vectors define

\[
\boxed{
\rho(\mathbf a,\mathbf b)
=\frac{|\mathbf a^H\mathbf b|}
{\|\mathbf a\|_2\|\mathbf b\|_2},
\qquad 0\le\rho\le1.
}
\]

This quantity is invariant to nonzero common complex scaling of either vector.

The corresponding projective angle is

\[
\boxed{
\alpha(\mathbf a,\mathbf b)
=\cos^{-1}\rho
\in[0,\pi/2].
}
\]

A squared projective leakage/chordal quantity is

\[
\boxed{
d_{\rm proj}^2
=1-\rho^2
=\sin^2\alpha.
}
\]

This is especially useful for narrowband subspace methods because it measures mismatch of one-dimensional complex subspaces rather than mismatch of arbitrary complex scale.

---

## 8. Exact link to rank-one signal-subspace leakage

Let

\[
\mathbf u
=\frac{\mathbf a}{\|\mathbf a\|_2}
\]

be the unit true/reference steering vector and

\[
\mathbf v
=\frac{\mathbf b}{\|\mathbf b\|_2}
\]

be the unit test/model vector.

The projector onto the orthogonal complement of the rank-one signal subspace is

\[
\boxed{
\mathbf P_{\perp}
=\mathbf I-\mathbf u\mathbf u^H.
}
\]

Then

\[
\boxed{
\|\mathbf P_{\perp}\mathbf v\|_2^2
=1-|\mathbf u^H\mathbf v|^2
=1-\rho^2
=d_{\rm proj}^2.
}
\]

Thus projective mismatch is not merely a geometric convenience: for a rank-one reference signal subspace, it is exactly the normalized energy of the model vector leaking into the orthogonal/noise subspace.

This identity is a direct bridge to Exploration 3.12.

---

## 9. Deterministic coupling metric check using GRP-016/017 seed

From Exploration 3.5,

\[
\mathbf a
=\begin{bmatrix}1\\-j\end{bmatrix},
\qquad
\mathbf b
=\begin{bmatrix}1-0.5j\\0.5-j\end{bmatrix}.
\]

The previously derived squared normalized alignment is

\[
\boxed{
\rho^2=0.8.
}
\]

Therefore

\[
\boxed{
d_{\rm proj}^2=1-0.8=0.2.
}
\]

The coupled response places 20% of its normalized energy outside the nominal rank-one subspace.

This is consistent with the reserved GRP-017 seed and shall be reconciled formally at Gate E rather than counted as a new GRP.

---

## 10. Phase-only versus projective metrics answer different questions

If

\[
\mathbf b=2\mathbf a,
\]

then

\[
\rho=1,
\qquad
 d_{\rm proj}=0,
\]

but a phase-only aligned residual remains nonzero because the amplitude scale differs.

Conversely, if the only difference is common phase,

\[
\mathbf b=e^{j\phi}\mathbf a,
\]

both phase-only and projective errors vanish.

Therefore GeoDOA shall not choose one metric globally and call it `manifold_error`.

---

## 11. Per-channel amplitude error

For nonzero reference component \(a_n\), define an amplitude ratio

\[
\boxed{
r_{A,n}
=\frac{|b_n|}{|a_n|}
}
\]

and logarithmic amplitude error

\[
\boxed{
e_{A,n,\rm dB}
=20\log_{10}r_{A,n}.
}
\]

This metric is undefined when the reference magnitude is zero.

Near response nulls, ratio-based amplitude metrics can become numerically unstable and should be accompanied by absolute-error or threshold/quality semantics.

---

## 12. Per-channel relative phase error

After a declared common-phase/gauge alignment, a channel-relative phase residual may be

\[
\boxed{
e_{\phi,n}
=\operatorname{wrap}
\left(\angle b_n-\angle a_n-\phi_{\rm align}\right).
}
\]

The wrap interval shall be explicit, e.g. \((-\pi,\pi]\).

Near a magnitude null, phase may be physically/numerically poorly defined, so phase-error reporting requires an amplitude-confidence rule.

---

## 13. Delay and phase-slope error

For a delay-sensitive calibration, phase error at one frequency is insufficient.

With transfer phase \(\phi(f)\), a delay-related residual may be derived from phase slope:

\[
\boxed{
\Delta\tau
=\frac{1}{2\pi}
\frac{d\,\Delta\phi(f)}{df}
}
\]

under the accepted sign convention and after a valid phase-unwrapping/reference treatment.

Delay error has units of time and shall not be reported only in degrees unless the frequency is also declared.

---

## 14. Position error metrics

Position calibration shall preserve physical vector error

\[
\boxed{
\Delta\mathbf r_n
=\hat{\mathbf r}_n-\mathbf r_n^{\rm ref}
}
\]

in meters.

Possible derived metrics include

\[
\|\Delta\mathbf r_n\|_2,
\qquad
\frac{\|\Delta\mathbf r_n\|_2}{\lambda},
\qquad
\hat{\mathbf u}^T\Delta\mathbf r_n.
\]

These answer different questions. The wavelength-normalized and directional projections are derived, frequency/direction-dependent quantities and do not replace the physical error vector.

---

## 15. Gain/phase parameter metrics

For gain

\[
g_n=\rho_n e^{j\phi_n},
\]

GeoDOA may report separately

\[
\boxed{
\Delta\rho_n,
\quad
20\log_{10}(\hat\rho_n/\rho_n^{\rm ref}),
\quad
\operatorname{wrap}(\hat\phi_n-\phi_n^{\rm ref}).
}
\]

A complex Euclidean gain residual can additionally be useful, but it shall not hide the amplitude/phase decomposition when engineering interpretation is required.

---

## 16. Coupling/network parameter metrics

For compatible complex matrices, candidate norms include

\[
\boxed{
\|\Delta\mathbf C\|_F,
\qquad
\|\Delta\mathbf C\|_2.
}
\]

A relative Frobenius error may be

\[
\boxed{
\varepsilon_{C,F}
=\frac{\|\hat{\mathbf C}-\mathbf C_{\rm ref}\|_F}
{\|\mathbf C_{\rm ref}\|_F}.
}
\]

But direct comparison is valid only when the matrices represent the same physical quantity: Z with Z, S with S under same reference impedance, loaded-port operator with same loaded-port operator, or effective coupling with the same declared manifold domain.

---

## 17. Operator error and induced response error

A small matrix norm does not necessarily imply a small DOA-relevant response error for every source state.

If

\[
\mathbf b=(\mathbf H+\Delta\mathbf H)\mathbf a,
\]

then

\[
\boxed{
\Delta\mathbf b
=\Delta\mathbf H\mathbf a.
}
\]

The bound

\[
\boxed{
\|\Delta\mathbf b\|_2
\le
\|\Delta\mathbf H\|_2\|\mathbf a\|_2
}
\]

is useful but can be conservative and does not directly encode projective DOA sensitivity.

Therefore operator metrics and induced manifold metrics shall remain distinct.

---

## 18. Domain-aggregated manifold metrics

A calibration exists over a domain \(\Omega\) of direction/frequency/polarization/state.

A weighted integrated error may be

\[
\boxed{
E
=\frac{\int_{\Omega}
w(\xi)e(\xi)\,d\mu(\xi)}
{\int_{\Omega}w(\xi)\,d\mu(\xi)}.
}
\]

For a discrete grid,

\[
\boxed{
E
=\frac{\sum_m w_m e_m}{\sum_m w_m}.
}
\]

The measure/weights define the engineering question and shall be declared.

Uniform angle weighting, uniform direction-cosine weighting, uniform solid-angle weighting, and operational-prior weighting are not equivalent.

---

## 19. Worst-case and percentile metrics

Mean error can hide localized failures near endfire, nulls, resonances, or calibration-domain boundaries.

GeoDOA shall permit reporting of at least:

- mean/weighted mean;
- RMS where meaningful;
- median;
- high percentile;
- maximum/worst-case;
- location/state of worst-case error.

A scalar average without domain coverage information is insufficient for scientific calibration quality claims.

---

## 20. Fit residual versus prediction error

Calibration fit residual is

\[
\boxed{
\mathbf r_{\rm fit}
=\mathbf y_{\rm cal}
-\hat{\mathbf y}(\hat{\boldsymbol\theta})
}
\]

on data used for estimation.

Held-out prediction residual is

\[
\boxed{
\mathbf r_{\rm pred}
=\mathbf y_{\rm check}
-\hat{\mathbf y}(\hat{\boldsymbol\theta};\xi_{\rm check}).
}
\]

A model can have small fit error but poor prediction because of overfitting, model-form error, interpolation failure, or state mismatch.

GeoDOA shall not use training/calibration residual as the sole evidence of generalized calibration accuracy.

---

## 21. Repeatability versus accuracy

Repeated measurements may estimate repeatability/precision.

If repeated estimates are tightly clustered but share a systematic bias, repeatability can be excellent while physical accuracy is poor.

Therefore GeoDOA shall distinguish:

\[
\boxed{
\text{repeatability / precision}
\neq
\text{accuracy / bias relative to reference truth}.
}
\]

This distinction is especially important for chamber/CST cross-comparison and calibration-source uncertainty.

---

## 22. Uncertainty versus error

Error is a difference from a reference value, often unknown in physical experiments.

Uncertainty quantifies incomplete knowledge about a quantity or estimate.

A physical calibration artifact may legitimately report uncertainty without knowing the exact physical error.

GeoDOA shall not use `error_bar` semantics that imply known truth when only estimate uncertainty is available.

---

## 23. Local uncertainty propagation

For response \(\mathbf a(\boldsymbol\theta)\), linearize around \(\hat{\boldsymbol\theta}\):

\[
\mathbf a
\approx
\mathbf a(\hat{\boldsymbol\theta})
+\mathbf J_a\delta\boldsymbol\theta.
\]

If

\[
\mathbf P_{\theta}
=\operatorname{Cov}(\delta\boldsymbol\theta),
\]

then

\[
\boxed{
\mathbf R_{a}
\approx
\mathbf J_a\mathbf P_{\theta}\mathbf J_a^H.
}
\]

This is a first-order local approximation and can fail under strong nonlinearity, large uncertainty, wrapped phase, multimodal ambiguity, or parameter boundaries.

---

## 24. Identifiability definition

A parameterization is identifiable over a declared experiment/model if distinct admissible parameter states do not produce the same observable data, except for explicitly declared gauge/equivalence transformations.

Let

\[
\mathbf y=\mathcal F(\boldsymbol\theta).
\]

Global identifiability modulo gauge group \(\mathcal G\) means, conceptually,

\[
\boxed{
\mathcal F(\boldsymbol\theta_1)
=\mathcal F(\boldsymbol\theta_2)
\Rightarrow
\boldsymbol\theta_2
\sim_{\mathcal G}
\boldsymbol\theta_1.
}
\]

Identifiability belongs to the model/experiment, not to one optimizer run.

---

## 25. Global versus local identifiability

A model can be locally identifiable near one solution while retaining another distant solution that produces the same observations.

Therefore GeoDOA shall distinguish:

- global identifiability;
- local identifiability;
- non-identifiability;
- identifiability only after gauge/reference constraints.

A full-rank local Jacobian does not by itself prove global uniqueness.

---

## 26. Gauge freedom and observable equivalence classes

Examples of gauge/equivalence transformations already established include:

- common complex scale between source amplitude and channel gains;
- common phase reference;
- rigid translation unobservable from relative far-field phase;
- common latency unobservable from differential timing alone;
- common frequency/phase references under certain simultaneous observables.

GeoDOA shall represent such freedoms as deliberate equivalence classes rather than label them calibration failures.

An error metric shall either be gauge invariant or state which gauge has been fixed before comparison.

---

## 27. Local Jacobian observability

For differentiable model

\[
\mathbf y(\boldsymbol\theta),
\]

define

\[
\boxed{
\mathbf J_{\theta}
=\frac{\partial\mathbf y}
{\partial\boldsymbol\theta^T}.
}
\]

After removing/fixing known gauge directions, local rank deficiency of \(\mathbf J_{\theta}\) indicates locally unobservable parameter combinations.

The singular values of a properly scaled Jacobian provide sensitivity/conditioning information.

However, raw Jacobian conditioning is unit/parameterization dependent and shall not be compared across heterogeneous parameters without explicit scaling/normalization.

---

## 28. Parameter scaling in sensitivity analysis

Suppose \(\boldsymbol\theta\) contains meters, radians, seconds, and dimensionless gains.

The condition number of the unscaled Jacobian can change under a simple unit conversion from meters to millimeters.

Therefore GeoDOA shall not call a calibration problem `well-conditioned` from an unscaled mixed-unit Jacobian alone.

A scaled parameterization may use

\[
\boxed{
\tilde{\boldsymbol\theta}
=\mathbf S_{\theta}^{-1}
(\boldsymbol\theta-\boldsymbol\theta_0)
}
\]

with physically declared characteristic scales.

The choice of \(\mathbf S_{\theta}\) belongs to the diagnostic definition.

---

## 29. Singular values and near-identifiability

Even when the local Jacobian has full column rank, a very small singular value can mean that one parameter combination is only weakly observed and highly noise sensitive.

Thus

\[
\boxed{
\text{full rank}
\not\Rightarrow
\text{well-conditioned estimation}.
}
\]

GeoDOA shall distinguish structural identifiability from practical estimability/conditioning.

---

## 30. Fisher information as a model-dependent diagnostic

Under a fully declared probabilistic observation model, Fisher information may quantify local information about parameters.

For parameter vector \(\boldsymbol\theta\), denote

\[
\boxed{
\mathbf I_F(\boldsymbol\theta).
}
\]

A singular Fisher information matrix can indicate unidentifiable parameter directions under the declared statistical model.

When regularity conditions hold and the model is identifiable, the Cramér–Rao bound may provide a lower bound on covariance of unbiased estimators.

GeoDOA shall not use Fisher information/CRB without declaring:

- likelihood/noise model;
- deterministic versus stochastic source assumptions;
- nuisance parameters;
- gauge constraints;
- regularity assumptions;
- parameter units/scaling.

Fisher information is not a universal error metric.

---

## 31. Identifiability versus estimator bias

A parameter may be structurally identifiable yet estimated with substantial bias because of finite samples, model mismatch, regularization, local minima, or estimator approximation.

Conversely, a non-identifiable problem may return a stable-looking numerical solution because the optimizer or regularizer selects one representative of an equivalence family.

Therefore GeoDOA shall not infer identifiability from low empirical variance or optimizer repeatability.

---

## 32. Identifiability versus calibration reference choice

Choosing a reference channel, origin, phase reference, or normalization can remove a gauge degree of freedom from the numerical representation.

This makes a parameter vector unique under the chosen convention, but does not create new physical information.

GeoDOA shall distinguish

\[
\boxed{
\text{gauge fixing}
\neq
\text{new physical observability}.
}
\]

---

## 33. Source-dependent identifiability

A calibration parameter can be observable for one set of source states and unobservable for another.

Examples:

- one calibration direction observes only a projection of position error;
- one frequency cannot separate static phase from delay;
- one polarization cannot identify cross-polar response;
- one source level cannot characterize nonlinear compression coefficients robustly;
- one range may not separate certain near-field geometry effects.

Identifiability shall therefore be declared relative to calibration-experiment diversity.

---

## 34. Multi-parameter confounding

If two parameter perturbations produce similar first-order response changes,

\[
\mathbf J_{\theta_i}
\approx c\mathbf J_{\theta_j},
\]

they are locally confounded or poorly separable.

Relevant confounding families include:

- position phase versus electronic phase;
- delay versus phase over narrow frequency support;
- element amplitude versus receiver gain;
- embedded element response versus effective coupling;
- source angle versus geometry perturbation;
- source frequency versus LO frequency offset;
- common source phase versus common receiver phase.

GeoDOA shall preserve `unresolved/confounded` status where evidence does not support unique physical attribution.

---

## 35. Calibration metric must follow equivalence class

Before computing a manifold metric, the analysis shall declare one of at least:

```text
absolute physical comparison
common-phase equivalence
common-complex-scale equivalence
reference-channel gauge
normalized projective comparison
other explicitly defined gauge/equivalence class
```

The metric result is scientifically incomplete without this declaration.

---

## 36. Zero-vector and null-region policy

Projective metrics require nonzero vectors.

If

\[
\|\mathbf a\|_2=0
\quad\text{or}\quad
\|\mathbf b\|_2=0,
\]

then normalized coherence/projective angle is undefined.

GeoDOA shall return an explicit invalid/undefined metric state rather than NaN propagation silently treated as a large or small error.

Near-null vectors require quality thresholds and careful interpretation.

---

## 37. Weighted manifold metric

When channels have different relevance or uncertainty, a positive-semidefinite weighting matrix \(\mathbf W\) may define

\[
\boxed{
\|\mathbf x\|_{\mathbf W}^2
=\mathbf x^H\mathbf W\mathbf x.
}
\]

A weighted scale-aligned residual may be

\[
\boxed{
\min_c
(\mathbf b-c\mathbf a)^H
\mathbf W
(\mathbf b-c\mathbf a).
}
\]

The optimum, for \(\mathbf a^H\mathbf W\mathbf a>0\), is

\[
\boxed{
c^*
=\frac{\mathbf a^H\mathbf W\mathbf b}
{\mathbf a^H\mathbf W\mathbf a}.
}
\]

Weighting can encode noise precision, channel confidence, or engineering importance, but the interpretation must be explicit.

---

## 38. Noise-weighted/projective comparison

If downstream processing uses nonwhite noise covariance \(\mathbf R_n\succ0\), one possible geometry is the whitened space

\[
\boxed{
\bar{\mathbf a}
=\mathbf R_n^{-1/2}\mathbf a.
}
\]

A noise-weighted alignment can then compare \(\bar{\mathbf a}\) and \(\bar{\mathbf b}\).

This metric answers a different estimator-relevance question than ordinary Euclidean projective alignment and shall not replace the physical raw manifold metric.

---

## 39. Direction/frequency weighting is part of the metric

A broadband calibration metric may integrate over frequency with weights reflecting:

- uniform bandwidth;
- source spectrum;
- receiver passband;
- estimator-bin usage;
- operational prior.

A directional metric may weight uniformly in angle, direction cosine, solid angle, or application-specific prior.

GeoDOA shall record the weighting measure because the same pointwise errors can yield different aggregate scores.

---

## 40. Thresholds are profile-specific

There is no universal scientifically valid rule such as

```text
manifold error < 5% => calibrated
```

for all arrays, frequencies, apertures, SNRs, and DOA estimators.

Acceptable thresholds depend on:

- aperture/electrical size;
- source direction;
- number of sensors;
- SNR/noise covariance;
- source separation/correlation;
- estimator;
- calibration domain;
- required DOA accuracy/resolution;
- hardware/application tolerances.

GeoDOA shall therefore derive acceptance thresholds from validated profiles/requirements rather than hard-code generic scientific constants.

---

## 41. Metric monotonicity does not imply DOA monotonicity

A smaller global manifold norm error does not guarantee smaller DOA error in every condition.

Two mismatches can have equal norm but different projections onto DOA-sensitive tangent directions of the manifold.

Therefore 3.12 shall examine covariance/subspace consequences, and ADR-004 shall evaluate final DOA performance empirically/analytically under declared conditions.

---

## 42. Local manifold tangent and DOA-sensitive error

For scalar direction parameter \(\theta\), define local manifold tangent

\[
\boxed{
\mathbf a_{\theta}
=\frac{\partial\mathbf a}{\partial\theta}.
}
\]

A mismatch component parallel to the common complex-scale direction may be DOA-irrelevant for a projective estimator, while a mismatch component along the manifold tangent can resemble an angular shift.

This motivates later first-order DOA-bias analysis but does not establish a universal bias formula in 3.11.

---

## 43. Projective tangent concept

Because steering vectors may be equivalent up to common complex scale, the physically relevant tangent for normalized/projective DOA geometry is the component orthogonal to the steering vector:

\[
\boxed{
\mathbf a_{\theta,\perp}
=
\left(
\mathbf I-
\frac{\mathbf a\mathbf a^H}{\mathbf a^H\mathbf a}
\right)
\frac{\partial\mathbf a}{\partial\theta}.
}
\]

If this projected tangent is very small, nearby directions are difficult to distinguish in the normalized manifold geometry.

This is a geometric sensitivity concept, not a complete stochastic resolution bound.

---

## 44. Local angular equivalence of structured mismatch

For small scalar direction perturbation \(\Delta\theta\),

\[
\mathbf a(\theta+\Delta\theta)
\approx
\mathbf a(\theta)
+\mathbf a_{\theta}\Delta\theta.
\]

A structured calibration residual that projects strongly onto \(\mathbf a_{\theta,\perp}\) can therefore mimic a DOA change.

This provides the geometric interpretation behind the two-sensor position/gain-phase bias examples from 3.2/3.3.

---

## 45. Principal-angle terminology

For one-dimensional manifolds, the projective angle \(\alpha\) defined above is the principal angle between the two one-dimensional subspaces.

For multi-dimensional signal/eigenspaces, principal angles generalize this concept and are developed in 3.12.

GeoDOA shall not use `angle error` ambiguously for both physical DOA error and subspace principal angle.

---

## 46. Metric symmetry

Some metrics are symmetric:

\[
\rho(\mathbf a,\mathbf b)=\rho(\mathbf b,\mathbf a).
\]

Others, especially relative residuals normalized by a chosen reference norm, are not.

A metric report shall identify the reference/denominator semantics rather than assume symmetry.

---

## 47. Metric units

GeoDOA shall preserve dimensional meaning:

- position error: meters;
- delay error: seconds;
- frequency error: hertz;
- phase error: radians/degrees with explicit unit;
- amplitude ratio: dimensionless or dB;
- operator/manifold absolute residual: units inherited from response representation;
- normalized/projective metrics: dimensionless;
- projective/principal angle: radians/degrees with explicit unit.

Dimensionless normalization shall not be used to erase the underlying physical-unit error when both are useful.

---

## 48. Identifiability status as structured result

A future scientific result shall be capable of expressing more than true/false.

Conceptual statuses may include:

```text
identifiable under declared gauge
locally identifiable only
globally ambiguous
gauge-underdetermined
rank-deficient locally
weakly observable / ill-conditioned
unresolved due insufficient calibration diversity
not assessed
outside model validity
```

The exact software enum is deferred.

---

## 49. Conditioning status as structured result

Likewise, conditioning shall report diagnostics rather than one arbitrary Boolean.

Relevant quantities can include:

- singular values;
- scaled condition number;
- smallest observable singular value;
- parameter-direction sensitivity vectors;
- confidence/uncertainty inflation;
- regularization dependence.

Thresholds remain profile-specific.

---

## 50. Calibration residual attribution

A residual mismatch shall not automatically be attributed to the parameter family being calibrated.

For example, after fitting gain/phase mismatch, residual phase structure may be caused by position error, coupling, delay, reference-plane error, measurement bias, or interpolation.

GeoDOA shall distinguish:

\[
\boxed{
\text{residual observed mismatch}
}
\]

from

\[
\boxed{
\text{physically attributed residual cause}.
}
\]

Attribution requires an identifiable model/evidence.

---

## 51. Metric provenance

Every scientific error metric shall eventually preserve enough metadata to answer:

```text
reference object
test object
state/domain point(s)
reference plane
channel mapping
coordinate frame
frequency/range/polarization/state
alignment/equivalence rule
normalization
weighting
units
invalid/null handling
aggregation rule
interpolation model if applicable
uncertainty/confidence method
software/version provenance
```

A scalar number detached from these semantics is not a reproducible metric.

---

## 52. Initial Phase-1 metric profile

The ideal Phase-1 sensor profile can use deterministic reference comparisons such as:

- exact steering-vector agreement against hand calculation;
- translation-invariant/projective equality where appropriate;
- normalized inner product expected to equal one for identical declared models;
- covariance/eigenspace metrics from existing GRP seeds.

No empirical hardware calibration threshold is required for the initial ideal profile.

---

## 53. Boundary and failure conditions reserved for later gates

Error metrics/identifiability must later be stress-tested for at least:

- zero/near-zero reference vectors;
- null channels;
- missing channels;
- incompatible reference planes;
- mismatched channel order;
- mismatched coordinate frames;
- arbitrary grid-dependent gauge choices;
- wrapped phase discontinuities;
- undefined relative error at zero reference values;
- mixed units/scaling in Jacobians;
- false global-identifiability claims from local rank tests;
- full-rank but nearly singular sensitivity matrices;
- hidden gauge freedoms;
- source/calibration parameter confounding;
- insufficient direction/frequency/polarization diversity;
- non-Gaussian/nonregular cases where Fisher/CRB assumptions fail;
- parameter boundaries;
- multimodal likelihoods;
- nonlinear large-error regimes invalidating first-order propagation;
- fit-error overinterpretation;
- aggregation that hides local worst-case failures;
- weighting choices that change conclusions;
- thresholds transplanted between incompatible profiles;
- projective metrics used where absolute amplitude is required;
- absolute metrics used where common phase/scale is physically irrelevant.

These are exploration requirements, not Gate F PASS evidence.

---

## 54. Candidate decisions from Exploration 3.11

- **3.11-D1** — Parameter, operator, manifold, statistical, and estimator-output errors are distinct levels and shall not be collapsed into one generic error quantity.
- **3.11-D2** — Every error metric shall declare the reference and test scientific objects being compared.
- **3.11-D3** — Raw Euclidean manifold error preserves common phase/scale differences and is not universally DOA-relevant.
- **3.11-D4** — Phase-only alignment and common-complex-scale/projective alignment are distinct equivalence semantics.
- **3.11-D5** — The least-squares common complex scale is \(c^*=\mathbf a^H\mathbf b/(\mathbf a^H\mathbf a)\) for the declared \(\min_c\|\mathbf b-c\mathbf a\|^2\) problem.
- **3.11-D6** — Normalized coherence \(\rho=|\mathbf a^H\mathbf b|/(\|\mathbf a\|\|\mathbf b\|)\) is invariant to nonzero common complex scaling.
- **3.11-D7** — The projective angle \(\alpha=\cos^{-1}\rho\) and leakage \(1-\rho^2\) are first-class manifold-direction metrics.
- **3.11-D8** — For a rank-one reference signal subspace, \(1-\rho^2\) equals normalized energy of the test vector in the orthogonal/noise subspace.
- **3.11-D9** — GRP-016/017 coupling seeds are consistent with projective leakage \(0.2\) and shall be reconciled formally at Gate E.
- **3.11-D10** — Phase-only and projective metrics answer different questions when common amplitude scale differs.
- **3.11-D11** — Per-channel amplitude ratio/dB error and relative phase error require explicit null/low-amplitude handling.
- **3.11-D12** — Delay error shall preserve time units and phase-slope semantics rather than be reduced to one-frequency phase error.
- **3.11-D13** — Position error remains a physical vector in meters; wavelength-normalized and directional projections are derived diagnostics.
- **3.11-D14** — Gain/phase calibration quality should preserve separate amplitude and wrapped-phase metrics when engineering interpretation requires them.
- **3.11-D15** — Coupling/network matrix norms are meaningful only between identical physical matrix types/reference conditions.
- **3.11-D16** — Operator norm error and induced manifold error are distinct; one shall not substitute automatically for the other.
- **3.11-D17** — Domain aggregation requires explicit measure/weights; uniform angle, direction-cosine, solid-angle, and operational weighting are not interchangeable.
- **3.11-D18** — Mean calibration error shall be accompanied by distribution/worst-case/domain-location information where localized failure is relevant.
- **3.11-D19** — Calibration fit residual and held-out prediction error are distinct and shall not be conflated.
- **3.11-D20** — Repeatability/precision and physical accuracy/bias are distinct.
- **3.11-D21** — Error and uncertainty are distinct; exact physical error need not be known to report estimate uncertainty.
- **3.11-D22** — First-order Jacobian uncertainty propagation is a local approximation with explicit validity limits.
- **3.11-D23** — Identifiability is a property of the declared model/experiment modulo declared gauge freedoms, not of optimizer convergence.
- **3.11-D24** — Global and local identifiability are distinct; local full-rank sensitivity does not prove global uniqueness.
- **3.11-D25** — Known gauge freedoms shall be represented as observable equivalence classes rather than calibration failures.
- **3.11-D26** — Error metrics shall either be gauge invariant or declare the gauge fixed before comparison.
- **3.11-D27** — Local Jacobian rank after gauge handling is a valid local observability diagnostic under a differentiable model.
- **3.11-D28** — Raw mixed-unit Jacobian conditioning is parameterization/unit dependent and shall not be interpreted without declared scaling.
- **3.11-D29** — Full local rank does not imply good practical estimability; small singular values indicate weakly observed combinations.
- **3.11-D30** — Structural identifiability and numerical/statistical conditioning are distinct concepts.
- **3.11-D31** — Fisher information/CRB are permitted only under an explicitly declared probabilistic model, nuisance-parameter treatment, gauge constraints, and regularity assumptions.
- **3.11-D32** — A singular Fisher information matrix can diagnose unidentifiable directions under the declared statistical model but is not a universal metric.
- **3.11-D33** — Stable or low-variance numerical estimates do not prove identifiability.
- **3.11-D34** — Gauge fixing creates a unique representation but does not create new physical information.
- **3.11-D35** — Identifiability depends on calibration diversity/source state and may change with direction, frequency, polarization, range, and level.
- **3.11-D36** — Confounded physical causes shall remain unresolved when the experiment cannot distinguish them.
- **3.11-D37** — The equivalence/alignment class is part of every manifold metric definition.
- **3.11-D38** — Projective metrics are undefined for zero vectors and require explicit invalid/null handling.
- **3.11-D39** — Weighted metrics may encode noise precision, confidence, or engineering importance but must declare the weighting interpretation.
- **3.11-D40** — Noise-whitened manifold geometry and ordinary Euclidean manifold geometry answer different questions and shall remain distinct.
- **3.11-D41** — Frequency/direction weighting is part of a reported aggregate metric and must be reproducible.
- **3.11-D42** — No universal manifold-error threshold is accepted; acceptance tolerances are profile/application/estimator dependent.
- **3.11-D43** — Smaller global manifold norm error does not guarantee smaller DOA error under every condition.
- **3.11-D44** — Local manifold tangent geometry provides a DOA-sensitivity interpretation but is not by itself a stochastic performance bound.
- **3.11-D45** — Projecting the manifold tangent orthogonal to the steering vector isolates locally projective/DOA-relevant direction change under common-scale equivalence.
- **3.11-D46** — Structured sensor mismatch can mimic a small DOA shift when it projects onto the local manifold tangent.
- **3.11-D47** — `angle error` shall distinguish physical DOA angle error from subspace/projective principal angle.
- **3.11-D48** — Metric symmetry/normalization/reference denominator shall be explicit.
- **3.11-D49** — Physical-unit error and normalized dimensionless error may both be retained; normalization shall not destructively erase physical units.
- **3.11-D50** — Identifiability shall be reportable as structured status rather than one generic Boolean.
- **3.11-D51** — Conditioning shall preserve singular-value/scaling diagnostics rather than only one thresholded Boolean.
- **3.11-D52** — Residual mismatch and physical attribution of residual cause are distinct; attribution requires identifiable evidence.
- **3.11-D53** — Metric provenance shall preserve reference/test objects, state, plane, channel mapping, alignment, normalization, weighting, units, aggregation, and software lineage.
- **3.11-D54** — The initial ideal Phase-1 profile may use deterministic exact/projective reference metrics without hardware calibration thresholds.

---

## 55. Scientific anchors for this exploration

The contract is consistent with established array-calibration literature emphasizing that array self-calibration requires identifiability analysis and that calibrated-manifold accuracy can be evaluated using normalized inner-product/angle concepts in addition to raw norm residuals.

Representative anchors include:

- K. N. Ramamohan, S. P. Chepuri, D. Fernandez Comesana, and G. Leus, **Self-Calibration of Acoustic Scalar and Vector Sensor Arrays**, IEEE Transactions on Signal Processing, vol. 71, pp. 61–75, 2023, DOI: 10.1109/TSP.2022.3214383 — joint calibration/DOA estimation with explicit identifiability conditions.
- P. Comon and L. Deruaz, **Array Self Calibration: Identifiability Issues**, 1996 — local identifiability and remaining degrees of freedom in array self-calibration.
- B. Friedlander, **Calibration of antenna arrays using the extended manifold**, IET Radar, Sonar & Navigation, 2020 — calibrated-manifold accuracy assessed using both norm difference and angle/normalized inner product between manifold vectors.
- Classical statistical estimation theory for Jacobian sensitivity, Fisher information, nuisance parameters, and Cramér–Rao bounds under declared likelihood/regularity conditions.

These references support the scientific taxonomy; GeoDOA's exact metrics, gauges, weighting semantics, and acceptance thresholds remain project decisions subject to Gates A–F.

---

## 56. Immediate next step

The next work session shall start at **Exploration 3.12 — Covariance / Eigenspace / MUSIC Error Propagation**.

Exploration 3.12 must reconcile at least:

1. linear manifold/operator mismatch propagation into covariance;
2. first-order covariance perturbation;
3. additive versus structured covariance error;
4. eigenvalue perturbation;
5. eigengap dependence;
6. signal/noise-subspace principal angles;
7. Davis–Kahan/Wedin-type perturbation concepts and their assumptions;
8. rank-preserving versus rank-changing sensor transforms;
9. colored/unequal noise and whitening;
10. mismatch leakage into MUSIC noise subspace;
11. calibrated-model versus corrected-data covariance paths;
12. time-varying sensor operators across covariance windows;
13. I/Q widely-linear augmented covariance implications;
14. nonlinear/quantized covariance propagation limits;
15. finite-sample covariance error versus deterministic sensor-model error;
16. source correlation/coherence interactions;
17. first-order MUSIC pseudospectrum/peak consequences;
18. linkage to GRP-016/017 and later Gate-E evidence.

Do not start Gate A yet.
