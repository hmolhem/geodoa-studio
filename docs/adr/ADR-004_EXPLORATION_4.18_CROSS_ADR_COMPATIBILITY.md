# ADR-004 Exploration 4.18 — Cross-ADR Compatibility with ADR-001 / ADR-002 / ADR-003

- **ADR:** ADR-004 — Validation, Reproducibility, and Scientific Evidence
- **Phase:** 0C — Scientific Foundations
- **Exploration:** 4.18
- **Status:** EXPLORATION COMPLETE — CANDIDATE CONTRACT, NOT ACCEPTED
- **Depends on:** Accepted ADR-001, ADR-002, ADR-003; ADR-004 Explorations 4.1–4.17

## 1. Question

> Are the candidate evidence, validation, metric, stochastic, failure, hardware, provenance, and publication contracts developed in ADR-004 semantically compatible with the already accepted geometry/phase conventions of ADR-001, signal/covariance conventions of ADR-002, and sensor-imperfection/calibration/compatibility conventions of ADR-003, without redefining or weakening their authority?

This exploration performs a cross-ADR consistency audit before the initial Phase-1 validation profile and final cross-section reconciliation.

---

## 2. Core Principle

ADR-004 is an **evidence contract**, not a replacement physical-model contract.

Candidate authority rule:

```text
ADR-001 owns geometry / coordinate / receive-phase / reference conventions.
ADR-002 owns signal / propagation / snapshot / covariance / SNR / source-noise conventions.
ADR-003 owns sensor-imperfection / calibration / compatibility / identifiability conventions.
ADR-004 owns how evidence about those models is generated, scored, compared, qualified, reproduced, and published.
```

Candidate rule:

> ADR-004 shall consume accepted scientific semantics from ADR-001/002/003 as authoritative dependencies and shall not silently redefine their physical, statistical, calibration, or compatibility meanings through metric, failure, benchmark, or implementation convenience.

---

## 3. Authority Matrix

| Topic | Governing ADR | ADR-004 role |
|---|---|---|
| coordinate frame / angle convention | ADR-001 | preserve in truth, metrics, provenance |
| receive steering sign / phase reference | ADR-001 | verify/compare without redefining |
| physical geometry / active-channel identity | ADR-001 | condition identity and comparison resource |
| exact delay / far-field / narrowband approximations | ADR-002 | evidence role, compatibility, validation profile |
| snapshot semantics | ADR-002 | trial/condition provenance and adequacy |
| covariance / centered covariance / rank | ADR-002 | metric/reference definitions and tests |
| SNR / source / noise statistics | ADR-002 | condition/fair-comparison provenance |
| sensor operator graph | ADR-003 | perturbation-study condition and validation reference |
| calibration / reference plane / validity domain | ADR-003 | evidence/provenance/failure tracking |
| compatibility / identifiability | ADR-003 | typed benchmark eligibility/outcome |
| verification / validation / reproducibility | ADR-004 | governing evidence semantics |
| Monte Carlo / metrics / uncertainty | ADR-004 | governing evidence semantics |
| fair comparison / failure recording | ADR-004 | governing evidence semantics |
| float/fixed/FPGA cross-validation | ADR-004 | implementation evidence built on ADR-001/2/3 |

Candidate rule:

> When terminology overlaps, the upstream accepted ADR retains authority over scientific meaning; ADR-004 may only define the evidence treatment of that meaning.

---

## 4. ADR-001 Compatibility — Receive Steering Sign

ADR-001 accepted the receive steering convention

\[
a_n(\hat u,f)
=
\exp\left[-jk(\mathbf r_n-\mathbf r_{ref})^T\hat u\right].
\]

For the accepted 1-D profile,

\[
a_n(\theta,f)
=
\exp\left[-jk(x_n-x_{ref})\sin\theta\right].
\]

ADR-004 manifold metrics compare representations generated under this convention.

Candidate rule:

> ADR-004 validation/reference generation shall not introduce a second steering-sign convention for convenience. Any external artifact using a different convention requires an explicit, proven transform before comparison.

**Audit result:** compatible; no redefinition found.

---

## 5. ADR-001 Compatibility — Look Direction / Propagation Direction

ADR-001 distinguishes:

```text
look direction = array -> source
propagation direction = -look direction
```

Candidate rule:

> Truth provenance, external-tool registration, measured-manifold import, and physical-validation records in ADR-004 shall preserve this distinction rather than infer direction from sign conventions or file labels.

**Audit result:** compatible.

---

## 6. ADR-001 Compatibility — Angle and Direction Cosine

ADR-001 accepted the 1-D mapping

\[
u=\sin\theta,
\qquad
\theta\in[-\pi/2,\pi/2].
\]

ADR-004 Explorations 4.7, 4.9, and 4.14 intentionally distinguish metrics in `theta` and `u`.

Candidate rule:

> Metric coordinate is an evidence choice, but the coordinate transformation and visible-sector semantics remain governed by ADR-001.

Uniform weighting in `theta` shall not be mislabeled uniform weighting in `u`.

**Audit result:** compatible and explicitly aligned.

---

## 7. ADR-001 Compatibility — Phase Reference and Common Phase Gauge

ADR-001 distinguishes coordinate origin, expansion origin, phase reference, and active-channel selection, and accepts stable nominal-geometry phase reference semantics.

ADR-004 manifold comparison permits phase-invariant/projective metrics only when common phase is scientifically a gauge.

Candidate rule:

> ADR-004 gauge alignment removes only nuisance freedoms already justified by the governing scientific model; it shall not move the ADR-001 phase reference or conceal channel-dependent phase distortion.

A projective manifold match does not mean absolute phase-reference equality.

**Audit result:** compatible; authority boundary clarified.

---

## 8. ADR-001 Compatibility — Stable Channel Identity

ADR-001 requires stable channel identity and rejects silent sorting/reindexing.

ADR-004 Explorations 4.15–4.17 treat channel order as hardware/data provenance.

Candidate rule:

> Reordering that changes the relationship between sample channel and physical sensor is a scientific data-integrity transformation/failure unless explicitly declared and inverted.

**Audit result:** compatible and strengthened operationally.

---

## 9. ADR-001 Compatibility — Physical Position Authority

ADR-001 makes physical positions in meters authoritative and rejects silent normalization/snapping.

Candidate rule:

> ADR-004 configuration canonicalization may normalize **units**, but shall not normalize **geometry itself** by wavelength, aperture, sorting, lattice snapping, or centering unless the scientific profile explicitly defines that derived representation.

`0.5 m` and `50 cm` may canonicalize to the same physical value; `[0, 0.5] m` and `[0, 1] normalized` are not silently equivalent configurations.

**Audit result:** compatible; important canonicalization guard established.

---

## 10. ADR-002 Compatibility — Exact Path before Approximation

ADR-002 requires exact propagation/delay semantics before far-field/narrowband approximations.

Candidate rule:

> ADR-004 verification/validation evidence shall identify whether a reference is exact-path, far-field, narrowband, or another approximation profile; numerical agreement within an approximation cannot be promoted to validation of a more general physical model.

**Audit result:** compatible.

---

## 11. ADR-002 Compatibility — Far-Field and Narrowband Independence

ADR-002 treats far-field and narrowband as independent assumptions.

Candidate rule:

> ADR-004 profile identity, compatibility, and benchmark conditions shall record these assumptions independently rather than encode one composite `farfield_narrowband=true` semantic that obscures which approximation is responsible for validity/failure.

**Audit result:** compatible.

---

## 12. ADR-002 Compatibility — Narrowband Adequacy Metric

ADR-002 introduced aperture delay and narrowband indicator concepts such as

\[
\Delta\tau_{ap}
=
\max_n\tau_n-\min_n\tau_n,
\]

\[
\eta_{NB}
=2\pi\nu_{max}\Delta\tau_{ap}.
\]

Candidate rule:

> ADR-004 may validate, sweep, or threshold such quantities under a profile-specific acceptance policy, but it shall not replace the ADR-002 physical definition with an empirical performance threshold.

Metric and acceptance remain distinct.

**Audit result:** compatible.

---

## 13. ADR-002 Compatibility — Snapshot Semantics

ADR-002 defines a snapshot as a simultaneous-equivalent coherent observation at a common receiver epoch/state or calibrated equivalent.

Candidate rule:

> ADR-004 Monte Carlo `trial` is not a snapshot. Trial identity/adequacy shall never reinterpret snapshot count `L` as the number of Monte Carlo trials.

Conceptually:

```text
study -> condition -> Monte Carlo trial -> L snapshots inside that trial
```

unless a different declared stochastic hierarchy is used.

**Audit result:** compatible; semantic separation explicit.

---

## 14. ADR-002 Compatibility — Covariance Terminology

ADR-002 distinguishes second moment, covariance, centered sample covariance, source covariance rank, observed subspace rank, and source count.

Candidate rule:

> ADR-004 covariance error, eigenspace metrics, rank/failure diagnostics, and publication labels shall retain the exact covariance object identity rather than use bare `covariance matrix` ambiguously.

For example,

\[
\hat R_{centered}
\]

and uncentered second moment are not interchangeable evidence inputs.

**Audit result:** compatible.

---

## 15. ADR-002 Compatibility — Finite-Sample Rank

ADR-002 preserves centered sample covariance rank limits such as

\[
\operatorname{rank}(\hat R_{centered})
\le
\min(N,L-1).
\]

Candidate rule:

> ADR-004 numerical/failure logic shall not classify mathematically expected finite-sample rank deficiency as an implementation defect merely because a full-rank matrix was assumed implicitly.

Compatibility and model-order feasibility must be assessed first.

**Audit result:** compatible; failure taxonomy guard added.

---

## 16. ADR-002 Compatibility — Source Count versus Rank

ADR-002 distinguishes source count from source covariance rank and observed signal-subspace rank.

Candidate rule:

> ADR-004 detection/model-order/resolution metrics shall not call every rank deficiency a missed physical source. Coherent-source rank collapse and estimator output cardinality are different evidence objects.

**Audit result:** compatible.

---

## 17. ADR-002 Compatibility — SNR Is Typed

ADR-002 rejects bare SNR and requires typed signal/noise semantics.

ADR-004 Explorations 4.9, 4.12, 4.16, and 4.17 require SNR provenance.

Candidate rule:

> No ADR-004 comparison, plot label, config hash, or publication claim shall treat numeric `SNR=0 dB` as sufficient condition identity without its accepted SNR definition/profile.

**Audit result:** compatible and strongly reinforced.

---

## 18. ADR-002 Compatibility — White versus Colored Noise

ADR-002/003 establish that noise covariance and whitening affect ordinary subspace methods.

Candidate rule:

> ADR-004 fair comparisons and manifold/eigenspace metrics shall distinguish ordinary Euclidean/unwhitened and whitened spaces. Whitening is an explicit transform/profile, not an evaluation-side convenience applied to one method only.

**Audit result:** compatible.

---

## 19. ADR-002 Compatibility — MIMO Provenance

ADR-002 preserves physical `(Tx_i,Rx_j)` provenance and treats virtual geometry as derived.

Candidate rule:

> ADR-004 run/data/hardware provenance shall preserve physical MIMO channel identity where applicable; virtual-array ordering/geometry is a derived artifact and shall not replace physical channel provenance.

**Audit result:** compatible.

---

## 20. ADR-003 Compatibility — Sensor Operator Graph

ADR-003 rejects a universal imperfection matrix and accepts a typed ordered sensor operator graph.

Candidate rule:

> ADR-004 perturbation studies may isolate one operator at a time for diagnosis, but publication wording shall not imply that all sensor imperfections are one commutative additive/multiplicative error model.

Combined studies must preserve operator ordering and noncommutativity where material.

**Audit result:** compatible.

---

## 21. ADR-003 Compatibility — Manifold Identities

ADR-003 distinguishes

```text
a_nom
a_phys
a_meas
a_em
a_cal
optional a_truth
```

Candidate rule:

> ADR-004 manifold metrics shall identify the exact manifold roles being compared. A scalar `manifold_error` without endpoint identities is incomplete.

Examples:

```text
a_phys vs a_nom        -> physical/model mismatch
a_meas vs a_phys        -> measurement/receiver effect
a_cal vs a_phys         -> calibration residual
a_fixed vs a_float      -> implementation numerical error
```

**Audit result:** compatible and operationally clarified.

---

## 22. ADR-003 Compatibility — Phase-1 Identity Sensor

ADR-003 accepts Phase-1 ideal sensor semantics with

\[
H_{sensor}^{Phase1}\equiv I.
\]

Candidate rule:

> ADR-004 initial Phase-1 validation may use identity sensor behavior as the declared accepted profile, but shall not call that evidence validation of real sensor hardware or calibrated full-wave behavior.

**Audit result:** compatible.

---

## 23. ADR-003 Compatibility — Calibration Is Not Validation

ADR-003 explicitly separates calibration from validation.

ADR-004 Exploration 4.1 does the same.

Candidate rule:

> A calibration residual, calibration fit, or successful correction shall not be reported as independent validation unless held-out/external evidence satisfying the declared validation contract exists.

**Audit result:** fully compatible; no semantic drift found.

---

## 24. ADR-003 Compatibility — Reference Channel / Gauge

ADR-003 states that choosing a reference channel fixes a gauge but does not prove that channel ideal.

Candidate rule:

> ADR-004 gauge-aware metrics, hardware alignment, and calibration provenance shall preserve this distinction; gauge fixing may enable comparison but cannot be interpreted as reference-channel truth.

**Audit result:** compatible.

---

## 25. ADR-003 Compatibility — Coupling Models

ADR-003 distinguishes Z/S/load-transfer/coupling/full-manifold representations and rejects universal `S21 = C21` semantics.

Candidate rule:

> ADR-004 external-tool/manifold/coupling validation shall record which representation is being compared and the reference plane/port state. Agreement between different representations requires an explicit valid transform.

**Audit result:** compatible.

---

## 26. ADR-003 Compatibility — Embedded Patterns / Double Counting

ADR-003 warns that embedded/full-wave patterns may already include coupling effects.

Candidate rule:

> ADR-004 provenance and perturbation studies shall record included effects so imported measured/CST manifolds are not subsequently multiplied by an additional coupling operator without evidence that the effect is absent from the artifact.

**Audit result:** compatible.

---

## 27. ADR-003 Compatibility — Timing Sign Semantics

ADR-003 distinguishes physical delay, sampling-time offset, SRO, CFO, jitter, and latency, including opposite phase signs for physical delay versus later sampling under the accepted temporal convention.

Candidate rule:

> ADR-004 hardware timing provenance shall not collapse algorithmic latency, sampling skew, physical channel delay, and LO/CFO effects into one `delay` field or one phase-error metric.

**Audit result:** compatible.

---

## 28. ADR-003 Compatibility — ADC Quantization versus FPGA Fixed Point

ADR-003 explicitly states:

```text
ADC quantization != FPGA fixed-point arithmetic
```

ADR-004 Exploration 4.15 defines fixed-point cross-validation.

Candidate rule:

> ADC resolution/full-scale/quantizer semantics remain sensor/acquisition model parameters; FPGA word lengths/casts/rounding/saturation remain implementation parameters. They may coexist in one pipeline but shall have separate provenance and error attribution.

**Audit result:** fully compatible.

---

## 29. ADR-003 Compatibility — IQ / Nonlinearity / Pseudocovariance

ADR-003 allows augmented/improper signal behavior under IQ imbalance and nonlinear receiver effects.

Candidate rule:

> ADR-004 ordinary covariance/subspace metrics are valid only for profiles whose compatibility status supports them. If augmented statistics are required, ordinary Phase-1 metrics cannot be used silently as if the model were unchanged.

**Audit result:** compatible; profile boundary emphasized.

---

## 30. ADR-003 Compatibility — Compatibility Is Multi-Axis, Not Boolean

ADR-003 accepts typed compatibility states rather than one boolean.

ADR-004 Exploration 4.13 also rejects bare `success` booleans.

Candidate rule:

> ADR-004 benchmark eligibility shall consume ADR-003 compatibility status without reducing it to `compatible=true/false`. An analysis may derive a metric-specific eligibility decision, but the original compatibility axes/status remain authoritative provenance.

**Audit result:** compatible and mutually reinforcing.

---

## 31. ADR-003 Compatibility — Identifiability versus Compatibility

ADR-003 distinguishes identifiability from compatibility.

Candidate rule:

> ADR-004 `UNRESOLVED`, ambiguity, miss, failure, and incompatibility statuses shall not collapse identifiability failure into ordinary estimator non-success. Identifiability status is a property of the model/experiment relation and must remain visible.

**Audit result:** compatible.

---

## 32. ADR-003 Compatibility — Rank Preservation under Sensor Operators

ADR-003 notes that nonsingular linear sensor transforms can preserve signal rank while rotating/conditioning subspaces, whereas rank-deficient transforms may reduce rank.

Candidate rule:

> ADR-004 eigenspace/DOA diagnostics shall not infer source disappearance solely from rotated subspace geometry after a nonsingular sensor transform; rank, conditioning, manifold matching, and model-order evidence must be assessed separately.

**Audit result:** compatible.

---

## 33. ADR-003 Compatibility — Time-Varying Sensor Operators

ADR-003 notes that time-varying sensor operators may alter apparent rank and that

\[
E[H_t R H_t^H]
\neq
\bar H R\bar H^H
\]

in general.

Candidate rule:

> ADR-004 Monte Carlo/hierarchical provenance shall preserve redraw/state scope for time-varying sensor imperfections rather than replacing them with one average static matrix unless that approximation is explicitly the model under test.

**Audit result:** compatible.

---

## 34. ADR-003 Compatibility — Reference Uncertainty

ADR-003 distinguishes estimator error from reference error; ADR-004 Exploration 4.11 expands uncertainty treatment.

Candidate rule:

> ADR-004 confidence intervals on estimator Monte Carlo metrics shall not absorb physical reference uncertainty unless an explicit propagation model is declared. Reference uncertainty remains a distinct evidence layer.

**Audit result:** compatible.

---

## 35. ADR-003 Compatibility — Measured/CST Manifold Epistemic Role

ADR-003 states that measured/CST/full-wave manifolds are aggregate calibrated/model responses and not automatically truth.

ADR-004 Explorations 4.2, 4.16, 4.17 preserve epistemic/provenance roles.

Candidate rule:

> Importing a CST or measured manifold into a reproducibility package shall preserve its role as model prediction, measured reference, calibrated artifact, or other declared evidence class; content hash does not promote epistemic authority.

**Audit result:** compatible.

---

## 36. Cross-ADR Metric Alignment

ADR-003 accepted candidate/manifold diagnostics such as

\[
\rho
=
\frac{|a^Hb|}{\|a\|\|b\|},
\qquad
\alpha=\cos^{-1}\rho,
\qquad
1-\rho^2.
\]

ADR-004 Exploration 4.14 reuses them as evidence metrics.

Candidate rule:

> ADR-004 does not redefine these scientific quantities; it standardizes when they are appropriate, which reference roles they compare, and how they are reported/provenanced.

**Audit result:** compatible.

---

## 37. Cross-ADR MUSIC Alignment

ADR-003 accepts matched-manifold MUSIC reasoning and distinguishes data/projector error from search-manifold mismatch.

ADR-004 4.14/4.15 uses truth-direction leakage, projector error, spectrum error, and final DOA error as distinct levels.

Candidate rule:

> ADR-004 shall preserve separate data/eigenspace and search-manifold discrepancy channels; a single MUSIC denominator error shall not be attributed uniquely to sensor mismatch without controlled evidence.

**Audit result:** compatible.

---

## 38. Cross-ADR Failure-State Alignment

Potential semantic collision:

```text
ADR-003 compatibility status
ADR-004 failure status
ADR-004 metric eligibility
```

These are three different objects.

Candidate rule:

> Compatibility describes whether the model/method/profile relation is scientifically admissible; failure status describes what occurred during a concrete execution/evaluation; metric eligibility describes whether that outcome participates in one specific metric denominator.

Example:

```text
method/profile = COMPATIBLE
trial output = VALID_NO_DETECTION
matched-only RMSE eligibility = false
P_D eligibility = true
```

or

```text
method/profile = INCOMPATIBLE
execution status = NOT_EXECUTED_BY_POLICY
ordinary RMSE eligibility = false
```

**Audit result:** compatible after explicit three-layer separation.

---

## 39. Cross-ADR Truth / Calibration / Reference Alignment

Potential semantic collision:

```text
truth
reference
calibration estimate
validation measurement
```

Candidate rule:

> ADR-004 truth provenance shall preserve ADR-003 calibration distinction and shall not allow a calibration estimate to become `truth` simply because it is the only available numeric reference.

If scoring is estimate-to-calibration-reference, the metric shall be labeled accordingly.

**Audit result:** compatible.

---

## 40. Cross-ADR Hardware Boundary Alignment

ADR-004 4.15 introduces float/fixed/FPGA evidence without modifying ADR-001/2/3 physical semantics.

Candidate rule:

> Hardware acceleration begins from an accepted digital/scientific boundary. Moving an operation across PS/PL or changing numerical representation does not authorize changing sensor ordering, snapshot definition, SNR convention, phase reference, calibration reference plane, or algorithm profile silently.

**Audit result:** compatible.

---

## 41. Cross-ADR Provenance Alignment

ADR-004 4.16 canonicalizes semantic configuration.

Potential risk: canonicalization could accidentally erase distinctions that ADR-001/2/3 treat as scientifically meaningful.

Candidate non-collapsible fields include:

```text
phase reference
coordinate convention
physical channel order
far-field status
narrowband status
snapshot definition
SNR profile
covariance object type
source/noise statistics
sensor operator profile
calibration artifact/domain
compatibility profile
reference plane
ADC quantization profile
```

Candidate rule:

> Configuration canonicalization may normalize representation, units, and ordering only where upstream ADR semantics explicitly permit equivalence; it shall not canonicalize away a scientific distinction.

**Audit result:** compatible with this guard.

---

## 42. Cross-ADR Publication Alignment

ADR-004 4.17 freezes publication evidence.

Candidate rule:

> A publication package shall identify the exact accepted ADR/profile revisions governing its scientific semantics. Later ADR revisions do not retroactively change the meaning of a frozen package.

If a governing scientific convention changes materially, affected evidence requires explicit migration/reanalysis/new identity.

**Audit result:** compatible.

---

## 43. No Duplicate Authority Rule

Several ADR-004 sections restate upstream facts for evidence purposes.

Candidate rule:

> The governing ADR-004 draft should avoid presenting restated ADR-001/2/3 equations as newly accepted ADR-004 physical conventions. Restatements shall be marked as inherited dependencies or examples.

This prevents future divergence if an upstream ADR is revised.

---

## 44. Upstream Revision Rule

If ADR-001, ADR-002, or ADR-003 is superseded later:

Candidate rule:

> ADR-004 evidence packages retain the exact upstream ADR/profile versions under which they were generated. New runs use the new governing version only after compatibility/migration assessment.

No silent reinterpretation of historical results is allowed.

---

## 45. Cross-ADR Compatibility Check for Future Profiles

Every future validation profile should answer:

```text
Which ADR-001 geometry/phase profile applies?
Which ADR-002 propagation/snapshot/covariance/SNR profile applies?
Which ADR-003 sensor/calibration/compatibility profile applies?
Which ADR-004 evidence/metric/failure/provenance profile applies?
```

Candidate rule:

> A validation profile is incomplete if it cites ADR-004 metrics without identifying the upstream scientific semantics those metrics evaluate.

---

## 46. Potential Conflict Audit

The exploration specifically checked the following possible conflict areas:

1. **phase-invariant manifold metrics vs fixed phase reference** — no conflict if gauge removal is explicitly metric-level and does not redefine phase reference;
2. **configuration unit normalization vs no geometry normalization** — no conflict if only units/representation are canonicalized;
3. **failure as `R=0` vs incompatibility** — no conflict if metric mapping preserves original compatibility/failure status;
4. **matched-only RMSE vs missed-source evidence** — no conflict if conditioning/coverage remain explicit;
5. **whitened metrics vs ordinary covariance model** — no conflict if whitening is a declared compatible transform/profile;
6. **fixed-point quantization vs ADC quantization** — no conflict; separate pipeline stages/provenance;
7. **board validation vs physical validation** — no conflict; distinct evidence layers;
8. **CST/measured artifact hashing vs truth role** — no conflict; identity does not imply epistemic authority;
9. **trial identity vs snapshot identity** — no conflict; different hierarchy levels;
10. **source count vs subspace rank/model order** — no conflict if typed separately;
11. **metric threshold vs compatibility threshold** — no conflict if metric/acceptance/compatibility remain separate;
12. **common-phase alignment vs calibration** — no conflict if alignment is evaluation gauge handling, not inferred physical calibration.

**Audit result:** no blocking contradiction identified.

---

## 47. Semantic Drift Risks to Carry into 4.20

No contradiction was found, but the governing ADR draft must guard against several wording risks:

```text
RISK-01  using "truth" for measured/CST/calibration reference
RISK-02  using "valid" when compatibility vs execution vs metric eligibility is meant
RISK-03  using "covariance" without object type
RISK-04  using "delay" across physical/sampling/algorithm latency semantics
RISK-05  using "resolution" for grid spacing/beamwidth/peak count
RISK-06  using "equivalent" without gauge/engineering margin
RISK-07  using "hardware validated" for synthetic board replay
RISK-08  using "same configuration" when upstream ADR/profile versions differ
RISK-09  using "source count" for subspace rank/model order
RISK-10  using "calibrated" as evidence of physical validity
```

Candidate rule:

> These are drafting/reconciliation risks, not current contradictions, and shall be explicitly checked during Exploration 4.20 and pre-Gate review.

---

## 48. Candidate Compatibility Outcome

At the end of this exploration:

```text
ADR-001 compatibility: PASS AT EXPLORATION LEVEL
ADR-002 compatibility: PASS AT EXPLORATION LEVEL
ADR-003 compatibility: PASS AT EXPLORATION LEVEL
Blocking contradictions: NONE IDENTIFIED
Authority-boundary clarifications: REQUIRED IN GOVERNING DRAFT
Formal acceptance status: NOT ACCEPTED
```

This is not a Gate A–F PASS and does not accept ADR-004.

---

## 49. Candidate Decisions from Exploration 4.18

- **D4.18-01:** ADR-004 is an evidence contract and shall not redefine scientific semantics owned by ADR-001/002/003.
- **D4.18-02:** ADR-001 remains authoritative for geometry, coordinate, receive-phase, phase-reference, channel-identity, and physical-position semantics.
- **D4.18-03:** ADR-002 remains authoritative for propagation approximations, snapshot semantics, covariance objects, rank, source/noise statistics, SNR, and MIMO channel provenance.
- **D4.18-04:** ADR-003 remains authoritative for sensor operator graphs, calibration, reference planes, compatibility, identifiability, timing-imperfection semantics, ADC quantization, and measured/full-wave manifold roles.
- **D4.18-05:** ADR-004 gauge-aware metrics may remove only nuisance freedoms already justified by the governing upstream model and shall not redefine physical references.
- **D4.18-06:** Configuration canonicalization may normalize units/representation but shall not erase scientific distinctions established by upstream ADRs.
- **D4.18-07:** Monte Carlo trial identity and ADR-002 snapshot identity are distinct hierarchy levels.
- **D4.18-08:** Source count, source covariance rank, observed subspace rank, estimator model order, and output cardinality remain distinct across evidence layers.
- **D4.18-09:** Compatibility status, execution/failure status, and metric eligibility are three distinct objects.
- **D4.18-10:** Calibration estimate/reference, measured reference, external-tool prediction, and truth remain epistemically distinct.
- **D4.18-11:** ADC quantization and FPGA fixed-point arithmetic remain separate pipeline stages with separate provenance/error attribution.
- **D4.18-12:** Whitening is an explicit compatible transform/profile and shall not be silently applied asymmetrically in evaluation.
- **D4.18-13:** Physical sensor validation remains distinct from synthetic FPGA/board implementation validation.
- **D4.18-14:** Imported CST/measured artifact identity/content hash does not promote the artifact to truth.
- **D4.18-15:** Repeated upstream equations in ADR-004 shall be labeled inherited dependencies/examples rather than duplicate physical authority.
- **D4.18-16:** Historical evidence retains exact upstream ADR/profile versions and shall not be silently reinterpreted after future ADR revisions.
- **D4.18-17:** Future validation profiles shall identify applicable ADR-001, ADR-002, ADR-003, and ADR-004 profiles together.
- **D4.18-18:** No blocking contradiction among ADR-004 candidate decisions and accepted ADR-001/002/003 was identified at exploration level.
- **D4.18-19:** Semantic-drift risks listed in Section 47 shall be explicit checks during 4.20 and the pre-Gate consistency review.

---

## 50. Exploration 4.18 Conclusion

Exploration 4.18 is complete at candidate-contract level.

The central rule is:

> ADR-004 shall remain strictly downstream of the accepted scientific semantics in ADR-001, ADR-002, and ADR-003: it defines how models and implementations are verified, validated, scored, compared, qualified, reproduced, and published, but it does not acquire authority to redefine geometry/phase, signal/covariance, or sensor/calibration semantics. The cross-ADR audit found no blocking contradiction, provided that the governing draft preserves explicit authority boundaries, compatibility/failure/eligibility separation, epistemic reference roles, and non-collapsible upstream configuration fields.

No acceptance gate is started or passed by this exploration.

The next exploration is:

```text
4.19 — Initial Phase-1 Validation Profile
```
