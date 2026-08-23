# ADR-004 Exploration 4.19 — Initial Phase-1 Validation Profile

- **ADR:** ADR-004 — Validation, Reproducibility, and Scientific Evidence
- **Phase:** 0C — Scientific Foundations
- **Exploration:** 4.19
- **Status:** EXPLORATION COMPLETE — CANDIDATE CONTRACT, NOT ACCEPTED
- **Depends on:** Accepted ADR-001, ADR-002, ADR-003; ADR-004 Explorations 4.1–4.18

## 1. Question

> What is the smallest practical, scientifically defensible GeoDOA validation profile that can serve as the first implementation target for software verification, Monte Carlo benchmarking, algorithm/geometry comparison, and later float/fixed/FPGA cross-validation without introducing sensor/model complexity that Phase 1 has not yet accepted?

This exploration binds the accepted upstream scientific conventions and ADR-004 evidence contracts into one executable Phase-1 benchmark profile.

---

## 2. Profile Identity

Candidate profile name:

```text
VP-001 — Phase-1 Ideal Far-Field Narrowband 1-D DOA Validation Profile
```

Candidate short alias:

```text
VP-001
```

Candidate purpose:

```text
first reproducible software-scientific reference profile
first stochastic DOA benchmark profile
first geometry-comparison profile
first float/fixed/FPGA cross-validation source profile
```

Candidate rule:

> VP-001 shall be intentionally narrow. It establishes a trustworthy baseline before calibrated manifolds, coupling, colored noise, coherent-source remedies, wideband, near-field, TDM-MIMO, or physical-array validation are introduced.

---

## 3. Governing Scientific Profiles

VP-001 inherits:

```text
ADR-001 accepted 1-D geometry / angle / receive-steering conventions
ADR-002 PM-001 Reference Far-Field Narrowband Receive-Array Profile
ADR-003 Phase-1 ideal sensor-imperfection profile
ADR-004 evidence/metric/provenance contract
```

Candidate rule:

> VP-001 does not redefine these upstream conventions; it composes them into one executable validation profile.

---

## 4. Geometry Scope

VP-001 supports declared 1-D receive-array geometries with physical sensor positions

\[
x_n\in\mathbb R\;\text{meters}.
\]

Initial implementation may include:

```text
ULA
nested array
co-prime array
user-declared sparse linear array
```

provided the geometry is compatible with the tested algorithm.

Candidate rule:

> Physical positions in meters are authoritative; no silent wavelength normalization, sorting, snapping, duplicate removal, or active-mask-induced phase-reference change is allowed.

---

## 5. Coordinate / Steering Convention

Under ADR-001:

\[
\hat u(\theta)=[\sin\theta,\cos\theta,0]^T,
\]

with broadside

\[
\theta=0,
\]

and visible sector

\[
\theta\in[-\pi/2,\pi/2].
\]

Receive steering:

\[
a_n(\theta,f)
=
\exp[-jk(x_n-x_{ref})\sin\theta].
\]

Candidate rule:

> All VP-001 truth generation, manifold computation, search grids, metrics, plots, and hardware vectors use this convention unless an explicit external-artifact transform is proven and recorded.

---

## 6. Phase Reference

VP-001 uses the accepted stable phase reference associated with the declared nominal physical geometry.

Candidate rule:

> Active sensor masking shall not silently move the phase reference.

Common phase may be removed only in metrics where ADR-001/003 justify it as a nuisance gauge.

---

## 7. Propagation Model

VP-001 uses:

```text
far-field
narrowband
single carrier/reference frequency per condition
stationary geometry within trial
```

The narrowband steering model is inherited from ADR-002.

Candidate rule:

> VP-001 does not claim validity for near-field curvature or wideband aperture-delay effects; those conditions are OUTSIDE_PROFILE unless a later specialized profile is accepted.

---

## 8. Source Model

VP-001 source count `K` is condition-defined.

Primary initial cases:

```text
K = 1  for deterministic localization / manifold / subspace checks
K = 2  for association, detection, RMSE, and resolution studies
```

Source DOAs are exact synthetic point truth under ADR-001 coordinates.

Candidate rule:

> Multi-source truth is an unordered set unless persistent physical source identity is separately declared.

---

## 9. Source Statistics

Initial stochastic source profile:

```text
proper-complex
zero-mean
stationary within trial
independent sources by default
incoherent unless a study explicitly declares another accepted subprofile
```

Candidate rule:

> Source coherence/correlation is not silently introduced into the baseline VP-001 claim. A coherent-source study requires explicit condition/profile extension and compatibility review.

---

## 10. Noise Model

Initial noise profile:

```text
proper-complex
zero-mean
additive
spatially white
identical variance across channels
independent of sources
stationary within trial
```

Thus

\[
R_n=\sigma_n^2 I.
\]

Candidate rule:

> Colored/unequal noise is outside the baseline VP-001 profile unless an explicit compatible extension with whitening/metric semantics is declared.

---

## 11. Sensor / Receiver Profile

VP-001 inherits ADR-003 Phase-1 ideal behavior:

```text
nominal geometry = physical geometry
ideal identical scalar unit elements
no mutual coupling
unity differential gain/phase
zero differential channel delay
coherent common reference
no SRO/CFO/differential jitter
linear receiver
no DC/IQ/nonlinearity/clipping
unquantized floating acquisition
identity deterministic calibration
```

Therefore

\[
H_{sensor}^{Phase1}\equiv I.
\]

Candidate rule:

> VP-001 is a scientific baseline, not a claim that real hardware behaves ideally.

---

## 12. Snapshot Model

For each Monte Carlo trial, generate `L` simultaneous-equivalent coherent snapshots under ADR-002 semantics.

Candidate rule:

> `L` is snapshot count inside a trial; it is not the Monte Carlo trial count.

The trial/condition hierarchy remains:

```text
study
  -> condition
       -> Monte Carlo trial
            -> L snapshots
```

---

## 13. Sample Covariance

The baseline VP-001 estimator input uses the declared covariance object required by the algorithm profile.

For ordinary zero-mean synthetic source/noise models, the default candidate estimator is the uncentered sample second moment

\[
\hat R
=
\frac{1}{L}XX^H,
\]

with dimensions and snapshot orientation explicitly declared.

Candidate rule:

> Centered covariance is a different object and shall not be substituted silently. Any implementation shall declare whether the mean is known zero, assumed zero, or estimated/removed.

---

## 14. Baseline Algorithms

Candidate baseline algorithm set:

```text
Bartlett
MVDR/Capon
MUSIC
```

with MUSIC as the primary subspace-validation algorithm.

Optional later algorithms may include:

```text
ESPRIT where geometry compatibility holds
OMP/LASSO/sparse methods
subspace tracking
```

Candidate rule:

> VP-001 defines the data/evidence profile; it does not require every algorithm to support every geometry.

Compatibility status remains method-specific.

---

## 15. Oracle Source Count Policy

For the first scientific software reference, MUSIC may use known `K` as an explicit oracle-assisted mode.

Candidate label:

```text
MUSIC_ORACLE_K
```

Candidate rule:

> Oracle `K` shall be part of method/profile provenance and shall not be compared as a blind model-order estimator without harmonizing the information contract.

A later model-order-estimation profile may be added separately.

---

## 16. Search Grid

Search grid shall be explicit in angle `theta` for the initial profile.

Candidate provenance includes:

```text
search-sector bounds
grid spacing
endpoint inclusion
ordering
interpolation/refinement method, if any
```

Candidate rule:

> Grid spacing is an implementation/evaluation condition and shall not be interpreted as physical array resolution.

---

## 17. Peak Extraction

If a spectrum-based estimator requires peak extraction, the profile shall declare:

```text
peak-count policy
threshold/prominence policy
minimum peak spacing
boundary handling
interpolation/refinement
ordering/tie rule
```

Candidate rule:

> For core-estimator comparisons, peak extraction should be harmonized where scientifically appropriate; otherwise the comparison is explicitly a complete-pipeline comparison.

---

## 18. Truth-to-Estimate Association

VP-001 uses Exploration 4.6 semantics:

```text
unordered truth set
unordered valid estimate set
one-to-one minimum-cost assignment
explicit angular cost in theta for baseline profile
explicit association gate per benchmark
unmatched truth retained as miss candidate
unmatched estimate retained as spurious candidate
```

Candidate rule:

> No universal association gate is fixed by VP-001; each benchmark study must predeclare the gate and preserve it in provenance.

---

## 19. Single-Source Localization Study

Candidate single-source benchmark goals:

```text
steering/manifold correctness
covariance/eigenspace sanity
spectrum peak correctness
signed DOA error
bias/MSE/RMSE
angle dependence across visible sector
```

Candidate condition axes:

```text
theta0
SNR
L
geometry
algorithm
```

Candidate rule:

> Single-source studies should span broadside and off-broadside conditions so direction-cosine sensitivity is visible.

---

## 20. Two-Source Localization / Resolution Study

Candidate truth pair parameterization:

\[
\theta_1=\theta_c-\frac{\Delta\theta}{2},
\qquad
\theta_2=\theta_c+\frac{\Delta\theta}{2}.
\]

Condition axes include:

```text
pair midpoint theta_c
separation Delta theta
SNR
L
geometry
source power ratio
source correlation profile
algorithm
```

Candidate rule:

> Separation alone is insufficient; midpoint/absolute locations shall remain part of the condition identity.

---

## 21. Baseline Source-Power Profile

Initial two-source Phase-1 baseline:

```text
equal average source powers
```

Candidate rule:

> Unequal-power studies are valid extensions but require explicit power-ratio condition/provenance and shall not be pooled silently with equal-power results.

---

## 22. Resolution Event

Baseline truth-based pair resolution event:

```text
both truth sources have distinct admissible one-to-one matches
no truth member in the designated pair is missed
trial is scientifically eligible under VP-001
```

Extra spurious estimates are not automatically prohibited by the baseline `pair-resolved` event.

Candidate rule:

> If a clean-resolution event additionally requires no spurious detections, it is a different metric/event and shall be labeled separately.

---

## 23. Probability of Resolution

For each fixed condition:

\[
\widehat P_{res}
=
\frac{N_{resolved}}{N_{eligible}}.
\]

Candidate rule:

> Numerator, denominator, failure mapping, and event definition remain publication provenance.

VP-001 does not fix one universal trial count or one universal resolution probability threshold.

---

## 24. Localization Metrics

Candidate baseline localization metrics:

```text
signed matched error
bias
empirical variance diagnostic
MSE
RMSE
absolute error / quantiles as supporting diagnostics
matched coverage
```

GRP-018 remains the deterministic hand-check reference for bias/variance/MSE/RMSE semantics.

Candidate rule:

> Matched-only RMSE shall always be accompanied by coverage/miss/failure evidence.

---

## 25. Detection / Failure Metrics

Candidate baseline event metrics:

```text
P_D / miss probability under declared binary universe
spurious-detection count/probability as declared
P_res
estimator numerical failure rate
incompatibility count/status
unresolved/ambiguous count
```

Candidate rule:

> Formal false-alarm probability is reserved for an explicit null/absence protocol, not every unmatched estimate in ordinary multi-source localization.

---

## 26. Multi-Level Diagnostic Metrics

For MUSIC and implementation cross-validation, VP-001 should preserve as applicable:

```text
manifold correlation/projective error
covariance relative Frobenius error
Hermitian/PSD diagnostics
eigenvalue error
relevant eigengap
projector error
principal angles
MUSIC truth-direction leakage
spectrum error on common grid
peak/event mismatch
final DOA error
```

Candidate rule:

> Final DOA RMSE is not sufficient for mechanism diagnosis.

---

## 27. Deterministic Verification Layer

Before Monte Carlo claims, the implementation shall pass the applicable deterministic reference program.

For ADR-004 this includes at minimum:

```text
GRP-018 — Bias / Variance / MSE / RMSE by hand
```

and the upstream accepted GRPs needed to establish:

```text
steering sign / phase
covariance semantics
sample-rank behavior
MUSIC orthogonality
sensor Phase-1 identity assumptions
```

Candidate rule:

> Monte Carlo agreement does not replace deterministic semantic verification.

Formal GRP PASS remains a Gate-E activity.

---

## 28. Monte Carlo Trial Contract

Each stochastic condition shall declare:

```text
random variables and distributions
redraw scope
trial count policy
root seed / child-stream policy
condition identity
trial identities
source/noise family identities
algorithm-internal randomness, if any
```

Candidate rule:

> Trial identity is semantic and independent of worker count/execution order.

---

## 29. Common Random Numbers

For fair algorithm or geometry comparisons, VP-001 candidate default is:

```text
share exogenous source/noise realizations across compared methods
```

and, where geometry comparison scientifically permits, preserve matched generative source processes/noise draws under clearly defined channel-dimension semantics.

Candidate rule:

> CRN pairing shall be semantic, not inferred merely from identical root-seed literals.

---

## 30. Geometry-Comparison Resource Contract

Every geometry comparison shall state what is held fixed.

Candidate resource axes:

```text
physical sensor count
physical aperture
minimum spacing
RF-channel count
virtual/coarray DOF
```

Candidate rule:

> No geometry may be called universally superior without specifying the constrained resource set.

Condition-resolved trade-offs are preferred.

---

## 31. Monte Carlo Adequacy

VP-001 requires condition-level adequacy evidence.

Candidate requirements:

```text
requested/eligible/completed counts
running or block diagnostics for key metrics
rare-event/failure counts
precision target or fixed-budget rationale
final adequacy/stopping status
```

Candidate rule:

> No universal `N=1000` sufficiency rule exists.

---

## 32. Uncertainty

Candidate baseline:

```text
probability metrics -> bounded binomial-compatible interval; Wilson remains candidate default for IID Bernoulli conditions
bias/means -> compatible mean uncertainty method
MSE/RMSE -> declared method compatible with squared-error distribution
paired comparisons -> paired uncertainty on effect
```

Candidate rule:

> Confidence level/method/conditioning/counts are part of the result identity.

---

## 33. Failure Mapping

For a complete-pipeline system-level probability metric, a numerical estimator failure on an otherwise compatible valid trial may count as event non-success while preserving the original typed failure state.

For matched-only localization RMSE, that failure has no ordinary angular-error value and is excluded from that conditional metric while failure coverage is reported.

Candidate rule:

> Metric mapping does not erase typed failure evidence.

---

## 34. Initial Fair-Comparison Profile

Candidate fair-comparison baseline:

```text
same truth conditions
same source/noise semantics
same SNR definition
same L
same exogenous trial realizations via CRN
same association and metric contracts
same failure policy
same oracle-information policy where pure algorithm comparison is claimed
same search/postprocessing where scientifically appropriate
locked hyperparameters before final benchmark
paired effect/uncertainty analysis
```

Candidate rule:

> Any deliberate asymmetry converts the claim to a complete-pipeline or different-information comparison and must be labeled accordingly.

---

## 35. Provenance Minimum

Every VP-001 run shall retain:

```text
VP-001 version
ADR/profile versions
resolved canonical configuration + hash
Git commit SHA
software environment summary
geometry/source/noise/SNR/snapshot config
algorithm/postprocessor config
root seed + RNG derivation policy
condition/trial identities
association/metric/failure/uncertainty policy versions
requested/completed/failed/excluded trial IDs/counts
result artifact identities
```

Candidate rule:

> Publication/final benchmark evidence should prefer clean committed source state.

---

## 36. Publication Package Minimum

A final VP-001 result intended for publication/portfolio evidence should include:

```text
manifest
resolved configs
run provenance
trial-level or recomputable evidence
aggregate metrics + uncertainty
failure/exclusion summary
figure/table scripts and source IDs
reproduction instructions
artifact hashes
known limitations
```

Candidate rule:

> A plot alone is not a publication-grade VP-001 result.

---

## 37. Float Reference Path

The first accepted implementation target is a float64 software reference.

Candidate path:

```text
scientific contracts / GRPs
→ float64 reference
→ Monte Carlo VP-001 benchmark
→ frozen canonical stimuli/results
```

Candidate rule:

> Float64 reference status requires verification; being Python/NumPy does not automatically make it correct.

---

## 38. Fixed-Point / FPGA Extension

After float reference acceptance, VP-001 provides canonical digital stimuli and expected internal/result evidence for:

```text
float32 sensitivity
fixed-point model
bit-accurate model
HLS/RTL
FPGA board replay
```

Candidate cross-validation axes:

```text
covariance error
eigenspace/projector error
spectrum error
event/DOA agreement
saturation/overflow
latency / II / throughput
resources / timing closure
```

Candidate rule:

> Synthetic VP-001 board replay establishes implementation/integration evidence, not real-array physical validation.

---

## 39. Candidate Minimal Deterministic Smoke Conditions

Before broad Monte Carlo sweeps, VP-001 should include simple deterministic smoke cases such as:

```text
single source at broadside
single source off broadside
noise-free rank-one covariance sanity case
simple two-source well-separated case
known sample-covariance rank-limited case
```

Candidate rule:

> These are implementation smoke/reference conditions and do not add new canonical GRP numbers unless the roadmap is explicitly amended.

---

## 40. Candidate Initial Monte Carlo Sweep Families

The first executable benchmark family may be organized as:

### VP-001-A — Single-source accuracy

```text
theta sweep × SNR × L × geometry × algorithm
```

### VP-001-B — Two-source resolution

```text
midpoint × separation × SNR × L × geometry × algorithm
```

### VP-001-C — Algorithm comparison

```text
shared fixed conditions + CRN + harmonized evaluation
```

### VP-001-D — Geometry comparison

```text
resource-constrained geometry set + shared condition profile
```

### VP-001-E — Implementation cross-validation

```text
float64 → float32/fixed/HLS/FPGA on canonical stimuli
```

Candidate rule:

> These subprofiles are organizational candidates, not accepted public API names.

---

## 41. Explicitly Outside Baseline VP-001

The following are outside the initial baseline unless a later extension is declared:

```text
near-field propagation
wideband steering / beam squint
FMCW range-Doppler coupling studies
mutual coupling
position/gain/phase/timing imperfections
colored/unequal noise
IQ imbalance / nonlinearity / clipping
ADC quantization
measured/CST manifold substitution
coherent-source remedies
unknown-K/model-order benchmarking
TDM-MIMO temporal phase
physical hardware acquisition
real calibration
```

Candidate rule:

> `OUTSIDE VP-001` does not mean unimportant; it means intentionally deferred so the baseline reference can be verified cleanly first.

---

## 42. Extension Policy

A future VP-001 extension must identify which baseline assumptions change.

Examples:

```text
VP-001 + position error
VP-001 + colored noise + whitening
VP-001 + measured manifold
VP-001 + fixed-point implementation
```

Candidate rule:

> Extensions shall not retain the same profile identity if a scientific assumption affecting comparability changes materially.

---

## 43. Acceptance Threshold Policy

VP-001 defines metrics and evidence requirements but does not freeze universal pass/fail performance thresholds such as:

```text
RMSE < 1 deg
P_res > 0.9
relative covariance error < 1e-3
```

Candidate rule:

> Thresholds belong to specific verification tests, benchmark claims, or engineering requirements and shall be justified separately.

---

## 44. Candidate Phase-1 Evidence Ladder

A scientifically disciplined progression is:

```text
L0 — formula / convention verification
L1 — deterministic reference problems
L2 — float64 software implementation verification
L3 — VP-001 Monte Carlo stochastic characterization
L4 — fair algorithm / geometry comparison
L5 — float/fixed/HLS/FPGA cross-validation
L6 — later extended sensor/calibration profiles
L7 — later physical array/system validation
```

Candidate rule:

> Higher levels do not erase the evidence requirements of lower levels.

---

## 45. Why VP-001 Is a Useful First Profile

VP-001 intentionally isolates:

```text
array geometry
finite snapshots
source/noise randomness
subspace conditioning
search/association/postprocessing
algorithm behavior
implementation precision
```

while excluding sensor/calibration complexity.

This allows GeoDOA to establish whether the fundamental scientific/software chain is correct before attributing discrepancies to hardware or real-sensor effects.

---

## 46. Candidate Readiness Criteria for Implementing VP-001

Before authoritative scientific implementation begins, the governing ADR-004 must eventually be accepted and the relevant Phase-0C gates must pass.

Candidate implementation-readiness checklist:

```text
ADR-001/002/003 accepted
ADR-004 accepted
VP-001 final profile frozen
GRP semantics passed Gate E
configuration/provenance schema implemented
trial/RNG semantics implemented
failure/status schema implemented
metrics/association semantics implemented
reference float tests available
```

Candidate rule:

> This exploration defines the target profile but does not authorize premature authoritative implementation before ADR-004 acceptance.

---

## 47. Invalid / Weak VP-001 Usage

The following would violate the intended baseline semantics:

1. use a measured/CST manifold but still label the run plain VP-001;
2. change to colored noise without declaring an extension;
3. move the phase reference when active sensors change;
4. center sample covariance silently despite zero-mean second-moment baseline;
5. use different SNR semantics across algorithms;
6. treat search-grid spacing as resolution;
7. compare known-K MUSIC to blind model-order method without labeling information asymmetry;
8. remove failed trials from `P_res` denominator without explicit policy;
9. report matched RMSE without coverage;
10. call FPGA synthetic replay physical validation;
11. call a geometry superior without resource constraints;
12. use one root seed without child-stream provenance;
13. change algorithm tuning after inspecting final benchmark and keep the same evidence identity;
14. introduce sensor imperfections but attribute all degradation to geometry/algorithm;
15. begin authoritative implementation and freeze software semantics before ADR-004 acceptance.

---

## 48. Cross-ADR Reconciliation

### ADR-001

VP-001 inherits exact 1-D geometry, direction, steering sign, phase-reference, physical-position, and stable-channel semantics.

### ADR-002

VP-001 inherits PM-001 far-field narrowband propagation, snapshots, source/noise statistics, covariance-object distinctions, SNR typing, and subspace/rank semantics.

### ADR-003

VP-001 uses the accepted ideal Phase-1 sensor profile with `H_sensor = I` and explicitly excludes later sensor/calibration complexity.

### ADR-004 4.1–4.18

VP-001 composes the candidate verification/validation, truth, deterministic evidence, stochastic trial, RNG, association, metrics, detection/resolution, adequacy, uncertainty, comparison, failure, multi-level diagnostics, FPGA, provenance, publication, and cross-ADR compatibility contracts.

**Cross-ADR result: no contradiction identified.**

---

## 49. Candidate Decisions from Exploration 4.19

- **D4.19-01:** VP-001 is the candidate initial executable GeoDOA validation profile: ideal 1-D far-field narrowband receive-array DOA under accepted Phase-1 sensor semantics.
- **D4.19-02:** VP-001 inherits ADR-001, ADR-002 PM-001, ADR-003 Phase-1 sensor, and ADR-004 evidence semantics without redefining them.
- **D4.19-03:** Initial primary source cases are `K=1` localization and `K=2` localization/resolution with exact synthetic point truth.
- **D4.19-04:** Baseline source/noise profile is proper-complex, zero-mean, stationary, independent-source, white equal-variance additive noise unless an extension is declared.
- **D4.19-05:** Baseline sensor profile is ideal with `H_sensor = I`; real sensor imperfections/calibration are outside plain VP-001.
- **D4.19-06:** Baseline sample input uses a declared zero-mean uncentered sample second moment; centered covariance is a distinct profile/object.
- **D4.19-07:** Bartlett, MVDR, and MUSIC are candidate baseline algorithms; MUSIC is the primary subspace reference, with oracle-K mode explicitly labeled.
- **D4.19-08:** Search-grid and peak-extraction semantics are configuration/provenance and do not define physical resolution.
- **D4.19-09:** Association follows one-to-one truth-to-estimate matching with a study-declared gate; unmatched truth/estimates remain typed evidence.
- **D4.19-10:** Two-source resolution depends on midpoint, separation, SNR, snapshots, geometry, source power/correlation, and algorithm—not separation alone.
- **D4.19-11:** Baseline pair resolution requires distinct admissible matches for both truth members; clean-resolution/no-spurious is a separate event if desired.
- **D4.19-12:** Matched RMSE, detection, spurious outcomes, P_res, and failure rate remain separate complementary metrics.
- **D4.19-13:** VP-001 requires deterministic verification before Monte Carlo performance claims and preserves GRP-018 plus applicable upstream GRP evidence.
- **D4.19-14:** CRN is the candidate default for fair stochastic algorithm comparisons under shared exogenous realizations.
- **D4.19-15:** Geometry comparisons require explicit resource constraints and condition-resolved reporting.
- **D4.19-16:** Trial adequacy and uncertainty are condition/metric specific; VP-001 fixes no universal Monte Carlo count.
- **D4.19-17:** Every VP-001 run retains canonical configuration, Git/software/RNG/trial/policy/artifact provenance sufficient for audit and reproduction.
- **D4.19-18:** Float64 is the first downstream software reference target only after scientific verification; fixed/HLS/FPGA layers validate against it through multi-level diagnostics.
- **D4.19-19:** Synthetic FPGA replay under VP-001 is implementation/integration evidence, not physical sensor validation.
- **D4.19-20:** Near-field, wideband, sensor imperfections, colored noise, measured manifolds, unknown-K, ADC effects, and physical acquisition are explicitly outside the plain baseline profile.
- **D4.19-21:** Extensions that materially change scientific assumptions require explicit new profile/subprofile identity.
- **D4.19-22:** VP-001 defines evidence and metric semantics but no universal algorithm-performance acceptance thresholds.
- **D4.19-23:** This exploration defines the target implementation profile but does not authorize authoritative implementation before ADR-004 acceptance.

---

## 50. Exploration 4.19 Conclusion

Exploration 4.19 is complete at candidate-contract level.

The central rule is:

> GeoDOA's first validation profile shall be a deliberately constrained, fully reproducible ideal 1-D far-field narrowband DOA benchmark that composes the accepted geometry, signal/covariance, and Phase-1 sensor conventions with ADR-004's deterministic verification, Monte Carlo, association, metric, failure, uncertainty, comparison, FPGA, provenance, and publication contracts. This profile establishes the scientific/software reference baseline first; sensor realism and physical hardware validation are layered later rather than mixed into the initial reference.

No acceptance gate is started or passed by this exploration.

The next exploration is:

```text
4.20 — Cross-Section Reconciliation
```
