# ADR-003 — Final Acceptance Record

- **ADR:** `ADR-003-sensor-imperfections-mutual-coupling-calibration.md`
- **Phase:** 0C — Scientific Foundations
- **Final status:** ACCEPTED
- **Acceptance date:** 2026-08-23
- **Purpose:** Final scientific acceptance of ADR-003 after Gates A–F and final cross-gate reconciliation.

## 1. Acceptance Decision

ADR-003 — Sensor Imperfections, Mutual Coupling, and Calibration is **ACCEPTED** as the authoritative GeoDOA scientific contract for its declared scope.

All Phase 0C acceptance gates pass:

| Gate | Requirement | Final Status | Primary Evidence |
|---|---|---|---|
| A | Physical consistency | PASS | `ADR-003_ACCEPTANCE_AUDIT.md` |
| B | Mathematical consistency | PASS | `ADR-003_ACCEPTANCE_AUDIT.md` |
| C | Dimensional and unit consistency | PASS | `ADR-003_GATE_C_DIMENSIONAL_UNIT_CONSISTENCY_AUDIT.md` |
| D | Software semantic consistency | PASS | `ADR-003_GATE_D_SOFTWARE_SEMANTIC_CONSISTENCY_AUDIT.md` |
| E | Hand-calculated reference evidence | PASS | `../science/golden_reference/ADR-003_GOLDEN_REFERENCE_PROBLEMS.md` |
| F | Boundary and failure analysis | PASS | `ADR-003_BOUNDARY_FAILURE_ANALYSIS.md`, `ADR-003_GATE_F_AUDIT.md` |
| Final | Cross-gate reconciliation | PASS | `ADR-003_FINAL_CROSS_GATE_RECONCILIATION.md` |

## 2. Accepted Core Decision

GeoDOA shall model nonideal sensor/receiver behavior through a **typed physical sensor/receiver operator graph**, not one universal imperfection matrix.

The accepted physical chain is conceptually:

```text
scene/source state
 -> propagation on declared physical geometry
 -> element/polarization/open-circuit response
 -> loading/mutual coupling/network response
 -> analog receiver gain/phase/delay/filter/LO/IQ response
 -> stage-specific receiver noise
 -> analog nonlinearity when active
 -> physical sampling epochs/aperture effects
 -> ADC clipping/quantization/code mapping
 -> digital measurement
 -> optional digital selection/deskew/calibration correction/DSP
```

Calibration remains a separate inference/correction activity and is not retroactively inserted as a physical cause of the measurement.

## 3. Accepted Response Taxonomy

The following response objects remain scientifically distinct:

\[
\boxed{
\mathbf a_{\rm nom},
\mathbf a_{\rm phys},
\mathbf a_{\rm meas},
\mathbf a_{\rm em},
\mathbf a_{\rm cal}
}
\]

and, when explicitly defined by simulation,

\[
\boxed{\mathbf a_{\rm truth}}.
\]

No implementation may silently switch among these meanings.

## 4. Accepted Position-Error Semantics

Physical geometry is

\[
\mathbf r_n^{\rm phys}
=\mathbf r_n^{\rm nom}+\boldsymbol\varepsilon_n.
\]

With the same fixed ADR-001 spatial reference,

\[
\boxed{
\delta\phi_n^{(\mathrm{fixed\ ref})}
\approx-k\hat{\mathbf u}^T\boldsymbol\varepsilon_n
}
\]

under the declared far-field first-order approximation.

A separately moved reference may use

\[
\boxed{
\delta\phi_n^{(\mathrm{moved\ ref})}
\approx-k\hat{\mathbf u}^T
(\boldsymbol\varepsilon_n-\boldsymbol\varepsilon_{\rm ref})
}
\]

only when that moved reference is explicitly declared.

The pairwise reference-invariant phase distortion is

\[
\boxed{
\delta\phi_{nm}
=-k(\boldsymbol\varepsilon_n-\boldsymbol\varepsilon_m)^T\hat{\mathbf u}.
}
\]

Rigid translation is therefore common phase rather than relative-manifold distortion in the accepted far-field profile.

## 5. Accepted Gain/Phase and Element Semantics

A bounded per-channel electronic response may use

\[
g_n=\rho_n e^{j\phi_n},
\qquad
\mathbf G=\operatorname{diag}(g_1,\ldots,g_N).
\]

Common phase is not spatial distortion and cancels from ordinary covariance.

Common gain is projectively irrelevant to manifold direction but may affect SNR/dynamic range depending on stage ordering relative to noise, nonlinearity, clipping, and ADC quantization.

Element response, element orientation, electromagnetic phase center, polarization response, and electronic channel gain remain distinct.

## 6. Accepted Coupling / Network Semantics

Mutual coupling is cross-element/cross-port electromagnetic interaction and shall not be reduced universally to diagonal gain/phase mismatch.

Under a declared Thevenin-style multiport specialization:

\[
\mathbf i=(\mathbf Z_A+\mathbf Z_L)^{-1}\mathbf v_{\rm oc}
\]

and

\[
\mathbf v_L
=\mathbf Z_L(\mathbf Z_A+\mathbf Z_L)^{-1}\mathbf v_{\rm oc}.
\]

The loaded-port transform

\[
\mathbf T_L
=\mathbf Z_L(\mathbf Z_A+\mathbf Z_L)^{-1}
\]

is not a universal DOA coupling matrix.

`Z`, `S`, `T_L`, effective coupling `C`, embedded patterns, and aggregate measured/EM manifolds are distinct objects.

## 7. Accepted Timing / Synchronization Semantics

The following remain distinct:

```text
static channel phase
physical/electrical channel delay
fixed sampling-time offset
sampling-rate offset (SRO)
sampling jitter
receiver-reference/LO phase offset
receiver-reference/LO frequency offset
post-acquisition digital latency
```

A positive physical waveform delay under `exp(-j omega t)` produces `exp(+j omega delta_tau)`, while observing the same tone at a later sampling epoch produces `exp(-j omega delta_t)`.

The exact fractional period/rate relation is

\[
1+\epsilon_T=\frac{1}{1+\epsilon_f},
\]

with small-error approximation

\[
\epsilon_T\approx-\epsilon_f.
\]

Material differential SRO/CFO over the covariance window can invalidate a fixed-manifold snapshot model.

## 8. Accepted Receiver / ADC Semantics

ADC acquisition quantization is distinct from downstream FPGA/processor fixed-point arithmetic.

For an ideal `N_b`-bit ADC with full-scale range

\[
V_{\rm FSR}=V_{\max}-V_{\min},
\]

the nominal ideal step is

\[
\Delta=\frac{V_{\rm FSR}}{2^{N_b}}.
\]

The approximation

\[
\sigma_q^2\approx\frac{\Delta^2}{12}
\]

is accepted only under its high-resolution/no-overload assumptions.

Clipping is nonlinear information loss and cannot be repaired by later digital rescaling.

DC offset, I/Q imbalance, nonlinear compression/intermodulation, clipping, and quantization remain distinct receiver effects.

## 9. Accepted Calibration Semantics

GeoDOA distinguishes:

```text
characterization
parameter calibration
model calibration
data correction/equalization
direct measured/EM manifold calibration
self/joint calibration
calibration tracking/maintenance
```

Calibration state, physical state, calibrated estimate, residual mismatch, uncertainty, validity domain, and provenance remain distinguishable.

Gauge fixing does not prove physical ideality.

Structural identifiability, local observability, conditioning, uncertainty, and optimizer convergence are independent concepts.

For fixed linear correction,

\[
\mathbf R_{n,\rm corr}
=\mathbf C_{\rm corr}\mathbf R_n\mathbf C_{\rm corr}^H.
\]

Singular physical response cannot be exactly inverted; pseudoinverse and regularized corrections do not recreate null-space information.

## 10. Accepted Regularization Unit Rule

For Tikhonov-type correction

\[
\mathbf C_\lambda
=(\mathbf H^H\mathbf H+\lambda\mathbf I)^{-1}\mathbf H^H,
\]

the accepted dimensional rule is

\[
\boxed{[\lambda\mathbf I]=[\mathbf H^H\mathbf H].}
\]

Therefore `lambda` is not universally dimensionless. It is dimensionless only for a corresponding dimensionless/scaled inverse problem.

## 11. Accepted Direct Measured / CST / Full-Wave Semantics

Measured and EM/full-wave manifolds are aggregate response evidence/models, not automatically physical truth and not automatically uniquely decomposable into physical causes.

Direct manifold artifacts must preserve, as applicable:

```text
complex response
frequency
direction/range
polarization basis
coordinate frame
channel identity
reference plane
normalization/gauge
included/de-embedded effects
interpolation method/domain
uncertainty/quality information
measurement or solver provenance
hardware/environment state
```

Magnitude-only response is insufficient by default for coherent MUSIC calibration.

Arbitrary independent phase gauge changes at interpolation nodes are not accepted.

Transmit far fields shall not silently become receive manifolds without convention-checked reciprocity/normalization transformation.

## 12. Accepted Error / Identifiability Metrics

No single universal manifold-error scalar is accepted.

Raw, phase-aligned, common-complex-scale-aligned, weighted, and projective metrics answer different scientific questions.

For nonzero compatible vectors:

\[
\rho
=\frac{|\mathbf a^H\mathbf b|}{\|\mathbf a\|\|\mathbf b\|},
\qquad
\alpha=\cos^{-1}\rho,
\qquad
 d_{\rm proj}^2=1-\rho^2.
\]

The equivalence/gauge class, units, normalization, weighting, and null handling are part of the metric definition.

## 13. Accepted Covariance / Eigenspace / MUSIC Semantics

For

\[
\mathbf A_{\rm phys}=\mathbf A+\Delta\mathbf A,
\]

the exact manifold-induced covariance perturbation is

\[
\Delta\mathbf R_A
=\Delta\mathbf A\mathbf R_s\mathbf A^H
+\mathbf A\mathbf R_s\Delta\mathbf A^H
+\Delta\mathbf A\mathbf R_s\Delta\mathbf A^H.
\]

Sensor-model and finite-sample errors remain distinct:

\[
\mathbf E_{\rm sensor}
=\mathbf R_{\rm phys}-\mathbf R_{\rm nom},
\qquad
\mathbf E_{\rm sample}
=\hat{\mathbf R}-\mathbf R_{\rm phys}.
\]

Isotropic white noise shifts population covariance eigenvalues without rotating eigenvectors. Colored noise may rotate ordinary eigenspaces and may require whitening/generalized processing.

For a rank-one physical unit vector `u`, unit model vector `v`, and physical noise projector `P_n=I-u u^H`,

\[
\boxed{
\mathbf v^H\mathbf P_n\mathbf v
=1-|\mathbf u^H\mathbf v|^2
=1-\rho^2.
}
\]

This is an exact rank-one population MUSIC leakage identity, not a universal angular-bias formula.

## 14. Accepted Compatibility Semantics

Estimator compatibility is multi-axis, not one Boolean.

At minimum it distinguishes:

```text
manifold representation
reference plane
coordinate/direction convention
narrowband/frequency validity
fixed-manifold/stationarity
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

`UNRESOLVED` shall never be silently promoted to compatible.

A static known/calibrated linear imperfection can remain classical-MUSIC compatible when the estimator uses the matched manifold and all other assumptions hold.

## 15. Accepted Initial Phase-1 Sensor Profile

The first authoritative ADR-003 implementation profile is intentionally ideal:

```text
nominal geometry = physical geometry
ideal identical scalar unit-response elements
no mutual coupling
unity differential gain/phase
zero differential channel delay
common coherent clock/reference
zero differential fixed skew/SRO/CFO/deterministic jitter
simultaneous-equivalent snapshots
linear receiver
no DC offset
no I/Q imbalance
no compression/intermodulation
no clipping
unquantized floating acquisition baseline
identity/not-applied deterministic calibration state
proper-complex spatially white equal-variance additive noise
ordinary covariance/subspace representation
```

Therefore, for deterministic sensor imperfections,

\[
\boxed{\mathcal H_{\rm sensor}^{\rm Phase1}\equiv\mathcal I.}
\]

Nonideal mechanisms are scientifically governed but remain implementation-deferred until activated through named/versioned bounded profiles.

## 16. Accepted Golden Reference Evidence

The canonical accepted ADR-003 Golden References are:

```text
GRP-014 — Position-error phase distortion and rigid-translation invariance
GRP-015 — Gain/phase mismatch and two-sensor DOA bias
GRP-016 — Mutual-coupling manifold distortion
GRP-017 — Coupling to covariance/eigenspace/MUSIC leakage
```

Supplemental deterministic evidence is preserved as `ADR-003-SRC-01` through `ADR-003-SRC-08`.

During final reconciliation, the exact GRP-014 angular-bias radian conversion was corrected to

\[
\boxed{0.01158601468\ \mathrm{rad}}
\]

for the already-correct `0.6638297424 deg` bias. The Golden Reference artifact was corrected before acceptance.

## 17. Accepted Boundary Taxonomy

ADR-003 accepts the four-class top-level response taxonomy:

- **REJECT**;
- **INCOMPATIBLE / REQUIRE OTHER MODEL**;
- **DIAGNOSTIC / WARN**;
- **VALID**.

`UNRESOLVED` remains a scientific knowledge state and cannot be silently promoted.

The detailed Gate-F artifact defines 140 cases spanning sensor, timing, ADC, calibration, measured-manifold, covariance/eigenspace, estimator, MIMO, profile, and provenance boundaries.

## 18. No-Silent-Coercion Rules

GeoDOA shall not silently:

- switch among nominal/physical/measured/EM/calibrated response meanings;
- infer units;
- normalize away physically meaningful amplitude;
- convert colored noise into a white-noise assumption;
- collapse delay, fixed skew, SRO, CFO, jitter, or digital latency;
- treat ADC bits as FPGA arithmetic word length;
- treat one-bit/coarse data as high-resolution float samples;
- treat clipping as additive noise;
- treat I/Q conjugate leakage as ordinary complex gain;
- treat a digital mask as a physical port-state change;
- treat Tx far fields as Rx manifolds without declared conversion;
- extrapolate calibration outside domain silently;
- apply already-included coupling/element/radome/receiver effects twice;
- merge source count, signal rank, sample rank, and selected model order;
- repair data numerically and present the repair as original evidence;
- promote unknown/unresolved compatibility to valid.

## 19. Evidence Set

The accepted ADR-003 evidence set consists of:

```text
docs/adr/ADR-003-sensor-imperfections-mutual-coupling-calibration.md
docs/adr/ADR-003_EXPLORATION_CHECKPOINT.md
docs/adr/ADR-003_PRE_GATE_CONSISTENCY_REVIEW.md
docs/adr/ADR-003_ACCEPTANCE_AUDIT.md
docs/adr/ADR-003_GATE_C_DIMENSIONAL_UNIT_CONSISTENCY_AUDIT.md
docs/adr/ADR-003_GATE_D_SOFTWARE_SEMANTIC_CONSISTENCY_AUDIT.md
docs/science/golden_reference/ADR-003_GOLDEN_REFERENCE_PROBLEMS.md
docs/adr/ADR-003_BOUNDARY_FAILURE_ANALYSIS.md
docs/adr/ADR-003_GATE_F_AUDIT.md
docs/adr/ADR-003_FINAL_CROSS_GATE_RECONCILIATION.md
docs/adr/ADR-003_FINAL_ACCEPTANCE_RECORD.md
```

Dedicated exploration 3.7–3.14 artifacts remain retained as derivation/provenance evidence.

## 20. What Acceptance Does Not Mean

ADR-003 acceptance does not mean all nonideal sensor models are implemented in Phase 1.

It does not mean measured/CST manifold import, mutual coupling, ADC quantization, SRO/CFO correction, I/Q imbalance, nonlinear receiver modeling, one-bit MUSIC, calibration solvers, or nonideal MIMO synchronization are already software-verified capabilities.

It means the scientific contracts governing those capabilities are now fixed sufficiently to prevent implementation from silently inventing incompatible semantics.

Every deferred nonideal family still requires a bounded named/versioned implementation profile with deterministic evidence, boundary behavior, and later verification before it becomes authoritative runtime behavior.

## 21. Closure Statement

ADR-003 has no unresolved scientific acceptance finding within its declared scope.

```text
ADR-003 STATUS: ACCEPTED
Gate A: PASS
Gate B: PASS
Gate C: PASS
Gate D: PASS
Gate E: PASS
Gate F: PASS
Final Cross-Gate Reconciliation: PASS
Cross-ADR-001 consistency: PASS
Cross-ADR-002 consistency: PASS
Initial Phase-1 deterministic sensor profile: IDENTITY / IDEAL
```
