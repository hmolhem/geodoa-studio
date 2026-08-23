# ADR-004 Gate A — Physical Consistency Audit

- **ADR:** ADR-004 — Validation, Reproducibility, and Scientific Evidence
- **Phase:** 0C — Scientific Foundations
- **Gate:** A — Physical Consistency
- **Gate result:** **PASS**
- **Governing draft:** `ADR-004-validation-reproducibility-scientific-evidence.md`
- **Reviewed governing content SHA:** `8cca2e3ac514cd031bee1d8c9e4c0347694ecb53`
- **Pre-Gate review:** `ADR-004_PRE_GATE_CONSISTENCY_REVIEW.md` — PASS
- **Depends on accepted:** ADR-001, ADR-002, ADR-003
- **Gates B–F:** Not evaluated by this audit
- **ADR-004 acceptance:** NOT ACCEPTED

> Gate A asks whether ADR-004's evidence semantics correctly represent the intended physical/scientific system and distinguish model assumptions from physical truth. A Gate A PASS does not establish mathematical, unit, software-semantic, Golden Reference, or boundary/failure acceptance.

---

## 1. Gate A Criterion

The Phase 0C roadmap defines Gate A as:

> Definitions and equations must match the intended physical system and distinguish model assumptions from physical truth.

For ADR-004, this requires more than checking one propagation equation. ADR-004 governs how GeoDOA interprets evidence about physical models. Therefore Gate A must verify that evidence labels cannot silently promote a synthetic assumption, calibration result, external-model output, numerical match, or FPGA execution into a stronger claim about physical reality.

---

## 2. Audit Scope

Gate A evaluates the following physical-consistency questions:

```text
A1   Does ADR-004 preserve ADR-001/002/003 physical authority?
A2   Does it distinguish truth/reference/model prediction/measurement?
A3   Does verification remain distinct from physical validation?
A4   Does calibration remain distinct from validation?
A5   Does VP-001 state ideal/far-field/narrowband assumptions as model assumptions?
A6   Does synthetic Monte Carlo evidence remain synthetic evidence?
A7   Does CST/external-tool agreement avoid automatic promotion to physical truth?
A8   Does FPGA replay avoid automatic promotion to physical sensor validation?
A9   Does real physical validation require traceable physical reference/domain evidence?
A10  Do sensor/channel/geometry identities remain physically meaningful through evaluation?
A11  Are out-of-profile physical regimes explicitly bounded rather than silently approximated?
A12  Are geometry/algorithm comparison claims conditioned on physical/resource context?
```

---

## 3. Upstream Physical Authority

ADR-004 explicitly remains downstream of:

```text
ADR-001 -> geometry / direction / receive phase / phase reference / channel identity
ADR-002 -> propagation / snapshots / source-noise / covariance / SNR / MIMO physical channels
ADR-003 -> sensor/receiver effects / calibration / reference planes / compatibility / identifiability
```

ADR-004 does not create a second steering-sign convention, second propagation model, second sensor-operator ordering, or alternate calibration semantics.

### Gate-A finding

**PASS.** Physical meaning remains owned by the accepted upstream scientific ADRs. ADR-004 governs evidence about those models rather than redefining them.

---

## 4. Physical Truth versus Scientific Reference

The governing draft distinguishes:

```text
exact simulation truth
reference value/artifact
physical measurement
calibration estimate
external-tool/model prediction
algorithm estimate
unresolved reference state
```

This prevents the physically invalid shortcut:

```text
available numeric target == physical truth
```

A CST result, measured manifold, calibration estimate, published value, or high-resolution numerical output requires a declared epistemic/reference role and uncertainty/domain provenance.

### Gate-A finding

**PASS.** Synthetic truth can be exact by construction within the declared simulation, while physical references remain measurement/model objects with appropriate epistemic limits.

---

## 5. Verification versus Physical Validation

ADR-004 defines verification as correctness relative to a declared model/specification/reference and physical validation as comparison to physical reality or a traceable physical reference within a declared domain and uncertainty model.

The following implication is explicitly rejected:

```text
software A == software B
    therefore
physical model validated
```

Likewise:

```text
FPGA == Python
    therefore
physical array validated
```

is rejected.

### Gate-A finding

**PASS.** Computational agreement cannot silently acquire physical-validation meaning.

---

## 6. Calibration versus Physical Validation

ADR-003 established calibration as a separate inference/correction process. ADR-004 preserves:

```text
calibration fit/residual != independent physical validation
```

A calibration artifact has a validity domain, reference plane, source evidence, uncertainty, and lineage. A reference channel fixes a gauge where applicable but is not thereby proven ideal.

Held-out/external evidence is required when an independent physical-validation claim is made.

### Gate-A finding

**PASS.** Calibration does not become circular validation.

---

## 7. VP-001 Physical Model Boundary

VP-001 is explicitly a bounded scientific baseline using:

```text
1-D receive-array geometry
far-field approximation
narrowband approximation
proper-complex zero-mean source/noise baseline
spatially white equal-variance additive noise
ADR-003 ideal Phase-1 sensor
H_sensor^Phase1 = I
unquantized floating acquisition
identity deterministic calibration
```

These are declared modeling assumptions, not claims that real arrays, receivers, or environments satisfy them universally.

The profile explicitly excludes from plain VP-001:

```text
near field
wideband / beam squint
mutual coupling
position/gain/phase/timing mismatch
colored/unequal noise
IQ imbalance / nonlinearity / clipping
ADC quantization
measured/CST manifold substitution
unknown-K benchmarking
TDM-MIMO temporal effects
physical acquisition/calibration validation
```

### Gate-A finding

**PASS.** The baseline is physically bounded and does not conceal idealizations.

---

## 8. Far-Field and Narrowband Physical Assumptions

ADR-004 inherits the far-field/narrowband physical meanings from ADR-002 rather than treating them as generic software flags.

Plain VP-001 requires both accepted PM-001 assumptions. Near-field curvature and wideband aperture-delay effects are outside the profile rather than silently approximated and then scored as if no model mismatch existed.

### Gate-A finding

**PASS.** Physical approximation boundaries remain explicit and independent.

---

## 9. Snapshot and Trial Physical Meaning

ADR-002 defines a snapshot as a simultaneous-equivalent coherent observation at a common receiver epoch/state or calibrated equivalent.

ADR-004 separately defines a Monte Carlo trial as a realization of the stochastic experiment:

```text
condition
  -> trial
       -> L snapshots
```

A larger number of Monte Carlo trials does not create more physical snapshots inside one trial, and a larger `L` does not create more independent benchmark trials.

### Gate-A finding

**PASS.** Physical acquisition semantics are not collapsed into simulation-loop semantics.

---

## 10. Source Count, Observable Rank, and Physical Interpretation

ADR-004 explicitly preserves the distinction among:

```text
physical/source count K
source-covariance rank
observed signal-subspace rank
estimator model order
estimated-output cardinality K_hat
```

Therefore coherent-source rank collapse, model-order mismatch, a missed estimate, or a rank-deficient sensor transform cannot automatically be interpreted as the physical disappearance of a source.

### Gate-A finding

**PASS.** Physical source multiplicity is not inferred from one numerical rank/cardinality quantity without the accepted model semantics.

---

## 11. Measurement and Reference Uncertainty

Physical validation uses traceable measurement/reference evidence within a declared uncertainty model. Increasing Monte Carlo trial count can reduce Monte Carlo sampling uncertainty but cannot remove a systematic physical-reference uncertainty.

The governing draft preserves reference uncertainty as distinct from estimator Monte Carlo uncertainty.

### Gate-A finding

**PASS.** Physical reference limitations cannot be averaged away by simulation repetition.

---

## 12. External Tool / CST Evidence

ADR-004 permits independent numerical/cross-tool evidence but explicitly treats it as verification/model-reference evidence unless a separate physical-validation contract exists.

The following is therefore invalid:

```text
CST agrees with GeoDOA
    therefore
real antenna/sensor behavior validated
```

A CST artifact remains a model prediction with solver/model/reference-plane/mesh/frequency/direction provenance. A measured artifact remains a measured reference with its own uncertainty and calibration state.

### Gate-A finding

**PASS.** External numerical agreement is not confused with measurement of nature.

---

## 13. Sensor-Manifold Physical Roles

The accepted ADR-003 manifold roles remain distinct:

```text
a_nom
a_phys
a_meas
a_em
a_cal
optional a_truth
```

ADR-004 metrics require the comparison endpoints/reference roles to be explicit. Therefore:

```text
a_phys vs a_nom
```

and

```text
a_fixed vs a_float
```

cannot both be reported as an untyped `manifold_error` with the same physical interpretation.

### Gate-A finding

**PASS.** Model mismatch, measurement mismatch, calibration residual, and implementation numerical mismatch remain physically distinct.

---

## 14. Gauge Alignment and Physical Meaning

ADR-004 allows gauge-aware comparisons only when the upstream model declares the corresponding degree of freedom non-identifiable or physically irrelevant for the claim.

Examples include common phase, common complex scale in a suitable manifold comparison, eigenvector phase, subspace basis rotation, and source permutation for unordered truth sets.

Gauge alignment does not authorize:

```text
moving the physical phase reference
removing channel-dependent phase distortion
renaming calibration error as a gauge
changing channel identity
```

### Gate-A finding

**PASS.** Evaluation invariance does not erase physically meaningful mismatch.

---

## 15. Detection / Resolution Physical Interpretation

ADR-004 defines detection and resolution as benchmark events relative to declared truth/reference and association semantics.

It explicitly prevents physical overinterpretation of:

```text
search-grid spacing
beamwidth
Rayleigh heuristic
number of spectrum peaks
truth separation alone
```

as equivalent to empirical resolution probability.

A source may be physically present while the estimator misses it; a numerical eigensolver failure is not physical source absence.

### Gate-A finding

**PASS.** Algorithmic/event outcomes remain distinct from physical source existence.

---

## 16. Geometry Comparison and Physical Resource Context

ADR-004 requires geometry comparisons to state physical/resource constraints such as:

```text
physical sensor count
physical aperture
minimum spacing
RF-channel count
virtual/coarray DOF
calibration/implementation burden
```

Thus a geometry cannot be labeled physically or scientifically superior merely because it changes aperture or hardware burden while the comparison describes the difference as topology only.

### Gate-A finding

**PASS.** Geometry claims remain conditioned on the physical resources that produce the observed performance.

---

## 17. FPGA / Hardware Physical Boundary

The evidence ladder is explicitly:

```text
scientific contract
-> verified floating-point reference
-> fixed-point / bit-accurate model
-> HLS/RTL
-> synthesis / place-route / timing
-> FPGA board replay
-> physical sensor/system validation
```

A board executing frozen synthetic samples exercises real digital hardware and interfaces, but the physical sensor/propagation/analog acquisition chain is still synthetic or bypassed.

HIL evidence must state which components are physical and which are simulated.

Physical end-to-end validation requires real acquisition plus appropriate calibration/reference/environment evidence.

### Gate-A finding

**PASS.** Digital hardware reality is not mistaken for physical sensing-system validation.

---

## 18. ADC Quantization versus FPGA Fixed Point

ADR-003 establishes ADC quantization as an acquisition/sensor-chain effect. ADR-004 F11 treats FPGA fixed-point arithmetic as a downstream implementation effect.

These can coexist but are not physically interchangeable:

```text
ADC quantization -> measurement formation
FPGA fixed point -> digital implementation representation
```

### Gate-A finding

**PASS.** Error attribution preserves the physical pipeline stage.

---

## 19. Hardware Timing versus Physical Delay

ADR-003 owns physical delay, sampling offset/skew, SRO/CFO/jitter semantics. ADR-004 F11 owns implementation timing quantities such as latency, II, throughput, and timing closure.

The governing evidence contract does not collapse algorithm/kernel latency into propagation or sampling delay.

### Gate-A finding

**PASS.** Physical-time and implementation-time meanings remain separated.

---

## 20. Physical Validation Claim Requirements

A future physical-validation claim under ADR-004 must identify, as applicable:

```text
physical system / array state
scene/reference truth role
reference instrument/procedure
calibration artifact + validity domain
frequency/range/direction/polarization/environment domain
raw acquisition identity
measurement/reference uncertainty
software/hardware implementation identity
failure/exclusion policy
```

Physical reproducibility may be limited by unavoidable environmental/instrument realities, but those limits must be documented rather than replaced by synthetic certainty.

### Gate-A finding

**PASS.** Physical validation has a defensible evidence boundary.

---

## 21. Gate-A Boundary Cases Reviewed

The following potential physical-consistency failures were explicitly checked and are prevented by the governing draft:

1. calling synthetic generative truth a universally physical truth;
2. calling measured/CST/calibration output automatically `truth`;
3. calling calibration fit independent validation;
4. calling Python-vs-FPGA agreement physical validation;
5. calling timing closure scientific correctness;
6. calling near-field/wideband conditions plain VP-001;
7. calling Monte Carlo trial count physical snapshot count;
8. calling subspace rank physical source count;
9. calling numerical failure physical non-detection without preserving cause;
10. calling grid spacing physical resolution;
11. calling geometry performance independent of aperture/resource changes;
12. treating ADC quantization and FPGA fixed-point arithmetic as the same physical effect;
13. moving a phase reference through metric gauge alignment;
14. treating a content hash as epistemic authority;
15. allowing simulation repetition to remove physical-reference uncertainty.

**Result:** no blocking physical contradiction identified.

---

## 22. Gate A Checklist

```text
Model assumptions separated from physical truth                 PASS
ADR-001 physical/spatial authority preserved                    PASS
ADR-002 propagation/snapshot/statistical authority preserved    PASS
ADR-003 sensor/calibration authority preserved                  PASS
Truth/reference/model/measurement roles physically coherent     PASS
Verification vs physical validation                             PASS
Calibration vs validation                                      PASS
VP-001 ideal/far-field/narrowband boundaries                    PASS
Snapshot vs trial semantics                                     PASS
Source count vs rank/model order                                PASS
Reference uncertainty interpretation                            PASS
CST/external-tool evidence role                                 PASS
Gauge handling preserves physical meaning                       PASS
Resolution/detection interpretation                             PASS
Geometry resource context                                       PASS
FPGA replay vs physical validation                              PASS
ADC quantization vs FPGA fixed point                            PASS
Physical delay vs implementation latency                        PASS
Future physical-validation evidence requirements                PASS
Blocking physical contradiction                                 NONE
```

---

## 23. Gate A Decision

### **Gate A — Physical Consistency: PASS**

The governing ADR-004 draft correctly distinguishes model assumptions from physical truth and preserves the accepted physical authority of ADR-001, ADR-002, and ADR-003.

It does not allow synthetic truth, external numerical agreement, calibration fit, software cross-checks, FPGA execution, or publication reproducibility to silently become stronger physical-validation evidence than their provenance supports.

VP-001 remains an explicitly idealized bounded baseline rather than a claim about real hardware or all array regimes.

No Gate-A correction to the governing ADR was required after the pre-Gate correction commit.

---

## 24. Status after Gate A

```text
Pre-Gate consistency review                PASS
Gate A — Physical Consistency              PASS
Gate B — Mathematical Consistency          NEXT
Gate C — Dimensional / Unit Consistency     NOT STARTED
Gate D — Software Semantic Consistency      NOT STARTED
Gate E — Hand Reference Evidence            NOT STARTED
Gate F — Boundary / Failure Analysis         NOT STARTED
ADR-004 acceptance                          NOT ACCEPTED
Authoritative Phase-1 implementation        NOT YET AUTHORIZED
```

The next work item is:

```text
ADR-004 Gate B — Mathematical Consistency Audit
```
