# ADR-004 Exploration 4.13 — Failure-State Recording

- **ADR:** ADR-004 — Validation, Reproducibility, and Scientific Evidence
- **Phase:** 0C — Scientific Foundations
- **Exploration:** 4.13
- **Status:** EXPLORATION COMPLETE — CANDIDATE CONTRACT, NOT ACCEPTED
- **Depends on:** Accepted ADR-001, ADR-002, ADR-003; ADR-004 Explorations 4.1–4.12

## 1. Question

> How shall GeoDOA represent, preserve, aggregate, and report failed, invalid, incompatible, unresolved, ambiguous, missed, and degraded trial outcomes so that scientific evidence is not silently destroyed by `NaN`, exception handling, filtering, or forced numeric coercion?

This exploration defines the failure-state evidence contract used by later scientific metrics, hardware cross-validation, run provenance, and publication packages.

---

## 2. Core Principle

A failed or unresolved trial is not missing metadata. It is scientific evidence.

Candidate rule:

> GeoDOA shall preserve failure state as a typed outcome with cause, scope, stage, provenance, and downstream metric eligibility; no failed scientific state shall be reduced silently to an unlabeled `NaN`, dropped row, zero, maximum-angle penalty, or retry-generated replacement realization.

---

## 3. Failure Is Not One Concept

GeoDOA shall distinguish at least the following conceptual classes:

```text
VALID_RESULT
VALID_NO_DETECTION
MISSED_SOURCE
SPURIOUS_DETECTION
UNRESOLVED_SOURCE_GROUP
AMBIGUOUS_RESULT
INCOMPATIBLE_CONFIGURATION
OUTSIDE_DECLARED_DOMAIN
INVALID_INPUT
INVALID_REFERENCE_OR_TRUTH
MODEL_UNIDENTIFIABLE
NUMERICAL_FAILURE
ALGORITHM_NONCONVERGENCE
RESOURCE_FAILURE
HARDWARE_PROTOCOL_FAILURE
DATA_INTEGRITY_FAILURE
CALIBRATION_INVALID_OR_STALE
UNRESOLVED_SCIENTIFIC_STATE
NOT_ASSESSED
```

These are candidate scientific categories, not final software enums.

Candidate rule:

> Categories that differ in scientific meaning shall remain distinguishable even if all prevent ordinary metric computation.

---

## 4. Valid No-Detection versus Numerical Failure

Suppose a detector/estimator completes normally and returns no valid peaks.

That can be a scientifically valid output:

```text
VALID_NO_DETECTION
```

By contrast, an eigensolver crash, singular illegal solve, overflow, or unhandled exception is a different state:

```text
NUMERICAL_FAILURE
```

Candidate rule:

> Empty valid output and failed computation are not interchangeable.

This distinction is essential for `P_D`, miss rate, failure rate, and `P_res`.

---

## 5. Miss versus Failure

A **miss** is an evaluation outcome for an otherwise valid estimator output under a declared association/detection policy.

A **failure** means the method did not produce a scientifically valid output under the benchmark contract.

Candidate rule:

> `MISSED_SOURCE` shall not be used as a generic catch-all for numerical or compatibility failures.

A benchmark may map some failures to system-level non-success for a particular metric, but the original typed cause must remain available.

---

## 6. Incompatible Configuration versus Poor Performance

An algorithm may be mathematically incompatible with a condition.

Examples:

- ULA-structure-dependent ESPRIT on unsupported geometry;
- ordinary MUSIC under a profile requiring whitening but no whitening supplied;
- narrowband estimator on a condition explicitly outside the accepted narrowband profile;
- source count exceeding a method's declared identifiability/rank domain.

Candidate rule:

> Incompatibility shall not be converted into arbitrarily large RMSE or automatic algorithmic inferiority.

It is a domain-compatibility result.

---

## 7. Outside-Domain versus Incompatible

These two concepts are related but distinct.

### 7.1 Outside declared experiment/model domain

The condition itself lies outside the benchmark/profile's scientific validity.

### 7.2 Method incompatible within an otherwise valid benchmark condition

The benchmark condition is valid, but one particular method does not support it.

Candidate rule:

> GeoDOA shall preserve whether invalidity belongs to the study condition or to the method/profile compatibility relation.

---

## 8. Invalid Input versus Hard Scientific Case

Examples of invalid input:

```text
NaN sensor coordinate
negative snapshot count
malformed covariance dimensions
missing required calibration artifact
unitless value where units are mandatory
corrupt reference data
```

Examples of difficult but valid input:

```text
low SNR
closely spaced sources
nearly singular covariance
weak eigengap
endfire source
high source coherence within declared profile
```

Candidate rule:

> Difficult valid conditions shall not be reclassified as invalid merely because an algorithm performs poorly.

---

## 9. Numerical Failure Taxonomy

Numerical failure should preserve enough detail to identify the mechanism.

Candidate subcategories include:

```text
NONFINITE_GENERATED
NONFINITE_PROPAGATED
SINGULAR_SOLVE
ILL_CONDITIONED_BEYOND_POLICY
EIGENSOLVER_FAILURE
SVD_FAILURE
OPTIMIZER_DIVERGENCE
MAX_ITERATIONS_REACHED
OVERFLOW
UNDERFLOW_MATERIAL
DIVIDE_BY_ZERO
INVALID_LOG_OR_SQRT
NEGATIVE_VARIANCE_NUMERICAL
PSD_VIOLATION_BEYOND_TOLERANCE
FIXED_POINT_OVERFLOW
SATURATION_EXCEEDED_POLICY
```

Candidate rule:

> Numerical diagnostics shall distinguish genuine mathematical invalidity from finite-precision tolerance violations and from ordinary ill-conditioning.

---

## 10. Algorithm Nonconvergence

An iterative algorithm reaching its iteration limit is not necessarily the same as a crash.

Possible statuses:

```text
CONVERGED
STOPPED_BY_TOLERANCE
STOPPED_BY_MAX_ITER
DIVERGED
STAGNATED
INFEASIBLE
UNRESOLVED_CONVERGENCE_STATUS
```

Candidate rule:

> Iterative termination reason is part of scientific output provenance when it affects estimate validity.

If a max-iteration result is still accepted as a degraded approximate estimate, that acceptance policy must be explicit.

---

## 11. Ambiguous Result versus Failed Result

Some outputs may be numerically valid but scientifically ambiguous.

Examples:

- equal-cost truth-to-estimate assignments;
- grating-lobe alias candidates with no unique physical disambiguation;
- repeated eigenvalue with non-unique individual eigenvectors;
- unresolved calibration gauge;
- symmetry-induced multiple equivalent DOAs.

Candidate rule:

> Scientific ambiguity shall remain a typed state and shall not be mislabeled as numerical failure.

When an equivalence class is the correct scientific output, the evaluation should compare equivalence classes rather than force a unique point.

---

## 12. Unresolved Scientific State

Sometimes available evidence is insufficient to classify a trial confidently as valid, invalid, or failed.

Candidate status:

```text
UNRESOLVED_SCIENTIFIC_STATE
```

Examples:

- uncertain calibration validity domain;
- incomplete external-tool provenance;
- ambiguous reference-plane mapping;
- unknown source identity preventing defensible association;
- suspected but unconfirmed data corruption.

Candidate rule:

> `UNRESOLVED` is an allowed terminal evidence state and shall not be promoted to PASS/FAIL or replaced by a nominal assumption for convenience.

---

## 13. `NaN` Is a Numeric Representation, Not a Scientific Status

`NaN` may appear inside numerical arrays, but it does not explain why the quantity is unavailable.

Candidate rule:

> Scientific result objects shall separate `value` from `status/reason`; the status shall remain meaningful even when the numeric value is absent or nonfinite.

Conceptually:

```text
value: optional
status: typed
reason_code: typed/string
stage: declared
provenance: retained
```

No final class design is accepted here.

---

## 14. Stage-of-Failure Provenance

Failure stage should be recorded because identical final symptoms can arise from different mechanisms.

Candidate stages:

```text
CONFIGURATION
TRUTH_GENERATION
GEOMETRY
MANIFOLD
SOURCE_GENERATION
NOISE_GENERATION
SENSOR_MODEL
ACQUISITION
CALIBRATION
PREPROCESSING
COVARIANCE
EIGENDECOMPOSITION
MODEL_ORDER
ESTIMATION
PEAK_EXTRACTION
ASSOCIATION
METRIC
UNCERTAINTY
HARDWARE_TRANSFER
HARDWARE_KERNEL
POSTPROCESSING
PUBLICATION_EXPORT
```

Candidate rule:

> Failure provenance shall identify the earliest scientifically meaningful stage at which validity was lost, while optionally retaining downstream propagated effects.

---

## 15. Root Cause versus Propagated Failure

One root failure can cause many downstream unavailable quantities.

Example:

```text
covariance contains nonfinite value
 -> eigendecomposition unavailable
 -> MUSIC spectrum unavailable
 -> DOA estimate unavailable
 -> RMSE unavailable
```

Candidate rule:

> GeoDOA shall preserve root cause separately from downstream propagated unavailability to avoid counting one failure multiple times as independent causes.

---

## 16. Error, Warning, and Degradation

Not every diagnostic should invalidate a trial.

Candidate severity classes:

```text
INFO
WARNING
DEGRADED_VALID
FAILURE
INCOMPATIBLE
UNRESOLVED
```

Examples of `DEGRADED_VALID` may include:

- condition number above preferred range but below rejection threshold;
- fixed-point saturation count within declared acceptable budget;
- calibration artifact near edge of validity interval;
- optimizer reached looser fallback tolerance accepted by policy.

Candidate rule:

> Diagnostic severity and scientific validity are related but not identical; the acceptance policy must declare which diagnostics invalidate a result.

---

## 17. Thresholds for Failure Must Be Declared

Examples:

```text
condition-number threshold
PSD tolerance
Hermitian tolerance
maximum allowed saturation count
calibration-age limit
residual norm threshold
optimizer convergence tolerance
```

Candidate rule:

> Failure/degradation thresholds are acceptance policy, not universal mathematical constants, and shall be versioned/provenanced.

No generic `1e-6` failure threshold is accepted globally.

---

## 18. Retry Semantics

Exploration 4.5 requires stable trial identity.

If a trial fails and is retried:

- the same exogenous realization must be preserved;
- retry count and reason must be recorded;
- a successful retry does not erase the original failure event;
- whether retries are allowed in final evidence must be declared.

Candidate rule:

> Retry is an execution-recovery mechanism, not a license to resample until success.

---

## 19. Replacement Trials Are Different Trials

If a failed trial is replaced by a fresh random realization, the replacement has a new scientific trial identity.

Candidate rule:

> Replacement sampling shall not preserve the original trial index while silently changing the realization.

If replacement is used for a fixed number of valid outcomes, the sampling/stopping design must disclose that conditioning.

---

## 20. Selective Failure Deletion Bias

Dropping failed trials can systematically favor fragile methods.

Example:

```text
Method A: 20% numerical failures; RMSE on survivors = 0.2 deg
Method B: 0% failures; RMSE = 0.4 deg
```

Candidate rule:

> Survivor-only metrics shall carry explicit coverage/failure denominators and shall not support unconditional superiority claims by themselves.

---

## 21. Failure Metrics

Useful aggregate failure evidence may include:

```text
probability of any failure
failure rate by stage
failure rate by reason
conditional failure rate by condition
retry rate
incompatibility rate over benchmark domain
unresolved-state rate
degraded-valid rate
```

Candidate rule:

> Failure-rate metrics require the same denominator/uncertainty discipline as other event probabilities.

---

## 22. Failure Denominator Semantics

Possible denominators include:

```text
requested trials
scientifically eligible trials
method-compatible trials
executed trials
hardware transactions
source-level opportunities
```

Candidate rule:

> A generic `failure rate` without its event unit and denominator is incomplete.

---

## 23. Failure and `P_res`

Exploration 4.9 allows different policies.

For a system-level complete-pipeline `P_res`, a method failure on an otherwise eligible trial may count as

\[
R_t=0.
\]

For a conditional valid-output `P_res`, the same failure may be excluded from that conditional denominator while failure probability is reported separately.

Candidate rule:

> The typed failure record is preserved regardless of how a particular metric maps it into its event universe.

---

## 24. Failure and RMSE

By default, numerical failure does not have a natural angular error value.

Candidate rule:

> RMSE shall not silently assign arbitrary angular penalties to numerical/incompatibility failures.

If an application defines a composite loss with explicit failure cost, that loss is a different metric and shall not be called ordinary localization RMSE.

---

## 25. Failure and Fair Comparison

Exploration 4.12 requires symmetric accounting.

Candidate rule:

> Compared methods shall be evaluated under the same failure taxonomy and eligibility policy whenever the scientific meaning permits it.

A method-specific incompatibility may legitimately differ, but it must remain visible rather than being removed from the comparison domain after results are observed.

---

## 26. Data Integrity Failures

Examples:

```text
file checksum mismatch
missing samples
duplicate trial IDs
channel-order mismatch
timestamp discontinuity
truncated artifact
schema/version mismatch
unexpected unit conversion
```

Candidate rule:

> Data-integrity failures shall invalidate affected evidence unless a declared recovery procedure repairs them with preserved provenance.

Silent coercion is forbidden.

---

## 27. Calibration Failures

Calibration-related states may include:

```text
CALIBRATION_MISSING
CALIBRATION_STALE
OUTSIDE_CALIBRATION_DOMAIN
CALIBRATION_MODEL_MISMATCH
CALIBRATION_SOLVE_FAILURE
CALIBRATION_UNCERTAINTY_EXCESSIVE
CALIBRATION_REFERENCE_INVALID
```

Candidate rule:

> Calibration failure shall not be conflated with estimator failure, because the remedy, claim scope, and evidence interpretation differ.

---

## 28. Hardware Failure States

Hardware/SoC studies may require additional states:

```text
DMA_TIMEOUT
FRAME_LENGTH_MISMATCH
STREAM_UNDERRUN
STREAM_OVERRUN
AXI_PROTOCOL_ERROR
CLOCK_DOMAIN_ERROR
BITSTREAM_MISMATCH
FIXED_POINT_OVERFLOW
SATURATION_POLICY_VIOLATION
TIMING_REQUIREMENT_NOT_MET
RESOURCE_LIMIT_EXCEEDED
BOARD_RESET_OR_TRANSPORT_FAILURE
```

Candidate rule:

> Hardware transport/control failures remain distinct from scientific-kernel numerical disagreement.

Exploration 4.15 will define cross-validation consequences.

---

## 29. Deterministic Regression Failure versus Stochastic Trial Failure

A Golden Reference Problem regression mismatch is deterministic verification evidence.

A stochastic Monte Carlo trial failure is an outcome under a probability law.

Candidate rule:

> Deterministic verification failures and stochastic performance failures shall not be aggregated into one generic scientific failure rate.

They belong to different evidence layers.

---

## 30. Test Infrastructure Failure

CI runner outage, missing dependency, disk full, or test harness crash may prevent evidence generation without implying the scientific method failed.

Candidate rule:

> Infrastructure/execution failure shall be distinguishable from method/scientific failure.

Otherwise engineering outages can contaminate algorithm-performance statistics.

---

## 31. Exception Handling Policy

Software exceptions may be appropriate for invalid program states, but publication-grade trial execution should capture scientifically expected failure modes into structured evidence where possible.

Candidate rule:

> Expected domain/numerical failure modes should be translated into typed trial outcomes at a controlled boundary; unexpected programming defects may still raise exceptions and should be classified as implementation defects, not scientific misses.

---

## 32. Programming Bug versus Scientific Failure

A coding bug is not a property of the scientific method.

Examples:

- wrong array indexing;
- stale cache;
- incorrect unit conversion;
- race condition;
- accidental sensor reordering.

Candidate rule:

> Confirmed implementation defects invalidate affected evidence and require rerun/reverification; they shall not be retained as legitimate algorithmic failure-rate samples.

The invalidated run itself remains provenance/history, but not accepted scientific evidence.

---

## 33. Versioned Failure Taxonomy

As GeoDOA grows, failure categories may evolve.

Candidate rule:

> Failure taxonomy and reason codes shall be versioned so historical results remain interpretable.

Merging or renaming statuses later must preserve mapping/provenance.

---

## 34. Human-Readable Reason plus Stable Code

Publication/debugging benefits from both:

```text
stable_reason_code
human_readable_message
```

Candidate rule:

> Human text alone is insufficient for robust aggregation; numeric code alone is insufficient for scientific diagnosis.

No final encoding scheme is accepted here.

---

## 35. Minimal Failure Record

A failure/degraded record should preserve, as applicable:

```text
trial/run identity
method/configuration identity
status class
reason code
severity
stage
root cause
human-readable detail
scientific condition
whether metric-eligible
whether retry attempted
retry identity/count
relevant numerical diagnostics
software/Git version
hardware/calibration/data artifact identity
parent/root failure link if propagated
```

Candidate rule:

> Failure evidence must be traceable to the exact condition and implementation that produced it.

---

## 36. Metric Eligibility Is Separate from Failure Status

One typed outcome can be eligible for some metrics and not others.

Example:

```text
VALID_NO_DETECTION
```

may be:

- eligible for detection probability;
- eligible as `R=0` for unconditional `P_res`;
- not eligible for matched-only localization RMSE.

Candidate rule:

> Metric eligibility shall be determined by the metric contract, not encoded implicitly by one global valid/invalid flag.

---

## 37. No Bare `success: bool`

A single boolean cannot preserve necessary scientific semantics.

Candidate rule:

> GeoDOA shall avoid using a bare `success` flag as the authoritative scientific outcome representation.

A derived convenience boolean may exist, but the typed status/reason remains authoritative.

---

## 38. Failure-State Aggregation Must Preserve Hierarchy

If one device realization causes failures across many repeated noise trials, counting all failures as independent may misrepresent mechanism frequency.

Candidate rule:

> Failure analysis shall preserve hierarchical provenance so device-level, condition-level, and trial-level mechanisms can be distinguished.

This inherits Explorations 4.4 and 4.10.

---

## 39. Failure-State Visualization

Useful diagnostics may include:

```text
failure heatmap over SNR/separation
failure reason histogram
stage-by-condition matrix
per-method incompatibility map
degraded-valid rate versus condition
hardware failure timeline
```

Candidate rule:

> Visualization shall derive from the structured failure record and shall not become the only retained evidence.

---

## 40. Candidate Phase-1 Failure Profile

For initial synthetic Phase-1 DOA studies, a conservative candidate is:

```text
valid estimator result
valid zero-detection
miss / spurious estimate via association
unresolved source group
ambiguous association
method incompatible
outside profile/domain
invalid input/configuration
numerical failure
algorithm nonconvergence
nonfinite result
not assessed / unresolved
```

with:

```text
stable trial identity
stage/reason provenance
no silent replacement realizations
metric-specific eligibility
failure counts reported beside localization/detection/resolution metrics
```

This remains candidate until ADR-004 acceptance.

---

## 41. Invalid / Weak Failure Handling Cases

The following are scientifically weak or invalid unless explicitly justified:

1. drop every `NaN` row before computing metrics with no accounting;
2. convert numerical failure to zero error;
3. convert incompatibility to maximum angular error;
4. treat valid no-detection as solver crash;
5. treat every solver crash as ordinary miss;
6. rerun failed trials with new random realizations until they succeed;
7. keep only successful retries and erase original failure evidence;
8. count downstream propagated failures as independent root causes;
9. classify hard but valid low-SNR trials as invalid input;
10. mark a scientifically ambiguous result as numerical failure;
11. hide method-specific incompatibility by shrinking the benchmark domain post hoc;
12. include confirmed programming-bug outcomes in algorithm failure statistics;
13. use one global `success` boolean as the only evidence state;
14. aggregate device-cluster failures as IID without hierarchical provenance;
15. silently repair corrupt data without recording the repair and original artifact identity.

---

## 42. Cross-ADR Reconciliation

### ADR-001

Aliasing, projection ambiguity, domain boundaries, coordinate validity, and channel identity may create legitimate ambiguity/out-of-domain states rather than numerical failures.

### ADR-002

Rank limitations, snapshot semantics, source coherence, covariance validity, and model-domain assumptions may create compatibility or identifiability states.

### ADR-003

Calibration validity, sensor mismatch, coupling, timing, colored noise, identifiability, and UNRESOLVED compatibility states map naturally into typed failure/degradation evidence.

### ADR-004 Explorations 4.4–4.5

Trial identity persists through failure/retry; retry does not redefine the stochastic realization.

### ADR-004 Explorations 4.6–4.9

Miss, spurious detection, unresolved group, and resolution failure remain evaluation outcomes distinct from computation failures.

### ADR-004 Explorations 4.10–4.12

Failure counts affect adequacy, uncertainty, and fair comparisons and therefore cannot be silently excluded.

**Cross-ADR result: no contradiction identified.**

---

## 43. Candidate Decisions from Exploration 4.13

- **D4.13-01:** Failed, invalid, incompatible, ambiguous, unresolved, missed, and degraded outcomes are typed scientific evidence states, not generic missing values.
- **D4.13-02:** Valid no-detection, missed source, numerical failure, incompatibility, and outside-domain states are distinct.
- **D4.13-03:** `NaN` is not an authoritative scientific status; status/reason and numeric value are separate concepts.
- **D4.13-04:** Failure records preserve stage, root cause, propagated effects, severity, and provenance.
- **D4.13-05:** Difficult valid conditions shall not be mislabeled invalid because a method performs poorly.
- **D4.13-06:** Ambiguity/identifiability states remain distinct from numerical failure.
- **D4.13-07:** `UNRESOLVED` is a legitimate terminal evidence state and shall not be silently promoted to pass/fail.
- **D4.13-08:** Numerical failure taxonomy shall distinguish nonfinite values, singular/ill-conditioned operations, solver failure, nonconvergence, overflow, and policy violations where material.
- **D4.13-09:** Failure/degradation thresholds are versioned acceptance policy, not universal constants.
- **D4.13-10:** Retry preserves the same exogenous trial realization and original failure record; replacement realization is a new trial.
- **D4.13-11:** Survivor-only metrics require coverage/failure reporting and do not establish unconditional performance.
- **D4.13-12:** Failure-rate metrics require explicit event unit, denominator, and uncertainty treatment.
- **D4.13-13:** Ordinary RMSE does not assign universal numeric penalties to failures/incompatibilities.
- **D4.13-14:** Data-integrity, calibration, hardware, infrastructure, deterministic-regression, and stochastic-scientific failures remain distinguishable.
- **D4.13-15:** Confirmed implementation defects invalidate affected scientific evidence rather than becoming algorithm failure samples.
- **D4.13-16:** Failure taxonomy/reason codes shall be versioned and aggregation-safe.
- **D4.13-17:** Metric eligibility is metric-specific and shall not be inferred from one global validity boolean.
- **D4.13-18:** Publication-grade failure records preserve trial/method/condition identity, reason, stage, diagnostics, retry, and software/hardware/calibration provenance.

---

## 44. Exploration 4.13 Conclusion

Exploration 4.13 is complete at candidate-contract level.

The central rule is:

> GeoDOA shall treat every scientifically meaningful non-success state as structured evidence with typed cause, stage, severity, provenance, retry history, and metric-specific eligibility; misses, valid no-detections, ambiguity, incompatibility, out-of-domain conditions, numerical failures, calibration/hardware/data failures, and unresolved states shall remain distinguishable, and no filtering, `NaN` coercion, retry, or arbitrary penalty may erase their scientific meaning.

No acceptance gate is started or passed by this exploration.

The next exploration is:

```text
4.14 — Spectrum / Manifold / Covariance / Eigenspace / DOA Metrics
```
