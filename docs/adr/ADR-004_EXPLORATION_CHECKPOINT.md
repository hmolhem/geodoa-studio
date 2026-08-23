# ADR-004 — Exploration Checkpoint

- **ADR:** ADR-004 — Validation, Reproducibility, and Scientific Evidence
- **Phase:** 0C — Scientific Foundations
- **Status:** GOVERNING DRAFT COMPLETE — PRE-GATE REVIEW PASS — GATES A-B PASS — GATE C NEXT — NOT ACCEPTED
- **Branch:** `docs/phase0c-scientific-conventions`
- **Depends on:** Accepted ADR-001, ADR-002, ADR-003
- **Roadmap:** `../PHASE0C_SCIENTIFIC_CONTRACTS_ROADMAP.md`
- **Started:** 2026-08-23

## 1. Primary Question

> Under what evidence may GeoDOA Studio call a model, algorithm, experiment, calibration result, numerical implementation, or hardware result verified, validated, reproducible, or better than another method?

ADR-004 shall define the scientific evidence contract used by all later GeoDOA studies. It shall not prescribe one universal benchmark or one universal pass/fail threshold.

## 2. Exploration Sequence

The working exploration sequence is:

```text
4.1   Verification vs Validation
4.2   Ground Truth and Provenance
4.3   Deterministic Reference Evidence
4.4   Random Variables and Trial Semantics
4.5   Seed / RNG / Common Random Numbers
4.6   Multi-Source Truth-to-Estimate Association
4.7   Bias / Variance / MSE / RMSE
4.8   Detection / Miss / False Alarm / Resolution
4.9   Probability of Resolution
4.10  Monte Carlo Adequacy and Convergence
4.11  Confidence Intervals / Metric Uncertainty
4.12  Fair Algorithm / Geometry Comparison
4.13  Failure-State Recording
4.14  Spectrum / Manifold / Covariance / Eigenspace / DOA Metrics
4.15  Floating-Point / Fixed-Point / FPGA Cross-Validation
4.16  Run Identity / Configuration Hash / Provenance
4.17  Publication Evidence and Reproducibility Package
4.18  Cross-ADR Compatibility with ADR-001/002/003
4.19  Initial Phase-1 Validation Profile
4.20  Cross-Section Reconciliation
```

The exploration organization is complete. The governing ADR-004 draft consolidates these candidate decisions into the reconciled `F1–F14` decision families.

## 3. Roadmap Coverage Requirements

ADR-004 must cover at least:

- ground-truth definition and provenance;
- verification versus physical validation;
- analytical reference validation;
- numerical cross-reference validation;
- external-tool validation;
- hardware/experimental validation;
- deterministic Golden Reference Problems;
- random-variable declaration;
- Monte Carlo trial semantics;
- root seed and deterministic child-stream policy;
- common random numbers for fair comparisons;
- trial-count adequacy and convergence diagnostics;
- bias;
- variance;
- MSE and RMSE;
- multi-source truth-to-estimate association;
- missed and false detections;
- resolution versus accuracy;
- probability of resolution;
- failure-state recording;
- spectrum-level diagnostics;
- manifold, covariance, eigenvalue, eigenspace, and DOA error metrics;
- uncertainty/confidence intervals for aggregate metrics;
- fair benchmark requirements;
- data, configuration, calibration, algorithm, software, Git, and seed provenance;
- scientific metrics versus computational/hardware metrics;
- floating-point, fixed-point, and FPGA cross-validation.

Explorations 4.1–4.20 collectively cover these roadmap requirements at candidate-contract level, and the governing draft has now been written and passed the dedicated pre-Gate consistency review.

## 4. Initial Golden Reference Reservation

The Phase 0C roadmap reserves:

```text
GRP-018 — Bias, Variance, MSE, and RMSE by hand
```

Additional ADR-004 deterministic evidence may use `ADR-004-SRC-*` identifiers so that canonical GRP numbering is not changed without an explicit roadmap decision.

GRP-018 remains exploration/reference content until formal Gate E evidence is created and passed.

## 5. Working Rules

1. Exploration is complete and the governing ADR-004 draft exists.
2. The dedicated pre-Gate consistency review passed.
3. Gate A — Physical Consistency passed.
4. Gate B — Mathematical Consistency passed.
5. Gate C — Dimensional / Unit Consistency is now the next acceptance step; Gates D–F remain not started.
6. Exploration calculations are not formal Golden Reference PASS evidence until Gate E.
7. Verification, validation, calibration, benchmarking, and reproducibility shall remain distinct concepts.
8. Metric computation and acceptance policy shall remain distinct.
9. Failed/missed/unresolved trials shall not be silently deleted from benchmark evidence.
10. Randomness and seed provenance shall be explicit enough to reconstruct a trial.
11. Comparative claims shall preserve fairness/provenance rather than rely on uncontrolled independent realizations.
12. A numerical match to a software baseline does not by itself establish physical validation.
13. Hardware acceleration shall be assessed against an accepted scientific reference, not only against another hardware implementation.
14. ADR-004 shall remain downstream of ADR-001/002/003 authority for geometry/phase, signal/covariance, and sensor/calibration semantics.
15. Compatibility status, execution/failure status, and metric eligibility shall remain distinct.
16. `XX^H/L` in the VP-001 baseline shall be called the uncentered sample second moment, not centered sample covariance.
17. Divisor-`N` empirical variance used in exact finite-sample MSE decomposition shall remain distinct from divisor-`N-1` sample variance used for statistical variance estimation.
18. VP-001 confirmatory Monte Carlo studies should prefer predeclared fixed-`N` execution with achieved uncertainty/adequacy reporting; no universal numeric `N` is accepted.
19. Wilson score interval is the VP-001 default for ordinary IID fixed-`N` Bernoulli probability reporting, not a universal ADR-004 interval method.
20. Source count `K`, source-covariance rank, observed subspace rank, estimator model order, and estimated-output cardinality `K_hat` shall remain distinct.
21. VP-001 baseline end-to-end `P_D` and `P_res` metric universes and numerical-failure mappings are explicit in the governing draft.
22. External-tool/cross-tool numerical agreement is reference/verification evidence unless a separate physical-validation contract is satisfied.
23. Real-scalar `e^2` bias/MSE formulas are scoped to real localization metrics; future complex-valued error metrics require an explicit complex squared-error definition.
24. Normalized manifold correlation/projective metrics require nonzero vectors; zero/invalid manifold cases require typed ineligibility or a different declared metric.

## 6. Current Status

```text
4.1   Verification vs Validation                      COMPLETE
4.2   Ground Truth and Provenance                    COMPLETE
4.3   Deterministic Reference Evidence               COMPLETE
4.4   Random Variables and Trial Semantics           COMPLETE
4.5   Seed / RNG / Common Random Numbers             COMPLETE
4.6   Multi-Source Truth-to-Estimate Association     COMPLETE
4.7   Bias / Variance / MSE / RMSE                   COMPLETE
4.8   Detection / Miss / False Alarm / Resolution    COMPLETE
4.9   Probability of Resolution                      COMPLETE
4.10  Monte Carlo Adequacy and Convergence           COMPLETE
4.11  Confidence Intervals / Metric Uncertainty      COMPLETE
4.12  Fair Algorithm / Geometry Comparison           COMPLETE
4.13  Failure-State Recording                        COMPLETE
4.14  Multi-Level Scientific Error Metrics           COMPLETE
4.15  Float / Fixed / FPGA Cross-Validation          COMPLETE
4.16  Run Identity / Configuration / Provenance      COMPLETE
4.17  Publication / Reproducibility Package          COMPLETE
4.18  Cross-ADR Compatibility                        COMPLETE
4.19  Initial Phase-1 Validation Profile             COMPLETE
4.20  Cross-Section Reconciliation                   COMPLETE

Governing ADR-004 draft                               COMPLETE — DRAFT ONLY
Pre-Gate consistency review                           PASS
Gate A — Physical Consistency                         PASS
Gate B — Mathematical Consistency                     PASS
Gate C — Dimensional / Unit Consistency               NEXT
Gate D — Software Semantic Consistency                NOT STARTED
Gate E — Hand Reference Evidence                      NOT STARTED
Gate F — Boundary / Failure Analysis                  NOT STARTED
ADR-004 acceptance                                    NOT ACCEPTED
```

## 7. Pre-Gate Review Record

The dedicated review is:

```text
ADR-004_PRE_GATE_CONSISTENCY_REVIEW.md
```

It identified and resolved four pre-Gate omissions before PASS:

```text
PG-004-01  explicit P_D/P_res metric universes/denominators
PG-004-02  explicit population variance semantics
PG-004-03  K / rank / model-order / K_hat distinctions
PG-004-04  explicit independent numerical / external-tool evidence role
```

The corrections are included in governing-draft commit:

```text
4675f312214ebc0eaaa64a2041bb582931cf2332
```

The reviewed governing-draft content SHA is:

```text
8cca2e3ac514cd031bee1d8c9e4c0347694ecb53
```

## 8. Gate A Record

The Gate A physical-consistency audit is:

```text
ADR-004_GATE_A_AUDIT.md
```

Gate A passed without requiring a post-review governing-draft correction.

Gate A confirmed, among other items:

```text
model assumptions remain distinct from physical truth
verification remains distinct from physical validation
calibration remains distinct from validation
VP-001 remains an ideal bounded profile
CST/external numerical agreement remains model/reference evidence
synthetic FPGA board replay remains implementation/integration evidence
physical source count remains distinct from rank/model-order/output cardinality
ADC quantization remains distinct from FPGA fixed-point arithmetic
physical delay remains distinct from implementation latency
```

Gate A commit:

```text
9b3f261858b435ce493189c1ee9802b68c17d78f
```

## 9. Gate B Record

The Gate B mathematical-consistency audit is:

```text
ADR-004_GATE_B_AUDIT.md
```

Gate B passed without requiring a governing-draft correction.

Gate B verified, among other items:

```text
bias / variance / MSE / RMSE identities
exact finite-sample MSE decomposition
v_N versus s^2 roles
GRP-018 arithmetic consistency at audit level
multi-source assignment / unequal-cardinality handling
P_D / P_res numerator-denominator semantics
uncentered XX^H/L Hermitian / PSD / rank properties
source count versus rank/model order
rho / alpha / d_proj bounds and projective invariance
rank-one projector and subspace-basis invariance
eigenvector nonuniqueness / eigengap interpretation
CRN paired-effect mathematics
finite-precision equivalence semantics
metric versus threshold separation
```

Gate B also carried explicit mathematical domain conditions forward for Gate F, including nonzero-vector requirements for normalized manifold metrics and real-scalar scope for the current `e^2` localization formulas.

Gate B commit:

```text
7b6fb7e68816ca51c336b526a72e656d61c16dac
```

## 10. Reconciled Decision Families in the Governing ADR

The governing draft consolidates exploration decisions into:

```text
F1   Evidence-role separation
F2   Typed truth/reference authority
F3   Deterministic verification ladder
F4   Stochastic experiment identity / RNG / CRN
F5   Association / detection / resolution semantics
F6   Metric semantics
F7   Monte Carlo adequacy / uncertainty
F8   Fair comparison
F9   Typed non-success evidence
F10  Multi-level scientific diagnosis
F11  Float/fixed/HLS/RTL/FPGA evidence ladder
F12  Provenance / configuration / immutability
F13  Publication evidence / reproducibility package
F14  VP-001 initial validation profile
```

Detailed exploration files remain supporting rationale and traceability evidence.

## 11. Immediate Work Item

Begin:

```text
ADR-004 Gate C — Dimensional and Unit Consistency Audit
```

Gate C shall verify that every physical or metric quantity used by ADR-004 has explicit units or is explicitly dimensionless; that squared-error units, covariance/spectrum/manifold metrics, angle versus direction-cosine coordinates, probability quantities, timing/performance units, fixed-point scaling, and canonical configuration unit normalization are unambiguous and compatible with ADR-001/002/003.

Gate C PASS does not imply Gates D–F PASS and does not accept ADR-004.
