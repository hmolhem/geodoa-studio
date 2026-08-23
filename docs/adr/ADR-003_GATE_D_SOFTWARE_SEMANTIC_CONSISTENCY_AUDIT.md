# ADR-003 — Gate D Software Semantic Consistency Audit

- **ADR:** `ADR-003-sensor-imperfections-mutual-coupling-calibration.md`
- **Phase:** 0C — Scientific Foundations
- **Gate:** D — Software Semantic Consistency
- **Status:** PASS
- **Prior gates:** Gate A PASS, Gate B PASS, Gate C PASS
- **Acceptance status:** ADR-003 remains NOT ACCEPTED

> This audit verifies that ADR-003 scientific meaning maps cleanly into the GeoDOA domain/layered architecture without hidden sorting, implicit normalization, unlabeled axes, silent approximation, destructive provenance loss, or premature class inflation. It does not implement the domain model and does not constitute Gate E or Gate F evidence.

---

## 1. Audit question

Can ADR-003's distinctions among nominal/physical/measured/EM/calibrated response, geometry error, element response, coupling/loading, electronics, timing/sampling, staged noise, receiver/ADC effects, calibration, direct manifolds, covariance/eigenspace consequences, and estimator compatibility be represented in GeoDOA's planned object-oriented/domain-centric architecture without collapsing scientifically distinct concepts into generic fields or mutable convenience matrices?

---

## 2. Architectural baseline inspected

The audit is reconciled against:

- `GEODOA_STUDIO_MASTER_START_HANDOFF.md`;
- `PHASE0C_SCIENTIFIC_CONTRACTS_ROADMAP.md`;
- accepted ADR-001;
- accepted ADR-002 and its Gate-D audit;
- governing ADR-003 and Explorations 3.1–3.14;
- the current repository implementation state, where `src/geodoa/__init__.py` is intentionally empty and no scientific implementation has yet become authoritative.

This is important: Gate D evaluates **semantic implementability**, not whether classes already exist.

---

## 3. Core architectural compatibility — PASS

The Master Start Handoff already requires:

```text
object-oriented engineering where it improves domain modeling
immutable domain entities
typed value objects
replaceable behaviors/interfaces/protocols
processing-pipeline composition
dependency inversion
registries
pure numerical kernels where natural
no scientific logic inside GUI callbacks
```

ADR-003 maps cleanly to this direction.

The sensor model should therefore be represented as domain data + typed behaviors/reference-plane transformations, while small array algebra remains implementable as pure numerical kernels.

**Result: PASS.**

---

## 4. Response identity must not collapse into one `manifold` field — PASS

ADR-003 distinguishes:

```text
a_nom
a_phys
a_meas
a_em
a_cal
a_truth  (simulation only)
```

A future API shall not expose one mutable `manifold` property whose meaning changes according to hidden mode flags.

A clean mapping is possible through either typed response artifacts/value objects or explicit role/provenance metadata at public boundaries.

The numerical kernel may still accept a plain complex array once semantics have been validated at the boundary.

**Result: PASS.**

---

## 5. Nominal geometry must remain immutable provenance — PASS

The Master Handoff's immutable `LinearArrayGeometry` direction is compatible with ADR-003 provided:

1. nominal physical coordinates are preserved as the declared design/reference geometry;
2. realized physical coordinates are represented as a distinct sensor state or derived physical geometry view;
3. calibration estimates do not overwrite nominal coordinates destructively;
4. sorted/display views do not mutate physical channel identity.

A position-error model shall not silently modify the canonical nominal-geometry object in place.

**Result: PASS.**

---

## 6. Physical channel identity versus ordering — PASS

ADR-001/002 already require persistent physical channel identity.

ADR-003 extends this requirement because calibration, gain/phase error, dead-channel state, coupling matrices, timing errors, measured manifolds, and ADC metadata are channel-indexed.

Therefore:

```text
physical channel ID != row number after arbitrary sorting
```

Any sorted geometric view, reduced array, calibration artifact, or imported manifold must carry an explicit mapping back to stable physical channel identity.

**Result: PASS.**

---

## 7. Sensor-effect composition must be typed, not one `imperfection_matrix` — PASS

A future software design shall not create one generic matrix field that ambiguously represents geometry error, element response, mutual coupling, receiver gain, timing, and calibration correction.

A bounded linear specialization may numerically compose

\[
\mathbf G\mathbf C\mathbf P\mathbf a,
\]

but software semantics must preserve which factor represents which effect and at what reference plane.

This maps naturally to composition/interfaces without requiring every individual equation to become a stateful class.

**Result: PASS.**

---

## 8. Reference-plane semantics must be explicit at composition boundaries — PASS

ADR-003's conceptual RP-0 through RP-9 model maps cleanly to software metadata/protocols.

A future operator/artifact should expose enough information to validate:

```text
input reference plane
output reference plane
input/output quantity semantics
channel identity/order
frequency/state domain
included effects
de-embedding state
normalization/gauge
provenance
```

Matrix shape alone shall never authorize operator composition.

**Result: PASS.**

---

## 9. Master-Handoff `MAN-009 mutual-coupling matrix/model` requires semantic refinement — RESOLVED

The early Master Start Handoff used the planned label:

```text
MAN-009 Mutual-coupling matrix/model
```

ADR-003 now provides the more precise scientific contract.

The software interpretation shall be:

```text
physical network/loading model
or
explicit effective-manifold coupling specialization
```

rather than one universal `coupling_matrix` abstraction.

`Z`, `S`, `T_L`, effective `C`, embedded response, and aggregate direct manifold remain distinct types/roles.

The Master-Handoff requirement is therefore **refined, not contradicted**.

**Result: PASS / RESOLVED REFINEMENT.**

---

## 10. Master-Handoff generic timing field requires decomposition — RESOLVED

The Master Start Handoff contains broad planning labels such as:

```text
PHY-013 Clock/timing offset
IMP-010 Timing skew
IMP-011 Carrier-frequency/phase offset
```

ADR-003 requires the software model to distinguish at least:

```text
physical/electrical channel delay
fixed sampling-time offset
sample-rate offset (SRO)
sampling jitter
receiver/LO phase offset
receiver/LO frequency offset
post-acquisition digital latency
```

A future generic `clock_skew` scalar shall therefore not become authoritative.

The earlier requirement catalog remains useful as planning taxonomy but is semantically refined by ADR-003.

**Result: PASS / RESOLVED REFINEMENT.**

---

## 11. Master-Handoff `calibrated/nonideal steering vector` requires role separation — RESOLVED

The earlier BPM-002 label `Calibrated/nonideal steering vector` is too broad for the accepted ADR-003 taxonomy.

Software shall not conflate:

```text
physical response
measured response
EM/CST response
calibrated estimator response
nominal response
```

A plotting/view layer may offer a human-facing category such as `nonideal`, but public scientific artifacts must retain the underlying response role and provenance.

**Result: PASS / RESOLVED REFINEMENT.**

---

## 12. Element response and electronic gain must remain separate concepts — PASS

Even when both are numerically diagonal complex arrays, their software semantics differ:

- element response may depend on direction, frequency, polarization, orientation, and environment;
- electronic gain/phase belongs to receiver/channel state.

A generic `complex_gain[N]` shall not silently serve both roles.

A pure kernel may multiply diagonal responses after validation, but the domain model must preserve their origin.

**Result: PASS.**

---

## 13. Direct measured/CST manifold artifacts require schema-bearing metadata — PASS

A direct manifold importer shall not return only an anonymous complex matrix.

Public/imported artifacts must retain at least:

```text
semantic axes
physical channel/port identity
coordinate frame / direction convention
frequency grid
range or source-state axes when applicable
polarization basis when applicable
reference plane
normalization/gauge
included effects / de-embedding
interpolation domain
measurement/solver provenance
quality/uncertainty metadata where available
```

Once validated, a numerical estimator kernel may consume an interpolated complex steering vector without carrying all metadata internally.

**Result: PASS.**

---

## 14. No destructive normalization — PASS

ADR-003 requires raw measured/EM/calibrated amplitude and phase to remain recoverable.

Therefore software shall distinguish:

```text
raw response artifact
normalized derived view
phase-aligned comparison view
common-scale-aligned comparison view
unit-norm estimator/search view
```

A call such as `normalize=True` shall not overwrite the authoritative calibrated artifact in place.

**Result: PASS.**

---

## 15. Calibration is a separate object/process from the physical forward model — PASS

Software shall not mutate the physical model so that calibrated estimates become indistinguishable from realized physical truth.

The architecture can cleanly represent:

```text
physical sensor state
calibration observation/evidence
calibration model/artifact
calibrated processing model
optional data correction
residual/uncertainty
```

This preserves the ADR-003 causal separation while remaining compatible with immutable domain entities.

**Result: PASS.**

---

## 16. Model calibration and data correction must use different operations — PASS

Two software paths are required conceptually:

1. estimator receives a different steering/manifold model;
2. measured data are transformed before covariance/estimation.

They shall not be represented by one ambiguous `apply_calibration()` whose effect is undocumented.

The API may expose a higher-level calibration workflow, but its result must state whether it produced a model artifact, a data transform, or both.

**Result: PASS.**

---

## 17. Calibration domain and state must be queryable — PASS

A future calibration artifact shall support explicit compatibility validation against the requested run state.

At minimum, the software contract must be capable of expressing applicable domains for:

```text
frequency
direction/source position
range
polarization
time/age
temperature/environment
gain/AGC state
sample rate / LO state
active channels
physical port terminations
platform/radome configuration
hardware/firmware revision
```

Not every profile must populate every axis, but absence, irrelevance, bounded value, and unresolved state shall be distinguishable.

**Result: PASS.**

---

## 18. Interpolation and extrapolation must be explicit behaviors — PASS

A direct manifold lookup shall not silently nearest-neighbor or extrapolate outside its calibration domain.

The artifact/model must retain:

```text
interpolation method
coordinate used for interpolation
phase/gauge handling
extrapolation policy
quality/null handling
```

Out-of-domain behavior belongs to compatibility/failure policy, not hidden array indexing.

**Result: PASS.**

---

## 19. Pointwise gauge and grid-coherent gauge must not collapse — PASS

Software comparison utilities may align two vectors by arbitrary common phase at one state.

However, a direct-manifold interpolation artifact must preserve a coherent phase gauge across its grid.

Therefore a function intended for pairwise projective error shall not be reused destructively as a calibration-grid normalization routine.

**Result: PASS.**

---

## 20. Error metric APIs require explicit equivalence semantics — PASS

There shall be no authoritative generic:

```python
manifold_error(a, b)
```

whose alignment/normalization is implicit.

The caller or metric object must select/declare semantics such as:

```text
raw Euclidean
phase-aligned relative
common-complex-scale aligned
projective/coherence
weighted/whitened
```

and retain any required reference, weights, units, and null-vector policy.

**Result: PASS.**

---

## 21. Unit-bearing operators and Gate-C lambda rule map cleanly to software — PASS

Gate C establishes that operators may be unit-bearing across reference planes and that Tikhonov `lambda` is not universally dimensionless:

\[
[\lambda I]=[H^H H].
\]

Software shall therefore not define a universal untyped `regularization: float` whose physical scale is assumed invariant across all operator representations.

A future regularization configuration must either:

1. operate on an explicitly nondimensionalized/scaled inverse problem and store the scaling convention; or
2. carry enough operator/unit context to interpret `lambda` consistently.

This requirement is semantically implementable without changing the mathematical formula.

**Result: PASS.**

---

## 22. Noise variance must be stage/reference-plane aware — PASS

ADR-002 already prohibits ambiguous generic `sigma` semantics.

ADR-003 additionally requires noise sources to be attached conceptually to the stage at which they enter.

A future `NoiseModel` or equivalent need not be one large class hierarchy, but it must preserve:

```text
injection plane
covariance/variance meaning
units
channel correlation
state dependence
downstream transformation provenance
```

A single top-level `noise_variance` is sufficient only for a bounded profile whose semantics explicitly match it.

**Result: PASS.**

---

## 23. ADC data representation must distinguish volts from codes — PASS

Software shall distinguish at least conceptually:

```text
analog/pre-quantization sample
ADC code
ADC dequantized engineering-unit sample
normalized floating DSP sample
```

An integer code array and a voltage array may share shape but are not semantically interchangeable.

ADC `bits` must remain separate from FPGA/processor arithmetic word length.

**Result: PASS.**

---

## 24. I/Q widely-linear profiles require explicit statistical representation — PASS

A material conjugate term shall not be hidden inside an ordinary complex gain array.

Software compatibility must be capable of distinguishing:

```text
ordinary complex-linear profile
widely-linear profile
corrected-to-ordinary profile
```

and therefore whether ordinary covariance or augmented covariance/statistics are required.

**Result: PASS.**

---

## 25. Nonlinearity/clipping cannot masquerade as manifold mismatch — PASS

A future simulation/receiver pipeline shall not represent compression or clipping as an arbitrary static steering-vector perturbation.

The run record must be able to state when the linear-manifold contract is violated.

A clipped dataset shall retain overrange/clipping diagnostics rather than only a post-scaled floating array.

**Result: PASS.**

---

## 26. Digital mask and physical port state require different semantics — PASS

The Master Handoff contains `Sensor availability mask`, while ADR-003 distinguishes digital selection from physical port/termination state.

The software mapping shall therefore distinguish:

```text
post-acquisition channel selection/availability view
physical port enabled/disabled/open/short/termination state
```

A digital subset may reuse the same physical calibration state if scientifically valid; a physical port-state change may invalidate coupling/manifold calibration for all channels.

**Result: PASS.**

---

## 27. MIMO virtual-channel semantics remain lineage-bearing — PASS

A virtual MIMO channel shall not be stored merely as row `m` of a virtual array.

It must be possible to recover at least:

```text
Tx physical identity
Rx physical identity
acquisition epoch/order where relevant
calibration state
virtual-coordinate derivation rule
```

This extends ADR-002's `(Tx_i,Rx_j)` provenance and is compatible with the Master Handoff's pair-to-virtual-index requirement.

**Result: PASS.**

---

## 28. Compatibility must be structured, not one `compatible: bool` — PASS

ADR-003 defines compatibility across multiple axes:

```text
manifold/reference plane
coordinate convention
bandwidth
stationarity
snapshot coherence
linearity
ordinary vs augmented statistics
noise/covariance model
quantization regime
calibration domain/state
port state
rank/model order
interpolation domain
required preprocessing
```

Software shall preserve the limiting reason(s), required preprocessing, and unresolved states.

A top-level convenience boolean may be derived for a specific profile/policy but shall not destroy the detailed compatibility vector/result.

**Result: PASS.**

---

## 29. Profile identity must replace scattered feature flags — PASS

The Phase-1 ideal sensor model should be a versioned profile/configuration with explicit defaults, not a set of independent booleans such as:

```text
use_coupling=False
use_gain_error=False
use_clock_error=False
use_adc=False
...
```

Such booleans can create scientifically impossible combinations and hidden semantics.

A profile may be composed from typed sub-configurations, but its scientific identity/revision must be recordable for reproducibility.

**Result: PASS.**

---

## 30. Phase-1 scope maps cleanly without implementing deferred effects — PASS

The current package contains no authoritative scientific implementation, which is consistent with Phase 0C governance.

After ADR acceptance, the initial Phase-1 implementation may instantiate only:

```text
ideal geometry = physical geometry
ideal scalar elements
no coupling distortion
unity differential electronics
coherent common timing/reference
linear unquantized/no-overload receiver
white equal-variance proper-complex noise
ordinary covariance/classical MUSIC compatibility
```

The domain model may leave extension points for later sensor effects without implementing or exposing unvalidated behavior.

**Result: PASS.**

---

## 31. No premature class inflation — PASS

ADR-003 does not require a class for every equation.

Recommended semantic boundary:

- rich immutable/value-object semantics for configuration, artifacts, provenance, channel identity, calibration, reference planes, and compatibility results;
- pure functions/array kernels for matrix multiplication, covariance congruence, normalization views, projector metrics, interpolation kernels, and deterministic reference calculations where stateful identity is unnecessary.

This follows the Master Start Handoff's OOP-without-class-inflation requirement.

**Result: PASS.**

---

## 32. GUI/CLI/notebook independence — PASS

Sensor-model scientific logic must remain below presentation layers.

The same validated configuration/artifact/pipeline shall be executable from:

```text
unit tests
Python API
CLI
notebook
GUI
future hardware/service backend
```

A GUI toggle shall never become the sole source of a scientific convention or calibration state.

**Result: PASS.**

---

## 33. Serialization and provenance — PASS

Future serialized calibration/manifold/sensor-profile artifacts must preserve scientific meaning, not merely numerical arrays.

At minimum, stable serialization must be capable of preserving:

```text
artifact/profile type and revision
units
coordinate/direction convention
reference planes
physical channel identities
frequency/state domain
normalization/gauge
included/de-embedded effects
calibration provenance
software/Git provenance
compatibility warnings/state where applicable
```

Exact serialization technology is deferred.

**Result: PASS.**

---

## 34. Reproducibility boundary — PASS

ADR-003's semantics are compatible with the project requirement that runs retain configuration hash, software version/Git commit, calibration/input identity, numerical backend, and warnings/failure status.

ADR-004 will govern the formal run/evidence contract, but ADR-003 creates no semantic obstacle to that provenance chain.

**Result: PASS.**

---

## 35. Semantic failure states that must remain distinguishable

Gate D confirms that software must be able to distinguish at least:

```text
invalid/malformed configuration
unknown/unresolved semantic metadata
outside calibration domain
reference-plane incompatibility
unit incompatibility
channel-identity mismatch
model mismatch/degraded approximation
required preprocessing absent
physical port-state mismatch
unsupported ordinary-vs-augmented statistics
nonlinear/clipped regime
quantization-profile incompatibility
insufficient rank/model-order compatibility
valid but low-confidence/performance-limited state
```

These states shall not all collapse to a generic exception or a generic `False` without reason/provenance.

Formal failure taxonomy is exercised at Gate F.

---

## 36. Hidden operations explicitly prohibited

The software architecture shall not silently:

```text
sort sensors and lose physical channel mapping
replace nominal geometry with calibrated/physical geometry
normalize calibrated amplitudes destructively
rephase each direct-manifold grid node independently
infer angle units from magnitude
infer distance units from numeric scale
convert Hz to rad/s without explicit conversion
convert seconds to samples without sample-rate context
apply coupling twice
use S21 as an effective manifold coupling coefficient by shape alone
turn physical delay into sampling skew
turn SRO/CFO into static phase
convert a digital mask into a physical termination change
whiten data without transforming the steering model
apply inverse correction without recording changed noise statistics
apply calibration outside domain silently
treat ADC codes as volts
use ADC bit depth as FPGA fixed-point width
use one-bit samples in a high-resolution covariance profile silently
collapse I/Q conjugate leakage into ordinary gain
promote measured/CST response to truth
promote unresolved metadata to compatible
```

**Result: PASS.**

---

## 37. Blocking findings

```text
Hidden sorting required by ADR-003:              NONE
Implicit normalization required:                 NONE
Unlabeled-axis requirement:                      NONE
Silent approximation required:                   NONE
Destructive provenance requirement:              NONE
Generic-matrix collapse required:                NONE
Conflict with immutable-domain architecture:     NONE
Conflict with pure numerical kernels:            NONE
Conflict with GUI-independent scientific core:   NONE
Conflict with Phase-1 bounded implementation:    NONE
```

The early Master-Handoff labels for coupling, timing, and nonideal/calibrated steering require semantic refinement, but ADR-003 provides the required refinement before implementation. These are resolved design clarifications, not Gate-D failures.

---

## 38. Gate D decision

\[
\boxed{\text{Gate D — Software Semantic Consistency: PASS}}
\]

ADR-003 maps cleanly to GeoDOA's domain-centric architecture without requiring hidden sorting, implicit normalization, unlabeled axes, silent approximation, destructive provenance loss, or class inflation.

The current lack of scientific implementation is consistent with Phase 0C governance; Gate D establishes the semantic constraints that later implementation must obey.

ADR-003 remains **NOT ACCEPTED** because Gates E and F plus final cross-gate reconciliation have not passed.

The next formal work item is:

\[
\boxed{\text{Gate E — Hand-Calculated Reference Evidence}}
\]
