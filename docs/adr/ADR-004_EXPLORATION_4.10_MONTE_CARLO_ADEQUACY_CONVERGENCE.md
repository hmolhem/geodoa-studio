# ADR-004 Exploration 4.10 — Monte Carlo Adequacy and Convergence

- **ADR:** ADR-004 — Validation, Reproducibility, and Scientific Evidence
- **Phase:** 0C — Scientific Foundations
- **Exploration:** 4.10
- **Status:** EXPLORATION COMPLETE — CANDIDATE CONTRACT, NOT ACCEPTED
- **Depends on:** Accepted ADR-001, ADR-002, ADR-003; ADR-004 Explorations 4.1–4.9

## 1. Question

> How shall GeoDOA decide whether a Monte Carlo study has enough trials, whether an aggregate metric has converged sufficiently for its intended claim, and whether additional trials are needed without relying on arbitrary fixed trial counts?

This exploration defines adequacy and convergence semantics. Exact confidence-interval methods are deferred to Exploration 4.11.

---

## 2. Core Principle

There is no universal scientifically valid rule such as

```text
100 trials is enough
1000 trials is enough
10000 trials is always enough
```

for all GeoDOA studies.

Monte Carlo adequacy depends on at least:

```text
metric type
required precision
confidence target
true/observed event probability
tail behavior / catastrophic outliers
condition difficulty
trial dependence
effective sample size
failure rate
paired vs independent design
number of conditions/comparisons
computational budget
intended scientific claim
```

Candidate rule:

> Trial count shall be justified by uncertainty and convergence evidence relative to the intended claim, not by a universal constant.

---

## 3. What Monte Carlo Convergence Means

Let `M_N` be an aggregate statistic computed after `N` eligible trials.

Examples include:

\[
\widehat{\mathrm{Bias}}_N,
\quad
\widehat{\mathrm{MSE}}_N,
\quad
\widehat{\mathrm{RMSE}}_N,
\quad
\widehat P_{D,N},
\quad
\widehat P_{\rm res,N}.
\]

Monte Carlo convergence concerns stability of the estimator of the population performance quantity as evidence accumulates.

Candidate rule:

> Convergence of an aggregate statistic is not the same as algorithmic convergence of an optimizer, eigensolver, iterative estimator, or calibration routine.

These concepts shall remain distinct.

---

## 4. Law-of-Large-Numbers Intuition Is Necessary but Not Sufficient

For suitable IID or ergodic conditions,

\[
M_N \to M
\]

as `N` grows.

But publication-grade adequacy requires more than invoking asymptotic convergence.

GeoDOA must still establish:

- what population quantity `M` means;
- whether trial assumptions support the chosen estimator;
- how precise `M_N` needs to be;
- whether finite-`N` evidence is stable enough for the stated claim.

Candidate rule:

> Asymptotic consistency does not by itself justify a finite trial count.

---

## 5. Running Estimates as Diagnostics

A basic convergence diagnostic is the running statistic

\[
M_n,
\qquad n=1,2,\dots,N.
\]

For example,

\[
\widehat{\mathrm{MSE}}_n
=
\frac{1}{n}\sum_{i=1}^{n} e_i^2.
\]

Likewise,

\[
\widehat P_{\rm res,n}
=
\frac{1}{n}\sum_{i=1}^{n} R_i.
\]

Candidate rule:

> Running estimates are useful diagnostics but visual flatness alone is not a sufficient adequacy criterion.

A curve can appear flat while still having uncertainty too large for the intended comparison.

---

## 6. Batch / Block Stability

Trials may be partitioned into deterministic analysis blocks of size `B` for convergence diagnostics.

For block `b`, compute a block statistic

\[
M^{(b)}.
\]

Large systematic disagreement among later blocks suggests insufficient evidence, nonstationarity, hidden dependence, or rare-event sensitivity.

Candidate rule:

> Batch stability may support convergence diagnosis, but block size and interpretation shall be declared and shall not replace formal uncertainty estimates.

---

## 7. Adequacy Is Metric-Specific

A trial count adequate for mean bias may be inadequate for a rare failure probability.

Examples:

- estimating a mean near the center of a light-tailed distribution;
- estimating RMSE dominated by rare catastrophic errors;
- estimating `P_res≈0.5`;
- estimating `P_res≈0.99`;
- estimating a 99.9th percentile;
- comparing two algorithms whose expected difference is very small.

Candidate rule:

> One study may require different adequacy assessments for different reported metrics.

---

## 8. Probability Metrics — Variance Scale

For an IID Bernoulli event `R_t` with probability `p`,

\[
\widehat p
=
\frac{1}{N}\sum_{t=1}^N R_t
\]

has variance

\[
\operatorname{Var}(\widehat p)
=
\frac{p(1-p)}{N}.
\]

The standard-error scale is therefore

\[
\operatorname{SE}(\widehat p)
\approx
\sqrt{\frac{p(1-p)}{N}}.
\]

The maximum Bernoulli variance occurs at

\[
p=0.5,
\]

giving the worst-case standard-error scale

\[
\operatorname{SE}_{\max}
=
\frac{1}{2\sqrt N}.
\]

Candidate rule:

> This formula is a planning/diagnostic scale under the declared Bernoulli assumptions, not a universal confidence-interval method.

Formal interval selection is deferred to Exploration 4.11.

---

## 9. Rough Probability Trial-Count Planning

If an approximate standard-error target `s_target` is used for planning and worst-case `p=0.5` is assumed,

\[
N
\gtrsim
\frac{1}{4s_{\rm target}^2}.
\]

Examples:

```text
SE target 0.05  -> N approximately 100
SE target 0.02  -> N approximately 625
SE target 0.01  -> N approximately 2500
```

These are rough planning values, not universal publication thresholds.

Candidate rule:

> Planning calculations may guide initial trial budgets, but final adequacy shall use the observed study structure and the actual claim.

---

## 10. Near-Zero / Near-One Event Probabilities

When `p` is near 0 or 1, observing no failures or no successes in a small sample does not prove the corresponding probability is exactly 0 or 1.

Example:

```text
100/100 resolved
```

supports a high resolution probability but does not establish

\[
P_{\rm res}=1.
\]

Candidate rule:

> Zero observed failures or successes shall be reported as finite-sample evidence, not as proof of zero or unit population probability.

Confidence bounds are deferred to 4.11.

---

## 11. Rare Events Require Event Counts, Not Only Percentages

For rare failures, reporting

```text
failure rate = 0.1%
```

without stating that it came from, for example, `1/1000` trials is inadequate.

Candidate rule:

> Rare-event evidence shall report event counts and denominators explicitly.

A rate based on one observed event is highly uncertain even when `N` appears numerically large.

---

## 12. RMSE / MSE Convergence

For localization errors `e_i`,

\[
\widehat{\mathrm{MSE}}_N
=
\frac{1}{N}\sum e_i^2.
\]

Thus convergence of MSE depends on the distribution of the squared-error variable

\[
Z=e^2.
\]

If `Z` has large variance or a heavy tail, MSE/RMSE may require many more trials than bias.

Candidate rule:

> Adequacy for RMSE shall consider the variability/tail behavior of squared errors, not only the apparent stability of signed error means.

---

## 13. Catastrophic Errors and Heavy Tails

A DOA estimator may behave well on most trials but occasionally lock onto a sidelobe or alias, creating a very large squared error.

Because RMSE squares errors, rare catastrophes can dominate the metric.

Candidate requirements:

- retain catastrophic trials;
- inspect error distribution/tail diagnostics;
- do not stop early merely because no catastrophe has yet occurred;
- report catastrophic-event rates or quantiles when scientifically relevant.

Candidate rule:

> Early apparent RMSE stability before rare-event discovery is not strong convergence evidence.

---

## 14. Bias Convergence Can Be Misleading Through Cancellation

Signed errors may cancel:

\[
+2^\circ,-2^\circ,+2^\circ,-2^\circ
\]

giving near-zero bias while dispersion remains large.

Candidate rule:

> Convergence of bias alone shall never be used as evidence that localization performance as a whole has converged.

MSE/RMSE, spread, detection/failure metrics, and condition diagnostics remain separate.

---

## 15. Condition-Wise Adequacy

If a study contains multiple conditions `c`, each condition has its own evidence count

\[
N_c.
\]

A large global trial count

\[
N_{\rm total}=\sum_c N_c
\]

does not guarantee each condition is adequately sampled.

Candidate rule:

> Adequacy shall be assessed at the finest condition granularity required by the scientific claim.

A dense easy-region study shall not compensate silently for weak evidence near the resolution boundary.

---

## 16. Transition Regions Often Need More Evidence

For probability metrics such as `P_res`, the statistical variance of a Bernoulli estimator is largest near `p=0.5`.

Therefore transition regions around the resolution threshold may require more trials than obvious `p≈0` or `p≈1` regions if a uniform precision target is desired.

Candidate rule:

> Adaptive trial allocation across conditions is permitted when its policy is predeclared or transparently recorded and does not bias the estimator.

---

## 17. Adaptive Monte Carlo Allocation

A study may begin with `N0` trials per condition and allocate additional trials where uncertainty remains high.

Conceptually:

```text
initial trial block
      ↓
uncertainty / convergence assessment
      ↓
more trials for unresolved conditions
      ↓
stop when declared criterion is met or budget exhausted
```

Candidate requirements:

- stopping/allocation rule declared;
- all trials retained;
- no preferential deletion;
- final per-condition counts reported;
- statistical interpretation consistent with the sequential design.

Detailed sequential interval implications are deferred to 4.11.

---

## 18. Fixed-Budget Studies

Sometimes computational cost imposes a fixed maximum trial count.

Candidate rule:

> If the trial budget is exhausted before the desired precision is achieved, GeoDOA shall report the remaining uncertainty rather than silently declaring convergence.

`budget-limited` and `precision-qualified` are different evidence statuses.

---

## 19. Absolute versus Relative Precision Targets

For a metric `M`, adequacy may be based on an absolute tolerance

\[
\delta_{abs}
\]

or relative tolerance

\[
\delta_{rel}\,|M|.
\]

Near zero, relative tolerances can become unstable or meaningless.

Candidate rule:

> Precision targets shall state whether they are absolute, relative, or hybrid and shall respect the scale/units of the metric.

No universal precision threshold is accepted here.

---

## 20. Comparison Claims Need Difference Precision

Suppose two algorithms have RMSEs

```text
A = 1.02 deg
B = 1.00 deg
```

The observed ranking is not scientifically strong unless uncertainty in the difference is sufficiently small.

For paired Common Random Numbers designs, evidence should focus on trial-level paired differences/events where appropriate.

Candidate rule:

> Adequacy for a comparative claim is adequacy of the comparison quantity, not merely separate convergence of each method's marginal metric.

Detailed comparative uncertainty is deferred to 4.11 and 4.12.

---

## 21. Paired Designs Can Improve Efficiency

When methods share exogenous realizations, paired differences may have lower variance than independent comparisons.

For scalar trial metrics `X_A` and `X_B`, define

\[
D=X_A-X_B.
\]

Then

\[
\operatorname{Var}(D)
=
\operatorname{Var}(X_A)
+
\operatorname{Var}(X_B)
-2\operatorname{Cov}(X_A,X_B).
\]

Positive covariance from common trials can reduce the variance of the difference.

Candidate rule:

> Trial-count adequacy shall respect paired versus independent comparison design.

---

## 22. Dependence Reduces Effective Evidence

If trials are correlated, nominal trial count `N` may overstate effective information.

This can occur with:

- reused noise blocks;
- overlapping time windows;
- shared device realizations;
- correlated source sequences;
- hierarchical random effects;
- repeated measurements without full re-randomization.

Candidate rule:

> Nominal `N` shall not be interpreted as IID effective sample size when the trial contract includes dependence.

A universal effective-sample-size formula is not imposed here because the dependence structure is study-specific.

---

## 23. Hierarchical Monte Carlo Adequacy

Suppose a study simulates `D` devices, each with `T` noise trials:

\[
N=D\times T.
\]

If device variation is a major population uncertainty, increasing `T` while keeping `D=1` does not adequately sample the device ensemble.

Candidate rule:

> Hierarchical studies shall assess adequacy at each scientifically relevant random-effect level, not only by total trial count.

---

## 24. Replication across Root Seeds

Changing the root seed creates another sample from the same declared stochastic model.

Independent reruns with different root seeds can diagnose sensitivity to one realization ensemble.

Candidate rule:

> Replication across root seeds is supporting robustness evidence but does not substitute for adequate total sampling under the declared design.

The seeds and allocation must remain provenance.

---

## 25. Stopping Rules Must Be Predeclared or Fully Transparent

Stopping a simulation when a favorable ranking appears can bias evidence.

Candidate rule:

> Sequential stopping based on observed metrics is permitted only under a declared/transparent rule compatible with the intended inference; otherwise a fixed predeclared trial count should be used.

Examples of weak practice:

```text
run until method A looks better
stop after 20 consecutive successes
stop when the plotted curve looks smooth
```

without a scientific stopping contract.

---

## 26. Running Convergence Thresholds

A practical engineering diagnostic may compare recent estimates:

\[
|M_N-M_{N-B}| < \epsilon.
\]

But this alone is insufficient because two nearby running estimates can occur by chance.

Candidate rule:

> Incremental stability thresholds may be used as diagnostics or one component of a stopping rule, but they shall be paired with uncertainty/coverage evidence appropriate to the metric.

---

## 27. Multiple Conditions and Multiple Metrics

A benchmark may test hundreds of conditions and metrics.

If a stopping rule is applied independently to each one, some conditions may appear converged by chance.

Candidate rule:

> Large benchmark families shall preserve per-condition/metric adequacy status and avoid implying uniform precision unless such precision was actually targeted and demonstrated.

Multiple-comparison inference is deferred to 4.11/4.12 where relevant.

---

## 28. Convergence Status Is Typed

Candidate conceptual statuses:

```text
PRECISION_TARGET_MET
BUDGET_LIMITED
INSUFFICIENT_TRIALS
RARE_EVENT_UNRESOLVED
DEPENDENCE_UNRESOLVED
NONSTATIONARITY_SUSPECTED
TAIL_UNSTABLE
CONVERGENCE_NOT_ASSESSED
```

These are conceptual evidence states, not final software enums.

Candidate rule:

> A run shall not be labeled simply `converged=True` when the scientific reason/target is unknown.

---

## 29. Minimum Trial Counts May Still Exist as Safety Floors

A profile may impose a minimum trial floor before any precision-based stopping check is allowed.

This is useful to prevent pathological early stopping.

Candidate rule:

> Minimum floors are profile/study safeguards, not universal proof of adequacy.

For example, a study may require at least `N_min` trials **and** satisfy an uncertainty target.

No global `N_min` is accepted in this exploration.

---

## 30. Pilot Studies

A pilot run can estimate variance, event rates, runtime, and tail behavior to plan the full trial budget.

Candidate rule:

> Pilot evidence used for design/tuning shall be distinguished from final held-out benchmark evidence when independence matters.

If pilot trials are included in the final estimate, that reuse shall be explicit and statistically compatible with the design.

---

## 31. Hardware Runtime and Monte Carlo Budget

FPGA/SoC acceleration may permit far larger Monte Carlo studies than software-only execution.

However computational throughput does not change the scientific definition of adequacy.

Candidate rule:

> Faster hardware may reduce the cost of reaching an evidence target; it does not lower the evidence target itself.

Similarly, a slow implementation does not justify weak uncertainty claims.

---

## 32. Reproducible Convergence Diagnostics

Convergence diagnostics shall be reconstructable from retained trial identities and cumulative order semantics.

Because trials are semantically keyed, GeoDOA can define a canonical analysis order, e.g. by trial index, even when execution was parallel/out-of-order.

Candidate rule:

> Diagnostic curves shall use a declared canonical trial ordering rather than scheduler completion order.

---

## 33. Monte Carlo Ordering versus IID Exchangeability

Under IID sampling, trial order is statistically exchangeable, but running curves still depend numerically on order.

Candidate rule:

> Running convergence plots are diagnostic views of one ordered realization sequence, not invariant scientific observables; final aggregate metrics should remain order-independent when their definitions are symmetric in trials.

---

## 34. Recommended Adequacy Evidence Package

A publication-grade Monte Carlo condition should preserve, as applicable:

```text
requested trial count
eligible trial count
completed trial count
failure/exclusion counts
metric-specific effective count
running metric history or checkpoints
uncertainty target
stopping rule
final stopping reason
batch/block diagnostics
rare-event counts
tail/outlier diagnostics
paired/independent design
hierarchical allocation counts
root seed / trial identities
budget limit, if any
adequacy status
```

Candidate rule:

> Trial count without stopping/uncertainty context is incomplete evidence when a convergence claim is made.

---

## 35. Candidate Phase-1 Adequacy Profile

For initial synthetic DOA Monte Carlo studies, a conservative candidate is:

```text
trial semantics: accepted 4.4
RNG/replay: accepted 4.5
condition-level trial counts: explicit
probability metrics: report event counts and denominators
RMSE/MSE: retain trial-level squared errors and tail diagnostics
running/batch diagnostics: available for key metrics
precision target: declared per study/metric
minimum safety floor: study-specific, if used
stopping: fixed-N or declared precision/budget rule
failure/incompatibility counts: retained
paired comparison: preserve CRN pairing
convergence status: typed, not a bare bool
```

This remains candidate until ADR-004 acceptance.

---

## 36. Invalid / Weak Adequacy Cases

The following are scientifically weak or invalid unless explicitly justified:

1. `N=1000` declared adequate solely because 1000 sounds large;
2. report probability without denominator/event count;
3. claim `P=1` because all 20 trials succeeded;
4. stop when the preferred algorithm first becomes better;
5. assess convergence only from a visually flat running curve;
6. pool all conditions to justify weak evidence at hard conditions;
7. ignore trial dependence and treat nominal `N` as IID effective sample size;
8. increase only within-device trials when device-to-device variation is the target population;
9. discard rare catastrophic errors as outliers merely to stabilize RMSE;
10. declare convergence after budget exhaustion without reporting remaining uncertainty;
11. use scheduler completion order to define stochastic convergence history;
12. claim equal adequacy for bias, RMSE, and rare-event probability from one undifferentiated trial count;
13. compare two algorithms based on tiny observed metric difference without assessing uncertainty of the difference;
14. adaptively allocate/stop trials but omit the allocation/stopping rule;
15. reuse pilot/tuning evidence as independent final validation without disclosure.

---

## 37. Cross-ADR Reconciliation

### ADR-001

Condition-resolved adequacy may depend on angle/direction coordinate and field-of-view location; no contradiction.

### ADR-002

Trial independence, snapshot dependence, source/noise statistics, and hierarchical temporal structure define the stochastic law used by Monte Carlo evidence.

### ADR-003

Device-static sensor imperfections versus trial-varying noise can create hierarchical ensembles requiring separate adequacy at each level.

### ADR-004 Exploration 4.4

Adequacy counts scientifically defined trials, not loop iterations.

### ADR-004 Exploration 4.5

Stable trial identities and CRN pairing permit reproducible accumulation, resume, and paired comparison.

### ADR-004 Explorations 4.7–4.9

Metric-specific adequacy applies separately to localization moments, detection probabilities, and resolution probabilities.

**Cross-ADR result: no contradiction identified.**

---

## 38. Candidate Decisions from Exploration 4.10

- **D4.10-01:** No universal Monte Carlo trial count is accepted as sufficient across GeoDOA studies.
- **D4.10-02:** Adequacy is metric-, condition-, precision-, dependence-, and claim-specific.
- **D4.10-03:** Monte Carlo convergence is distinct from internal algorithmic/iterative convergence.
- **D4.10-04:** Running and block statistics are diagnostics, not sufficient standalone proof of adequacy.
- **D4.10-05:** Probability-metric planning may use Bernoulli standard-error scale, but final interval methodology is deferred to 4.11.
- **D4.10-06:** Zero observed failures/successes do not prove population probability zero/one.
- **D4.10-07:** RMSE adequacy depends on squared-error tail behavior and may be dominated by rare catastrophic errors.
- **D4.10-08:** Adequacy shall be assessed per scientifically relevant condition; total pooled `N` may be misleading.
- **D4.10-09:** Adaptive trial allocation is allowed only with transparent allocation/stopping policy and retained evidence.
- **D4.10-10:** Budget exhaustion and precision-qualified stopping are distinct statuses.
- **D4.10-11:** Comparative adequacy concerns uncertainty of the comparison quantity, especially under paired CRN designs.
- **D4.10-12:** Trial dependence reduces effective information; nominal `N` shall not silently imply IID evidence.
- **D4.10-13:** Hierarchical Monte Carlo studies require sampling adequacy at each relevant random-effect level.
- **D4.10-14:** Sequential stopping based on observed outcomes requires a declared inference-compatible rule.
- **D4.10-15:** Convergence status shall be typed rather than represented by an unexplained boolean.
- **D4.10-16:** Pilot, tuning, and final evidence roles remain distinct when independence matters.
- **D4.10-17:** Hardware acceleration changes evidence cost, not scientific adequacy requirements.
- **D4.10-18:** Reproducible running diagnostics use canonical trial identity/order rather than execution completion order.

---

## 39. Exploration 4.10 Conclusion

Exploration 4.10 is complete at candidate-contract level.

The central rule is:

> GeoDOA shall judge Monte Carlo adequacy through metric-specific uncertainty and convergence evidence at the relevant condition and hierarchy levels, with explicit trial counts, dependence assumptions, stopping/allocation policy, rare-event/tail diagnostics, and typed stopping status; no fixed trial count, visually flat curve, or exhausted compute budget shall by itself establish adequate scientific evidence.

No acceptance gate is started or passed by this exploration.

The next exploration is:

```text
4.11 — Confidence Intervals and Metric Uncertainty
```
