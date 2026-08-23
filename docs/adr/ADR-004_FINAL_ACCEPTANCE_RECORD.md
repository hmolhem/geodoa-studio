# ADR-004 — Final Acceptance Record

- **ADR:** `ADR-004-validation-reproducibility-scientific-evidence.md`
- **Phase:** 0C — Scientific Foundations
- **Final status:** ACCEPTED
- **Acceptance date:** 2026-08-23
- **Purpose:** Final scientific acceptance of ADR-004 after exploration reconciliation, pre-Gate review, Gates A–F, formal Golden Reference evidence, boundary/failure analysis, and Final Cross-Gate Reconciliation.
- **Accepted normative content reviewed through Gates A–F:** blob `8cca2e3ac514cd031bee1d8c9e4c0347694ecb53`
- **Final Cross-Gate Reconciliation:** `ADR-004_FINAL_CROSS_GATE_RECONCILIATION.md` — PASS

## 1. Acceptance Decision

ADR-004 — Validation, Reproducibility, and Scientific Evidence is **ACCEPTED** as the authoritative GeoDOA scientific evidence contract for its declared scope.

All required Phase 0C evidence stages pass:

| Stage | Requirement | Final Status | Primary Evidence |
|---|---|---|---|
| Pre-Gate | Governing-draft consistency | PASS | `ADR-004_PRE_GATE_CONSISTENCY_REVIEW.md` |
| A | Physical consistency | PASS | `ADR-004_GATE_A_AUDIT.md` |
| B | Mathematical consistency | PASS | `ADR-004_GATE_B_AUDIT.md` |
| C | Dimensional and unit consistency | PASS | `ADR-004_GATE_C_AUDIT.md` |
| D | Software semantic consistency | PASS | `ADR-004_GATE_D_AUDIT.md` |
| E | Golden / hand reference evidence | PASS | `ADR-004_GATE_E_AUDIT.md`, `../science/golden_reference/ADR-004_GOLDEN_REFERENCE_PROBLEMS.md` |
| F | Boundary and failure analysis | PASS | `ADR-004_BOUNDARY_FAILURE_ANALYSIS.md`, `ADR-004_GATE_F_AUDIT.md` |
| Final | Cross-gate reconciliation | PASS | `ADR-004_FINAL_CROSS_GATE_RECONCILIATION.md` |

No blocking scientific, mathematical, dimensional, software-semantic, Golden-Reference, boundary/failure, cross-ADR, VP-001, or cross-gate contradiction remains.

## 2. Accepted Core Decision

GeoDOA Studio shall treat scientific evidence as a **typed, layered, provenance-preserving system**.

The accepted evidence chain is:

```text
accepted physical/statistical model
    -> deterministic verification
    -> verified software reference
    -> declared stochastic experiment
    -> typed estimator/trial outcomes
    -> association / detection / resolution / localization metrics
    -> adequacy + uncertainty
    -> fair comparison / engineering interpretation
    -> float/fixed/HLS/RTL/FPGA cross-validation where applicable
    -> immutable run/provenance record
    -> publication/reproducibility package
```

ADR-004 remains downstream of ADR-001/002/003 scientific authority and governs how evidence about those accepted models is generated, scored, compared, qualified, reproduced, and published.

## 3. Accepted Evidence Roles and Truth/Reference Semantics

The following remain distinct:

```text
verification
physical validation
calibration
reproducibility
benchmark comparison
implementation cross-validation
```

Thus software agreement, CST/external-tool agreement, calibration fit, reproducibility, and synthetic FPGA replay do not by themselves establish physical validation.

GeoDOA distinguishes exact simulation truth, reference artifact, physical measurement, calibration estimate, external-tool/model prediction, algorithm estimate, and unresolved reference state. `truth` is reserved for exact-by-construction or otherwise explicitly justified truth roles. Evaluator access to truth does not authorize estimator access; true `K`, true manifold, true noise covariance, true SNR, and related generative parameters are oracle information when supplied to the algorithm.

## 4. Accepted Experimental / RNG Semantics

The accepted hierarchy is:

```text
study -> condition -> Monte Carlo trial -> L snapshots/samples
```

with separate method, implementation, run/execution, artifact, and build identities.

Snapshot count `L`, Monte Carlo count `N`, source count `K`, source-covariance rank, observed subspace rank, estimator model order, output cardinality `K_hat`, and matched/source-opportunity counts remain distinct.

Exact stochastic replay requires root seed/seed-set, RNG family/version semantics, semantic child-stream derivation, study/condition/trial identity, random-family identity, substream role, and redraw scope. Process-global mutable RNG is not authoritative. CRN shares scientifically common exogenous latent randomness under a declared mapping.

## 5. Accepted Association / Detection / Resolution Semantics

Multi-source truth is unordered unless persistent physical identities are independently justified. The accepted evaluation sequence is:

```text
raw estimator output
-> execution/failure state
-> one-to-one evaluator association
-> detected / missed / spurious outcomes
-> resolution event
-> localization metrics on declared matched universe
```

Unequal cardinality preserves unmatched truth and unmatched estimates. Spurious output is not automatically formal false alarm; formal `P_FA` requires a null/detection-theory protocol. Resolution requires distinct admissible one-to-one matches for required truth members. Search-grid spacing, beamwidth, Rayleigh heuristics, peak count, and truth separation are not definitions of empirical resolution probability.

## 6. Accepted Bias / Variance / MSE / RMSE Semantics

For a real scalar localization estimate and fixed truth:

\[
e=\hat q-q,
\qquad
\operatorname{Bias}=E[e],
\]

\[
\operatorname{Var}(\hat q)=E[(e-E[e])^2],
\]

\[
\operatorname{MSE}=E[e^2]
=\operatorname{Var}(\hat q)+\operatorname{Bias}^2,
\qquad
\operatorname{RMSE}=\sqrt{\operatorname{MSE}}.
\]

For finite errors:

\[
\bar e=\frac1N\sum_i e_i,
\qquad
v_N=\frac1N\sum_i(e_i-\bar e)^2,
\]

and exactly

\[
\boxed{\widehat{MSE}=v_N+\bar e^2.}
\]

The divisor-`N-1` sample variance `s^2` is distinct from `v_N`. Future complex-valued errors require an explicit complex error metric rather than silent reuse of the real `e^2` formulas.

## 7. Accepted Event-Probability Universes

For VP-001 baseline end-to-end resolution:

\[
\widehat P_{res}=\frac{N_{resolved}}{N_{eligible,compatible}}.
\]

For VP-001 source-level end-to-end detection:

\[
\widehat P_D
=\frac{N_{detected\ truth\ opportunities}}
{N_{eligible\ truth\ opportunities\ in\ compatible\ trials}}.
\]

Valid misses/unresolved events and numerical/algorithm failures on otherwise eligible compatible trials are end-to-end non-successes, with failure status preserved. Invalid input/reference, outside-profile states, and method incompatibility are excluded from ordinary event universes and reported separately. Conditional survivor metrics require distinct identities.

## 8. Accepted Matrix, Units, and Metric Semantics

For VP-001,

\[
\hat R^{(2)}=\frac1LXX^H
\]

is the **uncentered sample second moment**, not centered sample covariance.

Bias/RMSE use the base localization unit; variance/MSE use its square. Probability and normalized projective quantities are dimensionless. Covariance/eigenvalue units derive from snapshot units. dB is a logarithmic representation of a declared ratio/reference.

For nonzero compatible vectors:

\[
\rho(a,b)=\frac{|a^Hb|}{\|a\|\|b\|},
\qquad
\alpha=\cos^{-1}\rho,
\qquad
 d_{proj}^2=1-\rho^2.
\]

## 9. Accepted Monte Carlo / Comparison Semantics

There is no universal adequate Monte Carlo trial count. Adequacy depends on metric, precision, condition difficulty, tails/events, dependence, failures, design, claim, and budget. VP-001 confirmatory studies initially prefer predeclared fixed `N` with achieved adequacy/uncertainty reporting. Wilson is the VP-001 default only for ordinary IID fixed-`N` Bernoulli event evidence.

Fair comparison preserves task/domain, truth/reference, source/noise/SNR/L semantics, sensor/calibration profile, oracle information, pre/postprocessing, association/metric/failure policy, tuning budget, CRN/pairing, resource constraints, uncertainty, and runtime scope. `p>0.05` is not equivalence.

## 10. Accepted Failure / Eligibility Semantics

Compatibility status, execution/outcome status, and metric eligibility are distinct. No universal `success` Boolean may replace them. `NaN` is not a scientific failure taxonomy.

The accepted governing rule is:

> Failure shall be represented at the earliest scientifically correct layer, preserved through downstream evidence, and mapped into each metric by an explicit eligibility/denominator policy rather than by silent filtering, numeric coercion, or overloaded success flags.

## 11. Accepted Float / Fixed / FPGA Evidence Ladder

The accepted ladder is:

```text
accepted scientific contract
-> verified float64 reference
-> float32 assessment if used
-> explicit fixed-point numerical model
-> bit-accurate implementation model
-> HLS/RTL verification
-> synthesis/place-route/timing evidence
-> FPGA/SoC board execution
-> later physical sensor/system validation
```

Fixed-point semantics include signedness, word/integer/fractional widths, scale, rounding/truncation, saturation/wrap, casts, accumulator widths, coefficient quantization, and material operation ordering. Bit-exactness and bounded numerical equivalence are distinct. ADC acquisition quantization remains distinct from FPGA fixed-point arithmetic. Synthetic board replay is not physical validation.

## 12. Accepted Provenance / Publication Semantics

Scientific identity distinguishes study, condition, trial/ensemble, algorithm, implementation, run, data/calibration/external artifact, derived result/figure/table, and hardware build. A timestamp, path, filename, branch, run token, or root seed alone is insufficient.

Canonical configuration uses a versioned semantic representation with explicit units, resolved defaults, stable serialization, authoritative/derived distinctions, and upstream ADR/profile/schema versions. SHA-256 is the Phase-1 baseline fingerprint mechanism unless later versioned replacement is adopted.

Figures/tables are derived artifacts, not the evidence package. Scientific-value transformations must be scripted or deterministically recorded. Accepted/cited evidence is immutable/versioned. Reproducibility does not itself prove correctness or physical validity.

## 13. Accepted VP-001 Initial Validation Profile

VP-001 — Phase-1 Ideal Far-Field Narrowband 1-D DOA Validation Profile — is accepted as the initial bounded executable profile jointly governed by ADR-001/002/003/004.

Its baseline includes K=1/K=2 primary cases, proper-complex zero-mean stationary sources, independent/incoherent equal-power two-source baseline, proper-complex white equal-variance noise, ideal Phase-1 sensor, L simultaneous-equivalent snapshots per trial, uncentered sample second moment `XX^H/L`, Bartlett/MVDR/MUSIC candidate baselines, explicit oracle-K labeling, one-to-one evaluator association, fixed-N confirmatory preference, and Wilson only for ordinary IID fixed-N Bernoulli event metrics.

Plain VP-001 excludes near field, wideband, coupling, position/gain/phase/timing imperfections, colored noise, IQ/nonlinearity/clipping, ADC quantization, measured/CST manifold substitution, coherent-source remedies, unknown-K benchmarking, TDM-MIMO temporal effects, and physical acquisition/calibration validation. These require named/versioned extensions or other profiles.

## 14. Accepted Golden Reference Evidence

Canonical Golden Reference:

```text
GRP-018 — Bias, Variance, MSE, and RMSE by hand
truth                 10 deg
estimates             9, 10, 12, 13 deg
errors                -1, 0, 2, 3 deg
bias                  1 deg
v_N                   2.5 deg^2
sample variance s^2   10/3 deg^2
MSE                   3.5 deg^2
RMSE                  sqrt(3.5) = 1.8708286933869707 deg
```

Supplemental accepted references:

```text
ADR-004-SRC-01  association / spurious / resolution
ADR-004-SRC-02  P_res denominator / numerical-failure mapping
ADR-004-SRC-03  source-level P_D opportunity counting
ADR-004-SRC-04  projective metric / rank-one projector leakage
```

## 15. Accepted Boundary Evidence

`ADR-004_BOUNDARY_FAILURE_ANALYSIS.md` classifies `F-004-001` through `F-004-110`, including truth/reference validity, trial/RNG identity, config/provenance, VP-001 boundaries, covariance/subspace, association/cardinality, metric/event denominators, Monte Carlo uncertainty, normalized metrics, comparison fairness, FPGA/protocol/build failures, publication integrity, compatibility/identifiability, and data-integrity boundaries.

Representative accepted responses include:

```text
N=0 metric universe                    -> undefined / not assessed, not numeric zero
N=1 divisor-(N-1) sample variance     -> undefined
zero-vector normalized correlation    -> undefined metric
association tie without policy        -> ambiguous / unresolved
singular whitening                    -> require other/regularized treatment
near-field under plain VP-001         -> incompatible profile, not invalid physics
numerical failure in eligible trial   -> typed failure + end-to-end event non-success
invalid/out-of-profile condition      -> not coerced into ordinary event failure
packing/build mismatch                -> hardware/data-integrity failure
missing publication artifact          -> incomplete/downgraded reproducibility
```

## 16. Evidence Set

The accepted ADR-004 evidence set consists of:

```text
docs/adr/ADR-004-validation-reproducibility-scientific-evidence.md
docs/adr/ADR-004_EXPLORATION_CHECKPOINT.md
docs/adr/ADR-004_EXPLORATION_4.20_CROSS_SECTION_RECONCILIATION.md
docs/adr/ADR-004_PRE_GATE_CONSISTENCY_REVIEW.md
docs/adr/ADR-004_GATE_A_AUDIT.md
docs/adr/ADR-004_GATE_B_AUDIT.md
docs/adr/ADR-004_GATE_C_AUDIT.md
docs/adr/ADR-004_GATE_D_AUDIT.md
docs/science/golden_reference/ADR-004_GOLDEN_REFERENCE_PROBLEMS.md
docs/adr/ADR-004_GATE_E_AUDIT.md
docs/adr/ADR-004_BOUNDARY_FAILURE_ANALYSIS.md
docs/adr/ADR-004_GATE_F_AUDIT.md
docs/adr/ADR-004_FINAL_CROSS_GATE_RECONCILIATION.md
docs/adr/ADR-004_FINAL_ACCEPTANCE_RECORD.md
```

Explorations 4.1–4.19 remain retained as derivation/rationale/provenance evidence.

## 17. What Acceptance Does Not Mean

ADR-004 acceptance does **not** mean authoritative Phase-1 software has already been implemented or verified. It does not mean deferred profiles are implemented. It does not make every Monte Carlo study adequate, every comparison fair, or every fixed/HLS/RTL/FPGA result accepted automatically. Synthetic FPGA replay remains distinct from physical validation.

## 18. Implementation Authorization Consequence

With ADR-001, ADR-002, ADR-003, and ADR-004 accepted, the initial Phase-0C scientific semantics required by VP-001 are sufficiently governed to begin **authoritative Phase-1 implementation planning and implementation**, subject to the repository roadmap and normal engineering workflow.

Implementation shall consume these contracts rather than reconstruct scientific conventions from memory. The first implementation targets should derive from VP-001 and the accepted Golden Reference suite, with software tests for Gate-D obligations and Gate-F boundaries.

Acceptance authorizes implementation work; it does not pre-accept the implementation.

## 19. Final Decision

### **ADR-004: ACCEPTED**

The final invariant is:

> GeoDOA Studio shall preserve the scientific identity, provenance, domain, uncertainty, failure state, comparison contract, and metric universe of evidence from accepted physical/statistical model through deterministic verification, stochastic evaluation, implementation cross-validation, and publication, without silently upgrading epistemic authority or discarding scientifically meaningful non-success evidence.

```text
Explorations 4.1–4.20                  COMPLETE
Pre-Gate consistency review            PASS
Gate A — Physical                      PASS
Gate B — Mathematical                  PASS
Gate C — Dimensional / Unit            PASS
Gate D — Software Semantic             PASS
Gate E — Golden Reference              PASS
Gate F — Boundary / Failure            PASS
Final Cross-Gate Reconciliation        PASS
ADR-004                                ACCEPTED
```
