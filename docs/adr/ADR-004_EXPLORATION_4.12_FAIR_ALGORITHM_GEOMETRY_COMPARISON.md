# ADR-004 Exploration 4.12 — Fair Algorithm and Geometry Comparison

- **ADR:** ADR-004 — Validation, Reproducibility, and Scientific Evidence
- **Phase:** 0C — Scientific Foundations
- **Exploration:** 4.12
- **Status:** EXPLORATION COMPLETE — CANDIDATE CONTRACT, NOT ACCEPTED
- **Depends on:** Accepted ADR-001, ADR-002, ADR-003; ADR-004 Explorations 4.1–4.11

## 1. Question

> Under what conditions may GeoDOA legitimately claim that one algorithm, array geometry, calibration strategy, or implementation is better, worse, equivalent, or more efficient than another?

This exploration defines fairness, comparability, tuning, pairing, oracle-information, and trade-space semantics required for scientific benchmarking.

---

## 2. Core Principle

A comparison is scientifically meaningful only when the compared methods are evaluated under a declared comparison contract.

Candidate rule:

> GeoDOA shall not treat two numbers as directly comparable merely because they share a metric name.

At minimum, comparability may depend on:

```text
same scientific question
compatible truth/reference definition
same condition/profile domain
compatible signal/noise/SNR semantics
same trial universe
same association/event semantics
same metric definition/units/weighting
symmetric or explicitly justified tuning policy
explicit oracle-information policy
paired or declared independent stochastic design
failure handling parity
uncertainty on the comparison quantity
computational/hardware resource context
```

---

## 3. Comparison Object Must Be Explicit

GeoDOA may compare:

```text
algorithm vs algorithm
geometry vs geometry
sensor profile vs sensor profile
calibrated vs uncalibrated pipeline
float vs fixed-point vs FPGA implementation
complete system pipeline vs complete system pipeline
```

Candidate rule:

> The comparison object shall be named precisely. A claim about a complete pipeline shall not be restated as if it isolated one algorithmic component unless the experiment actually controlled the other factors.

---

## 4. Same Scientific Question

A fair comparison requires that methods solve the same declared task, or that task differences are explicit.

Examples of non-equivalent tasks:

- Method A receives true source count `K`; Method B estimates `K`.
- Method A receives calibrated manifold; Method B uses nominal manifold.
- Method A searches continuous angle; Method B is restricted to a coarse grid.
- Method A receives whitened data with known `R_n`; Method B does not.

Candidate rule:

> If methods receive different information or solve different inference problems, GeoDOA shall label the comparison accordingly rather than call it a pure algorithm comparison.

---

## 5. Oracle Information Must Be Declared

Oracle information may include:

```text
true source count
true noise variance/covariance
true source covariance
true sensor manifold
true calibration parameters
true SNR
true source ordering/identity
true support sparsity
```

Candidate rule:

> Any use of generative truth as algorithm input shall be declared as oracle information, and oracle-assisted performance shall not be presented as directly equivalent to blind/estimated-input performance.

A valid study may intentionally compare oracle and non-oracle modes, but those modes are different benchmark profiles.

---

## 6. Common Random Numbers for Fair Stochastic Comparison

When methods solve the same stochastic trial, shared exogenous realizations are preferred where scientifically valid.

For trial `t`:

\[
\omega_t^{(A)}=\omega_t^{(B)}
\]

for the physical/source/noise/sensor randomness intended to be common.

Candidate rule:

> Fair algorithm comparison should default to Common Random Numbers for shared exogenous mechanisms while preserving algorithm-internal randomness in separate streams.

This supports paired differences and paired event comparisons.

---

## 7. Same Seed Is Not Sufficient by Itself

Two methods initialized with the same integer seed may still consume different draw sequences.

Candidate rule:

> Pairing shall be established by semantic trial/random-family identity, not inferred from identical seed literals.

This inherits Exploration 4.5.

---

## 8. Condition Matching

Compared methods shall use compatible condition values and semantics.

Examples:

```text
same source DOAs
same source power ratio
same source correlation/coherence
same snapshot count and temporal model
same noise covariance model
same sensor realization when pairing is intended
same carrier/frequency and manifold convention
same calibration state where appropriate
```

Candidate rule:

> Equal parameter names are not sufficient if the underlying semantics differ.

---

## 9. SNR Fairness

SNR is a common source of hidden unfairness.

For example, one study may normalize per-source power while another holds total signal power fixed as source count changes.

Candidate rule:

> Algorithm/geometry comparison shall use the same declared SNR definition and normalization location unless the purpose of the study is specifically to compare different normalization regimes.

For geometry comparisons, per-sensor versus total-array received power normalization shall be explicit.

---

## 10. Geometry Comparison Requires a Resource Constraint

Calling one array geometry `better` is incomplete unless the resource basis is declared.

Possible constraints include:

```text
same number of physical sensors
same physical aperture
same minimum spacing
same maximum aperture
same number of RF channels
same total cost/power budget
same virtual sensor count
same occupied lattice span
same calibration burden
```

Candidate rule:

> Geometry comparison shall declare the constrained resources and the differing resources. A sparse array with larger aperture is not automatically a fair `same-N` comparison to a compact ULA unless aperture is intentionally allowed to differ.

---

## 11. Physical Sensor Count versus Virtual Degrees of Freedom

For coarray/MIMO/sparse geometries, physical sensor count, unique difference lags, virtual aperture, contiguous coarray length, and nominal DOF are different quantities.

Candidate rule:

> GeoDOA shall not compare geometries on one resource axis while silently attributing performance gains to another.

Example:

```text
same physical N but different aperture
```

is a valid study, but the claim must be `performance at fixed physical sensor count`, not `pure geometry gain independent of aperture`.

---

## 12. Search Grid and Postprocessing Fairness

Performance may depend materially on:

```text
search grid
peak threshold
minimum peak spacing
interpolation
model-order rule
spectrum normalization
association gate
resolution-event definition
```

Candidate rule:

> Shared evaluation semantics should be identical across methods when the goal is to compare core estimators. If each method requires a method-specific postprocessor, the comparison is of complete pipelines and shall be labeled as such.

---

## 13. Algorithm-Specific Native Output Is Allowed

Some algorithms naturally output spectra, while others output direct parameter estimates.

Fairness does not require forcing every method through an unnatural identical internal interface.

Candidate rule:

> Methods may use their native estimators, but the downstream evaluation contract—truth association, event semantics, units, eligibility, and reporting—must remain compatible.

---

## 14. Tuning Fairness

Hyperparameters may include:

```text
regularization strength
shrinkage parameter
LASSO lambda
OMP stopping rule
peak threshold
model-order criterion
calibration regularization
fixed-point word length
```

Candidate rule:

> Tuning budgets, tuning data, objective, search space, and final locked values shall be disclosed.

A method tuned extensively on the final benchmark while another uses untouched defaults is not an unbiased algorithm comparison.

---

## 15. Training / Tuning / Final Evaluation Separation

A strong benchmark separates:

```text
exploration / development
calibration / fitting
tuning / hyperparameter selection
locked final evaluation
```

Candidate rule:

> Final benchmark conditions used to support comparative claims shall not be silently reused for post-hoc parameter selection.

If reuse occurs, the result is development/tuning evidence rather than independent final evaluation evidence.

---

## 16. Per-Method Optimal Tuning versus Common Hyperparameter

Two legitimate benchmark philosophies exist.

### 16.1 Common hyperparameter/policy

Useful when comparing methods under one shared operating rule.

### 16.2 Per-method tuned configuration

Useful when comparing each method near its best achievable performance under a symmetric tuning budget.

Candidate rule:

> GeoDOA shall declare which philosophy is used. Neither is universally fair in every study.

---

## 17. Data Leakage / Benchmark Leakage

Examples include:

- using final-test seeds to select a threshold;
- selecting a geometry after seeing final-test ranking;
- selecting only favorable SNR points for the headline claim;
- choosing association gates after inspecting which method wins.

Candidate rule:

> Post-hoc use of final evaluation evidence for design decisions shall be treated as benchmark leakage and disclosed.

---

## 18. Failure Handling Must Be Symmetric

If Method A fails on a trial while Method B succeeds, the trial shall not be removed solely because it harms A.

Candidate rule:

> Failure eligibility and aggregation policy shall be common across methods unless the scientific reason for asymmetry is explicit.

Failed/incompatible states retain their typed provenance.

---

## 19. Matched-Only Metrics Need Coverage Context

Suppose:

```text
A: matched RMSE = 0.2 deg, match coverage = 40%
B: matched RMSE = 0.4 deg, match coverage = 98%
```

Candidate rule:

> A lower success-conditioned RMSE does not establish overall superiority unless coverage/detection/failure outcomes are considered.

Comparative reporting should preserve both localization quality and event success.

---

## 20. Primary and Secondary Metrics

A study may predeclare a primary metric and supporting diagnostics.

Examples:

```text
primary: P_res at fixed separation
secondary: matched RMSE, P_D, false detections, runtime
```

or

```text
primary: RMSE at fixed SNR
secondary: bias, failure rate, memory, latency
```

Candidate rule:

> GeoDOA shall avoid declaring a winner by opportunistically selecting whichever metric favors a preferred method after results are observed.

---

## 21. Multi-Objective Comparison

Scientific and engineering performance may trade off:

```text
RMSE
P_res
failure rate
runtime
latency
throughput
memory
DSP/BRAM/LUT use
power
calibration complexity
sensor count
aperture
```

Candidate rule:

> No universal scalar utility function is imposed. Pareto trade-offs may be more honest than declaring one universal winner.

---

## 22. Pareto Dominance

Method A Pareto-dominates B over a declared metric set if A is no worse on all relevant axes and strictly better on at least one, under compatible uncertainty/decision semantics.

Candidate rule:

> Pareto claims shall declare the metric/resource set and shall not hide omitted axes that materially change the conclusion.

---

## 23. Runtime Fairness

Runtime comparisons require compatible timing scopes.

Possible scopes include:

```text
core numerical kernel only
end-to-end algorithm
including covariance construction
including peak extraction
including host-device transfers
including calibration preprocessing
including initialization/JIT/warm-up
```

Candidate rule:

> Runtime values with different timing scopes are not directly comparable.

Hardware/FPGA timing semantics are elaborated in Exploration 4.15.

---

## 24. Computational Environment Provenance

Runtime/resource results may depend on:

```text
CPU/GPU/FPGA model
clock frequency
thread count
BLAS/library backend
compiler flags
precision
OS/runtime
batch size
memory transfers
warm-up state
```

Candidate rule:

> Computational performance claims require environment provenance sufficient to interpret and reproduce the measurement.

Scientific accuracy comparisons can remain valid across environments when numerical semantics are controlled, but runtime claims cannot.

---

## 25. Complexity Claims versus Measured Runtime

Asymptotic complexity and measured runtime answer different questions.

Candidate rule:

> Big-O complexity, operation count, measured software runtime, and hardware latency/throughput shall remain separate evidence types.

---

## 26. Floating-Point Precision Fairness

If one algorithm uses float64 and another uses float32, observed differences may reflect both algorithm and precision.

Candidate rule:

> Numerical precision shall be controlled or explicitly included as part of the compared pipeline.

The same applies to fixed-point word length and saturation policy.

---

## 27. Preprocessing Fairness

Whitening, smoothing, diagonal loading, covariance shrinkage, spatial smoothing, calibration, normalization, and denoising may materially affect performance.

Candidate rule:

> Shared preprocessing shall be controlled when comparing downstream algorithms. Method-specific preprocessing is allowed only when the comparison is explicitly of full pipelines or the method mathematically requires it.

---

## 28. Geometry-Specific Algorithm Compatibility

Some algorithms exploit structure unavailable to others.

Examples:

- ULA-only ESPRIT assumptions;
- coarray processing for sparse arrays;
- gridless methods with geometry-specific models.

Candidate rule:

> A comparison shall not force an algorithm outside its declared compatibility domain merely to create a nominal head-to-head result.

If a method is incompatible, that is a typed result, not an infinite error or an automatic loss.

---

## 29. Comparison Domain Must Be Shared or Explicitly Restricted

A broad claim such as `A is better than B` requires a declared domain.

Examples:

```text
SNR in [-10,10] dB
snapshots in {20,50,100}
visible sector [-60,60] deg
two incoherent equal-power sources
ideal Phase-1 sensor profile
```

Candidate rule:

> Comparative claims are domain-bounded. Winning on one condition or a narrow selected subset does not establish global superiority.

---

## 30. Aggregate Ranking Can Hide Crossovers

Method A may be better at low SNR while B is better at high SNR.

Candidate rule:

> Condition-resolved curves/surfaces shall be preserved when performance crossovers are material. A single average ranking shall not replace the underlying interaction unless the weighting distribution is part of the target claim.

---

## 31. Macro versus Micro Benchmark Weighting

If conditions have unequal trial counts, micro averaging weights heavily sampled conditions more.

Candidate rule:

> Aggregate benchmark weighting shall represent the intended deployment/study distribution and be explicit.

Equal-condition macro weighting and distribution-weighted micro aggregation answer different questions.

---

## 32. Comparative Quantity and Uncertainty

For paired scalar trial metrics:

\[
D_t=M_t^{(A)}-M_t^{(B)}.
\]

For paired binary events:

\[
R_t^{(A)},R_t^{(B)}
\]

retain discordant outcomes.

Candidate rule:

> Comparison uncertainty shall target the difference/ratio/contrast itself, not be inferred from separate marginal error bars.

This inherits Exploration 4.11.

---

## 33. Statistical Significance Is Not a Winner Declaration

A tiny statistically clear difference may be practically irrelevant.

Candidate rule:

> GeoDOA shall pair uncertainty evidence with an engineering/practical effect-size interpretation when making superiority claims.

---

## 34. Superiority, Noninferiority, and Equivalence

Candidate comparison claim classes:

```text
SUPERIOR within domain D by declared metric/effect
NONINFERIOR within margin delta
EQUIVALENT within margin delta
TRADEOFF / PARETO-NONDOMINATED
INCONCLUSIVE given current uncertainty
INCOMPATIBLE comparison
NOT_ASSESSED
```

These are conceptual statuses, not final software enums.

Candidate rule:

> `No significant difference` shall not be promoted to `equivalent`; equivalence/noninferiority requires a predeclared practical margin.

---

## 35. Effect Size

Absolute differences often remain more interpretable than percentages.

Examples:

```text
RMSE difference = -0.12 deg
P_res difference = +0.08
latency difference = -3.5 us
```

Relative improvement may also be reported:

\[
\frac{M_B-M_A}{M_B},
\]

when meaningful and denominator-stable.

Candidate rule:

> Relative percentage improvement shall not replace the underlying absolute metric/effect and denominator provenance.

---

## 36. Baseline Selection

The baseline should be scientifically justified.

Possible baselines:

```text
canonical Bartlett/MVDR/MUSIC
published reference method
accepted prior GeoDOA method
nominal ULA geometry
floating-point scientific reference
```

Candidate rule:

> A weak straw-man baseline does not support a strong superiority claim over the state of practice.

Baseline identity/version/configuration is provenance.

---

## 37. External Published Baselines

Reproducing literature results requires compatibility checks for:

```text
array geometry
source model
SNR definition
snapshots
search grid
metric definition
association
failure handling
normalization
parameter tuning
```

Candidate rule:

> A copied headline number from a paper is not directly comparable unless the benchmark contracts are compatible.

---

## 38. Geometry Fairness Example

Suppose Geometry A and B each use `N=8` physical sensors, but A spans `7 lambda/2` while B spans `14 lambda/2`.

If A has RMSE 1.0 deg and B has 0.6 deg, a valid statement may be:

```text
At fixed physical sensor count N=8, Geometry B achieved lower RMSE under the tested profile.
```

But it is not justified to conclude:

```text
Geometry B's topology alone is superior independent of aperture.
```

Candidate rule:

> Resource-controlled wording shall track what was actually held fixed.

---

## 39. Algorithm Fairness Example

Suppose MUSIC uses true `K=2`, while another method estimates model order and sometimes returns one or three sources.

Candidate interpretation:

```text
MUSIC-oracle-K localization performance
vs
blind complete-pipeline performance
```

not

```text
pure algorithm accuracy comparison
```

unless both are placed under compatible model-order assumptions.

---

## 40. Calibration Fairness Example

Comparing nominal-manifold MUSIC against measured-manifold MUSIC is a valid pipeline comparison.

But the observed gain reflects both:

```text
manifold/calibration information
and
estimator behavior under that information
```

Candidate rule:

> GeoDOA shall not attribute full pipeline gains exclusively to the estimator when calibration/model fidelity changed simultaneously.

---

## 41. Hardware Comparison Fairness

Float/fixed/FPGA comparisons should distinguish:

```text
scientific equivalence/degradation
latency
throughput/II
resource use
power, if measured
host-transfer overhead
```

Candidate rule:

> Hardware acceleration claims shall compare complete and explicitly scoped timing paths and preserve the accepted scientific reference as the accuracy baseline.

Detailed hardware cross-validation is deferred to 4.15.

---

## 42. Reproducible Comparison Record

A publication-grade comparison should preserve, as applicable:

```text
comparison id/version
methods/geometries and versions
scientific task/domain
resource constraints
truth/reference profile
condition grid/distribution
oracle information
preprocessing
search/postprocessing
association/event/metric policies
tuning protocol and budget
locked hyperparameters
root seed / CRN pairing
trial counts/failure policy
aggregation weighting
point estimates
effect sizes
comparison uncertainty
runtime/resource environment
baseline identity
claim status and scope
```

Candidate rule:

> Comparative claims shall be reconstructable from the exact benchmark contract and trial-level evidence.

---

## 43. Candidate Phase-1 Fair-Comparison Profile

For initial GeoDOA synthetic studies:

```text
same accepted Phase-1 physical/signal/sensor profile
same exact truth conditions
same exogenous trial realizations via CRN
same SNR/snapshot/source semantics
same evaluation association and metrics
same failure accounting
oracle-K status explicit and harmonized when possible
search/postprocessing harmonized unless comparing full pipelines
hyperparameters locked before final benchmark
condition-level results preserved
paired effect/uncertainty retained
geometry comparisons declare physical N/aperture/resource constraints
runtime reported separately with environment provenance
```

This remains candidate until ADR-004 acceptance.

---

## 44. Invalid / Weak Fairness Cases

The following are scientifically weak or invalid unless explicitly justified:

1. compare algorithms on different noise/source realizations and call small differences decisive;
2. give one method oracle `K` but not disclose it;
3. tune one method on final test conditions and leave another untuned;
4. change SNR definition between methods/geometries;
5. compare geometry performance without stating sensor-count/aperture constraints;
6. hide increased aperture while attributing all gains to sparse topology;
7. use different association/failure rules for each algorithm;
8. report only matched RMSE while suppressing method-specific miss rates;
9. choose the headline metric after observing which method wins;
10. compare runtime with different timing scopes;
11. compare literature headline numbers under incompatible benchmark semantics;
12. declare equivalence because a difference was not statistically detected;
13. declare universal superiority from one SNR/angle/separation condition;
14. average away material performance crossovers;
15. call a full-pipeline calibration improvement a pure estimator improvement;
16. compare one method in float64 against another in fixed/float32 without treating precision as part of the pipeline;
17. silently exclude a method's difficult failed trials;
18. use a weak straw-man baseline to imply state-of-the-art superiority.

---

## 45. Cross-ADR Reconciliation

### ADR-001

Geometry comparisons inherit physical positions, aperture, coordinate/direction conventions, stable channel identity, and no-silent-normalization rules.

### ADR-002

Signal/SNR/snapshot/source-correlation semantics define comparable trial conditions.

### ADR-003

Sensor, coupling, calibration, noise, timing, and compatibility profiles must be matched or explicitly varied as part of the comparison object.

### ADR-004 Explorations 4.4–4.5

Fair stochastic comparisons preserve trial identity and Common Random Numbers where appropriate.

### ADR-004 Explorations 4.6–4.9

Association, localization, detection, and resolution semantics are shared evaluation contracts.

### ADR-004 Explorations 4.10–4.11

Adequacy and uncertainty target the actual comparison quantity, not only each marginal method metric.

**Cross-ADR result: no contradiction identified.**

---

## 46. Candidate Decisions from Exploration 4.12

- **D4.12-01:** A fair comparison requires an explicit comparison contract; equal metric labels alone do not establish comparability.
- **D4.12-02:** Compared methods must solve the same scientific task or task/information differences must be explicit.
- **D4.12-03:** Oracle information shall be disclosed and harmonized when a pure algorithm comparison is intended.
- **D4.12-04:** Common Random Numbers are the preferred default for shared exogenous stochastic mechanisms in paired comparisons.
- **D4.12-05:** SNR, source/noise/snapshot, truth, sensor, association, failure, and metric semantics shall be compatible across compared methods.
- **D4.12-06:** Geometry comparisons shall declare the resource constraint set, including physical sensor count and aperture where material.
- **D4.12-07:** Physical sensor count, virtual DOF, coarray size, and aperture are distinct comparison resources.
- **D4.12-08:** Shared postprocessing should be harmonized for core-estimator comparison; method-specific postprocessing implies complete-pipeline comparison.
- **D4.12-09:** Tuning data, search budget, objective, and locked hyperparameters are benchmark provenance; final-test leakage shall be disclosed.
- **D4.12-10:** Common-parameter and per-method-optimal tuning are distinct legitimate benchmark philosophies and shall be declared.
- **D4.12-11:** Failure and eligibility handling shall be symmetric unless asymmetry is scientifically justified.
- **D4.12-12:** Matched-only localization superiority shall not ignore detection/failure coverage.
- **D4.12-13:** Multi-objective scientific/engineering trade-offs may require Pareto reporting rather than a universal winner.
- **D4.12-14:** Runtime, asymptotic complexity, operation count, latency, throughput, and resource use are distinct evidence types with explicit scope/environment.
- **D4.12-15:** Preprocessing and numerical precision shall be controlled or explicitly included in the compared pipeline.
- **D4.12-16:** Incompatible methods are typed as such rather than coerced into numeric losses.
- **D4.12-17:** Comparative claims are domain-bounded and shall preserve condition-wise crossovers when material.
- **D4.12-18:** Aggregate benchmark weighting shall represent an explicit target distribution/policy.
- **D4.12-19:** Uncertainty shall target the comparative effect itself; statistical significance and engineering significance remain distinct.
- **D4.12-20:** Superiority, noninferiority, equivalence, tradeoff, inconclusive, and incompatible are distinct claim classes.
- **D4.12-21:** Relative improvement percentages shall accompany, not replace, absolute metrics/effects.
- **D4.12-22:** Baseline identity/configuration and external-study compatibility are part of comparative provenance.
- **D4.12-23:** Gains caused jointly by calibration/model changes and estimation shall not be attributed solely to the estimator.
- **D4.12-24:** Publication-grade comparison records preserve task, resources, tuning, trials, pairing, metrics, uncertainty, environment, and claim scope.

---

## 47. Exploration 4.12 Conclusion

Exploration 4.12 is complete at candidate-contract level.

The central rule is:

> GeoDOA shall call one algorithm, geometry, or implementation better than another only under an explicit domain-bounded comparison contract that controls or declares truth, stochastic realizations, SNR/signal/sensor semantics, oracle information, preprocessing, tuning, evaluation policy, failure handling, resource constraints, and computational scope; comparative uncertainty shall target the effect itself, and engineering trade-offs shall not be hidden behind a single opportunistic winner metric.

No acceptance gate is started or passed by this exploration.

The next exploration is:

```text
4.13 — Failure-State Recording
```
