# ADR-004 Gate F — Boundary and Failure Analysis Audit

- **ADR:** ADR-004 — Validation, Reproducibility, and Scientific Evidence
- **Phase:** 0C — Scientific Foundations
- **Gate:** F — Boundary / Failure Analysis
- **Gate result:** **PASS**
- **Governing draft:** `ADR-004-validation-reproducibility-scientific-evidence.md`
- **Boundary evidence:** `ADR-004_BOUNDARY_FAILURE_ANALYSIS.md`
- **Golden reference evidence:** `../science/golden_reference/ADR-004_GOLDEN_REFERENCE_PROBLEMS.md`
- **Prior gates:** Pre-Gate review PASS; Gates A–E PASS
- **ADR-004 acceptance:** NOT ACCEPTED

> Gate F verifies that invalid inputs, out-of-profile scenarios, ambiguous states, estimator non-successes, numerical/hardware failures, metric-domain failures, provenance failures, and publication-integrity failures have explicit scientific responses and are not silently coerced into ordinary successful evidence.

---

## 1. Gate F Criterion

Gate F requires boundary/failure behavior to be explicit enough that implementation and scientific reporting cannot hide the layer at which evidence became invalid, incompatible, unresolved, failed, or ineligible.

The core response classes reviewed are:

```text
REJECT / INVALID
INCOMPATIBLE / REQUIRE OTHER PROFILE OR MODEL
VALID NON-SUCCESS
EXECUTION FAILURE
DIAGNOSTIC / WARN
UNRESOLVED
NOT ASSESSED
```

These classes are combined with ADR-004's separate compatibility, execution-status, and metric-eligibility layers rather than collapsed into one global success flag.

---

## 2. Boundary Evidence Reviewed

The dedicated analysis defines `F-004-001` through `F-004-110`, covering:

```text
truth/reference provenance
study/condition/trial identity
RNG and common-random-number semantics
configuration/hash/provenance
VP-001 profile boundaries
covariance/subspace domains
association/cardinality/ties
localization metrics
P_D / P_res denominators
Monte Carlo adequacy / uncertainty
normalized manifold/subspace metrics
fair comparisons
tuning / oracle-information asymmetry
fixed-point / HLS / RTL / FPGA
publication / reproducibility
calibration / compatibility / identifiability
data integrity / search-sector / nonfinite values
```

**Coverage result:** PASS.

---

## 3. Invalid versus Out-of-Profile Science

The analysis correctly distinguishes an invalid object from valid science requiring another profile.

Examples:

```text
negative/undefined metric denominator       -> INVALID / UNDEFINED METRIC
near-field scene under plain VP-001         -> INCOMPATIBLE / REQUIRE NEAR-FIELD PROFILE
colored-noise scene under white-noise VP-001-> INCOMPATIBLE / REQUIRE OTHER PROFILE
unknown truth coordinate/frame              -> INVALID scoring until resolved
```

A valid physical scene is not rejected merely because VP-001 is insufficient.

**Result:** PASS.

---

## 4. Valid Scientific Non-Success versus Execution Failure

The analysis preserves the distinction:

```text
miss / unresolved source pair / valid no detection
```

versus

```text
numerical failure / algorithm nonconvergence / resource failure / protocol failure
```

Both may affect end-to-end evidence but remain different scientific records.

**Result:** PASS.

---

## 5. Zero-Denominator Boundaries

The following undefined cases are explicitly handled:

```text
N=0 matched localization metric universe
N=1 divisor-(N-1) sample variance
N_eligible=0 for P_res
no eligible truth opportunities for source-level P_D
zero reference norm for relative errors
zero vector for normalized manifold correlation
L=0 sample second-moment estimate
L<2 centered covariance
```

The required behavior is typed undefined/not-assessed/reject as appropriate, never silent numeric `0`, `1`, or bare `NaN`.

**Result:** PASS.

---

## 6. End-to-End Denominator Integrity

The analysis verifies that for baseline VP-001:

- compatible eligible numerical/algorithm failures remain non-success in end-to-end `P_D`/`P_res`;
- invalid inputs/references and method-incompatible/outside-profile conditions are not forced into ordinary event denominators;
- survivor-only conditional metrics require distinct identities;
- numerator cannot exceed denominator.

This is consistent with GRP supplemental references `ADR-004-SRC-02` and `ADR-004-SRC-03`.

**Result:** PASS.

---

## 7. Association / Cardinality / Tie Boundaries

The analysis explicitly prevents:

```text
silent extra-peak truncation
fake padding of missing DOAs
one estimate matched to multiple truths under one-to-one profile
label-based bypass of unordered-set association
library-order tie resolution without declared tie/ambiguity policy
```

Ambiguous equal-cost association remains typed ambiguous/unresolved when policy does not resolve it scientifically.

**Result:** PASS.

---

## 8. Coordinate and Metric-Domain Boundaries

The analysis closes Gate-B domain conditions:

```text
real-valued e^2 localization formulas only on real scalar metric domain
complex quantities require declared complex error metric
angle and direction-cosine errors are distinct
circular/wrapped domains require declared topology-aware metric
rho/projective metrics require nonzero vectors
principal-angle/projector comparisons require declared dimension policy
```

**Result:** PASS.

---

## 9. Numerical Guard versus Silent Repair

The analysis distinguishes a narrow roundoff guard from arbitrary numerical repair.

Example:

```text
rho = 1 + tiny roundoff
```

may be clipped to `[0,1]` only under an explicit numerical-tolerance guard; a materially invalid `rho` shall not be silently clamped.

Similarly, Hermitian/PSD repair, regularization, whitening, normalization, interpolation, and other transforms must be explicit derived operations with preserved original diagnostics.

**Result:** PASS.

---

## 10. Trial/RNG/Replay Boundaries

The analysis explicitly handles:

```text
duplicate trial IDs with different realizations
same realization duplicated under multiple trial IDs
retry that redraws randomness
replacement retaining old trial ID
unknown RNG family/version under exact-replay claim
process-global RNG order dependence
seed cherry-picking
accidental sharing of internal algorithm randomness
```

These failures correctly affect exact replay, fairness, or confirmatory status rather than being hidden as ordinary stochastic variation.

**Result:** PASS.

---

## 11. Configuration / Cache / Resume Boundaries

The analysis rejects or downgrades evidence when:

```text
material defaults are unresolved
schema/hash semantics are ambiguous
unit normalization changes science
branch name substitutes for Git SHA
uncaptured dirty source is used for exact/publication claims
cache dependencies are incomplete
resume occurs after material config/source changes
```

**Result:** PASS.

---

## 12. Fair-Comparison Boundaries

The analysis prevents:

```text
paired claims on uncontrolled independent trials
final-set tuning presented as held-out confirmation
oracle-vs-blind comparison labeled equal-information
geometry superiority without resource disclosure
kernel-only vs end-to-end runtime comparison
CI overlap/nonoverlap used as a direct significance test
p>0.05 used as equivalence
winner-only condition reporting
```

**Result:** PASS.

---

## 13. Hardware / FPGA Boundaries

The analysis explicitly distinguishes:

```text
fixed-point-format incompleteness
ADC quantization vs FPGA fixed point
HLS/RTL numerical mismatch
packing/endianness/protocol failure
bitstream/build provenance mismatch
timing-closure failure
resource exhaustion
synthetic board replay vs physical validation
```

A hardware integration failure is not automatically a localization error and a timing-closure failure does not erase otherwise valid algorithm mathematics.

**Result:** PASS.

---

## 14. Publication / Reproducibility Boundaries

The analysis handles:

```text
untraceable figure/table
manual undocumented value edits
silent overwrite of cited artifacts
missing raw/calibration dependency
proprietary unavailable dependency
exact-environment mismatch
reproducibility package overclaimed as physical correctness
```

Reproducibility level may be downgraded without invalidating all science when a dependency is unavailable, but the limitation must remain explicit.

**Result:** PASS.

---

## 15. Calibration / Compatibility / Identifiability Boundaries

The analysis prevents semantic collapse among:

```text
calibrated
validated
compatible
high-performing
identifiable
```

An unidentifiable scene is not simply an estimator miss, and unresolved compatibility is not promoted to compatible for convenience.

**Result:** PASS.

---

## 16. Metric-Specific Eligibility Matrix

The boundary analysis includes an explicit matrix distinguishing treatment of:

```text
valid success
valid miss/unresolved
numerical/algorithm failure
invalid input/reference/data integrity
outside-profile/incompatible condition
unresolved compatibility/identifiability
hardware/resource/protocol failure
```

across:

```text
end-to-end P_D / P_res
matched RMSE
failure-rate metrics
compatibility reporting
```

This matrix directly enforces the ADR-004 rule that no global `success` boolean can preserve all metric semantics.

**Result:** PASS.

---

## 17. Carried-Forward Gate B / Gate D Conditions

Every explicit boundary condition carried from Gate B and Gate D is classified in the Gate-F analysis, including:

```text
zero manifold
zero relative-error denominator
N=0 / N=1
association ties
unequal subspace dimensions
Wilson non-IID misuse
singular whitening
unknown RNG version
duplicate trial identity
schema/hash ambiguity
incomplete cache dependencies
stale/missing calibration
hardware packing mismatch
bitstream/build mismatch
missing publication raw artifact
backend nondeterminism under exact replay
```

No carried-forward condition remains unclassified.

**Result:** PASS.

---

## 18. Silent-Coercion Audit

The analysis explicitly forbids silent conversion of:

```text
UNRESOLVED -> VALID
INCOMPATIBLE -> R=0
failure -> removed denominator
miss/failure -> arbitrary RMSE angle
spurious estimates -> truncated away
missing estimate -> fake numeric DOA
external artifact -> truth
one seed -> exact replay
p>0.05 -> equivalence
flat MC curve -> adequacy proof
spurious output -> formal P_FA
search-grid spacing -> physical resolution
repaired artifact -> original-valid evidence
new artifact -> overwrite old cited evidence
```

**Result:** PASS.

---

## 19. Gate F Checklist

```text
Boundary response taxonomy                           PASS
Earliest-layer failure attribution                   PASS
Invalid vs incompatible distinction                  PASS
Valid non-success vs execution failure               PASS
Zero-denominator / N=0 / N=1 handling                PASS
Trial/RNG/retry/replacement boundaries               PASS
VP-001 out-of-profile boundaries                     PASS
Covariance/subspace boundaries                       PASS
Association/cardinality/tie boundaries               PASS
Localization-coordinate/unit boundaries              PASS
P_D/P_res denominator integrity                      PASS
MC adequacy / CI / dependence boundaries             PASS
Normalized metric / projector boundaries             PASS
Fair-comparison / tuning / equivalence boundaries    PASS
Fixed/HLS/RTL/FPGA boundaries                        PASS
Publication/reproducibility boundaries               PASS
Calibration/compatibility/identifiability boundaries PASS
Data-integrity / nonfinite boundaries                PASS
Metric-specific eligibility matrix                   PASS
Carried Gate-B/Gate-D conditions classified          PASS
Forbidden silent coercions                           PASS
Blocking boundary/failure ambiguity                  NONE
```

---

## 20. Gate F Decision

### **Gate F — Boundary / Failure Analysis: PASS**

ADR-004 contains sufficient scientific boundary semantics for Phase 0C acceptance consideration.

The contract distinguishes invalid evidence, valid science outside a selected profile, valid scientific non-success, execution failure, unresolved scientific state, and metric-specific ineligibility. It defines how these states propagate into `P_D`, `P_res`, localization metrics, fair comparisons, hardware evidence, and publication/reproducibility claims without silent coercion.

No governing-draft correction was required for Gate F.

---

## 21. Status after Gate F

```text
Pre-Gate consistency review                PASS
Gate A — Physical Consistency              PASS
Gate B — Mathematical Consistency          PASS
Gate C — Dimensional / Unit Consistency     PASS
Gate D — Software Semantic Consistency      PASS
Gate E — Hand Reference Evidence            PASS
Gate F — Boundary / Failure Analysis         PASS
Final Cross-Gate Reconciliation             NEXT
ADR-004 acceptance                          NOT ACCEPTED
Authoritative Phase-1 implementation        NOT YET AUTHORIZED
```

The next work item is:

```text
ADR-004 Final Cross-Gate Reconciliation
```

That reconciliation shall verify that Gate-A through Gate-F conclusions, Gate-E reference evidence, pre-Gate corrections, and the governing draft form one mutually consistent final contract before an ADR-004 acceptance record is written.
