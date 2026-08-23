# ADR-004 — Exploration Checkpoint

- **ADR:** ADR-004 — Validation, Reproducibility, and Scientific Evidence
- **Phase:** 0C — Scientific Foundations
- **Status:** EXPLORATION IN PROGRESS — NOT ACCEPTED
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

The numbering is an exploration organization, not an accepted final section layout. It may be refined before the governing ADR draft as long as roadmap coverage is preserved.

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

## 4. Initial Golden Reference Reservation

The Phase 0C roadmap reserves:

```text
GRP-018 — Bias, Variance, MSE, and RMSE by hand
```

Additional ADR-004 deterministic evidence may use `ADR-004-SRC-*` identifiers so that canonical GRP numbering is not changed without an explicit roadmap decision.

## 5. Working Rules

1. No governing ADR-004 draft before the exploration reaches cross-section reconciliation.
2. No acceptance Gate A before a governing ADR-004 draft exists and a pre-Gate consistency review passes.
3. Exploration calculations are not formal Golden Reference PASS evidence until Gate E.
4. Verification, validation, calibration, benchmarking, and reproducibility shall remain distinct concepts.
5. Metric computation and acceptance policy shall remain distinct.
6. Failed/missed/unresolved trials shall not be silently deleted from benchmark evidence.
7. Randomness and seed provenance shall be explicit enough to reconstruct a trial.
8. Comparative claims shall preserve fairness/provenance rather than rely on uncontrolled independent realizations.
9. A numerical match to a software baseline does not by itself establish physical validation.
10. Hardware acceleration shall be assessed against an accepted scientific reference, not only against another hardware implementation.

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
4.15  Float / Fixed / FPGA Cross-Validation          IN PROGRESS — NEXT
4.16  Run Identity / Configuration / Provenance      NOT STARTED
4.17  Publication / Reproducibility Package          NOT STARTED
4.18  Cross-ADR Compatibility                        NOT STARTED
4.19  Initial Phase-1 Validation Profile             NOT STARTED
4.20  Cross-Section Reconciliation                   NOT STARTED

Governing ADR-004 draft                               NOT STARTED
Pre-Gate consistency review                           NOT STARTED
Gates A-F                                             NOT STARTED
ADR-004 acceptance                                    NOT ACCEPTED
```

## 7. Immediate Work Item

Complete Exploration 4.15 and define floating-point, fixed-point, bit-accurate, HLS/RTL, and FPGA cross-validation against the accepted scientific reference, including quantization/overflow semantics, stage-by-stage numerical tolerances, detection/event equivalence, latency/throughput/resource evidence, and the boundary between implementation verification and physical hardware validation.
