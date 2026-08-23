# ADR-004 — Validation, Reproducibility, and Scientific Evidence

- **Status:** Accepted — all Phase 0C acceptance Gates A–F and final cross-gate reconciliation passed
- **Phase:** 0C — Scientific Foundations
- **Scope:** Verification, physical validation, truth/reference provenance, stochastic experiments, metrics, uncertainty, fair comparison, failure-state evidence, float/fixed/FPGA cross-validation, run provenance, publication reproducibility, and the initial VP-001 validation profile
- **Depends on:** `ADR-001-coordinate-direction-spatial-conventions.md`, `ADR-002-wave-propagation-signal-measurement-model.md`, `ADR-003-sensor-imperfections-mutual-coupling-calibration.md`, `PHASE0C_SCIENTIFIC_CONTRACTS_ROADMAP.md`
- **Exploration record:** `ADR-004_EXPLORATION_CHECKPOINT.md` and dedicated Explorations 4.1–4.20
- **Cross-section reconciliation:** `ADR-004_EXPLORATION_4.20_CROSS_SECTION_RECONCILIATION.md`
- **Pre-Gate review:** `ADR-004_PRE_GATE_CONSISTENCY_REVIEW.md` — PASS
- **Gate audits:** `ADR-004_GATE_A_AUDIT.md` through `ADR-004_GATE_F_AUDIT.md` — PASS
- **Golden Reference evidence:** `../science/golden_reference/ADR-004_GOLDEN_REFERENCE_PROBLEMS.md` — GRP-018 PASS
- **Boundary/failure evidence:** `ADR-004_BOUNDARY_FAILURE_ANALYSIS.md`
- **Final cross-gate reconciliation:** `ADR-004_FINAL_CROSS_GATE_RECONCILIATION.md` — PASS
- **Final acceptance record:** `ADR-004_FINAL_ACCEPTANCE_RECORD.md`
- **Supersedes:** None
- **Superseded by:** None

> ADR-004 is **Accepted**. Its normative F1–F14 scientific evidence contract passed the dedicated pre-Gate review, Gates A–F, formal Golden Reference evidence, boundary/failure analysis, and final cross-gate reconciliation. Authoritative Phase-1 implementation may now consume this contract; implementation itself remains subject to independent verification and acceptance.

---

## 1. Decision Summary

GeoDOA Studio shall treat scientific evidence as a typed, layered, provenance-preserving system.

The governing evidence chain is:

```text
accepted physical/statistical model
    -> deterministic verification
    -> verified software reference
    -> declared stochastic experiment
    -> typed estimator/trial outcomes
    -> association / detection / resolution / localization metrics
    -> adequacy + uncertainty
    -> fair comparison / engineering interpretation
    -> float/fixed/HLS/RTL/FPGA cross-validation where applicable
    -> immutable run/provenance record
    -> publication/reproducibility package
```

ADR-004 does **not** redefine the scientific semantics owned by ADR-001, ADR-002, or ADR-003. It defines how evidence about those semantics is generated, scored, compared, qualified, reproduced, and published.

The initial executable validation profile is:

```text
VP-001 — Phase-1 Ideal Far-Field Narrowband 1-D DOA Validation Profile
```

VP-001 is intentionally narrow and establishes the software/scientific reference baseline before real sensor imperfections, colored noise, measured manifolds, wideband/near-field behavior, unknown model order, or physical-array validation are introduced.

---

## 2. Context and Decision Drivers

A DOA result is scientifically incomplete if the project cannot answer:

```text
What model/profile generated the evidence?
What was truth and what was only a reference?
Which stochastic realization was used?
How were multiple estimated sources associated to truth?
How were misses, failures, ambiguities, and incompatibilities handled?
Which denominator produced P_D or P_res?
How adequate was the Monte Carlo evidence?
What uncertainty belongs to the reported metric or comparison?
Was one method given oracle information or a larger tuning budget?
Did a fixed-point/FPGA result preserve the accepted scientific reference?
Which Git/config/data/calibration/build state produced the figure or table?
Can the result be reconstructed or reproduced?
```

Without a formal evidence contract, scientifically different studies can produce superficially comparable numbers, failed trials can disappear through filtering, hardware agreement can be mistaken for physical validation, and publication figures can become detached from their generating conditions.

ADR-004 therefore locks evidence semantics before Phase 1 authoritative implementation.

---

## 3. Scope and Authority

### 3.1 ADR authority

ADR-004 inherits without redefining:

```text
ADR-001 -> geometry, coordinate, direction, receive phase, phase reference,
           physical positions, channel identity
ADR-002 -> propagation, snapshots, source/noise statistics, covariance objects,
           rank, SNR, MIMO physical-channel provenance
ADR-003 -> sensor/receiver imperfections, calibration, reference planes,
           compatibility, identifiability, ADC quantization, measured/EM manifolds
```

ADR-004 governs:

- evidence-role vocabulary;
- truth/reference provenance;
- deterministic verification evidence;
- study/condition/trial/randomness semantics;
- truth-to-estimate association;
- detection/miss/spurious/resolution semantics;
- bias/variance/MSE/RMSE and event-probability metrics;
- Monte Carlo adequacy and uncertainty;
- fair algorithm/geometry/pipeline comparison;
- typed failure, ambiguity, incompatibility, and metric eligibility;
- multi-level scientific diagnostic metrics;
- floating/fixed/HLS/RTL/FPGA cross-validation;
- run/config/data/calibration/software/hardware provenance;
- immutable publication/reproducibility evidence;
- the bounded initial VP-001 validation profile.

### 3.2 Explicit non-goals

ADR-004 does not define one universal:

```text
association gate
search-grid spacing
peak threshold
Monte Carlo trial count
confidence level
RMSE threshold
P_res target
fixed-point word length
FPGA latency/resource target
condition-number cutoff
calibration tolerance
Python enum/class/schema
artifact archive service
```

Such values belong to named study, validation, engineering, or implementation profiles.

---

## 4. F1 — Evidence-Role Separation

The following evidence roles are distinct.

### 4.1 Verification

Evidence that an analytical, numerical, software, or implementation object correctly realizes a declared model, specification, or accepted reference.

### 4.2 Physical validation

Evidence comparing a model/system against physical reality or a traceable physical reference within a declared domain and uncertainty model.

### 4.3 Calibration

Inference or correction of model/instrument parameters. Calibration is not validation.

### 4.4 Reproducibility

Ability to reconstruct, recompute, rerun, or independently reproduce evidence at a declared level. Reproducibility is not correctness.

### 4.5 Benchmark comparison

Evidence comparing algorithms, geometries, calibrations, or implementations under a declared fairness contract.

### 4.6 Implementation cross-validation

Evidence that a downstream numerical/hardware implementation preserves an accepted upstream scientific implementation within declared equivalence semantics.

**Normative rule:** these terms shall not be used interchangeably in code, reports, figures, acceptance records, or publication claims.

---

## 5. F2 — Truth and Reference Provenance

GeoDOA shall distinguish:

```text
exact simulation truth
reference value/artifact
physical measurement
calibration estimate
external-tool/model prediction
algorithm estimate
unresolved reference state
```

`truth` is reserved for exact-by-construction or otherwise explicitly justified truth roles. A measured angle, CST manifold, calibration artifact, published number, or high-resolution numerical result is not automatically truth.

Every reference used for scoring shall preserve, as applicable:

```text
role
question/domain
coordinate/frame/reference plane
units
provenance
uncertainty
validity domain
parent artifact lineage
```

Truth available to the evaluator does not imply truth may be supplied to the algorithm. Supplying true `K`, true noise covariance, true manifold, true SNR, or another generative parameter is **oracle information** and must be declared in the method/comparison profile.

---

## 6. F3 — Deterministic Verification Ladder

Stable output from software is not automatically trustworthy reference evidence.

The preferred verification hierarchy is:

```text
scientific definition / derivation
    -> hand-solvable Golden Reference Problem
    -> exact/symbolic or high-confidence independent arithmetic
    -> independent numerical / cross-tool reference where appropriate
    -> software implementation comparison
    -> frozen regression artifact
    -> fixed/hardware promotion
```

A Golden Reference Problem shall preserve:

```text
scope/profile
inputs + units/frame/reference
exact/approximate status
expected analytical result
rounded/numerical presentation
independence from production implementation
tolerance rationale
failure interpretation
provenance/version
```

A regression test against saved production output detects change; it is not by itself an independent scientific oracle.

An external numerical tool, CST model, independent implementation, or high-precision computation may provide cross-reference/model evidence when its assumptions, reference planes, grids, and provenance are compatible. Agreement with such an artifact is verification/model-reference evidence unless a separate physical validation contract supplies traceable physical evidence; cross-tool agreement alone is not physical validation.

ADR-004's accepted canonical Golden Reference is:

```text
GRP-018 — Bias, Variance, MSE, and RMSE by hand
```

Formal expected values and supplemental deterministic references are recorded in `../science/golden_reference/ADR-004_GOLDEN_REFERENCE_PROBLEMS.md` and passed Gate E.

---

## 7. F4 — Stochastic Experiment Identity, RNG, and CRN

The canonical hierarchy is:

```text
study
  -> condition
       -> Monte Carlo trial
            -> L snapshot(s) / samples inside the trial
```

with separate method, implementation, run/execution, and artifact identities.

A Monte Carlo trial is a scientifically identified realization of a declared stochastic experiment, not a loop index or worker task.

The following counts/structural quantities remain distinct and shall not be used interchangeably:

```text
snapshot count L
Monte Carlo trial count N
physical/source count K
source-covariance rank
observed signal-subspace rank
estimator model order
estimated-output cardinality K_hat
matched-pair/source-opportunity count
condition count
```

Every random quantity shall have declared:

```text
identity
units/support/distribution
complex parameterization where relevant
dependence structure
redraw scope
conditional law
scientific visibility
scoring role
```

Exact stochastic replay requires more than a root seed. The provenance contract includes:

```text
root study seed or seed-set
RNG/bit-generator family + version semantics
versioned semantic child-stream derivation
study/condition/trial identity
random-family identity
substream role
redraw scope
```

Conceptually,

\[
S_{child}=H(S_{root},I_{study},I_{condition},I_{trial},I_{family},I_{role},V).
\]

Process-global mutable RNG state shall not be authoritative.

### 7.1 Common Random Numbers

Fair paired comparisons should share scientifically common exogenous latent randomness.

CRN does not require incompatible-dimensional arrays to be literally identical. Different geometries may share source waveforms and semantically paired noise/random families under a declared mapping. Algorithm-internal randomness remains separate unless intentionally paired.

---

## 8. F5 — Association, Detection, Miss, Spurious Output, and Resolution

Multi-source truth is an unordered set unless persistent physical identities are independently justified.

Let

\[
\Theta=\{\theta_1,\ldots,\theta_K\},
\qquad
\hat\Theta=\{\hat\theta_1,\ldots,\hat\theta_{\hat K}\}.
\]

Association is an evaluation operation applied after a valid estimator output.

For equal cardinality, a canonical assignment form is

\[
\pi^*=\arg\min_{\pi\in S_K}\sum_i C_{i,\pi(i)}.
\]

For unequal cardinality, unmatched truth and unmatched estimates remain explicit. Association gates, cost coordinates, tie rules, and ambiguity handling are study/profile semantics; no universal gate is accepted.

The canonical evaluation sequence is:

```text
raw estimator output
-> execution/failure state
-> association
-> detected / missed / spurious outcomes
-> resolution event
-> localization metrics on declared matched set
```

A **spurious/unmatched estimate** is not automatically a formal false alarm. Formal `P_FA` requires an explicit null/absence/detection-theory universe.

A designated source pair/group is truth-based resolved only when the required truth members receive distinct admissible one-to-one estimate matches under the declared event policy.

Beamwidth, Rayleigh criteria, search-grid spacing, peak count, or truth separation are not synonymous with empirical resolution success.

---

## 9. F6 — Metric Semantics

For scalar estimate `\hat q` and reference/truth `q`, define

\[
e=\hat q-q.
\]

For a fixed truth value `q_0`,

\[
\operatorname{Bias}=E[e],
\]

and

\[
\operatorname{Var}(\hat q)
=E\!\left[(\hat q-E[\hat q])^2\right]
=E\!\left[(e-E[e])^2\right].
\]

Then

\[
\operatorname{MSE}=E[e^2]
=\operatorname{Var}(\hat q)+\operatorname{Bias}^2,
\qquad
\operatorname{RMSE}=\sqrt{\operatorname{MSE}}.
\]

When truth itself is random across the target population, bias/variance/MSE shall identify the averaging distribution/conditioning and shall not silently reuse fixed-truth interpretations.

For `N` finite Monte Carlo errors:

\[
\bar e=\frac1N\sum_i e_i,
\qquad
\widehat{MSE}=\frac1N\sum_i e_i^2,
\qquad
\widehat{RMSE}=\sqrt{\widehat{MSE}}.
\]

Define the divisor-`N` empirical centered second moment

\[
v_N=\frac1N\sum_i(e_i-\bar e)^2.
\]

Then exactly,

\[
\widehat{MSE}=v_N+\bar e^2.
\]

This `v_N` is distinct from the divisor-`N-1` sample variance

\[
s^2=\frac1{N-1}\sum_i(e_i-\bar e)^2,
\]

which may be used for statistical variance/standard-error estimation under suitable assumptions.

Metrics shall declare:

```text
reference role
coordinate + units
association policy
included trial/pair/source-opportunity universe
failure mapping
weighting / macro-vs-micro aggregation
conditioning
```

Matched-only RMSE is conditional evidence and shall be accompanied by coverage/miss/failure information.

### 9.1 VP-001 matrix terminology

For VP-001's zero-mean synthetic baseline,

\[
\hat R^{(2)}=\frac1LXX^H
\]

is canonically the **uncentered sample second moment**. Centered sample covariance is a distinct matrix object.

### 9.2 Event-probability universes

For a declared fixed condition `C` and trial law `P_trial`, a resolution event indicator `R_t` defines

\[
P_{res}=P(R=1\mid C,P_{trial}).
\]

For VP-001's baseline end-to-end pair/group resolution metric,

\[
\widehat P_{res}
=\frac{N_{resolved}}{N_{eligible,compatible}},
\]

where the denominator is the set of scientifically eligible, method-compatible trials for the declared resolution event. A valid unresolved/missed trial contributes `R=0`; a numerical/algorithm failure on an otherwise eligible compatible trial also contributes `R=0` while retaining its typed failure record. Invalid-input, outside-profile, and method-incompatible conditions are not silently coerced into this ordinary denominator and are reported separately.

For VP-001 source-level end-to-end detection probability,

\[
\widehat P_D
=\frac{N_{detected\ truth\ opportunities}}{N_{eligible\ truth\ opportunities\ in\ compatible\ trials}}.
\]

An admissibly matched truth source is detected; a valid unmatched truth source is missed. If the method suffers a numerical/algorithm failure on an otherwise eligible compatible trial, the affected eligible truth-source opportunities are non-detections for this end-to-end `P_D`, while the failure status remains preserved.

Conditional valid-output probabilities are permitted only under distinct metric identities and must report their conditioning plus failure/coverage evidence. Metric mapping never erases the original outcome status.

---

## 10. F7 — Monte Carlo Adequacy and Uncertainty

There is no universal sufficient trial count such as `N=100`, `1000`, or `10000`.

Adequacy depends on:

```text
metric type
required precision
condition difficulty
rare/tail event probability
failure behavior
dependence/hierarchy
paired design
intended claim
computational budget
```

Flat running curves are diagnostic, not proof of adequacy.

Publication-grade stochastic evidence shall preserve condition-level counts, stopping reason, adequacy status, tail/failure diagnostics, and uncertainty where the claim depends on finite-sample estimation.

### 10.1 Bernoulli metrics

For ordinary IID fixed-`N` Bernoulli events, the VP-001 default interval is the Wilson score interval. Wald intervals are not a universal default, particularly near `0` or `1` or at small `N`.

Observing `0/N` or `N/N` does not establish exact population probability `0` or `1`.

### 10.2 Mean / MSE / RMSE uncertainty

Mean/bias uncertainty may use compatible standard-error/t procedures only when assumptions are appropriate.

MSE uncertainty is uncertainty in the mean of `e^2`. RMSE is a nonlinear transform; no universal RMSE confidence-interval formula is accepted. Valid approaches may include transformed MSE intervals, delta methods in regular regimes, or justified resampling.

### 10.3 Hierarchy and dependence

Repeated samples within one device/session/outer realization do not automatically create independent population evidence. Cluster, block, hierarchical, or other design-compatible uncertainty methods are required when dependence is material.

### 10.4 Stopping

Adaptive/sequential stopping is allowed only with a declared inference-compatible rule. VP-001 confirmatory studies should initially prefer a predeclared fixed `N` per condition, selected from pilot/planning evidence, followed by achieved adequacy/uncertainty reporting.

---

## 11. F8 — Fair Algorithm and Geometry Comparison

A fair comparison requires a declared comparison contract covering:

```text
scientific task/domain
truth/reference
source/noise/SNR/snapshot semantics
sensor/calibration profile
oracle information
preprocessing / postprocessing
association / metric / failure policy
tuning data, objective, search space, budget, locked values
CRN / paired-trial design
resource constraints
comparison uncertainty
runtime/timing scope
```

Equal metric names alone do not establish comparability.

A method tuned on the final benchmark while another remains untuned is not an unbiased algorithm comparison. Final evaluation evidence reused to choose thresholds, hyperparameters, association gates, geometries, or headline conditions becomes development/tuning evidence unless a new held-out evaluation is performed.

Geometry comparisons shall state what is fixed, including as applicable:

```text
physical sensor count
physical aperture
minimum spacing
RF-channel count
virtual/coarray DOF
calibration/implementation burden
```

Performance at fixed sensor count is not automatically topology-only performance independent of aperture.

Comparative uncertainty should target the actual paired difference/contrast. Non-overlap of marginal confidence intervals is not a substitute for direct comparison inference.

`not significantly different` does not establish equivalence. Superiority, noninferiority, and equivalence require declared effect/margin semantics.

---

## 12. F9 — Typed Non-Success Evidence

Three layers are authoritative and distinct:

```text
compatibility status       -> is method/profile scientifically admissible?
execution/outcome status   -> what happened in this run/trial?
metric eligibility         -> does the outcome belong in this metric universe?
```

No bare `valid` or `success` boolean may replace these layers.

Required semantic outcome families include:

```text
valid result
valid no detection
miss / spurious / unresolved source group
ambiguity / unidentifiability
incompatible / outside domain
invalid input/reference
numerical failure / algorithm nonconvergence
calibration / data-integrity / hardware / infrastructure failure
unresolved scientific state
not assessed
```

`NaN` is a numerical representation, not a scientific status.

Failure evidence shall preserve root cause, stage, severity, diagnostics, retry history, and metric-specific eligibility.

Retrying the same trial preserves the same scientific realization and original failure history. A replacement realization is a new trial identity.

For VP-001 end-to-end `P_D` and `P_res`, numerical/algorithm failure on an otherwise eligible method-compatible trial is non-success while the typed failure remains recorded. Incompatible or outside-profile conditions are separately accounted, not coerced into ordinary metric failures.

Ordinary localization RMSE shall not assign arbitrary angular penalties to numerical or compatibility failures.

---

## 13. F10 — Multi-Level Scientific Diagnostics

Final DOA RMSE is an end-to-end metric, not a complete failure diagnosis.

The canonical diagnostic chain is:

```text
manifold
-> covariance / second moment
-> eigenvalues / eigenspace
-> spectrum / objective
-> peak / event
-> final DOA
```

Reference-aware, gauge-aware diagnostics may include:

### 13.1 Manifold

\[
\rho(a,b)=\frac{|a^Hb|}{\|a\|\|b\|},
\qquad
\alpha=\cos^{-1}\rho,
\qquad
 d_{proj}^2=1-\rho^2.
\]

Raw norm, common-phase-aligned, common-complex-scale-aligned, whitened, and channel-resolved errors answer different questions and shall be labeled accordingly.

### 13.2 Covariance / second moment

Examples include relative Frobenius error, operator norm, Hermitian residual, PSD diagnostics, and trace/power discrepancy. Structural validity checks do not replace scientific matrix-error metrics.

Population/model error and finite-sample estimation error are distinct.

### 13.3 Eigenstructure

Useful evidence includes eigenvalue error, relevant eigengap, projector error, and principal angles. Individual eigenvector equality is not authoritative when phase/basis nonuniqueness applies.

### 13.4 MUSIC / spectrum

Truth-direction noise-subspace leakage, common-grid spectrum error, peak locations, threshold crossings, and final events are distinct levels.

No universal monotonic mapping from upstream norm error to downstream DOA error is assumed. Causal failure-mechanism claims require controlled evidence, not correlation alone.

---

## 14. F11 — Floating-Point, Fixed-Point, HLS/RTL, and FPGA Evidence Ladder

The implementation evidence ladder is:

```text
accepted scientific contract
-> verified float64 reference
-> float32 assessment if used
-> explicit fixed-point numerical model
-> bit-accurate implementation model
-> HLS/RTL verification
-> synthesis/place-route/timing evidence
-> FPGA/SoC board execution
-> later physical sensor/system validation
```

Agreement between downstream implementations does not establish scientific correctness if the common upstream reference is wrong.

Fixed-point provenance includes, per material stage:

```text
signedness
word/integer/fractional widths
rounding/truncation
saturation vs wrap
cast locations
product/accumulator widths
coefficient quantization
complex representation
operation ordering where material
```

Quantization effects shall be evaluated through downstream covariance/eigenspace/spectrum/event/DOA behavior, not only input LSB error.

Bit-exactness and bounded numerical equivalence are distinct targets and shall be declared per interface/test.

Hardware timing metrics remain distinct:

```text
latency
initiation interval
throughput
clock frequency / timing closure
resource use
power/energy where measured
```

Kernel-only speedup shall not be reported as end-to-end speedup unless numerator and denominator cover comparable work.

Board execution with synthetic/frozen vectors is digital implementation/integration evidence. It is not physical sensor validation.

---

## 15. F12 — Run, Configuration, Artifact, and Build Provenance

Required identity layers are distinct:

```text
study
condition
trial / trial ensemble
algorithm
implementation
run/execution
data / calibration / external-tool artifact
derived result / figure / table
hardware build
```

A timestamp, directory, filename, branch name, run token, or root seed alone is insufficient scientific identity.

### 15.1 Canonical configuration

Scientific configuration identity derives from a versioned canonical semantic representation with:

```text
explicit units
resolved defaults
stable numeric serialization
order semantics
null/optional semantics
authoritative-versus-derived values
upstream ADR/profile/schema versions
```

Canonicalization may normalize units/representation but shall not erase scientific distinctions such as phase reference, channel identity/order, far-field/narrowband status, snapshot/SNR/covariance semantics, sensor/calibration/reference-plane state, or compatibility profile.

A cryptographic content hash is the candidate identity mechanism; SHA-256 is the Phase-1 baseline unless a later versioned replacement is adopted.

Hashes support identity but do not replace human-readable resolved configuration or semantic diff.

### 15.2 Source and environment

Publication-grade runs identify exact Git commit SHA. Clean committed source is preferred; dirty execution requires preserved exact diff/content identity.

Critical numerical software versions/environment state shall be preserved to the level required by the reproducibility claim.

### 15.3 Data / calibration / external tools

Artifacts shall preserve content identity, schema, origin, units/frame/channel semantics, validity domain, and transformation lineage.

Calibration artifacts shall identify their exact validity state and reference plane. CST/measured artifact hashes identify content; they do not elevate epistemic authority.

### 15.4 FPGA build

Hardware evidence identifies source revision, tool/IP versions, part/board, constraints, clocks/directives, build settings, and bitstream/build artifact identity.

---

## 16. F13 — Publication Evidence and Reproducibility Package

A figure or table is a derived artifact, not the publication evidence package.

Every material quantitative claim should resolve to frozen evidence containing, as applicable:

```text
manifest
resolved configuration + hash
run/trial provenance
truth/reference role
association/metric/failure/uncertainty policy
trial-level or recomputable evidence
aggregate metrics + counts + uncertainty
failure/exclusion/incompatibility summary
figure/table generation lineage
software/environment identity
hardware-build identity
reproduction instructions
known limitations / reproducibility level
```

Scientific-value transformations shall be scripted or otherwise deterministically recorded. Hidden manual spreadsheet edits are not acceptable scientific provenance.

Recompute, full rerun, and independent reproduction are distinct claims.

Once cited/accepted evidence is frozen, later code/config/trial/policy changes create a new evidence identity. Corrections preserve the superseded package and create a new corrected package; silent replacement is forbidden.

A reproducibility package supports audit/reconstruction. It does not itself prove correctness or physical validity.

---

## 17. F14 — VP-001 Initial Validation Profile

VP-001 is the first accepted executable GeoDOA scientific validation profile.

### 17.1 Inherited scientific semantics

VP-001 uses:

```text
ADR-001 canonical 1-D geometry / theta / receive steering / stable phase reference
ADR-002 PM-001 far-field narrowband receive-array profile
ADR-003 ideal Phase-1 sensor profile
ADR-004 evidence contract
```

The canonical 1-D receive manifold remains inherited from ADR-001:

\[
a_n(\theta,f)
=\exp[-jk(x_n-x_{ref})\sin\theta].
\]

### 17.2 Baseline stochastic profile

```text
K = 1 primary localization/reference cases
K = 2 primary localization/resolution cases
proper-complex zero-mean stationary sources
independent/incoherent equal-power sources by baseline default
proper-complex white equal-variance additive noise
nominal = physical geometry
ideal identical scalar elements
no coupling / differential gain-phase / differential delay / SRO / CFO / IQ / clipping
unquantized floating acquisition
identity deterministic calibration
```

Thus the deterministic Phase-1 sensor operator is

\[
\mathcal H_{sensor}^{Phase1}\equiv\mathcal I.
\]

### 17.3 Snapshots and matrix input

Each Monte Carlo trial contains `L` simultaneous-equivalent snapshots under ADR-002 semantics.

The baseline zero-mean matrix estimate is the uncentered sample second moment

\[
\hat R^{(2)}=\frac1LXX^H.
\]

Centered sample covariance is a distinct object/profile choice.

### 17.4 Baseline algorithms and evaluation

Candidate baseline algorithms are Bartlett, MVDR/Capon, and MUSIC, with MUSIC as the primary subspace reference. Known source count may be used only under explicit oracle-K mode.

Search sector/grid, peak extraction, interpolation/refinement, association cost/gate, and tie handling are explicit configuration/provenance.

VP-001 uses one-to-one truth-to-estimate association. Matched error, bias/MSE/RMSE, coverage, detection/miss/spurious outcomes, `P_res`, failure evidence, and multi-level diagnostics remain distinct outputs.

For a designated pair, baseline resolution requires distinct admissible matches for both truth members. A stricter no-spurious event requires a separate metric identity.

### 17.5 Monte Carlo execution

No universal `N` is fixed. Initial confirmatory VP-001 studies prefer predeclared fixed `N` per condition with achieved uncertainty and adequacy reporting.

For ordinary IID fixed-`N` Bernoulli `P_D`/`P_res` reporting, Wilson score interval is the default.

Fair algorithm comparison should use CRN on scientifically common exogenous latent randomness and harmonized evaluation semantics.

Geometry comparison requires explicit resource constraints.

### 17.6 Implementation path

VP-001 supports the downstream chain:

```text
verified float64
-> optional float32
-> fixed-point model
-> bit-accurate model
-> HLS/RTL
-> FPGA board replay
```

with multi-level internal cross-validation where accessible.

### 17.7 Explicitly outside plain VP-001

```text
near field
wideband / beam-squint behavior
mutual coupling
position / gain / phase / timing imperfections
colored/unequal noise
IQ imbalance / nonlinearity / clipping
ADC quantization
measured/CST manifold substitution
coherent-source remedy studies
unknown-K/model-order benchmarking
TDM-MIMO temporal-phase effects
physical sensor acquisition/calibration validation
```

These are deferred profiles/extensions, not unimportant topics.

---

## 18. Metric and Acceptance Boundaries

ADR-004 separates:

```text
metric / evidence quantity
from
acceptance threshold / engineering requirement
```

No universal pass/fail value is established for RMSE, `P_res`, numerical equivalence, eigenspace error, condition number, confidence level, latency, resource use, or fixed-point degradation.

A profile/test/engineering requirement may declare such a threshold only with explicit units, domain, rationale, and uncertainty/evidence semantics.

---

## 19. Consequences

### 19.1 Positive consequences

The project gains:

- reproducible stochastic trial identity;
- explicit truth/reference epistemic roles;
- fair multi-method and multi-geometry comparison;
- correct handling of misses/failures/incompatibility;
- metric-specific uncertainty rather than decorative error bars;
- diagnostic traceability from manifold to final DOA;
- a defensible float/fixed/FPGA validation ladder;
- publication figures/tables linked to immutable evidence;
- a bounded first implementation target through VP-001.

### 19.2 Costs

The project must retain more metadata and evidence than a tutorial-style simulation, including resolved configuration, trial identities, policy versions, failure records, environment/build identity, and derived artifact lineage.

This overhead is intentional because GeoDOA Studio is an engineering/scientific framework rather than a plot-generation script.

---

## 20. Boundary and Deferred Cases

The following require later specialized profiles rather than silent extension of VP-001:

```text
near-field / wideband
colored noise + whitening
coherent sources / smoothing or other rank-restoration methods
measured/full-wave/calibrated manifolds
nonideal sensor operator families
unknown model order
rare-event specialized sampling
hierarchical device/session studies
physical array validation
real-time end-to-end hardware acquisition
```

A future extension shall identify which ADR-001/002/003/004 profile assumptions changed and receive a new profile/version identity when comparability is materially affected.

---

## 21. Traceability to Exploration Decision Families

```text
F1   <- Exploration 4.1
F2   <- 4.2
F3   <- 4.3
F4   <- 4.4–4.5
F5   <- 4.6, 4.8, 4.9
F6   <- 4.7 plus metric reconciliation in 4.20
F7   <- 4.10–4.11
F8   <- 4.12
F9   <- 4.13
F10  <- 4.14
F11  <- 4.15
F12  <- 4.16
F13  <- 4.17
F14  <- 4.19
Cross-ADR authority and terminology <- 4.18
Final reconciliation <- 4.20
```

The exploration documents remain supporting rationale and shall not be deleted after acceptance.

---

## 22. Acceptance Evidence and Historical Gate Entry Requirements

The dedicated pre-Gate review verified the former Gate-A entry requirements and passed. The original draft-stage requirement list remains historically informative:

```text
F1–F14 represented without omission
no ADR-001/002/003 authority redefined
truth/reference/calibration terms exact
snapshot/trial/source-count terminology exact
uncentered second moment vs centered covariance exact
v_N vs s^2 distinction exact
association/detection/resolution order exact
P_D/P_res denominator and failure mapping explicit
compatibility/failure/metric-eligibility separation explicit
metric vs threshold separation preserved
VP-001 fixed-N/Wilson defaults correctly scoped
hardware implementation vs physical validation boundary explicit
provenance/publication immutability represented
no exploration-only candidate implementation detail promoted unnecessarily
```

These requirements are no longer pending. `ADR-004_PRE_GATE_CONSISTENCY_REVIEW.md` passed, followed by Gates A–F and final cross-gate reconciliation.

---

## 23. Final Accepted Status

```text
Explorations 4.1–4.20                  COMPLETE
Governing ADR-004                      ACCEPTED
Pre-Gate consistency review            PASS
Gate A — Physical Consistency          PASS
Gate B — Mathematical Consistency      PASS
Gate C — Dimensional / Unit            PASS
Gate D — Software Semantic             PASS
Gate E — Golden Reference              PASS
Gate F — Boundary / Failure            PASS
Final Cross-Gate Reconciliation        PASS
Formal GRP-018 Gate-E evidence         PASS
Final Acceptance Record                COMPLETE
Authoritative Phase-1 implementation   AUTHORIZED TO BEGIN — NOT PRE-ACCEPTED
```

The authoritative acceptance record is `ADR-004_FINAL_ACCEPTANCE_RECORD.md`. The lifecycle metadata drift identified as `XG-004-01` in the final cross-gate reconciliation is resolved by this accepted-status synchronization.
