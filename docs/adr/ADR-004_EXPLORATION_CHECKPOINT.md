# ADR-004 — Exploration Checkpoint

- **ADR:** ADR-004 — Validation, Reproducibility, and Scientific Evidence
- **Phase:** 0C — Scientific Foundations
- **Status:** GOVERNING DRAFT COMPLETE — PRE-GATE REVIEW PASS — GATES A-E PASS — GATE F NEXT — NOT ACCEPTED
- **Branch:** `docs/phase0c-scientific-conventions`
- **Depends on:** Accepted ADR-001, ADR-002, ADR-003
- **Roadmap:** `../PHASE0C_SCIENTIFIC_CONTRACTS_ROADMAP.md`
- **Started:** 2026-08-23

## 1. Primary Question

> Under what evidence may GeoDOA Studio call a model, algorithm, experiment, calibration result, numerical implementation, or hardware result verified, validated, reproducible, or better than another method?

ADR-004 defines the scientific evidence contract used by later GeoDOA studies. It does not prescribe one universal benchmark or one universal pass/fail threshold.

## 2. Exploration Status

Explorations 4.1–4.20 are COMPLETE. The governing draft consolidates them into decision families `F1–F14`.

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
```

## 3. Governing Decision Families

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

## 4. Working Rules Carried Forward

1. Verification, physical validation, calibration, benchmarking, implementation cross-validation, and reproducibility remain distinct.
2. Metric computation and acceptance policy remain distinct.
3. Failed/missed/unresolved trials are not silently deleted from benchmark evidence.
4. Randomness/seed provenance must reconstruct trial identity independent of worker/order/global mutable RNG state.
5. Comparative claims preserve fairness, oracle-information, tuning, CRN, resource, and uncertainty provenance.
6. Numerical/software/hardware agreement does not by itself establish physical validation.
7. ADR-004 remains downstream of ADR-001/002/003 scientific authority.
8. Compatibility status, execution/failure status, and metric eligibility remain distinct.
9. `XX^H/L` in VP-001 is the uncentered sample second moment, not centered sample covariance.
10. Divisor-`N` empirical `v_N` used in exact finite-sample MSE decomposition is distinct from divisor-`N-1` sample variance `s^2`.
11. VP-001 confirmatory Monte Carlo studies prefer predeclared fixed-`N` execution with achieved adequacy/uncertainty evidence; no universal numeric `N` is accepted.
12. Wilson score interval is the VP-001 default only for ordinary IID fixed-`N` Bernoulli probability evidence.
13. Source count `K`, source-covariance rank, observed subspace rank, estimator model order, and output cardinality `K_hat` remain distinct.
14. VP-001 end-to-end `P_D` / `P_res` universes and numerical-failure mappings are explicit.
15. External-tool/CST agreement is reference/verification evidence unless a separate physical-validation contract is satisfied.
16. Real-scalar `e^2` formulas are scoped to real localization metrics; future complex-valued errors require an explicit complex squared-error definition.
17. Normalized manifold/projective metrics require valid nonzero vectors.
18. Metric identity preserves coordinate and units; bias/RMSE use base units, variance/MSE squared units.
19. Covariance/eigenvalue units derive from snapshot units; normalized projective/relative metrics are dimensionless on valid domains.
20. dB is a logarithmic representation of a declared ratio/reference, not an unlabeled physical base unit.
21. Fixed-point codes acquire physical/scientific meaning only through explicit scale/LSB semantics; ADC and FPGA quantization remain distinct stages.
22. Hardware latency, II, throughput, resource, power, and energy retain explicit units and scope.
23. Software preserves typed identities, resolved defaults, canonical unit conversion, stable channel ordering, provenance-preserving transforms, and immutable evidence.
24. Metric denominators derive from retained typed trial evidence rather than survivor-only filtering.
25. Cache/resume/retry/replacement preserve scientific identity and do not silently resample/reuse incompatible evidence.
26. Algorithm identity, implementation identity, fixed-point arithmetic profile, host/FPGA packing semantics, and build/artifact identity remain separately auditable.
27. GRP expected values are independent of production software and become formal oracles only at Gate E.

## 5. Pre-Gate Review Record

`ADR-004_PRE_GATE_CONSISTENCY_REVIEW.md` — PASS.

It identified and resolved before Gate A:

```text
PG-004-01  explicit P_D/P_res metric universes/denominators
PG-004-02  explicit population variance semantics
PG-004-03  K / rank / model-order / K_hat distinctions
PG-004-04  explicit independent numerical / external-tool evidence role
```

Governing-draft correction commit:

```text
4675f312214ebc0eaaa64a2041bb582931cf2332
```

Reviewed governing content SHA:

```text
8cca2e3ac514cd031bee1d8c9e4c0347694ecb53
```

## 6. Acceptance Gate Records

### Gate A — Physical Consistency

```text
ADR-004_GATE_A_AUDIT.md
PASS
commit 9b3f261858b435ce493189c1ee9802b68c17d78f
```

Key result: model assumptions, simulation truth, external references, calibration, FPGA execution, and physical validation remain correctly separated.

### Gate B — Mathematical Consistency

```text
ADR-004_GATE_B_AUDIT.md
PASS
commit 7b6fb7e68816ca51c336b526a72e656d61c16dac
```

Key result: bias/variance/MSE/RMSE, assignment/event denominators, covariance/rank semantics, projective/subspace invariances, CRN mathematics, and finite-precision equivalence are internally consistent.

### Gate C — Dimensional / Unit Consistency

```text
ADR-004_GATE_C_AUDIT.md
PASS
commit 07e6e8fb245835f89b9fe4cc305e4e7fee4da5e7
```

Key result: metric units, squared-error units, covariance/eigenvalue units, dimensionless probabilities/projective metrics, dB/SNR, fixed-point scaling, and hardware performance units are consistent.

### Gate D — Software Semantic Consistency

```text
ADR-004_GATE_D_AUDIT.md
PASS
commit 9feae24803842759a36d66a1135708a0a36b4746
```

Key result: hidden defaults/filtering/normalization/global RNG/reordering/provenance loss are forbidden; typed identities and immutable evidence are implementation obligations.

### Gate E — Golden / Hand Reference Evidence

```text
ADR-004_GATE_E_AUDIT.md
PASS
commit dae21e6f6dd022d7039e3d72b77dbce054f58824
```

Golden reference evidence:

```text
../science/golden_reference/ADR-004_GOLDEN_REFERENCE_PROBLEMS.md
commit f7f699b5ed008aa4cdbd42e78c84b5b9497feb2c
```

Formal canonical reference:

```text
GRP-018 — Bias, Variance, MSE, and RMSE by hand
```

Formal GRP-018 oracle:

```text
truth                 10 deg
estimates             9, 10, 12, 13 deg
errors                -1, 0, 2, 3 deg
bias                  1 deg
v_N                   2.5 deg^2
sample variance s^2   10/3 deg^2
MSE                   3.5 deg^2
RMSE                  sqrt(3.5) = 1.8708286933869707 deg
```

Supplemental references:

```text
ADR-004-SRC-01  association / spurious / resolution
ADR-004-SRC-02  P_res denominator / numerical-failure mapping
ADR-004-SRC-03  source-level P_D opportunity counting
ADR-004-SRC-04  projective metric / rank-one projector leakage
```

Gate E formally promotes GRP-018 from exploration arithmetic to accepted deterministic reference evidence.

## 7. Current Status

```text
Governing ADR-004 draft                               COMPLETE — DRAFT ONLY
Pre-Gate consistency review                           PASS
Gate A — Physical Consistency                         PASS
Gate B — Mathematical Consistency                     PASS
Gate C — Dimensional / Unit Consistency               PASS
Gate D — Software Semantic Consistency                PASS
Gate E — Hand Reference Evidence                      PASS
Gate F — Boundary / Failure Analysis                  NEXT
Cross-Gate reconciliation                             NOT STARTED
ADR-004 acceptance                                    NOT ACCEPTED
Authoritative Phase-1 implementation                  NOT YET AUTHORIZED
```

## 8. Immediate Work Item

Begin:

```text
ADR-004 Gate F — Boundary and Failure Analysis
```

Gate F shall classify boundary/invalid/failure behavior across metric domains, empty/zero denominators, association ties, nonzero-vector requirements, invalid units/configuration, out-of-profile scenarios, failed references/calibrations, stochastic replay/provenance defects, numerical failures, cache/resume/retry faults, hardware/protocol failures, and publication-evidence gaps.

Gate F PASS will complete the individual acceptance gates but will **not** by itself accept ADR-004. A final cross-gate reconciliation is required before final acceptance.
