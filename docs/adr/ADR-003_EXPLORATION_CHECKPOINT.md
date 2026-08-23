# ADR-003 — Exploration Checkpoint

- **Working title:** Sensor Imperfections, Mutual Coupling, and Calibration
- **Phase:** 0C — Scientific Foundations
- **Status:** EXPLORATION IN PROGRESS — NOT ACCEPTED
- **Branch:** `docs/phase0c-scientific-conventions`
- **Depends on:** `ADR-001-coordinate-direction-spatial-conventions.md`, `ADR-002-wave-propagation-signal-measurement-model.md`, `PHASE0C_SCIENTIFIC_CONTRACTS_ROADMAP.md`
- **Completed exploration sections:** 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7
- **Next exploration section:** 3.8 — Unified Sensor-Imperfection Operator
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
3.5  Mutual Coupling                                         COMPLETE
3.6  Channel Delay, Clock Skew, and Frequency Error          COMPLETE
3.7  Quantization / Receiver / Dynamic-Range Effects         COMPLETE
3.8  Unified Sensor-Imperfection Operator                    NEXT
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
\boxed{g_n\approx1+\alpha_n+j\phi_n}.
\]

This is a perturbation approximation only.

An arbitrary electronic phase mismatch is not equivalent to a position-induced phase error. A constant narrowband phase offset is also not equivalent to a physical channel-delay mismatch, which creates a frequency-dependent phase slope.

## 5.4 Covariance propagation

For

\[
\mathbf x
=\mathbf G\mathbf A\mathbf s+\mathbf n,
\]

\[
\mathbf R_{\rm sig}^{\rm phys}
=\mathbf G\mathbf R_{\rm sig}^{\rm nom}\mathbf G^H.
\]

Elementwise,

\[
[R_{\rm sig}^{\rm phys}]_{nm}
=[R_{\rm sig}^{\rm nom}]_{nm}
\rho_n\rho_m e^{j(\phi_n-\phi_m)}.
\]

Common phase cancels from covariance exactly. A common gain scales the signal covariance without rotating the simple signal-subspace direction.

## 5.5 Noise ordering and inverse correction

The placement of gain/response blocks relative to noise injection is scientifically material.

If data correction uses \(\mathbf G^{-1}\), then even initially white noise may become unequal-variance/colored:

\[
\mathbf R_{n,\rm corr}
=\mathbf G^{-1}\mathbf R_n\mathbf G^{-H}.
\]

Near-zero gains make inverse correction ill-conditioned; a zero-response/dead channel cannot be recovered by multiplicative inversion.

## 5.6 Two-sensor phase-error DOA bias

For a two-sensor array,

\[
\mathbf a_{\rm nom}(u)
=\begin{bmatrix}1\\e^{-jkdu}\end{bmatrix},
\]

and a relative phase error \(\phi_e\) on the second channel gives

\[
\boxed{\hat u=u_0-\frac{\phi_e}{kd}}.
\]

For \(d=\lambda/2\),

\[
\boxed{\Delta u=-\frac{\phi_e}{\pi}}.
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
\boxed{b_n=b_n(\hat{\mathbf u},f,\mathbf p,\ldots)}
\]

and

\[
\boxed{\mathbf P(\hat{\mathbf u},f,\mathbf p)=\operatorname{diag}(b_1,\ldots,b_N)}
\]

so that

\[
\boxed{\mathbf a_{\rm elem}=\mathbf P\mathbf a_{\rm geom}}.
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
\boxed{\eta_{\rm pol}=|\mathbf q^H\mathbf p|^2}.
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
=\mathbf P(\hat{\mathbf u}_q,f,\mathbf p_q)
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

# 7. Exploration 3.5 — Mutual Coupling

## 7.1 Physical meaning

In the GeoDOA receive-array context, mutual coupling is the electromagnetic interaction among array elements and ports that makes element and channel responses non-independent. The field/current state associated with one element can alter currents, terminal quantities, input/active impedances, and embedded responses associated with other elements.

Mutual coupling is therefore a first-class **cross-element / cross-port** physical effect. It is not merely an arbitrary per-channel complex gain.

A diagonal gain/phase model has the form

\[
y_n=g_nx_n,
\]

whereas an effective cross-channel coupling specialization can have

\[
\boxed{y_n=\sum_{m=1}^{N}C_{nm}x_m}
\]

with nonzero off-diagonal terms.

At a single operating point, one coupled response vector may sometimes be fitted numerically by a diagonal operator. Such a fit does not establish that the underlying physical interaction is diagonal and generally need not transfer to another direction, polarization, frequency, loading state, or array configuration.

## 7.2 Receive multiport semantics before an effective coupling matrix

GeoDOA shall not begin the physical definition of coupling by assuming universally that

\[
\mathbf a_c=\mathbf C\mathbf a.
\]

A more defensible receive-array starting point is a declared linear multiport representation.

Let \(\mathbf v_{\rm oc}\) be the **array-defined open-circuit receive-response vector** under a specified incident field and EM/modeling convention. It is not automatically an uncoupled geometry-only steering vector. Depending on how it was obtained, it may already reflect array interaction physics.

Let the antenna-array impedance matrix be \(\mathbf Z_A\) and let \(\mathbf Z_L\) denote the declared receiver/load termination matrix.

Under a declared Thevenin-style multiport current/voltage convention for which the corresponding inverses exist,

\[
\boxed{\mathbf i=(\mathbf Z_A+\mathbf Z_L)^{-1}\mathbf v_{\rm oc}}
\]

and loaded terminal voltage is

\[
\boxed{\mathbf v_L=\mathbf Z_L(\mathbf Z_A+\mathbf Z_L)^{-1}\mathbf v_{\rm oc}}.
\]

Define

\[
\boxed{\mathbf T_L=\mathbf Z_L(\mathbf Z_A+\mathbf Z_L)^{-1}}
\]

so that \(\mathbf v_L=\mathbf T_L\mathbf v_{\rm oc}\).

This is a loaded-port transform, not a universal definition of a DOA coupling matrix. It is meaningful only together with the definitions of \(\mathbf v_{\rm oc}\), port current/voltage sign convention, reference planes, \(\mathbf Z_A\), \(\mathbf Z_L\), frequency, and physical configuration.

If the available starting response is an isolated-element or geometry-only manifold rather than the array-defined open-circuit response, another explicit EM/effective mapping may be required before the loaded-port relation is scientifically valid.

## 7.3 Effective cross-channel coupling specialization

For a bounded model, GeoDOA may use

\[
\boxed{\mathbf a_c(\xi)=\mathbf C(\chi)\mathbf a_{\rm ref}(\xi)}
\]

where \(\xi\) denotes source-condition variables and \(\chi\) denotes sensor/system configuration variables.

The semantic type of \(\mathbf C\) must be declared: physical/network-derived operator, effective manifold operator, or aggregate empirical operator.

Thus \(\mathbf a_c=\mathbf C\mathbf a\) is a declared specialization, not a universal electromagnetic law.

## 7.4 Impedance, scattering, and effective-coupling semantics

Impedance parameters use port voltage/current semantics, \(\mathbf v=\mathbf Z\mathbf i\), whereas scattering parameters use incident/reflected port-wave semantics, \(\mathbf b_{\rm wave}=\mathbf S\mathbf a_{\rm wave}\). The port-wave symbol \(\mathbf a_{\rm wave}\) must never be confused with a steering/manifold vector.

For a common real scalar reference impedance \(Z_0\) and corresponding conventional wave normalization,

\[
\mathbf S=(\mathbf Z-Z_0\mathbf I)(\mathbf Z+Z_0\mathbf I)^{-1},
\]

\[
\mathbf Z=Z_0(\mathbf I+\mathbf S)(\mathbf I-\mathbf S)^{-1},
\]

when the required inverses exist. Unequal or complex reference impedances require their own explicit normalization/conversion convention.

Consequently, \(\mathbf Z\), \(\mathbf S\), \(\mathbf T_L\), an effective \(\mathbf C\), embedded patterns, and measured/full-wave manifolds are not directly interchangeable. In particular, \(S_{21}\neq C_{21}\) as a general scientific statement.

## 7.5 Dependence classes

For a passive linear time-invariant array in a fixed configuration, network matrices such as \(\mathbf Z_A(f)\) and \(\mathbf S(f)\) characterize the multiport system. The receive excitation is source-condition dependent:

\[
\mathbf v_{\rm oc}=\mathbf v_{\rm oc}(\hat{\mathbf u},f,\mathbf p,\ldots).
\]

An effective \(\mathbf C\) fitted between a geometry-only manifold and a full physical manifold may appear direction- or polarization-dependent because it absorbs other effects.

Network-parameter dependence, source-excitation dependence, and effective-manifold-operator dependence remain distinct.

## 7.6 Structural approximations

Reciprocity under compatible conventions can justify symmetric network quantities such as \(Z_{nm}=Z_{mn}\), but symmetric does not mean Hermitian.

Toeplitz coupling for a finite ULA is an approximation/specialization because edge elements can have different electromagnetic neighborhoods from interior elements. Circulant structure is not the default for an ordinary finite ULA. Banded/nearest-neighbor models require evidence or an explicit truncation policy.

Even if an impedance model is sparse/banded, \((\mathbf Z_A+\mathbf Z_L)^{-1}\) can be dense.

## 7.7 Embedded patterns and double counting

Isolated-element response, embedded-element response, full-wave/full-array complex manifold, direct measured manifold, and separately parameterized coupling operators are distinct.

If a CST/full-wave or measured response already contains mutual-coupling physics, GeoDOA shall not silently apply another coupling matrix unless explicit de-embedding/re-embedding provenance proves the decomposition valid.

## 7.8 Operator ordering

A physically interpretable receive chain may contain geometry/propagation, element/open-circuit receive response, port/network loading and cross-channel interaction, receiver electronics, and measurement. A specialization may produce \(\mathbf a_{\rm phys}=\mathbf G\mathbf T_L\mathbf a_{\rm oc}\), but the final universal ordering is deferred to 3.8.

In general \(\mathbf C\mathbf P\neq\mathbf P\mathbf C\).

## 7.9 Manifold and covariance distortion

For \(\mathbf x=\mathbf C\mathbf A\mathbf s+\mathbf n\), with shown noise injected after coupling,

\[
\boxed{\mathbf R_{\rm sig,c}=\mathbf C\mathbf R_{\rm sig}\mathbf C^H}.
\]

Also,

\[
\operatorname{rank}(\mathbf C\mathbf R\mathbf C^H)
\le\min\{\operatorname{rank}(\mathbf C),\operatorname{rank}(\mathbf R)\}.
\]

Nonsingular \(\mathbf C\) preserves rank but can change eigenvalues, eigenvectors, subspace orientation, and conditioning; rank-deficient coupling can reduce observable rank.

## 7.10 MUSIC consequence

For one source \(\mathbf b=\mathbf C\mathbf a(\theta_0)\), the physical noise subspace satisfies \(\mathbf E_n^H\mathbf b=0\). Nominal MUSIC may instead have \(\mathbf E_n^H\mathbf a(\theta_0)\neq0\). The algebra has not failed; the supplied manifold is mismatched.

## 7.11 Noise ordering

If

\[
\mathbf x=\mathbf C(\mathbf A\mathbf s+\mathbf n_{\rm pre})+\mathbf n_{\rm post},
\]

then

\[
\mathbf R_x=\mathbf C\mathbf A\mathbf R_s\mathbf A^H\mathbf C^H
+\mathbf C\mathbf R_{n,\rm pre}\mathbf C^H+\mathbf R_{n,\rm post}.
\]

Pre-coupling white noise generally becomes colored after nonunitary coupling.

## 7.12 Inverse decoupling and conditioning

For calibrated inverse correction, \(\mathbf y=\hat{\mathbf C}^{-1}\mathbf x\), noise and model error are transformed. \(\|\mathbf C^{-1}\|_2=1/\sigma_{\min}(\mathbf C)\) and \(\kappa_2=\sigma_{\max}/\sigma_{\min}\). Singular coupling has no exact inverse.

## 7.13 Residual coupling and attribution

\[
\Delta\mathbf C=\mathbf C-\hat{\mathbf C}
\]

and, when valid,

\[
\mathbf E_C=\hat{\mathbf C}^{-1}\mathbf C-\mathbf I
\]

have different semantics. Residual manifold mismatch must not automatically be labeled residual mutual coupling.

## 7.14 Channel dropout and termination changes

Digital masking after acquisition is distinct from a physical port-state/termination change. If \(\mathbf Z_L\) changes, the loaded transform generally changes for all surviving channels; deleting an old matrix row/column is not automatically valid.

## 7.15 Scientific verification notes

The exploration was cross-checked against established antenna/network practice for mutual impedance, S-parameters, loaded multiport receiving arrays, embedded-element patterns, and finite-array edge effects.

## 7.16 Candidate decisions from Exploration 3.5

- **3.5-D1** — Mutual coupling is an electromagnetic cross-element/cross-port phenomenon and is not equivalent to diagonal gain/phase mismatch.
- **3.5-D2** — Physical multiport receive semantics precede any generic DOA coupling-matrix specialization.
- **3.5-D3** — Array-defined open-circuit receive response, antenna impedance network, loading/termination, and loaded terminal response are distinct scientific objects.
- **3.5-D4** — Within a declared Thevenin-style multiport convention, loaded response may use \(\mathbf T_L=\mathbf Z_L(\mathbf Z_A+\mathbf Z_L)^{-1}\); this is a loaded-port transform, not a universal coupling law.
- **3.5-D5** — An open-circuit receive-response vector is not automatically an uncoupled geometry-only steering vector and may already include array interaction physics depending on its provenance.
- **3.5-D6** — \(\mathbf a_c=\mathbf C\mathbf a\) is a declared specialization, not a universal electromagnetic law.
- **3.5-D7** — A coupling operator must declare whether it is network-derived, effective-manifold, or aggregate empirical.
- **3.5-D8** — \(\mathbf Z\), \(\mathbf S\), \(\mathbf T_L\), an effective \(\mathbf C\), embedded patterns, and full measured/EM manifolds are not directly interchangeable.
- **3.5-D9** — Z/S conversion requires explicit reference-impedance and wave-normalization semantics; unequal/complex reference impedances require the corresponding declared convention.
- **3.5-D10** — A quantity such as \(S_{21}\) is not, in general, the coupling coefficient to insert directly into a DOA steering-manifold matrix.
- **3.5-D11** — Network-parameter dependence, source-excitation dependence, and effective-manifold-operator dependence remain distinct.
- **3.5-D12** — Reciprocity may justify symmetric network quantities under compatible conventions, but symmetric does not mean Hermitian.
- **3.5-D13** — Toeplitz coupling for a finite ULA is an approximation/specialization, not a universal physical law; edge effects may violate it.
- **3.5-D14** — Circulant structure is not the default model for an ordinary finite ULA.
- **3.5-D15** — Banded/nearest-neighbor coupling is a truncation approximation requiring evidence or an explicit approximation policy.
- **3.5-D16** — Sparse/banded impedance interaction does not imply a sparse/banded loaded or inverse operator.
- **3.5-D17** — Coupling and diagonal element/electronic operators are generally noncommutative; physical ordering matters.
- **3.5-D18** — Final unified operator ordering is deferred to Exploration 3.8.
- **3.5-D19** — In a declared linear specialization, coupled signal covariance propagates as \(\mathbf C\mathbf R\mathbf C^H\).
- **3.5-D20** — Nonsingular coupling preserves covariance rank but can change eigenvalues, eigenvectors, signal/noise-subspace orientation, and conditioning.
- **3.5-D21** — Rank-deficient coupling can reduce observable signal rank.
- **3.5-D22** — MUSIC noise-subspace orthogonality is with respect to the physical coupled manifold, not necessarily the nominal manifold.
- **3.5-D23** — Coupling/noise ordering must be explicit.
- **3.5-D24** — Pre-coupling spatially white noise may become colored/correlated after a nonunitary coupling transform.
- **3.5-D25** — Model calibration and inverse data decoupling are distinct operations.
- **3.5-D26** — Inverse decoupling can amplify noise and calibration/model error.
- **3.5-D27** — Minimum singular value and condition number provide different but complementary inverse-conditioning information.
- **3.5-D28** — Singular coupling has no exact inverse decoupling; pseudoinverse/regularization is a separate calibration strategy.
- **3.5-D29** — Additive residual \(\Delta\mathbf C\) and relative inverse residual \(\hat{\mathbf C}^{-1}\mathbf C-\mathbf I\) have different semantics and validity conditions.
- **3.5-D30** — Residual manifold mismatch must not be called residual coupling without physical-cause/identifiability evidence.
- **3.5-D31** — Digital channel masking and physical port-state/termination changes are different phenomena.
- **3.5-D32** — A changed termination/configuration may alter all surviving responses; row/column deletion from an old coupling matrix is not automatically valid.
- **3.5-D33** — Embedded-element, full-wave, and measured manifolds may already contain coupling physics.
- **3.5-D34** — GeoDOA requires included-effects/de-embedding provenance to prevent coupling double counting.
- **3.5-D35** — GRP-016 shall exercise deterministic mutual-coupling manifold distortion; GRP-017 shall continue that case through covariance/eigenspace/MUSIC consequences.
- **3.5-D36** — The initial Phase-1 validated profile may remain uncoupled while preserving the coupling contract as a later bounded extension.

---

# 8. Exploration 3.6 — Channel Delay, Clock Skew, and Frequency Error

## 8.1 Timing/frequency taxonomy

GeoDOA shall not use one ambiguous `phase_error` parameter for all receiver timing and frequency imperfections. Static phase offset, physical/electrical channel delay, fixed sampling-time offset, sampling-rate offset, sampling-time jitter, receiver-reference/LO phase and frequency error, and digital processing latency are distinct meanings.

## 8.2 Physical channel delay and sign convention

A pure additional channel delay obeys

\[
y_n(t)=x_n(t-\delta\tau_n),
\qquad
H_{\tau,n}(\omega)=e^{+j\omega\delta\tau_n}
\]

under the accepted GeoDOA \(e^{-j\omega t}\) convention. In complex-envelope form this includes envelope delay and carrier phase. A phase-only diagonal representation is a declared narrowband approximation, not the general definition.

## 8.3 Delay slope versus static phase offset

For a pure delay,

\[
\phi_{\tau,n}(\omega)=\omega\delta\tau_n,
\qquad
\frac{d\phi}{d\omega}=\delta\tau_n.
\]

Static phase offset has no such slope. Single-frequency phase alone may not identify the cause.

## 8.4 Channel-delay compatibility

Define differential channel-delay spread \(\Delta\tau_{\rm ch}\) and diagnostic \(\eta_{\rm ch-delay}=2\pi\nu_{\max}\Delta\tau_{\rm ch}\). This is separate from propagation aperture delay. No universal PASS/FAIL threshold is declared here.

## 8.5 Sampling-time model

A channel-specific acquisition-time model is

\[
\boxed{t_n[k]=t_0+\beta_n+kT_s(1+\epsilon_{T,n})+\eta_n[k]},
\]

with fixed offset \(\beta_n\), fractional sample-period error \(\epsilon_{T,n}\), and jitter \(\eta_n[k]\). If \(f_{s,n}=f_s(1+\epsilon_{f,n})\), then \(1+\epsilon_T=1/(1+\epsilon_f)\) and for small error \(\epsilon_T\approx-\epsilon_f\).

## 8.6 Sampling-time offset versus channel delay

Later sampling of \(z(t)=Ae^{-j\omega t}\) gives

\[
z(t+\delta t)=z(t)e^{-j\omega\delta t},
\]

opposite in sign to positive waveform delay because these are different physical operations. The relevant frequency depends on the sampling stage.

## 8.7 Fixed skew, SRO, and jitter

Fixed sampling offset is constant. SRO produces accumulated timing drift \(\delta t_n[k]=\beta_n+kT_s\epsilon_{T,n}\). Jitter is sample-varying uncertainty. Broadband SRO correction generally requires resampling/time-warp correction, not one fixed phase.

## 8.8 Common versus differential clock errors

Common clock error can preserve inter-channel synchronization while distorting an external time axis. Differential offset/SRO breaks simultaneity/coherence unless explicitly corrected.

## 8.9 Aperture delay, jitter, and processing latency

ADC aperture delay, aperture jitter, and conversion/buffer/DMA/FPGA latency are distinct. Post-acquisition data arriving later does not imply it was sampled later if sample identity and epoch are preserved.

## 8.10 Receiver-reference / LO error

Represent processed-baseband receiver-reference phase as \(e^{j\psi_n(t)}\), with

\[
\delta f_{\rm ref,n}(t)=\frac{1}{2\pi}\frac{d\psi_n}{dt}.
\]

Static phase offset is an intercept; frequency offset is phase evolution. Mapping physical LO error into processed-baseband sign requires explicit mixer convention.

## 8.11 Common versus differential reference error

A truly common phase process is projectively common across simultaneous spatial channels and cancels from an instantaneous covariance outer product. Differential frequency error creates a time-varying relative manifold.

## 8.12 Covariance-window coherence

For differential frequency error,

\[
\Gamma_{nm}=\frac1L\sum_k e^{j2\pi(\delta f_n-\delta f_m)t_k}.
\]

Continuous uniform averaging gives

\[
\Gamma_{nm}(T)=e^{j\pi\Delta f_{nm}T}\operatorname{sinc}(\Delta f_{nm}T),
\]

so cross-channel coherence can attenuate over long windows.

## 8.13 Snapshot validity under SRO

Differential SRO challenges ADR-002 simultaneous-equivalent snapshot semantics. For broadband signals, coherent reconstruction generally requires interpolation/resampling with explicit provenance.

## 8.14 Doppler/source/LO distinction

Physical Doppler, source-frequency uncertainty, and receiver reference frequency error remain distinct causes even if one observed residual frequency contains all of them. Shared reference topology may correlate sampling and LO errors.

## 8.15 TDM-MIMO implication

A common temporal phase process can become a relative virtual-channel phase when virtual channels are acquired at different times. TDM snapshot construction must preserve acquisition-time and phase-compensation provenance.

## 8.16 Calibration and identifiability

Calibration shall type phase intercept, channel delay, sample-time offset, SRO, oscillator phase/frequency, and jitter separately. Multi-frequency calibration can reveal delay slope; common errors may require an external reference.

## 8.17 Small deterministic checks

A +100 ps physical delay at 100 MHz gives +3.6 degrees under the declared convention, while sampling the same waveform +100 ps later gives -3.6 degrees. A +10 ppm sample-rate error accumulates about 10 microseconds of epoch drift over one second. A 1 Hz differential frequency error averaged for 0.5 s yields coherence magnitude \(2/\pi\approx0.6366\).

## 8.18 Scientific verification notes

Exploration 3.6 was reconciled with ADR-002 delay/Fourier/snapshot semantics and established ADC synchronization, aperture-jitter, CFO, and SRO practice.

## 8.19 Candidate decisions from Exploration 3.6

- **3.6-D1** — Static narrowband phase offset, physical channel delay, sampling-time offset, sampling-rate offset, jitter, oscillator phase/frequency error, and digital processing latency are distinct scientific meanings.
- **3.6-D2** — A pure physical delay obeys the accepted GeoDOA transfer factor \(e^{+j\omega\delta\tau}\).
- **3.6-D3** — RF/IF channel delay can alter both envelope alignment and carrier phase; phase-only representation is a declared narrowband approximation.
- **3.6-D4** — Pure delay has phase slope \(d\phi/d\omega=\delta\tau\); static phase offset does not.
- **3.6-D5** — A single-frequency phase measurement generally cannot identify static phase offset versus delay-induced phase without additional information.
- **3.6-D6** — Receiver/channel delay requires its own bandwidth-delay compatibility diagnostic separate from propagation-aperture delay.
- **3.6-D7** — No universal timing/delay compatibility threshold is declared during exploration.
- **3.6-D8** — Fixed sampling-time offset is defined by the physical sample epoch and is not the same operation as delaying the waveform.
- **3.6-D9** — For \(e^{-j\omega t}\), later sampling by \(+\delta t\) produces \(e^{-j\omega\delta t}\), opposite in sign to a positive waveform delay under the declared definitions.
- **3.6-D10** — The frequency relevant to sampling-time phase depends on the physical sampling stage; RF, IF, and baseband sampling require provenance.
- **3.6-D11** — GeoDOA shall prefer explicit fixed sampling-time offset, sampling-rate offset, and jitter semantics over ambiguous bare clock-skew terminology.
- **3.6-D12** — A useful sample-time model separates fixed offset, fractional sample-period error, and sample-to-sample jitter.
- **3.6-D13** — Fractional sample-rate error and fractional sample-period error have opposite first-order signs and must not be conflated.
- **3.6-D14** — Common fixed sampling-time offset may preserve relative spatial simultaneity while changing absolute observation epoch; differential fixed offset does not.
- **3.6-D15** — A common sample-rate error on a genuinely shared clock can preserve inter-channel synchronization while distorting the external physical time scale.
- **3.6-D16** — Differential SRO accumulates relative time drift and generally requires resampling/time-warp correction for broadband coherent processing.
- **3.6-D17** — Sampling-time jitter is distinct from deterministic skew/SRO and is further developed with receiver/ADC effects in Exploration 3.7.
- **3.6-D18** — ADC aperture delay, aperture jitter, and post-acquisition digital/FPGA latency are different quantities.
- **3.6-D19** — Processing/DMA/pipeline latency does not change acquisition time if sample identity and epoch correspondence are preserved.
- **3.6-D20** — Receiver-reference phase shall be representable as a time-varying phase process whose derivative defines residual reference-frequency error.
- **3.6-D21** — Static receiver-reference phase offset and nonzero frequency offset are different models.
- **3.6-D22** — Mapping physical LO error into processed-baseband residual frequency requires an explicit mixer/downconversion sign convention.
- **3.6-D23** — A truly common oscillator phase process is a common complex factor across simultaneous spatial channels and cancels from an instantaneous covariance outer product.
- **3.6-D24** — Differential oscillator/reference frequency error creates a time-varying relative manifold and can rotate/attenuate cross-channel covariance over a finite window.
- **3.6-D25** — Finite-window covariance coherence under constant differential frequency error is governed by the explicit snapshot-time average \(\Gamma_{nm}\), not by one static phase value.
- **3.6-D26** — Common temporal phase/frequency error can become relative virtual-channel phase when TDM/non-simultaneous channels are assembled into one virtual snapshot.
- **3.6-D27** — Snapshot construction must preserve acquisition-time and synchronization/correction provenance.
- **3.6-D28** — Physical Doppler, source-frequency uncertainty, and receiver LO/reference frequency error are distinct causes even when they contribute to one observed residual frequency.
- **3.6-D29** — Shared oscillator/reference topology may correlate sampling-rate and LO-frequency errors; independence shall not be assumed by default.
- **3.6-D30** — Integer-sample alignment and fractional-delay/resampling correction are distinct operations with different numerical/noise consequences.
- **3.6-D31** — Calibration shall declare whether it estimates phase intercept, channel delay, sample-time offset, SRO, oscillator phase/frequency, jitter, or an aggregate effective correction.
- **3.6-D32** — Multi-frequency/broadband calibration may identify delay through phase slope, subject to phase unwrapping and model-validity conditions.
- **3.6-D33** — Common timing/frequency errors may be unidentifiable from relative spatial data without an external reference.
- **3.6-D34** — Calibration validity/provenance must preserve clock/LO topology, reference identity, lock/restart state, center frequency, sample rate, acquisition stage, calibration bandwidth/waveform, time/temperature, and correction method as applicable.
- **3.6-D35** — Residual delay, timing offset, SRO, and frequency error require typed residuals; a generic residual phase is insufficient when error evolves across frequency or time.
- **3.6-D36** — The initial Phase-1 validated profile may assume synchronized channels, common coherent clock/reference, zero differential channel delay/SRO/CFO, and no timing jitter while preserving these contracts for later bounded extensions.

---

# 9. Exploration 3.7 — Quantization / Receiver / Dynamic-Range Effects

## 9.1 Receiver-chain scope and semantic boundaries

Exploration 3.7 covers imperfections that arise in the analog receive chain, data conversion, and finite-resolution measurement representation. It does **not** collapse all hardware imperfections into one additive-noise term.

A useful conceptual chain is

```text
physical sensor / coupled port response
    ↓
analog receiver gain, filtering, noise, offset, I/Q conversion, nonlinearity
    ↓
sampling instant / aperture uncertainty
    ↓
ADC input and full-scale constraint
    ↓
quantizer / code mapping / overrange behavior
    ↓
digital measurement samples
    ↓
subsequent DSP / FPGA arithmetic
```

ADC quantization and FPGA/processor fixed-point arithmetic are separate scientific stages. ADC quantization changes the measurement representation at acquisition; FPGA arithmetic quantization occurs later inside an implementation and has its own scaling, rounding, saturation, and word-length semantics.

## 9.2 Ideal uniform ADC quantizer

For an explicitly declared ideal uniform \(N_b\)-bit quantizer with analog full-scale input span

\[
\boxed{V_{\rm FSR}=V_{\max}-V_{\min}},
\]

and \(2^{N_b}\) quantization intervals, define the ideal step size

\[
\boxed{\Delta=\frac{V_{\rm FSR}}{2^{N_b}}}.
\]

This formula assumes the declared uniform idealization. The exact transition levels, reconstruction levels, endpoint behavior, signed/unsigned code mapping, two's-complement/offset-binary encoding, and mid-rise versus mid-tread convention must be explicit when code-exact behavior matters.

For an in-range nearest-level idealization,

\[
y=Q(x),
\qquad
e_q=Q(x)-x,
\]

and away from endpoint ambiguities,

\[
\boxed{|e_q|\le\frac{\Delta}{2}}.
\]

This deterministic in-range error bound is different from a stochastic quantization-noise model.

For a complex baseband sample, GeoDOA shall not assume that a physical ADC directly quantizes a complex number. A physical I/Q receiver usually has two real converter paths or another explicitly declared architecture. An abstract complex quantizer may be used only when its relationship to physical I/Q conversion is stated.

## 9.3 Exact quantization error versus additive quantization-noise approximation

The quantizer is nonlinear:

\[
\boxed{y=Q(x)}.
\]

Writing

\[
Q(x)=x+e_q
\]

is an identity if \(e_q\equiv Q(x)-x\), but treating \(e_q\) as independent, white, zero-mean noise is an **additional statistical approximation**.

Under the classical high-resolution/no-overload conditions in which the quantization error is effectively distributed uniformly over one quantization cell,

\[
\boxed{e_q\sim\mathcal U\left(-\frac{\Delta}{2},\frac{\Delta}{2}\right)}
\]

is a useful model, giving

\[
\boxed{\operatorname{E}[e_q]=0,
\qquad
\sigma_q^2=\frac{\Delta^2}{12}}.
\]

GeoDOA shall not assume this model blindly. Quantization error can be signal-correlated, spectrally structured, periodic, or strongly non-Gaussian for low-level, deterministic, coherent, low-resolution, or overloaded inputs. Dither or naturally occurring receiver noise may make additive-noise assumptions more accurate, but dither itself is a declared physical/algorithmic condition.

## 9.4 Ideal quantization SNR and ENOB

For a full-scale sinusoid applied to an ideal \(N_b\)-bit uniform ADC, with only the classical uniform quantization-noise model and no overload, thermal noise, jitter, distortion, or nonlinearity, the familiar result is

\[
\boxed{\operatorname{SNR}_{q,\rm dB}
\approx6.02N_b+1.76\ \text{dB}}.
\]

This result is not a universal SNR law for arbitrary waveforms, amplitudes, bandwidths, or converters. Its signal definition and full-scale convention must be stated.

For practical converters, **nominal resolution** \(N_b\) and **effective number of bits** are different. Under the conventional sinusoidal dynamic-test definition,

\[
\boxed{\operatorname{ENOB}
\approx\frac{\operatorname{SINAD}_{\rm dB}-1.76}{6.02}}.
\]

ENOB depends on test conditions such as input frequency, amplitude, sample rate, analog front-end, clock quality, and which distortion/noise components enter SINAD. ENOB shall not be used as a drop-in replacement for nominal code width or DC accuracy.

Likewise, SNR, SINAD, THD, SFDR, ENOB, dynamic range, and noise-free resolution are distinct metrics and must not be reported under one generic `adc_quality` field.

## 9.5 Full scale, dBFS, headroom, saturation, and clipping

The ADC has a finite allowed input region. If the analog input exceeds the declared conversion range, the in-range quantization bound \(|e_q|\le\Delta/2\) no longer applies.

A saturating quantizer can be represented abstractly as

\[
\boxed{y=Q_{\rm sat}(x;V_{\min},V_{\max})}.
\]

Clipping/overrange is a nonlinear information-loss event, not ordinary quantization noise. It can create harmonics, intermodulation, biased amplitudes, covariance distortion, and false spatial/statistical structure.

GeoDOA shall preserve an overrange/clipping diagnostic where the modeled converter supplies one. Samples or frames containing overrange events shall not silently be treated as statistically equivalent to valid in-range samples.

`dBFS` requires an explicit full-scale reference convention. Peak full-scale, RMS full-scale sine, full-scale span, and code-span references are not interchangeable without a declaration.

## 9.6 Receiver thermal/electronic noise versus quantization error

Receiver noise is generated physically before and/or within acquisition electronics. Quantization error is generated by the discrete amplitude mapping of the ADC. They are different phenomena.

A simple declared chain may be

\[
\boxed{\mathbf z[k]=\mathbf G_{\rm rx}\mathbf x[k]+\mathbf n_{\rm rx}[k]}
\]

followed by

\[
\boxed{\mathbf y[k]=\mathcal Q(\mathbf z[k])}.
\]

The receiver-noise covariance

\[
\mathbf R_{n,\rm rx}
=\operatorname E[\mathbf n_{\rm rx}\mathbf n_{\rm rx}^H]
\]

need not be spatially white, equal-variance, or independent across channels. Shared supplies, clock feedthrough, coupling, common references, and receiver architecture can create correlated noise.

Under a bounded additive-quantization approximation, one may write

\[
\mathbf y\approx\mathbf z+\mathbf e_q
\]

and then, only with the required independence assumptions,

\[
\mathbf R_y
\approx
\mathbf R_z+\mathbf R_q.
\]

Analog receiver noise may also act as natural dither, changing quantizer statistics. This does not make receiver noise and quantization noise the same physical source.

## 9.7 Gain staging, dynamic range, and AGC

Analog gain before the ADC controls how the available converter range is used. Too little gain can make weak signals occupy only a small number of codes and increase the relative importance of downstream ADC noise/quantization. Too much gain can reduce headroom and drive analog compression or ADC clipping.

Therefore receiver gain staging is a tradeoff among at least

\[
\boxed{\text{sensitivity / noise figure}
\leftrightarrow
\text{ADC utilization}
\leftrightarrow
\text{headroom / compression / clipping}
\leftrightarrow
\text{linearity / SFDR}}.
\]

Analog gain applied before quantization is not equivalent to digital scaling applied after quantization. Digital scaling cannot recover information already lost to clipping or coarse quantization.

An AGC state shall be treated as part of measurement provenance. For an ideal common gain

\[
\mathbf G_{\rm AGC}[k]=g_c[k]\mathbf I,
\]

all channels receive the same instantaneous scale, which can preserve normalized spatial direction at each snapshot. However, time-varying common gain still weights snapshots differently and changes absolute signal/noise levels.

Channel-dependent AGC or unequal gain control has

\[
\mathbf G_{\rm AGC}[k]
=\operatorname{diag}(g_1[k],\ldots,g_N[k]),
\]

which can directly distort relative manifold amplitude and make the covariance process time varying.

Gain-control state, settling/transient state, update timing, and whether gain is analog or digital must be explicit.

## 9.8 Aperture jitter as a receiver/acquisition error

Exploration 3.6 defined sample-time jitter semantically. Here its receiver-performance consequence is made explicit.

For a small sampling-time error \(\delta t\),

\[
\boxed{x(t+\delta t)
\approx x(t)+x'(t)\delta t}.
\]

Thus jitter-induced amplitude error scales with signal slew rate, not merely with signal amplitude.

For a sinusoid of frequency \(f_{\rm in}\) and uncorrelated RMS aperture jitter \(\sigma_t\), the classical jitter-limited SNR approximation is

\[
\boxed{\operatorname{SNR}_{\rm jitter,dB}
\approx-20\log_{10}(2\pi f_{\rm in}\sigma_t)}.
\]

This is a specialized sinusoidal/RMS result, not a universal stochastic model for arbitrary waveforms.

Common and differential jitter must remain distinguishable. A common narrowband sample-time fluctuation may appear as a common instantaneous phase perturbation, while channel-specific or partially correlated jitter can create relative spatial error. Clock-tree topology and jitter correlation therefore belong to provenance.

## 9.9 DC offset, mean removal, and spurious covariance modes

Let a receiver add a deterministic or slowly varying offset vector \(\mathbf d\):

\[
\boxed{\mathbf y=\mathbf x+\mathbf d}.
\]

The uncentered second moment is

\[
\mathbf R_y^{(2)}
=\operatorname E[\mathbf y\mathbf y^H].
\]

If \(\operatorname E[\mathbf x]=\mathbf0\), then

\[
\boxed{\mathbf R_y^{(2)}
=\mathbf R_x+\mathbf d\mathbf d^H}.
\]

A constant channel-offset vector can therefore create an additional rank-one term in the uncentered second moment.

An ideal centered covariance removes a truly constant offset when the mean is exactly known/estimated under compatible stationarity conditions. Finite-sample mean estimation, drifting offsets, DC leakage, LO feedthrough, and source components at/near DC can leave residual structure.

GeoDOA shall preserve the ADR-002 distinction between uncentered second moment and centered sample covariance; `DC offset removed` is not an automatic property of every covariance computation.

## 9.10 I/Q imbalance is a widely linear impairment

In a quadrature/direct-conversion receiver, I/Q amplitude mismatch, phase mismatch, and DC offset can mix the desired complex signal with its conjugate image.

A useful per-array widely linear model is

\[
\boxed{\mathbf y
=\mathbf A_{\rm IQ}\mathbf x
+\mathbf B_{\rm IQ}\mathbf x^*
+\mathbf d_{\rm IQ}}.
\]

For independent per-channel I/Q imbalance, \(\mathbf A_{\rm IQ}\) and \(\mathbf B_{\rm IQ}\) may be diagonal. Ideal quadrature balance corresponds to the conjugate-image coefficient vanishing:

\[
\boxed{\mathbf B_{\rm IQ}=\mathbf0}.
\]

Thus I/Q imbalance is not generally equivalent to an ordinary complex gain matrix \(\mathbf G\mathbf x\).

For centered data define covariance and pseudocovariance

\[
\mathbf R_x=\operatorname E[\mathbf x\mathbf x^H],
\qquad
\mathbf P_x=\operatorname E[\mathbf x\mathbf x^T].
\]

Ignoring offset for this expression,

\[
\boxed{
\begin{aligned}
\mathbf R_y
={}&\mathbf A\mathbf R_x\mathbf A^H
+\mathbf A\mathbf P_x\mathbf B^H\\
&+\mathbf B\mathbf P_x^*\mathbf A^H
+\mathbf B\mathbf R_x^*\mathbf B^H.
\end{aligned}}
\]

Consequently, ordinary covariance alone may be insufficient to describe an improper/noncircular complex receiver process. Future I/Q-aware estimation may require augmented/widely linear statistics.

## 9.11 Analog nonlinearity, compression, and intermodulation

Receiver amplifiers, mixers, and ADC front ends can depart from linear superposition before hard clipping occurs.

A memoryless complex-envelope specialization may be represented locally as

\[
\boxed{y_n
=a_{1,n}x_n+a_{3,n}|x_n|^2x_n+a_{5,n}|x_n|^4x_n+\cdots}.
\]

This is a behavioral model, not a universal transistor-level law.

Once the receiver is nonlinear,

\[
F(x_1+x_2)\neq F(x_1)+F(x_2),
\]

so multiple sources/interferers can create harmonics and intermodulation products not present in the linear array model. A strong blocker can therefore influence a weak-source DOA estimate even when the blocker itself lies outside the ideal signal model.

P1dB, IIP2/IIP3, THD, and SFDR are receiver/converter characterization metrics; they are not interchangeable and are not themselves direct coefficients of the polynomial model without an explicit mapping.

Analog compression and ADC clipping are distinct nonlinear stages, although both may occur in the same receiver under excessive level.

## 9.12 Covariance and eigenspace consequences

For exact quantization or nonlinear receiver response,

\[
\boxed{\mathbf R_y
=\operatorname E[\mathcal F(\mathbf x)\mathcal F(\mathbf x)^H]}
\]

is the primary definition. In general it cannot be reduced to \(\mathbf R_x+\sigma^2\mathbf I\).

Under the restricted additive, spatially white quantization approximation,

\[
\mathbf R_y\approx\mathbf R_x+\sigma_q^2\mathbf I,
\]

ideal quantization noise only shifts eigenvalues and preserves eigenvectors. This special result is frequently useful, but it must not be generalized to unequal channel steps, channel-dependent gain, correlated quantization error, clipping, I/Q imbalance, or nonlinear compression.

If

\[
\mathbf R_q=\operatorname{diag}(\sigma_{q,1}^2,\ldots,\sigma_{q,N}^2)
\]

with unequal entries, even an additive approximation can rotate eigenspaces relative to the ideal equal-noise case.

Clipping/nonlinearity can also make the effective response source-amplitude dependent, violating the fixed linear manifold assumption used by classical MUSIC. The correct question is therefore not merely `how many bits?` but whether the complete receiver/quantizer model remains compatible with the estimator's covariance/manifold assumptions.

## 9.13 Coarse and one-bit quantization as a separate estimator regime

Very coarse quantization shall not be justified through the high-resolution \(\Delta^2/12\) approximation by default.

For example, for zero-mean jointly Gaussian **real** variables \(x_i,x_j\), one-bit sign quantization obeys the classical arcsine relationship

\[
\boxed{\operatorname E[\operatorname{sgn}(x_i)\operatorname{sgn}(x_j)]
=\frac{2}{\pi}\arcsin(\rho_{ij})},
\]

where \(\rho_{ij}\) is the normalized unquantized correlation coefficient.

Complex one-bit array models have corresponding real/imaginary correlation relations under their declared Gaussian/properness/normalization assumptions. This illustrates a crucial point: severe quantization transforms covariance **nonlinearly**, but under special statistical assumptions enough correlation structure can sometimes be recovered or exploited for DOA estimation.

One-bit/coarse-ADC MUSIC and arcsine-law covariance recovery are therefore future specialized estimator profiles, not evidence that ordinary unquantized MUSIC is automatically compatible with one-bit data.

## 9.14 Floating-point samples, ADC codes, dequantized values, and FPGA fixed point

GeoDOA shall distinguish at least four numerical meanings:

1. **Analog-equivalent / pre-ADC sample value** represented numerically in floating point for simulation.
2. **ADC output code** with declared code width, coding, full-scale map, and saturation semantics.
3. **Dequantized numerical value** obtained by mapping the code back to declared physical/normalized units.
4. **DSP/FPGA fixed-point value** created later by digital arithmetic with its own word length, scaling, rounding, overflow, and saturation behavior.

A Python `float64` array can represent an ideal analog-equivalent sampled model; its machine precision is not the ADC resolution. Conversely, converting ADC codes to `float64` does not undo acquisition quantization.

FPGA arithmetic effects belong to implementation/numerical realization and must not be double counted as ADC quantization. The final hardware co-design flow may contain both effects, but their provenance and insertion stages remain separate.

## 9.15 Calibration, characterization, and provenance

Receiver/ADC calibration and characterization may include, as applicable:

- ADC gain and offset error;
- transition-level / DNL / INL characterization;
- channel full-scale range and code mapping;
- channel gain/phase response and gain-state tables;
- I/Q amplitude/phase imbalance and DC/LO leakage;
- clipping/overrange statistics;
- ENOB/SINAD/SNR/THD/SFDR test condition;
- P1dB/IIP2/IIP3 or another receiver-linearity characterization;
- aperture jitter/clock source and correlation topology;
- temperature, sample rate, center frequency, bandwidth, analog gain/AGC state, and supply/reference conditions.

A calibration artifact shall state whether it corrects raw ADC codes, dequantized values, complex baseband samples, covariance, or a processing manifold. Corrections at different stages need not commute.

A receiver characterized at one gain state, sample rate, center frequency, or temperature shall not silently be assumed valid in another state.

## 9.16 Small deterministic checks

### Ideal 12-bit quantizer

For an ideal \(12\)-bit uniform converter with

\[
V_{\rm FSR}=2\ \text{V},
\]

\[
\boxed{\Delta=\frac{2}{4096}
=4.8828125\times10^{-4}\ \text{V}
\approx488.28\ \mu\text{V}}.
\]

Under the classical uniform-error approximation,

\[
\boxed{\sigma_q=\frac{\Delta}{\sqrt{12}}
\approx140.95\ \mu\text{V}}.
\]

For an ideal full-scale sinusoid,

\[
\boxed{\operatorname{SNR}_q
\approx6.02(12)+1.76=74.0\ \text{dB}}.
\]

These values are ideal-reference calculations, not a prediction of a real 12-bit ADC's ENOB.

### Jitter-limited SNR

For \(\sigma_t=1\ \text{ps RMS}\),

\[
\operatorname{SNR}_{\rm jitter}(100\ \text{MHz})
\approx64.04\ \text{dB},
\]

while

\[
\operatorname{SNR}_{\rm jitter}(1\ \text{GHz})
\approx44.04\ \text{dB}.
\]

The same clock jitter therefore becomes much more restrictive as analog input frequency increases.

### Constant DC offset and second moment

Let

\[
\mathbf R_x=\mathbf I_2,
\qquad
\mathbf d=\begin{bmatrix}0.5\\0.5\end{bmatrix}.
\]

Then the uncentered second moment is

\[
\mathbf R_y^{(2)}
=\mathbf I_2+
\begin{bmatrix}0.25&0.25\\0.25&0.25\end{bmatrix}
=
\begin{bmatrix}1.25&0.25\\0.25&1.25\end{bmatrix},
\]

with eigenvalues \(1.5\) and \(1.0\). A common constant offset has therefore created a rank-one second-moment mode even though the underlying covariance was identity. Exact centering removes this deterministic offset in the ideal stationary case.

These are exploration checks, not new formal GRP numbers.

## 9.17 Scientific verification notes

The 3.7 contract is grounded in several established technical lineages:

- classical quantization theory, including Bennett's analysis of quantized-signal spectra and the later Widrow quantization-noise framework that explains when a nonlinear uniform quantizer may be approximated by additive noise;
- IEEE ADC terminology/test practice, particularly the IEEE 1241 family for sampled/quantized converter characterization;
- standard ADC engineering results for \(\Delta^2/12\), ideal full-scale sine \(6.02N+1.76\) dB, SINAD/ENOB, overrange behavior, and aperture-jitter limitations;
- classical RF receiver theory for cascaded noise, gain staging, compression, intercept points, and dynamic-range tradeoffs;
- quadrature-receiver impairment theory in which I/Q imbalance is naturally widely linear and can introduce conjugate-image terms and pseudocovariance dependence;
- quantized array-processing literature, including arcsine-law covariance relations and one-bit MUSIC/DOA methods, demonstrating that severe quantization is an estimator-model issue rather than merely an additive-noise penalty.

These sources justify the contract boundaries and candidate models. Formal ADR-003 evidence and acceptance still require Gates A–F after Explorations 3.8–3.14.

## 9.18 Candidate decisions from Exploration 3.7

- **3.7-D1** — Analog receiver impairments, ADC sampling/quantization, and downstream DSP/FPGA arithmetic are separate stages with explicit provenance.
- **3.7-D2** — An ideal uniform ADC profile shall declare full-scale span, nominal bit resolution, code/coding semantics, quantizer convention, and overload behavior.
- **3.7-D3** — For the declared ideal uniform specialization, \(\Delta=V_{\rm FSR}/2^{N_b}\).
- **3.7-D4** — The in-range nearest-level error bound \(|e_q|\le\Delta/2\) is distinct from a stochastic quantization-noise model.
- **3.7-D5** — Treating quantization error as independent white uniform noise is an approximation with validity assumptions, not a universal property of quantizers.
- **3.7-D6** — The variance \(\Delta^2/12\) is used only under the declared classical uniform-error assumptions.
- **3.7-D7** — The \(6.02N+1.76\) dB result is an ideal full-scale-sine quantization reference, not a generic SNR law.
- **3.7-D8** — Nominal ADC bits and ENOB are distinct; ENOB is a test-condition-dependent dynamic metric tied to SINAD under its declared convention.
- **3.7-D9** — SNR, SINAD, THD, SFDR, ENOB, and dynamic range remain distinct metrics.
- **3.7-D10** — `dBFS` requires an explicit full-scale reference convention.
- **3.7-D11** — Saturation/clipping is a nonlinear overrange condition and shall not be modeled as ordinary in-range quantization noise.
- **3.7-D12** — Overrange/clipping diagnostics and affected-sample provenance should be retained when available.
- **3.7-D13** — Receiver thermal/electronic noise and ADC quantization error are different physical/statistical sources.
- **3.7-D14** — Receiver noise covariance need not be spatially white or channel independent.
- **3.7-D15** — Analog gain before quantization and digital scaling after quantization are not equivalent operations.
- **3.7-D16** — Gain staging explicitly trades sensitivity/noise figure, ADC utilization, headroom, compression/clipping, and linearity/SFDR.
- **3.7-D17** — AGC state is measurement provenance; common, channel-dependent, static, and time-varying AGC modes have different spatial/statistical consequences.
- **3.7-D18** — Common scalar AGC can preserve instantaneous normalized manifold direction but can still alter temporal weighting and absolute signal/noise levels.
- **3.7-D19** — Channel-dependent/time-varying AGC can create relative manifold distortion and covariance nonstationarity.
- **3.7-D20** — Small sampling jitter produces an error proportional to waveform derivative; jitter sensitivity therefore grows with signal frequency/slew rate.
- **3.7-D21** — The classical sinusoidal jitter-limited SNR formula is a specialized RMS result, not a universal jitter model.
- **3.7-D22** — Common, differential, and correlated jitter remain distinguishable through clock-tree provenance.
- **3.7-D23** — Constant receiver DC offset contributes a rank-one term to an uncentered second moment when the underlying signal is zero mean.
- **3.7-D24** — Centered covariance can remove a truly constant offset ideally, but finite-sample/drifting/DC-near-signal cases require explicit handling.
- **3.7-D25** — I/Q imbalance is generally a widely linear impairment involving both \(\mathbf x\) and \(\mathbf x^*\), not merely an ordinary complex gain.
- **3.7-D26** — I/Q-imbalanced covariance can depend on pseudocovariance; augmented/widely linear statistics remain a future compatible extension.
- **3.7-D27** — Receiver compression/nonlinearity violates linear superposition and can create source-dependent intermodulation products.
- **3.7-D28** — P1dB, IIP2/IIP3, THD, and SFDR are distinct characterization metrics and are not direct interchangeable model coefficients.
- **3.7-D29** — Analog compression and ADC clipping are different nonlinear stages.
- **3.7-D30** — Exact nonlinear/quantized covariance is defined by \(E[\mathcal F(\mathbf x)\mathcal F(\mathbf x)^H]\); an additive white-noise reduction requires explicit assumptions.
- **3.7-D31** — Equal spatially white additive quantization noise may preserve eigenvectors in a restricted model; unequal/correlated/signal-dependent quantization need not.
- **3.7-D32** — Very coarse and one-bit quantization shall not default to the high-resolution \(\Delta^2/12\) model.
- **3.7-D33** — Arcsine-law/one-bit covariance methods are specialized statistical estimator regimes with explicit Gaussian/normalization assumptions.
- **3.7-D34** — Floating-point analog-equivalent samples, raw ADC codes, dequantized values, and FPGA/DSP fixed-point values are distinct numerical meanings.
- **3.7-D35** — Converting ADC codes to floating point does not recover information lost during acquisition quantization.
- **3.7-D36** — FPGA fixed-point quantization shall not be double counted as ADC quantization; each insertion stage retains separate scaling/rounding/overflow semantics.
- **3.7-D37** — Receiver/ADC calibration must state the data stage it corrects and the operating domain over which it is valid.
- **3.7-D38** — Calibration/characterization provenance may include gain state, sample rate, center frequency, bandwidth, clock, full scale, coding, temperature, I/Q state, linearity, and overrange conditions as applicable.
- **3.7-D39** — The initial Phase-1 validated profile may remain an ideal unquantized linear receiver represented in floating point while preserving explicit receiver/ADC extension contracts.
- **3.7-D40** — Later receiver profiles must declare estimator compatibility rather than silently feeding clipped, nonlinear, or severely quantized data into algorithms derived for an ideal linear covariance model.

---

# 10. Reserved Golden Reference Problems for ADR-003

The Phase 0C roadmap reserves:

- **GRP-014 — Position-error phase distortion**
- **GRP-015 — Gain/phase mismatch**
- **GRP-016 — Mutual-coupling manifold distortion**
- **GRP-017 — Coupling to covariance to eigenspace distortion**

Current conceptual seeds:

### GRP-014 seed

Two-sensor half-wavelength array, known spacing perturbation, known source direction. Verify

\[
\delta d\rightarrow\delta\phi\rightarrow\hat u\rightarrow\Delta\theta,
\]

plus a rigid-translation invariant subcase.

### GRP-015 seed

Use common-phase and relative-phase subcases to verify covariance/spatial invariance versus analytical two-sensor DOA bias.

### GRP-016 seed

For \(u_0=0.5\), \(\mathbf a=[1,-j]^T\), and \(\mathbf C=[[1,0.5],[0.5,1]]\),

\[
\mathbf b=\mathbf C\mathbf a=[1-0.5j,\ 0.5-j]^T,
\]

\[
\frac{b_2}{b_1}=0.8-0.6j,
\]

whose phase is approximately \(-36.87^\circ\), yielding nominal uncoupled phase-match estimate \(\hat u\approx0.20483\) instead of \(0.5\).

### GRP-017 seed

For the GRP-016 case with unit source power,

\[
\mathbf R_{\rm sig}=\mathbf b\mathbf b^H
=\begin{bmatrix}1.25&1+0.75j\\1-0.75j&1.25\end{bmatrix},
\]

with eigenvalues \(\{2.5,0\}\). Adding unit white noise gives eigenvalues \(\{3.5,1\}\). Nominal/coupled squared alignment is \(0.8\), leaving complementary normalized nominal projection \(0.2\) into the physical noise subspace.

These remain seeds until formal Gate E evidence is created.

---

# 11. Non-Negotiable Cross-ADR Rules Already Inherited

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

# 12. Immediate Next Step — Exploration 3.8 Unified Sensor-Imperfection Operator

The next work session must start at **3.8 — Unified Sensor-Imperfection Operator**, not redo 3.1–3.7 unless a contradiction is found.

Exploration 3.8 must reconcile at least:

1. which imperfections alter geometry/propagation before any channel operator exists;
2. which effects are diagonal linear, cross-channel linear, conjugate/widely linear, time-varying, stochastic additive, sampling-time, quantizing, or nonlinear;
3. which operators can be composed as matrices and which require general functions/operators;
4. the physically meaningful ordering among element response, coupling/loading, electronic gain/phase/delay, I/Q conversion, receiver noise, sampling, ADC quantization, and post-acquisition processing;
5. source-dependent versus receiver-state-dependent operators;
6. common versus relative/projective effects;
7. noise injection points and how they transform under downstream operators;
8. time/frequency dependence and snapshot compatibility;
9. how embedded/full-wave/measured manifolds bypass or absorb portions of a parametric decomposition without double counting;
10. how the unified model exposes estimator compatibility rather than hiding incompatible effects behind one `imperfection_matrix`;
11. what the minimal Phase-1 ideal profile instantiates from the unified contract;
12. what metadata/provenance is required so that later calibration, covariance propagation, and hardware implementation remain scientifically traceable.

Do not start Gate A yet.

---

# 13. Acceptance Status

As of this checkpoint:

```text
ADR-001 — ACCEPTED — Gates A–F PASS
ADR-002 — ACCEPTED — Gates A–F PASS
ADR-003 — EXPLORATION IN PROGRESS
    3.1 COMPLETE
    3.2 COMPLETE
    3.3 COMPLETE
    3.4 COMPLETE
    3.5 COMPLETE
    3.6 COMPLETE
    3.7 COMPLETE
    3.8 NEXT
    3.9–3.14 PENDING
    Gates A–F NOT STARTED
ADR-004 — NOT STARTED
```

No statement in this checkpoint may be treated as an accepted ADR-003 contract until the remaining exploration, Gates A–F, cross-gate reconciliation, and final acceptance are completed.
