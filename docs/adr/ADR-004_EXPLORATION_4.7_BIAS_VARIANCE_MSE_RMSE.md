# ADR-004 Exploration 4.7 — Bias, Variance, MSE, and RMSE

- **ADR:** ADR-004 — Validation, Reproducibility, and Scientific Evidence
- **Phase:** 0C — Scientific Foundations
- **Exploration:** 4.7
- **Status:** EXPLORATION COMPLETE — CANDIDATE CONTRACT, NOT ACCEPTED
- **Depends on:** Accepted ADR-001, ADR-002, ADR-003; ADR-004 Explorations 4.1–4.6
- **Golden Reference reservation:** GRP-018 — Bias, Variance, MSE, and RMSE by hand

## 1. Question

> How shall GeoDOA define, estimate, aggregate, and report bias, variance, MSE, and RMSE so that the reported quantities have unambiguous probability space, units, conditioning, association semantics, failure coverage, and finite-Monte-Carlo interpretation?

This exploration establishes the localization-error contract used by later Monte Carlo studies. It does **not** define a universal success threshold or miss/false-detection penalty.

---

## 2. Core Principle

A number labeled `RMSE` is scientifically incomplete unless GeoDOA can answer:

```text
error of what quantity?
relative to what truth/reference?
in what coordinate and units?
over what population/condition distribution?
after what multi-source association?
which trials are included?
how are failures/misses handled?
what weighting is used?
how many trials contributed?
```

Candidate rule:

> Bias, variance, MSE, and RMSE are properties of a declared error random variable under a declared experiment distribution; they are not context-free properties of an algorithm.

---

## 3. Scalar Error Variable

For one valid matched scalar estimate in trial `i`, define

\[
e_i = \hat q_i-q_i,
\]

where `q` may be angle, direction cosine, range, delay, or another declared quantity.

For the Phase-1 angular DOA profile:

\[
e_{\theta,i}=\hat\theta_i-\theta_i.
\]

The sign convention is therefore explicit:

```text
positive error -> estimate greater than reference
negative error -> estimate less than reference
```

Candidate rule:

> Signed error definition shall be fixed before bias is computed; absolute error is not bias.

---

## 4. Population Bias

For a fixed truth value `q0`, estimator bias is

\[
\operatorname{Bias}(\hat q\mid q_0)
=E[\hat q\mid q_0]-q_0
=E[e\mid q_0].
\]

More generally, if truth varies across a declared study distribution,

\[
\operatorname{Bias}_{\mathcal P}=E_{\mathcal P}[\hat q-q].
\]

These are different scientific statements.

Candidate rule:

> GeoDOA shall distinguish conditional bias at a declared condition from bias averaged across a condition distribution.

A broad aggregate bias can cancel positive and negative regional biases and therefore shall not replace condition-resolved diagnostics when spatial dependence is material.

---

## 5. Population Variance

For fixed truth `q0`, estimator variance is

\[
\operatorname{Var}(\hat q\mid q_0)
=E\!\left[\left(\hat q-E[\hat q\mid q_0]\right)^2\middle|q_0\right].
\]

Because subtracting a constant truth does not change variance,

\[
\operatorname{Var}(e\mid q_0)=\operatorname{Var}(\hat q\mid q_0).
\]

Variance measures spread around the estimator mean; it does not measure displacement of that mean from truth.

---

## 6. Population MSE and RMSE

For scalar error

\[
\operatorname{MSE}(\hat q)
=E[e^2]
=E[(\hat q-q)^2].
\]

For fixed truth `q0`, the familiar decomposition is

\[
\boxed{
\operatorname{MSE}
=
\operatorname{Var}(\hat q)
+
\operatorname{Bias}(\hat q)^2
}
\]

under the same probability law/conditioning.

RMSE is

\[
\boxed{
\operatorname{RMSE}=\sqrt{\operatorname{MSE}}
}
\]

and therefore has the same physical units as `q`.

For angular DOA reported in degrees:

```text
Bias: degrees
standard deviation: degrees
MSE: degrees^2
RMSE: degrees
```

Candidate rule:

> Unit-bearing metrics shall never be reported without the coordinate/unit used to construct the error.

---

## 7. Bias–Variance Decomposition Derivation

Let

\[
\mu_e=E[e].
\]

Then

\[
e=(e-\mu_e)+\mu_e.
\]

Squaring and taking expectation,

\[
E[e^2]
=
E[(e-\mu_e)^2]
+2\mu_e E[e-\mu_e]
+\mu_e^2.
\]

Since

\[
E[e-\mu_e]=0,
\]

we obtain

\[
E[e^2]
=
\operatorname{Var}(e)+\mu_e^2.
\]

For fixed truth,

\[
\mu_e=\operatorname{Bias}(\hat q),
\]

so

\[
\operatorname{MSE}
=
\operatorname{Var}(\hat q)
+
\operatorname{Bias}^2.
\]

This derivation is reserved for GRP-018 evidence.

---

## 8. Finite Monte Carlo Estimates

Suppose `N` eligible matched scalar errors are

\[
e_1,\ldots,e_N.
\]

The empirical mean error is

\[
\bar e
=
\frac{1}{N}\sum_{i=1}^{N}e_i.
\]

For a fixed-truth Monte Carlo condition, the natural Monte Carlo bias estimate is

\[
\widehat{\operatorname{Bias}}_{\rm MC}=\bar e.
\]

The empirical MSE is

\[
\widehat{\operatorname{MSE}}_{\rm MC}
=
\frac{1}{N}\sum_{i=1}^{N} e_i^2,
\]

and empirical RMSE is

\[
\widehat{\operatorname{RMSE}}_{\rm MC}
=
\sqrt{
\frac{1}{N}\sum_{i=1}^{N} e_i^2
}.
\]

These are finite-sample Monte Carlo estimates of population quantities, not the exact population metrics.

---

## 9. Critical Denominator Distinction: `N` versus `N-1`

Define the empirical centered second moment

\[
v_N
=
\frac{1}{N}\sum_{i=1}^{N}(e_i-\bar e)^2.
\]

Then the exact finite-data identity is

\[
\boxed{
\widehat{\operatorname{MSE}}_{\rm MC}
=
v_N+\bar e^2
}
\]

because both terms use divisor `N`.

By contrast, the usual unbiased sample-variance estimator is

\[
s_e^2
=
\frac{1}{N-1}\sum_{i=1}^{N}(e_i-\bar e)^2.
\]

In general,

\[
\widehat{\operatorname{MSE}}_{\rm MC}
\ne
s_e^2+\bar e^2.
\]

Candidate rule:

> GeoDOA shall not mix the `N-1` unbiased sample-variance estimator with the exact finite-sample MSE decomposition and then claim an algebraic contradiction.

Both quantities are useful, but they answer different finite-sample questions and must be named clearly.

---

## 10. Candidate GRP-018 Hand Problem

The Phase 0C roadmap reserves GRP-018 for a hand-computable bias/variance/MSE/RMSE problem.

### 10.1 Candidate data

Let the fixed true DOA be

\[
\theta_0=10^\circ
\]

and four valid estimates be

\[
\hat\theta=\{9^\circ,10^\circ,12^\circ,13^\circ\}.
\]

Errors are

\[
e=\{-1^\circ,0^\circ,2^\circ,3^\circ\}.
\]

### 10.2 Monte Carlo bias estimate

\[
\bar e
=
\frac{-1+0+2+3}{4}
=1^\circ.
\]

Thus

\[
\boxed{\widehat{\operatorname{Bias}}_{\rm MC}=1^\circ.}
\]

### 10.3 Empirical MSE

\[
\widehat{\operatorname{MSE}}_{\rm MC}
=
\frac{(-1)^2+0^2+2^2+3^2}{4}
=
\frac{14}{4}
=3.5\ \mathrm{deg}^2.
\]

### 10.4 Empirical RMSE

\[
\widehat{\operatorname{RMSE}}_{\rm MC}
=
\sqrt{3.5}
\approx
1.870828693^\circ.
\]

### 10.5 Centered second moment using divisor `N`

The error deviations from the empirical mean are

\[
\{-2,-1,1,2\}^\circ.
\]

Therefore

\[
v_N
=
\frac{4+1+1+4}{4}
=
2.5\ \mathrm{deg}^2.
\]

Then

\[
v_N+\bar e^2
=
2.5+1
=
3.5\ \mathrm{deg}^2,
\]

which exactly equals empirical MSE.

### 10.6 Unbiased sample variance

\[
s_e^2
=
\frac{10}{3}
\approx
3.333333333\ \mathrm{deg}^2.
\]

Hence

\[
s_e^2+\bar e^2
\approx
4.333333333\ \mathrm{deg}^2,
\]

which is **not** the empirical MSE. This is expected because `s_e^2` uses `N-1` while empirical MSE uses `N`.

### 10.7 GRP-018 status

This is a **candidate hand solution only** during Exploration 4.7.

It shall not be labeled formal Golden Reference PASS until:

1. the governing ADR-004 is stable;
2. Gate E is reached;
3. the canonical GRP artifact is created/reconciled;
4. arithmetic and units are independently checked.

---

## 11. RMSE Is Not Standard Deviation

RMSE and standard deviation coincide only when bias is zero under the same probability law.

In general,

\[
\operatorname{RMSE}
=
\sqrt{\sigma^2+b^2}
\ge \sigma,
\]

where

\[
\sigma=\sqrt{\operatorname{Var}(\hat q)},
\qquad
b=\operatorname{Bias}(\hat q).
\]

Candidate rule:

> GeoDOA shall not use `RMSE`, `standard deviation`, `spread`, and `precision` interchangeably.

---

## 12. Accuracy versus Precision

For localization metrics:

```text
bias          -> systematic displacement
variance/std  -> stochastic spread / precision component
MSE/RMSE      -> combined squared-error accuracy measure
```

An estimator can have:

- low variance but high bias;
- low bias but high variance;
- low RMSE only when the combined error is low.

No one scalar fully characterizes estimator behavior.

---

## 13. Fixed Truth versus Random Truth Across Trials

If every trial uses the same `theta0`, the condition-specific bias has direct interpretation.

If truth varies by trial,

\[
\theta_i\sim p_\Theta,
\]

then

\[
\bar e
=
\frac{1}{N}\sum_i(\hat\theta_i-\theta_i)
\]

estimates bias averaged over the declared truth distribution.

This may conceal angle-dependent structure.

Candidate requirements:

- record the truth distribution/sweep;
- report condition-resolved metrics when scientifically material;
- do not present distribution-averaged bias as if it were uniform over angle.

---

## 14. Multi-Source Error after Association

Exploration 4.6 requires explicit truth-to-estimate association before per-source localization error is formed.

For matched pair `(i,j)`:

\[
e_{ij}=\hat\theta_j-\theta_i.
\]

Only then may matched-pair bias/MSE/RMSE be computed.

Candidate rule:

> Multi-source RMSE shall state whether it is source-conditioned, trial-conditioned, pooled over matched pairs, or aggregated by another declared weighting rule.

No silent array-index scoring is permitted.

---

## 15. Pooled Matched-Pair RMSE versus Per-Trial Weighting

Suppose trial `t` has `m_t` valid matched pairs.

A pooled matched-pair MSE is

\[
\widehat{\operatorname{MSE}}_{\rm pair}
=
\frac{\sum_t\sum_{k=1}^{m_t} e_{tk}^2}
{\sum_t m_t}.
\]

This weights trials in proportion to their number of matched sources.

An alternative is equal trial weighting:

\[
\widehat{\operatorname{MSE}}_{\rm trial}
=
\frac{1}{T}
\sum_{t=1}^{T}
\left(
\frac{1}{m_t}\sum_{k=1}^{m_t}e_{tk}^2
\right),
\]

for trials where that expression is defined.

These are not generally equal.

Candidate rule:

> Aggregation weighting is part of the metric definition and must be explicit.

No universal weighting policy is accepted here for all study types.

---

## 16. Missing and False Detections Must Not Vanish into RMSE

If localization RMSE is computed only on successfully matched estimates, it is a **conditional localization metric**.

Conceptually:

\[
\operatorname{RMSE}_{\rm matched}
=
\sqrt{E[e^2\mid \text{valid matched estimate}] }.
\]

That can be scientifically useful, but it does not measure detection completeness.

Candidate rule:

> Success-conditioned/matched-only RMSE is permitted only when its conditioning is explicit and corresponding miss/false/failure coverage is reported separately.

GeoDOA shall not silently drop missed sources or failed trials and label the surviving metric simply `RMSE` as if it represented unconditional system performance.

The treatment of misses, false detections, and typed failures is developed in Explorations 4.8 and 4.13.

---

## 17. No Universal Artificial Error Penalty for Misses

One tempting practice is to assign an arbitrary large angular error to every miss so that one scalar RMSE includes detection failure.

Phase 0C does not accept such a universal penalty because the result depends on an application-specific loss function.

Candidate rule:

> Misses and false detections shall remain typed outcomes unless a benchmark explicitly defines and justifies a composite loss/penalty.

Thus localization RMSE and detection/resolution metrics remain separate by default.

---

## 18. Estimator Failure versus Large Localization Error

A numerical failure, incompatible model, invalid covariance, or no-valid-output state is not a finite angle error.

Candidate rule:

> GeoDOA shall not coerce typed estimator failure into `NaN -> 0`, `NaN -> max_angle`, or another hidden numeric value before aggregation.

Failure coverage is preserved and reported separately unless a declared composite decision loss explicitly maps failures to costs.

---

## 19. Angle Error versus Direction-Cosine Error

Under ADR-001,

\[
u=\sin\theta.
\]

Therefore

\[
e_u=\hat u-u
\]

and

\[
e_\theta=\hat\theta-\theta
\]

measure different geometrical discrepancies.

Near broadside, small errors satisfy approximately

\[
e_u\approx \cos\theta\,e_\theta
\]

when `e_theta` is expressed in radians.

Near endfire, angular error and direction-cosine error have very different scaling.

Candidate rule:

> `RMSE_theta` and `RMSE_u` are distinct metrics; conversion is not a constant scale over the full visible sector.

---

## 20. Degrees versus Radians

If squared angular error is computed in radians and later converted incorrectly by multiplying the MSE by `180/pi`, the units are wrong.

If

\[
e_{\rm deg}
=\frac{180}{\pi}e_{\rm rad},
\]

then

\[
\operatorname{MSE}_{\rm deg}
=\left(\frac{180}{\pi}\right)^2
\operatorname{MSE}_{\rm rad},
\]

while

\[
\operatorname{RMSE}_{\rm deg}
=\frac{180}{\pi}
\operatorname{RMSE}_{\rm rad}.
\]

Candidate rule:

> Unit conversion shall be applied at the correct power for squared metrics.

---

## 21. Coordinate Topology

For ADR-001's initial visible-sector DOA profile, ordinary signed angular error follows the declared non-circular sector.

A future 360-degree azimuth profile may require wrapped/circular error such as a principal angular difference.

Candidate rule:

> Error topology follows the scientific direction domain; generic angle wrapping is not universal.

---

## 22. Reference Uncertainty

Exploration 4.2 established that measured references may themselves be uncertain.

If

\[
\hat\theta=\theta_{\rm phys}+e_{\rm est},
\qquad
\theta_{\rm ref}=\theta_{\rm phys}+e_{\rm ref},
\]

then observed comparison error is

\[
e_{\rm obs}
=\hat\theta-\theta_{\rm ref}
=e_{\rm est}-e_{\rm ref}.
\]

Therefore measured-reference RMSE generally includes reference error/uncertainty.

Candidate rule:

> RMSE against a measurement reference shall be labeled as estimate-to-reference error unless reference uncertainty is negligible or separately propagated strongly enough to justify a physical-truth interpretation.

Detailed uncertainty propagation is deferred to Exploration 4.11.

---

## 23. Deterministic Algorithms Still Have Monte Carlo Variance

An estimator can be deterministic as software while its output varies across random data realizations.

Thus:

```text
algorithm RNG absent
```

does not imply

```text
estimator variance = 0.
```

Estimator variance arises from the experiment probability law, including source/noise/sensor randomness.

This reconciles Explorations 4.4 and 4.5.

---

## 24. Conditional Metrics and Hidden Selection Bias

Reporting only trials where an estimator succeeds can make a fragile estimator appear extremely accurate.

Example:

```text
Method A: matches only 40% of sources, RMSE_matched = 0.2 deg
Method B: matches 98% of sources, RMSE_matched = 0.4 deg
```

The statement `A is more accurate` is incomplete without the conditioning/coverage context.

Candidate rule:

> Conditional localization metrics shall be accompanied by the denominator and eligibility/coverage statistics needed to interpret selection effects.

---

## 25. Macro versus Micro Aggregation Across Conditions

Suppose conditions have unequal trial counts.

A micro-aggregate pools all eligible errors:

\[
\operatorname{MSE}_{\rm micro}
=
\frac{\sum_c\sum_i e_{ci}^2}{\sum_c N_c}.
\]

A macro-aggregate gives each condition equal weight:

\[
\operatorname{MSE}_{\rm macro}
=
\frac{1}{C}\sum_c
\left(\frac{1}{N_c}\sum_i e_{ci}^2\right).
\]

They answer different questions.

Candidate rule:

> Condition weighting shall be declared; unequal sampling density shall not silently redefine the target performance distribution.

---

## 26. Robust Metrics Are Complementary, Not Replacements

Heavy-tailed or catastrophic-error regimes may motivate additional metrics such as:

```text
median absolute error
quantiles
trimmed summaries
catastrophic-error probability
```

These can complement RMSE but shall not be silently substituted while retaining the label `RMSE`.

Phase 0C does not mandate a universal robust metric here.

---

## 27. Comparison of Algorithms

For methods `A` and `B`, simply comparing two estimated RMSE values does not quantify uncertainty in the difference.

When Common Random Numbers are used, paired trial-level evidence should be retained so later analysis can exploit pairing.

Candidate rule:

> Metric calculation shall preserve trial-level identities needed for paired comparative inference; statistical confidence of a ranking is deferred to Exploration 4.11/4.12.

---

## 28. Metric Provenance

A publication-grade metric record should preserve, as applicable:

```text
metric name/version
quantity and coordinate
units
truth/reference role and revision
conditioning variables
association policy/version
eligibility rule
failure/miss handling policy
aggregation weighting
number requested / eligible / matched / failed
per-condition trial counts
oracle model-order status
root study/run identity
```

Candidate rule:

> A scalar metric shall be traceable back to the trial-level evidence and policy that produced it.

---

## 29. Candidate Phase-1 Metric Profile

For initial stationary, far-field, narrowband synthetic DOA studies with exact point truth, a conservative candidate profile is:

```text
primary localization coordinate: theta, explicitly deg or rad
signed error: theta_hat - theta_true
association: accepted ADR-004 association policy
bias: empirical mean signed matched-pair error
MSE: empirical mean squared matched-pair error
RMSE: sqrt(empirical MSE)
variance diagnostic: clearly distinguish divisor-N centered moment from N-1 sample variance
miss/false/failure outcomes: reported separately, not silently discarded
condition aggregation: explicit
oracle-K status: explicit
```

This remains candidate until ADR-004 acceptance.

---

## 30. Invalid / Weak Metric Cases

The following are scientifically weak or invalid unless explicitly bounded:

1. RMSE computed before multi-source association;
2. estimate and truth arrays paired by output index;
3. misses/failures silently removed with no denominator reported;
4. arbitrary max-angle penalty inserted without declaring a composite loss;
5. MSE reported with angle units rather than angle-squared units;
6. radian MSE converted to degree MSE using a first-power scale factor;
7. `N-1` sample variance inserted into the exact empirical MSE decomposition;
8. aggregate bias reported over a broad symmetric angle sweep while hiding strong angle-dependent bias;
9. macro and micro aggregation mixed across methods;
10. matched-only RMSE called unconditional system RMSE;
11. physical-reference uncertainty ignored in a validation claim;
12. standard deviation labeled RMSE despite nonzero bias;
13. `RMSE_theta` and `RMSE_u` treated as equivalent over the full visible sector;
14. numerical failure coerced into an undocumented numeric angle error;
15. trial or source weights changed between algorithms without disclosure.

---

## 31. Cross-ADR Reconciliation

### ADR-001

Error coordinates, angle units, visible-sector topology, direction cosine, and frame semantics inherit ADR-001.

### ADR-002

Snapshot/source/noise distributions define the probability law over which estimator performance is measured. Population covariance and finite-sample covariance remain distinct.

### ADR-003

Sensor mismatch may induce systematic bias and altered variance; metric definitions do not assume ideal sensors unless the profile declares the accepted Phase-1 ideal sensor baseline.

### ADR-004 Exploration 4.2

Truth/reference role and uncertainty determine what the error variable means.

### ADR-004 Explorations 4.4–4.5

Monte Carlo metrics are conditioned on the declared trial ensemble and reproducible stochastic identities.

### ADR-004 Exploration 4.6

Multi-source localization errors are formed only after accepted association and preserve unmatched outcomes separately.

**Cross-ADR result: no contradiction identified.**

---

## 32. Candidate Decisions from Exploration 4.7

- **D4.7-01:** Bias, variance, MSE, and RMSE are defined for a declared error variable under a declared probability law/conditioning.
- **D4.7-02:** Signed scalar error is `estimate - reference` in the declared coordinate/unit.
- **D4.7-03:** Conditional bias and distribution-averaged bias are distinct and shall not be conflated.
- **D4.7-04:** Population MSE decomposes as variance plus squared bias under the same conditioning.
- **D4.7-05:** Empirical Monte Carlo MSE uses the mean of squared eligible errors; RMSE is its square root.
- **D4.7-06:** The exact finite-sample empirical identity uses the divisor-`N` centered second moment; the `N-1` unbiased sample variance is a different estimator.
- **D4.7-07:** RMSE, standard deviation, bias, and precision are not interchangeable terms.
- **D4.7-08:** Multi-source errors are computed only after explicit association.
- **D4.7-09:** Pooled-pair, per-trial, macro-condition, and micro-condition aggregation are distinct weighting contracts.
- **D4.7-10:** Matched-only/success-conditioned RMSE is allowed only with explicit conditioning and coverage reporting.
- **D4.7-11:** Misses, false detections, and typed failures are not assigned a universal artificial angular penalty by default.
- **D4.7-12:** Numerical/incompatibility failures remain typed states rather than hidden numeric errors.
- **D4.7-13:** Angular and direction-cosine RMSE are distinct metrics; squared-unit conversion uses the squared conversion factor.
- **D4.7-14:** Reference uncertainty affects estimate-to-reference error interpretation.
- **D4.7-15:** Deterministic software can exhibit nonzero estimator variance across stochastic trials.
- **D4.7-16:** Metric records preserve eligibility denominators, association, aggregation, units, reference role, and run provenance.
- **D4.7-17:** GRP-018 candidate hand data are `{theta0=10 deg; estimates=9,10,12,13 deg}`, yielding bias `1 deg`, empirical MSE `3.5 deg^2`, empirical RMSE `sqrt(3.5)=1.870828693 deg`, divisor-`N` centered variance `2.5 deg^2`, and `N-1` sample variance `10/3 deg^2`.

---

## 33. Exploration 4.7 Conclusion

Exploration 4.7 is complete at candidate-contract level.

The central rule is:

> GeoDOA shall compute bias, variance, MSE, and RMSE only from explicitly defined, unit-bearing, associated error variables under declared trial/condition distributions and eligibility rules; localization error metrics shall preserve the distinction between systematic bias, stochastic spread, matched-only accuracy, misses/false detections/failures, aggregation weighting, and finite-Monte-Carlo estimation.

No acceptance gate is started or passed by this exploration.

GRP-018 is scientifically designed here but remains **candidate evidence**, not formal Gate-E Golden Reference PASS.

The next exploration is:

```text
4.8 — Detection, Miss, False Alarm, and Resolution
```
