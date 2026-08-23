# ADR-004 Exploration 4.5 — Seed, RNG, and Common Random Numbers

- **ADR:** ADR-004 — Validation, Reproducibility, and Scientific Evidence
- **Phase:** 0C — Scientific Foundations
- **Exploration:** 4.5
- **Status:** EXPLORATION COMPLETE — CANDIDATE CONTRACT, NOT ACCEPTED
- **Depends on:** Accepted ADR-001, ADR-002, ADR-003; ADR-004 Explorations 4.1–4.4

## 1. Question

> How shall GeoDOA generate, identify, partition, reproduce, and share stochastic realizations so that Monte Carlo evidence remains reproducible, fair, parallelization-safe, algorithm-order-independent, and scientifically interpretable?

This exploration defines the stochastic identity contract required before multi-source association and aggregate performance metrics are specified.

---

## 2. Core Principle

A single integer seed is not a sufficient scientific description of a Monte Carlo experiment.

GeoDOA must preserve at least:

```text
root seed / stochastic study identity
RNG family and version semantics
semantic child-stream derivation policy
condition identity
trial identity
random-variable family identity
redraw scope
pairing / sharing policy
realization provenance
```

Candidate rule:

> Random realization identity shall be derived from scientific semantics, not from incidental execution order.

Thus stochastic output shall not silently change merely because:

- algorithms are reordered;
- a new algorithm is inserted;
- plotting is enabled;
- worker count changes;
- trials are parallelized;
- chunk size changes;
- a failed trial is retried;
- one branch consumes extra random numbers internally.

---

## 3. Root Seed versus Child Streams

The **root seed** identifies a stochastic study namespace, not one monolithic mutable random stream.

Conceptually:

\[
S_{\rm child}
=
\mathcal H(
S_{\rm root},
\mathrm{study\_id},
\mathrm{condition\_id},
\mathrm{trial\_id},
\mathrm{random\_family},
\mathrm{substream\_role},
\mathrm{version}
),
\]

where `H` denotes a deterministic seed-derivation mechanism with stable canonical serialization semantics.

This equation is conceptual; Phase 0C does not require a particular hash function or RNG API.

Candidate rule:

> Root seed + semantic identity shall determine a child stream without dependence on how many random numbers another component has already consumed.

---

## 4. Stateful Global RNG Is Not an Authoritative Scientific Contract

The pattern

```python
seed(root)
for condition in conditions:
    for trial in trials:
        ... draw everything from one global generator ...
```

is fragile because realization identity depends on traversal order and draw count.

It may be used in disposable exploratory scripts, but shall not define authoritative publication-grade GeoDOA evidence.

Failure examples:

- adding a diagnostic random draw changes every later trial;
- changing `conditions` ordering changes every realization;
- inserting a new algorithm before another changes algorithm-specific randomness;
- parallel execution changes scheduling and therefore stream consumption.

---

## 5. Semantic Random Families

Randomness should be partitioned by physical/statistical meaning.

Candidate random families include:

```text
source_waveform
source_symbol_or_snapshot
source_amplitude
source_phase
source_activity
source_position_or_DOA
source_motion
source_correlation_latent
thermal_or_receiver_noise
colored_noise_latent
sensor_position_error
channel_gain_phase_error
coupling_uncertainty
clock_timing_error
jitter
ADC_dither_or_quantization_auxiliary
algorithm_random_initialization
bootstrap_resampling
hardware_test_stimulus
```

The exact list is profile-dependent.

Candidate rule:

> Random families that represent different scientific mechanisms shall not be coupled accidentally through one shared mutable stream.

---

## 6. Redraw Scope and Stream Scope Must Agree

Exploration 4.4 distinguishes fixed device state, condition-level randomness, trial-level randomness, snapshot-level randomness, and hierarchical randomness.

The RNG hierarchy must encode that same structure.

Example:

```text
study
 ├─ device realization       redraw once per simulated device
 │   ├─ position errors
 │   └─ fixed gain/phase mismatch
 └─ condition
     └─ trial
         ├─ source realization
         └─ noise realization
             └─ snapshot sequence
```

A channel mismatch intended to stay fixed for 100 noise trials must not be regenerated merely because the implementation calls a random function inside the trial loop.

---

## 7. Trial Identity

A stochastic trial shall have a stable identity independent of execution location.

Conceptually:

```text
trial_id = (study_id, condition_id, trial_index_or_uuid, stochastic_contract_version)
```

The trial identity should be sufficient to regenerate all declared stochastic components, provided the required algorithm/RNG versions and upstream artifacts are available.

Candidate rule:

> Trial identity is a scientific identity, not a worker index, batch index, process ID, wall-clock timestamp, or array position after sorting.

---

## 8. Condition Identity Must Be Canonical

If child streams depend on condition identity, condition identity must not depend on arbitrary dictionary ordering, float string formatting, GUI presentation order, or filenames alone.

Candidate requirements:

- canonical field names;
- canonical units before identity derivation;
- stable ordering of structured fields;
- explicit scientific-profile/version identity;
- normalized representation of categorical values;
- careful float serialization policy;
- explicit distinction between `30 deg` and `0.523598... rad` at input while allowing canonical physical equivalence if the configuration contract so defines.

Detailed run/configuration hashing is deferred to Exploration 4.16.

---

## 9. RNG Algorithm Identity Is Provenance

A numerical seed without RNG algorithm identity is not sufficient for long-term replay.

GeoDOA publication-grade evidence should preserve, as applicable:

```text
RNG library/provider
bit-generator / PRNG family
algorithm/version semantics
seed-derivation policy version
distribution sampling method when behavior may vary
software/library versions required for exact replay
```

Candidate rule:

> Exact bitwise replay and statistical reproducibility are distinct claims.

A future library version may generate a statistically equivalent distribution without reproducing the exact historical bitstream.

Both cases can be scientifically useful, but the claim must be explicit.

---

## 10. Exact Replay versus Statistical Reproduction

GeoDOA shall distinguish:

### 10.1 Exact realization replay

The same trial regenerates the same intended stochastic realization, ideally bit-for-bit where the declared platform/software contract supports it.

### 10.2 Distributional/statistical reproduction

A rerun generates valid independent realizations from the same declared probability model but not necessarily the historical realization sequence.

### 10.3 Result reproduction

The reported aggregate findings are reproduced within declared statistical/numerical uncertainty.

Candidate rule:

> `reproducible` without stating which level is meant is insufficient for strong scientific claims.

---

## 11. Common Random Numbers (CRN)

When two methods are compared under stochastic conditions, GeoDOA should support **Common Random Numbers** when pairing is scientifically valid.

For methods `A` and `B`, paired trial `i` should share the same exogenous realization:

\[
\omega_i^{(A)}=\omega_i^{(B)}=\omega_i,
\]

for random mechanisms that are intended to be common.

Then a paired difference may be formed:

\[
D_i=M_i^{(A)}-M_i^{(B)}.
\]

This often reduces variance of the estimated performance difference when the paired responses are positively correlated.

Candidate rule:

> Fair algorithm comparison should default toward shared exogenous realizations where methods are solving the same scientific trial and sharing is physically/statistically meaningful.

---

## 12. CRN Does Not Mean Share Every Random Number

CRN must be scoped by mechanism.

Example:

Shared across algorithms:

```text
true source directions
source waveform realization
sensor realization
receiver-noise realization
snapshot realization
```

Potentially algorithm-specific:

```text
random initialization
stochastic optimizer proposals
random tie-breaking
internal randomized sketch/projection
```

Candidate rule:

> Exogenous experiment randomness and endogenous algorithm randomness shall use distinct semantic streams.

Otherwise an algorithm's internal draw count could corrupt the physical realization or unfairly couple two methods.

---

## 13. Paired versus Independent Comparisons

Two scientifically legitimate designs exist:

### 13.1 Paired comparison

Methods use common exogenous realizations.

Useful when asking:

> On the same realized problem, how much better/worse is method A than method B?

### 13.2 Independent comparison

Methods receive independent realizations from the same distribution.

This may be appropriate for some experimental designs but generally yields a noisier direct difference estimate.

Candidate rule:

> The comparison design—paired or independent—shall be declared, not inferred from the presence of the same root seed.

Exploration 4.12 will define fair benchmark policy in more detail.

---

## 14. Adding Algorithms Shall Not Perturb Existing Trials

Suppose a benchmark originally contains:

```text
Bartlett
MVDR
MUSIC
```

and later adds:

```text
ESPRIT
```

The exogenous trial realizations for Bartlett/MVDR/MUSIC shall remain unchanged solely because ESPRIT was added.

Therefore child-stream derivation must not be based on algorithm list position.

Similarly, removing one failed algorithm must not alter the physical/noise realization used by the others.

---

## 15. Parallelization and Scheduling Independence

A reproducible trial must not depend on:

```text
worker_id
thread_id
process_id
GPU block/thread identity
batch execution order
completion order
scheduler timing
```

Workers should receive trial identities or deterministic child-stream keys, not draw from a shared stream whose state depends on scheduling.

Candidate rule:

> Execution topology is implementation provenance; it shall not define scientific randomness unless the experiment explicitly studies execution nondeterminism itself.

---

## 16. Failure, Retry, and Resume Semantics

If trial `i` fails due to an algorithmic/numerical error, rerunning or resuming the study shall regenerate the same exogenous trial realization rather than silently consume a new one.

Candidate requirements:

- failed trial retains its identity;
- retry does not increment scientific trial identity unless explicitly declared a new trial;
- partial-study resume uses stable identities;
- skipped trials remain visible in coverage/accounting;
- retry policy is separate from stochastic sampling policy.

This prevents selective replacement of difficult realizations.

---

## 17. Rejection Sampling and Variable Draw Counts

Some distributions or algorithms consume a variable number of random bits/draws.

This is another reason not to chain unrelated scientific mechanisms through one shared stream.

Candidate rule:

> Variable internal draw count in one random family shall not shift the realization of another family.

Substreams or keyed generation isolate such effects.

---

## 18. Correlated Random Variables

Independent substreams do not imply the modeled quantities themselves must be independent.

If physical/statistical correlation is required, it must be generated intentionally from a declared joint model.

Example:

\[
\mathbf z\sim\mathcal{CN}(\mathbf 0,\mathbf I),
\qquad
\mathbf n=\mathbf L\mathbf z,
\qquad
\mathbf L\mathbf L^H=\mathbf R_n.
\]

Here the latent base stream can be independent while the resulting noise channels are correlated by design.

Candidate rule:

> RNG stream independence and physical random-variable independence are distinct concepts.

---

## 19. Complex Random Variables

For proper-complex Gaussian variables, the generation convention shall be explicit enough to preserve intended variance.

For example, if

\[
z=x+jy,
\quad
x,y\sim\mathcal N(0,\sigma^2/2),
\]

independently, then

\[
E|z|^2=\sigma^2.
\]

A generator that instead assigns variance `sigma^2` to both real and imaginary parts produces total complex power `2 sigma^2`.

Candidate rule:

> Distribution parameterization is part of the stochastic contract; seed identity alone cannot rescue an ambiguous variance convention.

---

## 20. Random Permutations and Source Ordering

If source labels/order are randomized, the permutation must have its own semantic role and must not alter the underlying physical truth set unintentionally.

Similarly, shuffling output presentation order must not create a new scientific realization.

Detailed source-to-estimate association is deferred to Exploration 4.6.

---

## 21. Bootstrap / Resampling Randomness

Bootstrap, permutation tests, randomized confidence procedures, and similar post-processing introduce a second stochastic layer.

Candidate rule:

> Analysis/resampling randomness shall be separated from data-generation randomness.

Thus one can replay the original experiment while changing only the bootstrap seed, or vice versa.

Exploration 4.11 will define uncertainty reporting.

---

## 22. Hardware and Fixed-Point Stimulus Reuse

For float/fixed/FPGA cross-validation, identical digital input stimuli should be replayable across implementations when the comparison intends sample-for-sample equivalence.

Candidate hierarchy:

```text
scientific trial realization
      ↓
canonical digital stimulus artifact or reconstructable stream identity
      ↓
float reference
fixed-point model
HLS/RTL/FPGA implementation
```

Hardware transport chunking, DMA packetization, and execution timing shall not silently change the scientific stimulus unless those effects are explicitly under test.

---

## 23. Seed Privacy / Secrecy Is Not a Scientific Requirement

Seeds are provenance, not security credentials.

Publication-grade benchmark seeds may be disclosed for exact replay.

If hidden challenge/test sets are required for evaluation governance, secrecy of the test conditions is a separate protocol concern and must not be conflated with pseudorandomness quality.

---

## 24. Root Seed Changes Define a New Realization Ensemble

Changing the root seed while keeping all other configuration fixed creates a different realization ensemble/sample from the same declared stochastic model.

Candidate rule:

> A result that materially depends on one convenient root seed should not be presented as a robust population claim without adequate Monte Carlo evidence.

Trial-count adequacy and sensitivity to stochastic sampling are deferred to Exploration 4.10.

---

## 25. Seed Selection and Cherry-Picking

A seed shall not be selected post hoc because it produces a visually favorable spectrum, an unusually large improvement, or a desired ranking and then presented as representative without disclosure.

Allowed uses include:

- deterministic tutorial/example seed;
- explicitly labeled diagnostic/failure seed;
- predeclared benchmark seed set;
- full Monte Carlo ensemble with all eligible trials retained.

Candidate rule:

> Seed choice is part of experimental design; post-hoc seed selection is evidence selection and must be disclosed.

---

## 26. Minimal Publication-Grade Stochastic Provenance

A stochastic study should preserve, as applicable:

1. root seed or seed-set identity;
2. stochastic-contract / derivation-policy version;
3. RNG/bit-generator identity;
4. library/version requirements for exact replay;
5. condition identity;
6. trial identity;
7. semantic random-family identities;
8. redraw scopes;
9. CRN/shared-versus-independent policy;
10. algorithm-specific RNG policy;
11. number of requested, completed, failed, and excluded trials;
12. reason for any exclusion;
13. resampling/bootstrap RNG identity if used;
14. realization artifact/hash when raw stochastic inputs are materialized.

---

## 27. Candidate API Semantics — Conceptual Only

Phase 0C should constrain semantics without prematurely choosing classes/functions.

A future implementation may expose concepts similar to:

```text
StochasticStudyIdentity
ConditionIdentity
TrialIdentity
RandomFamily
StreamKey
PairingPolicy
RNGProvenance
```

but these names are not accepted software architecture decisions in this exploration.

The scientific requirement is that semantics survive implementation changes.

---

## 28. Invalid / Weak RNG Evidence Cases

The following are scientifically weak or invalid for authoritative comparison unless explicitly bounded:

1. only `np.random.seed(0)` is recorded;
2. RNG family/version omitted when exact replay is claimed;
3. one global mutable RNG shared by unrelated mechanisms;
4. realization changes when algorithms are reordered;
5. realization changes when worker count changes;
6. retry uses a fresh realization and replaces a failed trial;
7. CRN claimed although methods actually use different noise/source realizations;
8. exogenous and algorithm-internal randomness share one stream;
9. sensor manufacturing error redrawn per snapshot despite being modeled as fixed per device;
10. paired comparison inferred solely because both methods started from the same integer seed;
11. seed chosen after inspecting performance without disclosure;
12. a stochastic distribution is ambiguous even though seed is known;
13. a library upgrade changes RNG behavior but historical exact-replay claim is retained without provenance;
14. parallel scheduling determines stream assignment.

---

## 29. Cross-ADR Reconciliation

### ADR-001

Random geometry/angle perturbations inherit canonical units, coordinate frames, direction conventions, phase references, and stable channel identities.

### ADR-002

Random source/noise/snapshot processes inherit the declared signal, covariance, source-correlation, snapshot, and measurement semantics. Randomness cannot repair an ill-defined SNR or source model.

### ADR-003

Random sensor imperfections inherit the distinction between device-static, condition-dependent, time-varying, calibrated, and residual effects. A fixed manufacturing realization must not be treated as temporal white randomness unless the profile explicitly says so.

### ADR-004 Exploration 4.4

RNG scope must implement the redraw hierarchy defined by the scientific trial contract.

**Cross-ADR result: no contradiction identified.**

---

## 30. Candidate Decisions from Exploration 4.5

- **D4.5-01:** A single integer seed is insufficient stochastic provenance for authoritative evidence.
- **D4.5-02:** Root seed identifies a study namespace; scientific random families use deterministic semantic child streams/substreams.
- **D4.5-03:** Child-stream identity shall depend on scientific identity, not traversal order or mutable global RNG consumption.
- **D4.5-04:** Trial randomness shall be stable under algorithm insertion/removal/reordering and parallel execution.
- **D4.5-05:** Random-family scope shall match the redraw scope declared in Exploration 4.4.
- **D4.5-06:** RNG algorithm/version and seed-derivation-policy version are provenance when exact replay is claimed.
- **D4.5-07:** Exact realization replay, distributional reproduction, and aggregate-result reproduction are distinct claims.
- **D4.5-08:** Common Random Numbers shall share exogenous realizations across compared methods when scientifically valid.
- **D4.5-09:** Exogenous scientific randomness and endogenous algorithm randomness shall use distinct semantic streams.
- **D4.5-10:** Paired versus independent comparison is an explicit study design decision.
- **D4.5-11:** Failed/retried/resumed trials retain stable scientific identities and do not silently receive replacement realizations.
- **D4.5-12:** Independent RNG streams do not imply physical/statistical independence; intended correlation comes from an explicit joint model.
- **D4.5-13:** Distribution parameterization, including complex variance convention, is part of the stochastic contract.
- **D4.5-14:** Bootstrap/resampling randomness is separate from generative experiment randomness.
- **D4.5-15:** Float/fixed/FPGA comparisons may reuse identical canonical digital stimulus realizations when sample-for-sample comparison is intended.
- **D4.5-16:** Root-seed changes create a new realization sample; favorable post-hoc seed selection shall not masquerade as representative evidence.
- **D4.5-17:** Condition/trial/stream identities require canonical serialization/version semantics; implementation details are deferred to later architecture work.

---

## 31. Exploration 4.5 Conclusion

Exploration 4.5 is complete at candidate-contract level.

The central rule is:

> GeoDOA stochastic evidence shall be generated from versioned, semantically keyed random-stream identities whose scope follows the scientific trial hierarchy; fair comparisons shall deliberately share exogenous realizations through Common Random Numbers when appropriate, while algorithm-internal randomness remains isolated, and neither execution order nor parallelization may silently redefine a scientific trial.

No acceptance gate is started or passed by this exploration.

The next exploration is:

```text
4.6 — Multi-Source Truth-to-Estimate Association
```
