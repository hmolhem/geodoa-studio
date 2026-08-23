# ADR-004 Exploration 4.4 — Random Variables and Trial Semantics

- **ADR:** ADR-004 — Validation, Reproducibility, and Scientific Evidence
- **Phase:** 0C — Scientific Foundations
- **Exploration:** 4.4
- **Status:** EXPLORATION COMPLETE — CANDIDATE CONTRACT, NOT ACCEPTED
- **Depends on:** Accepted ADR-001, ADR-002, ADR-003; ADR-004 Explorations 4.1–4.3

## 1. Question

> What exactly is a stochastic experiment, condition, trial, realization, replicate, and sample in GeoDOA, and how must random quantities be declared so that Monte Carlo performance claims are scientifically interpretable and reproducible?

This exploration defines trial semantics before ADR-004 defines concrete seed-stream policy, truth-to-estimate association, aggregate error metrics, or Monte Carlo convergence policy.

---

## 2. Core Principle

GeoDOA shall not treat “run the simulation 1000 times” as a sufficient Monte Carlo specification.

A stochastic study must declare:

1. what is held fixed;
2. what is swept deterministically;
3. what is randomized;
4. the probability law/support of every randomized quantity;
5. the dependence/correlation structure among random quantities;
6. the level at which each quantity is redrawn;
7. what constitutes one trial;
8. what output/failure state is produced by that trial;
9. how trials are aggregated.

The candidate governing rule is:

> A Monte Carlo trial is a scientifically identified realization of a declared stochastic experiment, not merely an iteration number in a loop.

---

## 3. Experiment, Study, Condition, Trial, and Sample

GeoDOA shall distinguish at least the following conceptual levels.

### 3.1 Study

A **study** is the full scientific comparison or investigation.

Example:

```text
Compare ULA and nested array MUSIC RMSE over SNR = -10:5:20 dB.
```

A study may contain multiple sweep conditions and multiple algorithms/geometries.

### 3.2 Condition / sweep point

A **condition** is a declared deterministic point in the study design.

For example:

```text
geometry = ULA-8
SNR = 0 dB
K = 2 sources
L = 100 snapshots
source separation = 5 deg
sensor profile = Phase1 ideal
```

The condition identifies the scientific scenario before stochastic realizations are drawn.

### 3.3 Trial

A **trial** is one realization of all stochastic variables designated to be redrawn at trial level, evaluated under one declared condition.

For trial `m`:

\[
\omega_m \in \Omega
\]

represents the realized stochastic state, and the trial output is conceptually

\[
\mathcal Y_m
=
\mathcal F(\mathcal C,\omega_m),
\]

where `C` is the fixed condition and `F` is the complete generation/processing pipeline.

### 3.4 Snapshot / sample within a trial

A snapshot, fast-time sample, slow-time sample, frequency bin, or channel sample is **not automatically a Monte Carlo trial**.

ADR-002 measurement-axis semantics remain authoritative.

For example, `L=100` snapshots can belong to one trial and may be statistically correlated.

### 3.5 Replicate

A **replicate** is a repeated experiment intended to estimate variability under a declared repeatability/reproducibility design.

A software Monte Carlo trial may function as a computational replicate, but physical laboratory replicates may involve additional hierarchy such as remounting, recalibration, temperature cycling, or separate acquisition sessions.

The replicate level must therefore be declared rather than inferred from repetition alone.

---

## 4. Fixed, Swept, and Randomized Quantities

Every material experiment parameter shall conceptually belong to one of these roles for a given study:

```text
FIXED
DETERMINISTIC_SWEEP
RANDOMIZED
DERIVED
ESTIMATED
```

These are scientific roles, not final software enums.

### Example

A study may declare:

```text
fixed:
    N = 8 sensors
    L = 100 snapshots
    nominal spacing = lambda/2

swept:
    SNR in {-10, -5, 0, 5, 10} dB

randomized per trial:
    source waveform realization
    additive-noise realization

randomized once per condition:
    physical sensor-position perturbation

derived:
    sample covariance

estimated:
    DOA peaks
```

This is scientifically different from redrawing sensor-position error independently in every trial.

---

## 5. Random Variable Declaration

A publication-grade stochastic variable declaration should preserve, as applicable:

- scientific quantity identity;
- symbol/name;
- units;
- support/domain;
- probability distribution/family;
- distribution parameters;
- complex/proper/improper semantics where relevant;
- dependence/correlation structure;
- redraw level;
- conditional dependencies;
- source of randomness or generator identity;
- whether the realization is observable by the estimator;
- whether it is used only for scoring;
- whether it is retained/reconstructible.

Example:

\[
\mathbf n[\ell]\sim\mathcal{CN}(\mathbf 0,\sigma^2\mathbf I),
\qquad \ell=1,\ldots,L,
\]

is incomplete if temporal independence is required but not stated.

A stronger declaration is conceptually:

```text
n[:, l] ~ proper complex Gaussian(0, sigma^2 I)
independent across l
independent of source snapshots
redrawn for every trial
```

---

## 6. Redraw Level Is Part of the Model

The same marginal distribution can produce a different experiment depending on when it is redrawn.

Candidate hierarchy:

```text
study-level random state
condition-level random state
trial-level random state
snapshot-level random state
sample-level random state
channel-level random state
source-level random state
```

Examples:

- manufacturing position error may be drawn once per physical-array realization and held fixed over many noise trials;
- thermal noise may be redrawn at sample/snapshot level;
- a source angle may be fixed at a sweep point or randomly redrawn per trial;
- clock offset may be fixed over one acquisition while jitter varies sample by sample;
- calibration error may be common to a block of trials rather than independently redrawn each trial.

Candidate rule:

> Redraw scope is scientifically meaningful and must not be changed silently by implementation convenience.

---

## 7. Hierarchical / Nested Randomness

Many realistic studies require more than one stochastic level.

Example:

1. draw one physical array realization;
2. for that array, draw many source/noise realizations;
3. estimate conditional performance;
4. repeat across many physical arrays.

Let

\[
\boldsymbol\epsilon^{(q)}
\]

be a manufacturing realization and

\[
\omega^{(q,m)}
\]

the signal/noise realization inside it.

Then an error metric may be studied conditionally:

\[
E[e^2\mid\boldsymbol\epsilon^{(q)}]
\]

or unconditionally:

\[
E_{\boldsymbol\epsilon,\omega}[e^2].
\]

These are different scientific questions.

GeoDOA shall preserve the hierarchy rather than flattening all observations into one unlabeled pool.

---

## 8. Conditional versus Unconditional Performance

Performance claims must identify what randomness is averaged over.

Examples:

### Conditional noise performance

```text
RMSE conditional on fixed physical geometry and fixed true source angles,
averaged only over signal/noise realizations.
```

### Manufacturing-averaged performance

```text
RMSE averaged over both sensor-position errors and signal/noise realizations.
```

### Random-scene performance

```text
RMSE averaged over a declared source-angle distribution as well as noise.
```

A single scalar `RMSE = x deg` is incomplete if the averaging measure is unknown.

Candidate rule:

> Every expectation-based metric inherits the probability measure over which the expectation is taken.

---

## 9. Population Quantity versus Realization

ADR-002 already distinguishes population covariance from sample covariance. ADR-004 generalizes the evidence rule.

For a random variable `X`:

```text
probability law of X
population expectation E[X]
one realized value x_m
finite-sample estimator of E[X]
```

are distinct objects.

For example:

\[
\mathbf R_x=E[\mathbf x\mathbf x^H]
\]

is a population second-order quantity, while

\[
\hat{\mathbf R}_m
\]

is one finite-snapshot realization/estimate in trial `m`.

A Monte Carlo average

\[
\frac1M\sum_{m=1}^{M}\hat{\mathbf R}_m
\]

is another estimator; it is not the population quantity merely because `M` is large.

---

## 10. Independence Must Be Declared, Not Assumed

Random quantities may be:

```text
independent
conditionally independent
correlated
deterministically coupled
shared/common-mode
unknown dependence
```

Examples relevant to GeoDOA:

- coherent sources are not independent source processes;
- source and interference processes may be correlated;
- calibration errors may be correlated across channels;
- oscillator errors may be common-mode across channels;
- position errors may be mechanically correlated;
- sensor gain drift may share temperature dependence;
- TDM-MIMO virtual channels may share underlying source/noise state but differ in acquisition time.

Candidate rule:

> Independence is a model assumption requiring explicit declaration where it affects evidence or expected performance.

---

## 11. IID Trials Are a Special Case

Monte Carlo trials are often independent and identically distributed, but ADR-004 shall not assume IID trials universally.

Non-IID designs include:

- quasi-Monte Carlo;
- antithetic/paired sampling;
- common-random-number comparisons;
- sequential/adaptive experiments;
- physical repeated measurements with drift;
- nested/hierarchical trials;
- blocked experiments;
- correlated time-series realizations.

The aggregation/uncertainty method must match the actual design.

Detailed variance-reduction and uncertainty policy are deferred to Explorations 4.5, 4.10, and 4.11.

---

## 12. Trial Identity versus Trial Index

`trial_index = 37` is not sufficient scientific identity.

A reproducible trial is conceptually determined by:

```text
condition identity
stochastic-design identity
root/child random-stream identity
trial-level random-variable realization identity
software/scientific-profile identity
relevant calibration/data artifact identity
```

The exact run-identity implementation is deferred to Exploration 4.16, while seed-stream construction is deferred to 4.5.

Candidate rule:

> Loop order and trial index shall not be the sole provenance mechanism for randomness.

This is important because parallelization, batching, or adding a new algorithm must not silently change the scientific realization assigned to an existing trial.

---

## 13. One Trial Must Produce a Complete Outcome

A trial outcome is not limited to a successful numeric DOA vector.

A trial may produce:

```text
successful estimate
partial estimate
missed detection
false detection
unresolved sources
algorithm incompatibility
numerical failure
invalid generated state
out-of-domain condition
hardware timeout/overflow/saturation
```

Detailed failure-state semantics are deferred to Exploration 4.13.

Candidate rule:

> Every attempted trial contributes a typed outcome to the experiment record; failed outcomes are not silently absent observations.

---

## 14. No Silent Resampling after Failure

A dangerous workflow is:

```text
draw realization
algorithm fails
silently draw another realization
continue until M successful trials exist
```

This changes the effective sampling distribution and conditions the reported metric on algorithm success.

If a study intentionally reports conditional-on-success performance, it must say so and separately report the success/failure probability.

Candidate rule:

> Trial replacement/resampling after failure is prohibited unless the resampling rule is itself an explicit part of the experiment design and its statistical consequence is reported.

---

## 15. Deterministic Trials Are Valid

Not every benchmark requires randomness.

A Golden Reference Problem may be a deterministic one-trial experiment:

\[
P(\omega=\omega_0)=1.
\]

Likewise a deterministic sweep can evaluate exact model behavior without Monte Carlo averaging.

Candidate rule:

> Deterministic evidence and stochastic evidence are complementary; randomness shall be introduced only when it represents the scientific question.

---

## 16. Random Source Parameters versus Random Source Signals

GeoDOA shall distinguish randomness in source **state/parameters** from randomness in source **waveform realizations**.

Examples:

```text
source angle fixed, source waveform random
source angle random, waveform deterministic
both angle and waveform random
source covariance fixed, finite snapshots random
source count random
```

These produce different probability measures and different interpretations of bias/RMSE.

A random-angle benchmark therefore does not estimate the same quantity as an RMSE curve at a fixed angle.

---

## 17. Random Sensor Imperfections versus Unknown Fixed Imperfections

An imperfection may be physically fixed but epistemically unknown.

Examples:

- one manufactured array has fixed position errors;
- one receiver has fixed channel-delay mismatch over a run;
- one calibration residual is unknown but not redrawn physically between snapshots.

Modeling such a quantity as a random variable across an ensemble can be useful, but it does not imply the physical quantity is randomly changing in time.

Candidate rule:

> Ensemble randomness used to represent manufacturing/population uncertainty shall remain distinct from temporal randomness within one physical device/acquisition.

This directly inherits ADR-003's physical ordering and state semantics.

---

## 18. Pseudorandomness versus Physical Randomness

Software Monte Carlo normally uses deterministic pseudorandom generators.

This is compatible with stochastic modeling because the PRNG realizes samples from a declared probability model.

However:

```text
reproducible PRNG sequence
    !=
physical evidence that the real phenomenon follows that distribution.
```

The probability law remains a model assumption requiring physical justification when used for validation claims.

---

## 19. Randomness Visible to the Algorithm

For each random quantity, GeoDOA should distinguish whether the realized value is:

```text
hidden from the estimator
provided as configuration/oracle information
estimated jointly
observed indirectly through measurements
used only for scoring
```

Example:

If source angles are randomly generated but exact `K` is given to MUSIC, then `K` is oracle information even though the angles remain hidden.

This preserves Exploration 4.2's truth-versus-oracle rule.

---

## 20. SNR and Random Power Normalization

A stochastic experiment must define whether SNR is imposed using:

- population source/noise powers;
- expected signal power;
- per-trial realized signal power;
- per-snapshot normalization;
- measured output power after sensor transformations;
- another explicitly declared definition.

These choices create different stochastic experiments.

Candidate rule:

> GeoDOA shall not silently renormalize every trial to an exact realized SNR when the intended model specifies population-level SNR, or vice versa.

ADR-002 SNR semantics remain authoritative; ADR-004 adds experiment-level provenance.

---

## 21. Stochastic State Must Not Depend Accidentally on Execution Order

A common implementation hazard is consuming one global RNG stream sequentially so that:

- changing algorithm order;
- enabling a plot;
- adding a diagnostic draw;
- changing parallel worker count;
- skipping a failed condition

changes all subsequent scientific realizations.

Exploration 4.5 will define the root-seed/child-stream policy.

The candidate requirement established here is:

> Scientific random-state identity must be tied to experiment/trial semantics rather than incidental execution order.

---

## 22. Comparison Pairing Is a Trial-Design Decision

When two algorithms or geometries are compared, one may intentionally use the same underlying stochastic scene/noise realization for both methods.

This creates **paired** outcomes:

\[
(Y_m^{(A)},Y_m^{(B)}).
\]

Alternatively, independent realizations may be scientifically desired.

Neither design is universally correct.

However, the design must be explicit because it changes the variance and interpretation of the comparison.

Common Random Numbers are developed formally in Exploration 4.5; fair benchmark policy is developed in 4.12.

---

## 23. Data Reuse across Conditions

Reusing a stochastic realization across sweep points can be intentional or accidental.

Examples:

- same standardized noise realization rescaled to different SNR values;
- same source waveform reused across geometry comparisons;
- same manufacturing realization used over all SNR sweep points;
- fresh independent draw at every condition.

These designs answer subtly different questions and induce correlation across reported curves.

Candidate rule:

> Cross-condition stochastic coupling/reuse must be deliberate and provenance-bearing.

---

## 24. Trial Count Does Not Define Evidence Quality by Itself

`M = 10000` trials does not guarantee a trustworthy performance estimate if:

- the stochastic law is wrong or unspecified;
- trials are unintentionally duplicated;
- failures are dropped;
- hierarchical dependence is ignored;
- confidence uncertainty is not assessed;
- the algorithm was tuned on the same conditions;
- the target event is too rare for the trial count.

Trial-count adequacy and convergence are deferred to Exploration 4.10.

---

## 25. Candidate Trial Record

Without prescribing final software classes, one trial record should conceptually be able to identify:

```text
study_id
condition_id
trial_id
scientific_profile_id
truth/reference_id
random_stream/realization identity
fixed/swept/random variable realization metadata
input data identity
algorithm/configuration identity
calibration identity, if applicable
output estimate(s)
typed outcome/failure status
diagnostics required for later aggregation
```

The record must preserve enough information to determine what probability experiment produced the outcome.

---

## 26. Cross-ADR Reconciliation

### ADR-001

Random positions/angles still use accepted units, coordinate frames, direction conventions, phase references, and stable identities.

### ADR-002

Snapshots, source statistics, noise statistics, source count, covariance, temporal correlation, physical/virtual channels, and SNR retain ADR-002 semantics. A snapshot index is not automatically a Monte Carlo-trial index.

### ADR-003

Randomized imperfection ensembles must preserve physical state/redraw semantics. Manufacturing uncertainty, channel drift, sample jitter, and calibration residuals must not collapse into one generic random mismatch.

### ADR-004 4.1–4.3

Trial semantics preserve verification/validation roles, truth provenance, oracle separation, and deterministic-reference evidence. Deterministic GRPs remain valid degenerate stochastic experiments and are not replaced by Monte Carlo evidence.

**Cross-ADR result: no contradiction identified.**

---

## 27. Candidate Decisions from Exploration 4.4

- **D4.4-01:** A Monte Carlo trial is a scientific realization of a declared stochastic experiment, not merely a loop iteration.
- **D4.4-02:** Study, condition/sweep point, trial, snapshot/sample, and replicate are distinct concepts.
- **D4.4-03:** Every material quantity is explicitly fixed, deterministically swept, randomized, derived, or estimated for the study.
- **D4.4-04:** A random variable declaration includes its law/support, units, dependence assumptions, and redraw scope where relevant.
- **D4.4-05:** Redraw level is part of the scientific model and shall not change silently.
- **D4.4-06:** Hierarchical/nested randomness shall retain its hierarchy rather than be flattened into unlabeled trials.
- **D4.4-07:** Conditional and unconditional performance claims must state what randomness is averaged over.
- **D4.4-08:** Population quantities, realizations, finite-sample estimates, and Monte Carlo estimates remain distinct.
- **D4.4-09:** Independence/IID assumptions are explicit assumptions, not defaults inferred from repeated draws.
- **D4.4-10:** Trial identity is not reducible to loop index or execution order.
- **D4.4-11:** Every attempted trial produces a typed outcome; failures are not silently deleted.
- **D4.4-12:** Silent resampling/replacement of failed trials is prohibited.
- **D4.4-13:** Deterministic trials remain valid scientific evidence and can be viewed as degenerate random experiments.
- **D4.4-14:** Random source parameters, random source waveforms, and random source count are distinct experiment dimensions.
- **D4.4-15:** Ensemble randomness for fixed-but-unknown sensor imperfections is distinct from temporal physical randomness.
- **D4.4-16:** Reproducible PRNG sampling does not establish physical validity of the assumed probability law.
- **D4.4-17:** Random truth used for scoring remains distinct from oracle information supplied to an estimator.
- **D4.4-18:** SNR normalization level is part of the stochastic experiment and shall not be silently altered per trial.
- **D4.4-19:** Scientific random-state identity shall not accidentally depend on algorithm order, plotting, batching, or parallel execution.
- **D4.4-20:** Paired versus independent comparison realizations are explicit trial-design choices.
- **D4.4-21:** Cross-condition stochastic reuse/coupling must be deliberate and recorded.
- **D4.4-22:** Trial count alone does not establish Monte Carlo adequacy.

---

## 28. Exploration 4.4 Conclusion

Exploration 4.4 is complete at candidate-contract level.

The central rule is:

> GeoDOA shall define each stochastic study through explicit condition, random-variable, dependence, redraw-scope, trial-identity, and outcome semantics so that every Monte Carlo aggregate has a recoverable probability experiment behind it.

No acceptance gate is started or passed by this exploration.

The next exploration is:

```text
4.5 — Seed / RNG / Common Random Numbers
```
