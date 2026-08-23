# ADR-003 — Boundary and Failure Analysis

- **Governing ADR:** `ADR-003-sensor-imperfections-mutual-coupling-calibration.md`
- **Phase:** 0C — Scientific Foundations
- **Gate:** F — Boundary and Failure Analysis
- **Status:** Complete — candidate evidence for Gate F PASS
- **Prior gates:** Gates A–E PASS

## 1. Purpose

ADR-003 governs sensor/receiver imperfections, coupling/loading, timing/synchronization errors, ADC/receiver effects, calibration, measured/EM manifolds, mismatch metrics, covariance/eigenspace propagation, and estimator compatibility.

Gate F identifies where these semantics are malformed, physically meaningful but outside a selected profile, unidentifiable, poorly conditioned, outside calibration domain, statistically incompatible, or algorithmically unusable.

The purpose is not to reject every nonideal sensor. The purpose is to report failure at the layer where it actually occurs.

---

## 2. Required Response Classes

GeoDOA shall distinguish:

- **REJECT** — the requested input, artifact, transformation, or scientific claim is undefined or internally inconsistent under the governing contract;
- **INCOMPATIBLE / REQUIRE OTHER MODEL** — the physical scenario is meaningful, but the selected sensor/calibration/statistical/estimator profile is insufficient;
- **DIAGNOSTIC / WARN** — computation may proceed, but ambiguity, conditioning, approximation sensitivity, uncertainty, or interpretation limitations must remain explicit;
- **VALID** — the condition lies within the declared profile and operation domain.

`UNRESOLVED` may remain a scientific knowledge state inside compatibility/calibration reporting, but it shall never be silently promoted to `VALID` or `COMPATIBLE`.

---

## 3. Failure-Layer Hierarchy

Preferred diagnostic order:

```text
Domain/input validity
    -> unit/reference-plane/channel-identity validity
    -> physical sensor-profile compatibility
    -> timing/sampling compatibility
    -> receiver/ADC operating-region compatibility
    -> calibration-domain and provenance validity
    -> calibration identifiability / conditioning
    -> covariance/statistical compatibility
    -> eigenspace/model-order feasibility
    -> estimator applicability
    -> performance / peak interpretation
```

A downstream MUSIC failure shall not hide an upstream clipping, timing, calibration-domain, or reference-plane incompatibility.

---

# 4. Geometry and Position-Error Boundaries

### F-001 — Nonfinite physical or nominal position

**Required behavior:** `REJECT` NaN/Inf physical coordinates or position-error values in canonical scientific processing.

### F-002 — Position-error units unknown

A position perturbation cannot be inferred as meters, wavelengths, millimeters, or normalized spacing from numeric magnitude.

**Required behavior:** `REJECT` scientific application of the perturbation until units/reference frequency are explicit.

### F-003 — Position error applied by silently overwriting nominal geometry

Nominal design provenance and realized physical geometry are distinct.

**Required behavior:** `REJECT` destructive semantic overwrite when the operation claims to preserve nominal provenance. Store/derive physical geometry explicitly.

### F-004 — Far-field position-phase formula used outside established far-field regime

The exact geometry remains meaningful.

**Required behavior:** `INCOMPATIBLE / REQUIRE EXACT OR NEAR-FIELD MODEL` for the first-order far-field phase shortcut; do not reject the physical geometry.

### F-005 — Ambiguous phase-reference displacement

Using `epsilon_ref` without declaring whether the ADR-001 stable nominal reference moved recreates the Gate-A ambiguity.

**Required behavior:** `REJECT` the referenced phase-perturbation calculation until fixed-reference versus moved-reference semantics are explicit.

### F-006 — Rigid translation labeled relative-manifold distortion

Under the declared far-field model, common translation produces common phase but zero pairwise distortion.

**Required behavior:** computation may be `VALID`; the interpretation that rigid translation alone changes relative manifold is invalid and shall be rejected/diagnosed.

### F-007 — Large perturbation inserted into a first-order bias formula

**Required behavior:** retain exact physical geometry/model if available; mark first-order bias formula `DIAGNOSTIC / WARN` or `INCOMPATIBLE` under the declared approximation policy.

---

# 5. Gain/Phase and Electronic-Channel Boundaries

### F-008 — Nonfinite complex gain

**Required behavior:** `REJECT` NaN/Inf channel gain/phase parameters.

### F-009 — Negative amplitude magnitude in polar gain representation

For `g=rho exp(j phi)` with `rho` defined as magnitude, `rho < 0` is semantically invalid because the sign belongs in phase.

**Required behavior:** `REJECT` negative magnitude under this representation.

### F-010 — Zero channel gain

A physically dead/fully attenuated channel is meaningful.

**Required behavior:** sensor state may be `VALID`; exact inverse calibration of that channel is `INCOMPATIBLE / UNDEFINED`. Directional observability must be reassessed after effective rank/channel loss.

### F-011 — Common phase treated as relative mismatch

**Required behavior:** `REJECT` the semantic claim; common phase is valid but is not relative spatial distortion in the ordinary coherent covariance profile.

### F-012 — Common gain declared universally SNR-invariant

Whether common gain changes effective SNR/dynamic range depends on stage ordering relative to noise, ADC, clipping, and nonlinearities.

**Required behavior:** `REJECT` unconditional SNR-invariance claim without physical stage semantics.

### F-013 — Static electronic phase relabeled physical delay from one frequency

One-frequency phase cannot identify a unique delay slope.

**Required behavior:** `UNRESOLVED / INSUFFICIENT INFORMATION`; require multi-frequency or other physical evidence before delay interpretation.

---

# 6. Element, Orientation, and Polarization Boundaries

### F-014 — Magnitude-only pattern used as coherent complex manifold

**Required behavior:** `INCOMPATIBLE / REQUIRE COMPLEX RESPONSE OR ADDITIONAL PHASE MODEL` for coherent DOA calibration.

### F-015 — Polarization response without basis/handedness convention

**Required behavior:** reject coherent polarimetric interpretation until the transverse basis and look/propagation reference are declared.

### F-016 — Element response and receiver gain silently merged

A numerical product may be usable at one state, but causal calibration transfer becomes ambiguous.

**Required behavior:** aggregate response may be `VALID` only if explicitly labeled aggregate with included-effects provenance; reject a false causal decomposition.

### F-017 — EM phase center assumed equal to mechanical position without evidence

**Required behavior:** `DIAGNOSTIC / WARN` or require a bounded ideal-element profile; do not silently claim physical equivalence for nonideal elements.

### F-018 — Response null

At or near a complex-response null, phase may be undefined or ill-conditioned.

**Required behavior:** amplitude result may remain valid; phase/interpolation/calibration operations emit `DIAGNOSTIC / WARN` or become `INCOMPATIBLE` according to declared quality policy.

---

# 7. Mutual Coupling and Network Boundaries

### F-019 — Coupling matrix dimension/channel-order mismatch

**Required behavior:** `REJECT` composition when matrix dimension or stable channel identities do not match the declared array view.

### F-020 — Reference-plane mismatch in coupling composition

A matrix that numerically fits dimensions but maps incompatible physical quantities/planes is invalid.

**Required behavior:** `REJECT` composition.

### F-021 — `S21` used directly as universal coupling coefficient

**Required behavior:** `REJECT` the semantic substitution unless a declared derivation/calibration establishes the mapping under matching reference impedance/termination conditions.

### F-022 — Impedance/load matrix singularity

If `Z_A + Z_L` is singular, the declared inverse loaded-port formula is undefined.

**Required behavior:** `REJECT` that inverse operation or `REQUIRE OTHER NETWORK SOLUTION/MODEL`; do not manufacture an inverse.

### F-023 — Near-singular loading/coupling transform

The solution may exist but be numerically and physically sensitive.

**Required behavior:** `DIAGNOSTIC / WARN` with singular-value/conditioning evidence; downstream calibration uncertainty must not be hidden.

### F-024 — Coupling assumed Toeplitz/circulant/banded without evidence

**Required behavior:** profile/model `INCOMPATIBLE` with authoritative claim; approximation may run only when explicitly selected and labeled.

### F-025 — Symmetric network forced Hermitian

**Required behavior:** `REJECT` silent Hermitianization of a network matrix presented as physical evidence.

### F-026 — Effect already embedded in measured/EM manifold applied again

**Required behavior:** `REJECT` composition as double counting unless explicit de-embedding provenance shows the effect was removed.

### F-027 — Digital mask interpreted as physical port removal

**Required behavior:** `REJECT` semantic substitution. A physical termination-state change requires a coupling/loading model for the new state.

---

# 8. Operator-Graph and Reference-Plane Boundaries

### F-028 — Unsupported operator ordering

Because sensor operators need not commute, reordering must follow declared physical planes.

**Required behavior:** `REJECT` unproven reordering when it changes physical meaning.

### F-029 — Universal `imperfection_matrix` collapses nonlinear/sampling/quantization effects

**Required behavior:** `REJECT` authoritative representation that claims a single linear matrix covers nonlinear, time-grid, stochastic, and quantized effects generically.

### F-030 — Unit-incompatible operator composition

**Required behavior:** `REJECT` cross-plane composition whose output/input units do not match or are unknown.

### F-031 — Unknown included-effects contract

An aggregate operator/manifold without knowledge of what is included cannot safely compose with other corrections.

**Required behavior:** standalone exploratory use may be possible with `DIAGNOSTIC / WARN`; authoritative composition/calibration is `INCOMPATIBLE` until provenance is recovered.

---

# 9. Timing, Sampling, SRO, CFO, and Jitter Boundaries

### F-032 — Nonpositive actual sample rate

For `f_s,n=f_s(1+epsilon_f,n)`, require finite `f_s > 0` and `1+epsilon_f,n > 0`.

**Required behavior:** `REJECT` nonpositive/nonfinite actual sampling rate.

### F-033 — `epsilon_f = -1`

This makes actual sample rate zero and the reciprocal period relation singular.

**Required behavior:** `REJECT`.

### F-034 — Delay and sample-time offset merged into one unsigned `timing_error`

**Required behavior:** `REJECT` semantic collapse because physical-delay and later-sampling phase signs differ.

### F-035 — Fixed skew approximated as static phase outside a validated narrowband tone/profile

**Required behavior:** `INCOMPATIBLE / REQUIRE TIME-DOMAIN DESKEW OR WIDEBAND MODEL`.

### F-036 — Material SRO over covariance window with fixed-manifold processing

**Required behavior:** `INCOMPATIBLE / REQUIRE RESAMPLING, SHORTER WINDOW, OR TIME-VARYING MODEL`.

### F-037 — Differential CFO over covariance window

When relative phase evolves materially, one static manifold is insufficient.

**Required behavior:** `INCOMPATIBLE / REQUIRE FREQUENCY/TIME CORRECTION OR TIME-VARYING MODEL`.

### F-038 — Common CFO in truly simultaneous channels

A common phase evolution may cancel instantaneously in ordinary covariance.

**Required behavior:** potentially `VALID`; do not label it differential spatial distortion without acquisition-timing evidence.

### F-039 — Common oscillator in TDM virtual channels

Sequential acquisition can convert a common temporal phase evolution into relative virtual-channel phase.

**Required behavior:** require acquisition-time provenance/correction; otherwise virtual snapshot construction is `INCOMPATIBLE`.

### F-040 — Negative jitter standard deviation

**Required behavior:** `REJECT`. Zero jitter is a valid ideal edge case.

### F-041 — Nonfinite sample epochs or jitter samples

**Required behavior:** `REJECT` canonical timing processing.

### F-042 — Post-acquisition latency treated as physical sampling skew

**Required behavior:** `REJECT` semantic substitution unless latency actually changes the sampled physical epoch.

---

# 10. Receiver Noise and Staging Boundaries

### F-043 — Negative variance/noise power

**Required behavior:** `REJECT`; zero is a valid ideal noise-free edge case.

### F-044 — White-noise label after nonunitary transformation without covariance propagation

**Required behavior:** `REJECT` silent preservation of whiteness; recompute transformed covariance or explicitly justify invariance.

### F-045 — Stage of noise injection unknown

The same variance before versus after gain/coupling can imply different output covariance/SNR.

**Required behavior:** authoritative stage-sensitive claims report insufficient provenance; exploratory scalar-noise use requires an explicitly simplified profile.

### F-046 — Correlated stage noises treated as independent

**Required behavior:** `INCOMPATIBLE / REQUIRE CROSS-COVARIANCE TERMS`.

---

# 11. ADC, Quantization, and Dynamic-Range Boundaries

### F-047 — Invalid ADC full-scale range

Require finite `V_max > V_min` for the declared scalar full-scale model.

**Required behavior:** `REJECT` otherwise.

### F-048 — Invalid bit depth

For an ideal integer-bit ADC model, require positive integer `N_b`.

**Required behavior:** `REJECT` zero, negative, noninteger, or nonfinite bit count for that profile.

### F-049 — Input outside ADC range / clipping

The physical receiver state may be meaningful, but the baseline linear/no-overload profile is violated.

**Required behavior:** represent clipping explicitly; baseline profile `INCOMPATIBLE`. Never silently clamp and continue as though unclipped data were observed.

### F-050 — High-resolution `Delta^2/12` approximation used under overload

**Required behavior:** `INCOMPATIBLE`; exact/clipped quantizer model required.

### F-051 — High-resolution additive model used for coarse/one-bit quantization

**Required behavior:** `INCOMPATIBLE / REQUIRE SPECIALIZED QUANTIZED MODEL/ESTIMATOR`.

### F-052 — ADC volts and raw codes mixed without declared transfer

**Required behavior:** `REJECT` common physical/covariance operation until code-to-engineering-unit semantics are explicit.

### F-053 — ADC resolution confused with FPGA arithmetic word length

**Required behavior:** `REJECT` semantic substitution.

### F-054 — dBFS confused with absolute voltage/power dB reference

**Required behavior:** `REJECT` logarithmic interpretation unless the reference convention is declared.

### F-055 — Jitter SNR formula applied without input-frequency semantics

The common `-20 log10(2 pi f sigma_t)` relation is a bounded sinusoidal small-jitter result.

**Required behavior:** outside that profile, use `DIAGNOSTIC / WARN` or `REQUIRE OTHER MODEL`; do not treat it as universal ADC SNR.

---

# 12. DC Offset, I/Q Imbalance, and Nonlinearity Boundaries

### F-056 — Uncentered second moment called covariance in presence of nonzero mean

**Required behavior:** `REJECT` semantic claim; preserve as second moment unless centered.

### F-057 — Stable offset removed by exact mean centering

**Required behavior:** `VALID`; do not continue attributing the removed deterministic offset term to the centered covariance.

### F-058 — I/Q conjugate leakage forced into ordinary complex gain

When `B != 0` in `y=A x+B x*+d`, ordinary complex-linear representation is insufficient.

**Required behavior:** `INCOMPATIBLE / REQUIRE CORRECTION OR AUGMENTED/WIDELY-LINEAR STATISTICS`.

### F-059 — Improper data processed with covariance-only profile requiring propriety

**Required behavior:** `INCOMPATIBLE` unless pseudocovariance is negligible under a declared criterion or correction restores compatibility.

### F-060 — Nonlinear compression represented as fixed manifold

**Required behavior:** baseline linear profile `INCOMPATIBLE`; require nonlinear/bounded small-signal model.

### F-061 — Clipping repaired by digital rescaling

**Required behavior:** `REJECT` the reconstruction claim; clipped information is not restored by scalar gain.

### F-062 — Polynomial nonlinearity used outside calibrated amplitude region

**Required behavior:** `OUTSIDE MODEL DOMAIN / INCOMPATIBLE`; extrapolation requires explicit warning/model validation.

---

# 13. Calibration Artifact and Provenance Boundaries

### F-063 — Calibration artifact missing channel identity

**Required behavior:** `REJECT` application when channels cannot be matched unambiguously.

### F-064 — Calibration reference-plane mismatch

**Required behavior:** `REJECT` direct application; require conversion/de-embedding/re-embedding model.

### F-065 — Calibration hardware/termination state mismatch

**Required behavior:** `OUTSIDE CALIBRATION DOMAIN / INCOMPATIBLE` unless a validated transfer model exists.

### F-066 — Calibration frequency outside domain

**Required behavior:** explicit interpolation only inside declared supported domain; silent extrapolation is forbidden. Outside validated domain: `INCOMPATIBLE` or explicit exploratory warning.

### F-067 — Calibration direction/range/polarization outside domain

**Required behavior:** same as F-066; no silent nearest-neighbor substitution presented as calibrated truth.

### F-068 — Calibration expired or environmental state materially changed

**Required behavior:** `DIAGNOSTIC / WARN` or `OUTSIDE CALIBRATION DOMAIN` according to declared validity policy; do not silently assume timeless calibration.

### F-069 — Unknown included/de-embedded effects

**Required behavior:** `INCOMPATIBLE` for compound authoritative correction because double counting cannot be ruled out.

### F-070 — Gauge/reference normalization unknown

**Required behavior:** reject absolute/common-phase/common-scale-sensitive comparison until gauge semantics are explicit; projective comparison may remain valid if its required information is available.

### F-071 — Calibration artifact contains NaN/Inf/missing complex samples

**Required behavior:** `REJECT` ordinary interpolation/use unless an explicit missing-data model is selected. Never silently zero-fill.

### F-072 — Calibration uncertainty absent

Absence of uncertainty does not make the calibrated manifold numerically invalid.

**Required behavior:** deterministic use may be `VALID`; uncertainty-sensitive confidence claims receive `DIAGNOSTIC / WARN` / insufficient evidence.

---

# 14. Calibration Identifiability and Correction Boundaries

### F-073 — Reference-channel gauge mistaken for physical truth

**Required behavior:** `REJECT` claim that setting `g_ref=1` proves the reference channel is physically ideal.

### F-074 — Structurally non-identifiable parameter decomposition

Examples include one-frequency static phase versus delay, element gain versus receiver gain, or embedded response versus coupling without sufficient experiments.

**Required behavior:** retain aggregate calibrated response if observable; parameter-level result remains `UNRESOLVED / NON-IDENTIFIABLE`.

### F-075 — Local Jacobian rank deficient after gauge handling

**Required behavior:** local parameter-identification problem `INCOMPATIBLE / UNDERDETERMINED`; do not report a unique physical parameter estimate.

### F-076 — Full-rank but ill-conditioned calibration Jacobian/operator

**Required behavior:** computation may proceed with `DIAGNOSTIC / WARN`; report scaling, singular values/condition metrics, and uncertainty sensitivity.

### F-077 — Exact inverse requested for singular operator

**Required behavior:** `REJECT` exact inverse operation; pseudoinverse/regularized correction may be offered only as explicitly different operations.

### F-078 — Near-zero singular value and aggressive inverse correction

**Required behavior:** `DIAGNOSTIC / WARN` or policy-based incompatibility; transformed noise/model uncertainty must be reported.

### F-079 — Tikhonov regularization parameter with incompatible units/scaling

For `C_lambda=(H^H H+lambda I)^-1 H^H`, require `[lambda I]=[H^H H]` or an explicit nondimensionalized problem.

**Required behavior:** `REJECT` dimensionally incompatible regularization configuration.

### F-080 — Negative `lambda` labeled standard Tikhonov penalty

Under the standard positive-semidefinite ridge/Tikhonov interpretation, negative penalty is outside profile.

**Required behavior:** `REJECT` as standard Tikhonov configuration; a different mathematically declared method requires a separate profile.

### F-081 — Correction declared to recover null-space information

**Required behavior:** `REJECT` scientific claim.

---

# 15. Direct Measured / CST / Full-Wave Manifold Boundaries

### F-082 — Coordinate frame missing or unregistered

**Required behavior:** `REJECT` direction-dependent calibrated-manifold use.

### F-083 — Direction convention mismatch

**Required behavior:** require explicit coordinate transformation; silent sign/reflection conversion is `REJECT`.

### F-084 — Frequency axis missing for frequency-dependent data

**Required behavior:** `REJECT` frequency-specific use when physical frequency cannot be identified.

### F-085 — Complex phase unavailable

Magnitude-only data may support magnitude visualization but not coherent MUSIC manifold calibration by default.

**Required behavior:** coherent use `INCOMPATIBLE`.

### F-086 — Arbitrary independent per-node phase normalization before interpolation

**Required behavior:** `REJECT` as a grid-coherent calibrated manifold unless a gauge-alignment procedure restores coherence.

### F-087 — Interpolation across response null without quality handling

**Required behavior:** `DIAGNOSTIC / WARN` or incompatibility depending on declared interpolation-quality policy.

### F-088 — Silent extrapolation beyond measured/simulated grid

**Required behavior:** `REJECT` authoritative calibrated result; explicit exploratory extrapolation must retain warning/provenance.

### F-089 — CST/EM manifold labeled measured truth

**Required behavior:** `REJECT` provenance claim. It remains numerical EM evidence/prediction.

### F-090 — Measured manifold labeled exact physical truth

**Required behavior:** `REJECT` exact-truth claim unless the context is an artificial simulation that explicitly defines it as truth; measured response carries uncertainty/systematic error.

### F-091 — Transmit far field silently used as receive manifold

**Required behavior:** `REJECT` direct substitution unless reciprocity, normalization, reference plane, polarization, and convention conversion are established.

### F-092 — Channel ordering sorted by geometry and identity lost

**Required behavior:** `REJECT` destructive scientific transformation. Sorting may create a derived view only while stable physical identity remains recoverable.

---

# 16. Error-Metric and Gauge Boundaries

### F-093 — Raw manifold difference with incompatible units/normalizations

**Required behavior:** `REJECT` metric until responses are made semantically compatible.

### F-094 — Relative/projective metric with zero reference norm

Expressions dividing by `||a||` or `||a||||b||` are undefined for zero vector.

**Required behavior:** `REJECT` metric computation or return explicitly undefined; never force zero/one similarity.

### F-095 — Phase-aligned metric used when common amplitude is also gauge

**Required behavior:** metric may be `VALID` for phase-only question but is `INCOMPATIBLE` with a common-complex-scale equivalence question. Metric equivalence class must be declared.

### F-096 — Projective metric used when absolute gain is scientifically important

**Required behavior:** computation may be valid but insufficient; emit `DIAGNOSTIC / WARN` and retain an amplitude-sensitive metric.

### F-097 — Weighted metric with invalid weight matrix

For a declared positive-weight inner-product metric, require Hermitian positive semidefinite/definite properties as appropriate.

**Required behavior:** `REJECT` invalid weighting semantics.

### F-098 — Grid metric averaged without domain weighting/provenance

**Required behavior:** exploratory statistic may proceed if explicitly defined; reject claims of universal calibration error without declared grid/domain weighting.

---

# 17. Covariance and Eigenspace Boundaries

### F-099 — Sensor and sample covariance errors conflated

**Required behavior:** `REJECT` semantic claim; retain `E_sensor` and `E_sample` separately even when only their sum is observed.

### F-100 — Covariances compared at incompatible reference planes/units

**Required behavior:** `REJECT` direct subtraction/comparison.

### F-101 — White-noise eigenspace invariance assumed for colored noise

**Required behavior:** `INCOMPATIBLE`; use whitening/generalized model or explicit colored-noise analysis.

### F-102 — Whitening with singular/non-PD noise covariance

The standard Hermitian inverse square root requires positive definiteness.

**Required behavior:** `REJECT` standard whitening operation; alternative subspace/pseudoinverse treatment requires a separate declared profile.

### F-103 — Whitening data but not steering manifold

**Required behavior:** `REJECT` estimator construction.

### F-104 — Time-varying sensor operator replaced by mean operator without validation

**Required behavior:** `INCOMPATIBLE` with generic static-manifold covariance model; averaging `H` is not generally equivalent to averaging `H R H^H`.

### F-105 — Small covariance perturbation approximation with large mismatch

**Required behavior:** exact covariance relation may remain valid; first-order result is `DIAGNOSTIC / WARN` or `INCOMPATIBLE` under approximation policy.

### F-106 — Eigengap zero / signal-noise spectral cluster not separated

Subspace orientation can become non-unique/unstable.

**Required behavior:** `DIAGNOSTIC / WARN` or `INCOMPATIBLE` for perturbative subspace claims; do not report a finite robustness bound using division by zero gap.

### F-107 — Population gap replaced by sample gap in theorem without justification

**Required behavior:** `REJECT` theorem claim; sample eigengap may be reported separately as an empirical diagnostic.

### F-108 — Rank-deficient sensor transform ignored

**Required behavior:** recompute observable signal rank/model-order feasibility; do not assume rank preservation.

### F-109 — Additional covariance modes from time-varying sensor state called new physical sources

**Required behavior:** `REJECT` interpretation unless source-count evidence independently supports it.

---

# 18. MUSIC / Estimator Compatibility Boundaries

### F-110 — Nominal manifold used against known mismatched physical manifold

The computation itself may run.

**Required behavior:** label `DEGRADED / MISMATCHED MODEL`; do not call the profile matched classical MUSIC.

### F-111 — Matched static complex-linear imperfection

Known fixed position/gain/phase/coupling effects incorporated consistently into the steering manifold can remain classical-MUSIC compatible if all other assumptions hold.

**Required behavior:** `VALID` matched profile.

### F-112 — Colored noise with unwhitened white-noise MUSIC assumptions

**Required behavior:** `INCOMPATIBLE / REQUIRE WHITENING OR GENERALIZED METHOD`.

### F-113 — Widely-linear/IQ-impaired data with ordinary covariance MUSIC

**Required behavior:** `INCOMPATIBLE` unless correction restores ordinary-complex compatibility.

### F-114 — Clipped/nonlinear data passed to baseline linear MUSIC

**Required behavior:** `INCOMPATIBLE`; any exploratory output retains explicit receiver-model violation.

### F-115 — Coarse/one-bit quantized data passed to high-resolution baseline MUSIC without validated approximation

**Required behavior:** `INCOMPATIBLE / REQUIRE SPECIALIZED QUANTIZED ESTIMATOR`.

### F-116 — Model order leaves no noise subspace

For classical MUSIC require selected observable signal rank/order `< N_effective`.

**Required behavior:** `INCOMPATIBLE`; do not reinterpret as physical-scene invalidity.

### F-117 — Sample-rank ceiling insufficient for selected subspace order

**Required behavior:** statistical/algorithm profile `INCOMPATIBLE`; additional snapshots or another estimator/model needed.

### F-118 — Local MUSIC peak-shift formula at flat/nonisolated minimum

If denominator curvature/sensitivity term vanishes or peak is nonisolated, the local first-order bias formula is undefined/unreliable.

**Required behavior:** `INCOMPATIBLE` with that approximation; use direct spectrum/estimator analysis.

### F-119 — Projective leakage interpreted as full DOA error

`1-rho^2` is a rank-one subspace mismatch measure, not a universal angular-bias metric.

**Required behavior:** `REJECT` universal DOA-error interpretation.

### F-120 — Compatible model but poor performance

Low SNR, weak eigengap, close sources, small snapshot count, or large uncertainty can yield poor results without violating compatibility.

**Required behavior:** model may remain `VALID`; report performance/confidence failure separately.

---

# 19. Physical Channel / Mask / MIMO Boundaries

### F-121 — Zero active digital channels

**Required behavior:** `REJECT` spatial processing.

### F-122 — One active channel

Measurement may be valid, but phase-difference/array DOA is generally unidentifiable.

**Required behavior:** measurement `VALID`; directional array estimator `INCOMPATIBLE`.

### F-123 — Physical port termination changed but old calibration retained

**Required behavior:** `OUTSIDE CALIBRATION DOMAIN / INCOMPATIBLE` unless calibration explicitly covers the new network state.

### F-124 — MIMO virtual calibration without `(Tx,Rx)` lineage

**Required behavior:** `REJECT` publication-grade scientific artifact because physical provenance is lost.

### F-125 — TDM MIMO channels treated as simultaneous despite material phase evolution

**Required behavior:** `INCOMPATIBLE / REQUIRE TIMING COMPENSATION OR TIME-AWARE MODEL`.

### F-126 — Separable Tx/Rx gain model forced on nonseparable virtual-channel response

**Required behavior:** `INCOMPATIBLE`; use aggregate virtual-channel calibration or richer physical model.

---

# 20. Initial Phase-1 Profile Boundaries

The initial Phase-1 ADR-003 profile is deliberately ideal.

### F-127 — Nonzero deterministic imperfection requested in Phase-1 ideal profile

Examples: position error, gain mismatch, coupling, channel delay mismatch.

**Required behavior:** `INCOMPATIBLE / REQUIRE LATER VALIDATED PROFILE`; do not silently ignore the requested imperfection.

### F-128 — ADC quantization enabled under unquantized Phase-1 profile

**Required behavior:** require an explicitly activated future quantized profile; no silent float approximation presented as ADC modeling.

### F-129 — Measured/CST manifold requested under identity-manifold Phase-1 profile

**Required behavior:** require a direct-manifold calibrated profile; no silent import into ideal identity profile.

### F-130 — Colored noise requested under white equal-variance Phase-1 profile

**Required behavior:** `INCOMPATIBLE / REQUIRE COLORED-NOISE PROFILE/WHITENING`.

### F-131 — Near-field/wideband sensor-imperfection scenario requested in Phase-1

**Required behavior:** physical scenario remains meaningful; Phase-1 profile `INCOMPATIBLE`.

---

# 21. Workflow, Provenance, and No-Silent-Coercion Boundaries

### F-132 — Silent switch between nominal/physical/calibrated manifold

**Required behavior:** `REJECT` workflow behavior.

### F-133 — Silent normalization of amplitude-bearing manifold

**Required behavior:** `REJECT`; normalized derived views must preserve raw artifact/provenance.

### F-134 — Silent unit inference

**Required behavior:** `REJECT` magnitude-based guessing of meters/wavelengths, Hz/rad/s, seconds/samples, radians/degrees, volts/codes, or linear/dB semantics.

### F-135 — Silent calibration-domain extrapolation

**Required behavior:** `REJECT` authoritative claim.

### F-136 — Silent double counting

**Required behavior:** `REJECT` application of an effect already included in an aggregate response.

### F-137 — Silent numerical repair

Examples: matrix symmetrization, eigenvalue clipping, NaN zero-fill, phase unwrap repair, covariance PSD projection.

**Required behavior:** `REJECT` repair presented as original scientific evidence. Explicit repair may be a separate derived artifact with provenance.

### F-138 — Missing profile identity/version

Exploratory computation may remain possible.

**Required behavior:** publication/reproducibility claim reports insufficient provenance until scientific profile identity and relevant calibration state are recoverable.

### F-139 — Missing compatibility axis promoted to compatible

**Required behavior:** preserve `NOT_ASSESSED`/`UNRESOLVED`; never silently map unknown to compatible.

### F-140 — Generic `realistic_sensor=True`

A generic Boolean does not identify active physical mechanisms or calibration state.

**Required behavior:** `REJECT` as authoritative scientific configuration; require a named/versioned profile or typed effect composition.

---

# 22. Boundary Classification Summary

The failure classes are intentionally layer-specific.

## REJECT examples

```text
nonfinite positions/gains/times
invalid ADC range/bit depth
unit/reference-plane mismatch
double counting
singular exact inverse request
invalid calibration channel identity
zero-norm projective metric
silent manifold normalization
silent unit inference
silent numerical repair
invalid physical/operator composition
```

## INCOMPATIBLE / REQUIRE OTHER MODEL examples

```text
far-field shortcut outside far field
fixed phase model for material SRO/CFO
coarse quantization under high-resolution profile
widely-linear data under ordinary covariance profile
clipped/nonlinear data under baseline linear MUSIC
colored noise under unwhitened white-noise MUSIC
calibration outside frequency/direction/state domain
near-field/wideband/nonideal effects requested in Phase-1 ideal profile
```

## DIAGNOSTIC / WARN examples

```text
near-singular calibration/coupling operator
response near a null
ill-conditioned but identifiable calibration
calibration uncertainty unavailable
weak/collapsed empirical eigengap
explicit exploratory extrapolation
compatible model with poor finite-sample performance
```

## VALID examples

```text
zero noise variance in ideal noise-free profile
zero channel gain as a physical dead-channel state (but inverse is invalid)
common phase under ordinary coherent covariance
rigid translation under far-field relative-manifold semantics
matched static linear imperfection with matched manifold
identity deterministic sensor chain in Phase-1
```

---

# 23. Gate-F Coverage Matrix

| Contract family | Boundary coverage |
|---|---|
| Position/geometry error | F-001–F-007 |
| Gain/phase mismatch | F-008–F-013 |
| Element/polarization | F-014–F-018 |
| Coupling/loading/network | F-019–F-027 |
| Typed operator graph/reference planes | F-028–F-031 |
| Timing/SRO/CFO/jitter | F-032–F-042 |
| Receiver noise/staging | F-043–F-046 |
| ADC/quantization/dynamic range | F-047–F-055 |
| DC/IQ/nonlinearity | F-056–F-062 |
| Calibration provenance/domain | F-063–F-072 |
| Calibration identifiability/correction | F-073–F-081 |
| Measured/CST/direct manifold | F-082–F-092 |
| Error metrics/gauge | F-093–F-098 |
| Covariance/eigenspace | F-099–F-109 |
| MUSIC/estimator compatibility | F-110–F-120 |
| Channel mask/MIMO | F-121–F-126 |
| Initial Phase-1 boundary | F-127–F-131 |
| Workflow/provenance | F-132–F-140 |

---

# 24. Gate-F Candidate Conclusion

ADR-003 now explicitly distinguishes malformed inputs, physically meaningful scenarios outside a selected sensor profile, calibration-domain violations, non-identifiability, poor conditioning, statistical/eigenspace incompatibility, estimator incompatibility, and performance limitations.

No meaningful physical scenario is rejected solely because baseline classical MUSIC or the initial Phase-1 ideal sensor profile cannot represent it.

The governing rule is:

> Preserve the earliest failing scientific layer, require another model/profile when the physical scenario is meaningful, and never turn uncertainty, incompatibility, or missing provenance into an apparently valid sensor/DOA result through silent coercion.

This document is candidate Gate-F evidence. Formal Gate-F PASS is recorded separately after reconciliation against ADR-003 and Gates A–E.
