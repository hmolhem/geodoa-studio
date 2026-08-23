# ADR-004 — Boundary and Failure Analysis

- **Governing ADR:** `ADR-004-validation-reproducibility-scientific-evidence.md`
- **Phase:** 0C — Scientific Foundations
- **Gate:** F — Boundary and Failure Analysis
- **Status:** Complete — candidate evidence for Gate F PASS
- **Prior gates:** Pre-Gate review PASS; Gates A–E PASS
- **Golden reference evidence:** `../science/golden_reference/ADR-004_GOLDEN_REFERENCE_PROBLEMS.md`

## 1. Purpose

ADR-004 governs how GeoDOA Studio generates, scores, qualifies, compares, reproduces, and publishes scientific evidence.

Gate F identifies where evidence is malformed, outside a declared profile, statistically undefined, algorithmically non-successful, numerically failed, unidentifiable, insufficiently evidenced, unreproducible, or physically overclaimed.

The purpose is not to turn every non-success into an exception. The purpose is to preserve the distinction among:

```text
invalid evidence
valid physics outside selected profile
valid trial with scientific non-success
implementation/execution failure
unresolved scientific state
metric-specific ineligibility
```

A downstream metric shall never hide a more fundamental upstream failure.

---

## 2. Required Response Classes

ADR-004 uses layered responses rather than one universal status.

### 2.1 `REJECT / INVALID`

The requested input, transformation, metric, comparison, or scientific claim is undefined or internally inconsistent.

### 2.2 `INCOMPATIBLE / REQUIRE OTHER PROFILE OR MODEL`

The physical/statistical scenario may be meaningful, but the selected profile, estimator, covariance treatment, validation claim, or evidence contract is insufficient.

### 2.3 `VALID NON-SUCCESS`

The trial/question is scientifically eligible and compatible, execution produced a meaningful non-success such as a miss, unresolved source pair, or valid no-detection, and the event remains part of the relevant end-to-end denominator.

### 2.4 `EXECUTION FAILURE`

A compatible eligible operation was attempted but failed numerically, algorithmically, computationally, or in hardware/protocol execution. Failure is retained as evidence and mapped per metric policy.

### 2.5 `DIAGNOSTIC / WARN`

Computation may proceed, but conditioning, finite-sample uncertainty, approximation sensitivity, ambiguity, weak evidence, or interpretation limits must remain visible.

### 2.6 `UNRESOLVED`

Available evidence is insufficient to support a stronger scientific classification. `UNRESOLVED` shall not be silently promoted to `VALID`, `COMPATIBLE`, `TRUTH`, `CALIBRATED`, `VERIFIED`, or `VALIDATED`.

### 2.7 `NOT ASSESSED`

The evidence question was not evaluated. Lack of assessment is not evidence of success.

---

## 3. Failure-Layer Hierarchy

Preferred diagnostic order:

```text
input / domain / unit validity
    -> truth/reference/provenance validity
    -> upstream ADR profile compatibility
    -> trial/randomness identity validity
    -> algorithm/information-contract compatibility
    -> execution/numerical status
    -> estimator output cardinality / association
    -> event outcome
    -> metric eligibility / denominator
    -> uncertainty / adequacy
    -> comparison fairness
    -> implementation cross-validation
    -> publication/reproducibility claim
```

A final RMSE or `P_res` shall not hide an invalid truth reference, incompatible profile, duplicate trial identity, or broken artifact lineage.

---

# 4. Truth, Reference, and Epistemic Boundaries

### F-004-001 — Missing reference role

A numeric target is supplied for scoring without identifying whether it is simulation truth, measurement reference, calibration estimate, external model, or estimator output.

**Required behavior:** `REJECT` authoritative scoring until the reference role is declared.

### F-004-002 — CST/external-model output labeled physical truth without justification

**Required behavior:** `REJECT` the physical-truth claim. The artifact may remain valid model/reference evidence with provenance.

### F-004-003 — Measurement labeled exact truth while uncertainty is material/unknown

**Required behavior:** `UNRESOLVED` or use a typed measurement-reference role with uncertainty. Do not silently assign exact-truth authority.

### F-004-004 — Calibration estimate reused as independent validation truth

**Required behavior:** `REJECT` the independent-validation claim unless a held-out/external reference contract exists.

### F-004-005 — Truth/reference coordinate or frame unknown

**Required behavior:** `REJECT` coordinate-sensitive scoring until frame/coordinate registration is established.

### F-004-006 — Truth available to evaluator leaked into estimator without oracle declaration

**Required behavior:** comparison/evidence claim is `INVALID` for a non-oracle method identity; rerun or relabel the method/information contract.

### F-004-007 — Multiple plausible references disagree beyond declared uncertainty

**Required behavior:** preserve the disagreement as `UNRESOLVED`; do not select the most convenient reference silently.

---

# 5. Study / Condition / Trial Identity Boundaries

### F-004-008 — Duplicate trial identity with different stochastic realization

**Required behavior:** `REJECT` exact-replay/provenance claim. One trial identity shall not refer to two distinct realizations.

### F-004-009 — Same realization assigned multiple trial IDs to inflate `N`

**Required behavior:** `REJECT` independent-trial count interpretation; preserve the dependence/duplication and recompute the effective evidence universe.

### F-004-010 — Snapshot count `L` reported as Monte Carlo count `N`

**Required behavior:** `REJECT` the statistical interpretation; counts belong to different hierarchy levels.

### F-004-011 — Condition identity changes while run/trial IDs are retained

**Required behavior:** create new condition/trial identities; old evidence shall not be silently reinterpreted.

### F-004-012 — Trial replacement after failure retains old trial ID

**Required behavior:** `REJECT` provenance. A replacement realization requires a new trial identity.

### F-004-013 — Retry of same trial redraws source/noise

**Required behavior:** `REJECT` same-trial claim; redraw is a new realization.

---

# 6. RNG / Common-Random-Number Boundaries

### F-004-014 — Root seed present but RNG family/version absent under exact replay claim

**Required behavior:** exact stochastic replay is `UNRESOLVED / INSUFFICIENT PROVENANCE`; semantic reconstruction may still be possible at a weaker reproducibility level.

### F-004-015 — Process-global mutable RNG makes results worker/order dependent

**Required behavior:** implementation is `INCOMPATIBLE` with ADR-004 exact trial semantics until semantic child streams are used or nondeterminism is explicitly downgraded.

### F-004-016 — Algorithm-internal randomness accidentally shares exogenous CRN stream

**Required behavior:** fair-comparison claim is `INVALID` unless intentional pairing is declared.

### F-004-017 — Different geometry dimensions forced to share identical noise arrays by truncation/padding

**Required behavior:** `REJECT` that CRN construction unless the mapping has a valid scientific interpretation. Use semantic latent-randomness pairing instead.

### F-004-018 — Seed cherry-picking after inspecting outcome

**Required behavior:** the selected result is exploratory/tuning evidence, not confirmatory evidence under the original study identity.

---

# 7. Configuration and Provenance Boundaries

### F-004-019 — Required scientific default remains implicit

Examples include association gate, oracle-K, search grid, centering policy, fixed-point rounding, or failure mapping.

**Required behavior:** confirmatory run is `INVALID / INCOMPLETE CONFIGURATION` until the material default is resolved and recorded.

### F-004-020 — Same config hash generated under unknown/different schema semantics

**Required behavior:** `REJECT` scientific identity equivalence unless schema/canonicalization versions are included and compatible.

### F-004-021 — Unit normalization changes scientific meaning

Example: treating `0.5 m` as equivalent to `0.5 lambda` without frequency context.

**Required behavior:** `REJECT` canonicalization.

### F-004-022 — Branch name used as authoritative source revision

**Required behavior:** provenance is insufficient for publication-grade reconstruction; exact commit/content identity required.

### F-004-023 — Dirty working tree used without preserved patch/content identity

**Required behavior:** publication/exact-replay claim is `INCOMPATIBLE / INSUFFICIENT PROVENANCE` until the dirty state is captured.

### F-004-024 — Artifact path/filename used as sole identity

**Required behavior:** `REJECT` immutable-evidence claim; require content identity and lineage.

### F-004-025 — Cache hit lacks complete dependency identity

**Required behavior:** cache output is not authoritative scientific evidence. Recompute or prove dependency completeness.

---

# 8. VP-001 Profile Boundaries

### F-004-026 — Near-field scene processed as plain VP-001

**Required behavior:** `INCOMPATIBLE / REQUIRE NEAR-FIELD PROFILE`; do not reject the physical scene.

### F-004-027 — Wideband aperture-delay effects processed as plain VP-001

**Required behavior:** `INCOMPATIBLE / REQUIRE WIDEBAND PROFILE`.

### F-004-028 — Mutual coupling or sensor mismatch injected but evidence labeled plain VP-001

**Required behavior:** `REJECT` the VP-001 identity; use an explicit nonideal-sensor extension/profile.

### F-004-029 — Colored/unequal noise used while ordinary white-noise VP-001 inference is claimed

**Required behavior:** `INCOMPATIBLE` unless an explicit colored-noise/whitening profile is declared.

### F-004-030 — Measured/CST manifold silently substituted for the ideal VP-001 manifold

**Required behavior:** `REJECT` plain VP-001 identity; create a measured/EM/calibrated-manifold profile with provenance.

### F-004-031 — Unknown-K estimator compared to oracle-K MUSIC as if information were identical

**Required behavior:** comparison is not a fair same-information comparison; relabel as different-information/full-pipeline comparison or harmonize the information contract.

### F-004-032 — Coherent-source rank collapse treated as ordinary incoherent VP-001 case

**Required behavior:** `INCOMPATIBLE / REQUIRE COHERENT-SOURCE EXTENSION OR REMEDY PROFILE`.

### F-004-033 — TDM-MIMO temporal phase treated as simultaneous receive-array VP-001 data

**Required behavior:** `INCOMPATIBLE` until timing/motion/simultaneous-equivalent construction is explicitly established.

---

# 9. Matrix / Covariance / Subspace Boundaries

### F-004-034 — `XX^H/L` called centered sample covariance

**Required behavior:** `REJECT` the object label; it is the uncentered sample second moment under the VP-001 baseline.

### F-004-035 — Centering performed silently

**Required behavior:** `REJECT` provenance-equivalence claim. Centering is a scientific preprocessing transformation and changes the matrix object/rank ceiling.

### F-004-036 — `L=0`

No snapshot matrix estimate can be formed with denominator `L=0`.

**Required behavior:** `REJECT` matrix estimation.

### F-004-037 — Centered covariance requested with `L<2`

The conventional divisor `L-1` is undefined for `L=1`.

**Required behavior:** `REJECT` that estimator.

### F-004-038 — Expected finite-sample rank deficiency classified numerical failure

**Required behavior:** `REJECT` failure classification. Report rank feasibility/finite-sample limitation at the correct layer.

### F-004-039 — PSD/Hermitian repair performed silently

**Required behavior:** preserve original matrix diagnostics and record the repaired matrix as a derived transform. Do not call repaired output proof that original input was valid.

### F-004-040 — Whitening requested with singular/invalid noise covariance

**Required behavior:** `REJECT` unregularized inverse/whitening; require a declared regularization/specialized method or other profile.

### F-004-041 — Subspace dimension zero/full used where MUSIC noise/signal projector is undefined for requested operation

**Required behavior:** `INCOMPATIBLE` with that estimator/metric while preserving the underlying data as meaningful where applicable.

---

# 10. Association / Cardinality Boundaries

### F-004-042 — Association cost uses unknown/incompatible coordinate units

**Required behavior:** `REJECT` association until coordinate/unit semantics are aligned.

### F-004-043 — Negative association gate for nonnegative distance cost

**Required behavior:** `REJECT` configuration.

### F-004-044 — Equal-cost tie without declared deterministic tie/ambiguity policy

**Required behavior:** result is `AMBIGUOUS / UNRESOLVED`; do not silently rely on library iteration order.

### F-004-045 — Extra estimates truncated before evidence recording

**Required behavior:** `REJECT` full-pipeline evidence claim unless truncation is explicitly part of the declared postprocessor. Otherwise preserve spurious outputs.

### F-004-046 — Missing estimates padded with fake numeric DOAs

**Required behavior:** `REJECT` localization evidence. Preserve miss/absence as typed outcome.

### F-004-047 — One estimate reused to satisfy two truth sources under one-to-one profile

**Required behavior:** `REJECT` association; collapsed estimate cannot resolve both truths.

### F-004-048 — Source labels used to bypass unordered-set association without physical identity justification

**Required behavior:** `REJECT` labeled scoring for the generic unordered-source profile.

---

# 11. Localization Metric Boundaries

### F-004-049 — `N=0` localization metric universe

Bias/MSE/RMSE over zero eligible matched errors are undefined.

**Required behavior:** return typed `NOT ASSESSED / UNDEFINED METRIC` rather than numeric zero or NaN without status.

### F-004-050 — `N=1` unbiased sample variance requested

Divisor `N-1` is zero.

**Required behavior:** `REJECT / UNDEFINED` for `s^2`; bias/MSE/RMSE may still be defined for the one observation.

### F-004-051 — Complex-valued quantity passed through real `e^2` localization metric

**Required behavior:** `INCOMPATIBLE / REQUIRE COMPLEX ERROR METRIC` such as a declared `|e|^2` definition.

### F-004-052 — Angular wrap/circular variable outside declared visible interval scored by naive subtraction

**Required behavior:** use the declared coordinate topology/metric; otherwise `REJECT` the metric interpretation.

### F-004-053 — Direction-cosine error reported as angle error without transformation

**Required behavior:** `REJECT` unit/coordinate label. `u` and `theta` metrics are distinct.

### F-004-054 — Miss/numerical failure assigned arbitrary angular penalty under ordinary RMSE

**Required behavior:** `REJECT` ordinary localization RMSE. A separate explicitly declared loss function may use penalties.

### F-004-055 — Matched-only RMSE reported without coverage/miss/failure context

**Required behavior:** `DIAGNOSTIC / INCOMPLETE EVIDENCE`; do not interpret as end-to-end estimator performance.

---

# 12. Probability / Denominator Boundaries

### F-004-056 — `N_eligible=0` for `P_res`

The estimator `N_resolved/N_eligible` is undefined.

**Required behavior:** `NOT ASSESSED / UNDEFINED METRIC`; do not return `0` or `1`.

### F-004-057 — No eligible truth opportunities for source-level `P_D`

**Required behavior:** `NOT ASSESSED / UNDEFINED METRIC`.

### F-004-058 — Numerical failures removed from baseline end-to-end `P_res` denominator

**Required behavior:** `REJECT` baseline metric identity; this becomes a conditional survivor metric and needs a distinct name.

### F-004-059 — Numerical failures removed from baseline source-level `P_D` opportunity denominator

**Required behavior:** same as F-004-058; preserve end-to-end opportunity universe or relabel conditional metric.

### F-004-060 — Invalid/outside-profile conditions counted as ordinary `R=0`

**Required behavior:** `REJECT` denominator construction. Incompatibility/invalidity is separate from scientific event non-success.

### F-004-061 — `P_res` numerator exceeds denominator

**Required behavior:** `REJECT` evidence integrity; counting/identity corruption exists.

### F-004-062 — Formal `P_FA` reported from unmatched estimates without null-protocol denominator

**Required behavior:** `REJECT` `P_FA` terminology; report spurious/unmatched-estimate evidence instead.

### F-004-063 — Observed `0/N` or `N/N` reported as exact population probability 0 or 1

**Required behavior:** `REJECT` certainty claim; finite-sample uncertainty remains.

---

# 13. Monte Carlo Adequacy / Uncertainty Boundaries

### F-004-064 — Universal `N` declared adequate for all metrics/conditions

**Required behavior:** `REJECT` universal adequacy claim; adequacy is metric/condition/claim dependent.

### F-004-065 — Outcome-driven stopping without predeclared inference-compatible rule

**Required behavior:** final evidence is exploratory/adaptively selected; confirmatory uncertainty claim is `INVALID` under a fixed-N interpretation.

### F-004-066 — Wilson interval used for dependent/clustered opportunities as if IID

**Required behavior:** `INCOMPATIBLE / REQUIRE DEPENDENCE-AWARE INTERVAL`.

### F-004-067 — Confidence level omitted

**Required behavior:** interval evidence is incomplete; scientific publication claim is `DIAGNOSTIC / INSUFFICIENT PROVENANCE`.

### F-004-068 — Bootstrap resamples snapshots when scientific independent unit is trial/device/session

**Required behavior:** `REJECT` uncertainty interpretation; resample the correct scientific unit.

### F-004-069 — Reference systematic uncertainty treated as Monte Carlo uncertainty that vanishes with `N`

**Required behavior:** `REJECT` uncertainty model; keep reference uncertainty separate.

### F-004-070 — Flat running metric curve presented as proof of convergence/adequacy

**Required behavior:** `DIAGNOSTIC / INSUFFICIENT EVIDENCE` unless precision/uncertainty/tail/failure diagnostics support the claim.

---

# 14. Manifold / Normalized Metric Boundaries

### F-004-071 — `rho(a,b)` with `a=0` or `b=0`

The normalized correlation denominator is zero.

**Required behavior:** metric `UNDEFINED`; type the manifold/input state or use another declared metric.

### F-004-072 — Relative matrix/vector error with zero reference norm

**Required behavior:** `UNDEFINED` unless a profile explicitly defines an absolute-error fallback or denominator floor with distinct metric identity.

### F-004-073 — `acos(rho)` with floating `rho` slightly outside `[0,1]`

**Required behavior:** numerical clipping may be used only as a declared roundoff guard when the pre-clipped value is within an explicit numerical tolerance; otherwise diagnose invalid input/computation rather than silently clamp arbitrary values.

### F-004-074 — Common-phase/complex-scale alignment removes channel-dependent mismatch

**Required behavior:** `REJECT` the metric interpretation. Gauge alignment may remove only declared nuisance degrees of freedom.

### F-004-075 — Principal-angle/projector comparison with undeclared unequal subspace dimensions

**Required behavior:** `REJECT / REQUIRE DECLARED UNEQUAL-DIMENSION POLICY`.

### F-004-076 — Individual eigenvector error used as authoritative metric under repeated/near-repeated eigenvalues

**Required behavior:** `DIAGNOSTIC / REQUIRE SUBSPACE METRIC`; raw eigenvector comparison is basis-sensitive.

---

# 15. Fair Comparison Boundaries

### F-004-077 — Methods evaluated on different uncontrolled source/noise realizations but compared as paired

**Required behavior:** `REJECT` paired-comparison claim.

### F-004-078 — One method tuned on final evaluation set

**Required behavior:** that evidence becomes tuning/development evidence; rerun held-out final evaluation for confirmatory comparison.

### F-004-079 — Oracle information differs but comparison labeled equal-information

**Required behavior:** `REJECT` fairness label; declare information asymmetry or harmonize inputs.

### F-004-080 — Geometry comparison changes aperture/resource budget without disclosure

**Required behavior:** `REJECT` topology-only superiority claim; report resource-conditioned comparison.

### F-004-081 — Runtime comparison uses kernel-only time for one method and end-to-end time for another

**Required behavior:** `REJECT` speedup claim until scopes match.

### F-004-082 — Non-overlapping/overlapping marginal CIs used as direct significance test

**Required behavior:** `REJECT` inferential shortcut; analyze the actual paired/unpaired effect according to design.

### F-004-083 — `p>0.05` used to claim equivalence

**Required behavior:** `REJECT` equivalence claim; require declared equivalence/noninferiority margin and appropriate inference.

### F-004-084 — Only winning conditions reported after full benchmark inspection

**Required behavior:** result is exploratory/selective evidence; full condition coverage/provenance must remain available.

---

# 16. Fixed-Point / HLS / FPGA Boundaries

### F-004-085 — Fixed-point format specified only as `16-bit`

**Required behavior:** `INCOMPLETE / REJECT BIT-ACCURATE CLAIM`; signedness, scale, widths, rounding, saturation, casts, and accumulator semantics are required.

### F-004-086 — ADC quantization and FPGA fixed-point error merged into one generic quantization metric

**Required behavior:** `REJECT` causal attribution; stages require separate provenance unless an explicitly aggregate metric is declared.

### F-004-087 — HLS/RTL mismatch checked only at final DOA while intermediate saturation is hidden

**Required behavior:** final metric may be reported but failure localization is incomplete; bit-accurate implementation-equivalence claim requires relevant internal/overflow evidence according to the implementation contract.

### F-004-088 — Board output generated with channel/packing mismatch

**Required behavior:** `HARDWARE_PROTOCOL / DATA-INTEGRITY FAILURE`; do not score final DOA as normal algorithm evidence.

### F-004-089 — Bitstream identity does not match recorded source/build

**Required behavior:** `REJECT` reproducibility/implementation claim until build provenance is resolved.

### F-004-090 — Timing closure fails but numerical C simulation passes

**Required behavior:** numerical verification may remain valid; deployable hardware-performance claim fails. Do not collapse timing failure into algorithm scientific failure.

### F-004-091 — Synthetic FPGA replay labeled physical array validation

**Required behavior:** `REJECT` physical-validation claim. Retain as digital implementation/integration evidence.

### F-004-092 — Hardware resource exhaustion prevents execution

**Required behavior:** `RESOURCE FAILURE`; preserve as engineering evidence. Whether it enters a scientific end-to-end performance denominator depends on the explicitly declared system-level claim, not automatically on localization metrics.

---

# 17. Publication / Reproducibility Boundaries

### F-004-093 — Figure/table cannot be traced to run/config/trial evidence

**Required behavior:** publication evidence package is `INCOMPLETE`; quantitative claim shall not be treated as reproducible evidence.

### F-004-094 — Manual spreadsheet value edits not recorded

**Required behavior:** `REJECT` deterministic recomputation claim; reconstruct from scripted/raw evidence or record explicit lineage.

### F-004-095 — Accepted/cited artifact silently overwritten in place

**Required behavior:** `REJECT` evidence integrity. Restore immutable history and issue a new corrected artifact/package identity.

### F-004-096 — Referenced raw/calibration artifact missing

**Required behavior:** exact reproduction level is not achieved; downgrade reproducibility claim and preserve the missing-dependency limitation.

### F-004-097 — Proprietary external dependency cannot be shared

**Required behavior:** not automatically invalid science, but reproducibility level/limitations must be explicit and strongest shareable evidence retained.

### F-004-098 — Environment differs but result still matches

**Required behavior:** numerical result may be supporting reproduction evidence; do not claim exact environment replay unless environment identity actually matches.

### F-004-099 — Reproducible package used as proof of physical correctness

**Required behavior:** `REJECT` epistemic overclaim. Reproducibility and correctness/physical validation remain distinct.

---

# 18. Calibration / Compatibility / Identifiability Interaction Boundaries

### F-004-100 — `calibrated` used as synonym for `physically validated`

**Required behavior:** `REJECT` claim language.

### F-004-101 — `compatible` used as synonym for `high performance`

**Required behavior:** `REJECT` interpretation. Compatibility means assumptions permit the method; performance is separately measured.

### F-004-102 — `identifiable` used as synonym for `compatible`

**Required behavior:** `REJECT` semantic collapse. Identifiability is a model/experiment property; compatibility is profile applicability.

### F-004-103 — Unidentifiable scene scored as estimator miss without preserving identifiability state

**Required behavior:** preserve `MODEL_UNIDENTIFIABLE / UNRESOLVED SCIENTIFIC STATE`; do not attribute all failure to the estimator.

### F-004-104 — Compatibility unresolved but silently treated compatible to continue benchmark

**Required behavior:** `UNRESOLVED`; no authoritative compatible-method metric until the uncertainty is resolved or the study explicitly evaluates an approximation/degraded profile.

---

# 19. Numeric / Data-Integrity Boundaries

### F-004-105 — Nonfinite truth/estimate enters metric silently

**Required behavior:** type source/root cause first. Do not propagate NaN/Inf through aggregate metrics as if it were ordinary numeric evidence.

### F-004-106 — Integer overflow/wrap in fixed-point path unrecorded

**Required behavior:** `NUMERICAL / IMPLEMENTATION FAILURE` or declared wrap behavior depending on profile; saturation/overflow counts must be preserved when relevant.

### F-004-107 — Artifact checksum mismatch

**Required behavior:** `DATA_INTEGRITY_FAILURE`; do not use artifact as authoritative evidence until resolved.

### F-004-108 — Channel count differs from geometry/calibration metadata

**Required behavior:** `REJECT` composition/evaluation.

### F-004-109 — Search sector excludes declared truth but miss probability is interpreted as estimator performance

**Required behavior:** either classify configuration as incompatible/invalid for that truth condition or explicitly declare sector-limited performance. Do not silently count as ordinary estimator miss under a full-sector claim.

### F-004-110 — Search-grid resolution interpreted as physical resolution

**Required behavior:** `REJECT` claim; grid is numerical discretization, not empirical resolving power.

---

## 20. Metric-Specific Eligibility Matrix

The following table captures the baseline ADR-004/VP-001 intent. Study-specific profiles may refine it but shall not silently contradict it.

| Trial / condition state | End-to-end `P_D` / `P_res` | Matched RMSE | Failure-rate metric | Compatibility report |
|---|---|---|---|---|
| valid successful output | eligible | eligible if matched | no failure | compatible |
| valid miss/unresolved | eligible as non-success | no missing angular error; matched subset only | not execution failure | compatible |
| numerical/algorithm failure on eligible compatible trial | eligible as non-success | not ordinary angular error | eligible failure event | compatible but execution failed |
| invalid input/reference/data integrity | excluded from ordinary scientific event universe | excluded | report invalidity separately | not valid evidence |
| outside selected profile / method incompatible | not ordinary event trial | excluded | not ordinary algorithm failure | incompatible |
| unresolved compatibility/identifiability state | no authoritative ordinary metric unless profile defines treatment | generally not authoritative | preserve unresolved state | unresolved |
| hardware/resource/protocol failure | depends on declared system-level claim; never silently forced into localization metric | not ordinary angular error | engineering failure evidence | implementation-specific |

No single `success` boolean can reproduce this matrix without losing semantics.

---

## 21. Gate-B / Gate-D Boundary Conditions Closed

The boundary conditions explicitly carried forward from Gate B and Gate D are resolved as follows:

```text
real-scalar e^2 metric domain                 -> F-004-051
zero-vector normalized manifold metric        -> F-004-071
relative-error zero denominator               -> F-004-072
assignment ties                               -> F-004-044
principal-angle unequal dimensions            -> F-004-075
Wilson non-IID use                            -> F-004-066
N=1 sample variance                           -> F-004-050
singular whitening/inverse                    -> F-004-040
duplicate channel IDs                         -> invalid identity/composition, REJECT
duplicate trial IDs                           -> F-004-008/F-004-009
invalid unit strings                          -> REJECT at validated input boundary
missing resolved defaults                     -> F-004-019
unknown RNG family/version                    -> F-004-014
schema-version hash ambiguity                 -> F-004-020
incomplete cache dependencies                 -> F-004-025
resume after config/source change             -> new run/condition identity required
missing/stale calibration                     -> incompatible/outside calibration domain under ADR-003
packing/endianness mismatch                   -> F-004-088
bitstream/build mismatch                      -> F-004-089
missing publication raw artifact              -> F-004-096
backend nondeterminism under exact replay      -> exact-replay claim incompatible unless declared/resolved
```

No carried-forward boundary remains semantically unclassified.

---

## 22. Forbidden Silent Coercions

ADR-004-compliant evidence processing shall never silently:

- convert `UNRESOLVED` to `VALID`;
- convert method incompatibility into `R=0`;
- remove numerical failures from end-to-end event denominators;
- convert miss/failure into an arbitrary angular penalty under ordinary RMSE;
- truncate extra estimated peaks before evidence recording;
- pad missing estimates with synthetic DOAs;
- infer truth authority from file name/tool source;
- infer units from numeric magnitude;
- infer source count from rank or output cardinality;
- infer physical validation from Python/FPGA agreement;
- infer exact replay from one integer seed;
- infer equivalence from `p>0.05`;
- infer adequate Monte Carlo evidence from a visually flat curve;
- infer `P_FA` from generic spurious estimates without a null protocol;
- infer physical resolution from grid spacing or beamwidth;
- silently repair/correct data and score the repaired result as original evidence;
- silently overwrite accepted publication artifacts.

---

## 23. Gate-F Checklist

```text
Truth/reference invalidity classes defined                   PASS
Oracle/truth leakage boundary defined                        PASS
Study/condition/trial identity failures defined              PASS
RNG/CRN failure modes defined                                PASS
Config/hash/provenance boundaries defined                    PASS
VP-001 outside-profile cases defined                         PASS
Covariance/subspace boundaries defined                       PASS
Association/cardinality/tie boundaries defined               PASS
Localization metric N=0/N=1/coordinate boundaries defined    PASS
P_D/P_res denominator and zero-denominator boundaries        PASS
Monte Carlo adequacy/CI/dependence boundaries defined        PASS
Normalized manifold/projector boundaries defined             PASS
Fair-comparison/tuning/equivalence boundaries defined        PASS
Fixed/HLS/FPGA/protocol/resource boundaries defined          PASS
Publication/reproducibility integrity boundaries defined     PASS
Calibration/compatibility/identifiability interactions       PASS
Data-integrity/nonfinite/search-sector boundaries defined    PASS
Metric-specific eligibility matrix defined                   PASS
Gate-B/Gate-D carried conditions resolved                    PASS
Forbidden silent coercions enumerated                        PASS
Blocking boundary/failure ambiguity                          NONE IDENTIFIED
```

---

## 24. Boundary Analysis Conclusion

ADR-004 has sufficient boundary semantics to distinguish malformed evidence, valid but out-of-profile science, compatible-trial non-success, execution failure, unresolved scientific state, and metric-specific ineligibility.

The key governing principle is:

> Failure shall be represented at the earliest scientifically correct layer, preserved through downstream evidence, and mapped into each metric by an explicit eligibility/denominator policy rather than by silent filtering, numeric coercion, or overloaded success flags.

This boundary analysis is candidate evidence for Gate F. Formal Gate-F PASS is recorded separately in `ADR-004_GATE_F_AUDIT.md`.
