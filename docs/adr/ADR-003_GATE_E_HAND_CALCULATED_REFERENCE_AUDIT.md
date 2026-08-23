# ADR-003 — Gate E Hand-Calculated Reference Evidence Audit

- **ADR:** `ADR-003-sensor-imperfections-mutual-coupling-calibration.md`
- **Phase:** 0C — Scientific Foundations
- **Gate:** E — Hand-Calculated Reference Evidence
- **Status:** PASS
- **Prior gates:** A PASS, B PASS, C PASS, D PASS
- **Primary evidence:** `../science/golden_reference/ADR-003_GOLDEN_REFERENCE_PROBLEMS.md`
- **Acceptance status:** ADR-003 remains NOT ACCEPTED

## 1. Audit question

Do deterministic, manually inspectable reference problems exercise the material ADR-003 contracts strongly enough to serve as future regression-test oracles while preserving the distinction between exact identities, bounded approximations, profile-specific semantics, and later boundary/failure validation?

## 2. Canonical Golden Reference Problems — PASS

### GRP-014 — Position-error phase distortion

Verified coverage:

- physical versus nominal spacing;
- ADR-001 receive phase sign;
- fixed-reference channel phase perturbation;
- pairwise phase perturbation;
- nominal-model direction-cosine bias;
- exact angle conversion;
- bounded first-order angular bias;
- rigid-translation common-phase / pairwise invariance.

Verified key values:

```text
nominal spacing                    0.15 m
physical spacing                   0.153 m
u0                                 0.5
nominal pair phase                 -90.0 deg
physical pair phase                -91.8 deg
pair phase error                   -1.8 deg
u_hat                              0.51
theta_hat                          30.6638297424 deg
exact angular bias                 +0.6638297424 deg
first-order angular bias           +0.6615946745 deg
rigid-translation pair change      0
```

**Result: PASS.**

### GRP-015 — Gain/phase mismatch

Verified coverage:

- relative electronic phase mismatch;
- separation from geometry error;
- nominal-model direction-cosine bias;
- common phase covariance invariance.

Verified values:

```text
phi_e                              +10 deg on channel 2
u_hat                              0.4444444444444444
Delta u                            -0.0555555555555556
theta_hat                          26.3877999612 deg
angular bias                       -3.6122000388 deg
common phase covariance change     0 analytically
```

**Result: PASS.**

### GRP-016 — Mutual-coupling manifold distortion

Verified coverage:

- cross-channel operator effect;
- effective coupled steering vector;
- pairwise complex ratio;
- nominal uncoupled DOA mismatch.

Verified values:

```text
b                                  [1-0.5j, 0.5-1j]^T
b2/b1                              0.8-0.6j
|b2/b1|                            1
phase(b2/b1)                       -36.8698976458 deg
nominal inferred u                 about 0.204832764699
nominal inferred theta             about 11.8197094310 deg
```

**Result: PASS.**

### GRP-017 — Coupling to covariance/eigenspace/MUSIC

Verified coverage:

- rank-one covariance construction;
- Hermitian structure;
- white-noise eigenvalue shift;
- projective alignment;
- exact normalized MUSIC leakage identity;
- matched versus mismatched manifold behavior.

Verified values:

```text
R_sig = [[1.25, 1+0.75j],
         [1-0.75j, 1.25]]
eig(R_sig)                         {2.5, 0}
eig(R_sig + I)                     {3.5, 1}
a^H b                              2
||a||^2                            2
||b||^2                            2.5
rho^2                              0.8
1-rho^2                            0.2
normalized nominal MUSIC denom     0.2
normalized matched MUSIC denom     0
```

**Result: PASS.**

## 3. Supplemental deterministic references — PASS

The canonical roadmap reserves only GRP-014 through GRP-017 for ADR-003. The following references are therefore intentionally named `ADR-003-SRC-*`, following the established ADR-002 evidence pattern rather than consuming future GRP IDs.

### SRC-01 — Physical delay versus later sampling

Verified:

```text
100 MHz, +100 ps physical delay    +3.6 deg
100 MHz, +100 ps later sampling    -3.6 deg
```

**PASS.**

### SRC-02 — SRO reciprocal relation and epoch drift

Verified:

```text
epsilon_f                          +1e-5
epsilon_T                          about -9.999900001e-6
epoch difference after nominal 1s  about -9.999900001 us
```

**PASS.**

### SRC-03 — Differential CFO coherence

For `Delta f=1 Hz`, `T=0.5 s`:

```text
|Gamma|                            2/pi = 0.6366197724
arg(Gamma)                         +90 deg for [0,T]
```

**PASS.**

### SRC-04 — ADC quantization arithmetic

For a 12-bit ADC with 2-V full-scale range:

```text
Delta                              488.28125 uV
sigma_q                            about 140.954656 uV
ideal full-scale sine SNR          74.00 dB
```

The noise/SNR results remain explicitly tied to the high-resolution ideal quantization approximation.

**PASS.**

### SRC-05 — DC offset second moment

Verified:

```text
d                                  [0.5, 0.5]^T
R_y^(2)                            [[1.25,0.25],[0.25,1.25]]
eigenvalues                        {1.5,1}
```

**PASS.**

### SRC-06 — Inverse calibration noise amplification

For `H=diag(1,0.1)` and white unit noise:

```text
H^-1                               diag(1,10)
corrected noise covariance         diag(1,100)
condition number                   10
weak-channel variance gain         100
```

**PASS.**

### SRC-07 — Calibration-grid phase-gauge interpolation

Verified exact counterexample:

```text
pointwise endpoint projective equivalence   true
coherent midpoint                           [1,1]^T
independent pi-gauge midpoint               [0,0]^T
```

**PASS.**

### SRC-08 — Noncommuting operator order

Verified:

```text
C G = [[1,1],[0.5,2]]
G C = [[1,0.5],[1,2]]
C G - G C = [[0,0.5],[-0.5,0]]
```

**PASS.**

## 4. Coverage assessment

The evidence set directly exercises the following core ADR-003 contract families:

```text
position error
stable phase reference
rigid translation
relative gain/phase mismatch
common phase equivalence
cross-channel mutual coupling
covariance/eigenspace propagation
MUSIC mismatch leakage
physical delay vs sample-time sign
sample-rate offset
frequency-reference drift/coherence loss
ADC range and ideal quantization approximation
DC-offset second-moment effect
inverse calibration and noise amplification
calibration-grid gauge/interpolation
operator ordering/noncommutativity
```

## 5. Why some ADR-003 families do not receive a numeric GRP here

Gate E requires deterministic evidence for the core contracts, but not every future/deferred physical profile has a meaningful single canonical scalar reference at this stage.

The following remain primarily profile/boundary semantics and shall be exercised explicitly in Gate F and later implementation-specific validation:

- vector/polarimetric element response;
- embedded/full-wave measured-manifold provenance;
- I/Q imbalance under arbitrary improper source statistics;
- nonlinear compression/intermodulation;
- clipping;
- one-bit/coarse quantization;
- physical port/termination changes;
- out-of-calibration-domain behavior;
- near-field/wideband/TDM-MIMO compound profiles.

This is not an evidence gap in the initial Phase-1 profile because those capabilities remain explicitly implementation-deferred. When any such profile becomes authoritative, its activation rule requires dedicated deterministic evidence.

## 6. Evidence-type integrity — PASS

The evidence file correctly distinguishes:

```text
exact identity
exact deterministic linear algebra
exact continuous-window integral
bounded first-order approximation
ideal high-resolution ADC approximation
presentation-unit conversion
future numerical tolerance recommendation
```

No approximate result is promoted to an exact identity.

No future regression tolerance is presented as a physical acceptance threshold.

**Result: PASS.**

## 7. Reproducibility and regression-oracle readiness — PASS

Each canonical GRP now contains:

- declared inputs;
- sign/unit conventions;
- hand derivation;
- expected numerical results;
- scientific conclusion;
- recommended future deterministic software assertions.

The supplemental SRC references follow the same scientific contract and are sufficiently small to reproduce independently with paper, pencil, and a basic calculator.

**Result: PASS.**

## 8. Blocking findings

```text
Canonical GRP arithmetic contradiction:          NONE FOUND
ADR-001/ADR-002 sign mismatch:                   NONE FOUND
Exact/approximate evidence misclassification:    NONE FOUND
Reserved GRP numbering conflict:                 NONE FOUND
Missing deterministic evidence for Phase-1:      NONE FOUND
Regression-oracle ambiguity:                     NONE FOUND
```

## 9. Gate E decision

\[
\boxed{\text{Gate E — Hand-Calculated Reference Evidence: PASS}}
\]

The ADR-003 evidence set is sufficient for the currently bounded scientific contract and initial Phase-1 profile.

GRP-014 through GRP-017 are now formal ADR-003 Golden Reference Problems rather than exploration seeds.

`ADR-003-SRC-01` through `ADR-003-SRC-08` provide deterministic supplemental coverage without altering the canonical roadmap numbering.

ADR-003 remains **NOT ACCEPTED** because Gate F and final cross-gate reconciliation have not passed.

The next formal work item is:

\[
\boxed{\text{Gate F — Boundary and Failure Analysis}}
\]
