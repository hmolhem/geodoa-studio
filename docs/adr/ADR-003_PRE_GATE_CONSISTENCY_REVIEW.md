# ADR-003 — Pre-Gate Consistency Review

- **Phase:** 0C — Scientific Foundations
- **ADR under review:** `ADR-003-sensor-imperfections-mutual-coupling-calibration.md`
- **Status:** PRE-GATE REVIEW PASS — GATE A MAY BEGIN
- **Acceptance status:** ADR-003 remains NOT ACCEPTED
- **Reviewed against:** Accepted ADR-001, Accepted ADR-002, ADR-003 Exploration 3.14 reconciliation

> This review does not constitute Gate A, Gate B, or any later acceptance gate. Its sole purpose is to verify that the governing ADR-003 draft is coherent enough to enter the formal acceptance sequence.

---

## 1. Review Objective

Verify that the governing ADR-003 draft:

1. inherits accepted ADR-001/ADR-002 conventions without redefining them;
2. faithfully consolidates the reconciled 3.14 contract;
3. does not introduce a new blocking physical or mathematical contradiction;
4. preserves the intended Phase-1 implementation boundary;
5. keeps Gates A–F and Golden Reference evidence explicitly unpassed;
6. is sufficiently stable to begin Gate A — Physical Consistency.

---

## 2. Source-of-Truth Hierarchy Used for Review

The review applies the following authority order:

```text
Accepted ADR-001
    ↓
Accepted ADR-002
    ↓
ADR-003 Exploration 3.14 reconciliation
    ↓
Governing ADR-003 draft
    ↓
Earlier ADR-003 exploration documents as supporting rationale/evidence
```

The governing draft is therefore required to conform upward; it cannot silently override accepted ADR-001 or ADR-002.

---

## 3. ADR-001 Convention Check

### 3.1 Temporal phasor

Draft uses:

\[
\boxed{e^{-j\omega t}}
\]

**Result:** CONSISTENT.

### 3.2 Look direction

Draft preserves array-to-source \(\hat{\mathbf u}\).

**Result:** CONSISTENT.

### 3.3 Propagation direction

Draft preserves

\[
\boxed{\hat{\mathbf k}_{\rm prop}=-\hat{\mathbf u}}.
\]

**Result:** CONSISTENT.

### 3.4 Receive manifold sign

Draft inherits

\[
\boxed{
a_n
=\exp[-jk(\mathbf r_n-\mathbf r_{\rm ref})^T\hat{\mathbf u}].
}
\]

**Result:** CONSISTENT.

### 3.5 Canonical 1-D angular slice

Draft preserves broadside \(\theta=0\), positive angle toward \(+x\), and the accepted direction vector.

**Result:** CONSISTENT.

### 3.6 Geometry/reference semantics

Draft preserves nominal physical coordinates, stable channel identity, and relative/common-phase semantics rather than introducing destructive normalization.

**Result:** CONSISTENT.

---

## 4. ADR-002 Propagation and Measurement Check

### 4.1 Physical delay sign

Draft uses

\[
\boxed{x(t-\tau)\leftrightarrow X(\omega)e^{+j\omega\tau}}.
\]

**Result:** CONSISTENT.

### 4.2 Narrowband hierarchy

Draft treats phase-only delay and static manifold reductions as bounded narrowband specializations rather than exact general delay models.

**Result:** CONSISTENT.

### 4.3 Snapshot semantics

Draft requires simultaneous-equivalent coherent snapshots for the initial classical MUSIC profile and explicitly flags SRO/CFO/TDM timing violations.

**Result:** CONSISTENT.

### 4.4 Covariance semantics

Draft distinguishes population covariance, sample covariance, source covariance rank, signal-subspace dimension, sample rank, and model order.

**Result:** CONSISTENT.

### 4.5 Noise semantics

Draft does not introduce an unqualified generic SNR or one universal final noise variance for all physical stages.

**Result:** CONSISTENT.

### 4.6 MIMO provenance

Draft preserves physical \((\mathrm{Tx}_i,\mathrm{Rx}_j)\) identity and does not silently treat TDM virtual channels as simultaneous.

**Result:** CONSISTENT.

---

## 5. Exploration 3.14 Contract Check

The draft was checked against the compact C-1 through C-11 contract from 3.14.

### C-1 — Scientific object identity

Nominal, physical, measured, EM, calibrated, and simulation-truth responses remain distinct.

**Result:** PASS.

### C-2 — Physical cause/domain

Geometry, element, coupling, electronics, timing, noise, nonlinear response, quantization, and digital selection remain typed distinct.

**Result:** PASS.

### C-3 — Operator ordering/reference planes

The draft preserves typed reference-plane composition and rejects dimension-only compatibility.

**Result:** PASS.

### C-4 — Exact-before-approximate hierarchy

Exact position/path/delay/quantizer meanings precede far-field, narrowband, small-error, high-resolution, or linearized approximations.

**Result:** PASS.

### C-5 — Calibration separation

Calibration remains inference/model/correction rather than a causal forward block.

**Result:** PASS.

### C-6 — Calibration provenance/domain

Direction, frequency, polarization, hardware/state, time, reference planes, and included effects are retained as validity dimensions where applicable.

**Result:** PASS.

### C-7 — Gauge/equivalence semantics

Absolute, phase-only, common-complex-scale/projective, and gauge-fixed comparisons remain distinct.

**Result:** PASS.

### C-8 — Uncertainty/identifiability semantics

Error, uncertainty, repeatability, bias, identifiability, gauge, conditioning, and optimizer convergence remain distinct.

**Result:** PASS.

### C-9 — Statistical consequences

Sensor effects propagate according to physical ordering and are not universally represented as additive white covariance noise.

**Result:** PASS.

### C-10 — Estimator compatibility

Compatibility remains multi-axis/profile-specific with explicit no-silent-coercion rules.

**Result:** PASS.

### C-11 — Phase-1 boundedness

The ideal Phase-1 deterministic sensor graph remains identity and nonideal families remain deferred.

**Result:** PASS.

---

## 6. Reconciled Nuance Check

### 6.1 Common gain

Draft states that common gain is projectively irrelevant to ideal manifold direction but physical SNR/dynamic-range consequences depend on stage/noise ordering.

**Result:** RECONCILED.

### 6.2 Physical delay versus sample-time offset

Draft preserves the opposite tone-phase signs and treats them as different physical operations.

**Result:** RECONCILED.

### 6.3 Geometry phase versus electronic phase versus delay

Draft keeps all three distinct.

**Result:** RECONCILED.

### 6.4 Element response versus coupling

Draft preserves distinct semantics and explicit double-count prevention.

**Result:** RECONCILED.

### 6.5 Network quantities

Draft does not equate \(\mathbf Z\), \(\mathbf S\), \(\mathbf T_L\), effective \(\mathbf C\), embedded patterns, or aggregate manifolds.

**Result:** RECONCILED.

### 6.6 ADC versus FPGA fixed point

Draft explicitly separates ADC acquisition quantization from downstream arithmetic quantization.

**Result:** RECONCILED.

### 6.7 Population versus sample eigengap

Draft requires distinct semantics and does not silently substitute sample separation into population perturbation theorems.

**Result:** RECONCILED.

### 6.8 Direct measured/CST manifold

Draft permits aggregate calibrated use without promoting it to physical truth or requiring unique causal decomposition.

**Result:** RECONCILED.

---

## 7. Mathematical Consistency Spot Checks

These checks are not Gate B; they only look for a draft-blocking error before Gate A.

### 7.1 Position-error sign chain

The far-field phase perturbation retains

\[
\delta\phi_n
\approx
-k\hat{\mathbf u}^T
(\boldsymbol\varepsilon_n-\boldsymbol\varepsilon_{\rm ref}).
\]

**Result:** NO BLOCKER.

### 7.2 Coupling covariance

Draft uses the compatible linear specialization

\[
\mathbf R' = \mathbf C\mathbf R\mathbf C^H.
\]

**Result:** NO BLOCKER.

### 7.3 Data correction covariance

Draft uses

\[
\mathbf R_{\rm corr}
=\mathbf C_{\rm corr}\mathbf R\mathbf C_{\rm corr}^H.
\]

**Result:** NO BLOCKER.

### 7.4 Projective leakage

Draft preserves

\[
1-\rho^2
\]

and its exact rank-one noise-subspace interpretation.

**Result:** NO BLOCKER.

### 7.5 Quantization-noise approximation

\(\Delta^2/12\) is clearly marked as a restricted approximation.

**Result:** NO BLOCKER.

### 7.6 SRO sign relation

Draft preserves

\[
1+\epsilon_T=\frac{1}{1+\epsilon_f},
\qquad
\epsilon_T\approx-\epsilon_f.
\]

**Result:** NO BLOCKER.

---

## 8. Phase-1 Scope Check

The governing draft does not accidentally activate any explored nonideal family.

The initial authoritative candidate remains:

```text
ideal nominal=physical geometry
ideal identical scalar elements
no coupling distortion
unity differential electronics
zero differential delay/skew/SRO/CFO/jitter
linear receiver
no offset/IQ/nonlinearity/clipping
unquantized floating acquisition
white equal-variance proper-complex noise
ordinary covariance/classical MUSIC compatibility
```

**Result:** PASS.

---

## 9. Golden Reference Status Check

The draft reserves:

```text
GRP-014
GRP-015
GRP-016
GRP-017
```

but does not claim formal Gate-E PASS.

Exploratory numerical checks remain supporting evidence only.

**Result:** PASS.

---

## 10. Acceptance-State Check

The draft clearly states:

```text
Explorations 3.1–3.14: COMPLETE
Governing ADR draft: CREATED
Gates A–F: NOT STARTED
ADR-003: NOT ACCEPTED
```

No gate is implicitly marked passed.

**Result:** PASS.

---

## 11. Non-Blocking Draft Notes for Later Gates

The following items are intentionally deferred to formal gates and are not pre-Gate blockers:

1. Gate A must independently re-audit physical causality and reference-plane ordering.
2. Gate B must verify every retained equation and approximation boundary.
3. Gate C must audit SI units, dimensionless ratios, dB semantics, timing units, ADC quantities, and matrix-domain dimensions.
4. Gate D must translate the scientific contract into software semantics without prematurely fixing unnecessary architecture.
5. Gate E must formalize GRP-014 through GRP-017 and decide whether additional deterministic checks deserve Golden Reference status.
6. Gate F must exercise nulls, singular matrices, clipping, out-of-domain calibration, port-state changes, time variation, rank collapse, and other reserved boundary/failure states.
7. Final cross-gate reconciliation may still require edits before acceptance.

---

## 12. Blocking Findings

```text
Physical/sign contradiction:           NONE FOUND
ADR-001 convention override:           NONE FOUND
ADR-002 measurement override:          NONE FOUND
Reference-plane contradiction:         NONE FOUND
Calibration/forward-chain conflation:  NONE FOUND
ADC/FPGA quantization conflation:       NONE FOUND
Phase-1 scope leak:                     NONE FOUND
Premature Gate PASS claim:              NONE FOUND
Premature ADR acceptance claim:         NONE FOUND
```

---

## 13. Pre-Gate Disposition

\[
\boxed{
\text{PRE-GATE CONSISTENCY REVIEW: PASS}
}
\]

The governing ADR-003 draft is sufficiently coherent to enter the formal acceptance sequence.

The next formal work item is:

\[
\boxed{
\text{Gate A — Physical Consistency}
}
\]

ADR-003 remains **NOT ACCEPTED** until Gates A–F and final cross-gate reconciliation all pass.
