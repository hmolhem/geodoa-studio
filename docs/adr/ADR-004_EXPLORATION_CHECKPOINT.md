# ADR-004 — Exploration Checkpoint

- **ADR:** ADR-004 — Validation, Reproducibility, and Scientific Evidence
- **Phase:** 0C — Scientific Foundations
- **Status:** GOVERNING DRAFT COMPLETE — PRE-GATE REVIEW PASS — GATE A NEXT — NOT ACCEPTED
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
3. Gate A is now authorized as the next acceptance step; Gates B–F remain not started.
4. Exploration calculations are not formal Golden Reference PASS evidence until Gate E.
5. Verification, validation, calibration, benchmarking, and reproducibility shall remain distinct concepts.
6. Metric computation and acceptance policy shall remain distinct.
7. Failed/missed/unresolved trials shall not be silently deleted from benchmark evidence.
8. Randomness and seed provenance shall be explicit enough to reconstruct a trial.
9. Comparative claims shall preserve fairness/provenance rather than rely on uncontrolled independent realizations.
10. A numerical match to a software baseline does not by itself establish physical validation.
11. Hardware acceleration shall be assessed against an accepted scientific reference, not only against another hardware implementation.
12. ADR-004 shall remain downstream of ADR-001/002/003 authority for geometry/phase, signal/covariance, and sensor/calibration semantics.
13. Compatibility status, execution/failure status, and metric eligibility shall remain distinct.
14. `XX^H/L` in the VP-001 baseline shall be called the uncentered sample second moment, not centered sample covariance.
15. Divisor-`N` empirical variance used in exact finite-sample MSE decomposition shall remain distinct from divisor-`N-1` sample variance used for statistical variance estimation.
16. VP-001 confirmatory Monte Carlo studies should prefer predeclared fixed-`N` execution with achieved uncertainty/adequacy reporting; no universal numeric `N` is accepted.
17. Wilson score interval is the VP-001 default for ordinary IID fixed-`N` Bernoulli probability reporting, not a universal ADR-004 interval method.
18. Source count `K`, source-covariance rank, observed subspace rank, estimator model order, and estimated-output cardinality `K_hat` shall remain distinct.
19. VP-001 baseline end-to-end `P_D` and `P_res` metric universes and numerical-failure mappings are explicit in the governing draft.
20. External-tool/cross-tool numerical agreement is reference/verification evidence unless a separate physical-validation contract is satisfied.

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
Gate A                                                AUTHORIZED — NEXT
Gates B-F                                             NOT STARTED
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

## 8. Reconciled Decision Families in the Governing ADR

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

## 9. Immediate Work Item

Begin:

```text
ADR-004 Gate A — Physical Consistency Audit
```

Gate A shall verify that the governing ADR-004 evidence semantics and VP-001 profile correctly distinguish model assumptions from physical truth, physical validation from computational verification, calibration from validation, synthetic hardware replay from physical sensor validation, and inherited ADR-001/002/003 physical authority.

Gate A PASS does not imply Gates B–F PASS and does not accept ADR-004.
