# ADR-004 Exploration 4.6 — Multi-Source Truth-to-Estimate Association

- **ADR:** ADR-004 — Validation, Reproducibility, and Scientific Evidence
- **Phase:** 0C — Scientific Foundations
- **Exploration:** 4.6
- **Status:** EXPLORATION COMPLETE — CANDIDATE CONTRACT, NOT ACCEPTED
- **Depends on:** Accepted ADR-001, ADR-002, ADR-003; ADR-004 Explorations 4.1–4.5

## 1. Question

> When a trial contains multiple true sources and an estimator returns zero, one, several, reordered, duplicated, or spurious DOA estimates, how shall GeoDOA associate truth and estimates before computing error metrics without silently hiding misses, false detections, ambiguity, or source-identity assumptions?

This exploration defines the association layer required before bias, variance, MSE, RMSE, detection, and resolution metrics are formalized.

---

## 2. Core Principle

For ordinary multi-source DOA scoring, the physically relevant truth is typically an unordered finite set or multiset

\[
\Theta=\{\theta_1,\ldots,\theta_K\},
\]

and the estimator returns

\[
\widehat\Theta=\{\hat\theta_1,\ldots,\hat\theta_{\hat K}\}.
\]

Array index, generator order, sorted order, peak-height order, and estimator-output order do not automatically define physical correspondence.

Candidate rule:

> GeoDOA shall perform an explicit truth-to-estimate association step before per-source error metrics are computed unless persistent physical source identities provide a stronger declared correspondence.

---

## 3. Association Is Not the Estimator

Association is an evaluation operation applied after an estimator produces outputs.

It shall not silently feed truth information back into the estimator or peak extractor.

Thus:

```text
estimation / peak extraction
        ↓
raw estimated set
        ↓
association for scoring
        ↓
matched pairs + unmatched truth + unmatched estimates
        ↓
metrics
```

Candidate rule:

> Truth used for association is evaluation-only oracle information unless the scientific task explicitly includes known labels/track identities.

---

## 4. Assignment Formulation

Let a cost matrix be declared as

\[
C_{ij}=c(\theta_i,\hat\theta_j),
\]

where the cost function is defined in the physically appropriate coordinate/metric.

For point DOA truth in a non-wrapped visible angular sector, a common candidate is

\[
C_{ij}=|\hat\theta_j-\theta_i|
\]

or squared angular error.

For equal cardinality, the minimum-cost one-to-one assignment is

\[
\pi^*=
\arg\min_{\pi\in S_K}
\sum_{i=1}^{K} C_{i,\pi(i)}.
\]

For unequal cardinality, association must permit unmatched truth and unmatched estimates rather than force every item into a pair.

Implementation may later use Hungarian/linear-sum assignment or another exact method; the scientific contract is the declared cost and admissibility policy, not one library routine.

---

## 5. Match Gating / Admissibility

Minimum-cost assignment alone can create scientifically absurd pairs when an estimate is far from every true source.

Therefore GeoDOA shall support a declared admissibility/gating rule for metrics that distinguish detection from localization.

Conceptually:

\[
(i,j)\text{ admissible}
\iff
C_{ij}\le \tau_{\rm assoc},
\]

where `tau_assoc` is experiment/profile-specific.

Candidate rule:

> Association gate, estimator peak-search rule, angular resolution criterion, and final accuracy threshold are distinct quantities and shall not be silently conflated.

No universal angular gate is accepted in Phase 0C.

---

## 6. Association Output Must Preserve Unmatched Items

The result of association shall conceptually contain:

```text
matched_pairs
unmatched_truth      -> candidate misses
unmatched_estimates  -> candidate false/spurious detections
association_status
association_costs
policy/provenance
```

If `K != K_hat`, GeoDOA shall not truncate the longer list merely to make RMSE computable.

Candidate rule:

> Cardinality mismatch is scientific evidence and must remain visible.

---

## 7. Example — Reordered but Correct Estimates

Truth:

\[
\Theta=\{-10^\circ,20^\circ\}
\]

Estimate output:

\[
\widehat\Theta=\{19.5^\circ,-9.7^\circ\}.
\]

Index-wise scoring would produce large meaningless errors.

Minimum-cost one-to-one association gives

\[
-10^\circ \leftrightarrow -9.7^\circ,
\qquad
20^\circ \leftrightarrow 19.5^\circ,
\]

with errors

\[
0.3^\circ,\ -0.5^\circ.
\]

This illustrates why output order cannot define correspondence.

---

## 8. Example — Miss and False Detection

Truth:

\[
\Theta=\{-20^\circ,5^\circ,30^\circ\}.
\]

Estimates:

\[
\widehat\Theta=\{-19.6^\circ,29.7^\circ,60^\circ\}.
\]

With a reasonable declared gate, two pairs are admissible:

```text
-20  <-> -19.6
 30  <-> 29.7
```

while

```text
true 5 deg      -> unmatched truth / miss
estimate 60 deg -> unmatched estimate / false/spurious detection
```

The 60-degree estimate shall not be force-matched to 5 degrees merely because the two sets have the same cardinality.

---

## 9. Duplicate / Collapsed Peaks

Suppose two true sources exist near each other but the estimator returns one peak.

A single estimate shall not be duplicated and assigned to both truths merely to reduce localization error.

Candidate rule:

> Standard one-to-one association permits each estimate and each truth item to participate in at most one matched pair unless a specialized estimator explicitly outputs a multi-source composite object.

Thus one collapsed peak generally implies at least one unmatched truth item.

---

## 10. Persistent Source Identity versus Set Association

Some experiments may have stable source identities, e.g. tracked emitters or separately instrumented sources.

If trustworthy identity correspondence exists independently of the estimator, the evaluation may use label-aware association.

But source labels created only by generator ordering are not automatically physically meaningful.

Candidate rule:

> Use label-aware scoring only when source identity is part of the declared scientific problem and its provenance is independently available; otherwise use permutation-invariant set association.

---

## 11. Coordinate Used for Association

Association cost must respect ADR-001 geometry and the scientific observable.

Possible coordinates include:

```text
angle theta
direction cosine u
spatial frequency
2-D/3-D direction vector
range-angle state for specialized models
```

Near endfire, equal differences in `theta` do not correspond to equal differences in `u=sin(theta)`.

Therefore:

> The association coordinate/metric is part of the benchmark contract and shall be reported.

No universal choice is imposed across all future GeoDOA profiles.

---

## 12. Angular Periodicity and Domain Topology

For ADR-001's initial visible-sector convention, DOA does not use generic circular wrapping as if `-180 deg` and `+180 deg` were always equivalent.

Future azimuthal 360-degree models may require circular distance.

Candidate rule:

> Association distance shall follow the topology of the declared direction domain; generic modulo-angle wrapping is forbidden unless the profile defines it.

---

## 13. Ambiguous Minimum Assignments

Two or more assignments may have equal or nearly equal cost, especially for symmetric or unresolved configurations.

Candidate requirements:

- deterministic tie policy for reproducibility;
- tie/ambiguity diagnostic retained;
- no claim that tie-breaking proves physical source identity;
- metrics sensitive to ambiguous assignments should preserve that status where material.

Candidate rule:

> Deterministic tie-breaking is a software reproducibility rule, not scientific evidence that one physical correspondence is uniquely correct.

---

## 14. Association and Resolution Are Distinct

A favorable assignment does not prove two sources were resolved.

Example: if two truth sources are close and two numerical peaks happen to fall near them, a separate resolution criterion may still be required based on peak topology/separation/estimator semantics.

Likewise, one source may be accurately localized while a neighboring source is missed.

Therefore:

```text
association success != resolution success
association error    != probability of resolution
```

Detailed resolution semantics are deferred to Explorations 4.8 and 4.9.

---

## 15. Association and Model-Order Oracle Use

If the estimator is told the true `K`, then `K_hat=K` may be guaranteed by construction for some algorithms/peak extractors.

That does not imply correct detection performance.

Candidate rule:

> Benchmark reports shall distinguish oracle-known model order from estimated model order so that cardinality behavior is interpreted correctly.

Association remains necessary even under oracle-known `K` because ordering/permutation may still differ.

---

## 16. Failed Estimator Outputs

If an estimator returns no valid output because of numerical failure, incompatibility, invalid covariance, or another typed failure, association shall not fabricate an empty-but-successful estimate set.

The trial retains its failure state, and metric policy later decides how such trials contribute to aggregate summaries.

Candidate rule:

> Association operates only on scientifically valid estimator outputs; estimator failure status remains distinct from ordinary zero-detection output.

Detailed failure-state aggregation is deferred to Exploration 4.13.

---

## 17. Threshold Selection Must Not Be Post-Hoc Cherry-Picked

An association gate chosen after inspecting which value makes one algorithm look best compromises comparative evidence.

Allowed approaches include:

- predeclared fixed gate justified by the application;
- gate derived from an accepted resolution requirement;
- sensitivity analysis over a declared gate range;
- no gate for a pure equal-cardinality localization-only study, if that limitation is explicit.

Candidate rule:

> Association policy is part of experimental design and provenance, not a hidden post-processing convenience.

---

## 18. Matching Cost versus Reported Error Metric

The cost used to find the assignment need not be identical to the final reported metric, but the choice must be justified.

Example:

- assignment by absolute angular error;
- reporting signed error for bias;
- reporting squared error for MSE/RMSE.

However, a matching cost that materially favors the desired final metric or algorithm ranking must be declared.

---

## 19. Multi-Dimensional State Association

Future GeoDOA extensions may estimate more than angle, e.g. range-angle, Doppler-angle, or track state.

Then a cost may take the form

\[
C_{ij}=d(\mathbf x_i,\hat{\mathbf x}_j),
\]

possibly weighted/normalized by physically meaningful scales or uncertainty.

Candidate rule:

> Mixed-unit state association requires declared scaling/metric; raw Euclidean distance across degrees, meters, and hertz is not acceptable by default.

This mirrors ADR-003's rule that mixed-unit conditioning requires scaling.

---

## 20. Reference Uncertainty and Association

If truth/reference angles are uncertain, hard nearest-neighbor assignment can itself be uncertain.

GeoDOA should permit future specialized policies using intervals, covariance, probabilistic association, or set-valued references.

For Phase 1 synthetic exact-truth studies, point-reference assignment is sufficient.

Candidate rule:

> The association method must be compatible with the truth/reference type established in Exploration 4.2.

---

## 21. Association Provenance

Publication-grade result provenance should preserve, as applicable:

```text
association policy/version
association coordinate
cost definition
gate/admissibility rule
tie rule
label-aware vs permutation-invariant mode
oracle model-order status
truth cardinality K
estimate cardinality K_hat
matched pair identities/costs
unmatched truth identities
unmatched estimate identities
ambiguity diagnostics
```

This ensures reported RMSE can later be reconstructed from trial-level evidence.

---

## 22. Candidate Phase-1 Association Profile

For the initial stationary, far-field, narrowband, 1-D DOA profile, a conservative candidate is:

```text
truth representation: unordered point set of theta in ADR-001 visible sector
estimate representation: unordered finite set of valid DOA point estimates
association: one-to-one minimum-cost assignment
cost coordinate: declared theta-angle domain for baseline reports
cardinality mismatch: preserve unmatched truth/estimates
association gate: benchmark-specific, no universal default accepted here
source labels: ignored unless an experiment explicitly declares persistent identity
failure outputs: not converted into ordinary empty detections
```

This is a candidate profile, not final Phase-1 acceptance.

---

## 23. Invalid / Weak Association Cases

The following are scientifically weak or invalid unless explicitly justified:

1. compare truth and estimate arrays by index;
2. sort both arrays and assume sorting is always equivalent to optimal association;
3. truncate extra estimates before scoring;
4. duplicate one estimate to match multiple truths;
5. force far-away pairs because cardinalities happen to match;
6. silently use true generator source order as estimator identity;
7. choose association gate after observing method ranking;
8. use circular angle distance in a non-circular visible-sector domain;
9. report localization RMSE only on matched successes without separately reporting unmatched outcomes;
10. treat estimator numerical failure as an ordinary miss without preserving failure status;
11. use mixed-unit state Euclidean distance without scaling;
12. change matching policy between algorithms in the same comparison without explicit scientific justification.

---

## 24. Cross-ADR Reconciliation

### ADR-001

Association inherits angle/direction coordinate semantics, visible sector, projection ambiguity, units, and domain topology.

### ADR-002

Source count, source identity, snapshot semantics, physical versus virtual channels, and model-order meaning remain distinct from association.

### ADR-003

Sensor imperfections may bias or split/merge estimates but do not change the requirement for explicit evaluation association. Unresolved/confounded conditions remain scientific states rather than being repaired by assignment.

### ADR-004 Explorations 4.2–4.5

Association consumes typed truth/reference objects, operates after a reproducible trial realization, and preserves trial identity and provenance.

**Cross-ADR result: no contradiction identified.**

---

## 25. Candidate Decisions from Exploration 4.6

- **D4.6-01:** Multi-source DOA truth and estimator outputs are permutation-invariant sets/multisets unless persistent source identity is explicitly part of the experiment.
- **D4.6-02:** Explicit truth-to-estimate association precedes per-source error metrics.
- **D4.6-03:** Association is evaluation-only and shall not silently leak truth into the estimator.
- **D4.6-04:** Baseline association is one-to-one; one estimate shall not satisfy multiple truth sources.
- **D4.6-05:** Unequal cardinality preserves unmatched truth and unmatched estimates rather than truncating or duplicating values.
- **D4.6-06:** Minimum-cost assignment may require an explicit admissibility gate to avoid physically meaningless forced matches.
- **D4.6-07:** Association gate, resolution criterion, peak-extraction rule, and accuracy threshold are distinct scientific controls.
- **D4.6-08:** Association coordinate/metric follows the declared direction/state domain and is benchmark provenance.
- **D4.6-09:** Tie-breaking may be deterministic for reproducibility but does not establish unique physical identity.
- **D4.6-10:** Association success and source-resolution success are distinct.
- **D4.6-11:** Oracle-known source count shall be disclosed separately from estimated model-order performance.
- **D4.6-12:** Estimator numerical/incompatibility failure is not silently converted into an ordinary empty estimate set.
- **D4.6-13:** Reference uncertainty may require specialized association; point assignment is sufficient only for suitable point-reference studies.
- **D4.6-14:** Publication-grade metrics preserve association policy, pairings, unmatched items, and ambiguity provenance.

---

## 26. Exploration 4.6 Conclusion

Exploration 4.6 is complete at candidate-contract level.

The central rule is:

> GeoDOA shall score multi-source estimates through an explicit, permutation-invariant, one-to-one association contract that preserves unmatched truth, unmatched estimates, ambiguity, model-order assumptions, and the declared physical coordinate/metric; association may establish correspondence for scoring but shall not erase misses, false detections, estimator failures, or unresolved-source evidence.

No acceptance gate is started or passed by this exploration.

The next exploration is:

```text
4.7 — Bias, Variance, MSE, and RMSE
```
