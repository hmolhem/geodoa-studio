# ADR-003 — Exploration Checkpoint

- **Working title:** Sensor Imperfections, Mutual Coupling, and Calibration
- **Phase:** 0C — Scientific Foundations
- **Status:** EXPLORATION IN PROGRESS — NOT ACCEPTED
- **Branch:** `docs/phase0c-scientific-conventions`
- **Depends on:** `ADR-001-coordinate-direction-spatial-conventions.md`, `ADR-002-wave-propagation-signal-measurement-model.md`, `PHASE0C_SCIENTIFIC_CONTRACTS_ROADMAP.md`
- **Completed exploration sections:** 3.1, 3.2, 3.3, 3.4
- **Next exploration section:** 3.5 — Mutual Coupling
- **Acceptance gates:** Not started for ADR-003
- **Reserved Golden Reference Problems:** GRP-014 through GRP-017

> This document is a continuation checkpoint, not the governing accepted ADR. Candidate decisions below remain subject to reconciliation, Gates A–F, Golden Reference evidence, boundary/failure analysis, cross-ADR audit, and final acceptance.

---

## 1. Purpose

ADR-003 answers the question:

> How does the real sensor system depart from the ideal array model, and how are those departures represented, measured, calibrated, and propagated into DOA performance?

The central modeling transition is

\[
\boxed{
\text{Nominal propagation response}
\rightarrow
\text{physical sensor-system response}
\rightarrow
\text{calibrated processing model}
}
\]

ADR-003 must preserve physical causality and provenance. A real-sensor effect must not be collapsed into an arbitrary phase/gain perturbation merely because that is numerically convenient.

The scientific chain to preserve is

\[
\boxed{
\text{Physical cause}
\rightarrow
\text{measurement/manifold distortion}
\rightarrow
\text{covariance distortion}
\rightarrow
\text{eigenspace/subspace distortion}
\rightarrow
\text{DOA consequence}
}
\]

and, separately,

\[
\boxed{
\text{Calibration experiment/model}
\rightarrow
\text{estimated correction/manifold}
\rightarrow
\text{residual mismatch}
\rightarrow
\text{post-calibration DOA performance}
}
\]

---

## 2. Planned ADR-003 Exploration Sequence

```text
3.1  Ideal / Physical / Calibrated Manifold                 COMPLETE
3.2  Position Error and Geometry Perturbation                COMPLETE
3.3  Gain and Phase Mismatch                                 COMPLETE
3.4  Element Pattern and Polarization                        COMPLETE
3.5  Mutual Coupling                                         NEXT
3.6  Channel Delay, Clock Skew, and Frequency Error          PENDING
3.7  Quantization / Receiver / Dynamic-Range Effects         PENDING
3.8  Unified Sensor-Imperfection Operator                    PENDING
3.9  Calibration Models                                      PENDING
3.10 Direct Measured / CST-Derived Manifold Calibration      PENDING
3.11 Error Metrics and Identifiability                       PENDING
3.12 Covariance / Eigenspace / MUSIC Error Propagation       PENDING
3.13 Compatibility and Initial ADR-003 Profile               PENDING
3.14 Cross-Consistency Audit                                 PENDING
```

After exploration 3.14, ADR-003 must enter the standard Phase 0C acceptance sequence:

```text
Gate A — Physical Consistency
Gate B — Mathematical Consistency
Gate C — Dimensional and Unit Consistency
Gate D — Software Semantic Consistency
Gate E — Hand-Calculated Reference Evidence
Gate F — Boundary and Failure Analysis
        ↓
Final cross-gate reconciliation
        ↓
ACCEPTED only if all gates PASS
```

---

# 3. Exploration 3.1 — Ideal / Physical / Calibrated Manifold

## 3.1.1 Core taxonomy

GeoDOA must not use a single ambiguous concept called simply `steering_vector` for every scientific response.

The following meanings are distinct:

\[
\boxed{\mathbf a_{\rm nom}}
\]

**Nominal Manifold** — expected response from declared geometry, propagation model, and nominal sensor assumptions.

\[
\boxed{\mathbf a_{\rm phys}}
\]

**Physical Manifold** — actual response of the physical sensor system under a specified physical condition.

\[
\boxed{\mathbf a_{\rm meas}}
\]

**Measured Manifold** — experimental estimate of the physical response.

\[
\boxed{\mathbf a_{\rm em}}
\]

**EM-Simulated Manifold** — response predicted by an electromagnetic/full-wave model such as CST under declared simulation conditions.

\[
\boxed{\mathbf a_{\rm cal}}
\]

**Calibrated Processing Manifold** — response model deliberately selected or estimated for downstream processing after calibration.

In simulation, an exact declared truth manifold may additionally exist:

\[
\boxed{\mathbf a_{\rm truth}}
\]

Physical reality and a measured/calibrated estimate of physical reality are not the same scientific object.

## 3.1.2 Sensor-system transformation

Conceptually,

\[
\mathbf a_{\rm phys}
=
\mathcal H_{\rm sensor}[\mathbf a_{\rm nom}].
\]

The sensor-system transformation is not generally diagonal. Mutual coupling is explicitly a cross-channel effect.

For generated data,

\[
\mathbf x[k]
=
\mathbf A_{\rm phys}\mathbf s[k]+\mathbf n[k],
\]

while the estimator may use a different model,

\[
\mathbf A_{\rm model}
\in
\{\mathbf A_{\rm nom},\mathbf A_{\rm cal},\ldots\}.
\]

Thus model mismatch is a mismatch between the physical data-generating response and the response used by the estimator.

## 3.1.3 Calibration semantics

Calibration is not part of the forward propagation chain. It is an inverse/model-estimation/correction activity.

Forward system:

```text
Source / target
    ↓
Propagation
    ↓
Physical geometry
    ↓
Element / receiver response
    ↓
Cross-channel effects
    ↓
Measurement
```

Calibration activity:

```text
Calibration experiment / model
    ↓
Estimate sensor-system parameters or manifold
    ↓
Construct processing manifold and/or correction
    ↓
Residual calibration error
```

Model calibration and data correction are distinct operations. For example, if

\[
\mathbf x=\mathbf G\mathbf a s+\mathbf n,
\]

one may either use

\[
\mathbf a_{\rm cal}=\hat{\mathbf G}\mathbf a,
\]

or correct data with

\[
\mathbf x_{\rm corr}=\hat{\mathbf G}^{-1}\mathbf x.
\]

The second operation also transforms noise statistics and can amplify noise.

## 3.1.4 Calibration domain and provenance

Calibration is not a universal correction. Validity may depend on frequency, direction, polarization, temperature, array configuration, active-channel state, platform state, reference convention, and other conditions.

Calibration artifacts therefore require domain metadata and provenance.

## 3.1.5 Common-phase / common-scale alignment

A generic `manifold_error` is scientifically incomplete unless its equivalence class is declared.

Examples include phase-only alignment,

\[
\min_\phi\|\mathbf a_2-e^{j\phi}\mathbf a_1\|,
\]

and common complex-scale alignment,

\[
\min_{c\in\mathbb C}\|\mathbf a_2-c\mathbf a_1\|.
\]

These metrics answer different engineering questions.

## 3.1.6 Candidate decisions from Exploration 3.1

- **3.1-D1** — Nominal, physical, measured, EM-simulated, calibrated, and simulation-truth manifolds are distinct scientific meanings.
- **3.1-D2** — Physical manifold may exist without being exactly known; measured/calibrated responses are estimates or processing models, not physical truth by definition.
- **3.1-D3** — Sensor imperfections enter between nominal propagation response and observed sensor-system response.
- **3.1-D4** — Calibration is not a forward physical-propagation block.
- **3.1-D5** — Per-channel gain/phase mismatch and mutual coupling must not be collapsed into one model family.
- **3.1-D6** — Geometry perturbation belongs to geometry/path semantics, not arbitrary phase-noise semantics.
- **3.1-D7** — Parametric calibration and direct measured/EM manifold calibration are separate strategies.
- **3.1-D8** — Calibration requires declared domain and provenance.
- **3.1-D9** — Model calibration and data correction remain separate scientific operations.
- **3.1-D10** — Inverse calibration may transform noise covariance and create noise/numerical amplification.
- **3.1-D11** — Calibration quality must propagate beyond manifold error into covariance, eigenspace, and DOA performance.
- **3.1-D12** — Common phase, common complex scale, and physically meaningful amplitude mismatch use different equivalence semantics.
- **3.1-D13** — Measurement noise, structured interference, and systematic sensor imperfection are different phenomena.
- **3.1-D14** — Imperfection parameter distribution and realized physical imperfection are different scientific objects.
- **3.1-D15** — APIs must not silently switch among nominal/physical/measured/calibrated response meanings through hidden flags.

---

# 4. Exploration 3.2 — Position Error and Geometry Perturbation

## 4.1 Authoritative geometry representation

Physical sensor position is represented as

\[
\boxed{
\mathbf r_n^{\rm phys}
=
\mathbf r_n^{\rm nom}+\boldsymbol\varepsilon_n
}
\]

with \(\boldsymbol\varepsilon_n\) expressed in physical length units and an explicit frame.

A nominal one-dimensional array may have three-dimensional physical placement error.

## 4.2 Exact and first-order path perturbation

For source position \(\mathbf r_s\),

\[
R_n^{\rm nom}=\|\mathbf r_s-\mathbf r_n^{\rm nom}\|,
\qquad
R_n^{\rm phys}=\|\mathbf r_s-\mathbf r_n^{\rm phys}\|.
\]

The exact path perturbation is

\[
\delta R_n=R_n^{\rm phys}-R_n^{\rm nom}.
\]

With local look direction \(\hat{\mathbf u}_n\), the first-order perturbation is

\[
\boxed{
\delta R_n
\approx
-\hat{\mathbf u}_n^T\boldsymbol\varepsilon_n
}
\]

and in the far field the relative phase perturbation becomes

\[
\boxed{
\delta\phi_n
\approx
-k\hat{\mathbf u}^T
(\boldsymbol\varepsilon_n-\boldsymbol\varepsilon_{\rm ref})
}.
\]

A reference-free pairwise form is

\[
\boxed{
\delta\phi_{nm}
=
-k(\boldsymbol\varepsilon_n-\boldsymbol\varepsilon_m)^T\hat{\mathbf u}
}.
\]

## 4.3 Consequences

Position error is fundamentally a geometry/path error. Phase error is a derived, direction- and frequency-dependent consequence.

A common rigid translation has

\[
\boldsymbol\varepsilon_n=\mathbf t
\quad\forall n,
\]

so pairwise phase distortion vanishes. Internal deformation, array pose error, and element orientation error are different phenomena and must not be collapsed.

For exact spherical propagation, position error can change both phase and amplitude; phase-only perturbation is a far-field/relative-model specialization.

## 4.4 Covariance propagation

For a single-source diagonal phase perturbation \(\mathbf D_\varepsilon\),

\[
\mathbf R_{\rm sig}^{\rm phys}
=
\mathbf D_\varepsilon
\mathbf R_{\rm sig}^{\rm nom}
\mathbf D_\varepsilon^H.
\]

For small phase errors, with \(\mathbf\Phi=\operatorname{diag}(\delta\phi_n)\),

\[
\boxed{
\Delta\mathbf R
\approx
j(\mathbf\Phi\mathbf R-\mathbf R\mathbf\Phi)
}.
\]

The perturbation is structured, not additive white noise.

## 4.5 Two-sensor DOA-bias relation

For nominal spacing \(d\), true physical spacing \(d+\delta d\), and \(u_0=\sin\theta_0\), a nominal phase-matching estimator gives

\[
\boxed{
\hat u
=
\left(1+\frac{\delta d}{d}\right)u_0
}
\]

and, for small errors,

\[
\boxed{
\Delta\theta
\approx
\frac{\delta d}{d}\tan\theta_0
}.
\]

This relationship is a basis for GRP-014.

## 4.6 Calibration and identifiability

A calibrated estimate of physical position must not destructively overwrite nominal design geometry.

\[
\hat{\mathbf r}_n^{\rm phys}
=
\mathbf r_n^{\rm nom}+\hat{\boldsymbol\varepsilon}_n,
\]

with residual error

\[
\boldsymbol\varepsilon_n^{\rm res}
=
\boldsymbol\varepsilon_n-\hat{\boldsymbol\varepsilon}_n.
\]

Common translation may be unobservable from relative far-field phase. A single calibration direction generally observes only projections of position error. Geometry error and DOA may therefore be partially confounded.

Manufacturing tolerance, a stochastic uncertainty distribution, and a realized physical error are separate meanings.

## 4.7 Candidate decisions from Exploration 3.2

- **3.2-D1** — Physical position equals nominal position plus an explicit position-error vector in physical units and a declared frame.
- **3.2-D2** — Nominal 1-D geometry may have physical 3-D placement deviations.
- **3.2-D3** — Position error is first a geometry/path perturbation; phase error is derived.
- **3.2-D4** — Exact path perturbation precedes far-field approximations.
- **3.2-D5** — First-order far-field relative phase follows the declared ADR-001/ADR-002 sign chain.
- **3.2-D6** — Pairwise geometry distortion is a reference-invariant scientific representation.
- **3.2-D7** — Common rigid translation is not far-field relative-manifold distortion.
- **3.2-D8** — Rigid-body pose/frame error and internal geometry deformation are distinct.
- **3.2-D9** — Position-error sensitivity is direction- and frequency-dependent.
- **3.2-D10** — Broadside immunity is conditional on perturbation direction and propagation approximation.
- **3.2-D11** — Exact/near-field position perturbations may alter amplitude as well as phase.
- **3.2-D12** — Fixed physical error, uncertainty distribution, and manufacturing tolerance are separate.
- **3.2-D13** — Calibrated physical geometry must preserve nominal-design provenance.
- **3.2-D14** — Residual calibrated position error must be representable.
- **3.2-D15** — Dynamic deformation may invalidate quasi-static manifold assumptions within a covariance window.
- **3.2-D16** — Geometry calibration has observability and identifiability limits.
- **3.2-D17** — \(\varepsilon/\lambda\) is a derived frequency-dependent quantity, not a replacement for physical error in meters.
- **3.2-D18** — Position-error covariance distortion is structured and must not be modeled as additive white noise by default.

---

# 5. Exploration 3.3 — Gain and Phase Mismatch

## 5.1 Complex per-channel response

A narrowband per-channel complex response is

\[
\boxed{
g_n=\rho_n e^{j\phi_n}
}
\]

and the diagonal response operator is

\[
\boxed{
\mathbf G=\operatorname{diag}(g_1,\ldots,g_N)
}.
\]

Thus

\[
\boxed{
\mathbf a_{\rm gp}=\mathbf G\mathbf a_{\rm nom}
}.
\]

This diagonal channel model is fundamentally different from cross-channel mutual coupling.

## 5.2 Common versus relative mismatch

If \(\mathbf G=c\mathbf I\), the physical manifold differs by a common complex scale. Common phase does not constitute spatial distortion; common gain can change absolute amplitude/power and received SNR even when a normalized subspace direction is unchanged.

For a declared reference channel,

\[
\tilde g_n=\frac{g_n}{g_r}
=
\frac{\rho_n}{\rho_r}e^{j(\phi_n-\phi_r)}.
\]

The reference response must be nonzero and sufficiently conditioned for ratio normalization.

## 5.3 Small-error perturbation

For

\[
\rho_n=1+\alpha_n,
\qquad
|\alpha_n|\ll1,
\qquad
|\phi_n|\ll1,
\]

\[
\boxed{
g_n\approx1+\alpha_n+j\phi_n
}.
\]

This is a perturbation approximation only.

An arbitrary electronic phase mismatch is not equivalent to a position-induced phase error. A constant narrowband phase offset is also not equivalent to a physical channel-delay mismatch, which creates a frequency-dependent phase slope.

## 5.4 Covariance propagation

For

\[
\mathbf x
=
\mathbf G\mathbf A\mathbf s+\mathbf n,
\]

\[
\mathbf R_{\rm sig}^{\rm phys}
=
\mathbf G\mathbf R_{\rm sig}^{\rm nom}\mathbf G^H.
\]

Elementwise,

\[
[R_{\rm sig}^{\rm phys}]_{nm}
=
[R_{\rm sig}^{\rm nom}]_{nm}
\rho_n\rho_m e^{j(\phi_n-\phi_m)}.
\]

Common phase cancels from covariance exactly. A common gain scales the signal covariance without rotating the simple signal-subspace direction.

## 5.5 Noise ordering and inverse correction

The placement of gain/response blocks relative to noise injection is scientifically material.

If data correction uses \(\mathbf G^{-1}\), then even initially white noise may become unequal-variance/colored:

\[
\mathbf R_{n,\rm corr}
=
\mathbf G^{-1}\mathbf R_n\mathbf G^{-H}.
\]

Near-zero gains make inverse correction ill-conditioned; a zero-response/dead channel cannot be recovered by multiplicative inversion.

## 5.6 Two-sensor phase-error DOA bias

For a two-sensor array,

\[
\mathbf a_{\rm nom}(u)
=
\begin{bmatrix}
1\\e^{-jkdu}
\end{bmatrix},
\]

and a relative phase error \(\phi_e\) on the second channel gives

\[
\boxed{
\hat u=u_0-\frac{\phi_e}{kd}
}.
\]

For \(d=\lambda/2\),

\[
\boxed{
\Delta u=-\frac{\phi_e}{\pi}
}.
\]

This relation is a basis for GRP-015.

## 5.7 Identifiability

Relative gain/phase calibration may be identifiable even if an absolute common gain/phase is not identifiable from array data alone. Calibration must declare whether it is absolute, relative, gain-only, phase-only, or gain-plus-phase.

## 5.8 Candidate decisions from Exploration 3.3

- **3.3-D1** — Per-channel narrowband response uses a complex coefficient \(g_n=\rho_ne^{j\phi_n}\).
- **3.3-D2** — Pure gain/phase mismatch is represented by a diagonal transformation.
- **3.3-D3** — Common gain, common phase, and relative gain/phase mismatch are separate concepts.
- **3.3-D4** — Common phase is not spatial-manifold distortion.
- **3.3-D5** — Common gain may be projectively irrelevant for some DOA tasks while remaining relevant to calibrated amplitude/power.
- **3.3-D6** — Relative response requires explicit reference or pairwise semantics.
- **3.3-D7** — Near-zero reference response invalidates or ill-conditions relative normalization.
- **3.3-D8** — Gain dB semantics must distinguish amplitude and power ratios.
- **3.3-D9** — Small-error gain/phase linearization is an approximation, not a replacement for the physical complex response.
- **3.3-D10** — Arbitrary channel phase mismatch and position-induced phase error remain distinct physical models.
- **3.3-D11** — Constant narrowband phase offset and channel-delay mismatch remain distinct.
- **3.3-D12** — Response/noise ordering must be explicit.
- **3.3-D13** — Declared multiplicative channel response propagates into covariance as \(G R G^H\).
- **3.3-D14** — Common phase cancels in covariance; simple common gain scales signal covariance.
- **3.3-D15** — Relative gain/phase mismatch may rotate the physical signal subspace and break nominal MUSIC orthogonality.
- **3.3-D16** — Inverse data correction transforms noise covariance and may amplify noise.
- **3.3-D17** — Zero-gain/dead channels require separate channel-state handling, not impossible inverse calibration.
- **3.3-D18** — Residual complex-response error must be representable after calibration.
- **3.3-D19** — Relative calibration may be identifiable when absolute common gain/phase is not.
- **3.3-D20** — Channel response may depend on frequency, temperature, time, and configuration; calibration domain/provenance must preserve this.
- **3.3-D21** — Electronic channel response, element pattern, and mutual coupling remain distinct model families.
- **3.3-D22** — A diagonal fit to a coupled system at one operating point is not evidence of diagonal physical coupling.
- **3.3-D23** — Stochastic mismatch assumptions are separate from realized physical mismatch and calibration uncertainty.

---

# 6. Exploration 3.4 — Element Pattern and Polarization

## 6.1 Point sensor versus physical element

An element is not merely a spatial sample point. Its coherent receive response may depend on direction, frequency, polarization, orientation, and environment.

For an uncoupled scalar-element specialization,

\[
\boxed{
b_n=b_n(\hat{\mathbf u},f,\mathbf p,\ldots)
}
\]

and

\[
\boxed{
\mathbf P(\hat{\mathbf u},f,\mathbf p)
=
\operatorname{diag}(b_1,\ldots,b_N)
}
\]

so that

\[
\boxed{
\mathbf a_{\rm elem}
=
\mathbf P\mathbf a_{\rm geom}
}.
\]

Element response is generally complex:

\[
b_n=\rho_n e^{j\psi_n}.
\]

A magnitude-only radiation pattern is therefore insufficient for phase-coherent manifold calibration.

## 6.2 Distinction from electronic gain/phase mismatch

At one operating point a complex element response may numerically resemble a per-channel gain/phase error, but element response is generally direction-, frequency-, polarization-, and orientation-dependent.

Thus

\[
\mathbf G\neq\mathbf P(\hat{\mathbf u},f,\mathbf p)
\]

as scientific semantics.

## 6.3 Phase center and cause attribution

Mechanical sensor position and effective electromagnetic phase center are not universally identical. Pattern phase can sometimes resemble a geometric phase-center offset.

Therefore an observed manifold phase error does not by itself prove whether the physical cause is mechanical position, phase-center behavior, cable/electronics, element pattern, or coupling.

GeoDOA must distinguish observed/effective manifold error from physical-cause attribution.

## 6.4 Polarization semantics

The ADR-001/ADR-002 look direction is array-to-source, while propagation direction is

\[
\boxed{\hat{\mathbf k}_{\rm prop}=-\hat{\mathbf u}}.
\]

A plane-wave electric field is transverse to the propagation direction.

A coherent polarization representation requires an explicit transverse basis. A two-component Jones-like state can represent linear, circular, or elliptical polarization. Handedness and basis conventions must be declared rather than hidden in strings such as `RHCP`.

For a normalized receive polarization vector \(\mathbf q\) and incident polarization \(\mathbf p\), a simple normalized polarization-efficiency model is

\[
\boxed{
\eta_{\rm pol}=|\mathbf q^H\mathbf p|^2
}.
\]

For ideal linear polarization misalignment angle \(\alpha\),

\[
\eta_{\rm pol}=\cos^2\alpha.
\]

A physically valid polarization null may produce zero response; this does not make the physical scene invalid, but ratio normalization through that response becomes invalid/ill-conditioned.

## 6.5 Element orientation and array pose

Element orientation is distinct from element position and global array pose.

If \(\mathbf R_n\in SO(3)\) maps local element coordinates to the global frame, then the global direction/polarization must be transformed into the local element frame before evaluating the element pattern.

A correctly located but misoriented element can therefore exhibit amplitude, polarization, and phase-pattern mismatch without a geometric-position error.

## 6.6 Narrowband versus element-response flatness

Propagation narrowband compatibility does not guarantee that element response is frequency-flat over the same band.

A wideband manifold may require both

\[
\beta(f)
\]

for propagation and

\[
b_n(\hat{\mathbf u},f,\mathbf p)
\]

for element response.

## 6.7 Multiple sources

For source \(q\), element response can be source-condition specific:

\[
\mathbf a_q^{\rm phys}
=
\mathbf P(\hat{\mathbf u}_q,f,\mathbf p_q)
\mathbf a_{\rm geom}(\hat{\mathbf u}_q,f).
\]

A single direction-independent matrix \(\mathbf P\) generally cannot represent all sources.

Unknown polarization can become coupled to DOA estimation, and a scalar MUSIC model can become incompatible with a vector/polarimetric sensing problem.

## 6.8 Scalar and vector sensors

The initial GeoDOA profile may remain an ideal identical scalar-element model. However, the scientific architecture must not assume that one physical sensor location always equals one scalar measurement channel. Future vector/polarimetric sensors may provide multiple channels at one physical location.

## 6.9 EM simulation, embedded patterns, and double counting

Three modeling strategies must remain distinguishable:

1. **Parametric decomposition**, such as explicit geometry, isolated element response, electronic response, and coupling operators.
2. **Embedded/full-wave EM response**, such as a CST-derived complex manifold that may already include array/platform interactions.
3. **Direct measured manifold**, which may aggregate several real effects into one effective response.

An effect already embedded in a measured or EM-simulated manifold must not be applied again as a separate imperfection unless explicit de-embedding provenance justifies it.

This is particularly important for mutual coupling and embedded-element-pattern data.

## 6.10 Pattern metadata and calibration

Complex pattern calibration requires more than angle and gain magnitude. Relevant provenance may include direction grid, frequency, polarization basis, orientation, array configuration, active channels, platform/radome state, port termination, phase reference, normalization, measurement/simulation method, and environmental state.

Naive interpolation of wrapped phase is forbidden. Near deep pattern nulls, phase may be poorly conditioned or physically uninformative.

Absolute receive response, normalized complex pattern, directivity, gain, and realized gain are not interchangeable quantities.

Relative complex-pattern calibration and absolute amplitude/power calibration are also different tasks.

## 6.11 Polarization identifiability

A single calibration polarization generally cannot identify a full two-component complex polarization response. Multiple independent excitation states may be required.

## 6.12 Candidate decisions from Exploration 3.4

- **3.4-D1** — Element response and geometry/propagation response are separate meanings.
- **3.4-D2** — Element response is generally complex.
- **3.4-D3** — Element response may depend on direction, frequency, polarization, orientation, and environment.
- **3.4-D4** — An uncoupled scalar-element specialization may use a diagonal element-response operator.
- **3.4-D5** — Element pattern and electronic gain/phase mismatch are not the same scientific model.
- **3.4-D6** — Mechanical position and electromagnetic phase-center behavior are distinct.
- **3.4-D7** — Observed manifold error and attribution of its physical cause must be distinguished.
- **3.4-D8** — Polarization requires explicit propagation-direction and transverse-basis semantics.
- **3.4-D9** — Look direction and propagation direction must remain distinct in polarization conventions.
- **3.4-D10** — Polarization handedness/basis convention must be explicit.
- **3.4-D11** — A common identical element response may preserve normalized single-source manifold direction while changing signal level/SNR.
- **3.4-D12** — Unequal element responses may distort the signal manifold/subspace.
- **3.4-D13** — Element orientation, element position error, and global array pose are distinct.
- **3.4-D14** — Propagation narrowband compatibility does not imply element-response frequency flatness.
- **3.4-D15** — Multiple sources can require source-specific element-response operators.
- **3.4-D16** — Scalar-channel and future vector/polarimetric sensor models must remain semantically separable.
- **3.4-D17** — Source-condition-dependent pattern null is not a permanent dead channel.
- **3.4-D18** — Isolated element pattern, embedded element pattern, and direct array manifold are distinct.
- **3.4-D19** — Effects embedded in measured/EM manifolds shall not be silently re-applied.
- **3.4-D20** — Magnitude-only pattern data are insufficient for coherent complex-manifold calibration.
- **3.4-D21** — Transmit-to-receive pattern reuse requires explicit reciprocity, port, normalization, coordinate, and phase-reference provenance.
- **3.4-D22** — Co-pol/cross-pol labels require a declared polarization basis.
- **3.4-D23** — Pattern-null conditions require ill-conditioning diagnostics rather than declaring valid physical zero response invalid.
- **3.4-D24** — Absolute response, normalized complex pattern, directivity, gain, and realized gain are different scientific quantities.
- **3.4-D25** — Relative pattern calibration and absolute amplitude/power calibration are separate.
- **3.4-D26** — Pattern calibration is a multidimensional scientific object with domain and provenance.
- **3.4-D27** — Complex interpolation must respect phase wrapping and null behavior.
- **3.4-D28** — One calibration polarization is generally insufficient for full two-component polarization-response identification.
- **3.4-D29** — Unknown polarization may couple to DOA and affect estimator compatibility.
- **3.4-D30** — The initial validated GeoDOA profile may remain ideal, scalar, identical-element, unit-response, and uncoupled while preserving extension semantics.

---

# 7. Reserved Golden Reference Problems for ADR-003

The Phase 0C roadmap reserves:

- **GRP-014 — Position-error phase distortion**
- **GRP-015 — Gain/phase mismatch**
- **GRP-016 — Mutual-coupling manifold distortion**
- **GRP-017 — Coupling to covariance to eigenspace distortion**

Current conceptual seeds:

### GRP-014 seed

Two-sensor half-wavelength array, known spacing perturbation, known source direction. Verify the complete chain

\[
\delta d
\rightarrow
\delta\phi
\rightarrow
\hat u
\rightarrow
\Delta\theta,
\]

plus a rigid-translation invariant subcase.

### GRP-015 seed

Use two subcases:

1. common phase applied to all channels — verify covariance/spatial-manifold invariance up to common complex scale;
2. relative phase mismatch on one channel — verify analytical DOA bias for a two-sensor half-wavelength array.

GRP-016 and GRP-017 are intentionally deferred until Exploration 3.5 establishes the accepted candidate mutual-coupling semantics.

---

# 8. Non-Negotiable Cross-ADR Rules Already Inherited

ADR-003 must remain consistent with accepted ADR-001 and ADR-002. In particular:

- temporal phasor convention remains \(e^{-j\omega t}\);
- look direction is array-to-source and propagation direction is its negative;
- geometry/reference/common-phase semantics from ADR-001 remain authoritative;
- nominal physical coordinates are not silently replaced by normalized coordinates;
- common phase is not spatial distortion;
- exact path/propagation meaning precedes far-field or narrowband approximations;
- measurement axes, channel identity, snapshots, covariance semantics, noise semantics, and MIMO provenance remain those of ADR-002;
- no bare/unqualified SNR or unlabeled dB quantity is introduced;
- no hidden unit inference or silent normalization is allowed;
- no scientific model may silently promote/degrade itself to another model when compatibility fails.

---

# 9. Immediate Next Step — Exploration 3.5 Mutual Coupling

The next chat/work session must start at **3.5 — Mutual Coupling**, not redo 3.1–3.4 unless a scientific contradiction is found.

The required 3.5 questions include at least:

1. What physical phenomenon does `mutual coupling` mean in the GeoDOA sensor-modeling context?
2. Under what assumptions can it be represented by a linear cross-channel matrix \(\mathbf C\)?
3. Which side of element/electronic operators does \(\mathbf C\) act on, and why does ordering matter?
4. What makes coupling frequency-, geometry-, termination-, loading-, polarization-, and possibly direction-dependent?
5. What is the relationship among impedance/Z matrices, scattering/S matrices, port/network coupling, embedded element patterns, and an effective receive-manifold coupling operator?
6. Which of those quantities are directly interchangeable and which require a derivation/model of source/load/reference impedance?
7. When is a Toeplitz/banded/symmetric coupling matrix a useful approximation, and when is it unjustified?
8. How does coupling modify \(\mathbf a\), \(\mathbf R_x\), eigenvalues, eigenspaces, and MUSIC orthogonality?
9. How should coupling calibration and inverse/de-coupling conditioning be represented?
10. How are coupling-model residuals distinguished from measured/full-wave manifold calibration residuals?
11. How do active-channel masking, channel dropout, and changed terminations alter coupling semantics?
12. How must GeoDOA prevent double counting when using CST embedded/full-array responses?
13. What deterministic examples should become GRP-016 and GRP-017?

A central inherited rule from the roadmap is:

> Mutual coupling is a first-class sensor-modeling effect and must not be reduced to a generic per-channel phase/gain perturbation.

---

# 10. Acceptance Status

As of this checkpoint:

```text
ADR-001 — ACCEPTED — Gates A–F PASS
ADR-002 — ACCEPTED — Gates A–F PASS
ADR-003 — EXPLORATION IN PROGRESS
    3.1 COMPLETE
    3.2 COMPLETE
    3.3 COMPLETE
    3.4 COMPLETE
    3.5 NEXT
    3.6–3.14 PENDING
    Gates A–F NOT STARTED
ADR-004 — NOT STARTED
```

No statement in this checkpoint may be treated as an accepted ADR-003 contract until the remaining exploration, Gates A–F, cross-gate reconciliation, and final acceptance are completed.
