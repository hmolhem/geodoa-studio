# ADR-003 Exploration 3.14 — Cross-Section Reconciliation and Candidate ADR-003 Contract

- **Phase:** 0C — Scientific Foundations
- **Status:** EXPLORATION COMPLETE — CANDIDATE CONTRACT RECONCILED, NOT ACCEPTED
- **Parent ADR:** ADR-003 — Sensor Imperfections, Mutual Coupling, and Calibration
- **Branch:** `docs/phase0c-scientific-conventions`
- **Depends on:** Accepted ADR-001, Accepted ADR-002, ADR-003 Explorations 3.1–3.13
- **Acceptance gates:** Not started

> This document is the final exploration-stage reconciliation for ADR-003. It does not accept ADR-003. It establishes whether Explorations 3.1–3.13 are internally consistent enough to draft the governing ADR and then begin the standard Gates A–F sequence.

---

## 1. Reconciliation objective

Explorations 3.1–3.13 deliberately separated physical cause, manifold effect, measurement-chain effect, calibration, uncertainty, covariance propagation, eigenspace distortion, estimator compatibility, and Phase-1 scope.

Exploration 3.14 asks one final pre-draft question:

> Do the candidate contracts from 3.1–3.13 form one physically, mathematically, and semantically coherent sensor-imperfection model that remains consistent with accepted ADR-001 and ADR-002?

The reconciliation result is:

\[
\boxed{
\text{No blocking scientific contradiction was found across ADR-001/002 and ADR-003 Explorations 3.1–3.13.}
}
\]

Several wording, notation, domain, and profile nuances require explicit normalization in the governing ADR draft. Those reconciliations are recorded below.

This status means **ready to draft ADR-003**, not ready to accept ADR-003 and not yet ready to claim any Gate PASS.

---

## 2. Governing inherited conventions

ADR-003 shall inherit, not redefine, the accepted ADR-001/ADR-002 conventions.

### 2.1 Temporal phasor

\[
\boxed{e^{-j\omega t}}
\]

is the scientific temporal phasor convention.

### 2.2 Look and propagation direction

\[
\boxed{
\hat{\mathbf u}
=\text{array-to-source look direction}
}
\]

and

\[
\boxed{
\hat{\mathbf k}_{\rm prop}=-\hat{\mathbf u}
}
\]

for the incident propagation direction.

### 2.3 Nominal geometry-only receive manifold

\[
\boxed{
 a_n(\hat{\mathbf u},f)
 =
 \exp\!\left[-jk(\mathbf r_n-\mathbf r_{\rm ref})^T\hat{\mathbf u}\right]
}
\]

with

\[
 k=\frac{2\pi f}{v}.
\]

### 2.4 Canonical 1-D angular slice

\[
\boxed{
\hat{\mathbf u}(\theta)
=\begin{bmatrix}\sin\theta\\\cos\theta\\0\end{bmatrix},
\qquad
\theta\in[-\pi/2,\pi/2]
}
\]

with broadside \(\theta=0\) toward \(+y\), positive angle toward \(+x\).

### 2.5 Physical delay convention

A physical waveform delay

\[
x(t-\tau)
\]

has frequency-domain factor

\[
\boxed{e^{+j\omega\tau}}
\]

under the accepted Fourier/phasor convention.

### 2.6 Snapshot/covariance semantics

ADR-003 shall inherit ADR-002 distinctions among simultaneous-equivalent snapshots, covariance, second moment, centered sample covariance, source covariance rank, observed signal-subspace rank, physical source count, and sample rank.

---

## 3. Canonical ADR-003 scientific chain

The fully reconciled chain is

```text
scene / source state
    ↓
propagation evaluated on declared physical geometry
    ↓
element / polarization / open-circuit response
    ↓
port loading / mutual coupling / cross-channel network response
    ↓
analog receiver transfer: gain / phase / delay / filtering / LO / IQ
    ↓
receiver-noise injections at their physical stages
    ↓
analog nonlinear effects when active
    ↓
physical sampling epochs / aperture effects
    ↓
ADC range / clipping / quantization / code mapping
    ↓
digital measurement
    ↓
optional digital selection / deskew / calibration correction / DSP
    ↓
covariance / eigenspace / estimator
```

Calibration is associated with this physical chain but is not inserted retroactively as a physical cause.

The parallel calibration chain is

```text
calibration experiment / reference / model
    ↓
characterization and/or parameter/manifold estimation
    ↓
calibrated processing model and/or data correction
    ↓
residual mismatch + uncertainty + validity domain
    ↓
post-calibration covariance / eigenspace / DOA consequences
```

---

## 4. Reconciled manifold taxonomy

The following meanings are retained as distinct:

\[
\boxed{
\mathbf a_{\rm nom},
\mathbf a_{\rm phys},
\mathbf a_{\rm meas},
\mathbf a_{\rm em},
\mathbf a_{\rm cal}
}
\]

and, only in explicitly declared simulations,

\[
\boxed{\mathbf a_{\rm truth}}.
\]

The governing interpretations are:

- \(\mathbf a_{\rm nom}\): response predicted by nominal geometry/assumptions;
- \(\mathbf a_{\rm phys}\): actual physical deterministic coherent response for a declared physical state;
- \(\mathbf a_{\rm meas}\): experimental estimate of physical response;
- \(\mathbf a_{\rm em}\): EM/full-wave numerical prediction under declared simulation conditions;
- \(\mathbf a_{\rm cal}\): response deliberately supplied to processing after calibration/model construction;
- \(\mathbf a_{\rm truth}\): exact simulation truth only when the simulation defines such an object.

Neither measured nor CST/EM response is automatically relabeled physical truth.

---

## 5. Reconciliation: nominal geometry versus physical geometry

Exploration 3.2 is consistent with ADR-001 by preserving the nominal declared phase-center positions while introducing physical positions as

\[
\boxed{
\mathbf r_n^{\rm phys}
=\mathbf r_n^{\rm nom}+\boldsymbol\varepsilon_n.
}
\]

The governing resolution is:

1. nominal geometry remains the design/reference geometry;
2. physical geometry remains a separate realized state;
3. calibrated geometry is an estimate of physical geometry and shall not overwrite nominal provenance;
4. exact path evaluation precedes far-field phase-error approximations;
5. common rigid translation is not a far-field relative-manifold distortion;
6. pose/frame error, internal deformation, element orientation, and EM phase-center behavior remain separate causes.

No contradiction is present with ADR-001's stable phase-reference semantics.

---

## 6. Reconciliation: geometry phase versus electronic phase

An observed phase difference may arise from multiple physical causes.

The governing distinctions are:

### Geometry-derived phase

\[
\boxed{
\delta\phi_n
\approx
-k\hat{\mathbf u}^T
(\boldsymbol\varepsilon_n-\boldsymbol\varepsilon_{\rm ref})
}
\]

under the far-field narrowband approximation.

It is direction- and frequency-dependent because it originates from physical path change.

### Electronic static phase

\[
\boxed{
g_n=\rho_ne^{j\phi_n}}
\]

may contain a phase offset not explainable by geometry.

### Channel delay

A delay \(\delta\tau_n\) produces frequency-dependent phase

\[
\boxed{e^{+j\omega\delta\tau_n}}
\]

under the accepted delay convention.

One-frequency phase does not uniquely separate static electronic phase from physical/electrical delay.

Therefore 3.2, 3.3, and 3.6 are complementary, not interchangeable models.

---

## 7. Reconciliation: physical delay versus sampling-time offset

This is a critical sign/domain distinction.

### Waveform/channel delay

\[
 y(t)=x(t-\delta\tau)
\]

gives

\[
\boxed{e^{+j\omega\delta\tau}}.
\]

### Later sampling of a time-varying waveform

If the actual sample is taken at

\[
 t+\delta t,
\]

then for

\[
 x(t)=Ae^{-j\omega t}
\]

one obtains

\[
\boxed{x(t+\delta t)=x(t)e^{-j\omega\delta t}}.
\]

These signs are opposite because the physical operations are different.

The governing ADR shall prohibit collapsing channel delay and sample-time offset into one untyped `delay_error` parameter.

---

## 8. Reconciliation: fixed skew, SRO, jitter, and digital latency

The timing taxonomy from 3.6 is retained.

The following are not synonyms:

```text
fixed sampling-time offset
sample-rate offset (SRO)
sampling jitter
physical/electrical channel delay
receiver LO/reference phase
receiver LO/reference frequency offset
post-acquisition digital latency
```

The governing sampled-time model is

\[
\boxed{
 t_n[k]
 =t_0+\beta_n+kT_s(1+\epsilon_{T,n})+\eta_n[k].
}
\]

For actual sampling frequency

\[
f_{s,n}=f_s(1+\epsilon_{f,n}),
\]

\[
\boxed{
1+\epsilon_{T,n}=\frac{1}{1+\epsilon_{f,n}}
}
\]

and for small offsets

\[
\boxed{
\epsilon_{T,n}\approx-\epsilon_{f,n}.
}
\]

A fixed narrowband phase representation of timing error is a bounded specialization, not the primary timing definition.

---

## 9. Reconciliation: common phase and common complex scale

The explorations consistently use several equivalence levels. They are now normalized as follows.

### 9.1 Common phase

For

\[
\mathbf b=e^{j\phi}\mathbf a,
\]

the spatial projective direction is unchanged, and ordinary covariance is exactly unchanged:

\[
\boxed{
\mathbf b\mathbf b^H
=\mathbf a\mathbf a^H.
}
\]

### 9.2 Common amplitude/complex scale

For

\[
\mathbf b=c\mathbf a,
\]

projective manifold direction is unchanged, while

\[
\boxed{
\mathbf b\mathbf b^H
=|c|^2\mathbf a\mathbf a^H.
}
\]

### 9.3 Reconciled common-gain nuance

Statements that common gain may affect SNR are conditional on physical stage ordering.

If the same scalar multiplies both signal and already-present noise after all relevant noise injection, SNR may remain unchanged.

If analog gain occurs before later receiver/ADC noise, clipping, quantization, or nonlinearity, it can materially change effective SNR/dynamic range and estimator performance.

Therefore the governing rule is:

\[
\boxed{
\text{common gain is projectively irrelevant to ideal manifold direction but not universally irrelevant to the physical measurement chain.}
}
\]

This wording resolves the only potentially ambiguous common-gain phrasing across 3.3, 3.7, 3.8, 3.12, and 3.13.

---

## 10. Reconciliation: element response versus electronic gain

The scientific distinction remains:

\[
\boxed{
\mathbf G(f,t,\chi)
\neq
\mathbf P(\hat{\mathbf u},f,\mathbf p,\chi)
}
\]

as physical semantics, even if both may be diagonal at a particular operating state.

Electronic gain/phase is receiver/channel response.

Element response can depend on direction, frequency, polarization, orientation, and environment.

A numerical diagonal fit at one state does not prove the same physical cause or transferable model.

---

## 11. Reconciliation: polarization and propagation direction

Element/polarization semantics shall use ADR-001's explicit distinction

\[
\boxed{
\hat{\mathbf k}_{\rm prop}=-\hat{\mathbf u}.
}
\]

Any polarization handedness or transverse basis shall declare whether it is defined with respect to propagation direction or look direction.

No bare `RHCP/LHCP` label is scientifically complete without basis/handedness convention.

The initial Phase-1 profile remains scalar and avoids asserting a universal polarimetric convention beyond this foundation.

---

## 12. Reconciliation: coupling and network quantities

The following remain distinct:

\[
\boxed{
\mathbf Z_A,
\mathbf S,
\mathbf T_L,
\mathbf C,
\mathbf a_{\rm embedded},
\mathbf a_{\rm aggregate}
}
\]

where applicable.

Under the declared Thevenin-style specialization,

\[
\boxed{
\mathbf i
=(\mathbf Z_A+\mathbf Z_L)^{-1}\mathbf v_{\rm oc}
}
\]

and

\[
\boxed{
\mathbf v_L
=\mathbf Z_L(\mathbf Z_A+\mathbf Z_L)^{-1}\mathbf v_{\rm oc}.
}
\]

The loaded-port transform

\[
\boxed{
\mathbf T_L
=\mathbf Z_L(\mathbf Z_A+\mathbf Z_L)^{-1}
}
\]

is not a universal generic coupling matrix.

Likewise \(S_{21}\) is not automatically \(C_{21}\).

No contradiction remains after applying these type distinctions.

---

## 13. Reconciliation: reciprocity, symmetry, and Hermitian structure

The governing ADR shall preserve:

```text
reciprocal multiport may imply symmetric Z under applicable assumptions
symmetric matrix != Hermitian matrix
covariance matrices are Hermitian PSD by definition/model
coupling/network matrices are not made Hermitian merely for numerical convenience
```

This avoids importing covariance algebra into electromagnetic network semantics.

---

## 14. Reconciliation: finite-array coupling structure

No universal Toeplitz/circulant/banded coupling structure is accepted.

A finite approximately uniform array may admit an approximate Toeplitz/banded model under a declared evidence-supported profile.

A circulant model is not the default for a finite ULA.

Sparse impedance/network structure does not imply sparse inverse/loading transform.

These are modeling approximations, not scientific identities.

---

## 15. Reconciliation: embedded/full-wave response and double counting

Explorations 3.4, 3.5, 3.8, and 3.10 consistently require included-effects provenance.

The final rule is:

\[
\boxed{
\text{An effect already contained in a measured/EM/embedded aggregate response shall not be applied again unless it has been explicitly de-embedded.}
}
\]

This applies particularly to:

- mutual coupling;
- embedded element response;
- radome/platform scattering;
- feed/network response;
- receiver electronics;
- calibration fixtures/cables.

Reference-plane and included-effects metadata are mandatory for composition.

---

## 16. Reconciliation: typed operator graph

Exploration 3.8 remains the unifying representation.

GeoDOA does **not** define one universal sensor-imperfection matrix.

The physical graph may contain:

```text
geometry-state transformations
source-dependent element operators
cross-channel linear network operators
linear receiver operators
widely-linear IQ operators
sampling/time-grid operators
additive stochastic injection
nonlinear operators
quantizers/code mappings
digital selection operators
```

A product such as

\[
\boxed{
\mathbf a_{\rm phys}
=\mathbf G_{\rm rx}\mathbf C\mathbf P\mathbf a_{\rm geo}^{\rm phys}
}
\]

is a bounded linear-manifold specialization only when all terms share compatible reference planes/domains and no effects are double counted.

---

## 17. Reconciliation: reference planes

The conceptual reference planes from 3.8 are retained for the draft:

```text
RP-0 incident field/source condition
RP-1 geometry/propagation response
RP-2 element/open-circuit array response
RP-3 loaded/coupled port response
RP-4 analog receiver/baseband response
RP-5 continuous-time pre-sampling waveform
RP-6 sampled pre-quantization values
RP-7 ADC code output
RP-8 dequantized digital measurement
RP-9 selected/processed array view
```

These are scientific reference-plane concepts, not yet accepted API enum names.

Every operator/calibration artifact shall eventually declare enough information to identify compatible input/output planes, state, included effects, and provenance.

---

## 18. Reconciliation: noise ordering

Noise shall remain a stage-specific stochastic injection rather than a generic final scalar variance.

For a linear chain, noises injected at different stages are transformed differently downstream.

If independent,

\[
\boxed{
\mathbf R_y
=\mathbf H\mathbf R_x\mathbf H^H
+\sum_r
\mathbf H_{\rm down,r}
\mathbf R_{n_r}
\mathbf H_{\rm down,r}^H.
}
\]

If correlated, cross-covariance terms are required.

This reconciles 3.3 gain/noise ordering, 3.5 coupling/noise transformation, 3.7 receiver noise, 3.8 stage ordering, 3.9 correction noise amplification, and 3.12 colored-noise eigenspace effects.

---

## 19. Reconciliation: ADC quantization versus downstream fixed point

This separation is normative:

\[
\boxed{
\text{ADC acquisition quantization}
\neq
\text{FPGA/processor fixed-point quantization}.
}
\]

ADC quantization belongs to the sensor/measurement chain and maps analog/sampled values to codes.

FPGA/processor fixed-point effects belong to later numerical implementation/hardware algorithm design.

A `bits` field shall not be allowed to ambiguously represent both domains.

---

## 20. Reconciliation: quantization-noise approximation

The exact quantizer is nonlinear:

\[
\boxed{\mathbf y=\mathcal Q(\mathbf z).}
\]

The classical additive white model with variance

\[
\boxed{\sigma_q^2=\Delta^2/12}
\]

is a restricted approximation requiring declared assumptions such as no overload, adequate resolution, and sufficiently busy/dithered input conditions.

Coarse/one-bit quantization requires a specialized statistical/estimator profile.

No contradiction exists between exact quantizer semantics and the optional high-resolution approximation because the latter is explicitly typed as an approximation.

---

## 21. Reconciliation: calibration is inference, not physical causation

The final calibration taxonomy retains:

```text
characterization
parameter calibration
model calibration
data correction/equalization
direct measured/EM manifold calibration
self-calibration/joint estimation
calibration tracking/maintenance
```

The forward system causes the measurement.

Calibration estimates parameters/models or transforms data after observing/calibrating the system.

The final ADR shall never write a calibration operator as though it physically caused the original measurement.

---

## 22. Reconciliation: model calibration versus data correction

These two paths remain distinct.

### Model calibration

Use

\[
\boxed{
\mathbf a_{\rm cal}
}

or another calibrated operator inside the estimator while leaving measured data unchanged.

### Data correction

Use

\[
\boxed{
\mathbf y_{\rm corr}=\mathbf C_{\rm corr}\mathbf y.
}
\]

Then

\[
\boxed{
\mathbf R_{\rm corr}
=\mathbf C_{\rm corr}
\mathbf R_y
\mathbf C_{\rm corr}^H
}
\]

for a fixed linear correction.

The corrected noise covariance is transformed as well.

Therefore the two strategies can have different statistical consequences even when both reduce deterministic mismatch.

---

## 23. Reconciliation: inverse, pseudoinverse, and regularization

An exact inverse is only available when the relevant linear operator is square/nonsingular and the inversion is scientifically meaningful at the declared plane.

A pseudoinverse or regularized correction is not an exact inverse.

For example,

\[
\boxed{
\mathbf C_\lambda
=(\mathbf H^H\mathbf H+\lambda\mathbf I)^{-1}\mathbf H^H
}
\]

is a regularized correction with an explicit bias/noise-amplification tradeoff.

Small singular values and condition number are related but distinct diagnostics.

Information lost in a null space cannot be reconstructed by calibration.

---

## 24. Reconciliation: calibration identifiability and gauge

The following remain distinct:

- physical observability;
- structural/global identifiability;
- local identifiability;
- gauge fixing;
- numerical conditioning;
- estimator convergence;
- calibration uncertainty.

A reference-channel constraint such as

\[
 g_r=1
\]

fixes a representation gauge. It does not prove that the physical reference channel is error free.

Likewise, an optimizer returning a unique numerical answer does not prove global physical identifiability.

---

## 25. Reconciliation: direct measured/CST manifold

A direct measured or EM/CST manifold is accepted as an aggregate calibrated response model when its domain/provenance are declared.

It can replace an upstream parametric subgraph at a declared plane.

The final rules are:

1. measured \(\neq\) physical truth by definition;
2. EM/CST \(\neq\) measured truth by definition;
3. direct aggregate response need not be uniquely decomposed into physical causes;
4. included effects must be recorded;
5. coordinate frame and channel identity must be registered;
6. coherent complex phase must be preserved for coherent DOA use;
7. calibration domain must include relevant direction/frequency/polarization/range/state axes;
8. interpolation is part of the scientific calibrated model;
9. extrapolation outside domain is never silent;
10. transmit-field exports are not silently relabeled receive manifolds without convention-checked reciprocity conversion.

---

## 26. Reconciliation: grid-dependent phase gauge

At one state,

\[
\mathbf a'(\xi_m)=e^{j\phi_m}\mathbf a(\xi_m)
\]

may be projectively equivalent.

However, choosing unrelated \(\phi_m\) at every calibration node can alter an interpolated manifold.

Therefore the final ADR shall distinguish:

```text
pointwise projective equivalence
versus
grid-coherent gauge needed for interpolation/phase-slope use
```

No arbitrary per-angle phase normalization is applied silently to source calibration data.

---

## 27. Reconciliation: error metrics

There is no universal `manifold_error` scalar.

The final metric taxonomy shall retain at least:

### Raw Euclidean error

\[
\boxed{
\|\mathbf b-\mathbf a\|_2
}
\]

### Phase-only aligned error

\[
\boxed{
\min_\phi
\|\mathbf b-e^{j\phi}\mathbf a\|_2
}
\]

### Common-complex-scale alignment

\[
\boxed{
\min_c
\|\mathbf b-c\mathbf a\|_2
}
\]

### Normalized projective alignment

\[
\boxed{
\rho
=\frac{|\mathbf a^H\mathbf b|}
{\|\mathbf a\|\|\mathbf b\|}
}
\]

with

\[
\boxed{
1-\rho^2
}
\]

as one-dimensional subspace leakage.

The metric's reference/test objects, gauge/equivalence class, normalization, units, domain weighting, and null handling are part of its definition.

---

## 28. Reconciliation: projective leakage and MUSIC

For unit physical steering vector \(\mathbf u\) and unit model steering vector \(\mathbf v\),

\[
\boxed{
\mathbf v^H
(\mathbf I-\mathbf u\mathbf u^H)
\mathbf v
=1-|\mathbf u^H\mathbf v|^2.
}
\]

Thus the 3.11 projective leakage metric is exactly the normalized population MUSIC denominator at the true source in the rank-one case.

This bridge is retained as a central final-contract result.

---

## 29. Reconciliation: covariance error taxonomy

The exact bookkeeping is

\[
\boxed{
\hat{\mathbf R}-\mathbf R_{\rm nom}
=
\mathbf E_{\rm sensor}
+
\mathbf E_{\rm sample}
}
\]

where

\[
\mathbf E_{\rm sensor}
=\mathbf R_{\rm phys}-\mathbf R_{\rm nom}
\]

and

\[
\mathbf E_{\rm sample}
=\hat{\mathbf R}-\mathbf R_{\rm phys}.
\]

This identity does not imply independence.

Sensor/model mismatch can survive infinite snapshots; finite-sample error can remain even under perfect calibration.

---

## 30. Reconciliation: white versus colored noise

For population covariance

\[
\boxed{
\mathbf R=\mathbf R_{\rm sig}+\sigma^2\mathbf I,
}
\]

isotropic noise shifts eigenvalues without rotating eigenvectors.

For general

\[
\mathbf R_n\neq\sigma^2\mathbf I,
\]

ordinary eigenspaces can change.

A compatible whitened profile may use

\[
\boxed{
\mathbf R_n^{-1/2}\mathbf y,
\qquad
\mathbf R_n^{-1/2}\mathbf a
}
\]

when \(\mathbf R_n\succ0\) and the whitening model is valid.

This resolves baseline-white-noise semantics versus later colored-noise profiles.

---

## 31. Reconciliation: population versus sample eigengap

The final ADR shall use distinct notation for population and sample spectral separation.

A candidate notation is:

\[
\boxed{
\delta_{\rm pop}
}
\]

for the relevant population signal/noise spectral gap and

\[
\boxed{
\hat\delta_{\rm samp}
}
\]

for the observed sample eigengap.

The exact symbols may be polished in the governing draft, but the concepts shall not share one ambiguous `gap` variable.

Davis–Kahan-type bounds require the theorem-specific reference spectral separation rather than an arbitrary sample gap substituted silently.

---

## 32. Reconciliation: rank terminology

The following quantities remain separate:

```text
physical source count
source covariance rank
manifold matrix rank
signal covariance rank
observed signal-subspace dimension
sample covariance rank
chosen estimator/model order
```

A nonsingular sensor transform may preserve signal rank while rotating the subspace.

Coherent sources may reduce source-covariance/signal rank.

Mean-centered sample covariance has an algebraic rank ceiling involving \(L-1\).

No one quantity is named simply `number_of_modes` without qualification.

---

## 33. Reconciliation: time-varying sensor state

A sensor operator changing during a covariance window is not generally equivalent to one average static operator.

A mixture of instantaneous rank-one covariances can have rank greater than one.

Therefore additional covariance modes may arise from time-varying sensor state even when instantaneous source rank is unchanged.

This reconciles timing/CFO/SRO/AGC/deformation effects with the earlier warning that finite noise also fills covariance modes for finite samples.

The physical causes remain separate.

---

## 34. Reconciliation: widely-linear statistics

A general I/Q imbalance model

\[
\boxed{
\mathbf y=\mathbf A\mathbf x+\mathbf B\mathbf x^*+\mathbf d
}
\]

cannot be represented by one ordinary complex \(N\times N\) manifold matrix when \(\mathbf B\neq0\).

The augmented covariance

\[
\boxed{
\mathbf R_{\rm aug}
=
\begin{bmatrix}
\mathbf R_x&\mathbf P_x\\
\mathbf P_x^*&\mathbf R_x^*
\end{bmatrix}
}
\]

is retained for widely-linear/improper profiles.

The initial Phase-1 ordinary-complex profile excludes this regime.

---

## 35. Reconciliation: nonlinear and clipped regimes

Compression, intermodulation, clipping, and other nonlinear receiver effects are not hidden inside a static steering matrix.

Clipping is information destroying.

A linearized small-signal model is permitted only in a declared validated region.

The initial Phase-1 profile excludes nonlinear/clipped operation.

---

## 36. Reconciliation: MUSIC peak sensitivity

The local first-order peak-shift expression developed in 3.12 is retained only as a bounded local result.

It requires:

- smooth one-dimensional search coordinate;
- isolated nondegenerate ideal minimum;
- small perturbations;
- compatible reference/noise projector;
- correct derivative coordinate.

The final ADR shall label it an approximation rather than a universal bias formula.

No conflict exists with the exact two-sensor bias examples because those examples are separate bounded analytical models.

---

## 37. Reconciliation: compatibility policy

Compatibility is multi-axis, not Boolean.

The governing dimensions include at least:

```text
manifold
reference plane
coordinate/direction convention
bandwidth/narrowband validity
stationarity/fixed manifold
snapshot simultaneity/coherence
linear superposition
ordinary-complex vs augmented statistics
noise model
covariance model
quantization regime
calibration state/domain
physical channel/port state
source/subspace rank and model order
manifold/interpolation domain
required preprocessing
```

A run can be manifold-compatible yet noise-incompatible, or timing-compatible yet calibration-domain-incompatible.

This multi-axis policy is internally consistent with ADR-002's progressive compatibility concept.

---

## 38. Reconciliation: compatibility is not performance

A scientifically compatible profile can still perform poorly because of:

- low SNR;
- few snapshots;
- weak eigengap;
- close sources;
- source correlation;
- calibration uncertainty;
- poor conditioning;
- scan-grid limitations.

Conversely, an incompatible model can occasionally produce a numerically plausible estimate.

Therefore compatibility status and empirical performance metrics are separate outputs.

---

## 39. Reconciliation: initial Phase-1 ADR-003 sensor profile

The candidate initial profile is now fully reconciled.

### Physical/manifold state

```text
nominal geometry = physical geometry
far-field narrowband PM-001-compatible propagation
ideal identical scalar elements
unit complex element response
no polarization mismatch in the scalar bounded profile
no mutual coupling distortion
unity differential electronic gain/phase
zero differential channel delay
```

### Timing/reference state

```text
common coherent sampling/reference
zero differential fixed skew
zero differential SRO
zero differential CFO
zero timing jitter in deterministic sensor profile
simultaneous-equivalent snapshots
```

### Receiver/ADC state

```text
linear receiver
no DC offset
no I/Q imbalance
no compression/intermodulation
no clipping
unquantized floating acquisition baseline
```

### Calibration state

```text
no deterministic imperfection calibration required
identity / not-applied calibration state explicitly recorded
```

### Noise/statistics state

```text
additive proper-complex spatially white equal-variance noise
ordinary covariance/subspace representation
```

Thus

\[
\boxed{
\mathcal H_{\rm sensor}^{\rm Phase1}\equiv\mathcal I
}
\]

for deterministic sensor imperfections.

This is the candidate authoritative implementation profile after ADR-003 passes all acceptance gates.

---

## 40. Phase-1 exclusions remain explicit

The initial profile does not authoritatively implement:

```text
position error
nontrivial gain/phase mismatch
channel delay mismatch
mutual coupling
nonideal element/polarization response
measured/CST direct manifolds
colored-noise whitening
sample skew / SRO / CFO / jitter
I/Q imbalance
receiver nonlinearity
clipping
ADC quantization
near-field sensor-imperfection profile
wideband sensor-imperfection profile
vector/polarimetric sensors
TDM-MIMO synchronization calibration
self-calibration
adaptive calibration
one-bit/coarse-quantized MUSIC
```

These effects have scientific contracts now so later bounded profiles can be added without redefining foundational semantics.

---

## 41. Deferred-profile activation rule

A new imperfection family becomes authoritative only after a bounded profile defines and validates:

1. physical/operator semantics;
2. units and domain;
3. reference planes;
4. state/provenance;
5. calibration/correction behavior;
6. estimator compatibility;
7. deterministic analytical/reference checks;
8. failure/boundary behavior;
9. reproducibility/validation evidence;
10. downstream covariance/eigenspace/DOA consequences.

Exposing an optional software parameter is not sufficient.

---

## 42. Golden Reference reconciliation

ADR-003 currently reserves GRP-014 through GRP-017.

### GRP-014 — Position error / rigid translation

Candidate content:

- two-sensor spacing perturbation;
- half-wave or otherwise explicitly declared spacing;
- analytical \(\hat u=(1+\delta d/d)u_0\);
- small-angle \(\Delta\theta\approx(\delta d/d)\tan\theta_0\);
- rigid-translation relative-phase invariant.

### GRP-015 — Gain/phase mismatch

Candidate content:

- common phase covariance invariant;
- two-sensor relative phase-error analytical DOA bias;
- \(d=\lambda/2\) specialization \(\Delta u=-\phi_e/\pi\).

### GRP-016 — Coupled steering response

Candidate content:

\[
\mathbf a=\begin{bmatrix}1\\-j\end{bmatrix},
\qquad
\mathbf C=\begin{bmatrix}1&0.5\\0.5&1\end{bmatrix}
\]

with

\[
\boxed{
\mathbf b
=\mathbf C\mathbf a
=\begin{bmatrix}1-0.5j\\0.5-j\end{bmatrix}.
}
\]

The ratio

\[
\frac{b_2}{b_1}=0.8-0.6j
\]

has phase \(-36.87^\circ\), while nominal phase is \(-90^\circ\). Under nominal half-wave phase matching, the seed inferred direction cosine is approximately

\[
\boxed{\hat u\approx0.20483}
\]

for the declared \(u_0=0.5\) seed.

### GRP-017 — Coupled covariance / eigenspace / MUSIC leakage

Candidate content:

\[
\boxed{
\mathbf R_{\rm sig}
=\mathbf b\mathbf b^H
=\begin{bmatrix}
1.25&1+0.75j\\
1-0.75j&1.25
\end{bmatrix}
}
\]

with eigenvalues

\[
\boxed{\{2.5,0\}}.
\]

After adding \(\mathbf I\), eigenvalues are

\[
\boxed{\{3.5,1\}}
\]

with unchanged eigenvectors.

Nominal/coupled squared normalized alignment is

\[
\boxed{\rho^2=0.8}
\]

and nominal leakage into the physical rank-one noise subspace is

\[
\boxed{1-\rho^2=0.2}.
\]

These remain **reserved seeds**, not formal Gate-E PASS evidence until promoted and verified under the accepted ADR draft.

---

## 43. Additional Gate-E candidate checks

The explorations produced several deterministic checks that may become formal tests or remain supporting calculations.

Candidates include:

- physical delay versus later-sampling phase-sign check;
- SRO elapsed-time check;
- differential CFO coherence/sinc check;
- ideal ADC 12-bit step/noise/SNR check;
- jitter-limited SNR check;
- DC-offset covariance rank-one check;
- noncommuting \(\mathbf C\mathbf G\neq\mathbf G\mathbf C\) check;
- common gain before clipping check;
- calibration inverse noise-amplification check;
- calibration gauge ambiguity check;
- direct-manifold coordinate-registration check;
- direct-manifold phase-gauge interpolation check;
- first-order covariance expansion check;
- eigengap sensitivity check;
- time-varying rank-growth check;
- compatibility decision seeds from 3.13.

Gate E shall decide which deserve formal Golden Reference status and which remain explanatory tests.

No new GRP number is assigned in 3.14.

---

## 44. Cross-ADR scope reconciliation

### ADR-001 owns

- coordinate frame;
- look/propagation direction;
- temporal/spatial sign convention;
- nominal geometry reference semantics;
- physical units/channel identity;
- lattice/coarray geometric conventions.

### ADR-002 owns

- exact/approximate propagation and delay;
- far-field/narrowband diagnostics;
- measurement axes/snapshots;
- source/noise statistical semantics;
- covariance definitions;
- MIMO physical-channel provenance;
- propagation/measurement compatibility classes.

### ADR-003 owns

- deviations of real sensor/receiver system from ideal model;
- sensor-imperfection typed operators;
- calibration/correction;
- direct measured/EM manifolds;
- sensor mismatch metrics/identifiability;
- covariance/eigenspace/MUSIC propagation of sensor mismatch;
- estimator compatibility implications caused by sensor/receiver state.

### ADR-004 shall own

- validation hierarchy/protocol;
- seeds and reproducibility execution;
- sweeps/Monte Carlo policy;
- pass/fail thresholds;
- formal benchmark/report evidence.

This boundary is consistent across the explored documents.

---

## 45. Documentation-state reconciliation issue

One non-scientific repository-state issue remains.

`docs/adr/ADR-003_EXPLORATION_CHECKPOINT.md` was originally the consolidated exploration checkpoint for 3.1–3.6 and was later status-reconciled through 3.8. Its header/current sequence metadata still identifies 3.9 as the next section, while dedicated authoritative exploration records now exist through 3.14.

This is a **documentation status drift**, not a scientific contradiction.

Before Gate A begins, the repository shall safely reconcile that checkpoint metadata so it reflects:

```text
3.1–3.14 COMPLETE
next: draft governing ADR-003 / pre-Gate reconciliation
Gates: NOT STARTED
```

The large checkpoint body shall not be destructively rewritten merely to update status metadata.

---

## 46. No blocking scientific contradiction found

The audit found no blocking contradiction in the following critical chains:

```text
ADR-001 spatial sign
↔ ADR-002 propagation delay
↔ ADR-003 position/phase error

physical delay
↔ sampling-time sign
↔ SRO/CFO timing taxonomy

element response
↔ coupling/loading
↔ direct measured/CST included-effects provenance

physical forward model
↔ calibration estimation
↔ data correction

manifold mismatch
↔ covariance perturbation
↔ eigenspace rotation
↔ MUSIC leakage/bias

initial sensor profile
↔ classical MUSIC assumptions
↔ deferred-profile boundaries
```

The remaining tasks are contract drafting and gate verification, not conceptual exploration.

---

## 47. Resolved nuances to encode explicitly in the draft

The governing ADR draft shall explicitly encode these reconciliations rather than rely on readers inferring them from exploration history:

1. common gain affects SNR only according to physical stage/noise ordering;
2. physical delay and sampling-time offset have opposite tone-phase signs because they are different operations;
3. common rigid translation does not distort far-field relative manifold;
4. mechanical position and EM phase center are distinct;
5. arbitrary electronic phase, geometry-induced phase, and delay slope are distinct;
6. \(\mathbf Z\), \(\mathbf S\), \(\mathbf T_L\), effective \(\mathbf C\), and aggregate manifold are typed distinct quantities;
7. embedded/full-wave/manifold effects cannot be re-applied without de-embedding;
8. calibration is estimation/correction, not physical causation;
9. gauge fixing is not new physical information;
10. direct manifold may be estimator-useful without physical-cause identifiability;
11. pointwise projective gauge is not automatically interpolation-safe across a calibration grid;
12. ADC quantization and downstream fixed-point quantization are distinct;
13. population and sample eigengaps are distinct;
14. population/model mismatch and finite-sample covariance error are distinct;
15. compatibility and performance are distinct;
16. static matched imperfections can remain compatible with classical MUSIC;
17. nonlinear, coarse-quantized, time-varying, wideband, or augmented-statistics regimes require distinct profiles.

---

## 48. Candidate final ADR-003 contract

The governing ADR draft shall be constructed around the following compact contract.

### C-1 — Preserve scientific object identity

Nominal, physical, measured, EM, calibrated, and simulation-truth responses are distinct.

### C-2 — Preserve physical cause/domain

Geometry, element response, coupling/loading, electronics, timing, stochastic noise, nonlinear response, quantization, and digital selection are typed distinct effects.

### C-3 — Preserve operator ordering/reference planes

Effects compose only across scientifically compatible planes/domains; matrix dimensions alone do not establish compatibility.

### C-4 — Preserve exact-before-approximate hierarchy

Exact geometry/path/time/quantizer definitions precede far-field, narrowband, small-error, additive-noise, or linearized approximations.

### C-5 — Preserve calibration separation

Calibration estimates/constructs models or corrections; it is not part of the causal forward measurement chain.

### C-6 — Preserve calibration provenance/domain

Calibration validity is state-, frequency-, direction-, polarization-, hardware-, time-, and reference-plane-dependent where applicable.

### C-7 — Preserve gauge/equivalence semantics

Absolute, phase-aligned, common-complex-scale/projective, reference-channel, and other gauge-fixed comparisons are distinct.

### C-8 — Preserve uncertainty/identifiability semantics

Error, uncertainty, identifiability, observability, conditioning, regularization, and optimizer convergence are distinct.

### C-9 — Preserve statistical consequences

Sensor effects propagate to covariance/noise/eigenspace according to their physical order and cannot universally be represented as additive white covariance noise.

### C-10 — Preserve estimator compatibility

Compatibility is multi-axis and profile-specific; no silent coercion converts incompatible sensor/receiver states into baseline classical MUSIC.

### C-11 — Preserve Phase-1 boundedness

The initial authoritative profile remains the ideal deterministic sensor chain with white-noise classical MUSIC compatibility. Nonideal families remain scientifically specified but implementation-deferred until separately validated.

---

## 49. Candidate decision set from 3.14

- **3.14-D1** — Explorations 3.1–3.13 are scientifically reconcilable with accepted ADR-001 and ADR-002; no blocking contradiction was identified.
- **3.14-D2** — ADR-003 shall inherit ADR-001/ADR-002 spatial, delay, snapshot, covariance, source-statistics, and MIMO semantics rather than redefine them.
- **3.14-D3** — The canonical ADR-003 model is a typed physical sensor/receiver operator graph plus a separate calibration/correction graph.
- **3.14-D4** — Nominal, physical, measured, EM, calibrated, and simulation-truth manifolds remain distinct final-contract meanings.
- **3.14-D5** — Nominal geometry, realized physical geometry, calibrated geometry estimate, pose, orientation, and EM phase-center behavior remain distinct.
- **3.14-D6** — Geometry-induced phase, static electronic phase, physical/electrical delay, and sample-time offset are distinct effects with distinct sign/domain semantics.
- **3.14-D7** — Physical channel delay and later sampling of a tone retain opposite phase signs under the accepted convention because they are different physical operations.
- **3.14-D8** — Fixed skew, SRO, jitter, physical delay, LO phase/frequency error, and post-acquisition latency remain distinct timing families.
- **3.14-D9** — Common phase is covariance invariant in the bounded ordinary-complex model; common gain is projectively invariant but its physical SNR/dynamic-range consequence depends on stage/noise ordering.
- **3.14-D10** — Element response and electronic gain/phase remain physically distinct even when both admit diagonal numerical specializations.
- **3.14-D11** — Polarization semantics shall be referenced consistently to the accepted look/propagation-direction convention.
- **3.14-D12** — Z, S, loaded-port transforms, effective coupling matrices, embedded patterns, and aggregate manifolds remain typed distinct scientific objects.
- **3.14-D13** — Symmetric network matrices and Hermitian covariance matrices shall not be conflated.
- **3.14-D14** — Toeplitz/banded/circulant coupling structures are approximations requiring evidence and are not universal finite-array laws.
- **3.14-D15** — Included-effects/de-embedding provenance is mandatory to prevent element/coupling/platform/receiver double counting.
- **3.14-D16** — No universal sensor-imperfection matrix is accepted; one linear product is only a bounded compatible specialization.
- **3.14-D17** — Conceptual RP-0 through RP-9 reference-plane semantics are retained for the governing draft while API naming remains deferred.
- **3.14-D18** — Stage-specific noise injection and downstream transformation remain authoritative; one final generic noise variance is insufficient for general receiver profiles.
- **3.14-D19** — ADC acquisition quantization and downstream FPGA/processor fixed point are separate scientific/numerical stages.
- **3.14-D20** — Delta-squared-over-12 quantization noise is a restricted approximation, not the definition of ADC quantization.
- **3.14-D21** — Calibration taxonomy retains characterization, parameter/model calibration, correction, direct manifold calibration, self-calibration, and tracking as distinct activities.
- **3.14-D22** — Model calibration and data correction remain statistically distinct because data correction transforms covariance/noise.
- **3.14-D23** — Exact inverse, pseudoinverse, and regularized correction are distinct and shall retain singular-value/conditioning provenance.
- **3.14-D24** — Gauge fixing does not create new physical observability; calibration identifiability and numerical convergence remain distinct.
- **3.14-D25** — Measured/CST manifolds are aggregate calibrated response models and are not automatically physical truth.
- **3.14-D26** — Pointwise common-phase equivalence does not authorize arbitrary per-grid phase choices for interpolation.
- **3.14-D27** — No single generic manifold-error metric is accepted; equivalence class and normalization are part of the metric definition.
- **3.14-D28** — Rank-one projective leakage \(1-\rho^2\) remains exactly linked to the normalized population MUSIC noise-subspace denominator at the true source.
- **3.14-D29** — Sensor-induced population covariance mismatch and finite-sample covariance error remain separate error families.
- **3.14-D30** — Isotropic white noise preserves population covariance eigenvectors; colored/unequal noise generally does not.
- **3.14-D31** — Population and sample eigengaps shall use distinct semantics/notation in the governing ADR.
- **3.14-D32** — Physical source count, source-covariance rank, signal-covariance rank, observed subspace rank, sample rank, and selected model order remain distinct.
- **3.14-D33** — Time-varying sensor state can produce additional covariance modes and cannot generally be replaced by one averaged static manifold.
- **3.14-D34** — Widely-linear/IQ-impaired profiles require augmented statistics unless correction restores ordinary-complex compatibility.
- **3.14-D35** — Nonlinear/clipped regimes remain outside the baseline linear sensor/manifold contract.
- **3.14-D36** — First-order MUSIC peak-shift expressions remain bounded local approximations rather than universal bias laws.
- **3.14-D37** — Compatibility is a multi-axis profile decision and remains distinct from performance/confidence.
- **3.14-D38** — The candidate initial Phase-1 ADR-003 profile is the ideal deterministic sensor chain with additive proper-complex white equal-variance noise and ordinary classical MUSIC compatibility.
- **3.14-D39** — Nonideal sensor families remain implementation-deferred until separately bounded and validated; exploration completeness does not activate implementation scope.
- **3.14-D40** — GRP-014 through GRP-017 remain the reserved formal reference-problem range; exploratory checks do not receive new GRP numbers before Gate E.
- **3.14-D41** — The consolidated exploration checkpoint currently has status metadata drift beyond 3.8 and shall be safely reconciled before Gate A without destructive full-file rewrite.
- **3.14-D42** — ADR-003 is now ready for a governing draft, but no acceptance Gate has yet started or passed.

---

## 50. Readiness assessment

### Scientific exploration completeness

```text
3.1   Ideal / Physical / Calibrated Manifold                 COMPLETE
3.2   Position Error and Geometry Perturbation                COMPLETE
3.3   Gain and Phase Mismatch                                 COMPLETE
3.4   Element Pattern and Polarization                        COMPLETE
3.5   Mutual Coupling                                         COMPLETE
3.6   Channel Delay, Clock Skew, and Frequency Error          COMPLETE
3.7   Quantization / Receiver / Dynamic-Range Effects         COMPLETE
3.8   Unified Sensor-Imperfection Operator                    COMPLETE
3.9   Calibration Models                                      COMPLETE
3.10  Direct Measured / CST-Derived Manifold Calibration      COMPLETE
3.11  Error Metrics and Identifiability                       COMPLETE
3.12  Covariance / Eigenspace / MUSIC Error Propagation       COMPLETE
3.13  Compatibility and Initial ADR-003 Profile               COMPLETE
3.14  Cross-Section Reconciliation                            COMPLETE
```

### Blocking scientific contradictions

```text
NONE IDENTIFIED
```

### Non-scientific reconciliation item before Gate A

```text
Safely update consolidated ADR-003_EXPLORATION_CHECKPOINT.md status metadata
so that it reflects completion through 3.14.
```

### Gate status

```text
Gate A — NOT STARTED
Gate B — NOT STARTED
Gate C — NOT STARTED
Gate D — NOT STARTED
Gate E — NOT STARTED
Gate F — NOT STARTED
```

### Final exploration-stage disposition

\[
\boxed{
\text{READY TO DRAFT GOVERNING ADR-003 — NOT ACCEPTED}
}
\]

---

## 51. Immediate next step

The next work shall proceed in this order:

1. safely reconcile the consolidated exploration-checkpoint status metadata through 3.14;
2. draft the governing `ADR-003-sensor-imperfections-mutual-coupling-calibration.md` from the reconciled candidate contract;
3. perform a pre-Gate draft consistency review;
4. only then start **Gate A — Physical Consistency**;
5. continue Gates B–F in the standard Phase 0C sequence;
6. perform final cross-gate reconciliation;
7. mark ADR-003 `Accepted` only if every required gate passes.

Do not start Gate A before the governing ADR draft exists and the checkpoint status reconciliation is complete.
