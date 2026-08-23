# ADR-004 — Exploration Checkpoint

- **ADR:** ADR-004 — Validation, Reproducibility, and Scientific Evidence
- **Phase:** 0C — Scientific Foundations
- **Status:** GOVERNING DRAFT COMPLETE — PRE-GATE REVIEW PASS — GATES A-D PASS — GATE E NEXT — NOT ACCEPTED
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
5. Gate C — Dimensional / Unit Consistency passed.
6. Gate D — Software Semantic Consistency passed.
7. Gate E — Hand Reference Evidence is now the next acceptance step; Gate F remains not started.
8. Exploration calculations are not formal Golden Reference PASS evidence until Gate E.
9. Verification, validation, calibration, benchmarking, and reproducibility shall remain distinct concepts.
10. Metric computation and acceptance policy shall remain distinct.
11. Failed/missed/unresolved trials shall not be silently deleted from benchmark evidence.
12. Randomness and seed provenance shall be explicit enough to reconstruct a trial.
13. Comparative claims shall preserve fairness/provenance rather than rely on uncontrolled independent realizations.
14. A numerical match to a software baseline does not by itself establish physical validation.
15. Hardware acceleration shall be assessed against an accepted scientific reference, not only against another hardware implementation.
16. ADR-004 shall remain downstream of ADR-001/002/003 authority for geometry/phase, signal/covariance, and sensor/calibration semantics.
17. Compatibility status, execution/failure status, and metric eligibility shall remain distinct.
18. `XX^H/L` in the VP-001 baseline shall be called the uncentered sample second moment, not centered sample covariance.
19. Divisor-`N` empirical variance used in exact finite-sample MSE decomposition shall remain distinct from divisor-`N-1` sample variance used for statistical variance estimation.
20. VP-001 confirmatory Monte Carlo studies should prefer predeclared fixed-`N` execution with achieved uncertainty/adequacy reporting; no universal numeric `N` is accepted.
21. Wilson score interval is the VP-001 default for ordinary IID fixed-`N` Bernoulli probability reporting, not a universal ADR-004 interval method.
22. Source count `K`, source-covariance rank, observed subspace rank, estimator model order, and estimated-output cardinality `K_hat` shall remain distinct.
23. VP-001 baseline end-to-end `P_D` and `P_res` metric universes and numerical-failure mappings are explicit in the governing draft.
24. External-tool/cross-tool numerical agreement is reference/verification evidence unless a separate physical-validation contract is satisfied.
25. Real-scalar `e^2` bias/MSE formulas are scoped to real localization metrics; future complex-valued error metrics require an explicit complex squared-error definition.
26. Normalized manifold correlation/projective metrics require nonzero vectors; zero/invalid manifold cases require typed ineligibility or a different declared metric.
27. Metric identity shall preserve units/coordinate; bias/RMSE use the base metric unit while variance/MSE use its square.
28. Covariance/eigenvalue units derive from the declared snapshot measurement unit; normalized matrix/subspace metrics are dimensionless only on compatible nonzero-reference domains.
29. dB is a logarithmic representation of a declared ratio/reference and shall not be treated as an unlabeled physical base unit.
30. Fixed-point codes acquire scientific/physical units only through explicit scale/LSB semantics; ADC and FPGA quantization remain separate unit-bearing stages.
31. Hardware latency, II, throughput, resource, power, and energy metrics shall retain explicit unit and scope semantics.
32. Software implementation shall preserve typed domain identities, explicit resolved defaults, canonical unit conversions, stable channel ordering, and provenance-preserving transforms.
33. Scientific RNG behavior shall be semantic/trial-addressable and independent of worker/order/global mutable RNG state.
34. Failure status, compatibility, and metric eligibility shall remain distinct in software; NaN/empty output shall not silently define scientific meaning.
35. Metric denominators shall be derived from retained typed trial evidence rather than survivor-only filtering.
36. Cache/resume/retry/replacement behavior shall preserve scientific identity and shall not resample or reuse incompatible evidence silently.
37. Algorithm identity, implementation identity, fixed-point arithmetic profile, host/FPGA packing semantics, and build/artifact identity shall remain separately auditable.
38. Accepted/publication evidence shall be immutable/versioned and derived figure/table transformations shall remain scripted or explicitly recorded.

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
Gate C — Dimensional / Unit Consistency               PASS
Gate D — Software Semantic Consistency                PASS
Gate E — Hand Reference Evidence                      NEXT
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

Gate B also carried explicit mathematical domain conditions forward for Gate F, including nonzero-vector requirements for normalized manifold metrics and real-scalar scope for the current `e^2` localization formulas.

Gate B commit:

```text
7b6fb7e68816ca51c336b526a72e656d61c16dac
```

## 10. Gate C Record

The Gate C dimensional/unit-consistency audit is:

```text
ADR-004_GATE_C_AUDIT.md
```

Gate C passed without requiring a governing-draft correction.

Gate C verified, among other items:

```text
canonical radians versus direction-cosine semantics
error/bias/RMSE versus variance/MSE unit propagation
GRP-018 degree/radian conversion at audit level
probability/count dimensional semantics
association-cost/gate unit compatibility
snapshot -> covariance/eigenvalue unit propagation
relative matrix and projective metric normalization
principal/projective angle units
spectrum and dB representation semantics
SNR ratio versus dB representation
fixed-point scale/LSB unit semantics
ADC versus FPGA quantization units
latency / II / throughput / resource / power / energy units
canonical configuration unit normalization
external/calibration artifact unit provenance
```

Gate C commit:

```text
07e6e8fb245835f89b9fe4cc305e4e7fee4da5e7
```

## 11. Gate D Record

The Gate D software-semantic audit is:

```text
ADR-004_GATE_D_AUDIT.md
```

Gate D passed without requiring a governing-draft correction.

Gate D verified, among other items:

```text
typed study/condition/trial/method/implementation/run/artifact identities
authoritative versus derived configuration semantics
validated unit-conversion boundaries
stable channel identity and explicit permutations
resolved scientific defaults / canonical configuration hashing
semantic child RNG streams independent of worker/order/global state
CRN pairing and evaluation-side truth association
unequal-cardinality evidence preservation
failure status separate from NaN/numeric payload
compatibility / execution / metric-eligibility separation
no silent denominator filtering or arbitrary RMSE miss penalties
uncentered-second-moment object identity and no silent matrix repair
no silent physical geometry sorting/normalization/snapping
cache/resume/retry/replacement scientific identity
oracle-information provenance
algorithm versus implementation/build identity
fixed-point arithmetic / host-FPGA transport semantics
content-addressed data/calibration/build/publication artifact identity
immutable/versioned publication evidence
```

Gate D commit:

```text
9feae24803842759a36d66a1135708a0a36b4746
```

## 12. Reconciled Decision Families in the Governing ADR

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

## 13. Immediate Work Item

Begin:

```text
ADR-004 Gate E — Golden Reference / Hand Reference Evidence
```

Gate E shall create and formally verify GRP-018 and any necessary deterministic supplemental reference checks without promoting exploratory calculations or production outputs into accepted reference evidence merely because they match themselves.

Gate E PASS does not imply Gate F PASS and does not accept ADR-004.
