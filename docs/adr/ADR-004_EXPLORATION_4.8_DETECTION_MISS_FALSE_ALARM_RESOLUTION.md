# ADR-004 Exploration 4.8 — Detection, Miss, False Alarm, and Resolution

- **ADR:** ADR-004 — Validation, Reproducibility, and Scientific Evidence
- **Phase:** 0C — Scientific Foundations
- **Exploration:** 4.8
- **Status:** EXPLORATION COMPLETE — CANDIDATE CONTRACT, NOT ACCEPTED
- **Depends on:** Accepted ADR-001, ADR-002, ADR-003; ADR-004 Explorations 4.1–4.7

## 1. Question

> How shall GeoDOA distinguish successful localization, source detection, missed detection, false/spurious detection, estimator failure, and multi-source resolution so that detection and resolution evidence is not silently collapsed into localization RMSE?

This exploration defines event semantics needed before Probability of Resolution is formalized in Exploration 4.9.

---

## 2. Core Principle

Localization accuracy and detection/resolution performance answer different questions.

For a source estimate:

```text
localization asks: where is the estimated source relative to truth?
detection asks: was a valid source estimate produced and associated?
resolution asks: were multiple nearby sources represented as distinct valid source estimates?
```

Candidate rule:

> GeoDOA shall not infer detection or resolution performance from RMSE alone, and shall not infer localization accuracy from detection probability alone.

---

## 3. Trial-Level Outcome Taxonomy

A multi-source trial may produce several simultaneous source-level outcomes.

Conceptually:

```text
MATCHED_DETECTION
MISSED_SOURCE
FALSE_OR_SPURIOUS_DETECTION
UNRESOLVED_SOURCE_GROUP
VALID_ZERO_DETECTION
ESTIMATOR_FAILURE
INCOMPATIBLE_CONFIGURATION
INVALID_INPUT_OR_TRUTH
AMBIGUOUS_ASSOCIATION
```

These are conceptual evidence states, not final software enums.

Candidate rule:

> Detection outcomes and execution/model failures remain distinct scientific states.

A numerical failure is not automatically a miss; an ordinary no-detection result is not automatically a numerical failure.

---

## 4. Source-Level Detection Semantics

Given truth set

\[
\Theta=\{\theta_1,\dots,\theta_K\}
\]

and valid estimator outputs

\[
\widehat\Theta=\{\hat\theta_1,\dots,\hat\theta_{\hat K}\},
\]

Exploration 4.6 produces matched pairs, unmatched truth, and unmatched estimates under a declared association policy.

For a truth source `i`, a candidate detection event is:

\[
D_i = 1
\]

if and only if that truth source participates in an admissible matched pair under the declared association policy.

Then

\[
M_i=1-D_i
\]

is the source-level miss indicator for valid estimator output trials.

Candidate rule:

> Source detection is defined through the declared evaluation/association contract, not by estimator output count alone.

---

## 5. False / Spurious Detection Semantics

An unmatched valid estimate is a candidate false/spurious detection.

If `F_j` indicates estimate `j` is unmatched,

\[
F_j=1
\]

marks that output as unsupported by any admissible truth match under the declared policy.

Candidate terminology:

- **spurious detection** is a generic localization-benchmark term for an unmatched estimate;
- **false alarm** is reserved for studies where a detection-theoretic null/absence event and threshold semantics are explicitly declared.

Candidate rule:

> GeoDOA shall not use `false alarm` loosely when the experiment only establishes an unmatched DOA estimate; the benchmark must declare whether it is measuring unmatched-output rate or formal false-alarm probability under a null hypothesis.

---

## 6. Detection under `K=0`

A formal false-alarm study may include conditions with no true sources:

\[
K=0.
\]

Then any valid source detection may constitute a false alarm under the declared detector/threshold policy.

For repeated null trials,

\[
P_{FA}=P(\text{at least one declared detection}\mid K=0)
\]

is one possible trial-level false-alarm definition.

Other definitions, such as expected false detections per angular scan, may also be valid.

Candidate rule:

> `P_FA` is not universal; the event unit—per trial, per scan cell, per peak, per time interval—must be declared.

---

## 7. Model-Order Oracle Complication

If an algorithm is given the true source count `K` and the postprocessor is forced to return exactly `K` peaks, then output cardinality alone cannot demonstrate detection capability.

In that case:

```text
K_hat = K by construction
```

does not imply

```text
all K true sources were detected or resolved.
```

Candidate rule:

> Oracle-known model order must be disclosed, and detection/resolution metrics must still depend on admissible association and source separability rather than forced output count.

---

## 8. Missed Detection versus Poor Localization

A source estimate outside the association gate may be treated as a miss plus a spurious estimate rather than as one extremely large localization error, depending on the benchmark contract.

Candidate rule:

> Association admissibility determines whether an output is considered a localized detection; localization error is computed only for declared matched detections unless a composite loss is explicitly defined.

This preserves Exploration 4.7's separation of localization RMSE from detection outcomes.

---

## 9. Resolution Is a Joint Multi-Source Event

For two or more nearby true sources, resolution is not merely the existence of multiple estimator outputs.

A conservative resolution event for a truth subset

\[
G=\{\theta_{i_1},\ldots,\theta_{i_m}\}
\]

should require at least:

1. each truth source in the group has a distinct admissible matched estimate;
2. one-to-one association is satisfied;
3. the matched estimates are distinct under the estimator/output semantics;
4. no required member of the group is missed;
5. the trial is otherwise scientifically valid for the declared benchmark.

Candidate rule:

> Multi-source resolution is a joint event over a declared truth group and shall not be inferred solely from estimator output cardinality.

---

## 10. Resolution versus Accuracy

Consider two true sources

\[
\{-1^\circ,+1^\circ\}.
\]

An estimator returning

\[
\{-4^\circ,+4^\circ\}
\]

may produce two distinct peaks but poor localization.

Conversely, an estimator returning one peak at

\[
0^\circ
\]

may be near the midpoint yet fail to resolve two sources.

Thus:

```text
accurate individual localization != resolved pair automatically
resolved pair != high localization accuracy automatically
```

Candidate rule:

> Resolution and localization accuracy shall be reported as distinct axes unless a benchmark explicitly defines a combined event.

---

## 11. Topological / Peak Resolution versus Truth-Based Resolution

Two conceptually different notions exist:

### 11.1 Spectrum-topology resolution

A spectrum contains distinguishable peaks according to a declared topological rule, e.g. local maxima plus valley/prominence requirements.

### 11.2 Truth-based estimator resolution

Distinct estimator outputs can be one-to-one associated with distinct true sources under declared admissibility.

These may disagree.

Candidate rule:

> GeoDOA shall distinguish spectrum-topology resolution from truth-based source resolution; one shall not silently substitute for the other.

Detailed spectrum diagnostics are deferred to Exploration 4.14.

---

## 12. Peak Separation Alone Is Insufficient

A rule such as

```text
estimated peaks separated by more than X degrees
```

is insufficient by itself because the peaks may both correspond poorly to the truth sources.

Likewise, two estimates close to two truths may not satisfy a desired spectrum valley/prominence criterion.

Candidate rule:

> Any separation threshold is only one component of a declared resolution definition, not a universal proof of source resolution.

---

## 13. Resolution Group Definition

For more than two sources, a benchmark must state whether it evaluates:

```text
all-source trial resolution
pairwise resolution
nearest-neighbor resolution
resolution of a designated source pair/group
```

For an all-source event,

\[
R_{\rm all}=1
\]

may require every truth source in the trial to have a distinct admissible match.

For pairwise studies,

\[
R_{ij}=1
\]

may evaluate only a designated pair while other sources act as interferers.

Candidate rule:

> Resolution event granularity is part of the benchmark contract.

---

## 14. Source Separation Is a Condition Variable, Not the Resolution Outcome

True angular separation

\[
\Delta\theta_{ij}=|\theta_i-\theta_j|
\]

is an input/condition variable.

Resolution event `R` is an output/evidence variable.

Candidate rule:

> Saying `the sources are separated by 2 degrees` is not equivalent to saying `the algorithm resolved them`.

Exploration 4.9 will define probability of resolution as a function of declared conditions such as separation, SNR, snapshots, geometry, and sensor profile.

---

## 15. Resolution Limit versus Probability of Resolution

A deterministic quantity such as Rayleigh-like beamwidth, array beampattern mainlobe width, CRB, or asymptotic estimator property is not automatically the empirical resolution limit of a stochastic DOA algorithm.

Candidate rule:

> Analytical resolution heuristics and empirical probability-of-resolution curves are different evidence types and shall be labeled separately.

No universal Rayleigh criterion is adopted for GeoDOA DOA estimators in Phase 0C.

---

## 16. Source Correlation and Coherence

Resolution performance may depend strongly on source correlation/coherence.

Two source pairs with identical angular separation, SNR, and snapshots may have different resolution behavior if their source covariance structures differ.

Candidate rule:

> Resolution evidence shall inherit the source-correlation/coherence semantics of ADR-002; source separation alone is insufficient experiment description.

---

## 17. Array Geometry and Sensor Profile Dependence

Resolution depends on more than nominal aperture.

Relevant variables can include:

```text
array geometry
active-channel state
frequency
manifold model
sensor mismatch
coupling
calibration state
noise covariance
snapshot count
source powers/correlation
estimator/postprocessor
search grid
```

Candidate rule:

> A claimed resolution capability is profile- and condition-dependent, not a timeless scalar property of an algorithm name.

---

## 18. Grid-Limited Resolution

A discrete search grid may prevent estimates from representing arbitrarily close directions even if the continuous underlying estimator has finer theoretical capability.

Candidate requirements:

- search grid provenance retained;
- peak interpolation/refinement policy declared;
- grid spacing not silently confused with physical resolution;
- off-grid truth handling declared.

Candidate rule:

> Numerical grid resolution and physical/statistical source resolution are distinct concepts.

---

## 19. Detection Threshold and Peak Extraction Policy

Detection behavior depends on postprocessing choices such as:

```text
peak threshold
prominence
minimum peak distance
number-of-peaks rule
model-order estimate
search-domain boundaries
interpolation/refinement
```

These are part of the estimator/evaluation contract when they affect output detections.

Candidate rule:

> Algorithm comparison shall not change detection/peak-extraction rules asymmetrically unless the benchmark explicitly intends to compare complete pipelines with different postprocessors.

Fairness details are deferred to Exploration 4.12.

---

## 20. Detection Probability

For a declared source/condition, source-level probability of detection is conceptually

\[
P_D=P(D_i=1\mid \mathcal C),
\]

where `C` includes the declared condition/profile and trial distribution.

Empirically, over `N` eligible trials,

\[
\widehat P_D
=
\frac{1}{N}\sum_{t=1}^{N} D_{i,t}.
\]

Candidate rule:

> The denominator must represent eligible trials under the declared condition and shall not silently exclude difficult valid trials.

Confidence intervals are deferred to Exploration 4.11.

---

## 21. Miss Probability

For a valid binary source-level detection event under the same eligibility definition,

\[
P_M=1-P_D.
\]

But this identity does not include numerical failures or incompatible trials unless the study explicitly maps them into the detection event space.

Candidate rule:

> `P_M=1-P_D` is valid only for the declared binary detection universe; typed failures outside that universe remain separately accounted unless explicitly included by policy.

---

## 22. False Detection Metrics

Possible false/spurious metrics include:

```text
probability of at least one false detection per trial
expected number of false detections per trial
false detections per scan/angular interval
formal P_FA under K=0
false discovery fraction among reported estimates
```

They answer different questions.

Candidate rule:

> GeoDOA shall name the event and denominator explicitly rather than reporting a generic `false alarm rate` without definition.

---

## 23. Partial Resolution

For `K>2`, a trial may resolve some sources and merge/miss others.

Therefore binary all-or-none resolution can discard useful structure.

GeoDOA should preserve source/pair/group-level resolution evidence even if a top-level all-source event is also reported.

Candidate rule:

> Trial-level resolution summaries shall not destroy the underlying matched/unmatched group structure needed for diagnosis.

---

## 24. Ambiguous / Unidentifiable Cases

Some conditions may be physically or mathematically unidentifiable under the declared model, e.g. aliasing or projection ambiguity.

Candidate rule:

> An intrinsically ambiguous/unidentifiable condition shall not be treated as an ordinary estimator miss without preserving its compatibility/identifiability status.

This inherits ADR-001 aliasing/ambiguity semantics and ADR-003 identifiability semantics.

---

## 25. Boundary and Endfire Effects

Association/detection near visible-sector boundaries can be distorted by clipping, grid truncation, or asymmetric search support.

Candidate requirements:

- boundary-aware search domain declared;
- estimates outside allowed domain rejected/handled explicitly;
- edge conditions reported rather than silently pooled with interior conditions if behavior differs materially.

No universal boundary margin is adopted here.

---

## 26. Equal-Power and Unequal-Power Source Resolution

Two sources of unequal power can produce qualitatively different peak behavior than equal-power sources.

Candidate rule:

> Resolution claims shall preserve source-power ratio or source covariance provenance when relevant; `two-source resolution` without source-strength context may be incomplete.

---

## 27. Hardware / Fixed-Point Detection Equivalence

A hardware implementation may preserve approximate DOA values but alter peak count, threshold crossing, ordering, or prominence due to quantization.

Candidate rule:

> Float/fixed/FPGA cross-validation shall compare not only localization error but also typed detection/resolution outcomes when the algorithm includes thresholding or peak extraction.

Detailed cross-validation is deferred to Exploration 4.15.

---

## 28. Candidate Phase-1 Detection/Resolution Profile

For initial synthetic stationary far-field narrowband DOA studies, a conservative candidate profile is:

```text
truth: exact point-source DOAs under ADR-001
estimator output: valid finite set of DOA estimates
association: accepted 4.6 one-to-one policy
matched source: detection candidate
unmatched truth: miss candidate
unmatched estimate: spurious/false-detection candidate
formal false alarm: only when a K=0/null-event protocol is declared
resolution: designated truth group has distinct admissible one-to-one matches
localization accuracy: reported separately from resolution
oracle-K status: explicit
failure/incompatibility: typed separately
search-grid and peak-extraction policy: provenance
```

No universal association gate, peak threshold, or resolution threshold is accepted here.

---

## 29. Invalid / Weak Evidence Cases

The following are scientifically weak or invalid unless explicitly justified:

1. call every unmatched estimate a formal `false alarm` without defining an event denominator;
2. claim detection because the algorithm was forced to output `K` peaks;
3. claim resolution solely because two peaks exist;
4. claim resolution solely because truth separation exceeds one nominal beamwidth;
5. infer resolution probability from RMSE alone;
6. delete unmatched truth before computing detection rate;
7. map numerical failures into ordinary misses without disclosure;
8. change peak threshold between algorithms to favor one method;
9. confuse search-grid spacing with physical source resolution;
10. treat output cardinality equality as proof of correct association;
11. report `P_M=1-P_D` while silently excluding failures from only one side;
12. pool identifiable and fundamentally ambiguous conditions without preserving status;
13. call a midpoint estimate for two close sources `accurate resolution` because total squared error is small under a poor scoring rule;
14. ignore source-power/coherence differences in a resolution claim.

---

## 30. Cross-ADR Reconciliation

### ADR-001

Detection/resolution inherits visible-sector topology, aliasing, projection ambiguity, angle/direction coordinates, and domain boundaries.

### ADR-002

Source count, correlation/coherence, source powers, snapshots, noise statistics, and model-order semantics remain part of the condition profile.

### ADR-003

Sensor mismatch, calibration, colored noise, coupling, timing, and identifiability can change detection/resolution behavior and remain explicit profile variables.

### ADR-004 Exploration 4.6

Matched/unmatched truth and estimates provide the baseline source-level event structure.

### ADR-004 Exploration 4.7

Localization RMSE remains separate from miss/false/failure outcomes unless an explicit composite loss is defined.

**Cross-ADR result: no contradiction identified.**

---

## 31. Candidate Decisions from Exploration 4.8

- **D4.8-01:** Localization accuracy, source detection, and multi-source resolution are distinct scientific outputs.
- **D4.8-02:** A valid admissibly matched truth source defines a source-level detection candidate; unmatched truth defines a miss candidate.
- **D4.8-03:** Unmatched valid estimates are spurious/false detections; formal `false alarm` terminology requires an explicitly declared null/event denominator.
- **D4.8-04:** Estimator numerical failure, incompatibility, and ordinary zero-detection are distinct states.
- **D4.8-05:** Oracle-known `K` and forced output cardinality do not establish detection/resolution performance.
- **D4.8-06:** Multi-source resolution is a joint event requiring distinct one-to-one admissible matches for the declared truth group.
- **D4.8-07:** Resolution and localization accuracy remain separate axes by default.
- **D4.8-08:** Spectrum-topology resolution and truth-based estimator resolution are distinct.
- **D4.8-09:** Source separation is an input condition; successful resolution is an output event.
- **D4.8-10:** No universal Rayleigh/beamwidth criterion is accepted as GeoDOA's estimator-resolution definition.
- **D4.8-11:** Search-grid spacing and physical/statistical resolution are distinct.
- **D4.8-12:** Detection/peak-extraction policy is part of benchmark provenance and may materially affect `P_D`, false detections, and resolution.
- **D4.8-13:** `P_D`, `P_M`, false-detection metrics, and future `P_res` require explicit eligibility denominators and event definitions.
- **D4.8-14:** Partial pair/group resolution evidence should be retained even when an all-source trial summary is reported.
- **D4.8-15:** Fundamentally ambiguous/unidentifiable conditions remain typed and are not silently scored as ordinary misses.
- **D4.8-16:** Float/fixed/FPGA comparisons shall preserve detection/resolution event semantics, not only numerical DOA error.

---

## 32. Exploration 4.8 Conclusion

Exploration 4.8 is complete at candidate-contract level.

The central rule is:

> GeoDOA shall treat detection, miss, spurious/false detection, estimator failure, and multi-source resolution as typed event evidence derived from explicit association and benchmark semantics; resolution is a joint truth-group event requiring distinct admissible matches and shall remain separate from localization accuracy, spectrum topology, search-grid resolution, and oracle-imposed output cardinality.

No acceptance gate is started or passed by this exploration.

The next exploration is:

```text
4.9 — Probability of Resolution
```
