# ADR-004 — Exploration Checkpoint

- **ADR:** ADR-004 — Validation, Reproducibility, and Scientific Evidence
- **Phase:** 0C — Scientific Foundations
- **Status:** GOVERNING DRAFT COMPLETE — PRE-GATE REVIEW NEXT — NOT ACCEPTED
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

The exploration organization is complete. The governing ADR-004 draft now consolidates these candidate decisions into the reconciled `F1–F14` decision families.

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

Explorations 4.1–4.20 collectively cover these roadmap requirements at candidate-contract level, and the governing draft has now been written from the reconciled decision families.

## 4. Initial Golden Reference Reservation

The Phase 0C roadmap reserves:

```text
GRP-018 — Bias, Variance, MSE, and RMSE by hand
```

Additional ADR-004 deterministic evidence may use `ADR-004-SRC-*` identifiers so that canonical GRP numbering is not changed without an explicit roadmap decision.

GRP-018 remains exploration/reference content until formal Gate E evidence is created and passed.

## 5. Working Rules

1. Exploration is complete and the governing ADR-004 draft now exists.
2. No acceptance Gate A before the dedicated pre-Gate consistency review passes.
3. Exploration calculations are not formal Golden Reference PASS evidence until Gate E.
4. Verification, validation, calibration, benchmarking, and reproducibility shall remain distinct concepts.
5. Metric computation and acceptance policy shall remain distinct.
6. Failed/missed/unresolved trials shall not be silently deleted from benchmark evidence.
7. Randomness and seed provenance shall be explicit enough to reconstruct a trial.
8. Comparative claims shall preserve fairness/provenance rather than rely on uncontrolled independent realizations.
9. A numerical match to a software baseline does not by itself establish physical validation.
10. Hardware acceleration shall be assessed against an accepted scientific reference, not only against another hardware implementation.
11. ADR-004 shall remain downstream of ADR-001/002/003 authority for geometry/phase, signal/covariance, and sensor/calibration semantics.
12. Compatibility status, execution/failure status, and metric eligibility shall remain distinct.
13. `XX^H/L` in the VP-001 baseline shall be called the uncentered sample second moment, not centered sample covariance.
14. Divisor-`N` empirical variance used in exact finite-sample MSE decomposition shall remain distinct from divisor-`N-1` sample variance used for statistical variance estimation.
15. VP-001 confirmatory Monte Carlo studies should prefer predeclared fixed-`N` execution with achieved uncertainty/adequacy reporting; no universal numeric `N` is accepted.
16. Wilson score interval is the candidate VP-001 default for ordinary IID fixed-`N` Bernoulli probability reporting, not a universal ADR-004 interval method.

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
Pre-Gate consistency review                           NEXT
Gates A-F                                             NOT STARTED
ADR-004 acceptance                                    NOT ACCEPTED
```

## 7. Reconciled Decision Families in the Governing ADR

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

## 8. Immediate Work Item

Perform a dedicated pre-Gate consistency review of `ADR-004-validation-reproducibility-scientific-evidence.md` against:

- the reconciled decision families `F1–F14`;
- `ADR-004_EXPLORATION_4.20_CROSS_SECTION_RECONCILIATION.md`;
- the Phase 0C roadmap coverage requirements;
- accepted ADR-001, ADR-002, and ADR-003 authority boundaries;
- the exact terminology and denominator/failure/profile semantics established during reconciliation.

The review shall explicitly check covariance-object naming, `v_N` versus `s^2`, truth/reference/calibration roles, snapshot/trial/source-count distinctions, `P_D`/`P_res` universes, compatibility/failure/metric-eligibility separation, VP-001 fixed-`N`/Wilson scoping, hardware implementation versus physical validation, and publication/provenance immutability.

Gate A may begin only if this pre-Gate review passes.
