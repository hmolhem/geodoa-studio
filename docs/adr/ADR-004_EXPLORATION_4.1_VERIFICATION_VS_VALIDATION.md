# ADR-004 — Exploration 4.1: Verification vs Validation

- **ADR:** ADR-004 — Validation, Reproducibility, and Scientific Evidence
- **Phase:** 0C — Scientific Foundations
- **Exploration:** 4.1
- **Status:** EXPLORATION COMPLETE — CANDIDATE TERMINOLOGY, NOT ACCEPTED
- **Depends on:** Accepted ADR-001, ADR-002, ADR-003

## 1. Primary Question

> What distinct evidence claims shall GeoDOA use for mathematical/software verification, numerical cross-reference agreement, physical validation, hardware cross-validation, reproducibility, and comparative performance?

The core requirement is that GeoDOA must never use the word `validated` as a generic synonym for `seems correct`.

---

## 2. Governing Distinction

GeoDOA shall distinguish at least the following evidence questions:

```text
Did we formulate the intended model consistently?
        -> scientific/model verification

Did the implementation reproduce the governing equations/reference values?
        -> implementation verification

Does an independent numerical implementation/tool agree under matched assumptions?
        -> numerical cross-reference verification

Does the model predict/represent the physical system within a declared domain and uncertainty?
        -> physical validation

Does a fixed-point/FPGA implementation preserve the accepted scientific behavior within a declared tolerance?
        -> implementation cross-validation / equivalence evidence

Can another run reconstruct the result from recorded configuration/data/software/seeds?
        -> reproducibility

Is method A better than method B under a fair declared benchmark and uncertainty analysis?
        -> comparative evidence
```

These questions are related but not interchangeable.

---

## 3. Verification

### 3.1 Scientific/model verification

Scientific/model verification asks whether a mathematical/scientific construction is internally consistent with the governing contract.

Examples:

- ADR-001 steering sign follows from the accepted temporal convention and propagation direction;
- ADR-002 covariance rank statement follows from linear algebra;
- ADR-003 coupling covariance uses `C R C^H` for the declared linear transform;
- a narrowband approximation is used only inside its declared approximation domain.

Evidence may include:

- derivation;
- dimensional analysis;
- invariance checks;
- limiting cases;
- hand-calculated Golden Reference Problems;
- theorem-condition checks.

Scientific/model verification does **not** establish that the model accurately represents a real sensor.

### 3.2 Software implementation verification

Implementation verification asks whether code implements the accepted scientific specification correctly.

Examples:

- steering kernel reproduces GRP-001/002 values;
- covariance routine reproduces GRP-011/013;
- sensor mismatch kernel reproduces GRP-014–017;
- deterministic seed mapping reconstructs the same trial.

Typical evidence:

```text
unit tests
property/invariance tests
Golden Reference regression tests
independent hand calculation
known limiting cases
numerical tolerance audit
```

The canonical question is:

> Are we solving the equations right?

---

## 4. Numerical Cross-Reference Verification

A second implementation or external numerical tool may provide cross-reference evidence.

Examples:

- Python versus MATLAB;
- NumPy versus an independently implemented direct formula;
- floating-point software versus fixed-point emulator;
- GeoDOA manifold versus a separately exported/reference-processed CST manifold under matched conventions.

Cross-reference agreement is useful because independent implementations may expose implementation mistakes.

However:

\[
\boxed{\text{agreement between two codes is not automatically physical validation}.}
\]

Two implementations can agree while sharing the same wrong assumption, convention, normalization, or reference plane.

Therefore cross-reference evidence requires matched declaration of:

- governing physical model;
- units;
- sign conventions;
- normalization;
- reference planes;
- input data;
- numerical precision;
- tolerances.

---

## 5. Physical Validation

Physical validation asks whether the model/algorithm provides an adequate representation of physical reality for a declared intended-use domain.

The canonical question is:

> Are we solving the right physical model well enough for the declared use?

Potential evidence sources include:

- calibrated laboratory measurements;
- known-angle source measurements;
- antenna chamber data;
- measured channel/manifold data;
- controlled hardware experiments;
- comparison against independently characterized physical standards.

Physical validation must declare:

```text
validation quantity
physical reference/ground truth
measurement setup
instrumentation/calibration
environment/state
uncertainty
validity domain
acceptance metric
acceptance policy
```

A validation statement without a declared domain is incomplete.

Example:

```text
VALIDATED:
DOA bias < 0.5 deg for theta in [-40,40] deg,
SNR >= 10 dB,
3 GHz chamber calibration state C17,
95% confidence under the declared experiment.
```

is fundamentally stronger and more precise than:

```text
The algorithm was validated experimentally.
```

---

## 6. Analytical Reference Evidence

A deterministic analytical reference can establish verification evidence when its assumptions match the implementation profile.

Golden Reference Problems are therefore primarily **verification artifacts**.

They may also support validation indirectly, for example by validating a measurement/calibration pipeline against a physically traceable analytical setup, but a hand calculation alone does not generally establish real-world validity.

Normative distinction:

```text
Golden Reference match -> verification evidence
Measured physical agreement -> validation evidence
```

---

## 7. External-Tool Evidence

External tools can play different roles and must be labeled by role.

### 7.1 Independent numerical reference

Example: MATLAB implementation of the same equations.

Classification:

```text
numerical cross-reference verification
```

### 7.2 Physics-based simulation reference

Example: CST full-wave manifold.

Classification:

```text
external physics-model evidence / numerical validation against another model
```

It is not automatically measured physical truth.

### 7.3 Measurement/instrument reference

Example: calibrated VNA/channel/manifold measurement.

Classification:

```text
physical validation evidence
```

subject to measurement uncertainty and calibration provenance.

---

## 8. Hardware Evidence

FPGA/SoC evidence shall be separated into at least three questions.

### 8.1 Functional equivalence

Does the hardware compute the intended algorithm?

Compare against the accepted software/floating scientific reference using identical input vectors.

This is implementation verification/cross-validation.

### 8.2 Numerical degradation

How much scientific error is introduced by:

```text
fixed-point quantization
rounding
saturation
finite word length
pipeline reordering
approximate arithmetic
```

This requires output-level scientific metrics, not just bitwise comparison.

Examples:

- covariance Frobenius error;
- eigenspace principal angle;
- MUSIC spectrum error;
- DOA bias/RMSE degradation.

### 8.3 Hardware/system validation

Does the deployed system behave correctly with real acquisition/timing/interfaces?

This includes:

- AXI/DMA correctness;
- sample/channel ordering;
- latency alignment;
- saturation/overflow state;
- board-level acquisition;
- real sensor data where applicable.

A hardware kernel matching software vectors does not by itself validate the complete physical sensing system.

---

## 9. Reproducibility

Reproducibility is independent of verification/validation status.

A wrong result can be perfectly reproducible.

A physically validated result can be impossible to reproduce if provenance is missing.

Therefore:

\[
\boxed{\text{reproducibility is necessary evidence quality, not correctness by itself}.}
\]

GeoDOA reproducibility shall eventually require recoverable identity for:

- input data/artifact;
- configuration;
- scientific profile;
- calibration state;
- algorithm/version;
- random seed hierarchy;
- software/Git revision;
- numerical backend;
- warnings/failure status.

Detailed run identity is deferred to Exploration 4.16.

---

## 10. Repeatability, Reproducibility, Replicability

Terminology varies across disciplines. GeoDOA should avoid relying on ambiguous words without an operational definition.

Candidate operational vocabulary:

### Repeatability

Same implementation/environment/configuration/data/seeds reproduces the same deterministic or statistically equivalent result.

### Reproducibility

A recorded run can be reconstructed from preserved artifacts/configuration/software/provenance sufficiently to reproduce the scientific evidence.

### Independent replication

An independently constructed experiment or implementation reaches a statistically/scientifically consistent conclusion.

Final naming should be reconciled with ADR-004 publication/provenance requirements before acceptance.

---

## 11. Accuracy, Verification, and Validation Are Distinct

A numerical result can be:

```text
verified but physically invalid
unverified but accidentally close to truth
validated over one domain but invalid outside it
reproducible but wrong
accurate on average but high variance
low RMSE but high failure/miss rate due to conditional reporting
```

Therefore no single `validated=True` flag can represent scientific evidence.

---

## 12. Calibration Is Not Validation

Accepted ADR-003 already separates calibration from causation and validation.

ADR-004 inherits:

```text
calibration -> estimate/correct model or data
validation  -> independently assess adequacy/performance
```

Using the same data both to fit calibration parameters and to claim validation can create optimistic bias.

Candidate rule:

> Validation evidence should be independent of calibration/training evidence whenever the scientific claim depends on generalization beyond the calibration observations.

Possible mechanisms:

- held-out directions;
- held-out frequencies;
- held-out runs;
- separate measurement sessions;
- independent physical reference.

The exact independence policy is experiment-specific and shall be recorded.

---

## 13. Training/Tuning Is Not Validation

An algorithm parameter chosen to optimize a benchmark condition cannot use the same evidence as an unbiased final evaluation without disclosure.

GeoDOA shall distinguish:

```text
training/fitting
parameter selection/tuning
calibration
exploration
validation/evaluation
final locked benchmark
```

This distinction is particularly important for:

- shrinkage parameters;
- threshold selection;
- model-order criteria;
- peak-detection settings;
- calibration regularization;
- fixed-point word-length selection.

Detailed fair benchmarking is deferred to Exploration 4.12.

---

## 14. Benchmark Agreement Does Not Prove General Validity

Passing one benchmark establishes evidence only for the benchmark's declared domain.

A result such as

```text
Algorithm A improves RMSE by 12% over B
```

is incomplete unless accompanied by:

- benchmark conditions;
- truth definition;
- failure handling;
- trial count;
- uncertainty;
- fairness policy;
- tuning status;
- seed/randomization policy;
- scope of generalization.

Thus ADR-004 shall prohibit universal performance claims from undeclared benchmark scope.

---

## 15. Candidate Evidence Hierarchy

GeoDOA may use the following evidence hierarchy, not as a universal ranking of scientific value but as distinct evidence classes:

```text
E0 — definition/contract evidence
E1 — analytical/Golden Reference verification
E2 — software regression/property verification
E3 — independent numerical cross-reference
E4 — external physics-model comparison
E5 — controlled measured physical validation
E6 — deployed hardware/system validation
E7 — independent replication / cross-lab evidence
```

Important:

- higher number does not replace lower-level verification;
- physical validation does not excuse incorrect software implementation;
- exact Golden Reference verification does not prove physical realism;
- evidence classes should be attached to a claim, not treated as a single project-wide badge.

Final evidence-class naming remains candidate until cross-section reconciliation.

---

## 16. Claim Object Concept

A future GeoDOA evidence record should conceptually bind:

```text
claim
scope/domain
method/profile
metric
reference/truth
acceptance policy
observed result
uncertainty
provenance
supporting artifacts
evidence class
status
```

Example conceptual claim:

```text
Claim:
Fixed-point MUSIC backend reproduces floating reference DOA
within 0.10 deg for validation vector set V3.

Evidence:
E1/E2 + hardware cross-validation

Domain:
PM-001, Phase-1 ideal sensor profile, N=8, one source,
SNR >= 10 dB, declared scan grid.
```

This concept prevents evidence from being detached from the exact claim it supports.

---

## 17. Acceptance Policy Is Separate from Metric

A metric answers:

> What discrepancy/performance quantity did we compute?

An acceptance policy answers:

> What result is considered sufficient for this intended use?

For example:

\[
\mathrm{RMSE}=0.42^\circ
\]

is a measurement/result.

The statement

\[
\mathrm{RMSE}<0.5^\circ
\]

is an acceptance criterion.

ADR-004 shall never embed an undeclared universal threshold into a generic metric implementation.

---

## 18. Failure Evidence Is Evidence

A failed validation case is not missing data by default.

Examples:

```text
no peak returned
wrong model order
numerical solver failure
clipping detected
calibration outside domain
FPGA overflow
incompatible profile
```

These outcomes must be preserved as trial/evidence states and not silently removed from aggregate results.

Detailed failure-state semantics are deferred to Exploration 4.13.

---

## 19. Candidate Core Decisions from 4.1

### D4.1-01
Verification and physical validation are distinct evidence claims.

### D4.1-02
Scientific/model verification and implementation verification are distinct but complementary.

### D4.1-03
Agreement between two implementations/tools is numerical cross-reference evidence, not automatically physical validation.

### D4.1-04
Golden Reference Problems are primarily deterministic verification evidence.

### D4.1-05
Measured physical agreement requires declared validation quantity, physical reference, setup, uncertainty, domain, metric, and acceptance policy.

### D4.1-06
Calibration/training/tuning evidence shall not be silently reused as independent validation evidence.

### D4.1-07
Reproducibility is an evidence-quality property, not proof of correctness.

### D4.1-08
Hardware evidence shall distinguish functional equivalence, numerical degradation, and physical/system validation.

### D4.1-09
Metric computation and acceptance policy are separate scientific objects.

### D4.1-10
Evidence shall attach to a scoped claim; GeoDOA shall avoid a project-wide generic `validated=True` state.

### D4.1-11
Failed/incompatible validation outcomes are evidence states and shall not be silently dropped.

### D4.1-12
Validation statements are domain-bounded; benchmark success does not establish universal validity.

---

## 20. Open Questions Deferred

The following are intentionally deferred:

- exact truth/provenance object taxonomy -> 4.2;
- formal deterministic evidence contract -> 4.3;
- Monte Carlo trial identity -> 4.4;
- seed hierarchy -> 4.5;
- multi-source matching -> 4.6;
- estimator metrics -> 4.7–4.9;
- confidence intervals -> 4.11;
- fairness/tuning separation -> 4.12;
- exact failure-state enum/taxonomy -> 4.13;
- hardware metric set and float/fixed tolerances -> 4.15;
- run identity schema -> 4.16;
- publication artifact bundle -> 4.17.

No deferred item blocks completion of Exploration 4.1.

---

## 21. Exploration 4.1 Conclusion

The foundational evidence distinction is:

\[
\boxed{
\text{Verification asks whether the declared model/implementation is executed correctly;}
}
\]

\[
\boxed{
\text{Validation asks whether that model/system is adequate for the declared physical intended-use domain.}
}
\]

Numerical agreement, reproducibility, benchmarking, and hardware equivalence are additional evidence dimensions and must not be collapsed into either term without qualification.

**Exploration 4.1 status: COMPLETE — candidate decisions recorded, not accepted.**
