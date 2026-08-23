# ADR-004 — Final Cross-Gate Reconciliation

- **ADR:** ADR-004 — Validation, Reproducibility, and Scientific Evidence
- **Phase:** 0C — Scientific Foundations
- **Reconciliation result:** **PASS**
- **Governing draft:** `ADR-004-validation-reproducibility-scientific-evidence.md`
- **Pre-Gate review:** PASS
- **Gate A:** PASS
- **Gate B:** PASS
- **Gate C:** PASS
- **Gate D:** PASS
- **Gate E:** PASS
- **Gate F:** PASS
- **ADR-004 acceptance:** NOT YET RECORDED
- **Authoritative Phase-1 implementation:** NOT YET AUTHORIZED by this reconciliation alone

> This document verifies that the independently passed acceptance gates form one mutually consistent scientific evidence contract. It does not itself change ADR-004 status to Accepted; the final acceptance record and lifecycle-status synchronization remain separate finalization actions.

---

## 1. Reconciliation Question

The final reconciliation asks:

> After all Gate-A through Gate-F audits and their supporting evidence are considered together, does ADR-004 still define one coherent contract for physical interpretation, mathematics, units, software semantics, deterministic reference evidence, and boundary/failure behavior, without a later gate invalidating an earlier gate?

The answer is **YES**.

No blocking scientific, mathematical, dimensional, software-semantic, Golden-Reference, or boundary/failure contradiction remains.

---

## 2. Evidence Set Reconciled

The following records are jointly reconciled:

```text
ADR-004-validation-reproducibility-scientific-evidence.md
ADR-004_PRE_GATE_CONSISTENCY_REVIEW.md
ADR-004_GATE_A_AUDIT.md
ADR-004_GATE_B_AUDIT.md
ADR-004_GATE_C_AUDIT.md
ADR-004_GATE_D_AUDIT.md
ADR-004_GATE_E_AUDIT.md
ADR-004_GATE_F_AUDIT.md
ADR-004_BOUNDARY_FAILURE_ANALYSIS.md
../science/golden_reference/ADR-004_GOLDEN_REFERENCE_PROBLEMS.md
ADR-004_EXPLORATION_4.20_CROSS_SECTION_RECONCILIATION.md
ADR-004_EXPLORATION_CHECKPOINT.md
```

The accepted upstream scientific authorities remain ADR-001, ADR-002, and ADR-003.

---

## 3. Gate Results Reconciled

| Gate | Question | Result |
|---|---|---|
| Pre-Gate | Is the governing draft complete enough to enter acceptance gates? | PASS |
| A | Are evidence claims physically/scientifically interpreted correctly? | PASS |
| B | Are equations, probabilities, invariances, and rank/assignment semantics mathematically coherent? | PASS |
| C | Are physical/metric quantities dimensionally and unit consistent? | PASS |
| D | Can software preserve the scientific distinctions without silent semantic drift? | PASS |
| E | Are deterministic hand references independent, correct, and usable as future test oracles? | PASS |
| F | Are invalid, incompatible, failed, unresolved, and metric-ineligible states explicitly classified? | PASS |

No Gate result is reversed or weakened by a later Gate.

---

## 4. A ↔ B — Physical Interpretation versus Mathematics

Gate A established that simulation truth, physical measurement, calibration, external model output, implementation agreement, and physical validation are distinct evidence roles.

Gate B then verified the mathematical objects used to score such evidence without changing those roles.

Examples:

```text
physical source existence != estimator detection event
source count K != observed signal-subspace rank
external-tool numerical match != physical validation
FPGA/Python numerical match != physical validation
```

The mathematical definitions of bias, event probabilities, projective metrics, and subspace diagnostics therefore operate on explicitly typed references rather than redefining physical truth.

### Result

**CONSISTENT — PASS.**

---

## 5. B ↔ C — Mathematical Definitions versus Units

Gate B verified:

\[
\widehat{MSE}=v_N+\bar e^2
\]

and related metric definitions.

Gate C verified the corresponding unit propagation:

```text
error / bias / RMSE       -> base localization unit
variance / MSE            -> squared localization unit
probability               -> dimensionless
rho / d_proj^2            -> dimensionless
projective/principal angle -> radian
covariance/eigenvalue     -> snapshot-unit squared
```

Thus dimensional semantics do not alter or contradict the Gate-B mathematics.

### Result

**CONSISTENT — PASS.**

---

## 6. B ↔ E — Mathematical Definitions versus Golden Reference Evidence

Gate B established the finite-sample localization identities analytically.

Gate E independently instantiated those definitions in GRP-018:

```text
truth                 10 deg
estimates             9, 10, 12, 13 deg
errors                -1, 0, 2, 3 deg
bias                  1 deg
v_N                   2.5 deg^2
s^2                   10/3 deg^2
MSE                   3.5 deg^2
RMSE                  sqrt(3.5) deg
```

Two independent hand paths recover the same MSE:

```text
direct squared-error mean
bias + divisor-N centered second moment
```

Gate E therefore provides constructive evidence for Gate B rather than redefining it.

### Result

**CONSISTENT — PASS.**

---

## 7. C ↔ E — Unit Semantics versus GRP-018

Gate E preserves the Gate-C distinction:

\[
1^\circ=\frac{\pi}{180}\ \mathrm{rad}
\]

while squared-error quantities convert with the square of the angular scale.

Therefore:

```text
bias_deg -> bias_rad              linear conversion
RMSE_deg -> RMSE_rad              linear conversion
MSE_deg^2 -> MSE_rad^2            squared conversion
v_N_deg^2 -> v_N_rad^2            squared conversion
s^2_deg^2 -> s^2_rad^2            squared conversion
```

No unit inconsistency exists between the mathematical gate and the formal oracle.

### Result

**CONSISTENT — PASS.**

---

## 8. B ↔ F — Mathematical Domains versus Boundary Responses

Gate B carried forward mathematical domain conditions including:

```text
real-scalar e^2 localization metric domain
nonzero vectors for normalized manifold correlation
nonzero denominators for relative errors
N > 1 for divisor-(N-1) sample variance
valid association cost domain
declared unequal-subspace-dimension treatment
valid covariance for inverse/whitening operations
```

Gate F explicitly classifies these boundaries:

```text
F-004-050  N=1 sample variance undefined
F-004-051  complex quantity requires complex error metric
F-004-071  zero-vector rho undefined
F-004-072  zero-reference relative metric undefined
F-004-075  unequal subspace dimensions require declared policy
F-004-040  singular whitening/inverse requires other treatment
```

Gate F therefore closes Gate-B domain conditions without altering valid-domain mathematics.

### Result

**CONSISTENT — PASS.**

---

## 9. D ↔ F — Software Semantics versus Failure Behavior

Gate D prohibits silent scientific transformations such as:

```text
NaN survivor filtering
hidden centering
hidden normalization
hidden geometry sorting/snapping
implicit global RNG dependence
silent retry resampling
silent estimate truncation/padding
cache reuse with incomplete dependencies
```

Gate F provides typed outcomes when those boundaries are encountered.

Examples:

```text
N=0 metric universe                 -> undefined/not assessed, not numeric zero
association tie                     -> ambiguous/unresolved, not library-order truth
packing mismatch                    -> hardware protocol/data-integrity failure
cache dependency gap                -> nonauthoritative evidence
schema/hash ambiguity               -> identity not established
invalid/out-of-profile condition    -> excluded from ordinary event universe
```

The software obligations and boundary responses form one consistent operational contract.

### Result

**CONSISTENT — PASS.**

---

## 10. E ↔ F — Oracle Validity versus Edge Cases

GRP-018 and supplemental Gate-E references are deliberately inside well-defined domains.

Gate F does not modify their expected values; it defines what happens outside their domains.

Examples:

```text
GRP-018 uses N=4                 -> s^2 valid
N=1 outside this oracle         -> s^2 undefined under F-004-050
SRC-04 uses nonzero vectors     -> rho valid
zero-vector input               -> rho undefined under F-004-071
SRC-02 denominator is 5         -> P_res=0.4 valid
zero eligible denominator       -> P_res undefined under F-004-056
```

Thus Gate F protects oracle interpretation instead of creating alternate results.

### Result

**CONSISTENT — PASS.**

---

## 11. A ↔ F — Physical/Profile Boundaries

Gate A established VP-001 as an ideal bounded scientific profile rather than a universal physical model.

Gate F consistently classifies meaningful physics outside VP-001 as profile incompatibility rather than invalid physics:

```text
near field       -> require near-field profile
wideband         -> require wideband profile
mutual coupling  -> require nonideal-sensor profile
colored noise    -> require colored-noise/whitening profile
TDM-MIMO timing  -> require timing/simultaneous-equivalent profile
measured/CST manifold -> require measured/EM/calibrated-manifold profile
```

This preserves the central Phase-0C distinction:

```text
physically meaningful != compatible with selected simplified profile
```

### Result

**CONSISTENT — PASS.**

---

## 12. A ↔ D ↔ F — FPGA and Hardware Evidence

Across the three gates, the hardware evidence ladder remains:

```text
accepted scientific contract
-> verified float reference
-> fixed-point numerical model
-> bit-accurate model
-> HLS/RTL
-> synthesis/place-route/timing
-> FPGA board replay
-> physical sensor/system validation
```

Reconciled distinctions:

```text
numerical mismatch           != physical sensor mismatch
timing closure failure       != DOA-model scientific failure
hardware protocol mismatch   != ordinary estimator miss
synthetic board replay       != physical validation
ADC quantization             != FPGA fixed-point arithmetic
resource failure             != ordinary angular error
```

### Result

**CONSISTENT — PASS.**

---

## 13. B ↔ D ↔ F — `P_D` / `P_res` Denominator Semantics

The governing baseline end-to-end event semantics remain unchanged across all gates.

For compatible scientifically eligible trials:

```text
valid success                  -> event success where criteria satisfied
valid miss/unresolved          -> event non-success
numerical/algorithm failure    -> event non-success + typed failure preserved
```

By contrast:

```text
invalid input/reference        -> excluded from ordinary event universe
outside-profile/incompatible   -> excluded and reported separately
unresolved compatibility       -> no authoritative ordinary metric unless explicitly profiled
```

Gate D requires retained typed records; Gate F prevents silent denominator coercion; Gate E SRC-02/SRC-03 provides deterministic examples.

### Result

**CONSISTENT — PASS.**

---

## 14. F5/F6 ↔ E ↔ F — Association, Resolution, and Localization

The reconciled sequence remains:

```text
raw estimator output
-> execution state
-> association
-> detection/miss/spurious state
-> resolution event
-> localization metric on declared matched universe
```

Gate-E SRC-01 demonstrates:

```text
pair can be resolved
AND
an extra spurious estimate can exist
```

Gate F further prevents:

```text
truncating extra estimates
padding misses with fake angles
reusing one estimate for two truth sources
converting misses into arbitrary RMSE penalties
```

Thus association, event, and localization semantics remain distinct through all evidence layers.

### Result

**CONSISTENT — PASS.**

---

## 15. F7 ↔ F8 ↔ D ↔ F — Monte Carlo Adequacy and Fair Comparison

No gate introduces a universal Monte Carlo sample count or performance threshold.

The reconciled contract remains:

```text
adequacy depends on metric / condition / claim / dependence / tails / failures
VP-001 confirmatory studies initially prefer predeclared fixed N
Wilson is scoped to ordinary IID fixed-N Bernoulli evidence
CRN preserves paired exogenous randomness
fair comparison preserves oracle/tuning/resource/pre-postprocessing contracts
```

Gate F rejects misuse such as:

```text
universal N claim
outcome-driven stopping under fixed-N inference
Wilson on clustered dependent evidence
p>0.05 -> equivalence
unfair final-set tuning
mismatched runtime scopes
```

### Result

**CONSISTENT — PASS.**

---

## 16. F10 ↔ B/C/D/F — Multi-Level Diagnostics

The diagnostic ladder remains:

```text
manifold
-> covariance / second moment
-> eigenvalues / eigenspace
-> spectrum / objective
-> event / peak
-> final DOA
```

Reconciliation confirms:

- projective metrics remain dimensionless on their valid nonzero domain;
- principal/projective angles remain angular quantities;
- covariance/eigenvalue units follow measurement units;
- repeated/near-repeated eigenvalues favor subspace/projector metrics over raw eigenvector equality;
- upstream diagnostic correlation does not automatically prove causal mechanism;
- software transformations must be provenance preserving;
- boundary invalidity is not hidden by a downstream finite metric.

### Result

**CONSISTENT — PASS.**

---

## 17. F12/F13 ↔ D/F — Provenance and Publication Evidence

The run/provenance model remains consistent with publication immutability:

```text
study / condition / trial ensemble
algorithm / implementation
run / execution
input-data / calibration / external artifact
hardware build
derived result / figure / table
publication evidence package
```

Reconciliation confirms:

```text
branch/path/timestamp/seed alone are not scientific identity
semantic config hashing does not erase scientific distinctions
accepted/cited artifacts are immutable/versioned
manual scientific-value edits require explicit lineage
missing artifacts downgrade reproducibility claims
reproducibility does not prove correctness or physical validation
```

### Result

**CONSISTENT — PASS.**

---

## 18. Cross-ADR Reconciliation after Gates A–F

No later ADR-004 gate redefines accepted upstream authority.

### ADR-001 remains authoritative for

```text
geometry
coordinate/direction convention
receive steering sign
phase reference
physical positions
stable channel identity
```

### ADR-002 remains authoritative for

```text
propagation
far-field / narrowband meaning
snapshot semantics
source/noise/SNR semantics
covariance / second moment / rank distinctions
MIMO physical-channel provenance
```

### ADR-003 remains authoritative for

```text
sensor-imperfection operator graph
calibration
compatibility
identifiability
reference plane
ADC/receiver effects
measured/EM manifolds
```

ADR-004 remains downstream and governs evidence about those objects.

### Result

**CONSISTENT — PASS.**

---

## 19. VP-001 Final Cross-Gate Profile Check

VP-001 remains bounded to the intended initial baseline:

```text
1-D receive array
ADR-001 canonical geometry/angle/phase-reference semantics
ADR-002 PM-001 far-field narrowband profile
ADR-003 ideal Phase-1 sensor
K=1 and K=2 primary studies
zero-mean proper-complex source/noise baseline
white equal-variance additive noise
L simultaneous-equivalent snapshots per trial
uncentered sample second moment XX^H/L
Bartlett / MVDR / MUSIC candidate algorithms
oracle-K only when explicitly labeled
one-to-one evaluator association
fixed-N confirmatory preference
Wilson default only for ordinary IID fixed-N Bernoulli event metrics
float64 -> optional float32 -> fixed -> bit-accurate -> HLS/RTL -> FPGA replay
```

No Gate expands plain VP-001 silently to near-field, wideband, coupling, colored-noise, measured-manifold, unknown-K, TDM-MIMO, or physical-acquisition validation claims.

### Result

**CONSISTENT — PASS.**

---

## 20. Reconciliation Finding XG-004-01 — Lifecycle Metadata Drift

The governing ADR file was originally written before the acceptance gates and its lifecycle metadata/header still contains draft-era statements such as:

```text
pre-Gate consistency review pending
Gate A may begin only after pre-Gate review
formal Gate-E evidence pending
Gates A-F not started
```

The authoritative checkpoint and dedicated audit records now establish that the pre-Gate review and Gates A–F all passed.

### Classification

```text
Type: administrative / lifecycle-status drift
Scientific-contract effect: NONE
Normative F1-F14 contradiction: NONE
Cross-gate scientific blocker: NO
Final-acceptance action required: YES
```

### Required finalization action

Before ADR-004 is marked `Accepted`, the final acceptance transaction shall synchronize the governing ADR lifecycle metadata so that it references:

```text
Pre-Gate review PASS
Gates A-F PASS
Final Cross-Gate Reconciliation PASS
GRP-018 formal Gate-E evidence PASS
Final Acceptance Record
Status Accepted
```

The historical gate-entry language may remain only if clearly labeled historical process context; it shall not remain as current lifecycle status.

This administrative drift does **not** invalidate any Gate-A through Gate-F scientific result because all gates audited the stable governing normative content identified by the reviewed content SHA and subsequent gate records did not modify F1-F14 semantics.

### Result

**NON-BLOCKING FOR CROSS-GATE SCIENTIFIC PASS; BLOCKING ONLY FOR FINAL ACCEPTED STATUS UNTIL SYNCHRONIZED.**

---

## 21. Reconciliation Matrix

```text
A physical    <-> B mathematical                         PASS
A physical    <-> F profile/boundary                     PASS
B mathematical<-> C units                                PASS
B mathematical<-> E deterministic oracle                 PASS
B mathematical<-> F mathematical domains                 PASS
C units       <-> E oracle units                         PASS
C units       <-> D software boundaries                  PASS
D software    <-> F failure/status behavior              PASS
D software    <-> E oracle independence                  PASS
E oracle      <-> F oracle boundary behavior             PASS
A/D/F         <-> hardware/physical-validation boundary  PASS
B/D/E/F       <-> P_D / P_res denominator semantics      PASS
F5/F6/D/E/F   <-> association/resolution/localization    PASS
F7/F8/D/F     <-> MC adequacy/fair comparison            PASS
F10/B/C/D/F   <-> multi-level diagnostics                PASS
F12/F13/D/F   <-> provenance/publication                 PASS
ADR-001/2/3   <-> ADR-004 downstream authority           PASS
VP-001        <-> all gates                              PASS
```

---

## 22. Corrections Introduced Across the Lifecycle

The only governing-draft semantic corrections occurred before Gate A during the pre-Gate review:

```text
PG-004-01  P_D/P_res metric universes/denominators
PG-004-02  population variance semantics
PG-004-03  K/rank/model-order/K_hat distinctions
PG-004-04  independent numerical/external-tool evidence role
```

After that correction commit, Gates A–F did not require a further normative F1-F14 change.

Gate B/C/D/F added audit-level domain clarifications and boundary classifications; Gate E instantiated deterministic references. None changes the accepted meaning of the governing clauses.

### Result

**NO POST-GATE NORMATIVE SEMANTIC DRIFT IDENTIFIED.**

---

## 23. Blocking-Contradiction Audit

```text
Blocking physical contradiction                         NONE
Blocking mathematical contradiction                     NONE
Blocking unit/dimensional contradiction                  NONE
Blocking software-semantic contradiction                 NONE
Blocking Golden-Reference contradiction                  NONE
Blocking boundary/failure ambiguity                      NONE
Blocking cross-ADR contradiction                         NONE
Blocking VP-001 profile contradiction                    NONE
Blocking cross-gate scientific contradiction             NONE
```

Administrative lifecycle metadata sync remains required before final Accepted status, as recorded in XG-004-01.

---

## 24. Final Cross-Gate Decision

### **Final Cross-Gate Reconciliation: PASS**

The combined ADR-004 evidence is scientifically coherent across all acceptance dimensions.

The core final invariant is:

> GeoDOA Studio shall preserve the scientific identity, provenance, domain, failure state, and metric universe of evidence from physical/statistical model through software, stochastic evaluation, hardware cross-validation, and publication, without silently upgrading epistemic authority or discarding non-success evidence.

All six individual Gates remain valid after mutual reconciliation.

The next and only remaining ADR-004 scientific-foundation finalization action is:

```text
ADR-004 Final Acceptance Record
+
Governing ADR lifecycle metadata/status synchronization
```

ADR-004 is **not yet Accepted by this reconciliation document alone**.

---

## 25. Status after Final Cross-Gate Reconciliation

```text
Explorations 4.1–4.20                  COMPLETE
Governing ADR-004 normative draft      COMPLETE
Pre-Gate consistency review            PASS
Gate A — Physical Consistency          PASS
Gate B — Mathematical Consistency      PASS
Gate C — Dimensional / Unit            PASS
Gate D — Software Semantic             PASS
Gate E — Golden Reference              PASS
Gate F — Boundary / Failure            PASS
Final Cross-Gate Reconciliation        PASS
Lifecycle metadata synchronization     REQUIRED AT FINAL ACCEPTANCE
Final Acceptance Record                NEXT
ADR-004 status                         NOT YET ACCEPTED
Authoritative Phase-1 implementation   NOT YET AUTHORIZED
```
