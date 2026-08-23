# ADR-003 — Gate F Boundary and Failure Audit

- **Governing ADR:** `ADR-003-sensor-imperfections-mutual-coupling-calibration.md`
- **Boundary evidence:** `ADR-003_BOUNDARY_FAILURE_ANALYSIS.md`
- **Golden Reference evidence:** `../science/golden_reference/ADR-003_GOLDEN_REFERENCE_PROBLEMS.md`
- **Phase:** 0C — Scientific Foundations
- **Gate:** F — Boundary and Failure Analysis
- **Status:** PASS
- **Prior gates:** A PASS, B PASS, C PASS, D PASS, E PASS
- **ADR status:** NOT ACCEPTED — final cross-gate reconciliation pending

## 1. Audit question

Does ADR-003 explicitly identify malformed inputs, physical scenarios outside selected profiles, calibration-domain and provenance failures, structural non-identifiability, conditioning limits, receiver/ADC invalidity, covariance/eigenspace breakdowns, estimator incompatibility, and interpretation limits without silently coercing them into apparently valid DOA results?

## 2. Response taxonomy — PASS

ADR-003 adopts the same four-class top-level response taxonomy already used by accepted ADR-002:

```text
REJECT
INCOMPATIBLE / REQUIRE OTHER MODEL
DIAGNOSTIC / WARN
VALID
```

In addition, `UNRESOLVED` is preserved as a scientific knowledge state for compatibility/identifiability/calibration questions and is never silently promoted to compatible/valid.

This is consistent with ADR-003 Exploration 3.13 and the governing no-silent-coercion contract.

**Result: PASS.**

## 3. Failure-layer ordering — PASS

The boundary artifact diagnoses in this order:

```text
input/domain validity
 -> units/reference planes/channel identity
 -> sensor-profile compatibility
 -> timing/sampling
 -> receiver/ADC operating region
 -> calibration domain/provenance
 -> identifiability/conditioning
 -> covariance/statistics
 -> eigenspace/model order
 -> estimator applicability
 -> performance/peak interpretation
```

This prevents a downstream estimator symptom from masking an upstream sensor-model failure.

**Result: PASS.**

## 4. Coverage reconciliation — PASS

The boundary artifact contains 140 explicit cases covering all major ADR-003 contract families:

- geometry and position error;
- electronic gain/phase;
- element/orientation/polarization;
- mutual coupling/loading/network semantics;
- typed operator graph/reference planes;
- channel delay, skew, SRO, CFO, jitter and digital latency;
- receiver noise and stage ordering;
- ADC, quantization, clipping and dynamic range;
- DC offset, I/Q imbalance and nonlinearity;
- calibration provenance/domain;
- calibration identifiability, inversion and regularization;
- direct measured/CST/full-wave manifolds;
- error metrics, normalization and gauge;
- covariance/eigenspace perturbation;
- MUSIC/estimator compatibility;
- digital masks, physical port state and MIMO provenance;
- Phase-1 ideal-profile boundaries;
- workflow/provenance/no-silent-coercion behavior.

No governing ADR-003 contract family is left without boundary semantics.

**Result: PASS.**

## 5. Gate A cross-check — PASS

The Gate-A physical-reference correction remains preserved:

- fixed nominal phase reference and moved-reference specialization are distinct;
- rigid translation remains common phase, not pairwise distortion;
- physical delay and later sampling retain opposite phase-sign semantics;
- coupling/network and calibration causal ordering remain physically typed.

Boundary cases F-005, F-006, F-021, F-028, F-034, and related cases explicitly protect these physical distinctions.

**Result: PASS.**

## 6. Gate B cross-check — PASS

Gate-F cases correctly mark mathematical boundaries rather than converting invalid formulas into numbers:

- singular inverse requests are rejected;
- zero-norm projective metrics are undefined/rejected;
- whitening requires positive-definite noise covariance for the standard inverse-square-root profile;
- zero eigengap does not permit division by a robustness gap;
- large mismatch does not inherit first-order perturbation validity;
- local MUSIC peak-shift approximations require a valid isolated/nondegenerate local structure.

**Result: PASS.**

## 7. Gate C cross-check — PASS

Boundary cases preserve dimensional/unit contracts:

- no silent meter/wavelength, Hz/rad/s, seconds/samples, radian/degree, volts/code or dB/linear inference;
- operator composition requires unit/reference-plane compatibility;
- ADC full-scale/bit-depth validity is explicit;
- Tikhonov regularization requires `[lambda I]=[H^H H]` or explicit nondimensionalization/scaling.

No dimensional ambiguity is converted into an apparently valid numerical result.

**Result: PASS.**

## 8. Gate D cross-check — PASS

Gate-F semantics reinforce software-domain separation:

- nominal/physical/measured/EM/calibrated response identities cannot collapse silently;
- stable channel identity cannot be replaced by sorted row order;
- digital selection and physical port state remain distinct;
- timing-error mechanisms cannot collapse into one ambiguous scalar;
- ADC acquisition quantization remains distinct from FPGA arithmetic quantization;
- compatibility remains multi-axis rather than a single Boolean;
- generic `realistic_sensor=True` is explicitly rejected as an authoritative scientific profile.

**Result: PASS.**

## 9. Gate E cross-check — PASS

The Golden Reference evidence exercises representative valid/interpretable cases for:

- position error and rigid translation;
- gain/phase mismatch and common-phase covariance invariance;
- mutual coupling;
- covariance/eigenspace/MUSIC leakage;
- delay versus sampling sign;
- SRO and CFO behavior;
- ADC quantization approximation;
- DC offset;
- inverse-calibration noise amplification;
- calibration-grid phase gauge;
- operator noncommutativity.

Gate F supplies the complementary invalid/out-of-domain cases, including clipping, one-bit/coarse quantization, response nulls, singular calibration, measured/CST provenance failures, and eigengap collapse.

The evidence and failure analysis are complementary rather than contradictory.

**Result: PASS.**

## 10. Phase-1 boundary — PASS

The initial Phase-1 sensor profile remains deliberately ideal:

```text
nominal geometry = physical geometry
ideal scalar identical elements
no coupling
unity differential electronics
coherent common timing/reference
linear no-overload receiver
unquantized floating acquisition
identity/not-applied calibration state
proper-complex white equal-variance additive noise
```

Any requested nonideal effect is not silently ignored. It requires a later named/versioned validated profile.

This preserves the roadmap rule that scientific semantics may be defined before implementation while the first authoritative implementation remains bounded.

**Result: PASS.**

## 11. Blocking-findings summary

```text
Unclassified material boundary family:                NONE FOUND
Malformed input silently accepted:                    NONE FOUND
Meaningful physical scenario incorrectly rejected:   NONE FOUND
Calibration-domain failure silently accepted:         NONE FOUND
Non-identifiable parameter promoted to unique truth: NONE FOUND
Singular/undefined mathematical operation coerced:   NONE FOUND
Estimator failure hiding upstream model failure:      NONE FOUND
Phase-1 nonideal effect silently ignored:             NONE FOUND
Unknown compatibility silently promoted:             NONE FOUND
```

## 12. Gate F decision

\[
\boxed{\text{Gate F — Boundary and Failure Analysis: PASS}}
\]

ADR-003 has now passed Gates A through F.

However, **ADR-003 is still NOT ACCEPTED**. Acceptance requires:

1. final cross-gate reconciliation across the governing ADR and Gates A–F;
2. incorporation/reconciliation of any gate refinements that belong in the governing contract, including the Gate-C `lambda` unit/scaling rule and current status metadata;
3. verification that Golden Reference and boundary artifacts match the final governing wording;
4. creation of the final ADR-003 acceptance record;
5. only then changing ADR-003 status to `Accepted`.

The immediate next formal work item is:

\[
\boxed{\text{ADR-003 Final Cross-Gate Reconciliation}}
\]
