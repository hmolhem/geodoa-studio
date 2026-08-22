# ADR-002 — Final Acceptance Record

- **ADR:** `ADR-002-wave-propagation-signal-measurement-model.md`
- **Phase:** 0C — Scientific Foundations
- **Final status:** ACCEPTED
- **Acceptance date:** 2026-08-22
- **Purpose:** Final reconciliation of ADR-002 scientific acceptance evidence after Gates A–F.

## 1. Acceptance Decision

ADR-002 — Wave, Propagation, Signal, and Measurement Model is **ACCEPTED** as the authoritative GeoDOA scientific contract for its declared scope.

All six Phase 0C acceptance gates have passed:

| Gate | Requirement | Final Status | Primary Evidence |
|---|---|---|---|
| A | Physical consistency | PASS | `ADR-002_ACCEPTANCE_AUDIT.md` |
| B | Mathematical consistency | PASS | `ADR-002_ACCEPTANCE_AUDIT.md` |
| C | Dimensional and unit consistency | PASS | `ADR-002_ACCEPTANCE_AUDIT.md` |
| D | Software semantic consistency | PASS | `ADR-002_ACCEPTANCE_AUDIT.md` |
| E | Hand-calculated reference evidence | PASS | `../science/golden_reference/ADR-002_GOLDEN_REFERENCE_PROBLEMS.md` |
| F | Boundary and failure analysis | PASS | `ADR-002_BOUNDARY_FAILURE_ANALYSIS.md`, `ADR-002_GATE_F_AUDIT.md` |

The progressive acceptance audit remains preserved as the detailed record of Gate A–E findings and Gate F linkage. This final record controls the final acceptance status.

## 2. Exploration-to-Contract Reconciliation

ADR-002 was not written directly from a textbook shorthand. Its governing content was developed through the following exploration sequence before formalization:

```text
2.1   Waveform -> Delay -> Complex Baseband
2.2   Exact Spherical -> Far-Field Plane Wave
2.3   Narrowband vs Wideband
2.4   Source / Snapshot / Noise / Covariance
2.5   Measurement Axes / Passive / Active / FMCW / MIMO
2.6   Motion / Doppler / Stationarity / Migration / CPI
2.7   Medium / Attenuation / Phase & Group Velocity / Dispersion
2.8   Amplitude / Path Loss / SNR / Dynamic Range
2.9   Coherence / Multipath / Identifiability / Model Order
2.10  Compatibility Matrix / PM-001
2.11  Cross-Consistency Audit
```

All material refinements discovered during this sequence and Gates A–D were incorporated into the governing ADR rather than left only in exploratory discussion.

## 3. Material Cross-Consistency Corrections

The acceptance process found and resolved several high-value issues before implementation.

### 3.1 Scientific frequency versus software FFT coordinate

GeoDOA's scientific positive frequency uses `exp(-j2 pi f t)`, while the standard forward NumPy/MATLAB DFT kernel uses a negative exponent in the analysis transform. Consequently a GeoDOA positive-frequency complex exponential appears on the negative standard FFT coordinate.

For the accepted FMCW dechirp convention

```math
y=s_{\mathrm{rx}}s_{\mathrm{tx}}^*,
```

an up-chirp/static delay gives

```math
f_{b,\mathrm{sci}}=-\mu\tau,
```

while the standard forward FFT coordinate for the resulting exponential appears at `+mu tau`.

This distinction is normative and provenance-bearing.

### 3.2 General bistatic MIMO versus virtual-sum specialization

The general first-order bistatic path is

```math
\Delta\mathcal P_{ij}
\approx
-\Delta\mathbf r_{\mathrm{Tx},i}^T\hat{\mathbf u}_{\mathrm{Tx}}
-\Delta\mathbf r_{\mathrm{Rx},j}^T\hat{\mathbf u}_{\mathrm{Rx}}.
```

The common virtual-sum relation

```math
\Delta\mathbf r_{v,ij}
=
\Delta\mathbf r_{\mathrm{Tx},i}
+
\Delta\mathbf r_{\mathrm{Rx},j}
```

is accepted only under a common-look/colocated far-field specialization. GeoDOA shall not manufacture a virtual coordinate for arbitrary bistatic geometry.

### 3.3 Centered covariance unbiasedness

The conventional estimator

```math
\hat{\mathbf R}_c
=
\frac1{L-1}\mathbf X_c\mathbf X_c^H
```

is mathematically defined for `L >= 2`, but the label `unbiased` requires the appropriate statistical assumptions. Temporal correlation is not erased by choosing denominator `L-1`.

### 3.4 Reference-invariant plane-wave compatibility

A declared-reference path residual remains useful, but common phase is not spatial distortion. ADR-002 therefore also records a pairwise reference-invariant plane-wave compatibility quantity based on exact versus plane-wave pair differences.

### 3.5 Exact versus specialized aperture delay

The canonical aperture delay is obtained from actual path/group delays. `D_u/v` is a far-field homogeneous nondispersive specialization, not a universal near-field/wideband formula.

## 4. Cross-Gate Consistency Check

### 4.1 Physical consistency

PM-001 remains intentionally bounded rather than physically universal. Near-field, wideband, dispersive, lossy, multipath, moving-active, coherent-source, and colored-noise scenarios remain meaningful but require appropriate profiles/models/algorithms.

**Cross-check: PASS.**

### 4.2 Mathematical consistency

The accepted temporal sign, delay theorem, outgoing propagation phase, steering sign, Doppler sign, FMCW sign, MIMO path equations, covariance/rank equations, and sample-rank ceiling are mutually consistent.

**Cross-check: PASS.**

### 4.3 Dimensional consistency

Canonical SI-compatible quantities and semantic angular/logarithmic units remain consistent through propagation, FMCW, covariance, SNR, and MIMO equations. Scientific-frequency and FFT-coordinate signs are semantic mappings, not unit substitutions.

**Cross-check: PASS.**

### 4.4 Software semantic consistency

The final contract maps cleanly to the domain-centric architecture using compositional physical profiles, explicit measurement axes/snapshot construction, preserved channel/MIMO provenance, separate physical/statistical/algorithm layers, and pure numerical kernels after canonicalization.

**Cross-check: PASS.**

### 4.5 Golden Reference consistency

GRP-007 through GRP-013 match the existing Phase 0C catalog. Additional ADR-002 evidence is preserved as `ADR-002-SRC-01` through `ADR-002-SRC-05` to avoid renumbering the roadmap's existing GRP-014 through GRP-018 assignments.

**Cross-check: PASS.**

### 4.6 Boundary consistency

The Gate F taxonomy uses the same four response classes as ADR-001 and consistently distinguishes invalid input, model incompatibility, diagnostic ambiguity, and valid operation.

**Cross-check: PASS.**

## 5. Accepted PM-001 Profile

ADR-002 accepts the initial physical/measurement reference profile:

```text
PM-001 — Reference Far-Field Narrowband Receive-Array Profile

one-way receive-equivalent sensing
single direct propagation path
homogeneous medium
isotropic medium
nondispersive medium
lossless medium
finite positive constant propagation speed
plane-wave-compatible scene/geometry
array-narrowband-compatible signal/path
quasi-static spatial manifold over the declared window
ideal identical scalar receive channels
simultaneous-equivalent channel observations
relative geometry-only unit-magnitude manifold
normalized complex-baseband source/arrival coefficients
```

PM-001 is distinct from a statistical reference configuration and from algorithm-specific applicability requirements.

## 6. Final Accepted Scientific Decisions

ADR-002 now locks the following decisions:

- `exp(-j omega t)` is the scientific temporal phasor convention inherited from ADR-001;
- outgoing scalar propagation uses `exp(+j k R)`;
- exact geometric path and reference-relative delay precede far-field/narrowband approximation;
- ADR-001 steering is recovered as `exp[-j k (r_n-r_ref)^T u_hat]`;
- far-field and narrowband are independent compatibility axes;
- plane-wave compatibility is scene/direction/frequency/accuracy dependent;
- Fraunhofer distance is diagnostic rather than a universal binary boundary;
- aperture delay is generally derived from physical/group delays; `D_u/v` is a specialization;
- fractional bandwidth alone does not establish array narrowband compatibility;
- phase velocity, group velocity, attenuation, geometric spreading, and dispersion are distinct;
- absolute path response, relative response, and geometry-only manifold are distinct;
- PM-001 uses a homogeneous isotropic nondispersive lossless constant-speed medium;
- nonzero Doppler does not necessarily imply spatial-manifold nonstationarity;
- CPI, covariance window, and tracking interval are distinct;
- active sensing uses explicit propagation legs; generic factor-of-two propagation logic is prohibited;
- scientific signed FMCW frequency, mixer convention, chirp slope, FFT coordinate, and index ordering are distinct;
- raw multidimensional measurements and spatial snapshot matrices are distinct representations connected by explicit provenance-preserving transformations;
- a spatial snapshot is a simultaneous-equivalent receiver observation, not automatically a raw ADC sample;
- general bistatic MIMO preserves independent Tx/Rx look directions and physical pair provenance;
- virtual-sum geometry is a common-look/colocated far-field derived specialization;
- physical source/target, propagation path, and spatial arrival are distinct;
- covariance is distinguished from uncentered second moment;
- source count, arrival count, source covariance rank, observable signal rank, estimated model order, and detected peak count are distinct;
- coherent arrivals can reduce covariance rank without removing physical arrivals;
- centered sample covariance has rank ceiling `min(N,L-1)`;
- standard centered `1/(L-1)` unbiasedness requires appropriate statistical assumptions;
- white circular complex Gaussian reference noise has complex variance `sigma^2` and I/Q variances `sigma^2/2`;
- SNR is not a context-free dB scalar and must retain its measurement/normalization definition;
- physical/statistical/algorithm configurations remain separate layers;
- compatibility metrics and acceptance policies remain separate;
- no model/axis/unit/sign/normalization/repair operation may silently change scientific meaning.

## 7. Accepted Boundary Taxonomy

ADR-002 adopts the normative four-class taxonomy:

- **REJECT** — scientifically invalid/undefined input or operation;
- **INCOMPATIBLE / REQUIRE OTHER MODEL** — meaningful scenario outside the selected profile/model/algorithm;
- **DIAGNOSTIC / WARN** — valid computation with ambiguity, aliasing, conditioning, approximation sensitivity, or interpretation limits;
- **VALID** — operation lies within the declared contract.

No implementation may silently turn an `INCOMPATIBLE` case into PM-001 by automatic model switching or turn a diagnostic ambiguity into a unique physical claim.

## 8. Evidence Set

The accepted ADR-002 evidence set consists of:

```text
docs/adr/ADR-002-wave-propagation-signal-measurement-model.md
docs/adr/ADR-002_ACCEPTANCE_AUDIT.md
docs/adr/ADR-002_BOUNDARY_FAILURE_ANALYSIS.md
docs/adr/ADR-002_GATE_F_AUDIT.md
docs/adr/ADR-002_FINAL_ACCEPTANCE_RECORD.md
docs/science/golden_reference/ADR-002_GOLDEN_REFERENCE_PROBLEMS.md
```

The structure is intentionally analogous to ADR-001:

```text
Governing scientific decision
        -> progressive acceptance evidence
        -> deterministic hand-calculated evidence
        -> explicit boundary/failure evidence
        -> Gate F reconciliation
        -> final acceptance record
```

## 9. What Acceptance Does Not Mean

ADR-002 acceptance does not mean that Phase 1 propagation, FMCW, covariance, MIMO, or MUSIC implementations already exist or have passed software verification.

The accepted Golden Reference expected values become future test oracles. Implementations governed by ADR-002 must reproduce the accepted numerical/semantic behavior before they are considered verified.

Acceptance also does not mean that GeoDOA Phase 1 must immediately implement every phenomenon described by ADR-002. PM-001 remains deliberately narrow. Near-field, wideband, dispersive, moving-active, multipath, colored-noise, and other advanced capabilities require explicit future providers/profiles and their own verification evidence.

ADR-003 and ADR-004 remain independent scientific contracts requiring their own Gates A–F.

## 10. Closure Statement

ADR-002 has no unresolved scientific acceptance finding within its declared scope.

```text
ADR-002 STATUS: ACCEPTED
Gate A: PASS
Gate B: PASS
Gate C: PASS
Gate D: PASS
Gate E: PASS
Gate F: PASS
Cross-ADR-001 consistency: PASS
PM-001: ACCEPTED initial physical/measurement profile
```
