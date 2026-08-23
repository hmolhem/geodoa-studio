# ADR-003 Exploration 3.13 — Compatibility and Initial ADR-003 Profile

- **Phase:** 0C — Scientific Foundations
- **Status:** EXPLORATION COMPLETE — CANDIDATE CONTRACT, NOT ACCEPTED
- **Parent ADR:** ADR-003 — Sensor Imperfections, Mutual Coupling, and Calibration
- **Branch:** `docs/phase0c-scientific-conventions`
- **Depends on:** ADR-001, ADR-002, ADR-003 Explorations 3.1–3.12
- **Acceptance gates:** Not started

> This is the dedicated exploration record for ADR-003 Section 3.13. It is not an accepted governing ADR. Candidate decisions remain subject to 3.14 cross-section reconciliation, Gates A–F, Golden Reference evidence, boundary/failure analysis, and final acceptance.

---

## 1. Primary question

Explorations 3.1–3.12 established the scientific semantics of nominal/physical/calibrated manifolds, geometry errors, gain/phase mismatch, element and polarization response, coupling/loading, timing/clock/frequency errors, receiver/ADC effects, typed sensor operators, calibration, measured/CST manifolds, error metrics, identifiability, covariance/eigenspace perturbation, and MUSIC degradation.

Exploration 3.13 answers:

> Given a declared sensor/receiver/calibration state, how shall GeoDOA decide whether a classical narrowband covariance-based MUSIC profile is scientifically compatible, requires a declared preprocessing/model change, requires a different estimator/statistical representation, or must be rejected/deferred?

The governing principle is

\[
\boxed{
\text{Estimator compatibility is multi-axis and profile-specific; it is not one generic Boolean.}
}
\]

A profile is compatible only when all scientific assumptions required by that profile are satisfied simultaneously.

---

## 2. Compatibility dimensions

GeoDOA shall evaluate compatibility along distinct dimensions. At minimum:

```text
C1  manifold representation compatibility
C2  reference-plane compatibility
C3  coordinate / direction convention compatibility
C4  narrowband / frequency compatibility
C5  fixed-manifold / time-invariance compatibility
C6  snapshot simultaneity / coherent-epoch compatibility
C7  linear-superposition compatibility
C8  ordinary-complex versus augmented/widely-linear statistics compatibility
C9  noise-model compatibility
C10 covariance-model compatibility
C11 quantization / ADC-regime compatibility
C12 calibration-domain/state compatibility
C13 channel / port-state compatibility
C14 source-rank / model-order compatibility
C15 manifold-grid/interpolation-domain compatibility
C16 estimator-specific preprocessing compatibility
```

A downstream implementation may later encode these as typed status objects, but the scientific dimensions shall remain distinguishable.

---

## 3. Compatibility status vocabulary

A single axis may have a conceptual status such as:

```text
COMPATIBLE
COMPATIBLE_WITH_MATCHED_MODEL
REQUIRES_CALIBRATION
REQUIRES_DATA_CORRECTION
REQUIRES_WHITENING
REQUIRES_RESAMPLING_OR_DESKEW
REQUIRES_AUGMENTED_STATISTICS
REQUIRES_WIDEBAND_PROCESSING
REQUIRES_SPECIALIZED_QUANTIZED_ESTIMATOR
DEGRADED_APPROXIMATION
OUTSIDE_CALIBRATION_DOMAIN
INCOMPATIBLE
UNRESOLVED
NOT_ASSESSED
```

These labels are scientific semantics, not final API enum names.

A final profile-level result derives from all relevant axes and shall identify the limiting assumptions rather than returning only `false`.

---

## 4. Classical MUSIC reference profile

For ADR-003 compatibility purposes, the baseline classical MUSIC profile means:

\[
\boxed{
\mathbf x[k]
=\mathbf A(\boldsymbol\theta)\mathbf s[k]+\mathbf n[k]
}
\]

with the following scientific assumptions:

1. narrowband receive model at a declared frequency;
2. far-field directional manifold for the initial profile;
3. fixed sensor/manifold state over the covariance window;
4. simultaneous-equivalent coherent snapshots;
5. ordinary complex-linear source superposition;
6. proper-complex ordinary covariance is sufficient;
7. additive spatially white equal-variance noise for the unwhitened baseline;
8. no nonlinear receiver distortion in the operating regime;
9. no clipping/overload;
10. no coarse/one-bit quantization requiring specialized statistics;
11. signal/noise subspace dimension is scientifically defined;
12. search manifold and data reference plane are compatible;
13. calibration state, if used, is valid for the data state;
14. source/covariance conditions satisfy the selected MUSIC variant.

Failure of one assumption does not always make the physical dataset unusable; it may require a different profile or preprocessing chain.

---

## 5. Ideal initial ADR-003 profile

The initial bounded Phase-1 sensor profile shall be intentionally simple and deterministic.

### 5.1 Geometry and propagation

```text
nominal physical geometry = realized physical geometry
far-field propagation
narrowband model
ADR-001 direction/sign/phase-reference conventions
ADR-002 PM-001 propagation/measurement semantics
```

Hence

\[
\boxed{
\mathbf r_n^{\rm phys}=\mathbf r_n^{\rm nom}.
}
\]

### 5.2 Element response

```text
identical ideal scalar elements
unit complex element response
no polarization mismatch in the bounded scalar profile
no direction-dependent element distortion beyond ideal profile
```

Thus

\[
\boxed{
\mathbf P=\mathbf I.
}
\]

### 5.3 Coupling/loading

```text
no mutual-coupling distortion
ideal/reference loading state
no cross-channel network mixing
```

Thus

\[
\boxed{
\mathbf C=\mathbf I.
}
\]

### 5.4 Gain/phase/delay

```text
unity gain
zero differential electronic phase
zero differential channel delay
```

Thus

\[
\boxed{
\mathbf G=\mathbf I.
}
\]

### 5.5 Clock/synchronization/reference

```text
common coherent sampling/reference architecture
zero differential fixed sampling skew
zero differential SRO
zero differential CFO
zero timing jitter in deterministic sensor profile
simultaneous-equivalent snapshots
```

### 5.6 Receiver/ADC

```text
linear receiver
no DC offset
no I/Q imbalance
no compression/intermodulation
no clipping
unquantized floating measurement for the scientific baseline
ADC acquisition quantization not active
```

### 5.7 Calibration

```text
calibration requirement: none for deterministic sensor imperfections
calibration correction: identity / not applied
calibration state: explicitly ideal baseline
```

### 5.8 Noise

```text
additive proper-complex spatially white equal-variance noise
noise injected at the declared baseline measurement stage
```

### 5.9 Resulting deterministic sensor operator

Under these assumptions,

\[
\boxed{
\mathcal H_{\rm sensor}^{\rm Phase1}\equiv\mathcal I
}
\]

for the deterministic imperfection graph.

The purpose of this identity baseline is not to deny real sensor imperfections. It provides a scientifically controlled starting profile against which later bounded imperfection profiles can be activated one family at a time.

---

## 6. Profile naming principle

GeoDOA shall not use a generic name such as `realistic_sensor=True`.

Each validated profile shall state its active physics and estimator assumptions.

Conceptually:

```text
P-S0  Ideal Narrowband Classical MUSIC Sensor Profile
P-S1  Static Gain/Phase Mismatch — Matched Manifold
P-S2  Static Gain/Phase Mismatch — Nominal Manifold
P-S3  Static Coupling — Matched Coupled Manifold
P-S4  Colored Noise — Whitened MUSIC
P-S5  Measured/CST Direct Manifold — Matched Classical MUSIC
P-S6  Widely-Linear IQ Profile — Augmented Processing
P-S7  Timing/SRO Profile — Resampled/Wideband Processing
...
```

These labels are illustrative exploration names, not accepted public API identifiers.

---

## 7. Compatibility rule: static deterministic manifold mismatch

If a physical imperfection changes the deterministic steering manifold but remains:

- fixed over the covariance window;
- narrowband;
- complex linear;
- source-compatible;
- non-rank-destroying as required by the estimator;

then classical MUSIC may remain scientifically valid **if the search manifold is updated to the matched physical/calibrated manifold**.

Examples include bounded static:

- position errors;
- per-channel gain/phase mismatch;
- frequency-frozen channel delay phase;
- linear mutual coupling/loading;
- direction-dependent scalar element response;
- direct measured/CST manifold response.

Therefore

\[
\boxed{
\text{imperfection present}
\not\Rightarrow
\text{classical MUSIC impossible}.
}
\]

The critical condition is model/data compatibility.

---

## 8. Nominal-manifold use under static mismatch

If data are generated by

\[
\mathbf a_{\rm phys}(\theta)
\]

but MUSIC searches with

\[
\mathbf a_{\rm nom}(\theta),
\]

then the profile is scientifically classified as **mismatched classical MUSIC**, not as matched classical MUSIC.

The algorithm can still return an estimate, but nonzero population noise-subspace leakage and deterministic asymptotic bias may remain even with infinite snapshots.

GeoDOA shall expose the mismatch state rather than silently calling the run `MUSIC` with no model qualifier.

---

## 9. Position error compatibility

### Static known/calibrated position errors

If realized geometry is known or calibrated and the manifold is regenerated from physical coordinates,

```text
classical MUSIC compatibility: COMPATIBLE_WITH_MATCHED_MODEL
```

subject to the other baseline assumptions.

### Static unknown position errors with nominal manifold

```text
compatibility: DEGRADED_APPROXIMATION / MISMATCHED_MODEL
```

with deterministic bias/leakage possible.

### Time-varying deformation within covariance window

A single static manifold may be invalid:

```text
compatibility: INCOMPATIBLE with fixed-manifold profile
required: time-varying/state-aware processing or shorter validated stationarity window
```

---

## 10. Gain/phase mismatch compatibility

### Fixed per-channel complex gains, matched manifold

For

\[
\mathbf a_{\rm phys}=\mathbf G\mathbf a_{\rm nom},
\]

fixed nonsingular \(\mathbf G\) can be incorporated into the manifold.

```text
classical MUSIC: COMPATIBLE_WITH_MATCHED_MODEL
```

### Data correction

If \(\mathbf G^{-1}\) is applied to data, covariance/noise statistics transform and must remain compatible.

```text
classical MUSIC: requires re-evaluation of noise model
```

### Time-varying gain/phase over covariance window

```text
fixed-manifold classical MUSIC: potentially INCOMPATIBLE
```

unless the variation is negligible under a declared approximation.

---

## 11. Common phase and common gain compatibility

A common phase factor cancels from ordinary covariance and is projectively irrelevant to classical narrowband MUSIC under the bounded linear model.

A common gain rescales signal and noise only if it acts uniformly on the entire relevant measurement vector/stages. It may still matter physically through SNR, clipping, AGC, quantization, or nonlinear operating point.

Therefore:

```text
common phase after linear acquisition: typically compatible/invariant
common gain in purely linear floating profile: typically compatible after power interpretation
common gain before nonlinear/ADC stages: compatibility must be reassessed
```

---

## 12. Element-pattern compatibility

If scalar complex element responses are fixed and known for each source state,

\[
\mathbf a_{\rm phys}(\xi)
=\mathbf P(\xi)\mathbf a_{\rm geo}(\xi),
\]

then classical MUSIC can use the matched source-state-dependent manifold.

```text
compatibility: COMPATIBLE_WITH_MATCHED_MODEL
```

for the bounded scalar complex-linear case.

If the sensor is truly vector/polarimetric and ordinary scalar manifold representation is insufficient:

```text
compatibility: requires polarimetric/vector-sensor estimator profile
```

---

## 13. Mutual-coupling compatibility

For a fixed linear coupling/loading operator

\[
\mathbf a_{\rm phys}=\mathbf C\mathbf a_{\rm pre},
\]

classical MUSIC remains compatible if the physical coupled manifold is used and the noise model remains compatible.

```text
matched coupled manifold: COMPATIBLE_WITH_MATCHED_MODEL
nominal uncoupled manifold: MISMATCHED_MODEL
data decoupling: REQUIRES_NOISE_REEVALUATION
rank-deficient coupling transform: MAY_REDUCE_OBSERVABLE_RANK
```

A measured/embedded full-wave manifold that already includes coupling shall not receive the same coupling block again.

---

## 14. Colored-noise compatibility

Standard unwhitened classical MUSIC assumes an isotropic white-noise population eigenspace structure.

If

\[
\mathbf R_n\neq\sigma^2\mathbf I,
\]

then ordinary classical MUSIC is not automatically compatible.

If \(\mathbf R_n\succ0\) is known/estimated and whitening is scientifically valid,

\[
\mathbf y_w=\mathbf R_n^{-1/2}\mathbf y,
\qquad
\mathbf a_w=\mathbf R_n^{-1/2}\mathbf a,
\]

then a whitened MUSIC profile may be used.

```text
unwhitened classical MUSIC: INCOMPATIBLE / DEGRADED depending declared approximation
whitened MUSIC: COMPATIBLE if whitening model valid
```

---

## 15. Receiver-noise stage compatibility

Noise injected at different physical stages can undergo different downstream transforms.

A final covariance that happens to be approximately white may remain compatible with the baseline estimator even if its physical origin is complex.

Conversely, physically independent pre-coupling/pre-gain noises can become colored after cross-channel transforms.

Compatibility shall be assessed from the covariance/statistical model at the estimator's data plane, not solely from component-level noise labels.

---

## 16. Fixed channel delay compatibility

A fixed differential channel delay has multiple regimes.

### Narrowband/frequency-frozen regime

If

\[
2\pi\nu_{\max}\Delta\tau_{\rm ch}
\]

is sufficiently small under a validated narrowband profile, delay may reduce to a channel phase term at the declared frequency.

```text
compatibility: COMPATIBLE_WITH_MATCHED_MODEL
```

### Broadband regime

A static phase-only manifold is insufficient.

```text
compatibility: REQUIRES_WIDEBAND_PROCESSING or time-domain delay correction
```

No fixed phase matrix shall silently stand in for broadband delay.

---

## 17. Fixed sampling skew compatibility

For one narrowband tone/frequency, a fixed sampling-time offset can appear as a deterministic channel phase factor.

For broadband signals, a true sample-time offset changes the sampled waveform and generally requires deskew/interpolation.

```text
narrowband bounded approximation: possibly COMPATIBLE_WITH_MATCHED_MODEL
broadband physical timing profile: REQUIRES_RESAMPLING_OR_DESKEW
```

The sign convention remains distinct from physical waveform delay as established in 3.6.

---

## 18. SRO compatibility

Differential sample-rate offset produces a time-growing sampling-grid error.

A single fixed steering vector over a long covariance window is generally invalid.

```text
fixed-manifold classical MUSIC: INCOMPATIBLE beyond validated negligible-drift window
required: resampling/time-base correction, shorter stationary window, or time-varying model
```

No constant phase correction is accepted as a general SRO solution.

---

## 19. CFO / receiver frequency-reference compatibility

Differential CFO produces time-varying relative channel phase.

```text
fixed-manifold classical MUSIC: incompatible when phase drift is non-negligible over covariance window
```

A common oscillator factor may cancel in simultaneous covariance, but TDM MIMO can convert common time evolution into virtual-channel relative phase.

Compatibility therefore depends on acquisition architecture and covariance window.

---

## 20. Timing jitter compatibility

Random channel timing jitter is not a fixed deterministic manifold perturbation.

At sufficiently small jitter it may be represented by a validated additional noise/error model for a specific signal regime.

At larger jitter or high input frequency it can materially degrade phase coherence.

```text
baseline ideal classical MUSIC: jitter not active
imperfect profile: requires declared jitter statistical model and validation
```

No universal `jitter is white phase noise` assumption is accepted.

---

## 21. DC offset compatibility

A constant channel offset can create a rank-one term in an uncentered second moment.

If data are correctly centered and the offset is stable, much of the deterministic DC term can be removed.

```text
uncentered covariance profile: potentially INCOMPATIBLE / spurious mode
centered stable-offset profile: may be COMPATIBLE after declared centering/correction
```

Drift, finite-sample mean error, or signal DC content require separate treatment.

---

## 22. I/Q imbalance compatibility

A general I/Q-impaired response

\[
\mathbf y=\mathbf A\mathbf x+\mathbf B\mathbf x^*+\mathbf d
\]

is widely linear rather than ordinary complex linear.

If \(\mathbf B\neq0\) materially,

```text
ordinary classical MUSIC: not automatically compatible
required: correction that removes conjugate response, or augmented/widely-linear estimator profile
```

A simple complex-gain manifold update does not generally absorb the conjugate term.

---

## 23. Nonlinearity/compression compatibility

If receiver response depends nonlinearly on input amplitude or joint source state, superposition

\[
\mathbf x=\sum_q\mathbf a_q s_q
\]

can fail.

```text
classical linear covariance MUSIC: INCOMPATIBLE outside validated linear operating region
```

A calibrated small-signal linearization is valid only within its declared operating domain.

Compression/intermodulation/clipping shall not be silently represented as one fixed manifold matrix.

---

## 24. ADC clipping compatibility

Clipping is nonlinear and information destroying.

```text
classical floating linear profile: INCOMPATIBLE when clipping occurs materially
```

A run shall expose clipping/overrange state rather than proceed as if only SNR changed.

Post-clipping digital scaling cannot reconstruct clipped information.

---

## 25. High-resolution quantization compatibility

Under a validated high-resolution, no-overload approximation where quantization error is adequately modeled as small additive noise, classical covariance methods may remain approximately compatible.

```text
status: DEGRADED_APPROXIMATION / COMPATIBLE under declared quantization-noise assumptions
```

The ADC resolution/FSR/utilization assumptions shall be explicit.

The ideal Phase-1 profile remains unquantized to avoid embedding this approximation in the scientific foundation.

---

## 26. Coarse / one-bit quantization compatibility

For coarse or one-bit measurements, the high-resolution additive-noise approximation is invalid.

```text
ordinary classical covariance MUSIC on raw codes: INCOMPATIBLE by default
required: specialized quantized/correlation reconstruction or one-bit MUSIC profile
```

Such profiles are deferred rather than silently coerced into the baseline estimator.

---

## 27. Direct measured/CST manifold compatibility

A measured/CST-derived complex manifold can be fully compatible with classical MUSIC when:

1. it represents the same data reference plane;
2. coordinate/direction conventions are registered;
3. channel/port identity matches;
4. frequency/polarization/range/state are within the calibrated domain;
5. interpolation is valid at the requested source state;
6. included effects prevent double counting;
7. coherent complex phase is preserved;
8. the remaining receiver/statistical assumptions satisfy the MUSIC profile.

Therefore

```text
measured/CST manifold source: not inherently incompatible
matched, registered direct manifold: COMPATIBLE_WITH_MATCHED_MODEL
out-of-domain or wrong-plane manifold: INCOMPATIBLE / OUTSIDE_CALIBRATION_DOMAIN
```

---

## 28. Calibration compatibility

A calibration artifact shall not be applied merely because its matrix shape matches the data.

Compatibility requires:

```text
reference-plane match
frequency/state domain match
channel/port identity match
hardware/gain/termination state match
absolute/relative gauge compatibility
included/de-embedded effects compatibility
interpolation/extrapolation validity
time validity / drift status
```

Failure of any material condition can invalidate the calibration.

---

## 29. Calibration correction versus calibrated-manifold use

### Model calibration

If the physical covariance remains uncorrected and MUSIC uses a matched calibrated manifold:

```text
compatibility depends primarily on matched manifold + physical noise/statistics
```

### Data correction

If data are transformed by \(\mathbf C\):

\[
\mathbf R_{\rm corr}=\mathbf C\mathbf R\mathbf C^H,
\]

then noise and covariance compatibility must be re-evaluated.

Thus `calibrated=true` shall not hide whether calibration was model-side or data-side.

---

## 30. Active-channel digital mask compatibility

Post-acquisition digital selection

\[
\mathbf y_{\rm sel}=\mathbf S_{\rm mask}\mathbf y
\]

can define a reduced array view when the corresponding reduced manifold and covariance are selected consistently.

```text
compatibility: possible with stable physical-channel mapping
```

The reduced geometry/manifold shall preserve physical channel identity.

---

## 31. Physical port-state change compatibility

Opening, shorting, disabling, or reterminating a physical antenna/receiver port can alter coupling/loading and therefore the response of other channels.

```text
digital subset of a calibrated full physical state: potentially compatible
changed physical port/termination state: prior calibration/manifold may be INVALID
```

A digital mask shall never be used as a semantic substitute for physical port configuration.

---

## 32. Source correlation compatibility

Ordinary MUSIC can accommodate statistically correlated sources while the source covariance remains full rank and the signal-subspace dimension remains sufficient.

For fully coherent sources, \(\mathbf R_s\) can lose rank.

```text
full-rank source covariance: potentially compatible
rank-deficient coherent sources: classical covariance MUSIC may fail / requires spatial smoothing or specialized profile
```

This is a source-statistics compatibility issue, not a sensor-calibration failure.

---

## 33. Model-order compatibility

The noise projector requires a scientifically appropriate signal-subspace dimension.

If

\[
\hat q\neq q_{\rm observed},
\]

then the projector is structurally mispartitioned.

```text
compatibility: requires valid model-order/source-subspace selection
```

GeoDOA shall keep source count and observed subspace rank distinct.

---

## 34. Finite-sample compatibility

Finite snapshots do not make classical MUSIC scientifically incompatible by themselves.

They increase sample-covariance/eigenspace uncertainty and may impose rank limits.

```text
status: COMPATIBLE but finite-sample performance-limited
```

provided the sample covariance is mathematically defined for the selected profile.

Very small snapshot counts can make requested subspace dimension impossible; such states require explicit failure/status handling.

---

## 35. Mean-centering compatibility

If centered covariance is selected, the rank ceiling

\[
\operatorname{rank}(\hat{\mathbf R})\le\min(N,L-1)
\]

must be compatible with the desired signal/noise subspace split.

If \(L-1<q\), the requested centered sample-covariance profile cannot support the assumed signal-subspace dimension.

This is an algebraic compatibility condition.

---

## 36. Wideband compatibility

A frequency-dependent manifold

\[
\mathbf a(\theta,f)
\]

cannot be replaced by one narrowband vector when bandwidth/aperture delay violates the accepted narrowband condition.

```text
narrowband MUSIC profile: INCOMPATIBLE
required: frequency-bin/incoherent/coherent wideband or time-domain profile
```

The chosen wideband algorithm is outside the initial ADR-003 profile.

---

## 37. Near-field compatibility

A near-field source requires a position/range-dependent manifold

\[
\mathbf a(\mathbf r_s,f).
\]

Using a far-field directional search manifold is a model mismatch.

```text
far-field initial profile: OUTSIDE_PROFILE
future near-field matched manifold profile: potentially compatible with corresponding subspace estimator
```

---

## 38. Polarimetric/vector-sensor compatibility

A scalar manifold cannot represent arbitrary vector-sensor outputs or polarization coupling.

```text
scalar initial profile: OUTSIDE_PROFILE for vector/polarimetric sensor measurement
future augmented/vector manifold profile: required
```

A scalar projection onto one declared polarization can remain valid as a bounded specialization.

---

## 39. MIMO virtual-array compatibility

A MIMO virtual array may be processed by a MUSIC-like estimator only if its virtual-channel measurements satisfy the declared coherent snapshot/manifold assumptions.

Required checks include:

- stable \((\mathrm{Tx}_i,\mathrm{Rx}_j)\) provenance;
- waveform orthogonality/separation assumptions;
- Tx/Rx phase calibration;
- TDM timing/LO phase evolution;
- compatible virtual-manifold construction;
- no silent mixing of simultaneous and sequential physical epochs.

The ideal receive-array Phase-1 profile shall not automatically claim MIMO-TDM compatibility.

---

## 40. Compatibility matrix

The following table is a scientific summary, not an exhaustive API contract.

| Effect/state | Baseline classical MUSIC with nominal manifold | Matched/calibrated classical MUSIC | Required alternate handling |
|---|---|---|---|
| No deterministic imperfection | Compatible | Compatible | None |
| Static position error | Mismatched/degraded | Compatible with regenerated manifold | Calibration if unknown |
| Static gain/phase mismatch | Mismatched/degraded | Compatible with matched manifold | Optional data correction + noise re-evaluation |
| Fixed narrowband channel delay | Mismatched/degraded | Compatible with matched phase/delay model | Wideband correction if bandwidth matters |
| Static scalar element response | Mismatched if omitted | Compatible with matched manifold | Vector/polarimetric profile if scalar model insufficient |
| Static linear coupling/loading | Mismatched/degraded | Compatible with coupled manifold if noise model valid | Decoupling may require whitening/noise update |
| Colored/unequal noise | Baseline assumption violated | Not fixed by manifold alone | Whitening/generalized profile |
| Fixed narrowband sampling skew | Mismatched if omitted | Approx. compatible if phase specialization valid | Deskew for broadband |
| Differential SRO | Fixed manifold eventually invalid | Not solved by static manifold | Resampling/time-varying profile |
| Differential CFO | Fixed manifold eventually invalid | Not solved by static manifold | Synchronization/time-varying profile |
| Stable DC offset | Can create spurious mode uncentered | Potentially compatible after centering/correction | Drift-aware handling if nonstationary |
| I/Q conjugate imbalance | Ordinary model violated | Complex-gain manifold insufficient generally | Widely-linear correction/augmented statistics |
| Nonlinear compression | Linear model violated | Static manifold insufficient generally | Linear-region restriction/special nonlinear model |
| Clipping | Incompatible | Calibration cannot restore lost info | Reject/flag/specialized treatment |
| High-resolution ADC quantization | Approx. compatible under assumptions | Approx. compatible | Quantization-noise model |
| One-bit/coarse quantization | Incompatible by default | Standard calibrated manifold insufficient | Specialized quantized estimator |
| Measured/CST complex manifold | Nominal may be mismatched | Compatible if registered/in-domain/matched | Reject if plane/domain/provenance invalid |
| Coherent sources | Rank problem possible | Sensor calibration alone insufficient | Spatial smoothing/specialized estimator |
| Time-varying sensor state | Static covariance model may fail | Static matched manifold insufficient | State-aware/short-window/time-varying processing |
| Near-field source | Far-field profile mismatched | Requires near-field manifold | Near-field profile |
| Wideband source | Narrowband profile mismatched | Single manifold insufficient | Wideband profile |

---

## 41. Compatibility vector

A future run shall conceptually return a vector rather than only one Boolean:

\[
\boxed{
\mathbf c
=
(c_{\rm manifold},
 c_{\rm plane},
 c_{\rm coord},
 c_{\rm bandwidth},
 c_{\rm stationarity},
 c_{\rm snapshot},
 c_{\rm linearity},
 c_{\rm complex},
 c_{\rm noise},
 c_{\rm quant},
 c_{\rm calibration},
 c_{\rm port},
 c_{\rm rank},
 c_{\rm domain},
 \ldots).
}
\]

The profile-level decision is a policy over this vector.

This structure prevents a system from reporting `compatible` merely because the manifold dimensions match.

---

## 42. Profile-level decision hierarchy

A conceptual policy is:

### 42.1 Compatible

All mandatory assumptions of the selected estimator profile are satisfied.

### 42.2 Compatible with required preprocessing/model update

The data can be made compatible by a declared transformation that preserves a scientifically valid estimator model, such as:

- matched manifold calibration;
- whitening;
- deskew/resampling;
- de-embedding;
- channel selection with matched reduced manifold.

### 42.3 Degraded approximation

The selected profile is used outside exact assumptions but within a separately validated approximation regime.

The approximation and diagnostic shall be explicit.

### 42.4 Incompatible / reject

A required assumption is materially violated and no selected preprocessing/profile resolves it.

### 42.5 Unresolved

Insufficient metadata/evidence exist to assess compatibility.

`UNRESOLVED` shall not be silently converted to `COMPATIBLE`.

---

## 43. Warning versus rejection policy

A warning is appropriate when:

- the model remains mathematically defined;
- the approximation is intentional;
- diagnostics quantify the departure;
- the profile permits degraded operation.

A rejection is appropriate when:

- required reference-plane/channel mapping is unknown;
- requested state is outside calibration domain without allowed extrapolation;
- clipping invalidates the linear model;
- a scalar estimator receives incompatible vector/augmented data semantics;
- required covariance rank/subspace dimension is impossible;
- an operation would double-count a physical effect;
- timing/grid incompatibility invalidates snapshot semantics;
- metadata are insufficient to determine a scientifically meaningful interpretation.

The exact runtime policy is deferred to software design.

---

## 44. No silent coercion rule

GeoDOA shall not silently:

- normalize away a physically meaningful amplitude mismatch;
- convert colored noise to white-noise assumption;
- treat one-bit data as high-resolution float samples;
- treat time-varying SRO/CFO as one constant phase;
- treat transmit far-field exports as receive manifolds without conversion;
- treat a measured/CST grid point outside domain as nearest calibrated truth;
- treat a digital mask as a physical port-state model;
- treat a rank-deficient source covariance as full-rank independent sources;
- treat I/Q conjugate leakage as ordinary complex gain;
- treat clipping as additive noise;
- apply coupling twice because both a direct manifold and coupling matrix are present.

Incompatible semantics shall produce a visible status, warning, or rejection according to the selected profile.

---

## 45. Compatibility and uncertainty

A calibration/model may be technically inside its nominal domain but have high uncertainty near boundaries, nulls, weak eigengaps, or poorly observed parameter states.

Therefore compatibility and confidence are distinct:

\[
\boxed{
\text{compatible}
\not\Rightarrow
\text{accurate/high-confidence}.
}
\]

A profile may be scientifically compatible while performance is poor because SNR, snapshots, eigengap, source separation, or calibration uncertainty are unfavorable.

---

## 46. Compatibility and identifiability

A calibration parameter need not be uniquely physically identifiable for a direct aggregate manifold to be estimator-compatible.

For example, coupling versus embedded-pattern decomposition may be unidentifiable, while the directly measured aggregate manifold is sufficiently matched for MUSIC.

Thus:

\[
\boxed{
\text{physical-cause identifiability}
\neq
\text{estimator manifold compatibility}.
}
\]

Conversely, a physically interpretable parameter estimate does not guarantee a sufficiently matched estimator manifold if residual/model-form error remains large.

---

## 47. Compatibility and calibration residuals

A calibrated profile shall retain residual mismatch metrics from 3.11 and subspace/MUSIC diagnostics from 3.12.

Compatibility is an assumption/status decision; residual metrics quantify degree of mismatch.

No universal residual threshold is accepted in 3.13. Thresholds belong to validated bounded profiles and ADR-004 evidence.

---

## 48. Compatibility and finite-sample performance

A run may satisfy all physical compatibility requirements yet fail to resolve sources due to:

- low SNR;
- too few snapshots;
- small eigengap;
- close source separation;
- source correlation;
- poor model-order selection;
- coarse scan grid.

These are performance/failure outcomes, not evidence that the sensor calibration contract was semantically incompatible.

---

## 49. Compatibility and reproducibility

Every compatibility decision shall be reproducible from declared profile metadata.

A future run record shall retain enough information to reconstruct:

```text
selected estimator profile
sensor profile
active imperfection families
calibration artifact/version
reference planes
channel/port state
frequency/bandwidth
snapshot/time-window semantics
noise model
quantization regime
source-statistics assumptions
preprocessing chain
compatibility vector/statuses
warnings/rejections/approximations
```

Formal reproducibility governance belongs to ADR-004.

---

## 50. Initial Phase-1 compatibility contract

The initial ADR-003 Phase-1 profile is compatible with classical unwhitened MUSIC only when all of the following hold:

\[
\boxed{
\begin{aligned}
&\text{far-field narrowband source model},\\
&\text{fixed nominal=physical geometry},\\
&\text{ideal identical scalar elements},\\
&\text{no coupling distortion},\\
&\text{unity differential electronics},\\
&\text{common coherent timing/reference},\\
&\text{simultaneous-equivalent snapshots},\\
&\text{linear receiver},\\
&\text{ordinary proper-complex statistics},\\
&\text{white equal-variance additive noise},\\
&\text{unquantized/no-overload measurement},\\
&\text{valid source-subspace dimension},\\
&\text{matching ADR-001/ADR-002 manifold/reference conventions}.
\end{aligned}}
\]

This is the profile proposed for initial implementation after ADR acceptance.

---

## 51. Initial Phase-1 exclusions

The initial profile explicitly excludes authoritative implementation of:

- sensor position perturbation;
- electronic gain/phase mismatch;
- channel delay mismatch;
- mutual coupling;
- non-ideal element patterns;
- polarization mismatch;
- measured/CST direct manifolds;
- colored noise whitening;
- sample skew/SRO/CFO/jitter;
- I/Q imbalance;
- nonlinear receiver effects;
- clipping;
- ADC quantization;
- near-field sources;
- wideband processing;
- vector/polarimetric sensors;
- TDM-MIMO synchronization effects;
- adaptive/online calibration;
- self-calibration;
- one-bit/coarse-quantized estimators.

These scientific contracts are explored now so later extensions do not require changing foundational semantics.

---

## 52. Deferred profile activation rule

An excluded imperfection family may later become authoritative only through a bounded profile that declares:

1. physical/operator model;
2. parameter units and domain;
3. reference plane;
4. calibration semantics if any;
5. estimator compatibility requirements;
6. deterministic reference checks;
7. failure/boundary behavior;
8. validation protocol;
9. provenance/reproducibility contract;
10. effect on downstream covariance/DOA metrics.

No family becomes active merely because an optional software parameter exists.

---

## 53. Incremental activation order

A scientifically useful later progression is:

```text
ideal baseline
  -> one static diagonal gain/phase family
  -> one static geometry/position family
  -> one static coupling family
  -> matched measured/CST manifold family
  -> colored-noise/whitening family
  -> timing/delay family
  -> IQ/augmented family
  -> quantized family
  -> time-varying/wideband/near-field families
```

This order is a candidate engineering progression, not an accepted roadmap commitment.

The governing principle is one-family-at-a-time validation before compound realistic profiles.

---

## 54. Compound imperfection profiles

Once individual families are validated, compound profiles may activate multiple effects.

Their composition shall obey the typed operator/reference-plane ordering from 3.8.

A compound profile requires new validation because effects can interact nonlinearly or noncommutatively.

Passing isolated single-family tests does not prove that the combined profile is valid.

---

## 55. Compatibility test seeds

The following are candidate deterministic checks for later formal promotion; they are not Gate-E PASS evidence yet.

### CT-1 — Ideal profile

Under Phase-1 ideal assumptions:

\[
\boxed{
\mathbf a_{\rm phys}=\mathbf a_{\rm nom},
\qquad
\mathbf R_{\rm phys}=\mathbf R_{\rm nominal}.
}
\]

Expected compatibility: classical MUSIC compatible.

### CT-2 — Static common phase

For

\[
\mathbf a'=e^{j\phi}\mathbf a,
\]

population covariance is unchanged.

Expected compatibility: invariant for ordinary covariance MUSIC under the bounded linear model.

### CT-3 — Static relative phase mismatch

Use GRP-015 seed.

Expected:

```text
nominal manifold -> mismatched/degraded
matched gain/phase manifold -> compatible
```

### CT-4 — Static coupling

Use GRP-016/017.

Expected:

```text
nominal manifold -> leakage 0.2 in rank-one seed
matched coupled manifold -> population orthogonality restored
```

### CT-5 — Colored noise

Use a non-scalar positive-definite \(\mathbf R_n\).

Expected:

```text
unwhitened baseline classical MUSIC -> noise-model incompatibility
properly whitened data + manifold -> compatible whitened profile
```

### CT-6 — Time-varying operator

Use the 3.12 alternating rank-one response example.

Expected: fixed-manifold compatibility fails over the mixed covariance window.

### CT-7 — One-bit measurement

Expected: high-resolution additive quantization-noise compatibility rejected.

### CT-8 — Calibration domain mismatch

Request manifold outside calibrated direction/frequency/state domain.

Expected: `OUTSIDE_CALIBRATION_DOMAIN`, not silent interpolation/extrapolation.

---

## 56. Compatibility decision provenance

A compatibility result shall eventually record:

```text
profile ID/version
input data/reference plane
sensor/manifold artifact identity
calibration artifact identity
active physical state
compatibility dimensions evaluated
status per dimension
preprocessing required/performed
warnings/approximations
rejection reasons
scientific assumptions
software/Git provenance
```

This provenance is required so a later result can explain why one run was accepted and another rejected.

---

## 57. Separation from software architecture

This exploration constrains scientific behavior but does not yet accept:

- final class names;
- final enum names;
- configuration-file schema;
- GUI controls;
- plugin interfaces;
- exception classes;
- serialization format.

Those shall be designed only after the scientific contract is accepted and reconciled with repository architecture.

---

## 58. Cross-ADR boundary

ADR-003 owns:

- sensor imperfection semantics;
- calibration semantics;
- direct manifold semantics;
- estimator compatibility implications caused by sensor/receiver state.

ADR-004 shall own formal:

- deterministic/Monte Carlo validation execution;
- seeds/reproducibility procedures;
- pass/fail thresholds;
- sweep definitions;
- reporting/evidence artifacts.

Estimator implementation ADRs/work packages shall own algorithmic details beyond the compatibility contracts needed here.

---

## 59. Boundary and failure conditions reserved for later gates

Compatibility logic must later be stress-tested for at least:

- missing calibration provenance;
- wrong reference plane;
- wrong channel order;
- invalid coordinate registration;
- out-of-domain measured/CST manifold;
- double-counted coupling/element response;
- physically changed port/termination state;
- calibration artifact from wrong gain/temperature/hardware state;
- static manifold used across material SRO/CFO/drift;
- colored noise passed to unwhitened baseline profile;
- singular/ill-conditioned whitening covariance;
- rank-deficient sensor transform;
- insufficient sample-covariance rank;
- coherent-source rank collapse;
- wrong model order;
- widely-linear data passed to ordinary covariance profile;
- clipped/nonlinear measurements passed to linear profile;
- coarse/one-bit quantization passed to high-resolution profile;
- near-field data passed to far-field profile;
- wideband data passed to narrowband profile;
- vector/polarimetric data passed to scalar profile;
- TDM-MIMO data treated as simultaneous without timing-phase reconciliation;
- extrapolation silently treated as calibration;
- `UNRESOLVED` metadata silently promoted to compatible.

These are exploration requirements, not Gate F PASS evidence.

---

## 60. Candidate decisions from Exploration 3.13

- **3.13-D1** — Estimator compatibility is multi-axis and profile-specific, not one Boolean.
- **3.13-D2** — Compatibility dimensions shall separately include manifold, reference plane, coordinates, bandwidth, stationarity, snapshot coherence, linearity, complex-statistics representation, noise, covariance, quantization, calibration, port state, rank/model order, domain/interpolation, and preprocessing semantics.
- **3.13-D3** — Compatibility statuses shall distinguish exact compatibility, required model/preprocessing changes, degraded approximation, out-of-domain state, incompatibility, unresolved state, and not-assessed state.
- **3.13-D4** — The baseline classical MUSIC compatibility profile is narrowband, fixed-manifold, simultaneous-equivalent, ordinary complex-linear, white-noise, no-overload, and matched-manifold.
- **3.13-D5** — The initial Phase-1 deterministic sensor-imperfection graph is identity under explicitly ideal assumptions.
- **3.13-D6** — Initial Phase-1 uses nominal=physical geometry, ideal identical scalar elements, no coupling, unity electronics, coherent timing/reference, linear unquantized receiver, and white equal-variance additive noise.
- **3.13-D7** — The initial profile explicitly records no-required/identity calibration semantics rather than leaving calibration state ambiguous.
- **3.13-D8** — Validated profiles shall declare active physics; GeoDOA shall not use one generic `realistic_sensor` switch.
- **3.13-D9** — Static deterministic complex-linear manifold imperfections can remain compatible with classical MUSIC when a matched physical/calibrated manifold is supplied and other assumptions remain valid.
- **3.13-D10** — Nominal-manifold processing of physically mismatched data shall be labeled mismatched/degraded rather than silently treated as matched MUSIC.
- **3.13-D11** — Static calibrated geometry/position error is compatible with matched-manifold classical MUSIC; time-varying deformation may invalidate a fixed-manifold profile.
- **3.13-D12** — Fixed gain/phase mismatch is compatible with a matched manifold; inverse data correction requires noise/statistics re-evaluation.
- **3.13-D13** — Common phase is covariance-invariant in the bounded linear ordinary-covariance model; common gain may still matter through physical dynamic-range/SNR stages.
- **3.13-D14** — Scalar complex element-pattern mismatch can be incorporated into a matched manifold; vector/polarimetric effects may require a different estimator representation.
- **3.13-D15** — Fixed linear coupling/loading is compatible with a matched coupled manifold if noise/statistical assumptions remain valid.
- **3.13-D16** — Colored/unequal noise violates the baseline unwhitened MUSIC noise model; a valid whitening/generalized profile may restore compatibility.
- **3.13-D17** — Compatibility of receiver noise is assessed at the estimator data plane after physical downstream transforms, not by source-label semantics alone.
- **3.13-D18** — Fixed channel delay may reduce to matched narrowband phase only in a validated narrowband regime; broadband delay requires wideband/time-domain handling.
- **3.13-D19** — Fixed sampling skew may admit a narrowband phase specialization but broadband skew requires deskew/interpolation semantics.
- **3.13-D20** — Differential SRO is not generally compatible with one static manifold over long windows and requires time-base correction or a bounded stationary window.
- **3.13-D21** — Differential CFO can invalidate fixed-manifold covariance processing; common reference evolution can become relative in TDM MIMO.
- **3.13-D22** — Timing jitter requires a declared stochastic approximation/profile and is not silently modeled as one universal white phase-noise term.
- **3.13-D23** — Stable DC offset can create spurious covariance modes in uncentered statistics; centering/correction may restore compatibility only under declared assumptions.
- **3.13-D24** — Material I/Q conjugate imbalance requires correction or augmented/widely-linear processing; a complex-gain-only manifold is insufficient generally.
- **3.13-D25** — Material compression/nonlinearity invalidates the baseline linear-superposition MUSIC profile outside a validated linear region.
- **3.13-D26** — ADC clipping is an incompatibility/failure state for the baseline linear profile and is not corrected by post-acquisition scaling.
- **3.13-D27** — High-resolution quantization may be a declared degraded/additive-noise approximation; the initial Phase-1 profile remains unquantized.
- **3.13-D28** — Coarse/one-bit quantization requires a specialized quantized-statistics estimator profile and is not silently accepted by ordinary covariance MUSIC.
- **3.13-D29** — Measured/CST complex manifolds can be fully compatible with classical MUSIC when registered, in-domain, coherent, reference-plane matched, and free of double counting.
- **3.13-D30** — Calibration compatibility requires reference-plane, domain, channel, hardware/state, gauge, included-effects, interpolation, and time-validity agreement.
- **3.13-D31** — Model calibration and data correction remain distinct compatibility paths because data correction transforms covariance/noise statistics.
- **3.13-D32** — Digital channel selection can define a compatible reduced array when the reduced manifold/covariance preserve stable physical identity.
- **3.13-D33** — Physical port/termination changes can invalidate prior coupling/manifold calibration even when the digital channel set appears similar.
- **3.13-D34** — Source coherence/rank deficiency is a source-statistics compatibility problem and is not repaired by sensor calibration alone.
- **3.13-D35** — Valid model-order/subspace-dimension selection is an independent compatibility requirement.
- **3.13-D36** — Finite snapshots are performance-limiting rather than automatically incompatible, subject to algebraic covariance/subspace rank feasibility.
- **3.13-D37** — Mean-centered sample covariance requires \(L-1\) rank capacity compatible with requested signal-subspace dimension.
- **3.13-D38** — Wideband data are outside the single-manifold narrowband profile when aperture-delay/bandwidth assumptions fail.
- **3.13-D39** — Near-field sources are outside the initial far-field profile and require a range/position-dependent manifold profile.
- **3.13-D40** — Vector/polarimetric sensor measurements are outside the initial scalar profile unless reduced to a declared scalar specialization.
- **3.13-D41** — MIMO/TDM data require explicit Tx/Rx provenance and temporal coherence/calibration before a virtual-array MUSIC profile is declared compatible.
- **3.13-D42** — Compatibility shall be represented conceptually as a vector of scientific statuses, with a profile policy determining the aggregate decision.
- **3.13-D43** — `UNRESOLVED` shall never be silently promoted to `COMPATIBLE`.
- **3.13-D44** — Warning is appropriate only for intentional/diagnosed approximations; material semantic violations require rejection or another profile.
- **3.13-D45** — GeoDOA shall prohibit silent coercions that erase amplitude, noise color, timing variation, quantization regime, reference-plane mismatch, source-rank loss, or double-counted sensor physics.
- **3.13-D46** — Compatibility and confidence/performance are distinct; a compatible profile can still perform poorly under low SNR, weak eigengap, few snapshots, or high uncertainty.
- **3.13-D47** — Physical-cause identifiability and estimator-manifold compatibility are distinct; aggregate direct calibration may be estimator-compatible without unique causal decomposition.
- **3.13-D48** — Calibration residual metrics quantify degree of mismatch but do not replace profile compatibility semantics.
- **3.13-D49** — Compatibility decisions shall preserve reproducible profile, sensor, calibration, state, noise, quantization, preprocessing, and status provenance.
- **3.13-D50** — The initial Phase-1 profile explicitly excludes authoritative implementation of nonideal sensor/receiver families even though their scientific contracts are explored.
- **3.13-D51** — A deferred imperfection family becomes authoritative only through a bounded validated profile, not merely by exposing a software parameter.
- **3.13-D52** — Individual imperfection families should be validated before compound profiles; compound profiles require new interaction validation.
- **3.13-D53** — Compatibility test seeds are exploration evidence only and shall be promoted to formal GRPs/tests at Gate E when the final ADR contract is stable.
- **3.13-D54** — ADR-003 compatibility semantics constrain later software behavior but do not yet accept final classes, enums, schemas, GUI controls, or exceptions.

---

## 61. Immediate next step

The next work session shall start at **Exploration 3.14 — Cross-Section Reconciliation and Candidate ADR-003 Contract**.

Exploration 3.14 must perform a full consistency audit across Explorations 3.1–3.13, including at least:

1. terminology consistency across nominal/physical/measured/EM/calibrated/truth objects;
2. operator ordering/reference planes;
3. coordinate/sign/phase conventions against ADR-001 and ADR-002;
4. common phase/common scale semantics;
5. geometry versus electronic phase versus delay distinctions;
6. element/coupling/embedded-pattern double-count boundaries;
7. timing/SRO/CFO/sampling sign and domain semantics;
8. ADC acquisition quantization versus FPGA/processor fixed-point separation;
9. calibration versus correction versus validation boundaries;
10. direct measured/CST manifold semantics;
11. error-metric gauge/equivalence consistency;
12. identifiability versus conditioning consistency;
13. covariance/eigenspace/MUSIC propagation consistency;
14. compatibility matrix/profile logic;
15. Phase-1 initial profile consistency;
16. deferred profile boundaries;
17. reserved GRP-014 through GRP-017 content and any additional Gate-E candidates;
18. unresolved contradictions/open decisions;
19. candidate final ADR-003 decision set;
20. readiness assessment for drafting ADR-003 and only then starting Gate A.

Do not start Gate A before 3.14 reconciliation is complete.
