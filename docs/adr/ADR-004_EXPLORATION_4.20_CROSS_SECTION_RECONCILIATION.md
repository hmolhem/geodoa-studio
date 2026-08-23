# ADR-004 Exploration 4.20 — Cross-Section Reconciliation

- **ADR:** ADR-004 — Validation, Reproducibility, and Scientific Evidence
- **Phase:** 0C — Scientific Foundations
- **Exploration:** 4.20
- **Status:** EXPLORATION COMPLETE — CANDIDATE CONTRACT, NOT ACCEPTED
- **Depends on:** Accepted ADR-001, ADR-002, ADR-003; ADR-004 Explorations 4.1–4.19

## 1. Question

> Do the candidate contracts developed in Explorations 4.1–4.19 form one internally coherent scientific-evidence system, and what terminology, precedence rules, profile defaults, unresolved implementation choices, and consolidated decision groups shall govern the drafting of ADR-004?

This exploration is a reconciliation pass. It introduces no new scientific scope unless required to resolve a contradiction or ambiguity already exposed by earlier explorations.

---

## 2. Reconciliation Outcome

Candidate result:

```text
Explorations 4.1–4.19: COMPLETE
Blocking internal contradictions: NONE IDENTIFIED
Blocking cross-ADR contradictions: NONE IDENTIFIED
Terminology drift requiring canonicalization: RESOLVED BELOW
Implementation details intentionally not frozen: RETAINED AS NON-BLOCKING
Ready to draft governing ADR-004: YES
Ready to begin Gate A: NO
```

Candidate rule:

> Completion of exploration authorizes preparation of the governing ADR-004 draft, but no Gate A–F acceptance audit may begin until that draft exists and a pre-Gate consistency review passes.

---

## 3. Authority Precedence

The governing ADR shall preserve the following authority order:

```text
ADR-001 -> geometry, coordinate, receive-phase, reference, channel identity
ADR-002 -> propagation, snapshots, signal/source/noise, covariance, rank, SNR
ADR-003 -> sensor imperfections, calibration, reference planes, compatibility, identifiability
ADR-004 -> evidence, truth/reference roles, stochastic experiments, metrics, uncertainty,
           comparison, failures, implementation cross-validation, provenance, publication
```

Candidate rule:

> ADR-004 may reference upstream equations and semantics but shall label them inherited dependencies rather than duplicate physical authority.

---

## 4. Canonical Evidence Vocabulary

The following terms shall have distinct meanings in the governing draft.

### 4.1 Verification

Evidence that an analytical, numerical, software, or implementation object correctly realizes a declared model/specification/reference.

### 4.2 Physical validation

Evidence comparing a model/system against physical reality or a traceable physical reference within a declared domain and uncertainty model.

### 4.3 Calibration

Inference/correction of model or instrument parameters. Calibration is not validation.

### 4.4 Reproducibility

Ability to reconstruct/recompute/rerun evidence at a declared level. Reproducibility is not correctness.

### 4.5 Benchmark comparison

Evidence comparing methods/geometries/pipelines under a declared fairness contract.

Candidate rule:

> These terms shall not be used interchangeably in the governing ADR, result statuses, publication text, or software metadata.

---

## 5. Canonical Epistemic Vocabulary

The governing ADR shall distinguish:

```text
truth
reference
measurement
calibration estimate
external-tool/model prediction
algorithm estimate
unresolved reference state
```

Candidate rule:

> `truth` shall be reserved for exact-by-construction or otherwise explicitly justified truth roles. Measured, calibrated, CST, high-resolution numerical, or published-reference values shall not become truth merely because they are convenient scoring targets.

When a non-truth reference is used for scoring, metric identity shall include that reference role.

---

## 6. Truth Availability versus Algorithm Input

Earlier explorations distinguish truth used for evaluation from information provided to an algorithm.

Canonical rule:

> Truth available to the evaluator does not imply truth may be supplied to the estimator. Any true source count, true manifold, true noise covariance, true SNR, or other generative parameter supplied to a method is oracle information and must be declared in the method/comparison profile.

This resolves truth-provenance and fair-comparison overlap.

---

## 7. Canonical Experimental Hierarchy

The governing draft shall use:

```text
study
  -> condition
       -> Monte Carlo trial
            -> snapshot(s) / samples within trial
```

with separate:

```text
method / implementation
run / execution
artifact
```

Candidate rule:

> Snapshot count `L`, Monte Carlo trial count `N`, source count `K`, matched-pair count, and condition count are distinct quantities and shall never be reported interchangeably.

---

## 8. Canonical Randomness Rule

Reconciled stochastic policy:

```text
root study seed / seed-set
+ versioned RNG family
+ semantic child-stream derivation
+ condition identity
+ trial identity
+ random-family identity
+ redraw scope
```

Candidate rule:

> No process-global mutable RNG state and no lone integer seed shall be authoritative stochastic provenance.

Trial identity must be independent of worker order, scheduling, batching, or method execution order.

---

## 9. Common Random Numbers Reconciliation

CRN is strongly preferred for fair paired comparisons, but `same random realization` must respect model structure.

Canonical rule:

> Compared methods under the same physical condition should share all scientifically common exogenous latent randomness. They shall not be forced to consume identically shaped random arrays when dimensions or physical channel sets differ.

Examples:

- same geometry / same sensor count: share identical source/noise trial realization where appropriate;
- different geometries: share source waveforms and semantic latent random families; channel-specific noise is paired through a declared semantic mapping rather than pretending unequal-dimensional noise matrices are identical;
- algorithm-internal randomness remains separate unless intentionally paired.

This resolves a potential ambiguity in geometry comparisons.

---

## 10. Covariance Terminology Reconciliation

A significant terminology risk exists around `sample covariance`.

Canonical objects shall remain distinct:

### 10.1 Uncentered sample second moment

\[
\hat R^{(2)}
=
\frac{1}{L}XX^H.
\]

### 10.2 Centered sample covariance

\[
\hat C
=
\frac{1}{L-1}
(X-\bar x\mathbf 1^T)(X-\bar x\mathbf 1^T)^H
\]

under the declared sample-covariance convention.

### 10.3 Population covariance / second moment

These coincide only under appropriate zero-mean assumptions.

Candidate rule:

> VP-001 baseline shall refer to `uncentered sample second moment` for `XX^H/L`; the governing ADR shall not call it centered sample covariance. If a zero-mean population model permits identifying population covariance with the second moment, that equality shall be stated as a model property, not a naming shortcut.

This resolves the principal terminology ambiguity found in 4.19.

---

## 11. Empirical Variance Reconciliation

Two variance formulas appeared for different purposes.

### 11.1 Exact empirical MSE decomposition

For errors `e_i`, define the divisor-`N` centered second moment

\[
v_N
=
\frac{1}{N}\sum_{i=1}^{N}(e_i-\bar e)^2.
\]

Then exactly

\[
\widehat{MSE}
=v_N+\bar e^2.
\]

### 11.2 Unbiased sample variance estimator

\[
s^2
=
\frac{1}{N-1}\sum_{i=1}^{N}(e_i-\bar e)^2
\]

may be used for classical standard-error estimation under suitable assumptions.

Candidate rule:

> `v_N` and `s^2` shall not be conflated. The first supports exact finite-sample MSE decomposition; the second is a statistical variance estimator used where its assumptions apply.

This resolves 4.7/4.11 overlap.

---

## 12. Association / Detection / Resolution Reconciliation

Canonical order:

```text
raw estimator output
-> typed validity/failure state
-> truth-to-estimate association under declared gate/cost
-> detection/miss/spurious outcomes
-> resolution event
-> localization metrics on declared matched set
```

Candidate rule:

> Association is an evaluation operation; detection and resolution are event semantics built on valid outputs and association; RMSE is a localization metric and shall not define detection or resolution.

---

## 13. Spurious Detection versus Formal False Alarm

Canonical terminology:

- **spurious/unmatched estimate:** valid estimator output not associated to truth under the benchmark contract;
- **formal false alarm:** event defined under an explicit null/absence/detection-theory protocol with its own denominator.

Candidate rule:

> The governing ADR shall not call every unmatched multi-source estimate `P_FA` evidence.

---

## 14. Resolution Reconciliation

Canonical resolution semantics:

> A designated source pair/group is truth-based resolved only when its required truth members receive distinct admissible one-to-one estimate matches under the declared event policy.

Additional criteria such as `no spurious estimates` define stricter events and require separate names.

Candidate rule:

> Beamwidth, Rayleigh heuristic, grid spacing, peak count, peak separation, and truth separation are not interchangeable with empirical resolution success.

---

## 15. Probability-of-Resolution Universe

The general ADR shall permit multiple explicitly labeled universes, but VP-001 needs one baseline.

Reconciled VP-001 baseline:

```text
scientifically eligible + method-compatible trial
    estimator valid and pair resolved       -> R = 1
    estimator valid but unresolved/missed   -> R = 0
    numerical/algorithm failure             -> R = 0 for end-to-end P_res,
                                               while typed failure remains recorded
    invalid input / outside profile          -> excluded from VP-001 metric universe
    method incompatible by declared profile  -> not an ordinary P_res trial; report incompatibility separately
```

A conditional valid-output `P_res` may be reported only as a separately labeled secondary metric with failure rate alongside it.

Candidate rule:

> The baseline end-to-end probability metric shall not improve by silently deleting estimator failures.

---

## 16. Detection Probability Universe

For VP-001 source-level detection probability, the denominator shall be the declared eligible truth-source opportunities in method-compatible trials.

Reconciled mapping:

```text
admissibly matched truth source -> detected
valid unmatched truth source    -> missed
method numerical failure        -> non-detection for end-to-end P_D, plus failure record
outside-profile / invalid truth -> excluded and separately accounted
```

Candidate rule:

> Other conditional `P_D` definitions remain possible but require explicit distinct metric identity.

---

## 17. Metric versus Acceptance Policy

Across all explorations:

```text
metric = how much / how often / how different
acceptance criterion = whether that result is adequate for a declared claim
```

Candidate rule:

> ADR-004 shall define metric semantics and evidence requirements without introducing universal engineering thresholds such as `RMSE < 1 deg`, `P_res > 0.9`, or one global numerical tolerance.

Thresholds belong to profiles/tests/requirements and require justification.

---

## 18. Monte Carlo Adequacy Reconciliation

Canonical general rule:

> No universal `N` is sufficient. Adequacy is metric-, condition-, dependence-, tail-, precision-, and claim-specific.

Required diagnostics may include:

```text
trial counts / event counts
running or block estimates
MC standard-error/interval evidence where appropriate
rare-event/tail/failure diagnostics
hierarchical effective sampling awareness
stopping reason
```

A visually flat curve is not proof of adequacy.

---

## 19. VP-001 Stopping Policy Simplification

To keep the first implementation auditable, reconciled candidate default:

> Confirmatory VP-001 benchmark profiles should begin with a predeclared fixed trial count per condition, selected using pilot/planning evidence, and then report achieved uncertainty/adequacy diagnostics.

Sequential/adaptive stopping remains allowed in the general ADR only under a predeclared inference-compatible rule.

Candidate rule:

> VP-001 does not prescribe one numeric `N`; it prefers fixed-`N` confirmatory execution over outcome-driven stopping for the first reference implementation.

---

## 20. Probability Interval Reconciliation

General ADR rule:

> Binomial probability uncertainty requires a bounded method compatible with event count, sample size, dependence, and stopping design; Wald is not a universal default.

Reconciled VP-001 candidate default for ordinary IID fixed-`N` Bernoulli conditions:

```text
Wilson score interval
confidence level explicitly recorded
```

Candidate rule:

> Wilson is a VP-001 reporting default, not a universal method for clustered, sequential, weighted, rare-event-importance-sampled, or otherwise non-binomial evidence.

This resolves 4.11/4.19's `candidate default` ambiguity.

---

## 21. RMSE Uncertainty Reconciliation

Canonical rule:

> MSE is the mean of squared errors; RMSE is a nonlinear square-root transform. RMSE uncertainty shall derive from a declared valid treatment of MSE/squared-error evidence, such as transformed valid MSE intervals, delta methods in regular regimes, or justified resampling.

No universal RMSE-CI formula is frozen in ADR-004.

---

## 22. Failure / Compatibility / Metric-Eligibility Separation

Three authoritative layers:

```text
compatibility status  -> is the method/model/profile scientifically admissible?
execution/outcome status -> what happened in this concrete trial/run?
metric eligibility     -> does this outcome belong in this metric's universe?
```

Candidate rule:

> No single `valid` or `success` boolean shall collapse these three layers.

This is a mandatory terminology guard for the governing draft.

---

## 23. Failure-State Canonicalization

The governing ADR should define semantic failure families, not prematurely freeze software enum spellings.

Required families include:

```text
valid result / valid no detection
miss / spurious / unresolved group
ambiguity / unidentifiability
incompatible / outside domain
invalid input/reference
numerical failure / nonconvergence
calibration/data/hardware/infrastructure failure
unresolved scientific state
not assessed
```

Candidate rule:

> `NaN` remains a numeric representation only; root cause, stage, severity, retry history, and metric eligibility are separate structured evidence.

---

## 24. Retry / Replacement Reconciliation

Canonical rule:

```text
retry same trial -> same scientific realization, failure history retained
replacement realization -> new trial identity
```

A retry mechanism shall never resample until success while pretending the original trial survived.

---

## 25. Fair-Comparison Reconciliation

A fair comparison requires a declared contract covering:

```text
scientific task/domain
truth/reference
signal/noise/SNR/snapshots
sensor/calibration profile
oracle information
pre/postprocessing
association/failure/metric semantics
tuning data and budget
trial pairing / CRN
resource constraints
comparison uncertainty
computational timing scope
```

Candidate rule:

> `same metric name` is not sufficient evidence of comparability.

---

## 26. Geometry Comparison Reconciliation

Canonical resource distinctions:

```text
physical sensor count
physical aperture
minimum spacing
RF-channel count
virtual/coarray DOF
calibration / implementation burden
```

Candidate rule:

> Geometry superiority claims must state what is fixed and what is allowed to change. Performance at fixed physical sensor count is not automatically topology-only performance independent of aperture.

---

## 27. Tuning / Final-Test Reconciliation

Canonical evidence roles:

```text
exploration/development
calibration/fitting
tuning/hyperparameter selection
confirmatory/final evaluation
regression
physical validation
```

Candidate rule:

> Final-test evidence used to change hyperparameters, thresholds, geometry, association gates, or headline-condition selection becomes development/tuning evidence unless a new held-out evaluation is performed.

---

## 28. Statistical versus Engineering Claims

Canonical distinction:

```text
statistical uncertainty -> what finite evidence supports about a quantity/effect
engineering significance -> whether effect magnitude meets a practical requirement/margin
```

Candidate rule:

> `not significantly different` shall not mean `equivalent`. Superiority, noninferiority, and equivalence require claim-specific effect/margin semantics.

---

## 29. Multi-Level Error Chain Reconciliation

Canonical diagnostic chain:

```text
manifold
-> covariance
-> eigenvalue/eigenspace
-> spectrum/objective
-> peak/event
-> final DOA
```

Candidate rule:

> Intermediate errors localize disagreement but do not imply a universal monotonic causal map to final DOA. Mechanism attribution requires controlled evidence.

---

## 30. Gauge Reconciliation

Allowed nuisance alignments may include:

```text
common phase
common complex scale
individual eigenvector phase
subspace basis rotation
source permutation through association
```

Candidate rule:

> Gauge alignment is an evaluation transform only when upstream scientific semantics justify the nuisance freedom. It shall not move physical references, conceal channel-dependent mismatch, or become undeclared calibration.

---

## 31. Hardware Evidence Reconciliation

Canonical evidence ladder:

```text
accepted scientific contract
-> verified float64 reference
-> optional float32 assessment
-> explicit fixed-point model
-> bit-accurate implementation model
-> HLS/RTL verification
-> synthesis/place-route/timing evidence
-> FPGA board replay
-> later physical sensor/system validation
```

Candidate rule:

> Synthetic board replay is digital implementation/integration evidence, not physical array validation.

---

## 32. Bit-Exact versus Numerical-Equivalence Reconciliation

Canonical rule:

- bit-exactness applies where exact integer/fixed datapath equivalence is an intended interface contract;
- numerical equivalence/bounded degradation applies where operation reordering or representation changes legitimately alter low-order values.

The required target is declared per interface/test.

---

## 33. Scientific versus Computational Metrics

Canonical separation:

```text
scientific: manifold/covariance/subspace/spectrum/DOA/detection/resolution
engineering: latency/II/throughput/resource use/timing closure/power/energy
```

Candidate rule:

> These axes may be combined in Pareto analysis, but one shall not substitute for the other.

---

## 34. Provenance Reconciliation

Required identity layers:

```text
study
condition
trial / trial ensemble
algorithm
implementation
run/execution
data/calibration/external artifact
derived result/figure/table
hardware build
```

Candidate rule:

> `run_id`, timestamp, branch name, path, filename, or root seed alone is never sufficient scientific identity.

---

## 35. Canonical Configuration Hash Reconciliation

General rule:

> Hash the versioned canonical semantic configuration, not arbitrary user-authored serialization.

Canonicalization may normalize:

```text
units
representation
allowed order-insensitive sets
explicit defaults
```

but may not erase:

```text
phase reference
physical channel order
far-field/narrowband status
snapshot/SNR/covariance semantics
sensor/calibration/reference-plane state
compatibility profile
```

Candidate implementation preference:

```text
versioned cryptographic hash; SHA-256 remains Phase-1 candidate baseline
```

Hash algorithm choice is not a blocking scientific decision if versioned.

---

## 36. Publication Reconciliation

Canonical publication rule:

> Every material quantitative claim must resolve to a frozen/versioned evidence package containing resolved configuration, provenance, trial/metric/failure/uncertainty evidence, derived figure/table lineage, and reproduction instructions appropriate to the claimed level.

A figure/table is a derived artifact, not the sole evidence source.

---

## 37. Immutable Evidence Rule

Once cited/accepted evidence is frozen:

```text
change in code/config/trials/policies -> new evidence identity
bug correction -> preserve old package + new corrected package
```

Candidate rule:

> Silent in-place replacement of cited evidence is forbidden.

---

## 38. VP-001 Canonical Baseline after Reconciliation

Reconciled VP-001 remains:

```text
1-D receive arrays
ADR-001 steering/phase convention
far-field + narrowband PM-001
K=1 and K=2 primary cases
proper-complex zero-mean independent sources
proper-complex white equal-variance additive noise
ADR-003 Phase-1 ideal sensor, H_sensor = I
L simultaneous-equivalent snapshots per trial
uncentered sample second moment XX^H/L as baseline matrix object
Bartlett / MVDR / MUSIC; oracle-K MUSIC explicitly labeled
explicit theta search grid / peak policy
one-to-one association with study-declared gate
bias / MSE / RMSE + coverage
P_D / miss / spurious + P_res + failure evidence
fixed-N confirmatory Monte Carlo as preferred initial execution policy
Wilson interval default for ordinary IID fixed-N Bernoulli P_D/P_res reporting
full RNG/provenance/publication evidence
float64 -> fixed/HLS/FPGA implementation path
```

Candidate rule:

> These are candidate profile semantics to be written into the governing ADR/profile section; no authoritative scientific implementation is authorized before ADR-004 acceptance.

---

## 39. Intentionally Unfrozen Implementation Choices

The following need not block the governing ADR draft:

```text
final Python class names / enums
final YAML/JSON schema
final package-directory layout
exact hash serialization implementation
final UUID/run-id format
specific Hungarian solver/library
specific Wilson implementation/library
specific bootstrap library
specific HLS tool-flow automation
specific artifact archive/DOI service
```

Candidate rule:

> The governing ADR shall freeze scientific semantics and required provenance, not incidental library/API structure unless that structure changes scientific meaning.

---

## 40. Decisions Deferred to Study/Profile Level

The governing ADR shall intentionally not choose one universal value for:

```text
association gate
search-grid spacing
peak threshold/prominence
Monte Carlo N
confidence level
RMSE acceptance threshold
P_res target probability
fixed-point word lengths
FPGA resource/latency target
calibration tolerance
condition-number cutoff
```

Each must be declared/justified in its test/profile/engineering requirement.

---

## 41. Drafting Risks Resolved from 4.18

The semantic-drift risks from Exploration 4.18 reconcile as follows:

```text
RISK-01 truth -> use typed truth/reference roles
RISK-02 valid -> split compatibility / execution status / metric eligibility
RISK-03 covariance -> name exact matrix object
RISK-04 delay -> physical delay / sampling offset / algorithm latency distinct
RISK-05 resolution -> truth-event resolution distinct from grid/beamwidth/topology
RISK-06 equivalent -> state gauge and/or engineering margin
RISK-07 hardware validated -> distinguish implementation/board/physical validation
RISK-08 same configuration -> include ADR/profile/schema versions
RISK-09 source count -> distinct from rank/model order/output cardinality
RISK-10 calibrated -> calibration evidence does not imply validation
```

Candidate rule:

> These canonical distinctions shall be mandatory terminology checks in the governing draft and pre-Gate consistency review.

---

## 42. Consolidated Governing-ADR Structure

The governing ADR-004 should be drafted around the following consolidated sections rather than copying all 20 explorations verbatim:

```text
1. Decision / scope / authority
2. Evidence taxonomy: verification, validation, calibration, reproducibility
3. Truth/reference provenance
4. Deterministic reference evidence
5. Stochastic experiment / trial / RNG / CRN semantics
6. Association, detection, resolution, localization metrics
7. Monte Carlo adequacy and uncertainty
8. Fair algorithm/geometry comparison
9. Failure, ambiguity, incompatibility, eligibility
10. Multi-level scientific diagnostics
11. Float/fixed/HLS/FPGA cross-validation
12. Run/config/data/calibration/hardware provenance
13. Publication/reproducibility package
14. VP-001 initial validation profile
15. Boundaries / deferred profiles / consequences
```

Candidate rule:

> Exploration numbering is historical working organization and need not become the final ADR section numbering.

---

## 43. Consolidated Candidate Decision Families

The governing draft shall consolidate the detailed `D4.x-*` decisions into these authoritative families:

### F1 — Evidence-role separation
Verification, physical validation, calibration, reproducibility, benchmark comparison, and implementation cross-validation are distinct.

### F2 — Typed truth/reference authority
Truth/reference role, domain, frame, provenance, uncertainty, and allowed algorithm visibility are explicit.

### F3 — Deterministic verification ladder
Analytical/GRP/cross-reference evidence precedes promotion of software/hardware references.

### F4 — Stochastic experiment identity
Study/condition/trial/random-family/redraw semantics and reproducible RNG derivation are explicit.

### F5 — Association/event semantics
Unordered multi-source association, detection, miss, spurious output, resolution, and final localization metrics remain distinct.

### F6 — Metric semantics
Bias/variance/MSE/RMSE, probability metrics, denominators, units, coordinates, conditioning, and weighting are explicit.

### F7 — Adequacy/uncertainty
No universal trial count; finite stochastic evidence carries metric-compatible adequacy and uncertainty.

### F8 — Fair comparison
Task/information/tuning/randomness/evaluation/resources/timing scope and comparison uncertainty are controlled or declared.

### F9 — Typed non-success evidence
Failure, ambiguity, incompatibility, out-of-domain, unidentifiability, miss, and unresolved states are preserved.

### F10 — Multi-level diagnosis
Manifold/covariance/eigenstructure/spectrum/event/DOA metrics diagnose disagreement without false causal attribution.

### F11 — Hardware equivalence ladder
Scientific correctness -> float -> fixed -> bit-accurate -> HLS/RTL -> board -> physical validation remain separate layers.

### F12 — Provenance and immutability
Configuration, Git, RNG, data, calibration, analysis-policy, environment, hardware build, and artifact lineage are versioned and auditable.

### F13 — Publication evidence
Claims trace to frozen reproducibility packages; plots/tables alone are not evidence packages.

### F14 — VP-001 baseline
The first executable profile is ideal 1-D far-field narrowband DOA, deliberately excluding later realism.

Candidate rule:

> Detailed exploration decisions remain supporting rationale, while these families form the governing ADR's compact normative backbone.

---

## 44. No Blocking Open Scientific Question before Draft

After reconciliation, no unresolved issue requires additional exploration before the governing draft.

Non-blocking items intentionally remain profile/implementation choices, including exact thresholds, schemas, API names, and tool-library selections.

Candidate result:

```text
scientific semantics ready for governing draft: YES
profile VP-001 semantics ready for governing draft: YES
acceptance gates ready to begin immediately: NO
```

---

## 45. Required Pre-Gate Review after Draft

After the governing ADR-004 draft is created, the pre-Gate consistency review shall explicitly verify:

```text
all F1–F14 decision families represented
no upstream ADR authority duplicated/redefined
covariance-object terminology exact
truth/reference/calibration roles exact
snapshot/trial/count terminology exact
compatibility/failure/eligibility separation exact
P_D/P_res denominator/failure mapping explicit
metric versus threshold separation preserved
VP-001 fixed-N/Wilson defaults correctly scoped
hardware implementation vs physical validation boundary explicit
provenance/publication immutability requirements represented
no candidate exploration wording accidentally promoted beyond scope
```

Candidate rule:

> Gate A may start only after this review passes.

---

## 46. Golden Reference Program Reconciliation

GRP-018 remains reserved for:

```text
Bias / Variance / MSE / RMSE by hand
```

Its key finite-sample semantic check remains:

```text
truth = 10 deg
estimates = {9, 10, 12, 13} deg
errors = {-1, 0, 2, 3} deg
bias = 1 deg
MSE = 3.5 deg^2
RMSE = sqrt(3.5) = 1.870828693... deg
v_N = 2.5 deg^2
MSE = v_N + bias^2
unbiased sample variance = 10/3 deg^2, not the exact divisor-N decomposition term
```

Candidate rule:

> This remains exploration reference content until formal Gate E evidence is created and passed.

No additional canonical GRP number is introduced by reconciliation.

---

## 47. Exploration-to-Draft Traceability

The governing draft should retain a traceability appendix/table mapping:

```text
4.1  -> F1
4.2  -> F2
4.3  -> F3
4.4–4.5 -> F4
4.6–4.9 -> F5/F6
4.10–4.11 -> F7
4.12 -> F8
4.13 -> F9
4.14 -> F10
4.15 -> F11
4.16 -> F12
4.17 -> F13
4.18 -> authority/cross-ADR constraints across all families
4.19 -> F14
4.20 -> canonical reconciliation / drafting rules
```

Candidate rule:

> Exploration documents remain rationale/supporting evidence and shall not be deleted merely because a concise governing ADR is drafted.

---

## 48. Reconciliation Status

```text
Internal terminology reconciliation: PASS AT EXPLORATION LEVEL
Metric/event reconciliation: PASS AT EXPLORATION LEVEL
Stochastic/provenance reconciliation: PASS AT EXPLORATION LEVEL
Failure/compatibility reconciliation: PASS AT EXPLORATION LEVEL
Hardware evidence reconciliation: PASS AT EXPLORATION LEVEL
VP-001 profile reconciliation: PASS AT EXPLORATION LEVEL
Cross-ADR authority reconciliation: PASS AT EXPLORATION LEVEL
Blocking contradiction: NONE IDENTIFIED
Governing ADR-004 draft: AUTHORIZED AS NEXT STEP
ADR-004 accepted: NO
```

This is not a Gate A–F result.

---

## 49. Candidate Decisions from Exploration 4.20

- **D4.20-01:** Explorations 4.1–4.19 form a coherent candidate evidence contract with no blocking contradiction identified.
- **D4.20-02:** ADR-004 remains downstream of ADR-001/002/003 scientific authority and owns evidence semantics only.
- **D4.20-03:** Verification, validation, calibration, reproducibility, comparison, and implementation cross-validation remain distinct evidence roles.
- **D4.20-04:** Truth, reference, measurement, calibration estimate, external-model prediction, and estimator output remain distinct epistemic roles.
- **D4.20-05:** Study, condition, trial, snapshot/sample, method, implementation, run, and artifact identities remain distinct hierarchy levels.
- **D4.20-06:** `XX^H/L` in VP-001 is canonically the uncentered sample second moment; centered sample covariance is a distinct object.
- **D4.20-07:** Divisor-`N` empirical variance `v_N` is the exact MSE-decomposition term; divisor-`N-1` sample variance serves a different statistical-estimation role.
- **D4.20-08:** Association, detection, spurious output, resolution, and localization metrics follow a typed evaluation sequence and shall not define one another implicitly.
- **D4.20-09:** Formal false alarm remains distinct from generic unmatched/spurious estimates.
- **D4.20-10:** VP-001 end-to-end `P_res` and `P_D` count numerical algorithm failure as non-success while retaining typed failure evidence; incompatible/out-of-profile conditions are separately accounted rather than coerced into ordinary metric failures.
- **D4.20-11:** No universal Monte Carlo count is accepted; VP-001 confirmatory benchmarks prefer predeclared fixed-`N` execution with achieved adequacy/uncertainty reporting.
- **D4.20-12:** Wilson score interval is the candidate VP-001 default for ordinary IID fixed-`N` Bernoulli probability reporting, not a universal ADR-004 interval method.
- **D4.20-13:** Compatibility, execution/failure status, and metric eligibility are three distinct authoritative layers; no bare `valid`/`success` boolean replaces them.
- **D4.20-14:** Fair comparison requires controlled/declaration of task, information, stochastic realization, SNR/signal/sensor semantics, tuning, evaluation, resources, and comparison uncertainty.
- **D4.20-15:** CRN shares scientifically common exogenous latent randomness; it does not force incompatible-dimensional arrays to be numerically identical.
- **D4.20-16:** Gauge alignment removes only declared nuisance degrees of freedom and does not redefine physical phase/reference/calibration semantics.
- **D4.20-17:** Multi-level manifold-to-DOA diagnostics support failure localization but not automatic causal attribution.
- **D4.20-18:** Float/fixed/HLS/RTL/FPGA/physical validation remain distinct evidence layers; synthetic board replay is not physical validation.
- **D4.20-19:** Scientific and computational/hardware metrics remain separate axes, optionally combined through explicit trade-off analysis.
- **D4.20-20:** Scientific identities use versioned canonical semantics and provenance; hashes support identity but do not replace human-readable configuration or meaning.
- **D4.20-21:** Publication evidence is immutable/versioned and claim-traceable; corrections create new evidence identities.
- **D4.20-22:** VP-001 is reconciled as the candidate initial executable profile and intentionally excludes later sensor/wideband/near-field/physical complexity.
- **D4.20-23:** Thresholds, concrete APIs/schemas, software enum spellings, library choices, and tool automation remain non-blocking profile/implementation decisions unless they alter scientific meaning.
- **D4.20-24:** The governing ADR should consolidate exploration decisions into decision families F1–F14 rather than copy all exploration sections verbatim.
- **D4.20-25:** Completion of 4.20 authorizes drafting ADR-004 but does not authorize Gate A; a pre-Gate consistency review is mandatory after the draft.

---

## 50. Exploration 4.20 Conclusion

Exploration 4.20 is complete at candidate-contract level.

The reconciled central rule is:

> ADR-004 shall define a typed, layered, provenance-preserving scientific evidence system in which upstream scientific semantics remain authoritative; truth/reference roles, stochastic trials, association/events, localization metrics, failures, uncertainty, fair comparisons, implementation cross-validation, and publication artifacts remain explicitly distinguishable; VP-001 provides the first deliberately narrow executable benchmark; and no result may acquire stronger scientific meaning merely through filtering, numerical agreement, hardware execution, hashing, or reproducibility packaging. The exploration phase is now sufficiently reconciled to draft the governing ADR-004, after which a separate pre-Gate consistency review is required before Gate A.

No acceptance gate is started or passed by this exploration.

The next work item is:

```text
Draft governing ADR-004 from reconciled decision families F1–F14,
then perform the pre-Gate consistency review before any Gate A activity.
```
