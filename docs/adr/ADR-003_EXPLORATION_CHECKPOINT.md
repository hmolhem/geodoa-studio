# ADR-003 — Exploration Checkpoint

- **Working title:** Sensor Imperfections, Mutual Coupling, and Calibration
- **Phase:** 0C — Scientific Foundations
- **Status:** EXPLORATION COMPLETE — NOT ACCEPTED
- **Branch:** `docs/phase0c-scientific-conventions`
- **Depends on:** `ADR-001-coordinate-direction-spatial-conventions.md`, `ADR-002-wave-propagation-signal-measurement-model.md`, `PHASE0C_SCIENTIFIC_CONTRACTS_ROADMAP.md`
- **Completed exploration sections:** 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 3.10, 3.11, 3.12, 3.13, 3.14
- **Next step:** Draft governing ADR-003 and perform pre-Gate consistency review
- **Acceptance gates:** Not started for ADR-003
- **Reserved Golden Reference Problems:** GRP-014 through GRP-017

> This document is a continuation checkpoint, not the governing accepted ADR. Candidate decisions below remain subject to the governing ADR draft, Gates A–F, Golden Reference evidence, boundary/failure analysis, cross-ADR audit, and final acceptance. Dedicated exploration records for Sections 3.7–3.14 are authoritative for those later exploration sections.

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
3.1  Ideal / Physical / Calibrated Manifold                  COMPLETE
3.2  Position Error and Geometry Perturbation                COMPLETE
3.3  Gain and Phase Mismatch                                 COMPLETE
3.4  Element Pattern and Polarization                        COMPLETE
3.5  Mutual Coupling                                         COMPLETE
3.6  Channel Delay, Clock Skew, and Frequency Error          COMPLETE
3.7  Quantization / Receiver / Dynamic-Range Effects         COMPLETE
3.8  Unified Sensor-Imperfection Operator                    COMPLETE
3.9  Calibration Models                                      COMPLETE
3.10 Direct Measured / CST-Derived Manifold Calibration      COMPLETE
3.11 Error Metrics and Identifiability                       COMPLETE
3.12 Covariance / Eigenspace / MUSIC Error Propagation       COMPLETE
3.13 Compatibility and Initial ADR-003 Profile               COMPLETE
3.14 Cross-Section Reconciliation                            COMPLETE
```

After exploration 3.14, ADR-003 enters the standard Phase 0C acceptance sequence only after a governing ADR draft exists and passes a pre-Gate consistency review:

```text
Governing ADR-003 draft
        ↓
Pre-Gate consistency review
        ↓
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

If \(\mathbf G=c\mathbf I\), the physical manifold differs by a common complex scale. Common phase does not constitute spatial distortion; common gain can change absolute amplitude/power and, depending on physical stage/noise ordering, can change effective SNR/dynamic range even when a normalized subspace direction is unchanged.

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
- **3.3-D5** — Common gain may be projectively irrelevant for some DOA tasks while remaining relevant to calibrated amplitude/power and, depending on physical stage ordering, dynamic range/SNR.
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
- **3.4-D11** — A common identical element response may preserve normalized single-source manifold direction while changing signal level/SNR according to the physical signal/noise stage ordering.
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
\boxed{
y_n=\sum_{m=1}^{N}C_{nm}x_m
}
\]

with nonzero off-diagonal terms.

At a single operating point, one coupled response vector may sometimes be fitted numerically by a diagonal operator. Such a fit does not establish that the underlying physical interaction is diagonal and generally need not transfer to another direction, polarization, frequency, loading state, or array configuration.

## 7.2 Receive multiport semantics before an effective coupling matrix

GeoDOA shall not begin the physical definition of coupling by assuming universally that

\[
\mathbf a_c=\mathbf C\mathbf a.
\]

A more defensible receive-array starting point is a declared linear multiport representation.

Let

\[
\boxed{\mathbf v_{\rm oc}}
\]

be the **array-defined open-circuit receive-response vector** under a specified incident field and EM/modeling convention. It is not automatically an uncoupled geometry-only steering vector. Depending on how it was obtained, it may already reflect array interaction physics.

Let the antenna-array impedance matrix be

\[
\boxed{
\mathbf Z_A=
\begin{bmatrix}
Z_{11}&Z_{12}&\cdots\\
Z_{21}&Z_{22}&\cdots\\
\vdots&\vdots&\ddots
\end{bmatrix}
}
\]

and let \(\mathbf Z_L\) denote the declared receiver/load termination matrix.

Under a declared Thevenin-style multiport current/voltage convention for which the corresponding inverses exist,

\[
\boxed{
\mathbf i
=(\mathbf Z_A+\mathbf Z_L)^{-1}\mathbf v_{\rm oc}
}
\]

and loaded terminal voltage is

\[
\boxed{
\mathbf v_L
=\mathbf Z_L(\mathbf Z_A+\mathbf Z_L)^{-1}\mathbf v_{\rm oc}.
}
\]

Define, within that declared convention,

\[
\boxed{
\mathbf T_L
=\mathbf Z_L(\mathbf Z_A+\mathbf Z_L)^{-1}
}
\]

so that

\[
\mathbf v_L=\mathbf T_L\mathbf v_{\rm oc}.
\]

This is a **loaded-port transform**, not a universal definition of a DOA coupling matrix. It is scientifically meaningful only together with the definitions of \(\mathbf v_{\rm oc}\), port current/voltage sign convention, reference planes, \(\mathbf Z_A\), \(\mathbf Z_L\), frequency, and physical configuration.

If the available starting response is an isolated-element or geometry-only manifold rather than the array-defined open-circuit response, another explicit EM/effective mapping may be required before the loaded-port relation is scientifically valid. GeoDOA must not assume that \(\mathbf Z_A\) loading alone transforms an isolated geometry steering vector into a complete full-wave receive manifold.

## 7.3 Effective cross-channel coupling specialization

For a bounded model, GeoDOA may use

\[
\boxed{
\mathbf a_c(\xi)=\mathbf C(\chi)\mathbf a_{\rm ref}(\xi)
}
\]

where \(\xi\) denotes source-condition variables and \(\chi\) denotes sensor/system configuration variables.

However, the semantic type of \(\mathbf C\) must be declared. At least the following meanings are distinct:

1. **Physical/network-derived operator** — obtained from a declared multiport/loading model and defined between explicit port quantities.
2. **Effective manifold operator** — maps one declared response model to another over a declared calibration/model domain.
3. **Aggregate empirical operator** — fitted from data and potentially absorbing multiple physical effects, in which case it must not be labeled pure mutual coupling without evidence.

Therefore

\[
\boxed{
\mathbf a_c=\mathbf C\mathbf a
\text{ is a declared specialization, not a universal electromagnetic law.}
}
\]

## 7.4 Impedance, scattering, and effective-coupling semantics

Impedance parameters use port voltage/current semantics,

\[
\mathbf v=\mathbf Z\mathbf i,
\]

whereas scattering parameters use incident/reflected port-wave semantics,

\[
\boxed{
\mathbf b_{\rm wave}=\mathbf S\mathbf a_{\rm wave}.
}
\]

The port-wave symbol \(\mathbf a_{\rm wave}\) must never be confused with a steering/manifold vector.

For a common real scalar reference impedance \(Z_0\) and the corresponding conventional wave normalization, one familiar conversion is

\[
\boxed{
\mathbf S
=(\mathbf Z-Z_0\mathbf I)(\mathbf Z+Z_0\mathbf I)^{-1}
}
\]

with the inverse relation

\[
\boxed{
\mathbf Z
=Z_0(\mathbf I+\mathbf S)(\mathbf I-\mathbf S)^{-1}
}
\]

when the required inverses exist.

Unequal or complex reference impedances require their own explicit normalization/conversion convention. Consequently, \(\mathbf Z\), \(\mathbf S\), an effective receive coupling matrix \(\mathbf C\), a loaded-port transform \(\mathbf T_L\), and a measured/full-wave manifold are not directly interchangeable scientific objects.

In particular,

\[
\boxed{S_{21}\neq C_{21}}
\]

as a general scientific statement. A measured or simulated S-parameter cannot be copied directly into a DOA coupling matrix without a declared derivation and port/reference/load semantics.

## 7.5 What depends on direction, polarization, frequency, and configuration

For a passive linear time-invariant array in a fixed configuration, network matrices such as \(\mathbf Z_A(f)\) and \(\mathbf S(f)\) characterize the multiport system and are not generated anew merely because the incident source direction changes.

The receive excitation is source-condition dependent:

\[
\boxed{
\mathbf v_{\rm oc}
=\mathbf v_{\rm oc}(\hat{\mathbf u},f,\mathbf p,\ldots).
}
\]

Thus

\[
\mathbf v_L
=\mathbf T_L(f,\text{configuration})
\mathbf v_{\rm oc}(\hat{\mathbf u},f,\mathbf p,\ldots).
\]

An effective \(\mathbf C\) fitted directly between a geometry-only manifold and a full physical manifold may itself appear direction- or polarization-dependent because it may be absorbing embedded-element response and other effects in addition to network coupling.

The following dependence classes shall therefore remain distinguishable:

\[
\boxed{
\text{network-parameter dependence}
\neq
\text{source-excitation dependence}
\neq
\text{effective-manifold-operator dependence}.
}
\]

Coupling-related physical response can also depend on element geometry, spacing, frequency, material/platform/radome environment, matching networks, receiver loading, active/terminated port state, and physical configuration.

## 7.6 Symmetry, Toeplitz, circulant, and banded approximations

Reciprocity under compatible conventions can justify symmetric network quantities such as

\[
Z_{nm}=Z_{mn},
\]

but **symmetric does not mean Hermitian**.

A symmetric Toeplitz coupling matrix is a useful specialization for some idealized translationally uniform arrays:

\[
\mathbf C=
\begin{bmatrix}
c_0&c_1&c_2&\cdots\\
c_1&c_0&c_1&\cdots\\
c_2&c_1&c_0&\cdots\\
\vdots&\vdots&\vdots&\ddots
\end{bmatrix}.
\]

However, a finite ULA has edge elements with different electromagnetic neighborhoods from interior elements. Exact Toeplitz structure is therefore not a universal physical law for finite arrays.

Likewise, a circulant matrix is not the default physical model for an ordinary finite ULA; it requires periodic/circular symmetry or another explicit justification.

A nearest-neighbor or banded approximation,

\[
C_{nm}=0,
\qquad |n-m|>P,
\]

is a truncation model that requires evidence or a declared approximation policy. It must not be inferred merely from the fact that coupling often weakens with separation.

Further, even if a chosen impedance interaction model is sparse or banded,

\[
(\mathbf Z_A+\mathbf Z_L)^{-1}
\]

can be dense. Therefore sparse/banded mutual impedance does not imply a sparse/banded effective loaded transform.

## 7.7 Embedded-element patterns and prevention of double counting

An embedded element pattern is obtained for an element while it is embedded in the array and the other ports are terminated according to a declared reference/termination condition. Such a pattern incorporates interaction with neighboring elements.

Therefore the following are distinct:

- isolated-element response;
- embedded-element response;
- full-wave/full-array complex manifold;
- direct measured manifold;
- separately parameterized coupling operator.

If a CST/full-wave or measured response already contains mutual-coupling physics, GeoDOA shall not silently apply another coupling matrix to it.

The governing rule is

\[
\boxed{
\text{effect already embedded in response}
\not\Rightarrow
\text{apply the same effect again}
}
\]

unless explicit de-embedding/re-embedding provenance proves that the decomposition is valid.

This requires future calibration/manifold artifacts to preserve an explicit **included-effects / de-embedding provenance** record.

## 7.8 Operator ordering

A physically interpretable receive chain may conceptually contain

```text
incident field
    ↓
geometry / propagation
    ↓
element / open-circuit receive response
    ↓
port/network loading and cross-channel interaction
    ↓
receiver electronics
    ↓
measurement
```

For one declared specialization this may produce a form such as

\[
\mathbf a_{\rm phys}=\mathbf G\mathbf T_L\mathbf a_{\rm oc},
\]

but this is not yet the final universal ADR-003 operator ordering.

If \(\mathbf P\) represents isolated-element response, an explicit coupling/loading operator may legitimately follow it. If \(\mathbf P\) represents embedded-element response, applying a separate coupling operator may double count array interaction.

Moreover, in general,

\[
\boxed{
\mathbf C\mathbf P\neq\mathbf P\mathbf C.
}
\]

The unified ordering contract is intentionally deferred to Exploration 3.8 after channel timing/frequency and receiver effects have also been explored.

## 7.9 Manifold and covariance distortion

For the declared linear specialization

\[
\mathbf x
=\mathbf C\mathbf A\mathbf s+\mathbf n,
\]

where the shown noise is injected after the coupling block,

\[
\boxed{
\mathbf R_{\rm sig,c}
=\mathbf C\mathbf A\mathbf R_s\mathbf A^H\mathbf C^H
=\mathbf C\mathbf R_{\rm sig}\mathbf C^H.
}
\]

The rank obeys

\[
\boxed{
\operatorname{rank}(\mathbf C\mathbf R\mathbf C^H)
\le
\min\{\operatorname{rank}(\mathbf C),\operatorname{rank}(\mathbf R)\}.
}
\]

If \(\mathbf C\) is nonsingular,

\[
\boxed{
\operatorname{rank}(\mathbf C\mathbf R\mathbf C^H)
=\operatorname{rank}(\mathbf R).
}
\]

Nonsingular coupling can therefore preserve signal-covariance rank while changing eigenvalues, eigenvectors, subspace orientation, and numerical conditioning. Rank-deficient coupling can reduce observable rank.

## 7.10 MUSIC consequence

For one source let

\[
\mathbf b=\mathbf C\mathbf a(\theta_0).
\]

With post-coupling spatially white noise,

\[
\mathbf R_x
=\sigma_s^2\mathbf b\mathbf b^H+\sigma_n^2\mathbf I.
\]

The physical signal eigenvector is aligned with

\[
\frac{\mathbf b}{\|\mathbf b\|_2},
\]

not generally with the nominal manifold direction

\[
\frac{\mathbf a}{\|\mathbf a\|_2}.
\]

The physical noise subspace satisfies

\[
\boxed{
\mathbf E_n^H\mathbf b=0.
}
\]

If classical MUSIC is evaluated with the mismatched nominal manifold, then at the true DOA generally

\[
\boxed{
\mathbf E_n^H\mathbf a(\theta_0)\neq0.
}
\]

Thus the MUSIC algebra has not failed; the model supplied to MUSIC is mismatched to the physical coupled manifold.

## 7.11 Noise ordering

Coupling and noise injection do not commute semantically.

If

\[
\mathbf x
=\mathbf C(\mathbf A\mathbf s+\mathbf n_{\rm pre})
+\mathbf n_{\rm post},
\]

then, under the corresponding independence assumptions,

\[
\boxed{
\mathbf R_x
=
\mathbf C\mathbf A\mathbf R_s\mathbf A^H\mathbf C^H
+
\mathbf C\mathbf R_{n,\rm pre}\mathbf C^H
+
\mathbf R_{n,\rm post}.
}
\]

Even if

\[
\mathbf R_{n,\rm pre}=\sigma^2\mathbf I,
\]

then

\[
\mathbf C\mathbf R_{n,\rm pre}\mathbf C^H
=\sigma^2\mathbf C\mathbf C^H,
\]

which is not spatially white unless the relevant scaled-unitary condition is satisfied.

Detailed receiver-noise generation belongs later in ADR-003, but the ordering distinction is already mandatory.

## 7.12 Inverse decoupling and conditioning

Suppose a bounded effective model is

\[
\mathbf x=\mathbf C\mathbf a s+\mathbf n
\]

and calibration provides \(\hat{\mathbf C}\).

Data correction may attempt

\[
\mathbf y=\hat{\mathbf C}^{-1}\mathbf x.
\]

Then

\[
\boxed{
\mathbf y
=\hat{\mathbf C}^{-1}\mathbf C\mathbf a s
+\hat{\mathbf C}^{-1}\mathbf n.
}
\]

Even for exact calibration \(\hat{\mathbf C}=\mathbf C\), noise transforms as

\[
\boxed{
\mathbf R_{n,y}
=\mathbf C^{-1}\mathbf R_n\mathbf C^{-H}.
}
\]

The inverse norm satisfies

\[
\boxed{
\|\mathbf C^{-1}\|_2
=\frac{1}{\sigma_{\min}(\mathbf C)}.
}
\]

and the spectral condition number is

\[
\boxed{
\kappa_2(\mathbf C)
=\frac{\sigma_{\max}(\mathbf C)}{\sigma_{\min}(\mathbf C)}.
}
\]

A small minimum singular value can therefore produce strong noise and calibration-error amplification. Condition number measures relative sensitivity, while the absolute inverse gain also depends on \(\sigma_{\min}\); the two diagnostics must not be conflated.

If \(\mathbf C\) is singular, exact inverse decoupling does not exist. Pseudoinverse or regularized correction is a different calibration/estimation strategy and is deferred to Exploration 3.9.

## 7.13 Residual coupling and attribution

An additive operator residual may be defined without requiring invertibility:

\[
\boxed{
\Delta\mathbf C
=\mathbf C-\hat{\mathbf C}.
}
\]

If \(\hat{\mathbf C}\) is invertible and both operators have identical semantics/domain, a relative inverse residual may also be defined:

\[
\boxed{
\mathbf E_C
=\hat{\mathbf C}^{-1}\mathbf C-\mathbf I.
}
\]

These quantities answer different questions.

A residual manifold mismatch such as

\[
\mathbf a_{\rm phys}-\mathbf a_{\rm cal}
\]

must not automatically be labeled residual mutual coupling. It may contain position, element pattern, phase center, electronics, loading, measurement, interpolation, or other errors. Physical-cause attribution requires identifiability evidence.

## 7.14 Channel dropout, masking, and termination changes

A digital channel mask applied after ADC/receiver acquisition does not necessarily change the physical antenna network if all physical ports remain in the same terminated state.

By contrast, disabling an LNA, changing an input impedance, opening/shorting a port, disconnecting an element, changing a matching network, or otherwise changing a physical termination can alter the receive network itself.

If

\[
\mathbf Z_L\rightarrow\mathbf Z_L',
\]

then generally

\[
\boxed{
\mathbf T_L'
=\mathbf Z_L'(\mathbf Z_A+\mathbf Z_L')^{-1}
\neq
\mathbf T_L.
}
\]

The physical EM/network configuration may also change enough that the appropriate \(\mathbf Z_A\), embedded response, or calibrated manifold changes.

Therefore GeoDOA shall distinguish

\[
\boxed{
\text{digital channel masking}
\neq
\text{physical port-state / termination change}.
}
\]

A coupling model for a changed termination/configuration shall not be obtained merely by deleting a row/column from an old operator unless that reduction has been explicitly derived and validated.

## 7.15 Scientific verification notes

The exploration was cross-checked against established antenna/network practice:

- mutual coupling is treated as electromagnetic interaction among array elements and may be characterized through mutual impedance, S-parameters, coupling matrices, or embedded-element patterns;
- embedded element patterns are obtained with the element embedded in the finite array and other ports terminated according to a declared impedance, and they include neighboring-element coupling effects;
- S-to-impedance conversion depends on declared port/reference impedances, reinforcing that S-parameters are not standalone DOA coupling coefficients.

These verification sources support the modeling distinctions above; they do not replace the later ADR-003 Gate evidence or Golden Reference validation.

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

GeoDOA shall not use one ambiguous `phase_error` parameter for all receiver timing and frequency imperfections. At least the following meanings are distinct:

1. **Static narrowband channel phase offset** — a complex phase intercept at a declared operating point.
2. **Physical/electrical channel delay** — a waveform delay through cable, filter, RF/IF/baseband path, or another declared channel stage.
3. **Fixed sampling-time offset / sampling-clock phase skew** — different channels sample the waveform at different physical epochs even if their sample rates are equal.
4. **Sampling-rate offset (SRO)** — channel sample periods/rates differ, causing accumulated timing drift.
5. **Sampling-time jitter** — sample-to-sample timing uncertainty, distinct from deterministic skew/drift.
6. **Receiver-reference/LO phase offset** — static oscillator/reference phase difference.
7. **Receiver-reference/LO frequency offset** — time derivative of receiver-reference phase error.
8. **Digital transport / processing latency** — post-acquisition arrival or pipeline delay, which is not automatically a physical sample-time error.

The phrase `clock skew` is therefore too ambiguous to serve as a complete scientific parameter. APIs and reports should distinguish fixed sampling-time offset, sampling-rate offset, and jitter.

## 8.2 Physical channel delay and the GeoDOA sign convention

Let \(\delta\tau_n\) be a declared additional physical/electrical delay in channel \(n\) relative to a reference channel/stage. A pure delay acts as

\[
\boxed{
y_n(t)=x_n(t-\delta\tau_n).
}
\]

Under the accepted GeoDOA Fourier convention,

\[
x(t-\tau)\longleftrightarrow X(\omega)e^{+j\omega\tau},
\]

so the delay transfer factor is

\[
\boxed{
H_{\tau,n}(\omega)=e^{+j\omega\delta\tau_n}.
}
\]

For an RF signal represented by the complex envelope convention

\[
x_{\rm RF}(t)=\Re\{s(t)e^{-j\omega_c t}\},
\]

an additional channel delay produces

\[
\boxed{
s(t-\delta\tau_n)e^{+j\omega_c\delta\tau_n}.
}
\]

Therefore a physical delay contains two effects that must not be conflated:

- envelope/time alignment through \(s(t-\delta\tau_n)\);
- carrier-frequency phase \(e^{+j\omega_c\delta\tau_n}\).

If the envelope delay is negligible under a declared narrowband approximation,

\[
s(t-\delta\tau_n)\approx s(t),
\]

then the delay may be approximated at carrier frequency by a diagonal phase operator

\[
\boxed{
\mathbf D_{\tau,c}
=\operatorname{diag}
\left(e^{+j\omega_c\delta\tau_1},\ldots,e^{+j\omega_c\delta\tau_N}\right).
}
\]

This phase-only form is an approximation to a physical delay, not its general definition.

## 8.3 Delay slope versus static phase offset

For a pure delay,

\[
\phi_{\tau,n}(\omega)=\omega\delta\tau_n,
\]

so

\[
\boxed{
\frac{d\phi_{\tau,n}}{d\omega}=\delta\tau_n.
}
\]

This is consistent with ADR-002's accepted GeoDOA group-delay sign convention

\[
\tau_g=+\frac{d\phi}{d\omega}.
\]

By contrast, an ideal static phase offset

\[
H_{\phi,n}=e^{j\phi_{0,n}}
\]

has zero phase slope with frequency.

Consequently,

\[
\boxed{
\text{static phase offset}
\neq
\text{physical delay}
}
\]

as physical models, even though a single-frequency measurement may be unable to distinguish them.

A useful parametric local response can therefore contain both intercept and slope,

\[
\boxed{
H_n(\omega)
\approx
\rho_n(\omega)
\exp\{j[\phi_{0,n}+\omega\delta\tau_n]\},
}
\]

over a declared validity band. Higher-order phase curvature represents dispersion/filter behavior beyond a pure delay.

## 8.4 Channel-delay narrowband compatibility

Let the relative additional channel-delay spread be

\[
\boxed{
\Delta\tau_{\rm ch}
=\max_n\delta\tau_n-
\min_n\delta\tau_n.
}
\]

For spectral offsets \(|\nu|\le\nu_{\max}\), define the diagnostic

\[
\boxed{
\eta_{\rm ch-delay}
=2\pi\nu_{\max}\Delta\tau_{\rm ch}.
}
\]

This has the same scientific logic as ADR-002's aperture bandwidth-delay diagnostic, but it describes **receiver/channel differential delay**, not propagation-aperture delay.

GeoDOA does not prescribe a universal PASS/FAIL threshold here. A threshold belongs to a later validation/compatibility policy. If the declared tolerance makes the residual envelope shift negligible, a carrier-phase-only approximation may be used. Otherwise the channel response must remain time/frequency dependent.

## 8.5 Sampling-time model

Let the nominal processing time grid be

\[
\boxed{
t[k]=t_0+kT_s.
}
\]

A useful channel-specific acquisition-time model is

\[
\boxed{
t_n[k]
=t_0+\beta_n+kT_s(1+\epsilon_{T,n})+\eta_n[k],
}
\]

where:

- \(\beta_n\) is a fixed sampling-time offset in seconds;
- \(\epsilon_{T,n}\) is a dimensionless fractional sample-period error;
- \(\eta_n[k]\) is sample-to-sample timing jitter/uncertainty.

Thus the channel's timing error relative to the nominal grid is

\[
\boxed{
\delta t_n[k]
=\beta_n+kT_s\epsilon_{T,n}+\eta_n[k].
}
\]

If the actual sample rate is written

\[
f_{s,n}=f_s(1+\epsilon_{f,n}),
\]

then exactly

\[
\boxed{
1+\epsilon_{T,n}
=\frac{1}{1+\epsilon_{f,n}}
}
\]

and for small errors

\[
\boxed{
\epsilon_{T,n}\approx-\epsilon_{f,n}.
}
\]

GeoDOA shall preserve which fractional error is being reported; `ppm` without declaring sample-rate versus sample-period semantics is incomplete.

## 8.6 Sampling-time offset is not the same operation as channel delay

Let \(z_n(t)\) denote the continuous-time waveform at the physical point where channel \(n\) is sampled. A positive sampling-time offset means the waveform is observed later:

\[
\boxed{
y_n[k]=z_n(t[k]+\delta t_n[k]).
}
\]

For a monochromatic component under the GeoDOA temporal convention,

\[
z(t)=Ae^{-j\omega t},
\]

so

\[
\boxed{
z(t+\delta t)
=z(t)e^{-j\omega\delta t}.
}
\]

This sign is opposite to the pure physical-delay transfer factor \(e^{+j\omega\delta\tau}\) because the two operations are physically different:

```text
channel delay:      shift the waveform later, x(t) -> x(t-delta_tau)
sampling-time skew: observe the existing waveform at a later epoch, t -> t+delta_t
```

The frequency \(\omega\) in the sampling-time relation is the frequency of the waveform at the declared sampling point. Direct-RF, IF, and complex-baseband sampling therefore require explicit stage/frequency provenance.

## 8.7 Fixed skew, SRO, and jitter

The timing model separates three effects:

### Fixed sampling-time offset

If

\[
\epsilon_{T,n}=0,
\qquad
\eta_n[k]=0,
\]

then

\[
\delta t_n[k]=\beta_n.
\]

For a sufficiently narrowband signal this can sometimes be represented by a fixed phase at a declared frequency, but for a general waveform it remains a fractional-time alignment problem.

### Sampling-rate offset

If

\[
\epsilon_{T,n}\neq0,
\]

then the timing error accumulates with sample index:

\[
\boxed{
\delta t_n[k]
=\beta_n+kT_s\epsilon_{T,n}.
}
\]

For a tone, this produces a phase drift linear in \(k\). For a broadband/general waveform it is a time-warp/resampling problem and cannot generally be reduced to one fixed diagonal phase matrix.

### Sampling-time jitter

\(\eta_n[k]\) is stochastic or otherwise sample-varying timing uncertainty. It is not deterministic fixed skew or SRO. Detailed stochastic jitter/noise and ADC impairment modeling is deferred to Exploration 3.7, but the semantic distinction is locked for later reconciliation.

## 8.8 Common versus differential sampling-clock errors

Decompose fixed timing offset as

\[
\beta_n=\beta_c+\tilde\beta_n
\]

and period error as

\[
\epsilon_{T,n}=\epsilon_{T,c}+\tilde\epsilon_{T,n}.
\]

A **common** fixed timing shift can preserve relative spatial simultaneity among channels while shifting the absolute/external observation epoch. A **differential** fixed timing shift violates exact simultaneity unless an equivalent alignment/calibration operation is performed.

Likewise, a shared common sample clock can have a common rate error relative to an external reference while keeping physical channels mutually synchronized. Such an error still changes the physical time scale and can bias Doppler/frequency/time-axis interpretations.

Differential SRO is more severe for spatial coherence because relative sample epochs drift continuously across channels. Coherent processing may therefore require resampling to a common time grid, not merely multiplying by a fixed phase factor.

## 8.9 Aperture delay, aperture jitter, and processing latency

GeoDOA shall preserve three separate engineering meanings:

- **ADC aperture delay** — deterministic delay between a declared sampling-clock edge/reference and the actual sampling instant;
- **aperture/sampling jitter** — sample-to-sample uncertainty in that instant;
- **conversion/buffer/DMA/FPGA processing latency** — delay after the sample has already been physically acquired.

Channel-to-channel aperture-delay mismatch can contribute to effective fixed sampling-time offset. Jitter contributes uncertainty/noise-like timing error. Digital pipeline latency does **not** alter the physical acquisition epoch if sample identity, ordering, and timestamp/index correspondence remain correct.

Therefore

\[
\boxed{
\text{data arrives later at processing}
\not\Rightarrow
\text{signal was sampled later}.
}
\]

This distinction is mandatory for future FPGA/SoC backends and deterministic-latency reporting.

## 8.10 Receiver-reference / LO phase and frequency error

To avoid hiding mixer-sign conventions, GeoDOA can define a processed-baseband receiver-reference phase process

\[
\boxed{
\psi_n(t)
}
\]

through the multiplicative factor

\[
\boxed{e^{j\psi_n(t)}.
}
\]

Define the corresponding residual receiver-reference frequency error by

\[
\boxed{
\delta f_{\rm ref,n}(t)
=\frac{1}{2\pi}\frac{d\psi_n(t)}{dt}.
}
\]

For constant residual frequency error,

\[
\boxed{
\psi_n(t)
=\psi_n(0)+2\pi\delta f_{\rm ref,n}t.
}
\]

Thus a static oscillator/reference phase offset and a frequency offset are different models:

```text
static phase offset     -> constant phase intercept
frequency offset        -> phase that evolves with time
```

When mapping a physical LO frequency error into \(\delta f_{\rm ref,n}\), the mixer/downconversion sign convention must be declared. GeoDOA shall not infer that sign from the words `LO error` alone.

## 8.11 Common versus differential receiver-reference error

Write

\[
\psi_n(t)=\psi_c(t)+\tilde\psi_n(t).
\]

If all simultaneously observed channels receive the same common phase factor,

\[
\mathbf D_c(t)=e^{j\psi_c(t)}\mathbf I,
\]

then that factor is projectively common across the spatial snapshot. For an instantaneous outer product,

\[
\boxed{
\mathbf D_c(t)\mathbf R\mathbf D_c^H(t)=\mathbf R.
}
\]

Thus a truly common oscillator phase/frequency error need not distort an instantaneous spatial covariance/manifold direction, even though it remains important for coherent temporal processing, absolute phase/frequency interpretation, waveform demodulation, and synchronization to external systems.

Differential receiver-reference phase/frequency error is different. Define

\[
\mathbf D_f(t)
=\operatorname{diag}
\left(e^{j2\pi\delta f_1t},\ldots,e^{j2\pi\delta f_Nt}\right).
\]

Then for a static underlying spatial covariance \(\mathbf R_0\),

\[
\boxed{
\mathbf R(t)
=\mathbf D_f(t)\mathbf R_0\mathbf D_f^H(t).
}
\]

The physical signal/noise-subspace orientation can therefore drift with time.

## 8.12 Covariance-window coherence under differential frequency error

For snapshots at times \(t_k\), the \((n,m)\) covariance term under constant differential residual frequency error acquires the averaging factor

\[
\boxed{
\Gamma_{nm}
=\frac{1}{L}
\sum_{k=1}^{L}
\exp\left[j2\pi(\delta f_n-\delta f_m)t_k\right].
}
\]

Hence differential oscillator error can reduce or rotate cross-channel covariance terms when the covariance estimator averages over a window during which relative phase evolves.

For continuous uniform averaging over \([0,T]\), let

\[
\Delta f_{nm}=\delta f_n-\delta f_m.
\]

Then

\[
\boxed{
\Gamma_{nm}(T)
=e^{j\pi\Delta f_{nm}T}
\operatorname{sinc}(\Delta f_{nm}T),
}
\]

where

\[
\operatorname{sinc}(x)=\frac{\sin(\pi x)}{\pi x}.
\]

This result makes the coherence consequence explicit: relative frequency error is not merely a fixed phase bias; over a sufficiently long window it can attenuate cross-channel coherence and alter covariance rank/eigenspace behavior.

No universal acceptable \(|\Delta f|T\) threshold is declared at this exploration stage.

## 8.13 Sampling-rate offset and spatial snapshot validity

ADR-002 defines a spatial snapshot as a simultaneous-equivalent coherent observation of the declared channels. Differential SRO directly challenges that contract.

For a tone \(z(t)=Ae^{-j\omega t}\) and the deterministic sampling model,

\[
\boxed{
z(t_n[k])
=z(t[k])
\exp\{-j\omega[\beta_n+kT_s\epsilon_{T,n}]\}.
}
\]

The relative phase therefore drifts with \(k\). For a broadband waveform, the stronger statement applies: different channels are evaluating the waveform at different physical times, so coherent reconstruction generally requires interpolation/resampling or another explicitly validated equivalent construction.

An integer-sample correction and a fractional-delay/resampling correction are different operations. The latter can introduce interpolation bandwidth, filter, boundary, and noise-correlation effects that must retain provenance.

## 8.14 Physical Doppler, source frequency error, and receiver oscillator error

ADR-002's Doppler is a propagation/path phenomenon caused by motion. Receiver-reference/LO frequency error is an instrumentation phenomenon. Source carrier uncertainty is a source/waveform phenomenon.

These may all contribute to an observed residual temporal frequency, but they remain scientifically distinct:

\[
\boxed{
\text{physical Doppler}
\neq
\text{source-frequency uncertainty}
\neq
\text{receiver LO/reference error}.
}
\]

A single narrowband observation may not make these causes identifiable without a known reference, calibration waveform, motion model, or additional measurements.

If the sampling clock and LO are derived from the same physical oscillator/reference, their errors may be correlated or share one fractional-frequency cause. GeoDOA shall preserve shared-reference provenance rather than assuming independent random errors by default.

## 8.15 Non-simultaneous / TDM MIMO implication

A common temporal phase process can become a **relative virtual-channel phase** when channels used to construct one virtual-array snapshot are acquired at different physical times.

If virtual channel \(q\) is observed at time \(t_q\), a common evolving phase \(e^{j\psi(t)}\) contributes

\[
\boxed{e^{j\psi(t_q)}
}
\]

which is no longer common across the assembled virtual-channel vector unless \(\psi(t_q)\) is effectively constant or explicitly corrected.

Therefore common CFO/Doppler/oscillator phase that is harmless to a truly simultaneous physical Rx snapshot may distort a TDM-MIMO virtual manifold. Snapshot construction must preserve acquisition-time provenance and any synchronization/phase compensation used to create a simultaneous-equivalent view.

## 8.16 Calibration and identifiability

Timing/frequency calibration must declare exactly what is being estimated:

- fixed phase intercept;
- physical/electrical channel delay;
- fixed sampling-time offset;
- sample-rate/period error;
- oscillator/reference phase offset;
- oscillator/reference frequency offset;
- stochastic jitter/phase-noise parameters;
- or an aggregate effective correction.

Important identifiability limits include:

1. At one frequency, a static phase offset and a delay-induced phase can be indistinguishable.
2. A frequency sweep or sufficiently broadband known calibration waveform can expose phase slope and therefore delay, subject to phase unwrapping and model validity.
3. Channel delay and sampling-time offset can produce similar effective alignment errors but represent different physical stages and opposite signed shifts under the definitions above.
4. Common clock or LO errors may be invisible to relative spatial calibration without an external reference.
5. Observed residual frequency may confound oscillator error, source-frequency error, and physical Doppler.
6. Calibration validity may change after oscillator relock, device restart, clock-tree change, sample-rate change, center-frequency change, temperature change, or receiver reconfiguration.

Calibration provenance should therefore include, as applicable, clock/LO topology, shared-reference identity, lock/restart state, center frequency, sample rate, acquisition stage, calibration waveform/bandwidth, timestamp/epoch, temperature/environment, and correction method.

Residuals must preserve their scientific type, for example

\[
\delta\tau_n^{\rm res},
\qquad
\beta_n^{\rm res},
\qquad
\epsilon_{T,n}^{\rm res},
\qquad
\delta f_n^{\rm res}.
\]

A generic `phase_residual` is insufficient when the physical error evolves across frequency or time.

## 8.17 Small deterministic checks

### Delay versus sampling-time sign

For a \(100\,\text{MHz}\) monochromatic component and a positive \(100\,\text{ps}\) physical channel delay,

\[
\Delta\phi_{\rm delay}
=2\pi(100\times10^6)(100\times10^{-12})
\approx0.06283\,\text{rad}
=+3.6^\circ.
\]

For a positive \(100\,\text{ps}\) sampling-time offset, meaning the same waveform is sampled \(100\,\text{ps}\) later,

\[
\Delta\phi_{\rm sample}
=-2\pi(100\times10^6)(100\times10^{-12})
=-3.6^\circ.
\]

At \(1\,\text{GHz}\), the magnitude becomes \(36^\circ\), demonstrating why a physical delay cannot generally be replaced by a frequency-independent phase constant.

### Sampling-rate drift

Let

\[
f_s=10\,\text{MHz}
\]

and suppose one channel's actual sample rate is high by \(+10\,\text{ppm}\):

\[
\epsilon_f=10^{-5}.
\]

Then

\[
\epsilon_T
=\frac{1}{1+10^{-5}}-1
\approx-9.9999\times10^{-6}.
\]

After approximately one nominal second of sample indexing, the channel's physical sample epoch leads the nominal grid by about \(10\,\mu\text{s}\). This is accumulated timing drift, not a fixed phase error.

### Differential frequency coherence

For two channels with

\[
\Delta f_{12}=1\,\text{Hz}
\]

and continuous covariance averaging over

\[
T=0.5\,\text{s},
\]

\[
|\Gamma_{12}|
=|\operatorname{sinc}(0.5)|
=\frac{2}{\pi}
\approx0.6366.
\]

Thus a seemingly small differential frequency error can substantially attenuate cross-channel covariance when the coherent averaging interval is long enough.

These are exploration checks, not new formal GRP numbers. GRP-014 through GRP-017 remain reserved as already defined.

## 8.18 Scientific verification notes

The exploration was cross-checked against accepted ADR-002 and established synchronization/ADC practice:

- ADR-002 defines a pure delay under the GeoDOA Fourier convention with the factor \(e^{+j\omega\tau}\), separates narrowband phase from envelope delay, and defines a spatial snapshot as simultaneous-equivalent coherent channel observation.
- Analog Devices documentation distinguishes ADC aperture delay from aperture jitter and notes that channel timing mismatch/clock skew produces frequency-dependent error.
- MathWorks synchronization documentation distinguishes carrier-frequency offset from sampling-clock offset; sampling-clock mismatch shifts sampling instants while carrier-frequency offset produces phase evolution over time.
- Sampling-rate-offset literature for asynchronous sensor arrays treats SRO as a coherence problem requiring estimation/compensation or resampling to a common time base before coherent distributed processing.

These references support the semantic distinctions above; they do not replace ADR-003's later Gates A–F or formal validation evidence.

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
- **3.6-D11** — GeoDOA shall prefer explicit `fixed sampling-time offset`, `sampling-rate offset`, and `jitter` semantics over an ambiguous bare `clock skew` parameter.
- **3.6-D12** — A useful sample-time model separates fixed offset, fractional sample-period error, and sample-to-sample jitter.
- **3.6-D13** — Fractional sample-rate error and fractional sample-period error have opposite first-order signs and must not be conflated.
- **3.6-D14** — Common fixed sampling-time offset may preserve relative spatial simultaneity while changing absolute observation epoch; differential fixed offset does not.
- **3.6-D15** — A common sample-rate error on a genuinely shared clock can preserve inter-channel synchronization while distorting the external physical time scale.
- **3.6-D16** — Differential SRO accumulates relative time drift and generally requires resampling/time-warp correction for broadband coherent processing.
- **3.6-D17** — Sampling-time jitter is distinct from deterministic skew/SRO and will be developed further with receiver/ADC effects in Exploration 3.7.
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

# 9. Reserved Golden Reference Problems for ADR-003

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

### GRP-016 seed

Use a two-sensor half-wavelength array with

\[
u_0=0.5,
\qquad
\mathbf a=
\begin{bmatrix}
1\\-j
\end{bmatrix},
\qquad
\mathbf C=
\begin{bmatrix}
1&0.5\\
0.5&1
\end{bmatrix}.
\]

Then

\[
\boxed{
\mathbf b=\mathbf C\mathbf a
=
\begin{bmatrix}
1-0.5j\\
0.5-j
\end{bmatrix}
}
\]

and the relative response is

\[
\boxed{
\frac{b_2}{b_1}=0.8-0.6j.
}
\]

Its phase is approximately \(-36.87^\circ\), whereas the nominal relative phase is \(-90^\circ\). A nominal uncoupled phase-matching model would therefore infer

\[
\boxed{
\hat u\approx0.20483
}
\]

instead of \(u_0=0.5\).

This seed exercises deterministic manifold distortion and nominal-model DOA bias. It remains a seed until formal Gate E evidence is created.

### GRP-017 seed

Continue the GRP-016 case. For unit source power,

\[
\boxed{
\mathbf R_{\rm sig}
=\mathbf b\mathbf b^H
=
\begin{bmatrix}
1.25&1+0.75j\\
1-0.75j&1.25
\end{bmatrix}
}
\]

with

\[
\|\mathbf b\|_2^2=2.5
\]

and signal-covariance eigenvalues

\[
\boxed{\{2.5,0\}}.
\]

If post-coupling white noise has variance \(\sigma_n^2=1\), then

\[
\mathbf R_x=\mathbf R_{\rm sig}+\mathbf I
\]

has eigenvalues

\[
\boxed{\{3.5,1\}}.
\]

The squared alignment between nominal and coupled manifold directions is

\[
\boxed{
\frac{|\mathbf a^H\mathbf b|^2}
{\|\mathbf a\|_2^2\|\mathbf b\|_2^2}
=0.8.
}
\]

For this two-channel, one-source case, the complementary normalized nominal-manifold projection onto the physical noise subspace is therefore \(0.2\). This seed exercises the chain

\[
\boxed{
\text{coupling}
\rightarrow
\text{manifold rotation}
\rightarrow
\text{covariance}
\rightarrow
\text{eigenspace rotation}
\rightarrow
\text{nominal-MUSIC orthogonality error}.
}
\]

It remains a seed until formal Gate E evidence is created.

---

# 10. Non-Negotiable Cross-ADR Rules Already Inherited

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

# 11. Immediate Next Step — Governing ADR-003 Draft

Exploration is complete through 3.14. The next repository step is to draft the governing ADR-003 from the reconciled contract in `ADR-003_EXPLORATION_3.14_CROSS_SECTION_RECONCILIATION.md`, then perform a pre-Gate consistency review.

The draft shall consolidate—not merely concatenate—the exploration results. It shall preserve the reconciled distinctions among:

1. nominal / physical / measured / EM / calibrated response objects;
2. geometry, element, coupling, electronics, timing, noise, nonlinear, sampling, and ADC stages;
3. physical delay versus sample-time offset/SRO/jitter;
4. calibration inference versus data correction;
5. direct measured/CST manifold calibration and included-effects/de-embedding provenance;
6. error/uncertainty/identifiability/conditioning semantics;
7. covariance/eigenspace/MUSIC propagation;
8. multi-axis estimator compatibility;
9. the bounded initial Phase-1 ideal sensor profile;
10. GRP-014 through GRP-017 reservations.

Do not start Gate A until the governing ADR draft exists and the pre-Gate review is complete.

---

# 12. Acceptance Status

As of this reconciled checkpoint:

```text
ADR-001 — ACCEPTED — Gates A–F PASS
ADR-002 — ACCEPTED — Gates A–F PASS
ADR-003 — EXPLORATION COMPLETE — NOT ACCEPTED
    3.1 COMPLETE
    3.2 COMPLETE
    3.3 COMPLETE
    3.4 COMPLETE
    3.5 COMPLETE
    3.6 COMPLETE
    3.7 COMPLETE
    3.8 COMPLETE
    3.9 COMPLETE
    3.10 COMPLETE
    3.11 COMPLETE
    3.12 COMPLETE
    3.13 COMPLETE
    3.14 COMPLETE
    Governing ADR draft: NEXT
    Gates A–F: NOT STARTED
ADR-004 — NOT STARTED
```

No statement in this checkpoint may be treated as an accepted ADR-003 contract until the governing ADR, Gates A–F, cross-gate reconciliation, and final acceptance are completed.
