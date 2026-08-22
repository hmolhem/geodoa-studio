# ADR-002 — Boundary and Failure Analysis

- **Governing ADR:** `ADR-002-wave-propagation-signal-measurement-model.md`
- **Phase:** 0C — Scientific Foundations
- **Gate:** F — Boundary and Failure Analysis
- **Status:** Complete — candidate evidence for Gate F PASS

## 1. Purpose

ADR-002 governs wave, propagation, measurement, snapshot, covariance, source/noise, FMCW, and MIMO scientific semantics. Gate F identifies where those semantics are invalid, underdetermined, outside PM-001, statistically incompatible, algorithmically unusable, or interpretation-limited.

The purpose is not to reject every difficult physical scenario. It is to report failure at the layer where it actually occurs.

## 2. Required Response Classes

GeoDOA shall distinguish:

- **REJECT** — the requested input/domain object/operation is scientifically undefined or inconsistent under the governing contract;
- **INCOMPATIBLE / REQUIRE OTHER MODEL** — the physical scenario is meaningful but the requested profile/model/algorithm is insufficient;
- **DIAGNOSTIC / WARN** — computation may proceed, but ambiguity, aliasing, conditioning, approximation sensitivity, or interpretation limitations must remain explicit;
- **VALID** — the condition lies within the declared contract.

A physically valid scene shall not be rejected merely because PM-001 or a particular DOA estimator cannot represent it.

## 3. Failure-Layer Hierarchy

The preferred diagnostic order is:

```text
Domain/input validity
    -> physical-model compatibility
    -> propagation-approximation compatibility
    -> measurement-construction compatibility
    -> statistical-model compatibility
    -> structural identifiability
    -> finite-sample feasibility/conditioning
    -> algorithm applicability
    -> spectrum/peak interpretation
```

A later-layer estimator failure shall not be used to hide an earlier structural/model incompatibility.

## 4. Wave/Frequency/Medium Boundaries

### F-001 — Invalid physical carrier frequency

PM-001 requires a positive finite physical carrier.

**Required behavior:** `REJECT` nonfinite or nonpositive physical `f_c`. Negative baseband/spectral offsets remain valid under their own semantics.

### F-002 — Bandwidth boundaries

`B < 0` is invalid. `B = 0` is a valid CW edge case.

**Required behavior:**

- negative bandwidth: `REJECT`;
- zero bandwidth: `VALID` for CW/narrowband spatial modeling;
- do not claim bandwidth-based range resolution for `B = 0`.

### F-003 — Invalid propagation speed

PM-001 requires finite `v > 0`.

**Required behavior:** `REJECT` nonfinite or nonpositive propagation speed.

### F-004 — Medium outside PM-001

Dispersive, lossy, inhomogeneous, or anisotropic media are meaningful physical models but outside PM-001.

**Required behavior:** `INCOMPATIBLE / REQUIRE OTHER MODEL`, not geometry rejection.

### F-005 — Negative attenuation in a declared passive-loss model

**Required behavior:** `REJECT` `alpha < 0` when `alpha` is explicitly a passive attenuation/loss coefficient. This rule does not claim that active/gain media are physically impossible; such media require a different model.

## 5. Path and Far-/Near-Field Boundaries

### F-006 — Negative path length

**Required behavior:** `REJECT` negative physical geometric path length.

### F-007 — Coincident source/sensor and `1/R` singularity

Geometric distance `R = 0` may describe coincident points, but ideal scalar spherical spreading `1/R` is singular.

**Required behavior:** geometry may remain representable; reject/invalidate the singular point-source spreading operation or require another local model.

### F-008 — Source inside/near aperture

Exact geometry may be valid, but the expansion parameter `||delta||/R` may not be small.

**Required behavior:** exact/spherical modeling may proceed; plane-wave/far-field approximation is `INCOMPATIBLE` when compatibility is not established.

### F-009 — Plane-wave compatibility failure

When exact spherical relative paths produce material phase curvature under the declared acceptance policy, PM-001 is insufficient.

**Required behavior:** `INCOMPATIBLE / REQUIRE SPHERICAL MODEL`. Never silently promote the selected profile.

### F-010 — Missing far-field threshold policy

ADR-002 can compute curvature metrics without a universal threshold.

**Required behavior:** report metric/evidence; do not invent PASS/FAIL when no acceptance policy is declared.

### F-011 — Common phase

A common complex phase factor does not constitute spatial distortion.

**Required behavior:** computation remains `VALID`; a claim that common phase alone is manifold distortion is an invalid interpretation.

### F-012 — Zero reference response

`H_n/H_ref` is undefined for `H_ref = 0`.

**Required behavior:** `REJECT` the relative-ratio operation, not necessarily the scene. Choose a valid reference/representation explicitly.

## 6. Narrowband/Wideband Boundaries

### F-013 — Narrowband compatibility failure

If declared aperture-delay/bandwidth tolerance is exceeded, replacing true differential envelope delay by a single carrier phase is not accepted.

**Required behavior:** `INCOMPATIBLE / REQUIRE WIDEBAND MODEL`.

### F-014 — Ambiguous bandwidth semantics

If a diagnostic requires full width versus one-sided offset/occupied bandwidth and the supplied `B` meaning is unknown, the diagnostic is not reproducible.

**Required behavior:** reject the diagnostic request or return insufficient-semantics/provenance; do not guess.

### F-015 — Direction-specific narrowband validity

A scenario may be narrowband-compatible in one direction and not another.

**Required behavior:** preserve direction/scan-domain context; do not make an unconditional global `array_is_narrowband` claim.

## 7. Motion, Doppler, and Time-Scale Boundaries

### F-016 — Nonzero Doppler with stable manifold

Nonzero `f_D` alone does not invalidate PM-001's spatial manifold.

**Required behavior:** potentially `VALID` when spatial-manifold compatibility is otherwise satisfied.

### F-017 — Material manifold migration

If `A(t)` changes materially over the covariance/snapshot window, the constant-manifold model is insufficient.

**Required behavior:** `INCOMPATIBLE / REQUIRE TIME-VARYING MODEL` or shorter compatible window.

### F-018 — Range migration across a fixed range-cell snapshot construction

**Required behavior:** `INCOMPATIBLE / REQUIRE MIGRATION-AWARE SNAPSHOT CONSTRUCTION`; do not misreport this as a DOA estimator failure.

### F-019 — Acceleration invalidates constant-Doppler approximation

When declared Doppler/acceleration compatibility is exceeded, constant-Doppler modeling is insufficient.

**Required behavior:** require a time-varying Doppler/path model.

### F-020 — CPI semantics

CPI, covariance window, and tracking interval are different concepts.

**Required behavior:** reject/diagnose semantic substitution of one for another. Operations requiring a positive CPI reject nonpositive duration.

## 8. Passive/Active and FMCW Boundaries

### F-021 — Full active path requested through PM-001

PM-001 is a one-way receive-equivalent profile.

**Required behavior:** full Tx-target-Rx propagation requires another active-sensing model. A post-processed receive-equivalent spatial view may use PM-001 only with preserved transformation provenance.

### F-022 — Generic `2R` active-path shortcut

`2R/v` is a monostatic specialization.

**Required behavior:** `REJECT` generic active-path logic that multiplies an arbitrary range by two without topology/path semantics.

### F-023 — Moving active target and stop-and-hop

Evaluating both Tx and Rx legs at one common epoch is an approximation.

**Required behavior:** if target motion during the relevant propagation/measurement interval is material under the declared policy, require a more exact active-motion model.

### F-024 — Invalid chirp duration

**Required behavior:** `REJECT` `T_c <= 0` for a chirp model requiring `mu = B/T_c`.

### F-025 — Zero FMCW slope

`mu = 0` is a valid CW-like waveform edge case but does not support the standard FMCW range inversion.

**Required behavior:** waveform may be valid; `R = v|f_b|/(2|mu|)` is `INCOMPATIBLE/UNDEFINED`.

### F-026 — Echo delay outside assumed chirp support

When a delayed echo does not belong to the assumed same-chirp processing interval, the simple stationary single-chirp equation is insufficient.

**Required behavior:** require frame/inter-chirp-aware processing/model.

### F-027 — Beat frequency beyond Nyquist

If sampled beat magnitude exceeds Nyquist, aliases occur.

**Required behavior:** sampled data may remain valid, but unique beat/range inference is incompatible without additional information; emit aliasing diagnostic.

### F-028 — Moving target with stationary FMCW range formula

When path-rate/Doppler coupling is material, `f_b = mu tau` alone is insufficient.

**Required behavior:** `INCOMPATIBLE / REQUIRE MOVING-TARGET FMCW MODEL`.

### F-029 — Missing mixer/dechirp convention

Signed beat-frequency interpretation depends on mixer ordering.

**Required behavior:** magnitude-only operations may be possible where mathematically justified; signed scientific interpretation reports insufficient provenance.

### F-030 — Missing scientific/FFT sign mapping

**Required behavior:** reject signed frequency interpretation if the conversion between scientific frequency and software FFT coordinate is unspecified.

### F-031 — `fftshift` misuse

`fftshift` only reorders indices.

**Required behavior:** treat any claim that it alone changes physical frequency sign as invalid interpretation.

## 9. MIMO Boundaries

### F-032 — General bistatic physical channel

Independent Tx/Rx look directions are valid.

**Required behavior:** keep the physical pair model; do not require virtual-sum geometry.

### F-033 — Forced virtual-sum geometry outside common-look regime

**Required behavior:** `REJECT` the transformation `r_v = r_Tx+r_Rx` when its common-look/colocated far-field condition is not established.

### F-034 — Duplicate derived virtual coordinates

Different physical pairs may map to the same derived virtual coordinate.

**Required behavior:** `VALID`; retain each physical `(Tx,Rx)` identity and do not collapse pairs silently.

### F-035 — Missing MIMO pair provenance

**Required behavior:** reject a scientific virtual-channel object that cannot recover its physical Tx/Rx lineage.

### F-036 — TDM-MIMO motion

Sequential Tx measurements are not automatically simultaneous.

**Required behavior:** when motion/timing phase is material, require time-aware/calibrated simultaneous-equivalent construction before forming a virtual spatial snapshot.

## 10. Measurement-Axis and Snapshot Boundaries

### F-037 — Raw tensor with undefined axes

**Required behavior:** reject scientific operations that depend on axis meaning. Shape alone shall not identify `Rx x chirp x fast_time`.

### F-038 — Axis metadata/payload mismatch

**Required behavior:** `REJECT` inconsistent declared lengths/coordinate mappings.

### F-039 — Duplicate channel identities

**Required behavior:** reject duplicate persistent identity in one channel set unless explicit multiplexing semantics make the identities distinct at another level.

### F-040 — Zero active channels

**Required behavior:** `REJECT` spatial snapshot construction.

### F-041 — One active channel

Measurement and scalar covariance may be valid, but phase-difference DOA is not identifiable.

**Required behavior:** measurement `VALID`; directional array-processing algorithms report `INCOMPATIBLE` as appropriate.

### F-042 — Zero snapshots

**Required behavior:** `REJECT` covariance construction.

### F-043 — One snapshot

Known-zero-mean `xx^H` is defined; estimated-mean `1/(L-1)` covariance is not.

**Required behavior:** distinguish these operations explicitly.

### F-044 — Asynchronous channels claimed as simultaneous

**Required behavior:** reject snapshot construction unless a timing model/calibration establishes simultaneous equivalence.

### F-045 — Incompatible measurement units

**Required behavior:** reject common covariance/statistical construction until explicit calibration/conversion provides a compatible measurement representation.

### F-046 — Nonfinite samples

**Required behavior:** reject ordinary canonical numerical processing of NaN/Inf unless an explicit missing-data model is selected. Never silently zero-fill.

## 11. Covariance and Statistical Boundaries

### F-047 — Covariance shape mismatch

**Required behavior:** `REJECT` non-square covariance or dimensions inconsistent with the declared channel set.

### F-048 — Non-Hermitian covariance

Material non-Hermitian residual violates covariance semantics.

**Required behavior:** reject as covariance. Tiny numerical residual may receive diagnostic and an explicit repair operation; repair is not validation.

### F-049 — Non-PSD covariance

Significant negative eigenvalues violate physical covariance semantics.

**Required behavior:** `REJECT`; tiny roundoff-level negative values may be diagnostic under a declared numerical tolerance. PSD clipping is explicit repair only.

### F-050 — Zero covariance

**Required behavior:** mathematically `VALID`; interpretation follows the zero-signal/zero-noise scenario.

### F-051 — Nonzero mean called covariance without centering

**Required behavior:** reject the semantic claim. `E[xx^H]` may be stored as uncentered second moment.

### F-052 — Correlated snapshots and unbiasedness claim

The centered `1/(L-1)` statistic remains computable for `L>=2`, but correlation can invalidate the standard unbiasedness claim.

**Required behavior:** diagnostic/invalid claim unless the required statistical assumptions are established.

### F-053 — Invalid source covariance or source power

**Required behavior:** reject materially non-PSD `R_s` and negative source powers. Zero source power is a valid edge case and does not automatically contribute observable rank.

### F-054 — Invalid normalized correlation coefficient

**Required behavior:** reject `|rho| > 1`; `|rho| = 1` is valid perfect coherence and may produce rank collapse.

### F-055 — Coherent sources versus classical source-count assumption

Coherent arrivals are valid physics/statistics.

**Required behavior:** report classical full-rank source-count/MUSIC assumptions as `INCOMPATIBLE` when required; do not label the covariance invalid.

### F-056 — Signal/noise cross-correlation

If `E[s n^H] != 0`, the simplified covariance sum omits cross terms.

**Required behavior:** require an extended covariance model.

### F-057 — Colored noise

Colored `R_n` is valid.

**Required behavior:** algorithms requiring white-noise eigenspace structure report `INCOMPATIBLE` or require whitening/generalization.

### F-058 — Noise variance edge cases

Negative variance is invalid. Zero variance is an ideal valid noise-free case.

**Required behavior:** reject negative variance; allow zero variance with corresponding infinite-SNR semantics where numerator is positive.

### F-059 — Zero/zero SNR

`P_s = 0` and `sigma^2 = 0` makes ratio SNR undefined.

**Required behavior:** reject the SNR computation or represent it as undefined; never manufacture a numeric dB value.

### F-060 — Undefined SNR semantics

A bare `SNR = X dB` without numerator, denominator, measurement location, aggregation, and normalization is not publication-grade provenance.

**Required behavior:** report insufficient provenance for reproducible benchmarking.

### F-061 — Ambiguous dB conversion

**Required behavior:** reject conversion when it is unknown whether input is an amplitude or power ratio.

### F-062 — RCS versus complex reflectivity

Linear physical RCS is nonnegative and carries `m^2`; complex scattering coefficients have different semantics.

**Required behavior:** reject semantic interchange without an explicit physical conversion/model.

### F-063 — Structured interference folded into white noise

**Required behavior:** reject silent transformation; allow only as an explicitly declared approximation.

### F-064 — Silent physical-manifold normalization

**Required behavior:** reject silent normalization of calibrated/physical amplitude-bearing manifold data.

## 12. Identifiability and Algorithm Boundaries

### F-065 — Spatial aliasing

Common-phase-equivalent steering for distinct directions is a valid computed ambiguity.

**Required behavior:** computation may proceed with `DIAGNOSTIC/WARN`; unique DOA claims are invalid without additional information.

### F-066 — 1-D projection ambiguity

Distinct 3-D directions with the same observable projection remain indistinguishable to the ideal scalar 1-D manifold.

**Required behavior:** computation allowed; unique 3-D interpretation is incompatible/invalid.

### F-067 — Physical source count larger than channel count

This is a physically valid scene.

**Required behavior:** do not reject the scene; assess algorithm/observability separately.

### F-068 — Classical MUSIC signal order

A nonempty classical MUSIC noise subspace requires `r_obs < N`.

**Required behavior:** invalid order parameters are rejected; `r_obs >= N` is algorithm incompatibility, not scene invalidity.

### F-069 — Centered sample-rank feasibility

If `L-1 < r` for a requested `r`-dimensional centered sample subspace, the sample covariance cannot represent that rank.

**Required behavior:** algorithm/statistical operation `INCOMPATIBLE`. Satisfying `L-1 >= r` does not guarantee adequate estimation.

### F-070 — Close but distinct sources

Exact model identifiability may coexist with poor finite-SNR resolution.

**Required behavior:** preserve distinction between structural identifiability and practical resolvability.

### F-071 — Merged/false MUSIC peaks

**Required behavior:** classify as spectral/peak-resolution/detection failure when upstream model/order/subspace conditions were otherwise valid; do not rewrite earlier evidence.

### F-072 — Oracle model order

**Required behavior:** permitted when explicitly recorded in run provenance; do not describe the resulting pipeline as blind model-order estimation.

## 13. Workflow/Provenance Boundaries

### F-073 — Silent model promotion

**Required behavior:** reject workflow behavior that silently switches from PM-001 plane-wave to spherical/wideband/etc. after a compatibility failure.

### F-074 — Silent model degradation

**Required behavior:** reject workflow behavior that silently replaces a requested richer physical model with PM-001 approximations.

### F-075 — Missing scientific profile identity

**Required behavior:** exploratory computation may be possible, but publication-grade/reproducible claims report insufficient provenance unless profile/contract identity is recoverable.

### F-076 — Unit inference from numeric magnitude

**Required behavior:** `REJECT` magnitude-based guessing of GHz/MHz, degrees/radians, meters/wavelengths, or dB/linear semantics.

### F-077 — Silent numerical repair

**Required behavior:** reject silent Hermitian symmetrization, PSD clipping, zero filling, or other repairs presented as original-data validation. Repair provenance must be explicit.

### F-078 — Missing acceptance threshold

**Required behavior:** report the metric and the absence of a policy; do not invent PASS/FAIL.

## 14. Gate F Coverage Summary

Gate F covers:

```text
invalid wave/medium inputs
far/near approximation boundaries
narrow/wide boundaries
motion/Doppler/migration boundaries
passive/active/FMCW boundaries
FFT/mixer sign provenance
MIMO physical/virtual boundaries
raw-axis/snapshot boundaries
covariance/statistical boundaries
SNR/scaling boundaries
spatial identifiability boundaries
algorithm/sample-rank boundaries
profile/provenance/numerical-repair boundaries
```

The detailed response rules preserve one governing principle:

> A meaningful physical scenario outside the selected approximation shall require another model, not be silently converted into an apparently valid PM-001 result.
