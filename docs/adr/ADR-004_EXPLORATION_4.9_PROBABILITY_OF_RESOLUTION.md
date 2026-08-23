# ADR-004 Exploration 4.9 — Probability of Resolution

- **ADR:** ADR-004 — Validation, Reproducibility, and Scientific Evidence
- **Phase:** 0C — Scientific Foundations
- **Exploration:** 4.9
- **Status:** EXPLORATION COMPLETE — CANDIDATE CONTRACT, NOT ACCEPTED
- **Depends on:** Accepted ADR-001, ADR-002, ADR-003; ADR-004 Explorations 4.1–4.8

## 1. Question

> How shall GeoDOA define, estimate, condition, compare, and report Probability of Resolution so that `P_res` refers to a reproducible stochastic event rather than an informal count of visible peaks?

This exploration converts the resolution event semantics from Exploration 4.8 into a probability/Monte-Carlo contract and prepares the ground for trial-count adequacy in Exploration 4.10.

---

## 2. Core Principle

Probability of Resolution is the probability of a **predeclared resolution event** under a **predeclared experiment distribution**.

Let

\[
R_t\in\{0,1\}
\]

be the resolution indicator for trial `t` under a declared truth group and declared resolution policy.

Then

\[
P_{\rm res}
=
P(R=1\mid \mathcal C,\mathcal P_{\rm trial}),
\]

where `C` denotes the fixed/swept scientific condition and `P_trial` denotes the stochastic trial law.

Candidate rule:

> `P_res` is not an intrinsic scalar property of an algorithm name; it is conditional on geometry, source configuration, SNR/noise semantics, snapshot count, sensor profile, estimator/postprocessor, association/resolution policy, and trial distribution.

---

## 3. Resolution Event Comes First

Before estimating `P_res`, GeoDOA must define the binary event `R`.

For a designated truth group

\[
G=\{\theta_{i_1},\ldots,\theta_{i_m}\},
\]

a baseline truth-based resolution event may require:

1. the trial is scientifically eligible under the declared profile;
2. estimator output is valid under the declared failure semantics;
3. every truth source in `G` has a distinct admissible one-to-one match;
4. no member of `G` is missed;
5. no one estimate is reused for multiple truth sources;
6. any additional declared group-specific criterion is satisfied.

Candidate rule:

> The event definition is part of the metric. Changing the event definition changes `P_res` even if the underlying estimator outputs are identical.

---

## 4. Empirical Probability of Resolution

For `N` eligible trials under the same declared condition and event definition,

\[
\widehat P_{\rm res}
=
\frac{1}{N}\sum_{t=1}^{N}R_t.
\]

If `n_res` trials resolve successfully,

\[
\widehat P_{\rm res}
=
\frac{n_{\rm res}}{N}.
\]

Candidate rule:

> The numerator and denominator must both be reconstructable from retained trial-level evidence.

The uncertainty of this finite Monte Carlo estimate is deferred to Exploration 4.11.

---

## 5. Denominator Semantics

The denominator `N` is not simply the number of loop iterations.

GeoDOA shall distinguish at least:

```text
requested trials
scientifically eligible trials
validly executed trials
resolved trials
unresolved-but-valid trials
failed trials
incompatible/out-of-domain trials
excluded trials with explicit reason
```

Candidate rule:

> Probability-of-resolution reports shall state which trial universe defines the denominator.

A method shall not improve `P_res` by silently discarding difficult unresolved trials.

---

## 6. Failure Handling and `P_res`

Typed estimator failures require explicit policy.

Three conceptually different choices may exist:

### 6.1 Failure counted as non-resolution

Appropriate when the system-level question is:

> Did this complete method resolve the sources on an otherwise valid trial?

Then a numerical/algorithmic failure can yield

\[
R_t=0.
\]

### 6.2 Failure excluded from conditional resolution analysis

Appropriate only when reporting a clearly labeled conditional metric such as

\[
P_{\rm res}\mid\text{valid estimator output}.
\]

The failure rate must then be reported separately.

### 6.3 Incompatible/out-of-domain condition

A fundamentally invalid condition may be outside the metric universe rather than a non-resolution event.

Candidate rule:

> Failure inclusion policy is benchmark semantics, not an implementation convenience; unconditional and success-conditioned `P_res` shall not share the same label.

Detailed failure taxonomy is deferred to Exploration 4.13.

---

## 7. Condition-Resolved `P_res`

A useful resolution study commonly evaluates

\[
P_{\rm res}(\Delta\theta,\mathrm{SNR},L,\ldots).
\]

For example,

\[
P_{\rm res}
=
P(
R=1
\mid
\Delta\theta,\mathrm{SNR},L,\mathcal G,\mathcal S,\mathcal A
),
\]

where:

- `Delta theta` = true source separation;
- `L` = snapshots;
- `G` = geometry/profile;
- `S` = sensor/noise/source statistical profile;
- `A` = algorithm/postprocessing configuration.

Candidate rule:

> Resolution probability shall preferably be reported as a condition-dependent curve/surface rather than collapsed prematurely into one grand average.

---

## 8. Source Separation Sweep

For a two-source experiment, a common design varies

\[
\Delta\theta
=
|\theta_2-\theta_1|.
\]

At each separation `Delta theta_k`, estimate

\[
\widehat P_{\rm res}(\Delta\theta_k).
\]

Candidate rule:

> Each separation point is its own Monte Carlo condition unless the experiment explicitly defines a random separation distribution.

Averaging all separations into one scalar can obscure the actual resolution transition.

---

## 9. Midpoint / Sector Dependence

Two pairs with the same angular separation can have different difficulty when centered at different locations in the visible sector.

Example:

```text
pair A: {-1 deg, +1 deg}
pair B: {78 deg, 80 deg}
```

have the same separation but not the same mapping in direction cosine `u=sin(theta)` or manifold sensitivity.

Candidate rule:

> A resolution-vs-separation study shall also declare pair midpoint/absolute source locations or an explicit distribution over them.

`P_res(Delta theta)` alone may be incomplete over a wide field of view.

---

## 10. Direction-Cosine versus Angular Separation

Under ADR-001,

\[
u=\sin\theta.
\]

For two sources,

\[
\Delta u
=|\sin\theta_2-\sin\theta_1|.
\]

Thus equal `Delta theta` does not imply equal spatial-frequency/direction-cosine separation across the visible sector.

Candidate rule:

> GeoDOA may report `P_res` versus angular separation, direction-cosine separation, or both, but the chosen coordinate is part of the scientific contract.

No universal equivalence is assumed.

---

## 11. Probability of Resolution versus Probability of Detection

For two sources, resolution usually implies both members were distinctly detected under the declared policy.

Therefore a common relationship is

\[
R=1
\Rightarrow
D_1=1,\quad D_2=1,
\]

but the converse need not hold if the resolution definition includes additional separation/topology constraints.

Hence

```text
P_res != P_D of one source
P_res != product of individual P_D values in general
```

because source detection events can be statistically dependent.

Candidate rule:

> GeoDOA shall not approximate `P_res` by multiplying marginal detection probabilities unless the required independence/model assumptions are explicitly justified.

---

## 12. Pairwise versus All-Source `P_res`

For `K>2`, several resolution probabilities may be meaningful.

### 12.1 Pairwise

\[
P_{\rm res}^{(i,j)}
=P(R_{ij}=1).
\]

### 12.2 Designated group

\[
P_{\rm res}^{(G)}
=P(R_G=1).
\]

### 12.3 All-source

\[
P_{\rm res}^{(\mathrm{all})}
=P(R_{\rm all}=1).
\]

These are not interchangeable.

Candidate rule:

> The truth group/granularity is part of the metric name/provenance.

---

## 13. Probability of Resolution Is Not a Deterministic Resolution Limit

A probability curve may transition gradually with separation.

For example:

```text
Delta theta = 1 deg  -> P_res = 0.15
Delta theta = 2 deg  -> P_res = 0.52
Delta theta = 3 deg  -> P_res = 0.91
```

No unique scalar `resolution limit` exists unless a benchmark defines an operating probability threshold.

Candidate rule:

> A scalar resolution threshold such as `Delta theta_90` is a derived benchmark quantity requiring a declared probability target, interpolation rule, condition profile, and uncertainty treatment.

---

## 14. Derived Resolution Thresholds

A benchmark may define

\[
\Delta\theta_p
=
\inf\{\Delta\theta:\ P_{\rm res}(\Delta\theta)\ge p\}
\]

for target probability `p`, e.g. `p=0.9`.

But practical finite-grid Monte Carlo data require choices about:

- monotonicity assumption;
- interpolation;
- noisy probability estimates;
- confidence bounds;
- non-monotonic empirical curves;
- finite separation grid.

Candidate rule:

> `Delta theta_90`, `Delta theta_95`, etc. are derived study-specific summaries, not universal array constants.

Detailed adequacy/uncertainty rules are deferred to 4.10 and 4.11.

---

## 15. Monotonicity Is Expected Often, Not Guaranteed Empirically

Physically one often expects resolution probability to increase with source separation under a fixed profile.

However finite Monte Carlo noise, grid effects, sidelobes, aliasing, postprocessing thresholds, source-power interactions, and estimator pathologies can produce non-monotonic estimates.

Candidate rule:

> GeoDOA shall not silently force a monotonic `P_res` curve unless a declared modeling/postprocessing method explicitly imposes and justifies monotonicity.

Unexpected non-monotonicity is diagnostic evidence.

---

## 16. SNR Dependence

Resolution probability depends on the exact SNR definition inherited from ADR-002.

Therefore

\[
P_{\rm res}(\mathrm{SNR})
\]

is meaningless unless SNR semantics identify:

```text
signal quantity/power reference
noise quantity/power reference
per-source vs total signal power
per-sensor/per-channel normalization
pre/post sensor-operator location
bandwidth/sample conventions where relevant
```

Candidate rule:

> `P_res at 0 dB` is not comparable across studies unless SNR definitions are compatible.

---

## 17. Snapshot Dependence

Finite snapshot count `L` is a direct performance condition.

Resolution evidence shall preserve whether:

- snapshots are independent/correlated;
- covariance is centered/uncentered as applicable;
- source processes are coherent/incoherent;
- effective rank limits apply.

Candidate rule:

> `P_res(L)` inherits ADR-002 snapshot/covariance semantics; equal numeric `L` does not guarantee equivalent information content across different temporal models.

---

## 18. Source Power Ratio

For two sources with powers `P1` and `P2`, define a declared power ratio such as

\[
\rho_P=10\log_{10}\frac{P_1}{P_2}.
\]

`P_res` can depend strongly on `rho_P`.

Candidate rule:

> Resolution studies shall declare equal-power assumptions or preserve source-power ratio as a condition variable.

---

## 19. Source Correlation / Coherence

For source covariance `R_s`, coherent versus incoherent sources can materially change subspace rank and resolution.

Candidate rule:

> Probability-of-resolution results shall preserve source-correlation/coherence provenance; a `P_res` curve from independent sources shall not be generalized silently to coherent sources.

---

## 20. Sensor Imperfection / Calibration Dependence

Under ADR-003, position error, gain/phase mismatch, coupling, timing/synchronization, colored noise, and calibration state may change the resolution event distribution.

Candidate rule:

> `P_res` shall be associated with a declared sensor/calibration profile. Ideal-manifold resolution evidence is not automatically evidence for an imperfect or mismatched system.

---

## 21. Search Grid and Peak Policy Dependence

Resolution probability may change when:

```text
search-grid spacing changes
peak interpolation is enabled/disabled
minimum peak distance changes
prominence/threshold changes
model-order selection changes
search sector changes
```

Candidate rule:

> `P_res` belongs to the complete estimator/postprocessing configuration used to define the resolution event, not to the spectral formula alone.

---

## 22. Common Random Numbers for `P_res` Comparison

When comparing algorithms `A` and `B`, Explorations 4.5 and 4.12 favor paired exogenous realizations when valid.

For each trial `t`, retain

\[
R_t^{(A)},\quad R_t^{(B)}
\]

under the same physical/source/noise realization.

This supports paired comparison of resolution events rather than comparing only two marginal proportions.

Candidate rule:

> Trial-level paired resolution indicators shall be retained when Common Random Numbers are used.

Statistical tests/intervals for paired binary outcomes are deferred to Exploration 4.11/4.12.

---

## 23. Requested Trial Count versus Effective Evidence

Suppose 1000 trials are requested but only 600 are validly eligible due to failures or exclusions.

Reporting

```text
P_res = n_res / 1000
```

or

```text
P_res = n_res / 600
```

answers different questions depending on the declared policy.

Candidate rule:

> GeoDOA shall preserve requested, eligible, executed, failed, and resolved counts so the probability interpretation is auditable.

---

## 24. Confidence and Trial Adequacy Are Not Optional Decorations

A finite estimate such as

\[
\widehat P_{\rm res}=0.90
\]

has very different evidential strength for `N=10` and `N=10000`.

Candidate rule:

> A probability estimate without its denominator is incomplete scientific evidence.

Rules for adequate `N`, convergence, and confidence intervals are deferred to Explorations 4.10 and 4.11.

---

## 25. Rare-Event Boundaries

When `P_res` is near 0 or 1, naive normal approximations can be poor for small `N`.

Candidate rule:

> GeoDOA shall not define probability-estimate reliability solely through symmetric `sqrt(p(1-p)/N)` error bars in all regimes; confidence methodology will be specified in Exploration 4.11.

This exploration records the boundary without choosing the final interval method.

---

## 26. Random Source Separation versus Fixed Separation

If `Delta theta` itself is randomized according to `p(Delta theta)`, then

\[
P_{\rm res}
=E_{\Delta\theta}[P(R=1\mid\Delta\theta)]
\]

is a distribution-weighted average and is different from a fixed-separation curve.

Candidate rule:

> Random-condition averages shall not be labeled as fixed-condition `P_res` without declaring the condition distribution.

---

## 27. Macro versus Micro Averaging Across Conditions

Suppose multiple separation/SNR conditions have different numbers of trials.

A micro average weights by trial count, while a macro average gives equal weight to conditions.

Candidate rule:

> Aggregated `P_res` across heterogeneous conditions requires an explicit weighting target; otherwise condition-resolved probabilities are preferred.

---

## 28. Reproducibility Provenance for `P_res`

A publication-grade `P_res` result should preserve, as applicable:

```text
resolution-event policy/version
truth group definition
association policy/version
association coordinate and gate
condition identity
source locations/separation/midpoint
SNR definition
snapshot count/statistics
source powers/correlation
sensor/calibration profile
algorithm and postprocessor configuration
search grid / peak extraction rules
root seed / trial identities
requested / eligible / resolved / failed counts
failure inclusion policy
paired-vs-independent comparison policy
```

Candidate rule:

> A reported resolution probability shall be reconstructable from trial-level event evidence and the exact event/condition contract.

---

## 29. Candidate Phase-1 `P_res` Profile

For the initial synthetic two-source stationary far-field narrowband DOA study, a conservative candidate is:

```text
truth: exact two-source point DOAs
resolution event: both sources obtain distinct admissible one-to-one matches
association: accepted 4.6 policy
resolution coordinate: declared theta-angle baseline
condition axes: separation, pair midpoint/locations, SNR, snapshots, source power/correlation, geometry/profile
failure policy: explicit per study; unconditional and conditional forms named separately
estimate: n_res / N_eligible under the declared event universe
uncertainty: required later under 4.11
search-grid / peak policy: fixed and recorded
oracle-K status: explicit
```

This remains candidate until ADR-004 acceptance.

---

## 30. Invalid / Weak `P_res` Evidence Cases

The following are scientifically weak or invalid unless explicitly justified:

1. define resolution as `two peaks exist` with no truth-based association;
2. divide by only successful algorithm runs while labeling the result unconditional `P_res`;
3. omit the number of trials;
4. pool different separations/SNRs and report one scalar without weights;
5. compare `P_res` across studies with incompatible SNR definitions;
6. claim a universal resolution limit from one chosen probability threshold without disclosure;
7. infer pair resolution from the product of marginal detection probabilities without dependence analysis;
8. ignore pair midpoint/endfire dependence when sweeping only angular separation;
9. silently enforce a monotonic curve after seeing noisy data;
10. change peak threshold/search grid between algorithms without declaring complete-pipeline comparison;
11. generalize ideal-sensor `P_res` to mismatched/calibrated hardware;
12. reuse favorable root seeds or discard unresolved trials;
13. treat incompatible/unidentifiable conditions as ordinary stochastic non-resolution without preserving status;
14. report `P_res=1` from a tiny trial count as conclusive evidence;
15. confuse deterministic beamwidth/Rayleigh-like criteria with empirical `P_res`.

---

## 31. Cross-ADR Reconciliation

### ADR-001

Resolution-condition coordinates inherit angle/direction-cosine semantics, visible-sector topology, aliasing, and midpoint/endfire geometry.

### ADR-002

SNR, snapshots, source covariance/coherence, noise statistics, source count, and finite-sample semantics define the probability law.

### ADR-003

Sensor/calibration profile, mismatch, coupling, colored noise, timing, and identifiability remain condition/provenance dimensions.

### ADR-004 Explorations 4.4–4.5

`P_res` is estimated over declared stochastic trials with reproducible trial identities and, for comparisons, deliberate pairing/CRN where appropriate.

### ADR-004 Exploration 4.6

Truth-to-estimate association defines admissible distinct matches.

### ADR-004 Exploration 4.8

The resolution event is a typed joint truth-group event distinct from localization accuracy and spectrum topology.

**Cross-ADR result: no contradiction identified.**

---

## 32. Candidate Decisions from Exploration 4.9

- **D4.9-01:** `P_res` is the probability of a predeclared resolution event under a declared condition and trial distribution.
- **D4.9-02:** Empirical `P_res` is `n_res/N` over an explicitly defined eligible trial universe.
- **D4.9-03:** Numerator/denominator and trial eligibility must be reconstructable from retained evidence.
- **D4.9-04:** Unconditional, valid-output-conditioned, and out-of-domain-excluded resolution probabilities are distinct metrics.
- **D4.9-05:** Resolution probability is condition-dependent and should generally be reported as a curve/surface over relevant variables rather than one scalar.
- **D4.9-06:** Source separation, midpoint/absolute location, coordinate (`theta` vs `u`), SNR, snapshots, source power/correlation, geometry, sensor/calibration profile, and postprocessing may all materially affect `P_res`.
- **D4.9-07:** Pairwise, designated-group, and all-source `P_res` are distinct event granularities.
- **D4.9-08:** `P_res` is not generally equal to a product of marginal source-detection probabilities.
- **D4.9-09:** A deterministic beamwidth/Rayleigh-like number is not the same evidence object as empirical `P_res`.
- **D4.9-10:** Derived thresholds such as `Delta theta_90` require a declared target probability, interpolation/monotonicity treatment, condition profile, and uncertainty analysis.
- **D4.9-11:** Empirical non-monotonicity shall remain visible unless a justified model explicitly imposes monotonicity.
- **D4.9-12:** Probability estimates require the denominator; adequacy/convergence and confidence methodology are deferred to 4.10/4.11.
- **D4.9-13:** Paired algorithm comparisons should retain paired binary resolution indicators under Common Random Numbers.
- **D4.9-14:** Aggregation across heterogeneous conditions requires explicit macro/micro/distribution weighting.
- **D4.9-15:** Publication-grade `P_res` preserves event, condition, failure policy, stochastic, algorithm, and sensor provenance.

---

## 33. Exploration 4.9 Conclusion

Exploration 4.9 is complete at candidate-contract level.

The central rule is:

> GeoDOA shall define Probability of Resolution as a condition-dependent probability of a predeclared joint resolution event over an auditable trial universe; empirical `P_res` shall retain denominator, failure/eligibility policy, association/event semantics, stochastic provenance, and condition axes, and shall remain distinct from deterministic resolution heuristics, localization RMSE, and marginal detection probabilities.

No acceptance gate is started or passed by this exploration.

The next exploration is:

```text
4.10 — Monte Carlo Adequacy and Convergence
```
