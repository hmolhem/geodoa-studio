# ADR-003 — Acceptance Audit

- **ADR:** `ADR-003-sensor-imperfections-mutual-coupling-calibration.md`
- **Phase:** 0C — Scientific Foundations
- **Audit status:** In progress — Gates A and B passed
- **Purpose:** Preserve explicit evidence for acceptance Gates A–F without conflating draft completion with scientific approval.

## Gate Status Summary

| Gate | Requirement | Status |
|---|---|---|
| A | Physical consistency | PASS |
| B | Mathematical consistency | PASS |
| C | Dimensional and unit consistency | NOT STARTED — NEXT |
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
4. **Timing taxonomy — PASS.** Static channel phase, physical/electrical channel delay, fixed sampling-time offset, SRO, jitter, receiver-reference phase/frequency error, and post-acquisition digital latency remain distinct.
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

---

# Gate B — Mathematical Consistency

## B.1 Audit question

Are the mathematical definitions, matrix operations, exact identities, approximations, perturbation relations, rank/eigenspace statements, calibration formulas, and MUSIC mismatch relations in the governing ADR algebraically correct and stated with appropriate validity conditions?

## B.2 Exact identities and algebra — PASS

1. **Physical-position definition — PASS.** `r_n^phys = r_n^nom + epsilon_n` is algebraically unambiguous.
2. **Exact path perturbation — PASS.** `delta R_n = ||r_s-r_n^phys|| - ||r_s-r_n^nom||` is an exact geometric difference prior to approximation.
3. **Fixed-reference phase perturbation — PASS.** The corrected far-field first-order expression `delta phi_n = -k u_hat^T epsilon_n` is algebraically consistent with the inherited steering exponent.
4. **Moved-reference specialization — PASS.** Explicitly displacing the reference by `epsilon_ref` yields `-k u_hat^T(epsilon_n-epsilon_ref)`.
5. **Pairwise phase perturbation — PASS.** `delta phi_nm = -k(epsilon_n-epsilon_m)^T u_hat` follows by channel-phase subtraction and is reference invariant.
6. **Rigid-translation pairwise invariant — PASS.** Setting every `epsilon_n=t` gives `delta phi_nm=0` exactly.
7. **Gain/phase parameterization — PASS.** `g_n=rho_n exp(j phi_n)` and `G=diag(g_n)` are consistent.
8. **Common phase covariance cancellation — PASS.** `(e^{j phi}a)(e^{j phi}a)^H = aa^H` exactly.
9. **Loaded-port equations — PASS.** Under the declared Thevenin specialization, `i=(Z_A+Z_L)^-1 v_oc`, `v_L=Z_L i`, and `T_L=Z_L(Z_A+Z_L)^-1` are algebraically consistent when the inverse exists.
10. **Physical-delay transfer — PASS.** Under the inherited transform convention, `x(t-delta_tau)` maps to multiplication by `exp(+j omega delta_tau)`.
11. **SRO period relation — PASS.** From `f_s,n=f_s(1+epsilon_f,n)`, the exact sample-period ratio is `1+epsilon_T,n = 1/(1+epsilon_f,n)`; the first-order result `epsilon_T,n ≈ -epsilon_f,n` follows by Taylor expansion.
12. **Later-sampling tone relation — PASS.** For `x(t)=A exp(-j omega t)`, direct substitution gives `x(t+delta t)=x(t)exp(-j omega delta t)`.
13. **Stage-specific linear covariance propagation — PASS.** A covariance component passing through `H` transforms as `H R H^H`; independent downstream noise terms add after the appropriate downstream transforms.
14. **ADC step and high-resolution variance — PASS.** `Delta=V_FSR/2^{N_b}` is the declared ideal nominal code-width convention and `Delta^2/12` is correctly limited to the uniform high-resolution additive-error approximation.
15. **DC-offset second moment — PASS.** For zero-mean signal plus constant `d`, the uncentered second moment gains `d d^H`; cross terms vanish under the stated zero-mean assumption.
16. **Widely-linear model — PASS.** `y=A x+B x*+d` correctly represents an ordinary-plus-conjugate linear response.
17. **Data-correction covariance — PASS.** Fixed linear correction produces `R_corr=C_corr R C_corr^H`; the same congruence applies to the noise covariance that actually passes through the correction.
18. **Pseudoinverse distinction — PASS.** `H^dagger` is not equated with an exact inverse.
19. **Tikhonov form — PASS.** `(H^H H + lambda I)^-1 H^H` is a valid standard regularized left-inverse/least-squares form for declared `lambda>0` or otherwise invertible regularized normal matrix; it is not labeled exact inversion.
20. **Projective scale minimizer — PASS.** For `min_c ||b-ca||_2^2` with nonzero `a`, the stated minimizer `c*=(a^H b)/(a^H a)` is correct.
21. **Normalized coherence — PASS.** `rho=|a^H b|/(||a|| ||b||)` lies in `[0,1]` for nonzero vectors by Cauchy–Schwarz.
22. **Projective angle/leakage — PASS.** `alpha=acos(rho)` and `d_proj^2=1-rho^2` are mathematically consistent for the declared one-dimensional complex-subspace comparison.
23. **Manifold covariance expansion — PASS.** With `A_phys=A+Delta A`, expansion of `(A+Delta A)R_s(A+Delta A)^H` yields exactly the two first-order cross terms plus the quadratic `Delta A R_s Delta A^H` term.
24. **First-order covariance truncation — PASS.** The governing ADR explicitly marks omission of the quadratic term as first order rather than exact.
25. **Sensor/sample covariance bookkeeping — PASS.** `Rhat-R_nom=(R_phys-R_nom)+(Rhat-R_phys)` is an exact identity and does not imply independence.
26. **White-noise eigenvector invariance — PASS.** Adding `sigma^2 I` to a Hermitian signal covariance shifts every eigenvalue equally and leaves its eigenvectors/eigenspaces unchanged.
27. **Whitening transformation — PASS.** For `R_n` Hermitian positive definite, the Hermitian inverse square root exists and consistent transformation of both data and steering vector is mathematically valid.
28. **Weyl-type eigenvalue bound — PASS.** `|lambda_tilde_i-lambda_i| <= ||E||_2` is correct for correspondingly ordered eigenvalues of Hermitian `R` and `R+E`.
29. **Principal-angle/projector semantics — PASS.** The governing text correctly treats principal angles/projector comparisons as subspace quantities rather than basis-column identities.
30. **Rank-one MUSIC leakage identity — PASS.** For unit `u`, `v`, and `P_n=I-u u^H`, `v^H P_n v = 1-|u^H v|^2 = 1-rho^2` exactly.
31. **MUSIC matched population condition — PASS.** With a true steering vector in the signal subspace, `P_n a(theta_k)=0` and the population denominator vanishes under the declared matched classical-MUSIC assumptions.

## B.3 Approximation and bound labeling — PASS

1. **Far-field position phase — PASS.** Labeled a first-order far-field approximation, not an exact near-field identity.
2. **Small SRO relation — PASS.** `epsilon_T≈-epsilon_f` is explicitly separated from the exact reciprocal relation.
3. **Quantization-noise model — PASS.** `Delta^2/12` and the ideal `6.02 N_b + 1.76 dB` SNR relation are explicitly restricted approximations, not universal ADC identities.
4. **Local uncertainty propagation — PASS.** `R_a ≈ J_a P_theta J_a^H` is labeled local/first-order.
5. **Davis–Kahan use — PASS.** The governing ADR states theorem-dependent spectral-gap assumptions and does not promote an informal proportionality to a universal equality.
6. **First-order eigenspace/eigenvector sensitivity — PASS.** Eigenvalue separation/eigengap dependence is correctly treated as perturbative and invalid near unresolved clusters without further care.
7. **MUSIC peak-shift result — PASS.** The draft retains local first-order peak-shift formulas only under smooth isolated nondegenerate peak and small-perturbation assumptions.
8. **Narrowband timing reductions — PASS.** Fixed delay/skew phase specializations are treated as bounded narrowband reductions rather than general broadband identities.

## B.4 Rank, covariance, and subspace consistency — PASS

1. **Rank terminology — PASS.** Source count, source-covariance rank, manifold rank, signal-covariance rank, observed signal-subspace dimension, sample-covariance rank, and selected model order remain mathematically distinct.
2. **Nonsingular congruence rank — PASS.** A nonsingular sensor transform preserves rank of the transformed covariance component while generally changing eigenvectors/eigenvalues.
3. **Rank-deficient transform — PASS.** A singular transform can reduce observable rank.
4. **Time-varying covariance mixture — PASS.** An average/sum of differently oriented low-rank positive-semidefinite matrices can have higher rank than each instantaneous term; the draft correctly avoids replacing this by one averaged static operator in general.
5. **Colored-noise eigenspace statement — PASS.** A non-scalar noise covariance need not commute with signal covariance, so ordinary covariance eigenspaces can rotate.
6. **Augmented statistics — PASS.** The widely-linear/improper case is correctly excluded from an ordinary-covariance-only representation by default.
7. **Projector/basis distinction — PASS.** Subspace comparison is invariant to arbitrary basis rotation within an eigenspace.
8. **Population versus sample eigengap — PASS.** They are retained as distinct quantities and no theorem silently substitutes one for the other.

## B.5 Golden Reference seed arithmetic cross-check — PASS

The reserved Gate-E seeds were independently recomputed during Gate B. This verifies arithmetic consistency only; it does **not** promote them to formal Gate-E evidence.

### GRP-014 seed

For physical spacing `d+delta d`, nominal fitting gives

\[
-kd\hat u=-k(d+\delta d)u_0
\]

so

\[
\boxed{\hat u=(1+\delta d/d)u_0}.
\]

With `u=sin(theta)`, the small-angle first-order conversion is

\[
\boxed{\Delta\theta\approx(\delta d/d)\tan\theta_0}.
\]

**Arithmetic/sign result: PASS.**

### GRP-015 seed

For second-channel electronic phase `phi_e`, nominal fitting gives

\[
-kd\hat u=-kdu_0+\phi_e
\]

and therefore

\[
\boxed{\Delta u=-\phi_e/(kd)}.
\]

For `d=lambda/2`, `kd=pi`, so

\[
\boxed{\Delta u=-\phi_e/\pi}.
\]

**Arithmetic/sign result: PASS.**

### GRP-016 seed

With

\[
\mathbf a=\begin{bmatrix}1\\-j\end{bmatrix},
\qquad
\mathbf C=\begin{bmatrix}1&0.5\\0.5&1\end{bmatrix},
\]

\[
\boxed{\mathbf b=C a=\begin{bmatrix}1-0.5j\\0.5-j\end{bmatrix}}.
\]

Also

\[
\boxed{b_2/b_1=0.8-0.6j}
\]

with phase approximately `-36.8698976 deg`.

Under nominal half-wave phase matching this yields the previously reserved inferred direction-cosine seed approximately

\[
\boxed{\hat u\approx0.20483}.
\]

**Arithmetic result: PASS.**

### GRP-017 seed

\[
\boxed{
\mathbf R_{\rm sig}=bb^H
=\begin{bmatrix}
1.25&1+0.75j\\
1-0.75j&1.25
\end{bmatrix}}
\]

has eigenvalues

\[
\boxed{\{2.5,0\}}.
\]

Adding `I` gives

\[
\boxed{\{3.5,1\}}.
\]

The squared normalized alignment is

\[
\boxed{\rho^2=0.8}
\]

and the normalized rank-one orthogonal/noise-subspace leakage is

\[
\boxed{1-\rho^2=0.2}.
\]

**Arithmetic/eigenstructure result: PASS.**

## B.6 Non-blocking mathematical notes for later gates

1. Gate C shall explicitly audit units and dimensional compatibility of `k`, position vectors, delays, frequencies, ADC voltages, covariance quantities, and regularization/scaling parameters.
2. Gate D shall ensure software shapes/types encode the matrix-domain assumptions audited here rather than allowing mathematically valid but semantically incompatible multiplication.
3. Gate E shall independently formalize the GRP inputs, expected outputs, tolerances, and deterministic verification procedure; the Gate-B arithmetic check is not Gate-E PASS evidence.
4. Gate F shall exercise zero vectors, singular/near-singular matrices, undefined projective metrics, calibration nulls, clipping, and eigengap collapse where formulas become undefined or perturbation approximations lose validity.
5. The governing ADR top-level status line still describes acceptance gates generically as not completed; final status metadata shall be synchronized as gates progress. This is documentation state, not a mathematical failure.

## B.7 Blocking findings

```text
Algebraic contradiction:                    NONE FOUND
Incorrect conjugation/transposition:        NONE FOUND
Exact relation mislabeled approximation:    NONE FOUND
Approximation mislabeled exact identity:    NONE FOUND
Rank/eigenspace contradiction:              NONE FOUND
MUSIC projector identity error:             NONE FOUND
GRP-014–017 arithmetic inconsistency:        NONE FOUND
```

## B.8 Gate B decision

\[
\boxed{\text{Gate B — Mathematical Consistency: PASS}}
\]

No unresolved mathematical contradiction remains in the governing ADR's declared scope.

Gate B confirms that the retained exact identities, approximations, perturbation statements, covariance congruences, rank/eigenspace statements, calibration formulas, and MUSIC relations are mathematically coherent under their declared assumptions.

ADR-003 remains **NOT ACCEPTED** because Gates C–F and final cross-gate reconciliation have not passed.

The next formal work item is:

\[
\boxed{\text{Gate C — Dimensional and Unit Consistency}}
\]
