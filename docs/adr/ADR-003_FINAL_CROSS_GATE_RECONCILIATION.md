# ADR-003 — Final Cross-Gate Reconciliation

- **ADR:** `ADR-003-sensor-imperfections-mutual-coupling-calibration.md`
- **Phase:** 0C — Scientific Foundations
- **Status:** PASS — ready for final acceptance record
- **Date:** 2026-08-23
- **Purpose:** Final reconciliation of ADR-003 after Gates A–F, Golden Reference evidence, and boundary/failure analysis.

## 1. Reconciliation Decision

ADR-003 has passed all six Phase 0C acceptance gates and, after final cross-gate reconciliation, contains no unresolved scientific contradiction within its declared scope.

The reconciliation result is:

```text
Gate A — Physical Consistency                  PASS
Gate B — Mathematical Consistency              PASS
Gate C — Dimensional and Unit Consistency      PASS
Gate D — Software Semantic Consistency         PASS
Gate E — Hand-Calculated Reference Evidence    PASS
Gate F — Boundary and Failure Analysis         PASS
Final Cross-Gate Reconciliation                PASS
```

ADR-003 is therefore eligible for final acceptance, subject only to final acceptance metadata/status synchronization and creation of `ADR-003_FINAL_ACCEPTANCE_RECORD.md`.

---

## 2. Gate A Reconciliation — PASS

Gate A identified one material ambiguity in the original draft's channel-wise position-error phase expression: a displaced `epsilon_ref` could be misread as moving ADR-001's stable nominal phase reference.

The governing contract was corrected to distinguish:

### Fixed ADR-001 reference

\[
\boxed{
\delta\phi_n^{(\mathrm{fixed\ ref})}
\approx-k\hat{\mathbf u}^T\boldsymbol\varepsilon_n
}
\]

from the explicitly specialized moved-reference case

\[
\boxed{
\delta\phi_n^{(\mathrm{moved\ ref})}
\approx-k\hat{\mathbf u}^T
(\boldsymbol\varepsilon_n-\boldsymbol\varepsilon_{\rm ref})
}
\]

and the reference-invariant pairwise result

\[
\boxed{
\delta\phi_{nm}
=-k(\boldsymbol\varepsilon_n-\boldsymbol\varepsilon_m)^T\hat{\mathbf u}.
}
\]

Rigid translation therefore remains a common-phase effect under the far-field model and produces no pairwise relative-manifold distortion.

**Cross-gate result: PASS.**

---

## 3. Gate B Reconciliation — PASS

Gate B independently confirmed the governing algebra, conjugation, covariance expansions, rank statements, eigenspace relations, calibration formulas, and MUSIC identities.

Material exact/approximate distinctions remain consistent:

- exact physical geometry precedes far-field approximation;
- exact SRO reciprocal relation precedes its small-error approximation;
- `Delta^2/12` remains a bounded high-resolution quantization approximation;
- covariance perturbation retains the exact quadratic term, while the first-order truncation is explicitly labeled;
- Davis–Kahan/eigenvector sensitivity statements remain bounds/perturbation relations rather than universal equalities;
- the rank-one MUSIC/projective leakage identity is exact under its declared unit-norm rank-one conditions.

No algebraic, conjugation, rank, or projector contradiction remains.

**Cross-gate result: PASS.**

---

## 4. Gate C Reconciliation — PASS

Gate C established a typed/reference-plane unit contract rather than assuming all sensor operators are dimensionless.

The important final unit rules are:

```text
physical positions/path lengths       meters
physical delays/skew/jitter           seconds
ordinary frequency                    hertz
angular frequency                     rad/s
wavenumber                             rad/m
scientific angles/phases               radians internally
ADC input quantities                  declared engineering units, typically volts
raw ADC codes                         dimensionless integer codes with declared transfer
covariance                            squared/product units of represented channels
```

The project shall not silently convert:

```text
meters <-> wavelengths
Hz <-> rad/s
seconds <-> samples
radians <-> degrees
volts <-> ADC codes
physical manifold <-> unit-norm steering
linear ratios <-> dB
```

### Tikhonov regularization refinement

For

\[
\mathbf C_\lambda
=(\mathbf H^H\mathbf H+\lambda\mathbf I)^{-1}\mathbf H^H,
\]

dimensional homogeneity requires

\[
\boxed{[\lambda\mathbf I]=[\mathbf H^H\mathbf H].}
\]

Therefore `lambda` is dimensionless only when `H`/the inverse problem has been expressed in compatible dimensionless/scaled coordinates. Otherwise `lambda` carries the units required to match `H^H H`.

This refinement is normative for later configuration/software semantics and is explicitly protected by Gate-F boundary case F-079.

**Cross-gate result: PASS.**

---

## 5. Gate D Reconciliation — PASS

Gate D confirmed that ADR-003 maps cleanly to the GeoDOA architecture without requiring premature class inflation or semantic collapse.

The following identities must remain distinct in software/public scientific artifacts:

```text
a_nom / a_phys / a_meas / a_em / a_cal / a_truth
nominal geometry / realized geometry / calibrated estimate
element response / electronic gain
Z / S / T_L / effective coupling C
channel delay / fixed sample skew / SRO / jitter / LO phase / CFO / digital latency
ADC volts / ADC codes / dequantized digital data / downstream fixed-point arithmetic
model calibration / data correction
physical port state / digital selection mask
ordinary-complex / augmented or widely-linear statistics
population covariance / sample covariance / uncentered second moment
```

Compatibility remains multi-axis rather than one generic Boolean.

Named/versioned sensor profiles are preferred over loose effect flags or a generic `realistic_sensor=True` switch.

The current repository has no material scientific implementation beyond the package skeleton, so no existing authoritative code contradicts this contract.

**Cross-gate result: PASS.**

---

## 6. Gate E Reconciliation — PASS AFTER NUMERICAL CORRECTION

The canonical ADR-003 Golden Reference set is:

```text
GRP-014 — Position-error phase distortion and rigid-translation invariance
GRP-015 — Gain/phase mismatch and two-sensor DOA bias
GRP-016 — Mutual-coupling manifold distortion
GRP-017 — Coupling to covariance/eigenspace/MUSIC leakage
```

Supplemental deterministic references are:

```text
ADR-003-SRC-01 — physical delay versus later sampling sign
ADR-003-SRC-02 — SRO fractional-period error and accumulated drift
ADR-003-SRC-03 — differential-CFO finite-window coherence
ADR-003-SRC-04 — ideal ADC step/quantization-noise/SNR arithmetic
ADR-003-SRC-05 — DC offset in an uncentered second moment
ADR-003-SRC-06 — inverse calibration and noise amplification
ADR-003-SRC-07 — calibration-grid phase gauge/interpolation failure
ADR-003-SRC-08 — noncommuting gain/coupling operators
```

### Final numerical correction discovered during reconciliation

A transcription error was found in GRP-014's degree-to-radian conversion for the exact angular bias.

The degree result was already correct:

\[
\hat\theta=\sin^{-1}(0.51)=30.6638297424^\circ
\]

so

\[
\Delta\theta
=0.6638297424^\circ.
\]

The correct radian conversion is

\[
\boxed{
\Delta\theta
\approx0.01158601468\ \mathrm{rad}
}
\]

rather than the earlier mistyped `0.011585033 rad`.

The Golden Reference artifact was corrected before final acceptance. The direction-cosine result, degree result, first-order approximation, rigid-translation result, and regression oracle were otherwise unchanged.

Independent arithmetic cross-checks confirm:

```text
GRP-014 inferred u                 0.51
GRP-014 inferred theta             30.6638297424 deg
GRP-014 exact angular bias         0.6638297424 deg
GRP-014 exact angular bias rad     0.01158601468 rad
GRP-015 inferred u                 4/9
GRP-015 inferred theta             26.3877999612 deg
GRP-016 b2/b1                      0.8 - 0.6j
GRP-016 inferred u                 0.204832764699
GRP-016 inferred theta             11.8197094310 deg
GRP-017 eigenvalues                {2.5,0} and {3.5,1} after +I
GRP-017 rho^2                      0.8
GRP-017 projective leakage         0.2
SRC-04 ADC step                    488.28125 uV
SRC-04 quantization sigma          about 140.954656 uV
```

**Cross-gate result: PASS.**

---

## 7. Gate F Reconciliation — PASS

Gate F defines 140 explicit boundary/failure cases across every material ADR-003 contract family.

The accepted top-level response taxonomy is:

- **REJECT** — invalid/undefined input, artifact, operation, or scientific claim;
- **INCOMPATIBLE / REQUIRE OTHER MODEL** — meaningful physical scenario outside the selected sensor/calibration/statistical/estimator profile;
- **DIAGNOSTIC / WARN** — computation may proceed with preserved ambiguity, conditioning, uncertainty, approximation sensitivity, or interpretation limits;
- **VALID** — operation lies within the declared profile.

`UNRESOLVED` remains a scientific knowledge state and is never silently promoted to compatible/valid.

The failure-layer ordering is accepted as:

```text
input/domain validity
 -> units/reference planes/channel identity
 -> physical sensor-profile compatibility
 -> timing/sampling compatibility
 -> receiver/ADC operating region
 -> calibration domain/provenance
 -> calibration identifiability/conditioning
 -> covariance/statistical compatibility
 -> eigenspace/model-order feasibility
 -> estimator applicability
 -> performance/peak interpretation
```

This prevents downstream estimator symptoms from masking upstream physical/calibration failures.

**Cross-gate result: PASS.**

---

## 8. Cross-ADR-001 / ADR-002 Consistency — PASS

ADR-003 continues to inherit without override:

- temporal phasor `exp(-j omega t)`;
- look direction from array to source;
- incident propagation direction `-u_hat`;
- receive steering sign `exp[-j k(r_n-r_ref)^T u_hat]`;
- stable nominal phase-reference semantics;
- exact path/delay before far-field/narrowband approximation;
- physical-delay transfer `exp(+j omega delta tau)`;
- snapshot simultaneous-equivalent semantics;
- covariance/source/noise/rank distinctions;
- physical MIMO `(Tx_i,Rx_j)` provenance.

ADR-003 adds real sensor/receiver deviations and calibration semantics without redefining those accepted foundations.

**Cross-ADR result: PASS.**

---

## 9. Initial Phase-1 Sensor Profile Reconciliation — PASS

The accepted initial ADR-003 implementation boundary remains deliberately ideal:

```text
nominal geometry = physical geometry
ideal identical scalar unit-response elements
no mutual-coupling distortion
unity differential electronic gain/phase
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

Thus, for deterministic sensor imperfections,

\[
\boxed{\mathcal H_{\rm sensor}^{\rm Phase1}\equiv\mathcal I.}
\]

The richer nonideal mechanisms are governed scientifically but remain implementation-deferred until activated through named/versioned bounded profiles with their own verification evidence.

**Cross-gate result: PASS.**

---

## 10. Evidence Set Reconciliation — PASS

The final ADR-003 scientific evidence set is:

```text
docs/adr/ADR-003-sensor-imperfections-mutual-coupling-calibration.md
docs/adr/ADR-003_EXPLORATION_CHECKPOINT.md
docs/adr/ADR-003_EXPLORATION_3.7_RECEIVER_QUANTIZATION.md
docs/adr/ADR-003_EXPLORATION_3.8_UNIFIED_SENSOR_IMPERFECTION_OPERATOR.md
docs/adr/ADR-003_EXPLORATION_3.9_CALIBRATION_MODELS.md
docs/adr/ADR-003_EXPLORATION_3.10_DIRECT_MEASURED_CST_MANIFOLD_CALIBRATION.md
docs/adr/ADR-003_EXPLORATION_3.11_ERROR_METRICS_IDENTIFIABILITY.md
docs/adr/ADR-003_EXPLORATION_3.12_COVARIANCE_EIGENSPACE_MUSIC_PROPAGATION.md
docs/adr/ADR-003_EXPLORATION_3.13_COMPATIBILITY_INITIAL_PROFILE.md
docs/adr/ADR-003_EXPLORATION_3.14_CROSS_SECTION_RECONCILIATION.md
docs/adr/ADR-003_PRE_GATE_CONSISTENCY_REVIEW.md
docs/adr/ADR-003_ACCEPTANCE_AUDIT.md
docs/adr/ADR-003_GATE_C_DIMENSIONAL_UNIT_CONSISTENCY_AUDIT.md
docs/adr/ADR-003_GATE_D_SOFTWARE_SEMANTIC_CONSISTENCY_AUDIT.md
docs/science/golden_reference/ADR-003_GOLDEN_REFERENCE_PROBLEMS.md
docs/adr/ADR-003_BOUNDARY_FAILURE_ANALYSIS.md
docs/adr/ADR-003_GATE_F_AUDIT.md
docs/adr/ADR-003_FINAL_CROSS_GATE_RECONCILIATION.md
```

No evidence artifact requires renumbering of the roadmap's GRP assignments.

**Cross-gate result: PASS.**

---

## 11. Blocking-Findings Summary

```text
Physical/sign contradiction:                       NONE
Mathematical contradiction:                        NONE
Dimensional/unit contradiction:                    NONE
Software-semantic contradiction:                   NONE
Golden Reference inconsistency after correction:   NONE
Unclassified material boundary family:             NONE
ADR-001 override:                                   NONE
ADR-002 override:                                   NONE
Phase-1 scope leak:                                 NONE
Premature implementation claim:                     NONE
Unresolved acceptance blocker:                      NONE
```

---

## 12. Final Reconciliation Decision

\[
\boxed{\text{ADR-003 Final Cross-Gate Reconciliation: PASS}}
\]

ADR-003 has no unresolved scientific acceptance finding within its declared scope.

The next and final formal actions are:

1. create `ADR-003_FINAL_ACCEPTANCE_RECORD.md`;
2. synchronize governing ADR metadata to `Accepted` and reference the final evidence artifacts;
3. preserve the bounded Phase-1 implementation profile and all deferred-profile requirements.
