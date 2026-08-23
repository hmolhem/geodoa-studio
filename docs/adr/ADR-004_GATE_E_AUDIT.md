# ADR-004 Gate E — Golden Reference / Hand Reference Evidence Audit

- **ADR:** ADR-004 — Validation, Reproducibility, and Scientific Evidence
- **Phase:** 0C — Scientific Foundations
- **Gate:** E — Hand Reference Evidence
- **Gate result:** **PASS**
- **Governing draft:** `ADR-004-validation-reproducibility-scientific-evidence.md`
- **Golden reference evidence:** `../science/golden_reference/ADR-004_GOLDEN_REFERENCE_PROBLEMS.md`
- **Canonical reserved problem:** GRP-018
- **Supplemental deterministic references:** ADR-004-SRC-01 through ADR-004-SRC-04
- **Gates A–D:** PASS
- **Gate F:** Not evaluated by this audit
- **ADR-004 acceptance:** NOT ACCEPTED

> Gate E verifies that ADR-004 has deterministic, hand-computable, implementation-independent reference evidence suitable for future Phase-1 test oracles. It does not accept boundary/failure behavior; Gate F remains required.

---

## 1. Gate E Criterion

Gate E asks whether the critical mathematical/evidence semantics of ADR-004 can be checked against deterministic references that do not depend on the future production implementation.

The evidence must be:

```text
small enough to inspect by hand/basic calculator
independent of production software outputs
explicit about inputs, units, exact/approximate status
traceable to governing ADR semantics
suitable for future regression-oracle use
clear about failure interpretation and tolerance rationale
```

---

## 2. Evidence Reviewed

The Gate-E evidence file contains:

```text
GRP-018       Bias / Variance / MSE / RMSE by hand
ADR-004-SRC-01  Multi-source association / spurious output / resolution
ADR-004-SRC-02  End-to-end P_res denominator / failure mapping
ADR-004-SRC-03  Source-level P_D opportunity counting
ADR-004-SRC-04  Projective manifold metric / projector leakage
```

No canonical GRP numbering beyond the roadmap-reserved GRP-018 was introduced.

---

## 3. GRP-018 Review

### Inputs

```text
truth      = 10 deg
estimates  = {9, 10, 12, 13} deg
N          = 4
```

Signed errors:

\[
\{-1,0,2,3\}^\circ.
\]

### Bias

\[
\bar e=1^\circ.
\]

### Direct MSE

\[
\widehat{MSE}
=\frac{1+0+4+9}{4}
=3.5\ \mathrm{deg}^2.
\]

### RMSE

\[
\widehat{RMSE}
=\sqrt{3.5}
=1.8708286933869707^\circ.
\]

### Divisor-`N` centered second moment

Centered errors:

\[
\{-2,-1,1,2\}^\circ.
\]

Therefore

\[
v_N=2.5\ \mathrm{deg}^2.
\]

and

\[
\boxed{\widehat{MSE}=v_N+\bar e^2=3.5\ \mathrm{deg}^2}.
\]

### Divisor-`N-1` sample variance

\[
s^2=\frac{10}{3}\ \mathrm{deg}^2.
\]

Hence

\[
s^2\neq v_N.
\]

### Gate-E finding

**PASS.** The reserved GRP verifies the core finite-sample localization metric semantics exactly.

---

## 4. Independent Calculation Paths

GRP-018 intentionally verifies MSE by two distinct hand paths:

```text
Path A: direct mean of squared errors
Path B: divisor-N centered moment + squared bias
```

Both return

\[
3.5\ \mathrm{deg}^2.
\]

This independence is important because future software that computes both quantities from the same buggy helper could otherwise reproduce its own error.

### Gate-E finding

**PASS.** The reference is not a single opaque expected number.

---

## 5. Unit Conversion Review

Using

\[
1^\circ=\frac{\pi}{180}\ \mathrm{rad},
\]

the evidence correctly gives:

\[
\bar e=\frac{\pi}{180}
\approx0.017453292519943295\ \mathrm{rad},
\]

\[
\widehat{MSE}
=3.5\left(\frac{\pi}{180}\right)^2
\approx0.00106616096925348\ \mathrm{rad}^2,
\]

\[
\widehat{RMSE}
=\sqrt{3.5}\frac{\pi}{180}
\approx0.0326521204403861\ \mathrm{rad}.
\]

### Gate-E finding

**PASS.** Base-unit and squared-unit conversion semantics are independently represented.

---

## 6. Tolerance Review

The deterministic reference tolerances are scoped to future regression tests and are not engineering-performance thresholds.

The degree-domain rational arithmetic is exact except for the square root; radian conversions additionally depend on ordinary float64 `pi`/transcendental evaluation.

The recommended tolerances are therefore appropriately tight for detecting implementation-semantic errors while remaining conceptually distinct from physical/model acceptance tolerances.

### Gate-E finding

**PASS.** No universal scientific threshold is introduced through regression tolerance language.

---

## 7. ADR-004-SRC-01 Review — Association / Spurious / Resolution

Given:

```text
truth      {0, 10} deg
estimates  {1, 9, 40} deg
association gate 3 deg
```

The admissible one-to-one matches are:

```text
0 -> 1
10 -> 9
```

with one unmatched/spurious estimate at `40 deg`.

The reference correctly distinguishes:

```text
baseline pair resolved = true
clean no-spurious resolution = false
```

and matched errors are `{+1,-1} deg`, giving matched RMSE `1 deg`.

### Gate-E finding

**PASS.** Association, spurious output, resolution, and localization error remain separate deterministic evidence objects.

---

## 8. ADR-004-SRC-02 Review — `P_res` Denominator

Five eligible compatible trials contain:

```text
2 resolved valid
2 unresolved/missed valid
1 numerical algorithm failure
```

The baseline end-to-end result is

\[
\widehat P_{res}=\frac25=0.4.
\]

A separately conditioned valid-output-only metric would be

\[
\widehat P_{res\mid valid}=\frac24=0.5.
\]

### Gate-E finding

**PASS.** The reference demonstrates that silent failure filtering changes the estimand and denominator.

---

## 9. ADR-004-SRC-03 Review — Source-Level `P_D`

Three trials with two truth sources each produce six eligible source opportunities.

Detected opportunities:

```text
Trial 1: 2
Trial 2: 1
Trial 3 numerical failure: 0
```

Thus

\[
\widehat P_D=\frac36=0.5.
\]

A separately conditioned valid-output metric is

\[
\widehat P_{D\mid valid}=\frac34=0.75.
\]

### Gate-E finding

**PASS.** Opportunity counting and failure mapping are explicit and hand-verifiable.

---

## 10. ADR-004-SRC-04 Review — Projective Metric

For

\[
a=[1,0]^T,
\qquad
b=\frac1{\sqrt2}[1,1]^T,
\]

both unit norm, the evidence gives

\[
\rho=\frac1{\sqrt2},
\]

\[
\alpha=\frac\pi4,
\]

\[
d_{proj}^2=\frac12,
\]

and

\[
\|P_a^\perp b\|_2^2=\frac12=1-\rho^2.
\]

Nonzero complex rescaling leaves `rho` unchanged.

### Gate-E finding

**PASS.** The projective metric and rank-one leakage identity are exactly verified on a nonzero-vector reference.

---

## 11. Evidence Independence Audit

The reference file explicitly states that no result is copied from saved GeoDOA production output.

The calculations use:

```text
integer/rational arithmetic
simple square roots
standard pi-based unit conversion
small finite assignment tables
simple probability counts
2-vector/projector algebra
```

No future implementation helper/library is required to establish the expected results.

### Gate-E finding

**PASS.** The evidence is independent enough to serve as a software oracle.

---

## 12. Coverage Adequacy

GRP-018 is the only canonical roadmap-reserved ADR-004 problem and is fully formalized.

The supplemental references cover the most failure-prone deterministic semantics not represented by GRP-018:

```text
multi-source association
resolution-vs-spurious distinction
end-to-end probability denominator
source-opportunity detection denominator
projective/gauge-aware manifold metric
```

Other ADR-004 contracts such as provenance immutability, calibration-vs-validation vocabulary, worker-order RNG semantics, and hardware build identity are structural/software contracts rather than natural hand-numeric GRPs and are appropriately covered by Gates A/D/F and future implementation tests.

### Gate-E finding

**PASS.** No additional canonical GRP is required before proceeding to Gate F.

---

## 13. Future Phase-1 Oracle Obligations

After ADR-004 acceptance, Phase-1 tests should promote these exact references into implementation tests without regenerating expected values from production code.

At minimum:

```text
GRP-018 bias/v_N/s^2/MSE/RMSE test
GRP-018 degree/radian squared-unit conversion test
SRC-01 unequal-cardinality association test
SRC-02 P_res failure-denominator test
SRC-03 source-level P_D opportunity test
SRC-04 projective-metric/projector identity test
```

The reference evidence shall remain frozen/versioned when used as accepted test oracle content.

---

## 14. Gate E Checklist

```text
Canonical GRP-018 present                         PASS
Inputs and truth/reference explicit               PASS
Signed error semantics                            PASS
Bias arithmetic                                   PASS
Direct MSE arithmetic                             PASS
RMSE arithmetic                                   PASS
Divisor-N empirical centered moment               PASS
Divisor-(N-1) sample variance distinction         PASS
Independent MSE calculation paths                 PASS
Degree/radian conversion                          PASS
Squared-unit conversion                           PASS
Regression tolerance rationale                    PASS
Failure interpretation                            PASS
Association/spurious/resolution supplemental      PASS
P_res denominator supplemental                    PASS
P_D opportunity supplemental                      PASS
Projective metric supplemental                    PASS
Independent of production implementation          PASS
Future regression-oracle suitability              PASS
Blocking hand-reference contradiction             NONE
```

---

## 15. Gate E Decision

### **Gate E — Golden / Hand Reference Evidence: PASS**

GRP-018 is now formally promoted from exploration arithmetic to accepted Gate-E deterministic reference evidence for ADR-004.

The supplemental `ADR-004-SRC-*` references provide additional small, transparent oracles for the association/event/probability/projective semantics most likely to be implemented incorrectly.

No governing-draft correction was required for Gate E.

---

## 16. Status after Gate E

```text
Pre-Gate consistency review                PASS
Gate A — Physical Consistency              PASS
Gate B — Mathematical Consistency          PASS
Gate C — Dimensional / Unit Consistency     PASS
Gate D — Software Semantic Consistency      PASS
Gate E — Hand Reference Evidence            PASS
Gate F — Boundary / Failure Analysis         NEXT
ADR-004 acceptance                          NOT ACCEPTED
Authoritative Phase-1 implementation        NOT YET AUTHORIZED
```

The next work item is:

```text
ADR-004 Gate F — Boundary and Failure Analysis
```
