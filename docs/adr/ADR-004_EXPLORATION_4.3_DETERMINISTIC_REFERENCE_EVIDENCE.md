# ADR-004 Exploration 4.3 — Deterministic Reference Evidence

- **ADR:** ADR-004 — Validation, Reproducibility, and Scientific Evidence
- **Phase:** 0C — Scientific Foundations
- **Exploration:** 4.3
- **Status:** EXPLORATION COMPLETE — CANDIDATE CONTRACT, NOT ACCEPTED
- **Depends on:** Accepted ADR-001, ADR-002, ADR-003; ADR-004 Explorations 4.1 and 4.2
- **Roadmap anchor:** Phase 0C Golden Reference Problem Program and Gate E

## 1. Question

> What evidence may GeoDOA use as a deterministic scientific reference or regression oracle, what makes such evidence trustworthy enough for verification, and how shall analytical, hand-calculated, high-precision numerical, independent-tool, software-reference, and hardware-reference results be distinguished?

This exploration establishes the candidate deterministic-evidence contract needed before stochastic trial semantics, Monte Carlo metrics, and formal Gate-E Golden Reference evidence are defined.

---

## 2. Core Principle

A deterministic reference is not trustworthy merely because it produces a stable number.

A verification oracle must have enough scientific independence, derivation/provenance, semantic clarity, and precision/tolerance definition to support the claim being made.

Candidate rule:

> GeoDOA shall distinguish the **reference result**, the **method used to establish that result**, the **claim it is allowed to verify**, and the **acceptance/tolerance policy used to compare an implementation against it**.

Therefore:

```text
reference value != derivation
reference value != tolerance
reference value != acceptance policy
reference value != physical validation
```

---

## 3. Deterministic Evidence Hierarchy

The following categories are candidate scientific roles, not final software enums.

### 3.1 Analytical / closed-form reference

A result derived algebraically from the accepted scientific contract.

Examples:

- two-sensor steering phase;
- exact rank-one covariance eigenvalues;
- translation-invariant pairwise phase;
- exact projector leakage identity;
- exact bias/variance decomposition for a tiny finite data set.

Strength:

- strongest reference for the bounded mathematical statement when the derivation is correct;
- transparent sign/unit/assumption inspection;
- highly suitable as a regression oracle.

Limitation:

- verifies the declared mathematical model, not physical reality.

### 3.2 Hand-calculated Golden Reference Problem

A deliberately small problem whose inputs, derivation, and expected outputs are independently reproducible with paper, pencil, and a basic calculator.

The Phase 0C roadmap requires such problems for core contracts.

Candidate rule:

> A Golden Reference Problem is a curated analytical verification artifact, not merely a stored expected-output vector.

Its value comes from inspectability and independence from production implementation.

### 3.3 Exact arithmetic / symbolic reference

A result may be representable exactly as an integer, rational, symbolic expression, algebraic identity, or exact matrix relation.

Examples:

```text
rho^2 = 4 / (2 * 2.5) = 0.8
rank-one eigenvalues = {||b||^2, 0}
MSE = variance + bias^2
```

Where exact representation is practical, GeoDOA should preserve it alongside decimal presentation.

### 3.4 High-precision numerical reference

Some accepted equations have no convenient closed-form decimal output, or the relevant reference is a numerically evaluated transcendental quantity.

A high-precision numerical calculation may serve as a deterministic reference if:

- the governing equation is independently established;
- precision exceeds the implementation under test by a material margin;
- the numerical method and precision are recorded;
- convergence/stability is checked where necessary;
- the reference is not produced by the same code path being tested.

High precision supports **numerical verification**, not physical validation.

### 3.5 Independent implementation / cross-tool reference

Agreement with an independently implemented model or another trusted tool may provide strong cross-reference evidence.

Examples:

```text
GeoDOA Python vs independently written MATLAB
NumPy result vs symbolic derivation
custom eigensolver result vs independent library
software floating-point reference vs FPGA output
```

Strength depends on actual independence.

Two wrappers around the same library call are not strong independent evidence simply because they live in different files.

### 3.6 External scientific tool reference

CST, MATLAB, another EM solver, a published implementation, or a laboratory analysis package may be used as external reference evidence when its configuration and semantics are recoverable.

Candidate rule:

> External-tool agreement supports the bounded cross-tool/model-consistency claim; it does not inherit truth status by brand or authority.

### 3.7 Accepted software reference implementation

Once a GeoDOA software kernel has itself passed its governing deterministic verification, it may become a reference for downstream representations such as fixed-point or FPGA implementations.

Example hierarchy:

```text
analytical / GRP reference
        -> verified floating-point kernel
        -> verified fixed-point model
        -> FPGA/SoC implementation
```

The software reference must retain the evidence that established its own authority.

### 3.8 Hardware/reference-instrument deterministic comparison

Hardware may be checked against a deterministic input vector and accepted software/fixed-point reference.

This can verify functional/numerical equivalence for the declared hardware datapath.

It is not by itself physical sensor validation unless the hardware is exercised in a physical experiment with an independent physical reference.

---

## 4. Evidence Strength Is Claim-Specific, Not a Universal Ranking

No single ordering is universally strongest for every claim.

Examples:

- a symbolic derivation is stronger than CST for verifying an algebraic sign identity;
- a calibrated chamber measurement is stronger than a hand calculation for validating an antenna pattern in a real mounting configuration;
- a bit-exact software model may be stronger than floating-point analytical output for verifying an FPGA's internal integer arithmetic;
- a high-precision numerical solver may be required when no practical hand calculation yields the needed decimal reference.

Candidate rule:

> Reference adequacy shall be assessed against the specific verification/validation claim, not by a universal `reference_quality` scalar.

---

## 5. Golden Reference Problem Admissibility

A candidate Golden Reference Problem should satisfy all of the following.

### 5.1 Bounded scope

It exercises one core contract or a small, interpretable composition of contracts.

### 5.2 Small size

It remains independently solvable with paper/pencil/basic calculator, consistent with the Phase 0C roadmap.

### 5.3 Explicit scientific profile

The governing ADR/profile and relevant assumptions are declared.

### 5.4 Explicit inputs

Inputs include units, coordinate/direction semantics, reference planes, channel identities, ordering, and normalization where applicable.

### 5.5 Manually inspectable derivation

The expected result is shown through enough intermediate steps to expose sign, unit, conjugation, indexing, normalization, rank, or approximation mistakes.

### 5.6 Expected outputs

The oracle states exact/symbolic results where practical and decimal results where useful.

### 5.7 Approximation classification

Exact and approximate quantities are labeled separately.

### 5.8 Tolerance rationale

Future software assertions receive a tolerance appropriate to numerical representation and conditioning; the tolerance is not silently promoted to a physical acceptance threshold.

### 5.9 Independence

The expected output is not copied from the production implementation being tested.

### 5.10 Provenance/version identity

The GRP artifact and governing contract revision are recoverable.

### 5.11 Failure interpretation

When relevant, the reference states what kind of mismatch indicates a sign error, unit error, indexing error, approximation violation, numerical tolerance issue, or unsupported profile.

---

## 6. Golden Reference Problem versus Unit Test

A GRP and a software unit test are related but not identical.

### Golden Reference Problem

Scientific artifact containing:

```text
scientific contract
inputs
assumptions
hand derivation
expected result
evidence classification
future oracle semantics
```

### Unit/regression test

Software artifact that executes code and compares outputs against the accepted oracle.

Candidate rule:

> Tests consume Golden Reference evidence; tests do not define the scientific truth of the Golden Reference merely by passing.

A test may be incorrect even when it passes if both implementation and stored expected values share the same error.

---

## 7. Anti-Circularity Rule

Circular verification is a material scientific failure mode.

Examples of weak/circular evidence:

1. run production function;
2. save its output as `expected.npy`;
3. assert future runs equal `expected.npy`;
4. claim the function is scientifically verified.

This only establishes regression stability relative to an earlier implementation.

Candidate rule:

> A frozen production output may be useful as a **regression snapshot**, but it shall not be labeled an independent scientific oracle unless its correctness is established through separate evidence.

The provenance should distinguish:

```text
scientific oracle
cross-tool reference
verified-software reference
regression snapshot
```

---

## 8. Independence Is a Spectrum

Reference independence should be described rather than reduced to a Boolean.

Potential shared-dependency dimensions include:

- same source code;
- same formula transcription;
- same numerical library;
- same data-preprocessing path;
- same calibration artifact;
- same random realization;
- same external solver;
- same hardware measurement chain;
- same sign/unit convention implementation.

Examples:

### Stronger independence

Hand derivation plus separately written implementation.

### Moderate independence

Independent MATLAB implementation using the same documented equation.

### Weaker independence

Two Python functions both calling the same hidden helper/library with identical preprocessing.

Candidate rule:

> Cross-reference evidence shall not claim stronger independence than its dependency structure supports.

---

## 9. Exact, Rounded, and Approximate Expected Values

GeoDOA deterministic evidence shall distinguish at least:

```text
EXACT_SYMBOLIC
EXACT_FINITE_ARITHMETIC
ROUNDED_PRESENTATION_OF_EXACT/DEFINED_QUANTITY
NUMERICALLY_EVALUATED_REFERENCE
MODEL_APPROXIMATION
EMPIRICAL_REFERENCE
```

These are conceptual categories, not final enums.

### 9.1 Exact symbolic

Example:

\[
\Delta\phi=-\pi/2.
\]

### 9.2 Rounded presentation

Example:

\[
\sin^{-1}(0.51)=30.6638297424^\circ
\]

is a decimal presentation of a mathematically defined transcendental result.

### 9.3 Approximation

Example:

\[
\Delta\theta\approx(\delta d/d)\tan\theta_0.
\]

The approximation must never use the same oracle tolerance/interpretation as an exact identity without explicit error policy.

---

## 10. Tolerance Contract

A tolerance is part of the comparison operation, not part of physical truth.

Candidate tolerance sources include:

- floating-point roundoff;
- decimal truncation/rounding of the published reference;
- conditioning/sensitivity of the mathematical operation;
- iterative numerical-solver tolerance;
- fixed-point quantization;
- hardware arithmetic representation;
- explicitly bounded model approximation.

These sources shall not be collapsed into one unexplained epsilon.

### 10.1 Absolute versus relative tolerance

For scalar/matrix comparison, the appropriate metric may involve

\[
|x- x_{\rm ref}|,
\]

\[
\frac{|x-x_{\rm ref}|}{|x_{\rm ref}|},
\]

or a declared norm/projective metric.

The metric must remain scientifically appropriate to units/gauge/scale.

### 10.2 Near-zero references

Pure relative error is unstable/undefined near zero.

An absolute or mixed tolerance may be required.

### 10.3 Condition-sensitive operations

A large forward output deviation can be consistent with a small backward error in an ill-conditioned problem.

Candidate rule:

> Tolerance design may need conditioning-aware evidence; a single global numeric tolerance shall not be presumed valid for every scientific kernel.

### 10.4 Physical acceptance threshold is separate

Example:

```text
software regression tolerance = 1e-12
physical DOA validation threshold = 0.5 deg
```

These answer different questions and must remain separate.

---

## 11. Semantic Oracles, Not Only Numeric Oracles

Some contracts require verifying semantics in addition to numbers.

Examples:

- expected channel identity ordering;
- expected units;
- nominal versus physical manifold role;
- correct sign convention;
- correct reference plane;
- correct compatibility/failure state;
- whether an approximation is allowed;
- whether a result is exact or approximate;
- whether a source is missed rather than assigned an arbitrary angle.

Candidate rule:

> A deterministic verification artifact may include both numeric expected values and expected semantic/status outputs.

This prevents numerically plausible but scientifically misclassified results from passing verification.

---

## 12. Deterministic Failure / Boundary References

Golden Reference evidence need not be limited to successful numerical calculations.

A deterministic test may establish that a scientifically invalid operation must produce a specific failure class.

Examples:

```text
zero-norm projective metric -> undefined/reject
unit-incompatible operator composition -> reject
wideband request under narrowband profile -> incompatible
out-of-domain calibration -> incompatible/warn per accepted policy
```

However, the Phase 0C canonical GRP catalog primarily emphasizes hand-calculated positive/reference problems, while full boundary taxonomy remains Gate F's responsibility.

Candidate rule:

> Deterministic negative/boundary cases may supplement GRPs, but they do not replace Gate-F boundary analysis.

---

## 13. Reference Transformation and Canonicalization

Sometimes a reference must be transformed before comparison.

Examples:

- degrees to radians;
- physical channel order to explicitly mapped processing order;
- scientific frequency sign to FFT-coordinate sign;
- raw manifold to a declared unit-norm view;
- physical covariance to whitened covariance with steering transformed consistently;
- float reference to explicitly quantized fixed-point representation.

Candidate rule:

> A comparison transformation is valid only when it is explicitly governed and provenance-preserving. Silent transformations may make an invalid comparison appear to pass.

The original reference artifact remains immutable/recoverable.

---

## 14. External-Tool Reference Requirements

When external tools are used as deterministic evidence, preserve as applicable:

- tool name/version;
- model/configuration file or immutable identity;
- solver settings;
- coordinate/sign convention mapping;
- units;
- normalization;
- reference plane;
- mesh/tolerance/precision settings where relevant;
- input data identity;
- export transformation;
- tool output selected for comparison;
- known shared assumptions/dependencies with GeoDOA.

For CST specifically, ADR-003's measured/EM manifold provenance rules remain authoritative.

---

## 15. Published Equations and Published Code

A publication is evidence, not an infallible oracle.

Candidate rules:

1. a published equation must be reconciled to GeoDOA's conventions before comparison;
2. a published codebase must preserve version/configuration/input identity;
3. reproducing a published number supports reproduction/cross-reference evidence;
4. disagreement triggers investigation rather than automatically making GeoDOA wrong;
5. publication authority does not override dimensional, sign, or physical contradictions found by accepted ADRs.

---

## 16. Software Reference Promotion

A software implementation may become an accepted downstream reference only through an explicit evidence chain.

Candidate progression:

```text
scientific contract accepted
    -> deterministic analytical/GRP evidence accepted
    -> floating-point implementation reproduces evidence
    -> implementation identity frozen/versioned
    -> floating-point implementation may serve as downstream reference
```

For fixed-point/FPGA:

```text
accepted float reference
    -> fixed-point numerical contract
    -> bit-accurate fixed-point reference
    -> HLS/RTL/FPGA comparison
```

Promotion is scope-specific. Verification of one kernel does not make the entire software stack a universal oracle.

---

## 17. Deterministic Reference Reproducibility

A deterministic reference should be reproducible without hidden mutable state.

Required/candidate provenance as applicable:

- governing ADR/profile revision;
- reference artifact revision;
- complete deterministic inputs;
- units and semantic mappings;
- tool/software versions;
- numerical precision;
- tolerance policy;
- expected outputs;
- derivation/source;
- transformation lineage;
- comparison metric;
- known approximation class.

A deterministic result that depends on unspecified environment/global state is not fully reproducible merely because no random number generator is used.

---

## 18. Golden Reference Catalog Governance

The Phase 0C roadmap reserves canonical GRP identities through GRP-018.

Candidate governance rules:

1. canonical GRP numbers shall not be silently renumbered;
2. corrections preserve change history/revision provenance;
3. material semantic changes require re-audit of dependent software tests;
4. supplemental evidence may use ADR-specific identifiers such as `ADR-004-SRC-*`;
5. a GRP is not `PASS` evidence for an ADR until formal Gate E;
6. exploration seeds/checks remain exploratory until Gate E promotes them;
7. accepted GRP expected values become future regression oracles, not immutable claims immune to correction;
8. if an accepted reference error is discovered, correct it transparently and invalidate/reconcile dependent evidence as needed.

This incorporates the lesson from prior ADR acceptance work: discovering and correcting an oracle transcription error is evidence-system improvement, not a reason to preserve a wrong expected value.

---

## 19. GRP-018 Reservation — Scope Seed Only

The roadmap reserves:

```text
GRP-018 — Bias, Variance, MSE, and RMSE by hand
```

Exploration 4.3 does **not** formalize GRP-018 or assign its final numbers. Those definitions depend on Exploration 4.7.

At this stage, the intended structure is only:

```text
small finite set of deterministic scalar estimates
known reference/truth value
manual sample/finite-set error calculations
bias
variance under explicitly declared denominator/ensemble semantics
MSE
RMSE
identity check linking MSE, variance, and bias^2 where mathematically applicable
```

The exact population/sample/finite-benchmark definitions, denominators, and multi-source extension are intentionally deferred.

Formal GRP-018 evidence belongs to Gate E after the governing ADR stabilizes.

---

## 20. What Deterministic Evidence Can and Cannot Establish

### It can establish, within scope:

- sign correctness;
- algebraic correctness;
- unit consistency;
- transformation correctness;
- implementation agreement with accepted equations;
- deterministic regression behavior;
- fixed-point/hardware equivalence to an accepted reference within a defined tolerance;
- correct failure/status semantics for deterministic boundary cases.

### It cannot establish by itself:

- physical validity of the forward model;
- statistical performance under random conditions;
- Monte Carlo convergence;
- confidence intervals for stochastic metrics;
- generalization outside the reference domain;
- calibration validity outside its domain;
- real-world system accuracy without physical reference evidence.

---

## 21. Failure / Weak-Evidence Cases

The following shall not silently become authoritative deterministic evidence:

1. production output frozen as expected output with no independent correctness evidence;
2. two implementations that secretly share the same core helper presented as independent;
3. a CST/MATLAB result with unknown conventions or configuration;
4. rounded textbook value used with an unjustifiably strict tolerance;
5. approximate formula labeled exact;
6. exact formula tested only against a loose physical threshold;
7. hardware result used as its own reference;
8. reference transformed by silent sorting/normalization/unit conversion;
9. expected value with lost governing ADR/profile identity;
10. a reference derived using oracle information not available to the claimed algorithm without disclosure;
11. comparison near zero using undefined/unstable relative error only;
12. a high-precision computation produced by the exact same implementation path under test;
13. a published value treated as authoritative despite convention mismatch;
14. an accepted GRP changed without dependent-test reconciliation.

---

## 22. Cross-ADR Reconciliation

### ADR-001

Deterministic references inherit coordinate frame, direction, angle, unit, phase-reference, channel-identity, lattice, and sign semantics. A reference in a different convention requires explicit transformation.

### ADR-002

Wave/delay/FFT/FMCW/snapshot/covariance/MIMO references inherit ADR-002 scientific semantics. A raw tensor cannot become a spatial snapshot oracle by shape alone.

### ADR-003

Nominal/physical/measured/EM/calibrated objects remain distinct; reference-plane, included-effects, calibration-domain, and normalization semantics are preserved in deterministic comparisons. CST/measurement evidence does not become physical truth through oracle use.

### ADR-004 Explorations 4.1–4.2

Deterministic evidence is primarily verification/cross-reference evidence. Its truth/reference role and epistemic status inherit Exploration 4.2 provenance rules.

**Cross-contract result: no contradiction identified.**

---

## 23. Candidate Decisions from Exploration 4.3

- **D4.3-01:** A deterministic reference must identify the result, establishment method, allowed claim, and comparison/tolerance policy separately.
- **D4.3-02:** Analytical/closed-form evidence is preferred when practical for bounded mathematical verification.
- **D4.3-03:** Golden Reference Problems are inspectable scientific artifacts, not stored expected-output vectors.
- **D4.3-04:** Every GRP must declare profile, inputs, derivation, expected outputs, approximation class, tolerance rationale, and provenance.
- **D4.3-05:** Tests consume accepted scientific oracles; passing a test does not define the oracle's correctness.
- **D4.3-06:** Frozen production output without independent correctness evidence is a regression snapshot, not an independent scientific oracle.
- **D4.3-07:** Reference independence is dependency-structured and shall not be overstated.
- **D4.3-08:** Exact, rounded, numerically evaluated, approximate, and empirical references remain distinguishable.
- **D4.3-09:** Numerical tolerance and physical/scientific acceptance threshold are distinct.
- **D4.3-10:** Tolerance must reflect numerical representation, conditioning, solver precision, quantization, or declared approximation source rather than one unexplained universal epsilon.
- **D4.3-11:** Deterministic oracles may include semantic/status expectations, not only numeric values.
- **D4.3-12:** Negative deterministic references may supplement GRPs but do not replace Gate-F boundary analysis.
- **D4.3-13:** Reference transformations must be explicit and provenance-preserving.
- **D4.3-14:** External-tool evidence requires version/configuration/convention/unit/reference-plane provenance sufficient for the comparison.
- **D4.3-15:** Published equations/code are evidence requiring convention reconciliation, not truth by authority.
- **D4.3-16:** A verified software implementation may be promoted to a downstream reference only through an explicit, scope-bounded evidence chain.
- **D4.3-17:** Deterministic reproducibility requires explicit inputs/state/tool/precision/tolerance provenance even in the absence of RNG.
- **D4.3-18:** Canonical GRP identities and revisions are governed; corrections require transparent reconciliation of dependent evidence.
- **D4.3-19:** GRP-018 remains reserved but not formalized until metric definitions stabilize and Gate E begins.
- **D4.3-20:** Deterministic verification cannot substitute for Monte Carlo statistical evidence or physical validation.

---

## 24. Exploration 4.3 Conclusion

Exploration 4.3 is complete at candidate-contract level.

The central rule is:

> A GeoDOA deterministic oracle must be scientifically inspectable, semantically typed, provenance-bearing, appropriately independent from the implementation under test, and compared through an explicit metric/tolerance whose meaning is distinct from physical validation or benchmark acceptance.

No formal Golden Reference PASS and no ADR acceptance gate is started by this exploration.

The next exploration is:

```text
4.4 — Random Variables and Trial Semantics
```
