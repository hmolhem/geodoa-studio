# ADR-003 — Acceptance Audit

- **ADR:** `ADR-003-sensor-imperfections-mutual-coupling-calibration.md`
- **Phase:** 0C — Scientific Foundations
- **Audit status:** In progress — Gate A passed
- **Purpose:** Preserve explicit evidence for acceptance Gates A–F without conflating draft completion with scientific approval.

## Gate Status Summary

| Gate | Requirement | Status |
|---|---|---|
| A | Physical consistency | PASS |
| B | Mathematical consistency | NOT STARTED |
| C | Dimensional and unit consistency | NOT STARTED |
| D | Software semantic consistency | NOT STARTED |
| E | Hand-calculated reference evidence | NOT STARTED |
| F | Boundary and failure analysis | NOT STARTED |

---

# Gate A — Physical Consistency

## A.1 Audit question

Does ADR-003 represent sensor/receiver imperfections, element response, mutual coupling/loading, timing/synchronization, receiver/ADC effects, calibration, direct measured/EM manifolds, and their covariance/DOA consequences as physically distinct mechanisms with correct causal ordering, reference semantics, and domains of validity while remaining consistent with accepted ADR-001 and ADR-002?

## A.2 Findings that pass

1. **ADR-001 temporal/sign inheritance — PASS.** The governing draft preserves `exp(-j omega t)`, array-to-source look direction, incident propagation direction `-u_hat`, and the accepted receive-manifold sign.
2. **ADR-002 physical delay inheritance — PASS.** A positive physical waveform delay is represented by `x(t-delta_tau)` and transfer factor `exp(+j omega delta_tau)` under the accepted Fourier convention.
3. **Physical delay versus later sampling — PASS.** Delaying a waveform and sampling the same waveform at a later epoch are physically distinct operations and produce the declared opposite tone-phase signs.
4. **Timing taxonomy — PASS.** Static channel phase, physical/electrical delay, fixed sampling-time offset, SRO, jitter, receiver-reference phase/frequency error, and post-acquisition digital latency remain distinct.
5. **Snapshot coherence — PASS.** Differential SRO/CFO and non-simultaneous/TDM acquisition are recognized as possible violations of a fixed simultaneous-equivalent snapshot model rather than hidden in one static phase matrix.
6. **Geometry error as physical position/path error — PASS after A-001 correction.** Physical position is nominal position plus an explicit displacement vector; exact path semantics precede the far-field phase specialization, and phase-reference semantics now match ADR-001.
7. **Rigid translation interpretation — PASS.** A common physical translation can add only a common far-field phase when the fixed nominal phase reference is retained; pairwise/relative spatial phase is unchanged.
8. **Geometry phase versus electronic phase versus delay — PASS.** These remain distinct physical causes.
9. **Element response versus electronic gain — PASS.** Element response may depend on direction, frequency, polarization, orientation, and environment; electronic gain/phase remains receiver/channel response.
10. **Mechanical position versus EM phase center — PASS.** The draft does not assume the electromagnetic phase center is universally identical to the mechanical sensor location.
11. **Polarization semantics — PASS.** Polarization requires an explicit transverse basis consistent with the accepted look/propagation convention.
12. **Mutual coupling physical meaning — PASS.** Coupling is cross-element/cross-port electromagnetic interaction rather than per-channel diagonal gain/phase mismatch.
13. **Multiport loading model — PASS.** Under the declared Thevenin-style specialization, `i=(Z_A+Z_L)^-1 v_oc` and `v_L=Z_L (Z_A+Z_L)^-1 v_oc` have coherent receive-network semantics.
14. **Loaded-port transform semantics — PASS.** `T_L=Z_L (Z_A+Z_L)^-1` is not declared a universal coupling matrix.
15. **Z/S/T_L/C distinction — PASS.** Impedance, scattering, loaded-port, effective coupling, embedded-pattern, and aggregate-manifold objects remain physically distinct; `S21` is not silently used as a DOA coupling coefficient.
16. **Reciprocity versus Hermitian structure — PASS.** Reciprocal/symmetric network structure is not confused with Hermitian covariance structure.
17. **Finite-array structural approximations — PASS.** Toeplitz, circulant, nearest-neighbor, and banded coupling forms require evidence and are not universal finite-array laws.
18. **Embedded/full-wave double-count prevention — PASS.** Effects already included in direct measured/EM/embedded responses cannot be applied again without de-embedding provenance.
19. **Typed physical operator graph — PASS.** Geometry, element response, loading/coupling, electronics, timing/sampling, noise injection, nonlinear response, quantization, and digital selection remain typed domains rather than one generic imperfection matrix.
20. **Reference-plane composition — PASS.** RP-0 through RP-9 semantics preserve physical stage meaning and reject dimension-only composition.
21. **Stage-specific receiver noise — PASS.** Noise is injected at declared stages and transformed only by downstream operators; nonunitary stages can color initially white noise.
22. **Common phase — PASS.** A common phase is not relative spatial distortion and cancels from ordinary covariance in the bounded coherent model.
23. **Common gain nuance — PASS.** Common gain is projectively irrelevant to ideal manifold direction, while physical SNR/dynamic-range effects depend on stage/noise ordering.
24. **ADC acquisition semantics — PASS.** Full scale, quantization, clipping, code mapping, and high-resolution quantization-noise approximation remain physically distinct.
25. **Clipping — PASS.** Clipping is nonlinear information loss and cannot be repaired by later digital scaling.
26. **ADC versus downstream fixed point — PASS.** ADC acquisition quantization is distinct from FPGA/processor arithmetic word-length effects.
27. **DC offset — PASS.** Stable receiver offset can create a rank-one term in an uncentered second moment rather than representing a new propagation source.
28. **I/Q imbalance — PASS.** General conjugate leakage is widely linear and is not silently reduced to ordinary complex gain.
29. **Receiver nonlinearity — PASS.** Compression/intermodulation can violate linear superposition and are not hidden in a fixed linear manifold.
30. **Calibration causal separation — PASS.** Calibration characterizes/estimates/corrects the system; it is not retroactively a physical cause of the original measurement.
31. **Model calibration versus data correction — PASS.** Updating the estimator model and transforming measured data are distinct operations with different statistical consequences.
32. **Inverse correction limits — PASS.** Singular physical response cannot be exactly inverted; pseudoinverse/regularization cannot recreate physically lost null-space information.
33. **Calibration domain/state — PASS.** Calibration validity can depend on frequency, direction, polarization, range, temperature, gain state, clock/LO state, port terminations, hardware revision, and time.
34. **Direct measured/EM manifold semantics — PASS.** Measured and CST/full-wave responses are aggregate evidence/models, not automatically physical truth and not necessarily uniquely decomposable into causes.
35. **Transmit versus receive manifold — PASS.** Transmit far fields are not silently relabeled receive steering vectors without convention-checked reciprocity/normalization transformation.
36. **Calibration-grid gauge — PASS.** Pointwise common phase does not license arbitrary independent phase choices across a calibration grid when interpolation or phase-slope use is required.
37. **Digital channel mask versus physical port state — PASS.** Post-acquisition selection remains distinct from opening, shorting, disabling, or reterminating a physical port that can alter coupling/loading.
38. **MIMO timing/provenance — PASS.** `(Tx_i,Rx_j)` lineage and non-simultaneous TDM phase evolution remain explicit; the initial receive-array profile does not silently claim TDM-MIMO compatibility.
39. **Population mismatch versus finite-sample error — PASS.** Deterministic sensor mismatch can survive infinite snapshots, while finite-sample covariance/eigenspace error remains even after perfect calibration.
40. **Initial Phase-1 physical profile — PASS.** The candidate Phase-1 profile is physically coherent as an ideal bounded sensor chain: nominal=physical geometry, ideal scalar identical elements, no coupling, unity differential electronics, coherent timing/reference, linear no-overload unquantized receiver, and proper-complex white equal-variance additive noise.

---

## A.3 Finding A-001 — Position-error phase reference ambiguity — RESOLVED

### A.3.1 Original issue

The first Gate-A audit found that Section 9 wrote the channel-wise far-field position-error phase as

\[
\delta\phi_n
\approx
-k\hat{\mathbf u}^T
(\boldsymbol\varepsilon_n-\boldsymbol\varepsilon_{\rm ref}),
\]

without first declaring that the phase reference itself had been displaced. This was ambiguous against ADR-001's stable nominal spatial phase-reference semantics.

### A.3.2 Governing correction

The governing ADR now distinguishes two physically different representations.

With the same fixed ADR-001 nominal phase reference for nominal and physical manifolds,

\[
\boxed{
\delta\phi_n^{(\mathrm{fixed\ ref})}
\approx
-k\hat{\mathbf u}^T\boldsymbol\varepsilon_n.
}
\]

Only when a separately displaced phase reference is deliberately defined,

\[
\mathbf r_{\rm ref}^{\rm phys}
=\mathbf r_{\rm ref}^{\rm nom}
+\boldsymbol\varepsilon_{\rm ref},
\]

does the referenced form become

\[
\boxed{
\delta\phi_n^{(\mathrm{moved\ ref})}
\approx
-k\hat{\mathbf u}^T
(\boldsymbol\varepsilon_n-\boldsymbol\varepsilon_{\rm ref}).
}
\]

The reference-invariant pairwise distortion remains

\[
\boxed{
\delta\phi_{nm}
=-k(\boldsymbol\varepsilon_n-\boldsymbol\varepsilon_m)^T\hat{\mathbf u}.
}
\]

### A.3.3 Re-audit checks

1. **Fixed-reference consistency — PASS.** The corrected channel-wise expression follows directly from substituting `r_n^phys=r_n^nom+epsilon_n` while retaining the same ADR-001 `r_ref`.
2. **Moved-reference specialization — PASS.** `epsilon_ref` now appears only when displacement of the comparison reference is separately and explicitly defined.
3. **Rigid-translation invariance — PASS.** For `epsilon_n=t` for every channel, all channels acquire the same common phase `-k u_hat^T t` relative to the fixed nominal reference, while `delta phi_nm=0` for every sensor pair.
4. **Common-phase semantics — PASS.** The correction is consistent with ADR-001's statement that common phase is not relative spatial distortion.
5. **No new physical contradiction — PASS.** The corrected statement does not alter exact-path definitions, pairwise geometry physics, calibration semantics, or Phase-1 scope.

### A.3.4 Resolution status

**RESOLVED — PASS.**

---

## A.4 Documentation-state reconciliation — RESOLVED

The governing ADR's current-disposition metadata was updated during the A-001 correction to record that the pre-Gate review has passed and Gate A is in progress/re-audit state.

This was a documentation synchronization item rather than a physical failure.

**Resolution status: PASS / NON-SCIENTIFIC.**

---

## A.5 Gate A decision

\[
\boxed{\text{Gate A — Physical Consistency: PASS}}
\]

No unresolved physical contradiction remains in ADR-003's declared scope after resolution of A-001.

The Gate-A audit confirms that the governing ADR is physically consistent with accepted ADR-001 and ADR-002 and preserves the required distinctions among geometry, element/polarization response, coupling/loading, electronics, timing/sampling, staged noise, nonlinear/ADC effects, calibration, direct measured/EM manifolds, and estimator-facing consequences.

ADR-003 remains **NOT ACCEPTED** because Gates B–F and final cross-gate reconciliation have not passed.

The next formal work item is:

\[
\boxed{\text{Gate B — Mathematical Consistency}}
\]
