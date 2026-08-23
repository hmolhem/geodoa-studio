# ADR-004 Exploration 4.14 — Multi-Level Scientific Error Metrics

- **ADR:** ADR-004 — Validation, Reproducibility, and Scientific Evidence
- **Phase:** 0C — Scientific Foundations
- **Exploration:** 4.14
- **Status:** EXPLORATION COMPLETE — CANDIDATE CONTRACT, NOT ACCEPTED
- **Depends on:** Accepted ADR-001, ADR-002, ADR-003; ADR-004 Explorations 4.1–4.13

## 1. Question

> Which scientific error metrics shall GeoDOA use at the manifold, covariance, eigenvalue/eigenspace, spectrum, detection, and final-DOA levels so that upstream numerical/model mismatch can be diagnosed before it is collapsed into one terminal RMSE value?

This exploration defines a multi-level diagnostic contract for scientific verification, implementation cross-validation, sensor-model studies, and algorithm failure analysis.

---

## 2. Core Principle

A final DOA error is an end-to-end consequence, not a complete diagnosis.

Candidate diagnostic chain:

```text
geometry / sensor / signal state
        ↓
manifold error
        ↓
covariance error
        ↓
eigenvalue / eigenspace error
        ↓
spectrum / objective error
        ↓
peak / detection / association error
        ↓
final DOA error
```

Candidate rule:

> GeoDOA shall preserve scientifically meaningful error metrics at intermediate levels rather than relying only on final localization RMSE.

No single metric is sufficient for all levels.

---

## 3. Reference Object Must Be Declared at Every Level

For any metric, GeoDOA must identify:

```text
quantity being compared
reference/truth role
units / normalization
coordinate / basis / gauge
conditioning variables
metric formula
eligibility policy
```

Examples:

- `a_nom` versus `a_phys`;
- `R_hat` versus `R_phys`;
- estimated signal subspace versus reference signal subspace;
- fixed-point spectrum versus floating-point reference spectrum;
- estimated DOA set versus generative truth set.

Candidate rule:

> A metric value without a typed reference object is scientifically incomplete.

---

## 4. Raw Norm Error Is Useful but Not Gauge-Invariant

For vectors `a` and `b`, a raw relative error may be

\[
\epsilon_{raw}
=
\frac{\|b-a\|_2}{\|a\|_2}.
\]

This is useful when absolute complex scale and phase are scientifically meaningful.

But if common complex phase is a gauge, raw norm error can report a large discrepancy even when the two steering vectors define the same spatial subspace.

Candidate rule:

> Raw norm metrics shall be used only when their gauge sensitivity matches the scientific question.

---

## 5. Common-Phase-Invariant Manifold Error

For steering vectors where common phase is nonphysical under the declared comparison, define

\[
\epsilon_{\phi}
=
\min_{\phi}
\frac{\|b-e^{j\phi}a\|_2}{\|a\|_2}.
\]

Candidate rule:

> Phase-invariant manifold comparison is preferred when ADR-001 declares common phase to be a gauge for the quantity being assessed.

The minimizing phase shall not be interpreted as a calibration parameter unless the experiment explicitly treats it as such.

---

## 6. Complex-Scale-Invariant Manifold Error

When both common amplitude and common phase are nuisance gauges, use complex least-squares scale

\[
c^*
=
\frac{a^H b}{a^H a}
\]

and residual

\[
\epsilon_c
=
\frac{\|b-c^*a\|_2}{\|b\|_2}
\]

or another declared normalization.

Candidate rule:

> Common phase and common complex scale are different gauge choices; GeoDOA shall declare which one is removed.

---

## 7. Manifold Correlation / Projective Similarity

Define normalized complex correlation

\[
\rho(a,b)
=
\frac{|a^H b|}{\|a\|_2\,\|b\|_2}.
\]

Then

\[
0\le \rho\le 1.
\]

A projective angle is

\[
\alpha
=
\cos^{-1}(\rho).
\]

For normalized vectors `u` and `v`, projection leakage is

\[
d_{proj}^2
=1-\rho^2
=\|P_u^\perp v\|_2^2.
\]

Candidate rule:

> `rho`, projective angle, and projection leakage are strong gauge-invariant diagnostics for rank-one steering-manifold mismatch.

This inherits the accepted ADR-003 identifiability/manifold results.

---

## 8. Weighted / Whitened Manifold Error

If noise covariance `R_n` is colored and known/declared, ordinary Euclidean geometry may not be the most relevant comparison geometry.

Define whitened manifold

\[
\bar a=R_n^{-1/2}a.
\]

Then projective or norm-based metrics may be computed in whitened coordinates.

Candidate rule:

> Whitened and unwhitened manifold metrics are distinct; the chosen noise metric space shall be declared.

No silent whitening is allowed.

---

## 9. Per-Sensor Magnitude and Phase Diagnostics

Aggregate manifold metrics can hide localized channel defects.

Useful diagnostics include:

\[
\Delta m_n = 20\log_{10}\frac{|b_n|}{|a_n|},
\]

and, after declared gauge alignment,

\[
\Delta\phi_n
=
\arg(b_n)-\arg(a_n).
\]

Candidate rule:

> GeoDOA should preserve channel-resolved manifold diagnostics alongside aggregate manifold metrics when sensor/model mismatch is being investigated.

---

## 10. Manifold Error over Direction/Frequency

A manifold is often a function

\[
a(\theta,f,\ldots).
\]

Therefore error may be a field:

\[
\epsilon_a(\theta,f).
\]

Candidate rule:

> Domain-resolved manifold error shall be preserved when mismatch is angle/frequency/state dependent; one global average shall not replace localized structure without an explicit weighting distribution.

---

## 11. Covariance Matrix Error

For reference covariance `R` and compared covariance `\widetilde R`, define

\[
E_R=\widetilde R-R.
\]

Candidate absolute metrics include

\[
\|E_R\|_F,
\qquad
\|E_R\|_2.
\]

A relative Frobenius metric is

\[
\epsilon_{R,F}
=
\frac{\|\widetilde R-R\|_F}{\|R\|_F}.
\]

Candidate rule:

> Covariance error metrics shall state whether the comparison is population-to-population, sample-to-population, sample-to-sample, or implementation-to-reference.

These are different evidence objects.

---

## 12. Population Model Error versus Finite-Sample Covariance Error

ADR-003 distinguished

\[
E_{sensor}=R_{phys}-R_{nom}
\]

from

\[
E_{sample}=\hat R-R_{phys}.
\]

Candidate rule:

> GeoDOA shall preserve deterministic/model covariance mismatch separately from finite-sample covariance estimation error.

Otherwise a sensor/model defect may be confused with ordinary snapshot variability.

---

## 13. Hermitian and PSD Diagnostics

A covariance-like matrix should be assessed for structural validity where the profile requires it.

Hermitian residual:

\[
\epsilon_H
=
\frac{\|R-R^H\|_F}{\|R\|_F}.
\]

PSD diagnostics may include:

```text
minimum eigenvalue
negative-eigenvalue magnitude beyond tolerance
PSD projection distance, if such projection is explicitly used
```

Candidate rule:

> Structural covariance diagnostics are validity checks, not replacements for scientific covariance-error metrics.

Silent PSD projection or Hermitian symmetrization shall be treated as a transform with provenance.

---

## 14. Trace / Power Diagnostics

If total covariance power is meaningful,

\[
\operatorname{tr}(R)
\]

can diagnose power mismatch.

Candidate relative trace discrepancy:

\[
\epsilon_{tr}
=
\frac{|\operatorname{tr}(\widetilde R)-\operatorname{tr}(R)|}{|\operatorname{tr}(R)|}.
\]

Candidate rule:

> Trace agreement does not imply covariance agreement; it is only a complementary power diagnostic.

---

## 15. Eigenvalue Error

Let ordered eigenvalues be

\[
\lambda_1\ge\lambda_2\ge\cdots\ge\lambda_N.
\]

Candidate diagnostics:

\[
\Delta\lambda_i
=
\tilde\lambda_i-\lambda_i,
\]

\[
\epsilon_{\lambda,i}
=
\frac{|\tilde\lambda_i-\lambda_i|}{\max(|\lambda_i|,\epsilon_{scale})}.
\]

Candidate rule:

> Relative eigenvalue error near zero requires a declared scale/floor; no bare relative error is accepted universally.

Eigenvalue ordering/tie conventions must be declared near degeneracy.

---

## 16. Eigengap Diagnostics

For signal/noise separation at model order `K`, define

\[
\delta_K
=
\lambda_K-\lambda_{K+1}.
\]

Candidate diagnostics include:

```text
absolute eigengap
relative eigengap
estimated-versus-reference eigengap error
condition-dependent eigengap distribution
```

Candidate rule:

> Eigenspace sensitivity shall be interpreted together with relevant eigengaps; small matrix error can still produce large eigenvector/subspace rotation when the gap is small.

---

## 17. Individual Eigenvector Error Is Not Always Identifiable

When eigenvalues are repeated or nearly repeated, individual eigenvectors can rotate within an invariant subspace without changing the scientific subspace.

Candidate rule:

> GeoDOA shall not use individual eigenvector difference as the authoritative metric when the scientific object is an eigenspace or when eigenvectors are non-unique up to phase/rotation.

Subspace metrics are preferred.

---

## 18. Subspace Projector Error

Let `U_s` and `\widetilde U_s` span reference and compared signal subspaces.

Define projectors

\[
P_s=U_sU_s^H,
\qquad
\widetilde P_s=\widetilde U_s\widetilde U_s^H.
\]

Candidate metrics include

\[
\|\widetilde P_s-P_s\|_F
\]

and

\[
\|\widetilde P_s-P_s\|_2.
\]

Candidate rule:

> Projector metrics are basis-rotation invariant and are preferred when the subspace—not the chosen eigenvector basis—is the scientific object.

---

## 19. Principal Angles

Let singular values of

\[
U_s^H\widetilde U_s
\]

be

\[
\sigma_i=\cos\psi_i.
\]

Then `psi_i` are principal angles between the subspaces.

Useful summaries include:

```text
max principal angle
RMS principal angle
sin(theta) norm
full principal-angle vector
```

Candidate rule:

> Principal-angle metrics are the preferred interpretable eigenspace-rotation diagnostics for equal-dimensional subspaces.

---

## 20. Unequal-Dimension Subspaces

If model-order estimates differ, signal/noise subspaces may have unequal dimensions.

Candidate rule:

> GeoDOA shall not silently compare unequal-dimensional subspaces using a metric that assumes equal rank.

The dimension mismatch itself is evidence and may require containment/chordal/generalized projector metrics or a typed model-order mismatch state.

No one universal unequal-rank metric is accepted here.

---

## 21. Davis–Kahan / Perturbation Interpretation

Perturbation theory motivates the qualitative relation

\[
\text{subspace rotation}
\sim
\frac{\|E_R\|}{\text{eigengap}}
\]

under appropriate conditions.

Candidate rule:

> Perturbation bounds may support diagnosis but shall not be used outside their theorem assumptions or presented as exact empirical error predictions.

The exact theorem/bound used must be cited in future formal theory artifacts.

---

## 22. MUSIC Orthogonality Diagnostic

For a reference steering vector `a(theta0)` and estimated noise-subspace projector `P_n`, define

\[
\eta_{MUSIC}(\theta_0)
=
\frac{a^H(\theta_0)P_n a(\theta_0)}{a^H(\theta_0)a(\theta_0)}.
\]

Under an ideal matched population model, this is zero at a true source direction.

Candidate rule:

> Noise-subspace leakage at truth is a direct diagnostic distinct from the final peak-location error.

---

## 23. Rank-One MUSIC and Manifold Correlation

For a single-source rank-one setting with normalized true and searched steering vectors, the ideal MUSIC denominator can be related to projective mismatch:

\[
D_{MUSIC}
=1-\rho^2.
\]

Candidate rule:

> GeoDOA may use this relation as an interpretive bridge between manifold mismatch and idealized MUSIC spectral degradation when the rank-one assumptions hold.

It shall not be generalized silently to arbitrary multi-source finite-sample cases.

---

## 24. Spectrum-Level Comparison Requires Normalization Semantics

A pseudospectrum may be compared in linear power, magnitude, inverse denominator, normalized peak scale, or dB.

Candidate rule:

> Spectrum-error metrics shall declare the exact spectrum representation and normalization before numerical comparison.

A spectrum normalized independently to unit peak can conceal absolute amplitude/denominator differences.

---

## 25. Linear-Spectrum Error

For spectra sampled on common grid `theta_g`, candidate metrics include

\[
\epsilon_{P,2}
=
\frac{\|\widetilde P-P\|_2}{\|P\|_2},
\]

or discrete weighted norms

\[
\epsilon_{P,w}^2
=
\sum_g w_g|\widetilde P_g-P_g|^2.
\]

Candidate rule:

> Spectrum norm errors require a common grid/domain or an explicit interpolation/regridding transform with provenance.

---

## 26. dB-Spectrum Error Requires a Floor

For

\[
P_{dB}=10\log_{10}P,
\]

values near zero require a declared floor.

Candidate rule:

> dB-spectrum error shall declare the floor/clipping policy; different floors can materially change aggregate error metrics.

No universal floor is accepted globally.

---

## 27. Spectrum Shape Diagnostics

Useful shape-level diagnostics may include:

```text
peak locations
peak heights/prominences
mainlobe width
valley depth between designated peaks
sidelobe maxima
integrated error over region
correlation after declared normalization
```

Candidate rule:

> Spectrum topology/shape metrics are diagnostic features and shall not be conflated automatically with truth-based resolution success.

This preserves Exploration 4.8.

---

## 28. Peak Location Error versus Spectrum Error

Two spectra can have large global norm difference yet identical peak locations.

Conversely, small global norm error can move a sharp peak enough to change final DOA.

Candidate rule:

> Spectrum-level and peak-location metrics answer different questions and should be reported together when diagnosing implementation/model perturbations.

---

## 29. Local Curvature / Peak Sensitivity

Near a well-defined isolated maximum, peak shift depends on local slope/curvature perturbations rather than only global spectrum norm.

Candidate rule:

> Local peak-shift approximations may be used as bounded diagnostics when differentiability, isolated-peak, and small-perturbation assumptions are declared.

No universal first-order peak-shift formula is accepted for all algorithms or failure regimes.

---

## 30. DOA-Level Metrics

Final DOA metrics inherit Explorations 4.6–4.9:

```text
signed error
bias
variance
MSE / RMSE
absolute error
quantiles
matched coverage
P_D / P_M
spurious detection metrics
P_res
catastrophic-error rate
```

Candidate rule:

> Final localization metrics remain the terminal performance outputs, but intermediate metrics are required for causal diagnosis and implementation cross-validation.

---

## 31. Set-Level DOA Metrics beyond One-to-One RMSE

Future studies with uncertain cardinality may require set distances such as assignment-based costs or bounded set metrics.

Candidate rule:

> Set-level metrics may complement typed miss/false-detection accounting, but shall not erase cardinality mismatch or replace the accepted association/event semantics without a dedicated contract.

No universal OSPA/Hausdorff-like metric is accepted in this exploration.

---

## 32. Error Propagation Is Not Necessarily Monotonic

Larger upstream error does not always imply larger final DOA error trial-by-trial.

For example:

- common phase can create raw manifold error but no DOA distortion;
- covariance perturbation may align benignly with insensitive eigendirections;
- small eigenspace perturbation near a flat/ambiguous spectrum can create a large peak jump.

Candidate rule:

> Multi-level metrics diagnose sensitivity and failure mechanism; they shall not assume a universal monotonic mapping from upstream norm error to downstream DOA error.

---

## 33. Gauge Alignment Must Precede Error Computation Where Required

Possible gauges include:

```text
common complex phase
common complex scale
subspace basis rotation
eigenvector phase/sign
source permutation
rigid translation-induced common receive phase
```

Candidate rule:

> GeoDOA shall remove only scientifically declared nuisance gauges before computing a gauge-invariant metric; no silent normalization/alignment is allowed.

The alignment transformation itself is provenance.

---

## 34. Units and Dimensionless Metrics

Examples:

```text
manifold projective angle -> rad/deg
covariance Frobenius error -> covariance units unless normalized
eigenvalue error -> signal-power units
principal angle -> rad/deg
DOA RMSE -> rad/deg
normalized correlations/projector leakage -> dimensionless
```

Candidate rule:

> Metric units/dimensionality shall be explicit; dimensionless normalization shall not be assumed merely because a metric is numerically between 0 and 1.

---

## 35. Absolute versus Relative Error

Relative error is useful for scale invariance but unstable near zero references.

Candidate rule:

> GeoDOA shall permit absolute, relative, or hybrid metrics depending on scale, but the denominator/floor policy must be declared.

No generic `relative_error = abs(err)/abs(ref)` is accepted near zero without safeguards.

---

## 36. Domain Weighting

If manifold/spectrum error is integrated across angle or frequency, weighting defines the scientific target.

Examples:

```text
uniform theta weighting
uniform direction-cosine weighting
deployment-prior weighting
source-conditioned weighting
frequency-band weighting
```

Candidate rule:

> Integrated error across a domain shall declare the integration coordinate and weights; uniform in `theta` is not equivalent to uniform in `u=sin(theta)`.

---

## 37. Reference Grid / Interpolation Error

Comparing external CST/measured manifolds or spectra on different grids may require interpolation.

Candidate rule:

> Interpolation error and grid mismatch shall be distinguished from the scientific object mismatch whenever materially possible.

Interpolation coordinate, method, extrapolation policy, and grid identity are provenance.

---

## 38. Tolerance versus Metric

A metric answers `how different?`.

A tolerance answers `is that difference acceptable for this claim?`.

Candidate rule:

> Metric definitions and acceptance thresholds shall remain separate.

For example:

```text
projector error = 2e-4
```

is not a PASS/FAIL statement until a profile-specific tolerance is declared.

---

## 39. Deterministic versus Statistical Metric Evidence

For a deterministic GRP or float/fixed vector comparison, the metric may be exact for that test case.

For Monte Carlo trials, metric values form random variables requiring aggregate uncertainty.

Candidate rule:

> The same mathematical metric can produce deterministic or stochastic evidence depending on the experiment; the evidence class shall be declared.

---

## 40. Multi-Level Error Tables

A useful cross-validation record may contain, per trial/condition:

```text
manifold_projective_error
covariance_relative_frobenius_error
max_eigenvalue_error
min_relevant_eigengap
max_principal_angle
projector_error
MUSIC_truth_leakage
spectrum_error
peak_location_error
matched_DOA_error
resolution_status
failure_status
```

Candidate rule:

> Multi-level metrics should remain joinable by stable trial/condition identities to support failure-mechanism analysis.

---

## 41. Causal Attribution Requires Controlled Experiments

Correlation between an upstream metric and final DOA error does not prove causation.

Candidate rule:

> Claims that a specific mechanism caused performance degradation require controlled perturbation, derivation, intervention, or otherwise justified causal evidence—not only metric correlation.

This is important for sensor-imperfection studies.

---

## 42. One-Factor Perturbation Studies

For mechanism isolation, GeoDOA may compare:

```text
nominal reference
+ position error only
+ gain/phase error only
+ coupling only
+ timing error only
+ quantization only
```

while controlling all other declared factors.

Candidate rule:

> One-factor studies are diagnostic tools; combined-realism studies remain necessary when interaction/noncommutativity matters.

ADR-003 already established that sensor operators may not commute.

---

## 43. Interaction Effects

If two perturbations are present, total degradation need not equal the sum of individual degradations.

Candidate rule:

> GeoDOA shall not assume additive error attribution for nonlinear pipelines, coupling between perturbations, or noncommuting sensor operators.

Interaction studies may require factorial or controlled multi-factor designs.

---

## 44. Model-Level versus Implementation-Level Metric Use

Examples:

### Scientific model validation

```text
measured manifold vs model manifold
measured covariance vs predicted covariance
DOA vs external physical reference
```

### Implementation verification

```text
Python manifold vs analytical reference
float covariance vs fixed-point covariance
Python eigenspace vs HLS/RTL eigenspace
float spectrum vs FPGA spectrum
```

Candidate rule:

> The same metric name shall carry evidence-role provenance so numerical agreement is not mislabeled physical validation.

---

## 45. Fixed-Point / FPGA Diagnostic Relevance

For downstream hardware cross-validation, the multi-level chain provides failure localization:

```text
input/sample mismatch?
      ↓
covariance mismatch?
      ↓
eigenstructure mismatch?
      ↓
spectrum mismatch?
      ↓
peak/event mismatch?
      ↓
DOA mismatch?
```

Candidate rule:

> Float/fixed/FPGA validation should compare the earliest scientifically meaningful internal states available, not only final DOA output.

Detailed policy is deferred to Exploration 4.15.

---

## 46. Computational Metrics Are Not Scientific Error Metrics

Runtime, latency, throughput, II, memory, LUT, FF, DSP, BRAM, URAM, power, and energy are engineering metrics.

Candidate rule:

> Computational/hardware metrics shall remain separate from scientific-error metrics, although both may enter a Pareto comparison.

This preserves Exploration 4.12.

---

## 47. Candidate Phase-1 Metric Set

For the initial Phase-1 narrowband 1-D DOA profile, a conservative candidate diagnostic set is:

### Manifold

```text
raw relative L2 error when absolute gauge matters
phase- or complex-scale-aligned relative error when gauge removal is declared
rho / projective angle / projection leakage
per-channel magnitude/phase residuals
```

### Covariance

```text
relative Frobenius error
Hermitian residual
minimum eigenvalue / PSD diagnostic
trace/power discrepancy
```

### Eigenstructure

```text
eigenvalue differences
relevant eigengap
projector norm difference
principal angles
```

### MUSIC / spectrum

```text
truth-direction noise-subspace leakage
common-grid spectrum error with declared normalization
peak locations/prominence/topology diagnostics
```

### Final estimator

```text
association/miss/spurious outcomes
bias / MSE / RMSE
P_D / P_res
failure-state record
```

This remains candidate until ADR-004 acceptance.

---

## 48. Invalid / Weak Metric Practices

The following are scientifically weak or invalid unless explicitly justified:

1. report only final RMSE while claiming a specific failure mechanism;
2. compare steering vectors by raw norm while common phase is a declared gauge;
3. silently phase-align/normalize one method but not another;
4. compare individual eigenvectors under repeated/near-repeated eigenvalues and call basis rotation an error;
5. compare unequal-dimensional subspaces with an equal-rank metric without disclosure;
6. use relative error with a zero/near-zero denominator and no floor/scale policy;
7. normalize each spectrum independently to unit peak and then claim absolute spectrum agreement;
8. compute dB error without declaring the floor;
9. compare spectra on different grids with silent interpolation;
10. infer physical validation from float-vs-fixed covariance agreement;
11. infer causality from correlation between covariance error and DOA RMSE alone;
12. assume larger upstream norm error always causes larger DOA error;
13. aggregate error uniformly in angle and describe it as uniform in spatial frequency;
14. treat trace agreement as covariance agreement;
15. treat one accepted tolerance as a universal threshold across all profiles.

---

## 49. Cross-ADR Reconciliation

### ADR-001

Gauge, phase reference, coordinate system, `theta`/`u`, stable channel identity, and no-silent-normalization rules govern manifold and DOA metrics.

### ADR-002

Population versus sample covariance, source/noise statistics, rank, snapshots, and signal/noise subspaces govern covariance/eigenstructure metrics.

### ADR-003

Accepted manifold mismatch, covariance perturbation, projective similarity, eigengap sensitivity, projector leakage, colored-noise whitening, and MUSIC mismatch relations are directly reused here.

### ADR-004 Explorations 4.2–4.3

Each metric requires a typed reference object and accepted deterministic evidence role.

### ADR-004 Explorations 4.6–4.9

Final DOA/detection/resolution metrics inherit association and event semantics.

### ADR-004 Explorations 4.10–4.13

Aggregate metrics require adequacy/uncertainty evidence and preserve typed failures rather than filtering them away.

**Cross-ADR result: no contradiction identified.**

---

## 50. Candidate Decisions from Exploration 4.14

- **D4.14-01:** GeoDOA shall preserve scientific error metrics at manifold, covariance, eigenvalue/eigenspace, spectrum, and final-DOA levels.
- **D4.14-02:** Every metric requires a declared reference role, coordinate/basis/gauge, units, normalization, and eligibility policy.
- **D4.14-03:** Raw manifold norm error is gauge-sensitive; phase- and complex-scale-invariant metrics shall be used when those gauges are scientifically irrelevant.
- **D4.14-04:** Normalized manifold correlation `rho`, projective angle, and projection leakage are canonical candidate gauge-invariant rank-one manifold diagnostics.
- **D4.14-05:** Whitened and unwhitened manifold metrics are distinct and require declared noise geometry.
- **D4.14-06:** Population/model covariance mismatch and finite-sample covariance error shall remain separate evidence objects.
- **D4.14-07:** Covariance diagnostics include matrix norm error plus structural Hermitian/PSD/power checks; structural checks do not replace error metrics.
- **D4.14-08:** Eigenvalue error, relevant eigengap, projector error, and principal angles are distinct eigenstructure diagnostics.
- **D4.14-09:** Individual eigenvector error is not authoritative when eigenvectors are non-unique; subspace/projector metrics are preferred.
- **D4.14-10:** Unequal subspace dimension/model order is itself evidence and shall not be hidden inside an equal-rank metric.
- **D4.14-11:** MUSIC truth-direction leakage is a direct subspace/manifold diagnostic distinct from final peak-location error.
- **D4.14-12:** Spectrum metrics require explicit representation, normalization, grid, floor, interpolation, and weighting semantics.
- **D4.14-13:** Spectrum error, peak topology, peak location, and truth-based resolution are distinct evidence levels.
- **D4.14-14:** Final DOA metrics remain terminal performance metrics but are insufficient alone for failure-mechanism attribution.
- **D4.14-15:** Gauge alignment transformations shall be explicit provenance and remove only declared nuisance degrees of freedom.
- **D4.14-16:** Absolute, relative, normalized, and domain-integrated metrics require scale/denominator/weighting contracts.
- **D4.14-17:** Multi-level metrics shall remain linked by stable trial/condition identities for diagnosis.
- **D4.14-18:** Correlation between upstream and downstream errors does not establish causation; controlled perturbation evidence is required for causal mechanism claims.
- **D4.14-19:** Combined perturbations need not be additive because sensor operators and downstream algorithms may be nonlinear/noncommutative.
- **D4.14-20:** The same numerical metric may support verification or validation depending on the reference/evidence role; the role shall be explicit.
- **D4.14-21:** Float/fixed/FPGA cross-validation should compare earliest available scientifically meaningful internal states, not only final DOA output.
- **D4.14-22:** Scientific-error metrics and computational/hardware metrics remain separate axes of engineering evidence.

---

## 51. Exploration 4.14 Conclusion

Exploration 4.14 is complete at candidate-contract level.

The central rule is:

> GeoDOA shall diagnose scientific discrepancy through a multi-level metric chain—from manifold to covariance to eigenstructure to spectrum to detection/association to final DOA—using reference-aware, gauge-aware, unit-aware, and domain-aware metrics; final localization error alone shall not be treated as sufficient evidence for mechanism attribution, numerical equivalence, or physical validity.

No acceptance gate is started or passed by this exploration.

The next exploration is:

```text
4.15 — Floating-Point, Fixed-Point, and FPGA Cross-Validation
```
