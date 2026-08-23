# ADR-004 Exploration 4.11 — Confidence Intervals and Metric Uncertainty

- **ADR:** ADR-004 — Validation, Reproducibility, and Scientific Evidence
- **Phase:** 0C — Scientific Foundations
- **Exploration:** 4.11
- **Status:** EXPLORATION COMPLETE — CANDIDATE CONTRACT, NOT ACCEPTED
- **Depends on:** Accepted ADR-001, ADR-002, ADR-003; ADR-004 Explorations 4.1–4.10

## 1. Question

> How shall GeoDOA quantify uncertainty in aggregate scientific metrics and comparative claims while keeping Monte Carlo sampling uncertainty, reference/measurement uncertainty, paired-comparison uncertainty, model uncertainty, and numerical uncertainty conceptually distinct?

This exploration establishes the uncertainty-reporting contract required before fair algorithm/geometry comparison is finalized in Exploration 4.12.

---

## 2. Core Principle

A reported point estimate such as

```text
RMSE = 1.2 deg
P_res = 0.91
bias = -0.15 deg
```

is incomplete whenever the scientific claim depends materially on finite-sample uncertainty.

Candidate rule:

> GeoDOA shall attach uncertainty to the quantity actually being claimed and shall state the uncertainty source, conditioning, interval/estimation method, and evidence denominator.

No one interval formula is valid for every metric or every dependence structure.

---

## 3. Uncertainty Taxonomy

GeoDOA shall distinguish at least the following uncertainty classes.

### 3.1 Monte Carlo sampling uncertainty

Uncertainty because only finitely many stochastic trials were sampled from the declared trial distribution.

Examples:

- uncertainty of empirical bias;
- uncertainty of MSE/RMSE;
- uncertainty of `P_D`;
- uncertainty of `P_res`;
- uncertainty of mean runtime over stochastic workloads.

### 3.2 Reference / measurement uncertainty

Uncertainty in the comparison reference itself.

Examples:

- rotary-stage angular accuracy;
- surveyed sensor position uncertainty;
- chamber instrumentation uncertainty;
- calibration-reference uncertainty.

### 3.3 Numerical / implementation uncertainty

Finite precision, approximation, solver tolerance, fixed-point quantization, interpolation, numerical conditioning, or nondeterministic execution may create numerical discrepancy.

### 3.4 Model / epistemic uncertainty

Uncertainty due to imperfect knowledge of the physical model or unvalidated assumptions.

Examples:

- unknown phase-center motion;
- uncertain mutual-coupling model;
- incomplete noise model;
- unmodeled environmental dependence.

### 3.5 Comparative uncertainty

Uncertainty in a difference, ratio, or ranking between methods/geometries.

### 3.6 Resampling / analysis uncertainty

Bootstrap, permutation, cross-validation, or other analysis procedures may introduce an additional stochastic layer.

Candidate rule:

> These uncertainty classes may interact, but they shall not be silently collapsed into a single generic `error bar` without a declared propagation model.

---

## 4. Confidence Interval versus Reference Uncertainty Interval

A confidence interval for a Monte Carlo metric and an instrument/reference uncertainty statement answer different questions.

For example:

```text
RMSE_MC = 0.42 deg, 95% CI [0.39, 0.45] deg
reference angle uncertainty = +/- 0.05 deg
```

The first describes uncertainty from finite stochastic sampling; the second describes uncertainty in the physical reference.

Candidate rule:

> Confidence intervals on Monte Carlo estimates shall not be interpreted automatically as total physical validation uncertainty.

---

## 5. Frequentist Confidence Semantics

If GeoDOA reports a frequentist confidence interval, the method and confidence level must be stated.

A 95% confidence procedure is a repeated-sampling coverage statement under its assumptions; it is not generally the statement

```text
there is a 95% probability that the fixed true parameter lies in this realized interval
```

under ordinary frequentist semantics.

Candidate rule:

> GeoDOA documentation shall avoid probabilistically incorrect interpretations of frequentist confidence intervals.

If future Bayesian credible intervals are used, they shall be labeled as such and inherit the declared prior/model assumptions.

---

## 6. Mean / Bias Uncertainty

For IID scalar errors `e_i`, empirical bias is

\[
\bar e = \frac{1}{N}\sum_{i=1}^N e_i.
\]

With finite sample standard deviation

\[
s_e^2
=\frac{1}{N-1}\sum_{i=1}^{N}(e_i-\bar e)^2,
\]

a classical standard-error estimate is

\[
\operatorname{SE}(\bar e)
=\frac{s_e}{\sqrt N}.
\]

For small samples under an approximately normal/appropriate setting, a Student-`t` interval may be considered:

\[
\bar e \pm t_{1-\alpha/2,N-1}\frac{s_e}{\sqrt N}.
\]

Candidate rule:

> This form is not universal; dependence, heavy tails, hierarchical trials, or selection-conditioned samples require compatible alternatives.

---

## 7. Probability Metrics: Wald Interval Is Not the Default

For a Bernoulli metric such as `P_res`, the naive Wald interval

\[
\hat p \pm z_{1-\alpha/2}\sqrt{\frac{\hat p(1-\hat p)}{N}}
\]

can perform poorly for small `N` or probabilities near 0 or 1.

Candidate rule:

> GeoDOA shall not adopt the Wald interval as a universal default for binomial event probabilities.

A bounded interval method with better finite-sample behavior—such as Wilson score or an exact/binomial-compatible method—shall be preferred for ordinary independent Bernoulli reporting, subject to final governing-ADR selection.

Phase 0C does not yet require one permanent library implementation.

---

## 8. Candidate Baseline for Independent Binomial Proportions

For ordinary independent Bernoulli event estimates, the Wilson score interval is a strong candidate baseline because it remains within `[0,1]` and behaves better than Wald in many finite-sample regimes.

For

\[
\hat p=\frac{x}{N}
\]

and normal quantile `z`, the Wilson center/half-width can be expressed as

\[
\tilde p
=
\frac{\hat p+z^2/(2N)}{1+z^2/N},
\]

\[
h
=
\frac{z}{1+z^2/N}
\sqrt{
\frac{\hat p(1-\hat p)}{N}
+\frac{z^2}{4N^2}
}.
\]

Then

\[
[\tilde p-h,\tilde p+h]
\]

is the Wilson interval.

Candidate rule:

> If the governing ADR later selects Wilson as the default independent-binomial interval, the method/version and confidence level shall remain provenance.

---

## 9. Zero-Event / All-Event Cases

Observing

```text
0 failures in N trials
```

or

```text
N successes in N trials
```

shall not collapse uncertainty to zero.

Candidate rule:

> Boundary event counts must use an interval procedure that retains nonzero uncertainty at finite `N`.

This directly supports Exploration 4.10's rule that `100/100` does not prove probability 1.

---

## 10. MSE Uncertainty

Empirical MSE is the sample mean of

\[
Z_i=e_i^2.
\]

Thus uncertainty in MSE is uncertainty in the mean of a nonnegative random variable that may be skewed or heavy-tailed.

Candidate rule:

> MSE uncertainty shall be assessed on the squared-error variable itself, with methods compatible with its empirical distribution and dependence structure.

A symmetric normal approximation may be acceptable in well-behaved large-`N` regimes, but it is not universal.

---

## 11. RMSE Uncertainty Is Nonlinear

RMSE is

\[
\operatorname{RMSE}=\sqrt{\operatorname{MSE}}.
\]

Therefore uncertainty in RMSE is a nonlinear transformation of MSE uncertainty.

Possible approaches include:

- transform an interval on MSE through the square root if the interval is valid/nonnegative;
- delta-method approximation in suitable regimes;
- bootstrap or another compatible resampling procedure when justified.

Candidate rule:

> GeoDOA shall not compute an RMSE confidence interval by simply adding/subtracting the MSE standard error in RMSE units.

---

## 12. Delta-Method Candidate for RMSE

If

\[
\hat m=\widehat{\operatorname{MSE}}
\]

is sufficiently regular and positive, with standard error `SE(m_hat)`, then for

\[
g(m)=\sqrt m,
\]

\[
g'(m)=\frac{1}{2\sqrt m}.
\]

A delta-method approximation gives

\[
\operatorname{SE}(\widehat{\operatorname{RMSE}})
\approx
\frac{\operatorname{SE}(\hat m)}{2\sqrt{\hat m}}.
\]

Candidate rule:

> This approximation is a candidate diagnostic for regular large-sample regimes, not a universal RMSE interval rule, especially near zero or under heavy tails.

---

## 13. Bootstrap Semantics

Bootstrap may be useful for nonlinear or difficult metric uncertainty.

But the resampling unit must follow the trial hierarchy.

Examples:

- ordinary IID trial bootstrap;
- paired bootstrap for algorithm comparisons;
- cluster/device bootstrap for hierarchical experiments;
- block bootstrap for dependent time/trial structure.

Candidate rule:

> Bootstrap shall resample the scientifically independent/effective unit, not blindly individual rows.

Resampling randomness is a separate RNG family under Exploration 4.5.

---

## 14. Bootstrap Is Not Automatically Valid

Bootstrap can fail or mislead when:

- sample size is tiny;
- tail events are too rare to have been observed;
- strong dependence is ignored;
- non-smooth estimators/events are treated naively;
- hierarchical structure is flattened;
- data selection has already conditioned away failures.

Candidate rule:

> GeoDOA shall not treat `bootstrap CI` as universally robust merely because it is nonparametric.

Method assumptions and resampling unit remain part of provenance.

---

## 15. Paired Scalar Comparisons

Under Common Random Numbers, let trial-level scalar performance quantities be

\[
X_t^{(A)},\quad X_t^{(B)}
\]

and define paired difference

\[
D_t=X_t^{(A)}-X_t^{(B)}.
\]

The primary comparative uncertainty should generally target

\[
E[D]
\]

rather than combine two independent marginal uncertainty bars.

Candidate rule:

> For paired designs, GeoDOA shall preserve and analyze pairing rather than discard it and pretend the methods were independent.

---

## 16. Paired Binary Comparisons

For binary outcomes such as resolution success, paired trial outcomes form four cells:

```text
A=1, B=1
A=1, B=0
A=0, B=1
A=0, B=0
```

Only discordant pairs directly inform the paired difference in success probability.

Candidate rule:

> Comparative uncertainty for paired binary outcomes shall use paired-event methodology rather than two unrelated binomial intervals when the scientific design is paired.

The governing ADR may later select a specific interval/test family; Phase 0C exploration does not freeze one software routine here.

---

## 17. Non-Overlap of Individual CIs Is Not the Comparison Test

A common weak practice is to conclude two methods differ only by visually checking overlap of their separate 95% confidence intervals.

Candidate rule:

> Method-comparison uncertainty shall be computed for the comparison quantity itself—difference, ratio, paired event contrast, etc.—not inferred from CI overlap heuristics.

---

## 18. Ratio Metrics

If a benchmark reports ratios such as

\[
\frac{\operatorname{RMSE}_A}{\operatorname{RMSE}_B},
\]

uncertainty may become highly nonlinear when the denominator is small or uncertain.

Candidate rule:

> Ratios require dedicated uncertainty treatment and denominator diagnostics; they shall not be treated as ordinary additive differences.

A log-ratio may be useful in some positive-metric comparisons, but no universal transformation is accepted here.

---

## 19. Multiple Conditions and Multiplicity

If a study examines many angles, SNR values, geometries, algorithms, and metrics, pointwise 95% intervals do not imply 95% simultaneous coverage over the entire family.

Candidate rule:

> GeoDOA shall distinguish pointwise uncertainty from simultaneous/family-level inference when broad claims depend on many comparisons.

No universal multiplicity correction is imposed in this exploration; the scientific claim determines whether adjustment or hierarchical summarization is needed.

---

## 20. Resolution Curves and `Delta theta_p`

If

\[
\widehat P_{\rm res}(\Delta\theta)
\]

is estimated at discrete separation points, uncertainty exists at each point and propagates into any derived threshold such as

\[
\Delta\theta_{90}.
\]

Candidate rule:

> A derived resolution threshold shall not be reported with false precision when the underlying probability curve has finite Monte Carlo uncertainty, grid spacing, interpolation, or non-monotonicity uncertainty.

The derived-threshold uncertainty method must be declared if such a scalar is used.

---

## 21. Reference-Uncertainty Propagation

Suppose a measured reference angle has uncertainty and estimator error is scored against it.

If an error model justifies independent zero-mean uncertainties,

\[
\sigma_{obs}^2
\approx
\sigma_{est}^2+\sigma_{ref}^2.
\]

But this relation is assumption-dependent and does not hold blindly for systematic bias, bounded errors, correlation, nonlinear transformations, or common calibration effects.

Candidate rule:

> Reference uncertainty shall be propagated only through a declared uncertainty model; no universal root-sum-square rule is accepted without its assumptions.

---

## 22. Systematic Reference Bias

Increasing Monte Carlo trial count does not remove systematic reference bias.

If

\[
\theta_{ref}=\theta_{phys}+b_{ref}+\eta_{ref},
\]

then `b_ref` can remain even as stochastic averaging drives Monte Carlo sampling uncertainty downward.

Candidate rule:

> Narrow Monte Carlo confidence intervals shall not be interpreted as evidence that systematic reference/model uncertainty is small.

---

## 23. Calibration Uncertainty

A calibration estimate may have uncertainty that propagates into downstream DOA performance.

Possible study designs include:

```text
fixed calibration artifact, noise trials vary
calibration re-estimated per device realization
joint calibration + measurement Monte Carlo
held-out validation after fixed calibration
```

These produce different uncertainty decompositions.

Candidate rule:

> Calibration uncertainty and measurement/noise Monte Carlo uncertainty shall remain distinguishable through the hierarchical trial contract.

---

## 24. Hierarchical Uncertainty

For device-to-device variation plus repeated noise trials, observations are clustered.

Naively treating all `D*T` outcomes as independent can yield overly narrow intervals.

Candidate rule:

> Uncertainty methods shall respect hierarchical/clustered trial structure and the actual unit of independent population sampling.

Possible future methods include random-effects models, cluster-robust procedures, hierarchical bootstrap, or explicit variance decomposition, depending on study design.

---

## 25. Finite Number of Devices

If only a few hardware devices are tested, thousands of repeated measurements on one device do not tightly characterize population-level device variation.

Candidate rule:

> Population claims across hardware units shall reflect the number of independent devices/assemblies, not merely the number of repeated captures.

---

## 26. Fixed-Point / FPGA Numerical Uncertainty

For deterministic sample-for-sample float/fixed/FPGA comparisons, the discrepancy may be deterministic rather than stochastic.

In that case a confidence interval may be inappropriate.

Candidate rule:

> Deterministic numerical bounds, maxima, quantiles over a test set, or exact mismatch counts may be more appropriate than statistical CIs when the evidence object is a deterministic regression suite.

Statistical uncertainty enters only when the stimulus/test set itself represents a stochastic sample from a population claim.

---

## 27. CI Width as a Stopping Criterion

Exploration 4.10 permits precision-based stopping.

A study may stop when a declared interval width/half-width target is reached, subject to minimum trial floors and sequential-design compatibility.

Candidate rule:

> If interval width drives stopping, the interval/stopping method must be compatible with repeated monitoring; a fixed-`N` confidence procedure shall not automatically be assumed valid under arbitrary optional stopping.

No universal sequential-CI method is frozen here.

---

## 28. Confidence Level Is Part of the Metric Record

`95% CI`, `90% CI`, and `99% CI` are different evidence statements.

Candidate rule:

> Confidence/coverage level shall be explicit and shall not be inferred from plotting conventions.

The repository shall not silently mix levels across methods within the same comparison.

---

## 29. One-Sided versus Two-Sided Intervals

Some engineering claims are one-sided, for example:

```text
P_res is at least 0.90
RMSE degradation is no more than 0.10 deg
failure probability is below 1e-3
```

Candidate rule:

> One-sided bounds may be scientifically preferable for bounded engineering requirements, but the direction, confidence level, and decision threshold must be predeclared or transparently reported.

---

## 30. Equivalence / Noninferiority versus Difference

A lack of statistically clear difference does not prove equivalence.

For implementation validation, the claim may instead be:

```text
FPGA degradation is within accepted tolerance delta
```

Candidate rule:

> Equivalence/noninferiority claims require an explicit practical tolerance/margin and an uncertainty procedure targeted to that claim; `not significantly different` is not equivalent to `equivalent`.

This will be important in Exploration 4.15.

---

## 31. Practical Significance versus Statistical Significance

With very large `N`, tiny differences can be statistically detectable but operationally irrelevant.

With small `N`, large practically important differences may remain statistically uncertain.

Candidate rule:

> GeoDOA shall distinguish statistical uncertainty from engineering/practical significance; benchmark acceptance margins are separate from confidence levels.

This preserves the `metric != acceptance threshold` rule from Exploration 4.1.

---

## 32. Uncertainty for Success-Conditioned Metrics

If RMSE is computed only on matched detections, its uncertainty is conditional on the success-selection process.

Candidate rule:

> A confidence interval for matched-only RMSE does not account by itself for uncertainty in the detection/miss process; the conditioning and matched denominator must accompany the interval.

If the success mechanism differs between algorithms, comparing only these conditional intervals can be misleading.

---

## 33. Tail and Quantile Uncertainty

If catastrophic-error probability or high quantiles are reported, uncertainty can be much larger than for means.

Candidate rule:

> Tail metrics require metric-specific uncertainty evidence and sufficient tail event counts; ordinary mean-based confidence formulas are not automatically applicable.

---

## 34. Transformations and Units

If a metric is transformed, uncertainty must transform consistently.

Example:

\[
\theta_{deg}=\frac{180}{\pi}\theta_{rad}.
\]

A confidence interval on angular RMSE transforms with the same first-power scale as RMSE, whereas an interval on MSE transforms with the squared scale.

Candidate rule:

> Uncertainty intervals inherit the dimensional transformation of the underlying metric.

---

## 35. Reporting Point Estimate + Interval + Counts

For event probabilities, a strong minimal record is conceptually:

```text
P_res_hat = 0.91
95% interval = [...]
resolved = 910
eligible = 1000
method = Wilson (candidate baseline)
condition = ...
```

For localization:

```text
RMSE_hat = ... deg
95% interval = [...]
matched pair count = ...
trial count = ...
association/conditioning = ...
uncertainty method = ...
```

Candidate rule:

> Intervals shall not replace raw event/trial counts and conditioning provenance.

---

## 36. Uncertainty Provenance

Publication-grade uncertainty evidence should preserve, as applicable:

```text
metric identity/version
point estimate
uncertainty class
interval/bound method
coverage/confidence level
one-sided/two-sided semantics
sample/trial count
independence/dependence assumptions
cluster/hierarchy level
pairing policy
bootstrap/resampling seed and unit
reference uncertainty source/model
stopping rule interaction
software/library method/version
```

Candidate rule:

> An interval is itself a derived scientific artifact with provenance, not decoration added to a plot.

---

## 37. Candidate Phase-1 Uncertainty Profile

For initial synthetic DOA Monte Carlo studies, a conservative candidate profile is:

```text
bias: report point estimate + compatible mean uncertainty
P_D / P_res: bounded binomial-compatible interval; Wilson is candidate baseline for independent Bernoulli trials
MSE/RMSE: retain trial-level squared errors; use a declared regular large-sample or resampling method compatible with the distribution
paired method comparison: analyze paired differences/events directly
reference uncertainty: not applicable for exact synthetic truth; required separately for physical validation
failure/miss conditioning: explicit
confidence level: explicit
trial/event counts: mandatory
hierarchical dependence: preserve if introduced
```

This remains candidate until ADR-004 acceptance.

---

## 38. Invalid / Weak Uncertainty Cases

The following are scientifically weak or invalid unless explicitly justified:

1. report a point metric without denominator when finite-sample uncertainty matters;
2. use Wald binomial intervals universally, including tiny samples and boundary probabilities;
3. report `100/100 -> P=1 with zero uncertainty`;
4. compare two paired algorithms using independent uncertainty analysis and discard pairing;
5. conclude significance/non-significance from overlap/non-overlap of marginal CIs alone;
6. treat a Monte Carlo CI as total physical validation uncertainty;
7. ignore systematic reference bias because Monte Carlo CI is narrow;
8. bootstrap individual rows from clustered/device data as if IID;
9. claim hardware equivalence because `p>0.05` or because a difference was not detected;
10. use one confidence level for one method and another for its comparator without disclosure;
11. apply arbitrary optional stopping while reporting a fixed-`N` interval as if unaffected;
12. give an RMSE interval using MSE-unit uncertainty without nonlinear transformation;
13. omit interval method/version from publication-grade evidence;
14. report a precise `Delta theta_90` while ignoring uncertainty and separation-grid granularity;
15. treat model uncertainty as if it were reducible simply by increasing Monte Carlo `N`.

---

## 39. Cross-ADR Reconciliation

### ADR-001

Metric/uncertainty units and coordinate transformations inherit angle/direction conventions and dimensional semantics.

### ADR-002

Trial dependence, source/noise statistics, snapshots, covariance, and source correlation determine whether IID assumptions are valid.

### ADR-003

Calibration, sensor mismatch, physical-reference uncertainty, device variation, and model uncertainty remain distinct from ordinary Monte Carlo noise.

### ADR-004 Exploration 4.5

Resampling/bootstrap randomness has separate RNG provenance; paired CRN designs preserve pair identity.

### ADR-004 Exploration 4.7

Bias/MSE/RMSE definitions and conditioning determine the target quantity whose uncertainty is estimated.

### ADR-004 Explorations 4.8–4.9

Event-probability uncertainty inherits exact detection/resolution event and denominator semantics.

### ADR-004 Exploration 4.10

Precision targets and stopping rules use uncertainty evidence but do not redefine the metric itself.

**Cross-ADR result: no contradiction identified.**

---

## 40. Candidate Decisions from Exploration 4.11

- **D4.11-01:** Monte Carlo sampling, reference/measurement, numerical, model/epistemic, comparative, and resampling uncertainties are distinct classes.
- **D4.11-02:** A Monte Carlo confidence interval is not automatically total physical-validation uncertainty.
- **D4.11-03:** Frequentist confidence intervals shall be interpreted according to repeated-sampling coverage semantics; Bayesian intervals, if used, shall be labeled separately.
- **D4.11-04:** Mean/bias uncertainty methods shall respect dependence, tail behavior, and hierarchy; the ordinary `s/sqrt(N)` form is conditional, not universal.
- **D4.11-05:** Wald binomial intervals are not accepted as a universal default; a bounded finite-sample method such as Wilson is the candidate independent-Bernoulli baseline.
- **D4.11-06:** Boundary event counts retain finite uncertainty; `0/N` and `N/N` do not imply exact probabilities 0 or 1.
- **D4.11-07:** MSE uncertainty targets the squared-error distribution; RMSE uncertainty requires nonlinear transformation/resampling treatment.
- **D4.11-08:** Bootstrap must resample the scientifically appropriate independent/cluster/block unit and is not universally valid.
- **D4.11-09:** Paired designs shall analyze paired differences/events rather than discard pairing.
- **D4.11-10:** Comparison uncertainty targets the difference/ratio/contrast itself; marginal-CI overlap is not a comparison test.
- **D4.11-11:** Pointwise and simultaneous/family-level uncertainty are distinct when many conditions/comparisons support a broad claim.
- **D4.11-12:** Derived resolution thresholds inherit uncertainty from probability estimates, grid spacing, and interpolation/modeling choices.
- **D4.11-13:** Reference/calibration uncertainty requires a declared propagation model and is not reduced merely by increasing Monte Carlo trials.
- **D4.11-14:** Hierarchical/device studies require uncertainty methods compatible with clustered population sampling.
- **D4.11-15:** Deterministic regression evidence may require deterministic bounds rather than confidence intervals.
- **D4.11-16:** Precision-based sequential stopping requires inference-compatible interval/stopping semantics.
- **D4.11-17:** Equivalence/noninferiority claims require explicit engineering margins; failure to detect a difference does not establish equivalence.
- **D4.11-18:** Statistical significance and practical engineering significance remain distinct.
- **D4.11-19:** Publication-grade uncertainty records preserve method, level, counts, dependence, pairing, hierarchy, reference uncertainty, stopping interaction, and software provenance.

---

## 41. Exploration 4.11 Conclusion

Exploration 4.11 is complete at candidate-contract level.

The central rule is:

> GeoDOA shall attach uncertainty to the exact scientific metric or comparison being claimed using a method compatible with its event/error distribution, conditioning, pairing, hierarchy, dependence, stopping rule, and reference model; Monte Carlo confidence, physical-reference uncertainty, numerical discrepancy, and model uncertainty shall remain distinct evidence objects, and no narrow interval shall by itself establish physical validity or engineering equivalence.

No acceptance gate is started or passed by this exploration.

The next exploration is:

```text
4.12 — Fair Algorithm and Geometry Comparison
```
