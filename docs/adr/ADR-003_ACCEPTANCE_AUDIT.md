# ADR-003 — Acceptance Audit

- **ADR:** `ADR-003-sensor-imperfections-mutual-coupling-calibration.md`
- **Phase:** 0C — Scientific Foundations
- **Audit status:** In progress
- **Purpose:** Preserve explicit evidence for acceptance Gates A–F without conflating draft completion with scientific approval.

## Gate Status Summary

| Gate | Requirement | Status |
|---|---|---|
| A | Physical consistency | NEEDS CORRECTION — A-001 |
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
3. **Physical delay versus later sampling — PASS.** The draft correctly distinguishes delaying the waveform from observing the same waveform at a later sampling epoch; for `exp(-j omega t)` these operations produce opposite phase signs.
4. **Timing taxonomy — PASS.** Static channel phase, physical/electrical delay, fixed sampling-time offset, SRO, jitter, receiver-reference phase/frequency error, and post-acquisition digital latency are physically distinct.
5. **Snapshot coherence — PASS.** Differential SRO/CFO and non-simultaneous/TDM acquisition are recognized as potential violations of a fixed simultaneous-equivalent snapshot model rather than hidden inside one static phase matrix.
6. **Geometry error as physical position/path error — PASS except Finding A-001.** Physical position is nominal position plus an explicit displacement vector; exact path semantics precede far-field phase specialization.
7. **Rigid translation interpretation — PASS.** A common physical translation can add only a common far-field phase when a fixed nominal phase reference is retained; it does not alter pairwise/relative spatial phase and therefore is not relative-manifold distortion.
8. **Geometry phase versus electronic phase versus delay — PASS.** These are retained as distinct physical causes and are not silently interchanged.
9. **Element response versus electronic gain — PASS.** Element response may depend on direction, frequency, polarization, orientation, and environment; electronic gain/phase remains a receiver/channel response.
10. **Mechanical position versus EM phase center — PASS.** The draft does not assume an immutable electromagnetic phase center identical to the mechanical sensor location.
11. **Polarization semantics — PASS.** Polarization requires an explicit transverse basis and remains tied to the accepted look/propagation-direction convention.
12. **Mutual coupling physical meaning — PASS.** Coupling is treated as cross-element/cross-port electromagnetic interaction rather than diagonal per-channel gain/phase mismatch.
13. **Multiport loading model — PASS.** Under the declared Thevenin-style specialization, `i=(Z_A+Z_L)^-1 v_oc` and `v_L=Z_L (Z_A+Z_L)^-1 v_oc` have a physically coherent receive-network interpretation.
14. **Loaded-port transform semantics — PASS.** `T_L=Z_L (Z_A+Z_L)^-1` is explicitly not declared a universal DOA coupling matrix.
15. **Z/S/T_L/C distinction — PASS.** Impedance, scattering, loaded-port, effective coupling, embedded-pattern, and aggregate-manifold quantities are not physically conflated; `S21` is not silently inserted as a steering-manifold coupling coefficient.
16. **Reciprocity versus Hermitian structure — PASS.** Reciprocal/symmetric network structure is not confused with Hermitian covariance structure.
17. **Finite-array structural approximations — PASS.** Toeplitz, circulant, nearest-neighbor, and banded coupling forms are treated as evidence-dependent approximations rather than universal finite-array laws.
18. **Embedded/full-wave double-count prevention — PASS.** Element, coupling, radome/platform, feed, receiver, cable, or fixture effects already contained in a direct measured/EM response cannot be applied again without explicit de-embedding provenance.
19. **Typed physical operator graph — PASS.** Geometry, element response, network/loading, electronics, timing/sampling, noise injection, nonlinear response, quantization, and digital selection are typed physical domains rather than one generic imperfection matrix.
20. **Reference-plane composition — PASS.** Conceptual RP-0 through RP-9 semantics prevent composition based only on array dimensions and preserve physical stage meaning.
21. **Stage-specific receiver noise — PASS.** Noise is injected at declared physical stages and transformed only by downstream operators; pre-coupling or pre-correction white noise can become colored under nonunitary transformations.
22. **Common phase — PASS.** A common phase factor does not constitute spatial distortion and cancels from ordinary covariance under the bounded coherent model.
23. **Common gain nuance — PASS.** Common gain is projectively irrelevant to ideal manifold direction, while SNR/dynamic-range consequences depend on where gain and noise/nonlinear/ADC stages occur physically.
24. **ADC acquisition semantics — PASS.** ADC full scale, quantization, clipping, code mapping, and high-resolution quantization-noise approximation are distinguished physically.
25. **Clipping — PASS.** Clipping is treated as nonlinear information loss and cannot be repaired by later digital scaling.
26. **ADC versus downstream fixed point — PASS.** Acquisition quantization is physically separate from FPGA/processor arithmetic word-length effects.
27. **DC offset — PASS.** Stable offset is treated as a receiver effect that can create a rank-one term in an uncentered second moment rather than a new propagation source.
28. **I/Q imbalance — PASS.** General conjugate leakage is modeled as a widely-linear receiver effect and is not silently reduced to ordinary complex gain.
29. **Receiver nonlinearity — PASS.** Compression/intermodulation are recognized as potential violations of linear superposition rather than hidden linear manifold distortions.
30. **Calibration causal separation — PASS.** Calibration characterizes/estimates/corrects the physical system; it is not inserted retroactively as a physical cause in the original forward measurement chain.
31. **Model calibration versus data correction — PASS.** Updating the estimator manifold and transforming measured data are physically/statistically distinct operations.
32. **Inverse correction limits — PASS.** Singular physical response cannot be exactly inverted; pseudoinverse/regularization does not create physically lost information.
33. **Calibration domain/state — PASS.** Calibration validity is allowed to depend on frequency, direction, polarization, range, temperature, gain state, clock/LO state, port terminations, hardware revision, and time.
34. **Direct measured/EM manifold semantics — PASS.** Measured and CST/full-wave responses are aggregate response models/evidence, not automatically physical truth and not automatically uniquely decomposable into causes.
35. **Transmit versus receive manifold — PASS.** Transmit far fields are not silently relabeled as receive steering vectors without a convention-checked reciprocity/normalization transformation.
36. **Calibration-grid gauge — PASS.** Pointwise common phase does not license arbitrary independent phase normalization at every grid node when interpolation or phase-slope behavior is required.
37. **Digital channel mask versus physical port state — PASS.** Post-acquisition selection is distinguished from opening, shorting, disabling, or reterminating a physical port that can change array coupling/loading.
38. **MIMO timing/provenance — PASS.** Physical `(Tx_i,Rx_j)` lineage and non-simultaneous TDM phase evolution remain explicit; the Phase-1 receive-array profile does not silently claim TDM-MIMO compatibility.
39. **Population mismatch versus finite-sample error — PASS.** Deterministic sensor mismatch can survive infinite snapshots, while finite-sample covariance/eigenspace error remains even after perfect calibration.
40. **Initial Phase-1 physical profile — PASS.** The candidate Phase-1 profile is physically coherent as an ideal bounded sensor chain: nominal=physical geometry, ideal scalar identical elements, no coupling, unity differential electronics, coherent timing/reference, linear no-overload unquantized receiver, and proper-complex white equal-variance additive noise.

---

## A.3 Finding A-001 — Position-error phase reference ambiguity — NEEDS CORRECTION

### A.3.1 Current governing-draft statement

Section 9 currently gives the far-field first-order phase perturbation as

```math
\delta\phi_n
\approx
-k\hat{\mathbf u}^T
(\boldsymbol\varepsilon_n-\boldsymbol\varepsilon_{\rm ref}).
```

while the same governing draft inherits ADR-001's stable nominal spatial phase-reference semantics.

### A.3.2 Physical issue

ADR-001's default spatial phase reference is tied to the declared nominal geometry and is intentionally stable rather than silently following sensor perturbations or active subsets.

If the physical sensor position is

```math
\mathbf r_n^{\rm phys}
=\mathbf r_n^{\rm nom}+\boldsymbol\varepsilon_n
```

and the same fixed nominal phase reference `r_ref` is used for nominal and physical manifolds, then

```math
a_n^{\rm nom}
=\exp[-jk(\mathbf r_n^{\rm nom}-\mathbf r_{\rm ref})^T\hat{\mathbf u}],
```

```math
a_n^{\rm phys}
=\exp[-jk(\mathbf r_n^{\rm nom}+\boldsymbol\varepsilon_n-\mathbf r_{\rm ref})^T\hat{\mathbf u}],
```

so the channel-wise perturbation relative to that fixed reference is

```math
\boxed{
\delta\phi_n^{(\mathrm{fixed\ ref})}
=-k\hat{\mathbf u}^T\boldsymbol\varepsilon_n.
}
```

The pairwise/reference-invariant relative distortion remains

```math
\boxed{
\delta\phi_{nm}
=-k(\boldsymbol\varepsilon_n-\boldsymbol\varepsilon_m)^T\hat{\mathbf u}.
}
```

For a common rigid translation `epsilon_n=t`, every channel acquires the same common phase

```math
-k\hat{\mathbf u}^T\mathbf t,
```

so pairwise relative phase is unchanged. This exactly preserves ADR-001's rule that common phase is not spatial distortion.

The expression

```math
-k\hat{\mathbf u}^T
(\boldsymbol\varepsilon_n-\boldsymbol\varepsilon_{\rm ref})
```

is valid only if a separate displacement `epsilon_ref` of the chosen phase-reference point is explicitly defined, e.g. when comparing manifolds expressed relative to a deliberately moved physical/calibrated reference. It shall not be written as though ADR-001's stable nominal `r_ref` automatically acquires a physical perturbation.

### A.3.3 Required governing-draft correction

Replace the current Section 9 far-field paragraph with a two-level statement:

```markdown
Under the far-field first-order approximation, when nominal and physical
manifolds use the same fixed ADR-001 spatial phase reference,

\[
\boxed{
\delta\phi_n^{(\mathrm{fixed\ ref})}
\approx
-k\hat{\mathbf u}^T\boldsymbol\varepsilon_n.
}
\]

If a comparison deliberately uses a separately displaced phase reference
\(\mathbf r_{\rm ref}^{\rm phys}=\mathbf r_{\rm ref}^{\rm nom}
+\boldsymbol\varepsilon_{\rm ref}\), then the corresponding referenced
perturbation is

\[
\boxed{
\delta\phi_n^{(\mathrm{moved\ ref})}
\approx
-k\hat{\mathbf u}^T
(\boldsymbol\varepsilon_n-\boldsymbol\varepsilon_{\rm ref}).
}
\]

The reference-invariant pairwise distortion is

\[
\boxed{
\delta\phi_{nm}
=-k(\boldsymbol\varepsilon_n-\boldsymbol\varepsilon_m)^T\hat{\mathbf u}.
}
\]
```

Then retain the existing statement that rigid translation produces no far-field **relative-manifold** distortion.

### A.3.4 Materiality

**Material physical/reference-semantic ambiguity.** The pairwise physics and rigid-translation conclusion are already correct, so no scientific program redesign is required. However, the channel-wise formula as currently written can be misread as moving ADR-001's stable reference and therefore must be corrected before Gate A can PASS.

### A.3.5 Resolution status

**NEEDS CORRECTION.**

---

## A.4 Non-blocking documentation note — current-disposition metadata

The governing ADR's final `Current Disposition` block still says `Pre-Gate consistency review: NEXT`, although `ADR-003_PRE_GATE_CONSISTENCY_REVIEW.md` records `PRE-GATE REVIEW PASS — GATE A MAY BEGIN`.

This is a repository-status synchronization issue, not a physical inconsistency. It shall be reconciled when the governing draft is next edited.

**Gate-A materiality:** NON-BLOCKING.

---

## A.5 Gate A decision

```text
Gate A — Physical Consistency: NEEDS CORRECTION
Blocking/resolution finding: A-001
All other audited physical mechanisms: PASS
```

Gate A shall be promoted to **PASS** only after:

1. the governing ADR Section 9 phase-reference formula is corrected as specified in A-001;
2. the corrected text is re-audited against ADR-001 stable-reference semantics and the pairwise rigid-translation invariant;
3. no new physical contradiction is introduced by that correction.

ADR-003 remains **NOT ACCEPTED**.

Gate B shall not start until Gate A is resolved and marked PASS.
