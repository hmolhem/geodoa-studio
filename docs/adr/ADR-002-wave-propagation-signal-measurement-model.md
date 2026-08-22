# ADR-002 — Wave, Propagation, Signal, and Measurement Model

- **Status:** Proposed — Phase 0C Gates A–F completed in design; repository acceptance reconciliation pending
- **Phase:** 0C — Scientific Foundations
- **Scope:** Wave, propagation, medium, motion, measurement, snapshot, covariance, source-statistics, FMCW, and MIMO measurement semantics
- **Depends on:** `ADR-001-coordinate-direction-spatial-conventions.md`, `GEODOA_STUDIO_MASTER_START_HANDOFF.md`, `PHASE0C_SCIENTIFIC_CONTRACTS_ROADMAP.md`
- **Acceptance audit:** `ADR-002_ACCEPTANCE_AUDIT.md`
- **Golden reference evidence:** `../science/golden_reference/ADR-002_GOLDEN_REFERENCE_PROBLEMS.md`
- **Boundary/failure evidence:** `ADR-002_BOUNDARY_FAILURE_ANALYSIS.md`
- **Supersedes:** None
- **Superseded by:** None

## 1. Decision Summary

ADR-002 defines how GeoDOA Studio turns a physical source/target and propagation path into a scientifically interpretable measurement and then into canonical array-processing quantities.

The governing chain is

```text
Physical scene
    -> propagation geometry/path
    -> propagation medium response
    -> received complex-baseband signal
    -> raw measurement axes/tensor
    -> explicit snapshot construction
    -> source/noise statistical model
    -> covariance / subspace-compatible representation
```

The initial validated physical/measurement profile is **PM-001 — Reference Far-Field Narrowband Receive-Array Profile**. PM-001 is a bounded reference profile, not a claim that all real sensor-array scenarios are far field, narrowband, stationary, lossless, or passive.

ADR-002 adopts the scientific temporal phasor convention inherited from ADR-001,

```math
\exp(-j\omega t),
```

and therefore uses outgoing scalar propagation phase

```math
\exp(+jkR).
```

For a homogeneous nondispersive medium with propagation speed `v`, exact path length `R_n`, and reference path `R_ref`, the relative delay is

```math
\Delta\tau_n
=
\frac{R_n-R_{\mathrm{ref}}}{v}.
```

Under the first-order far-field approximation,

```math
R_n-R_{\mathrm{ref}}
\approx
-(\mathbf r_n-\mathbf r_{\mathrm{ref}})^T\hat{\mathbf u},
```

so a static pure-delay complex-baseband channel reduces under the narrowband approximation to the ADR-001 geometry-only receive manifold

```math
a_n
=
\exp\!\left[
-jk_c(\mathbf r_n-\mathbf r_{\mathrm{ref}})^T\hat{\mathbf u}
\right].
```

This exact recovery of the accepted ADR-001 sign and reference semantics is normative.

## 2. Context and Decision Drivers

Array processing can appear deceptively simple when written only as

```math
\mathbf x[k]=\mathbf A\mathbf s[k]+\mathbf n[k].
```

Without an explicit propagation and measurement contract, however, the symbols can silently mix incompatible meanings: one-way versus two-way paths, phase velocity versus group velocity, spherical versus plane-wave propagation, true differential delay versus phase shift, raw ADC samples versus spatial snapshots, physical channels versus virtual MIMO channels, covariance versus uncentered second moment, physical source count versus observable subspace rank, and scientific signed frequency versus software FFT-bin coordinates.

ADR-002 therefore locks the physical and statistical semantics before Phase 1 implementation. The purpose is not to implement every possible propagation effect in Phase 1. The purpose is to ensure that unsupported effects are represented as explicit model/profile boundaries rather than hidden approximations.

## 3. Scope

ADR-002 governs:

- temporal complex-signal and scientific Fourier-sign conventions relevant to propagation;
- exact source-to-sensor path length and relative propagation delay;
- spherical-wave propagation and first/second-order plane-wave approximations;
- far-field compatibility diagnostics and their reference/common-phase semantics;
- narrowband versus wideband array compatibility;
- aperture differential delay and bandwidth-delay diagnostics;
- homogeneous, isotropic, nondispersive, lossy/dispersive, and extended medium semantics;
- phase velocity, group velocity, attenuation, and dispersion terminology;
- passive one-way and active multi-leg propagation distinctions;
- source/target motion, range rate, Doppler, range migration, angle/manifold migration, and coherent-processing validity concepts;
- FMCW chirp, dechirp, beat-frequency, range, mixer-sign, and FFT-coordinate semantics;
- raw measurement axes, tensors, and derived spatial snapshot matrices;
- physical MIMO Tx/Rx channel pairs and conditions under which a virtual-sum geometry is valid;
- source, target/scatterer, propagation path, and spatial-arrival distinctions;
- source/noise statistical assumptions, covariance and sample-covariance semantics;
- coherence, source covariance rank, observable signal rank, and model-order semantics;
- SNR and normalized/physical measurement-scaling semantics;
- compatibility response classes and the separation of scientific metrics from acceptance thresholds.

## 4. Explicit Non-Goals

ADR-002 does not fully define:

- element radiation/receive patterns, polarization, gain/phase mismatch, position error, channel-delay mismatch, clock/skew error, mutual coupling, ADC nonidealities, quantization, or calibration — governed primarily by ADR-003;
- universal numerical thresholds for far-field, narrowband, quasi-static, PSD, resolution, or benchmark acceptance — governed by ADR-004 and later validation policies;
- a complete ray tracer, full-wave solver, refractive medium solver, multipath engine, or relativistic moving-source solver;
- implementation-specific Python class names or a one-class-per-quantity domain model;
- a specific DOA estimator, model-order estimator, peak detector, or benchmark baseline.

## 5. Inherited ADR-001 Conventions

ADR-002 shall not redefine the accepted ADR-001 spatial contract.

The following are inherited:

- canonical temporal phasor `exp(-j omega t)`;
- look direction `u_hat` points from the array/localization region toward the source;
- incident propagation direction is `-u_hat`;
- coordinate origin, propagation-expansion origin, and spatial phase reference are distinct concepts;
- physical geometry is authoritative in meters and stable channel identity is distinct from row/order views;
- common phase does not constitute spatial manifold distortion;
- 3-D projection ambiguity and spatial aliasing are distinct;
- canonical geometry-only receive manifold is reference-relative and translation consistent.

## 6. Temporal Signal and Delay Convention

A real RF signal may be represented as

```math
x_{\mathrm{RF}}(t)
=
\Re\{s(t)e^{-j\omega_c t}\},
```

where `s(t)` is the complex envelope.

Under the scientific Fourier pair consistent with this convention,

```math
X(\omega)=\int x(t)e^{+j\omega t}\,dt,
```

a pure delay satisfies

```math
x(t-\tau)
\longleftrightarrow
X(\omega)e^{+j\omega\tau}.
```

For a static scalar pure-delay path,

```math
x_{\mathrm{BB}}(t)
=
s(t-\tau)e^{+j\omega_c\tau}.
```

The word `exact` may be applied to this relation only within the declared static pure-delay channel model. Dispersive, frequency-selective, or strongly time-varying channels require a more general transfer/path response.

## 7. Outgoing Propagation and Exact Path Geometry

With `exp(-j omega t)`, an outgoing monochromatic scalar field propagating toward increasing path coordinate has the phase form

```math
\exp(+jkR)\exp(-j\omega t).
```

Let an expansion/localization origin be `r_0`, source position

```math
\mathbf r_s=\mathbf r_0+R\hat{\mathbf u},
```

and

```math
\boldsymbol\delta_n=\mathbf r_n-\mathbf r_0.
```

The exact source-to-sensor path length is

```math
R_n
=
\|R\hat{\mathbf u}-\boldsymbol\delta_n\|_2.
```

Geometric distance may be zero for coincident points, but ideal scalar `1/R` point-source spreading is singular at zero range. Geometry validity and propagation-model validity are therefore distinct.

## 8. Spherical-to-Plane-Wave Expansion

The second-order expansion is

```math
R_n
=
R
-
\hat{\mathbf u}^T\boldsymbol\delta_n
+
\frac{\|\boldsymbol\delta_n\|^2-(\hat{\mathbf u}^T\boldsymbol\delta_n)^2}{2R}
+
O\!\left(\frac{\|\boldsymbol\delta_n\|^3}{R^2}\right).
```

It is an asymptotic expansion requiring the relevant aperture offsets to be small compared with source range. Define

```math
q_n
=
\|\boldsymbol\delta_n\|^2
-
(\hat{\mathbf u}^T\boldsymbol\delta_n)^2
=
\|\boldsymbol\delta_{n,\perp}\|^2.
```

For a reference channel/point,

```math
R_n-R_{\mathrm{ref}}
\approx
-
\hat{\mathbf u}^T(\boldsymbol\delta_n-\boldsymbol\delta_{\mathrm{ref}})
+
\frac{q_n-q_{\mathrm{ref}}}{2R}.
```

For an `x`-axis ULA in the ADR-001 canonical slice, `u = sin(theta)` and

```math
R_n
\approx
R-x_n\sin\theta+
\frac{x_n^2\cos^2\theta}{2R}
```

when the expansion coordinates are chosen consistently.

Far-field compatibility is a relation among scene geometry, direction, frequency, and required accuracy. It is not an intrinsic Boolean property of an array or source object.

## 9. Plane-Wave Compatibility Diagnostics

The declared-reference path residual is

```math
\delta R_{n,\mathrm{PW}}
=
(R_n-R_{\mathrm{ref}})
+
(\mathbf r_n-\mathbf r_{\mathrm{ref}})^T\hat{\mathbf u}.
```

A reference-specific phase error may be reported as

```math
\epsilon_{\mathrm{FF,ref}}(f)
=
|\beta(f)|\max_n|\delta R_{n,\mathrm{PW}}|.
```

Because common phase is not spatial distortion, a reference-invariant compatibility diagnostic shall also be available conceptually:

```math
\Delta R_{\mathrm{PW,pair}}
=
\max_{n,m}
\left|
(R_n-R_m)
+
(\mathbf r_n-\mathbf r_m)^T\hat{\mathbf u}
\right|,
```

```math
\epsilon_{\mathrm{FF,pair}}(f)
=
|\beta(f)|\Delta R_{\mathrm{PW,pair}}.
```

ADR-002 defines these quantities. It does not prescribe a universal numerical PASS/FAIL threshold.

The conventional Fraunhofer scale

```math
R_F\approx\frac{2D^2}{\lambda}
```

may be reported as a reference diagnostic, but shall not be treated as a universal binary plane-wave boundary.

## 10. Propagation Delay and Recovery of ADR-001 Steering

For PM-001's homogeneous nondispersive medium,

```math
\tau_n=\frac{R_n}{v},
\qquad
\Delta\tau_n=\frac{R_n-R_{\mathrm{ref}}}{v}.
```

Under the first-order far-field approximation,

```math
\Delta\tau_n
\approx
-
\frac{(\mathbf r_n-\mathbf r_{\mathrm{ref}})^T\hat{\mathbf u}}{v}.
```

The relative complex-baseband path is

```math
x_n(t)
=
s_{\mathrm{ref}}(t-\Delta\tau_n)
\exp(+j\omega_c\Delta\tau_n).
```

Under the narrowband approximation,

```math
s_{\mathrm{ref}}(t-\Delta\tau_n)
\approx
s_{\mathrm{ref}}(t),
```

so

```math
a_n
=
\exp(+j\omega_c\Delta\tau_n)
=
\exp[-jk_c(\mathbf r_n-\mathbf r_{\mathrm{ref}})^T\hat{\mathbf u}].
```

This equality is a normative cross-ADR consistency requirement.

## 11. Far Field and Narrowband Are Independent

Far-field approximation replaces spatial spherical curvature with a plane-wave relative-path model.

Narrowband approximation replaces differential envelope delay across the aperture with a carrier-frequency phase shift.

Therefore

```text
far field  does not imply  narrowband
narrowband does not imply  far field
```

and the two compatibility axes shall be represented independently.

## 12. Aperture Delay and Narrowband Compatibility

The canonical aperture delay spread is

```math
\Delta\tau_{\mathrm{ap}}
=
\max_n\tau_n-
\min_n\tau_n.
```

This exact/general definition is preferred when path delays are available.

For a far-field homogeneous nondispersive model,

```math
\Delta\tau_{\mathrm{ap}}
=
\frac{D_{\hat{\mathbf u}}}{v},
```

where

```math
D_{\hat{\mathbf u}}
=
\max_n(\mathbf r_n^T\hat{\mathbf u})
-
\min_n(\mathbf r_n^T\hat{\mathbf u}).
```

For spectral offsets `|nu| <= nu_max`, a primary narrowband metric is

```math
\eta_{\mathrm{NB}}
=
2\pi\nu_{\max}\Delta\tau_{\mathrm{ap}}.
```

If `B` denotes a declared full two-sided occupied bandwidth such that `nu_max = B/2`, the order metric `B Delta tau_ap` may be used. The bandwidth definition must be explicit.

For a nondispersive medium,

```math
B\Delta\tau_{\mathrm{ap}}
=
\left(\frac{B}{f_c}\right)
\left(\frac{D_{\hat{\mathbf u}}}{\lambda_c}\right).
```

Fractional bandwidth alone therefore does not establish array narrowband compatibility.

Narrowband compatibility is direction/scene dependent, not merely a waveform Boolean.

## 13. Wideband Manifold

For far-field propagation in a general medium,

```math
a_n(f,\hat{\mathbf u})
=
\exp[-j\beta(f)(\mathbf r_n-\mathbf r_{\mathrm{ref}})^T\hat{\mathbf u}].
```

Thus a wideband manifold is frequency dependent. Use of `a(f_c, u_hat)` over a band is an approximation whose compatibility must be assessed.

## 14. Propagation Medium and Complex Path Response

A general homogeneous scalar path response may be represented as

```math
H(\omega,R)
=
G_{\mathrm{geom}}(\omega,R)
\exp[-\alpha(\omega)R]
\exp[+j\beta(\omega)R].
```

The following are distinct:

- geometric spreading;
- medium attenuation/absorption;
- propagation phase;
- group delay/dispersion;
- sensor/receiver response;
- target/scatterer response.

For the chosen sign convention, a convenient complex wavenumber representation is

```math
\tilde k=\beta+j\alpha,
```

so

```math
\exp(j\tilde kR)=\exp(-\alpha R)\exp(j\beta R).
```

`beta` and `alpha` share inverse-length SI dimension but retain distinct semantic units (`rad/m` versus attenuation such as `Np/m`).

Absolute path response `H_n`, relative response `H_n/H_ref`, and geometry-only manifold are distinct scientific objects. A relative ratio is defined only when the reference response is nonzero.

The ideal spherical specialization

```math
\frac{R_{\mathrm{ref}}}{R_n}\exp[jk(R_n-R_{\mathrm{ref}})]
```

applies only to the declared ideal 3-D scalar spherical-spreading model; it is not a universal near-field law.

## 15. Phase Velocity, Group Velocity, and Dispersion

The phase velocity is

```math
v_\phi(\omega)=\frac{\omega}{\beta(\omega)}.
```

Under the GeoDOA Fourier-sign convention, group delay satisfies

```math
\tau_g=+\frac{d\phi}{d\omega}.
```

For a uniform path,

```math
\tau_g
=
R\frac{d\beta}{d\omega},
\qquad
v_g
=
\left(\frac{d\beta}{d\omega}\right)^{-1}.
```

A dispersive medium has nontrivial frequency dependence in `beta(omega)`. Around `omega_c`,

```math
\beta(\omega)
=
\beta_c
+
\beta_1\Omega
+
\frac12\beta_2\Omega^2+
\cdots.
```

The first-order slope determines group delay; higher-order terms can distort a waveform. Wideband and dispersive are not synonyms.

PM-001 uses

```math
\beta(\omega)=\frac{\omega}{v},
\qquad
\alpha=0,
\qquad
v_\phi=v_g=v.
```

## 16. Motion, Path Rate, and Doppler

A general time-varying narrowband measurement may be written

```math
\mathbf x[k]=\mathbf A[k]\mathbf s[k]+\mathbf n[k].
```

For a physical path length `P(t)` and a slowly varying narrowband path,

```math
\tau(t)=\frac{\mathcal P(t)}{v},
```

and

```math
f_D
=
-f_c\dot\tau
=
-\frac{\dot{\mathcal P}}{\lambda_c}.
```

For one-way passive propagation,

```math
f_D=-\frac{\dot R}{\lambda_c}.
```

For the monostatic stop-and-hop/quasi-static specialization,

```math
f_D=-\frac{2\dot R}{\lambda_c}.
```

GeoDOA defines `dot R > 0` as receding and `dot R < 0` as approaching, so under this scientific convention an approaching monostatic target has positive `f_D`.

These Doppler relations are low-velocity/slowly-varying-path approximations. Strongly time-varying or broadband motion may require retarded-time/time-scaling physics.

Nonzero Doppler alone does not imply a time-varying spatial manifold. A common Doppler phase can cancel in an instantaneous outer product when the spatial steering vector remains constant.

## 17. Quasi-Static Manifold, Migration, and Time Scales

PM-001 does not require zero physical velocity. It requires the spatial manifold to remain compatible with a constant-manifold approximation over the declared snapshot/covariance window.

Relevant diagnostics may include:

```math
\eta_R
=
\frac{\max_t|R(t)-R_0|}{\delta R_{\mathrm{res}}},
```

manifold drift under a precisely defined common-phase/projective equivalence, and Doppler/acceleration stability metrics.

A generic symbol such as `d_proj` shall not become normative until its equivalence class is explicitly defined (common phase only versus common complex scaling versus unit-norm projective distance).

Coherent Processing Interval (CPI), covariance-estimation window, and tracking interval are distinct time scales.

## 18. Passive, Active, and Multi-Leg Propagation

Passive receive-equivalent propagation uses a one-way source-to-receiver path.

Active sensing uses at least two physical legs:

```text
Tx -> target/scatterer -> Rx
```

with stationary/quasi-static path length

```math
\mathcal P
=
R_{\mathrm{Tx\to T}}
+
R_{\mathrm{T\to Rx}}.
```

The monostatic `2R` relation is a specialization and shall not be hard-coded into generic propagation semantics.

For moving targets the transmit and receive legs occur at different physical times. Evaluating both legs at one common epoch is a stop-and-hop/quasi-static approximation, not a universal exact moving-target law.

A post-processed active-radar range/Doppler cell may be represented by a receive-equivalent spatial observation model when the two-way physics and transformation provenance remain explicit. This does not make PM-001 a full radar propagation model.

## 19. Measurement Axes and Raw Data

GeoDOA distinguishes acquisition/measurement axes from derived physical axes and statistical roles.

Potential acquisition axes include:

- physical Rx channel;
- Tx index;
- fast time;
- slow time / chirp / pulse repetition;
- frequency or frequency step.

Derived axes may include:

- beat frequency;
- range;
- Doppler.

A snapshot is a statistical/array-processing semantic role, not automatically a raw acquisition axis.

The physical meaning of each axis, units/coordinate mapping, and provenance shall be explicit. Scientific axis semantics are distinct from memory layout, NumPy stride order, FFT output order, or AXI/DMA serialization order.

## 20. Spatial Snapshot Semantics

A spatial snapshot is a simultaneous-equivalent coherent observation of the declared active spatial channels at a common receiver observation state/epoch or under an explicitly calibrated equivalent construction.

The canonical spatial snapshot matrix is

```math
\mathbf X
=
[\mathbf x[1]\;\cdots\;\mathbf x[L]]
\in\mathbb C^{N\times L},
```

with rows as channels and columns as snapshots.

A raw multidimensional tensor is not a snapshot matrix merely because it has two or more dimensions. Snapshot construction is an explicit provenance-preserving transformation.

## 21. FMCW Model and Sign Semantics

Under the GeoDOA phasor convention, a linear chirp may be represented as

```math
s_{\mathrm{tx}}(t)
=
A\exp\{-j2\pi[f_ct+\tfrac12\mu t^2]\},
```

where signed chirp slope is

```math
\mu=\frac{B}{T_c}
```

under the associated declared bandwidth/sweep convention.

For stationary delay `tau` and dechirp convention

```math
y(t)=s_{\mathrm{rx}}(t)s_{\mathrm{tx}}^*(t),
```

```math
y(t)
=
\alpha\exp\{j2\pi[f_c\tau+\mu\tau t-\tfrac12\mu\tau^2]\}.
```

Therefore the **scientific signed beat frequency** under the GeoDOA `exp(-j2 pi f t)` convention is

```math
f_{b,\mathrm{sci}}=-\mu\tau.
```

For the same sampled exponential, the standard NumPy/MATLAB forward FFT coordinate has the opposite sign mapping and, for positive `mu` and positive delay in this dechirp convention, the peak appears at `+mu tau` on the conventional FFT frequency coordinate.

The following must remain distinct:

- scientific signed frequency;
- mixer/dechirp convention;
- signed chirp slope;
- software FFT-bin/frequency coordinate;
- frequency-index ordering such as `fftshift`.

`fftshift` is an index reordering operation; it does not by itself reconcile scientific and software frequency-sign conventions.

For stationary monostatic range magnitude,

```math
|f_b|=|\mu|\tau,
\qquad
R=\frac{v|f_b|}{2|\mu|}.
```

This relation is not a universal moving-target FMCW range formula.

## 22. MIMO Physical and Virtual Semantics

A physical MIMO measurement channel retains the pair provenance

```text
(Tx_i, Rx_j).
```

For a general far-field bistatic target, the Tx and Rx look directions need not be equal. To first order,

```math
\Delta\mathcal P_{ij}
\approx
-
\Delta\mathbf r_{\mathrm{Tx},i}^T\hat{\mathbf u}_{\mathrm{Tx}}
-
\Delta\mathbf r_{\mathrm{Rx},j}^T\hat{\mathbf u}_{\mathrm{Rx}}.
```

The corresponding relative spatial phase is

```math
a_{ij}
=
\exp\{-jk[
\Delta\mathbf r_{\mathrm{Tx},i}^T\hat{\mathbf u}_{\mathrm{Tx}}
+
\Delta\mathbf r_{\mathrm{Rx},j}^T\hat{\mathbf u}_{\mathrm{Rx}}
]\}.
```

Only under the common-look/colocated far-field specialization

```math
\hat{\mathbf u}_{\mathrm{Tx}}
\approx
\hat{\mathbf u}_{\mathrm{Rx}}
\approx
\hat{\mathbf u}
```

may a virtual displacement be written

```math
\Delta\mathbf r_{v,ij}
=
\Delta\mathbf r_{\mathrm{Tx},i}
+
\Delta\mathbf r_{\mathrm{Rx},j}.
```

Thus `r_v = r_Tx + r_Rx` is not a universal bistatic law. Virtual geometry is derived and never replaces physical Tx/Rx geometry or pair identity.

TDM-MIMO channels are not automatically simultaneous. Motion/timing compatibility is required before constructing a simultaneous-equivalent virtual snapshot.

## 23. Source, Target, Path, and Arrival Semantics

GeoDOA distinguishes:

- physical emitter/source;
- target/scatterer;
- propagation path;
- spatial arrival.

A single physical emitter may generate multiple arrivals through multipath. An extended target may generate multiple scattering arrivals. Therefore physical source/target count and spatial-arrival count are not synonyms.

In the canonical narrowband arrival model,

```math
\mathbf x[k]
=
\mathbf A\mathbf s[k]+
\mathbf n[k],
```

`A` is `N x Q_arr` and `s[k]` contains effective arrival-domain complex coefficients. These coefficients are not automatically raw transmitter waveform samples or calibrated physical powers.

## 24. Source/Noise Statistics and Covariance

Define source/arrival covariance

```math
\mathbf R_s
=
\mathbb E[\mathbf s\mathbf s^H].
```

For zero-mean signal/noise with zero signal-noise cross-covariance,

```math
\mathbf R_x
=
\mathbf A\mathbf R_s\mathbf A^H
+
\mathbf R_n.
```

If `E[s n^H] != 0`, the cross terms shall not be silently discarded.

A covariance is Hermitian positive semidefinite. If `mu_x != 0`,

```math
\mathbf C_x
=
\mathbb E[(\mathbf x-\boldsymbol\mu_x)
(\mathbf x-\boldsymbol\mu_x)^H]
```

is the covariance, while `E[x x^H]` is an uncentered second moment.

For known zero mean,

```math
\hat{\mathbf R}_0
=
\frac1L\mathbf X\mathbf X^H.
```

For sample-mean centering,

```math
\bar{\mathbf x}
=
\frac1L\sum_k\mathbf x[k],
\qquad
\mathbf X_c
=
\mathbf X-\bar{\mathbf x}\mathbf 1^T,
```

and the conventional centered estimator is

```math
\hat{\mathbf R}_c
=
\frac1{L-1}\mathbf X_c\mathbf X_c^H,
\qquad L\ge2.
```

Calling this estimator `unbiased` requires the relevant statistical assumptions (for example iid/common covariance conditions). The denominator `L-1` alone does not guarantee unbiasedness for correlated snapshots.

The centered rank ceiling is

```math
\operatorname{rank}(\hat{\mathbf R}_c)
\le
\min(N,L-1).
```

`L-1 >= r` is only a necessary rank-feasibility condition for representing an `r`-dimensional sample subspace; it is not a statistical adequacy guarantee.

## 25. Coherence, Observable Rank, and Model Order

ADR-002 distinguishes:

```text
Q_phys   physical source/target count
Q_arr    spatial-arrival count
r_s      rank(R_s)
r_obs    rank(A R_s A^H)
r_hat    estimated signal-subspace order
Q_peak   detected/selected peak count
```

These quantities may coincide under a restricted textbook model but are not definitions of one another.

In general,

```math
\operatorname{rank}(\mathbf A\mathbf R_s\mathbf A^H)
\le
\min(\operatorname{rank}\mathbf A,\operatorname{rank}\mathbf R_s).
```

If two arrivals are perfectly coherent, `s_2 = alpha s_1`, then `rank(R_s)=1` even when `Q_arr=2`.

If two steering vectors are common-phase equivalent because of spatial aliasing or projection ambiguity, `rank(A)` may fall even when the source covariance is full rank.

A model-order estimator based on covariance eigenspaces therefore estimates an observable/statistical subspace order. It shall not be labeled a physical-source counter unless additional assumptions justify that interpretation.

For classical MUSIC with white noise, a nonempty noise subspace requires

```math
r_{\mathrm{obs}}<N.
```

This is an algorithm-applicability condition, not a physical scene-validity rule.

## 26. Noise and SNR Semantics

The reference statistical configuration may use

```math
\mathbf n[k]
\sim
\mathcal{CN}(0,\sigma_n^2\mathbf I),
```

where

```math
\mathbb E|n_n|^2=\sigma_n^2
```

and for circular complex Gaussian noise

```math
\operatorname{Var}(\Re n_n)
=
\operatorname{Var}(\Im n_n)
=
\frac{\sigma_n^2}{2}.
```

Colored noise is valid physics/statistics but is outside the simplest white-noise reference configuration.

A bare statement such as `SNR = 10 dB` is insufficient for reproducible evidence. An SNR definition must specify numerator, denominator, measurement point, aggregation rule, and normalization context.

For PM-001 with unit-magnitude geometry-only manifold and one declared source power `P_s`, a reference per-channel complex-baseband input SNR may be

```math
\mathrm{SNR}_{\mathrm{ch}}
=
\frac{P_s}{\sigma_n^2}.
```

Noise standard deviation, complex noise variance, source amplitude, and source power are distinct quantities.

## 27. Units and Dimensional Semantics

Canonical internal physical quantities use SI-compatible units with explicit semantic angular/logarithmic distinctions:

| Quantity | Canonical semantic unit |
|---|---|
| position/range/aperture | m |
| time/delay | s |
| frequency/bandwidth/Doppler | Hz |
| angular frequency | rad/s |
| phase/angle | rad |
| wavelength | m |
| phase constant/wavenumber | rad/m |
| propagation speed | m/s |
| chirp slope | Hz/s |
| attenuation constant | typed inverse length, e.g. Np/m |
| direction cosine | dimensionless |
| geometry-only steering coefficient | dimensionless complex |
| snapshot value | declared measurement unit |
| covariance/eigenvalue | measurement-unit squared |
| correlation coefficient | dimensionless |
| SNR | dimensionless, optionally dB representation |
| RCS | m^2 |
| indices | dimensionless integer |

`Hz` and `rad/s` are not semantically interchangeable. `rad/m` phase constant and `Np/m` attenuation are not semantically interchangeable. External GHz/MHz/ns/cm/degree/dB inputs must be converted explicitly at validated boundaries.

Absolute path response need not be dimensionless; its unit depends on the declared response normalization. Relative same-unit path response is dimensionless when the denominator is nonzero.

Normalized simulation amplitude shall not be labeled physical voltage, field, or power without an explicit calibration/measurement model.

## 28. PM-001 — Reference Far-Field Narrowband Receive-Array Profile

PM-001 is the initial validated physical/measurement profile. It declares:

```text
one-way receive-equivalent sensing
single direct propagation path
homogeneous medium
isotropic medium
nondispersive medium
lossless medium
finite positive constant propagation speed
plane-wave-compatible geometry/scene
array-narrowband-compatible signal/path
quasi-static spatial manifold over the declared processing window
ideal identical scalar receive channels
simultaneous-equivalent channel observation
relative geometry-only unit-magnitude manifold
normalized complex-baseband source/arrival coefficients
```

PM-001 is compositional and versioned conceptually. It is not implemented as a combinatorial subclass for every possible far/near, narrow/wide, static/moving combination.

A separate reference statistical configuration may add zero-mean uncorrelated sources and spatially white circular complex Gaussian noise. A separate algorithm compatibility contract may add classical MUSIC requirements. These are not part of the physical profile itself.

## 29. Software Semantic Requirements

The software architecture shall preserve the following separations without requiring one class per mathematical symbol:

```text
PhysicalModelProfile
StatisticalScenario / source statistics
Estimator/Algorithm configuration

Absolute path response
Relative path response
Geometry-only manifold

Source / emitter
Target / scatterer
Propagation path
Spatial arrival

Raw measurement tensor
Measurement-axis semantics
Spatial snapshot set

Physical MIMO channel pair
Derived virtual channel/geometry

Population covariance
Sample covariance estimate
Uncentered second moment

Physical source count
Spatial-arrival count
Observable signal rank
Estimated subspace order
Detected peak count

Scientific signed frequency
Software FFT coordinate
```

Rich semantics belong at validated boundaries/domain/application layers; numerical kernels may remain simple pure NumPy-oriented functions operating on canonical data.

Authoritative primitive quantities shall be stored once; wavelength, wavenumber, and similar dependent quantities are derived from authoritative frequency/medium context rather than duplicated as independent truth.

Compatibility metrics are distinct from threshold/acceptance policies. ADR-002 defines what is measured; ADR-004 governs evidence and acceptance policy where a universal threshold is not part of the physical definition.

## 30. Required Response Classes

ADR-002 adopts the Phase 0C four-class response taxonomy:

- **REJECT** — the requested input/domain object/operation is scientifically undefined or inconsistent;
- **INCOMPATIBLE / REQUIRE OTHER MODEL** — the physical scenario is meaningful but the requested profile/model/algorithm is insufficient;
- **DIAGNOSTIC / WARN** — computation may proceed but ambiguity, aliasing, conditioning, approximation sensitivity, or interpretation limits must remain explicit;
- **VALID** — the condition lies within the declared contract.

A physically valid scene shall not be rejected merely because PM-001 or classical MUSIC is insufficient.

## 31. Forbidden Implicit Behavior

GeoDOA shall not silently:

- infer units from numeric magnitude;
- reinterpret Hz as rad/s or degrees as radians;
- switch plane-wave and spherical models;
- switch narrowband and wideband models;
- reinterpret scientific frequency using software FFT sign conventions;
- treat `fftshift` as a physical sign conversion;
- choose or change FMCW mixer/dechirp convention;
- discard signed chirp slope;
- infer raw tensor axis meaning from shape;
- treat every raw sample index as a spatial snapshot;
- renumber physical channels from matrix row order;
- collapse physical and virtual MIMO channel identities;
- manufacture a virtual-sum coordinate for arbitrary bistatic geometry;
- collapse source, target, path, and arrival semantics;
- equate physical source count with covariance rank/model order/peak count;
- call an uncentered second moment a covariance when the mean is nonzero;
- infer unbiasedness from use of `1/(L-1)` alone;
- silently center covariance data;
- silently Hermitian-symmetrize or PSD-clip a declared covariance;
- normalize a calibrated/full physical manifold without an explicit transformation;
- treat structured interference as white noise without a declared approximation;
- apply generic `delay *= 2` active-radar logic;
- promote/degrade a model profile after a compatibility failure;
- invent PASS/FAIL when only a metric has been computed and no threshold policy is declared.

## 32. Golden Reference Requirements

ADR-002 acceptance requires deterministic hand-calculated evidence for at least:

- spherical-versus-plane-wave curvature error;
- array narrowband bandwidth-delay compatibility;
- stationary FMCW beat sign and range;
- raw FMCW cube to range-selected spatial snapshots/covariance;
- small covariance eigendecomposition;
- MUSIC noise-subspace orthogonality;
- mean-centered sample-covariance rank ceiling;
- Doppler sign under the scientific convention;
- complex-noise/SNR scaling;
- coherent-arrival rank collapse;
- general bistatic versus common-look virtual-sum MIMO semantics;
- nondispersive phase/group-delay consistency.

The authoritative expected values are stored in `ADR-002_GOLDEN_REFERENCE_PROBLEMS.md` and become future Phase 1 software test oracles.

## 33. Boundary and Failure Requirements

Detailed Gate F behavior is recorded separately in `ADR-002_BOUNDARY_FAILURE_ANALYSIS.md`. The governing principles are:

- invalid numeric/domain inputs are rejected;
- valid physics outside PM-001 requires another model rather than silent approximation;
- measurement/statistical incompatibility is reported at its actual layer;
- structural identifiability limitations are not misreported as estimator failures;
- algorithm applicability conditions do not redefine physical scene validity;
- provenance deficits block scientific claims that depend on the missing convention/metadata;
- numerical repair is never presented as original-input validation.

## 34. Consequences

### 34.1 Positive consequences

- ADR-001 steering signs are recovered from propagation physics rather than duplicated by convention.
- Near/far, narrow/wide, static/dynamic, passive/active, and medium assumptions become independent scientific axes.
- Raw radar/FMCW/MIMO data can later map into one canonical array-processing view without erasing acquisition provenance.
- Scientific-frequency/FFT sign mismatch is explicit before implementation or FPGA validation.
- General bistatic MIMO is not incorrectly reduced to `r_Tx + r_Rx`.
- Covariance, rank, source count, model order, and peak count remain scientifically distinct.
- Future fixed-point/FPGA backends inherit explicit units, scaling, and measurement semantics.

### 34.2 Costs

- Configuration and result objects require more provenance than a minimal MUSIC script.
- Some conditions that a simple script would silently accept must produce incompatibility or diagnostic results.
- Active moving radar, wideband, near-field, dispersive, multipath, and calibrated-sensor extensions require additional profiles/providers rather than ad hoc flags.

These costs are intentional consequences of scientific traceability.

## 35. Deferred Decisions

The following are intentionally deferred:

- universal numeric thresholds for far-field/narrowband/quasi-static compatibility;
- exact normative definition of a generic projective/common-phase manifold distance;
- full moving-target FMCW beat decomposition;
- wideband Doppler time-scaling model;
- full inhomogeneous/ray/multipath propagation implementation;
- detailed active-radar stop-and-hop validity threshold;
- final Python class/type names;
- concrete run-identity schema and scientific-contract version storage mechanism.

Deferral does not permit hidden assumptions. A capability requiring one of these decisions must remain unavailable, explicitly approximated, or diagnostic until the governing contract is added.

## 36. Acceptance Criteria

ADR-002 is acceptable only if:

1. Gate A confirms physical consistency and scope boundaries;
2. Gate B confirms mathematical/sign/rank/covariance consistency;
3. Gate C confirms units and dimensional semantics;
4. Gate D confirms software semantic mapping without hidden inference/class inflation;
5. Gate E provides hand-calculated test-oracle evidence;
6. Gate F defines explicit boundary/failure behavior;
7. the final cross-gate audit confirms no contradiction with accepted ADR-001;
8. governing ADR, audit evidence, boundary evidence, and Golden Reference artifacts are all committed together on the Phase 0C branch before final acceptance status is recorded.
