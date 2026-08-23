# ADR-004 Exploration 4.2 — Ground Truth and Provenance

- **ADR:** ADR-004 — Validation, Reproducibility, and Scientific Evidence
- **Phase:** 0C — Scientific Foundations
- **Exploration:** 4.2
- **Status:** EXPLORATION COMPLETE — CANDIDATE CONTRACT, NOT ACCEPTED
- **Depends on:** Accepted ADR-001, ADR-002, ADR-003; ADR-004 Exploration 4.1

## 1. Question

> What may GeoDOA legitimately call `truth`, `ground truth`, `reference`, `measurement`, `calibration evidence`, or `estimate`, and what provenance must accompany each object so that later verification, validation, Monte Carlo, DOA-error, and hardware-comparison claims are scientifically defensible?

This exploration establishes the evidence identity rules needed before defining trial semantics or error metrics.

---

## 2. Core Distinction: Truth Is Not a Generic Array

GeoDOA shall not treat an arbitrary numerical array as ground truth merely because it is used on the right-hand side of an error formula.

A quantity may act as a truth/reference only relative to:

1. a declared scientific question;
2. a declared domain/state;
3. a declared reference frame and units;
4. a declared provenance chain;
5. a declared uncertainty/epistemic status where applicable.

Thus

```text
truth != measurement
truth != calibration estimate
truth != external-tool output
truth != estimator output
truth != nominal design
truth != CST prediction
truth != high-resolution numerical result by default
```

Any of these may become a **reference** for a bounded comparison if the role is declared, but the role does not erase its provenance or uncertainty.

---

## 3. Candidate Evidence/Truth Taxonomy

The following categories are conceptual scientific roles, not final software enums.

### 3.1 Generative simulation truth

A parameter/state explicitly supplied to a synthetic data generator is exact **with respect to that declared simulation experiment**.

Examples:

- source direction `theta_true` supplied to the forward model;
- physical sensor positions used by the synthetic generator;
- source covariance used to draw snapshots;
- deterministic coupling operator used to generate synthetic measurements;
- exact random realization after seed expansion when the realization itself is retained.

Candidate rule:

> Generative simulation truth is exact by construction inside the declared synthetic model, but it is not evidence that the synthetic model is physically valid.

Therefore:

```text
exact simulation truth
    does not imply
physical ground truth of a real system.
```

### 3.2 Derived simulation truth

A quantity deterministically derived from generative simulation state may be treated as derived truth if the transformation is itself part of the accepted scientific model and no additional estimation is introduced.

Examples:

- `u_true = sin(theta_true)` under ADR-001;
- exact pairwise delays computed from declared source/sensor positions;
- exact synthetic covariance `A R_s A^H + R_n` when all terms are generative-state quantities;
- exact physical synthetic manifold produced by the selected forward model.

The derivation and parent truth identities must remain recoverable.

### 3.3 Nominal/design reference

A CAD/design/specified geometry, target calibration coefficient, intended clock rate, or nominal component value is a **design reference**, not automatically physical truth.

Example:

```text
x_nominal = [0, 0.15, 0.30] m
```

is not evidence that manufactured positions equal those values.

### 3.4 Measurement reference

A quantity obtained from an instrument, survey, measurement campaign, or laboratory apparatus is a **measurement reference** with uncertainty, calibration state, coordinate/reference-plane semantics, and acquisition provenance.

A high-accuracy measurement may serve as the best available reference for validation while still remaining uncertain.

Candidate rule:

> Real-world validation normally compares against traceable measurement/reference evidence, not an epistemically exact physical truth claim.

### 3.5 Calibration reference

A known calibration fixture, reference source angle, loopback path, reference tone, chamber position, or calibration target is evidence used to estimate/calibrate a model.

It shall not automatically be reused as independent validation evidence.

Calibration reference and validation reference must therefore remain distinguishable even when they use the same physical instrumentation.

### 3.6 External-model/tool reference

Outputs from CST, another EM solver, MATLAB, a published reference implementation, symbolic algebra, or an independent numerical package are **external-model/reference evidence**.

Agreement with them can support verification or cross-reference consistency.

It does not by itself establish physical validation.

In particular:

```text
CST result != measured truth
MATLAB result != physical truth
higher precision result != physical truth
published code result != truth by authority
```

### 3.7 Hardware/instrument reference

An FPGA output may be compared to an accepted floating-point reference, and a sensor system may be compared against calibrated laboratory instrumentation.

The reference hierarchy must be declared:

```text
physical scene/reference apparatus
        -> acquired data
        -> accepted floating-point scientific reference
        -> fixed-point reference
        -> FPGA/SoC implementation
```

or whatever bounded hierarchy the experiment actually uses.

No lower layer becomes physical truth merely because it is used as a regression oracle for the next layer.

### 3.8 Estimate

Any quantity inferred from data by an algorithm, calibration process, optimizer, fit, inverse problem, or learned model is an **estimate** unless the experiment explicitly defines otherwise.

Examples:

- estimated DOA;
- estimated calibration gain;
- estimated covariance from finite snapshots;
- estimated source count;
- estimated position offset;
- estimated coupling coefficients.

An estimate must not silently replace its reference/truth object in later pipeline stages.

### 3.9 Unresolved / unavailable truth

Some real experiments do not provide a reliable reference for every latent quantity.

GeoDOA must permit:

```text
truth unavailable
truth partially observed
truth uncertain
truth interval/set valued
truth unresolved
```

rather than manufacturing a point truth for convenience.

---

## 4. Truth Is Question-Specific

One experiment can have strong truth/reference evidence for one quantity and weak or absent evidence for another.

Example:

A rotary stage may provide a traceable reference angle while exact channel phase-center positions remain uncertain.

Then:

```text
DOA reference: strong measured reference
sensor phase-center truth: uncertain / model dependent
coupling decomposition truth: possibly unavailable
```

Therefore a single experiment-level `has_ground_truth=True` is scientifically insufficient.

Truth/reference status shall be attached to the quantity/claim being evaluated.

---

## 5. Latent Physical Truth versus Observable Reference

GeoDOA must distinguish the conceptual physical state from what is actually known.

Let

\[
\boldsymbol\theta_{\rm phys}
\]

denote the physical latent parameter/state and

\[
\mathbf z_{\rm ref}
\]

a reference measurement related by

\[
\mathbf z_{\rm ref}
=
\mathcal M(\boldsymbol\theta_{\rm phys})+\boldsymbol\eta_{\rm ref}.
\]

In a simulation, `theta_phys` may be exactly known by construction.

In a real experiment, the physical latent value generally is not observed without uncertainty. A reference apparatus provides evidence about it.

Candidate rule:

> Do not collapse `physical latent state` and `observed reference measurement` into one object merely to simplify scoring.

---

## 6. Partial and Set-Valued Truth

Not every valid reference must be a single scalar/vector point.

Examples include:

- source known to lie within an angular interval;
- uncertain surveyed sensor location with covariance;
- calibration response with confidence bounds;
- ambiguous source identity but known unordered direction set;
- physical parameter known only up to common phase/scale gauge.

GeoDOA shall allow the scientific concept of:

```text
point reference
interval/set reference
probabilistic reference
projective/equivalence-class reference
unresolved reference
```

Error metrics must respect the reference type rather than coercing every case into Euclidean point error.

---

## 7. Multi-Source Truth Is Not Necessarily Ordered

For many DOA experiments, the physically relevant truth is an unordered set/multiset of arrivals:

\[
\Theta_{\rm true}=\{\theta_1,\ldots,\theta_K\}.
\]

Array index order, source-generator order, or output-peak order does not automatically create physical identity correspondence.

If persistent physical source identity exists, it may be retained as provenance. But scoring still requires an explicit association policy when estimator outputs are unordered.

This exploration therefore reserves the detailed association contract for Exploration 4.6.

---

## 8. Truth, Nuisance Parameters, and Oracle Information

A synthetic experiment may know parameters that the estimator is not allowed to use.

Examples:

- exact source count;
- exact noise variance;
- exact source covariance;
- exact calibration matrix;
- exact SNR;
- exact source ordering.

These are **generative truth** but may constitute **oracle information** from the estimator's perspective.

Candidate rule:

> Truth availability for evaluation does not imply permission to provide that truth to the algorithm.

Run provenance must distinguish:

```text
truth used only for scoring
truth intentionally supplied as oracle input
truth estimated by the algorithm
truth unavailable to the algorithm
```

Otherwise a benchmark may silently become easier than the claimed task.

---

## 9. Calibration, Tuning, Training, and Validation Independence

Evidence used to fit a model is not automatically independent evidence for validating that model.

GeoDOA shall distinguish at least:

```text
calibration/fitting data
hyperparameter/tuning data
training data, where applicable
validation evidence
final held-out evaluation evidence
```

The exact terminology may vary by workflow, but dependence must remain explicit.

Examples:

- a measured manifold used to fit coupling coefficients cannot be presented as independent evidence that those coefficients predict the same samples;
- an angle grid used to tune calibration interpolation errors is not automatically a held-out validation grid;
- a Monte Carlo condition used to choose `tau` cannot later be presented as untouched evidence for `tau` without disclosure.

Candidate rule:

> Reuse is permitted when scientifically justified, but independence claims require actual independence or explicitly modeled dependence.

---

## 10. Provenance Minimum for a Scientific Reference

A publication-grade reference/truth artifact should preserve, as applicable:

1. **identity** — stable artifact/run/reference identifier;
2. **scientific role** — generative truth, design reference, measurement reference, calibration reference, external-model reference, estimate, etc.;
3. **quantity identity** — DOA, position, manifold, covariance, calibration coefficient, timing offset, etc.;
4. **units** — consistent with ADR-001/003 unit rules;
5. **coordinate/reference frame** — including ADR-001 angle/direction convention;
6. **reference plane** — where relevant to sensor/network/manifold quantities;
7. **channel/source identity** — stable IDs, not row order alone;
8. **domain/state** — frequency, direction, range, polarization, temperature, hardware state, time, termination, acquisition mode as relevant;
9. **production method** — simulation generator, instrument, survey, chamber setup, solver, external code, analytical derivation;
10. **instrument/model/software identity** — version/configuration where applicable;
11. **calibration state** — for measured references;
12. **uncertainty/accuracy statement** — when not exact by construction;
13. **timestamp/validity interval** — when state may drift;
14. **parent inputs / derivation lineage** — for derived truth/reference quantities;
15. **data/configuration hash or immutable content identity** — where practical;
16. **Git/software revision** — for software-generated evidence;
17. **notes on independence** — calibration/tuning/training/held-out relationship where relevant.

Not every field applies to every artifact, but missing required provenance must remain visible rather than silently guessed.

---

## 11. Exactness and Uncertainty

Candidate epistemic classes:

```text
EXACT_BY_CONSTRUCTION
TRACEABLE_WITH_UNCERTAINTY
REFERENCE_WITH_UNQUANTIFIED_UNCERTAINTY
MODEL_PREDICTION
ESTIMATE
UNRESOLVED
```

These are conceptual categories, not final software enums.

### 11.1 Exact by construction

Appropriate for deterministic/synthetic truth inside a declared mathematical experiment.

### 11.2 Traceable with uncertainty

Appropriate for metrology/reference measurements with a stated uncertainty model/bound.

### 11.3 Reference with unquantified uncertainty

May still be usable, but precision/validation claims must acknowledge the missing uncertainty characterization.

### 11.4 Model prediction

CST/EM/analytical/high-fidelity numerical output remains model prediction even if considered a high-quality reference.

### 11.5 Estimate

Derived from observed data through an inference process.

### 11.6 Unresolved

Evidence insufficient to identify a unique/reference value.

---

## 12. Reference Uncertainty and Error Attribution

Suppose an estimate is compared with a measured reference:

\[
\hat\theta-\theta_{\rm ref}.
\]

This difference generally contains both estimator error and reference uncertainty/error.

If

\[
\theta_{\rm ref}=\theta_{\rm phys}+e_{\rm ref},
\qquad
\hat\theta=\theta_{\rm phys}+e_{\rm est},
\]

then

\[
\hat\theta-\theta_{\rm ref}=e_{\rm est}-e_{\rm ref}.
\]

Therefore experimental RMSE against an uncertain reference is not automatically identical to RMSE against inaccessible physical truth.

Candidate rule:

> Reference uncertainty shall be propagated, bounded, reported, or explicitly declared negligible relative to the validation objective before strong physical-accuracy claims are made.

The detailed uncertainty/CI contract is deferred to Exploration 4.11.

---

## 13. Simulation Truth Does Not Validate Reality

Synthetic simulation supports powerful verification because truth is known exactly by construction.

But even perfect recovery

\[
\hat\theta=\theta_{\rm true}
\]

for every synthetic trial only demonstrates correctness/performance under the selected synthetic model.

It does not demonstrate that:

- real antenna phase centers follow the model;
- actual mutual coupling matches the model;
- physical noise is white Gaussian;
- calibration remains valid outside its domain;
- ADC/receiver effects are negligible;
- actual hardware meets the same assumptions.

This preserves Exploration 4.1's verification/validation distinction.

---

## 14. Measured and CST/EM Manifold Rules

ADR-003 already distinguishes measured and EM-derived manifolds from physical truth.

ADR-004 extends that into evidence terminology:

### 14.1 CST/EM-derived manifold

Role:

```text
MODEL_PREDICTION / EXTERNAL_MODEL_REFERENCE
```

unless used inside an artificial synthetic experiment where it is explicitly chosen as the generative model.

### 14.2 Measured manifold

Role:

```text
MEASUREMENT_REFERENCE
```

with calibration/reference-plane/domain/uncertainty provenance.

It shall not be labeled epistemically exact physical truth merely because it was measured.

### 14.3 Synthetic truth using imported manifold

If a stored measured or CST manifold is intentionally frozen and used as the generator inside a synthetic experiment, the **generated experiment's reference response** may be exact by construction relative to that generator artifact.

That does not retroactively make the source artifact physically exact.

This distinction is important and shall be preserved in provenance.

---

## 15. Cross-Tool and High-Precision References

A second software implementation or higher-precision computation can provide reference evidence.

Examples:

```text
Python float64 vs symbolic result
Python vs MATLAB
float64 vs arbitrary precision
NumPy eigensolver vs independent eigensolver
software reference vs FPGA output
```

The candidate rule is:

> A numerical reference must be described by what it establishes: implementation agreement, numerical convergence, or bounded approximation consistency. It shall not be called physical ground truth unless a separate physical-reference argument exists.

---

## 16. Truth Artifact Immutability and Lineage

Publication-grade experiments should not silently mutate the reference used for scoring.

Candidate requirements:

- raw reference artifact retained or content-addressable;
- transformations create derived artifacts/views rather than overwrite the parent;
- corrections/coordinate conversions/normalizations retain lineage;
- updates to a calibration/reference artifact produce a new revision/identity;
- benchmark result records the exact reference revision used.

This does not force a specific storage technology in Phase 0C.

---

## 17. Validation Domain Is Part of the Reference Claim

A validation reference applies within a declared domain.

Examples:

```text
frequency range
angle/range sector
polarization
temperature/environment
hardware revision
termination/loading state
receiver gain state
sampling mode
array mounting configuration
measurement epoch
```

A reference that is valid at `f0` does not automatically validate behavior at `f1`.

A chamber-calibrated array does not automatically retain the same reference after physical reconfiguration.

Thus:

> Reference validity and calibration validity are domain-bearing claims, not timeless properties of a file.

---

## 18. Candidate Claim Grammar

GeoDOA evidence should encourage bounded statements such as:

```text
verified against GRP-018
agrees with independent MATLAB reference within X
validated against chamber angle reference over domain D
reproduced from run identity R
matched floating-point reference within tolerance T
measured against calibrated instrument with uncertainty U
```

and discourage unbounded claims such as:

```text
correct
accurate
validated
ground-truth matched
hardware proven
```

when the evidence/domain is not stated.

---

## 19. Failure / Insufficient-Provenance Cases

The following cases shall not silently become valid truth evidence:

1. numeric target with unknown units;
2. DOA reference with unknown angle convention/frame;
3. measured manifold with unknown channel ordering;
4. calibration artifact with unknown reference plane;
5. CST export with unknown normalization/excitation semantics;
6. estimator output reused as truth for the same estimator;
7. tuned condition presented as independent hold-out evidence without disclosure;
8. hardware output compared only against another implementation sharing the same bug and called physically validated;
9. reference file changed after benchmark without revision tracking;
10. uncertain real-world reference reported as exact truth;
11. partial truth coerced into a complete point vector;
12. source-generator order used as estimator association without an explicit policy;
13. generative oracle information silently supplied to an estimator that is claimed to operate blind;
14. missing truth silently replaced by nominal design values.

Detailed top-level response taxonomy will be reconciled at Gate F; this exploration establishes the semantic failure modes.

---

## 20. Cross-ADR Reconciliation

### ADR-001

Truth/reference angles, positions, directions, frames, units, phase references, and stable channel identities inherit ADR-001 semantics.

### ADR-002

Source count, arrivals, snapshots, covariance, physical/virtual MIMO identities, and measurement provenance inherit ADR-002 semantics. A finite-sample covariance estimate is not population truth merely because it is observed.

### ADR-003

Nominal/physical/measured/EM/calibrated manifolds remain distinct. Calibration evidence does not become physical truth through naming. Direct measured/CST artifacts retain domain and included-effects provenance.

**Cross-ADR result: no contradiction identified.**

---

## 21. Candidate Decisions from Exploration 4.2

- **D4.2-01:** Ground truth/reference is a typed scientific role with domain and provenance, not a generic numerical array.
- **D4.2-02:** Generative simulation truth is exact by construction only within the declared synthetic model.
- **D4.2-03:** Simulation truth does not by itself establish physical validation.
- **D4.2-04:** Deterministic quantities derived solely from accepted generative truth may be derived truth with parent lineage.
- **D4.2-05:** Nominal/design values are not automatically realized physical truth.
- **D4.2-06:** Real-world references are normally measurement/reference evidence with uncertainty rather than epistemically exact truth.
- **D4.2-07:** Calibration/fitting evidence and independent validation evidence remain distinct.
- **D4.2-08:** CST/EM/tool outputs are model/reference evidence, not physical truth by authority.
- **D4.2-09:** Estimates remain distinct from reference/truth objects.
- **D4.2-10:** Truth may be partial, uncertain, set-valued, probabilistic, gauge-equivalent, or unavailable.
- **D4.2-11:** Multi-source truth need not be ordered; association requires a separate declared policy.
- **D4.2-12:** Generative truth used only for scoring is distinct from oracle information supplied to an estimator.
- **D4.2-13:** Reference uncertainty contributes to observed estimate-minus-reference error and must not be silently attributed entirely to the estimator.
- **D4.2-14:** Scientific references require sufficient identity, unit, frame, domain, method, uncertainty, and revision provenance for the claim being made.
- **D4.2-15:** Reference transformations preserve lineage; publication-grade reference artifacts are not silently overwritten.
- **D4.2-16:** Validation claims are domain-bearing and reference-revision-bearing.
- **D4.2-17:** Numeric/cross-tool agreement is verification/cross-reference evidence unless separate physical evidence establishes validation.
- **D4.2-18:** Missing/unresolved truth must remain missing/unresolved rather than being replaced silently by nominal values.

---

## 22. Exploration 4.2 Conclusion

Exploration 4.2 is complete at candidate-contract level.

The central rule is:

> GeoDOA shall distinguish exact-by-construction synthetic truth, derived truth, nominal design reference, measured reference, calibration reference, external-model reference, hardware/instrument reference, estimate, and unresolved truth; every validation/error claim shall preserve the provenance, domain, uncertainty, and independence semantics needed to interpret that comparison correctly.

No acceptance gate is started or passed by this exploration.

The next exploration is:

```text
4.3 — Deterministic Reference Evidence
```
