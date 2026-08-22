# ADR-002 — Gate F Audit

- **ADR:** `ADR-002-wave-propagation-signal-measurement-model.md`
- **Phase:** 0C — Scientific Foundations
- **Gate:** F — Boundary and Failure Analysis
- **Status:** PASS
- **Primary evidence:** `ADR-002_BOUNDARY_FAILURE_ANALYSIS.md`

## 1. Audit Question

Does ADR-002 define boundary behavior strongly enough that GeoDOA can distinguish invalid inputs, physically valid scenarios outside PM-001, measurement/statistical incompatibility, structural identifiability limitations, algorithm applicability failures, and interpretation warnings without silent model switching or semantic loss?

## 2. Evidence Reviewed

Gate F reviewed the complete ADR-002 boundary taxonomy recorded in `ADR-002_BOUNDARY_FAILURE_ANALYSIS.md`, including:

- wave/frequency/medium validity;
- path singularities and plane-wave compatibility;
- narrowband/wideband boundaries;
- motion, Doppler, migration, and time-scale boundaries;
- active/passive and FMCW boundaries;
- scientific-frequency/FFT and dechirp-sign provenance;
- general bistatic versus common-look virtual MIMO behavior;
- raw measurement-axis and snapshot construction;
- covariance, source/noise, coherence, SNR, and unit/scaling boundaries;
- spatial identifiability and classical MUSIC applicability;
- profile identity, silent model switching, and numerical repair provenance.

## 3. Response Taxonomy — PASS

ADR-002 uses the same four response classes already accepted by ADR-001:

- **REJECT**;
- **INCOMPATIBLE / REQUIRE OTHER MODEL**;
- **DIAGNOSTIC / WARN**;
- **VALID**.

The taxonomy is internally consistent across ADR-001 and ADR-002.

## 4. Material Boundary Findings — PASS

The following high-risk failure modes are explicitly resolved:

1. **Far-field failure does not invalidate the scene.** It requires a spherical/near-field model rather than silent approximation.
2. **Narrowband failure does not invalidate the waveform/scene.** It requires a wideband model.
3. **Nonzero Doppler does not automatically invalidate a spatially quasi-static manifold.**
4. **Moving active-target `2R`/common-epoch formulas are bounded as stop-and-hop/quasi-static approximations.**
5. **FMCW signed beat frequency requires mixer convention, chirp-slope sign, and scientific/FFT-coordinate provenance.**
6. **`fftshift` is not a scientific frequency-sign transformation.**
7. **General bistatic MIMO does not permit unconditional `r_v = r_Tx+r_Rx`; common-look compatibility is required.**
8. **Physical Tx/Rx pair provenance cannot be discarded even when derived virtual coordinates coincide.**
9. **Raw measurement shape cannot substitute for axis semantics or snapshot provenance.**
10. **`L=1` known-zero second moment and estimated-mean covariance are different operations.**
11. **Hermitian/PSD repair is not validation and cannot be silent.**
12. **Coherent sources and colored noise are valid statistical cases even when a classical algorithm becomes incompatible.**
13. **Physical source count, observable signal rank, estimated order, and peak count are not silently equated.**
14. **Aliasing/projection ambiguity limits uniqueness claims without invalidating the underlying manifold computation.**
15. **A computed compatibility metric does not imply PASS/FAIL if no acceptance threshold/policy has been declared.**

## 5. Cross-Gate Check

### 5.1 Gate A — Physical consistency

Boundary rules preserve the distinction between physically meaningful scenarios and PM-001 limitations. Near-field, wideband, dispersive, multipath, moving-active, colored-noise, and coherent-source cases are not incorrectly labeled impossible.

**Cross-check: PASS.**

### 5.2 Gate B — Mathematical consistency

Boundary rules respect the mathematical domains established earlier: nonzero denominator for relative response, `L>=2` for estimated-mean covariance, `r_obs<N` for a nonempty classical MUSIC noise subspace, and common-look conditions for virtual-sum MIMO geometry.

**Cross-check: PASS.**

### 5.3 Gate C — Dimensional/unit consistency

Unit ambiguity is itself treated as a semantic/domain failure. No boundary condition reinterprets Hz/rad/s, amplitude/power dB, physical/normalized amplitude, or index/coordinate values without explicit conversion.

**Cross-check: PASS.**

### 5.4 Gate D — Software semantic consistency

The boundary taxonomy maps naturally to typed compatibility/diagnostic results and prohibits silent model promotion/degradation, axis guessing, channel identity loss, physical-manifold normalization, or numerical repair.

**Cross-check: PASS.**

### 5.5 Gate E — Golden Reference consistency

GRP-007 through GRP-013 and ADR-002-SRC-01 through SRC-05 exercise the highest-risk sign, range, rank, covariance, MIMO, medium, and snapshot boundaries. No expected value conflicts with the Gate F taxonomy.

**Cross-check: PASS.**

## 6. Gate F Decision

No unresolved boundary/failure contradiction remains within the declared ADR-002 scope.

```text
Gate F status: PASS
Physical invalidity vs model incompatibility: separated
Model incompatibility vs algorithm incompatibility: separated
Warnings vs uniqueness claims: separated
Silent model switching: prohibited
Silent numerical repair: prohibited
Missing policy -> invented PASS/FAIL: prohibited
```

ADR-002 is ready for final cross-gate acceptance reconciliation.
