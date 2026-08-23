# ADR-003 — Sensor Imperfections, Mutual Coupling, and Calibration

- **Status:** Accepted — all Phase 0C acceptance Gates A–F and final cross-gate reconciliation passed
- **Phase:** 0C — Scientific Foundations
- **Scope:** Sensor/receiver imperfections, calibration, measured/EM manifolds, mismatch propagation, and estimator compatibility
- **Depends on:** `ADR-001-coordinate-direction-spatial-conventions.md`, `ADR-002-wave-propagation-signal-measurement-model.md`, `PHASE0C_SCIENTIFIC_CONTRACTS_ROADMAP.md`
- **Exploration record:** `ADR-003_EXPLORATION_CHECKPOINT.md` and dedicated Explorations 3.7–3.14
- **Cross-section reconciliation:** `ADR-003_EXPLORATION_3.14_CROSS_SECTION_RECONCILIATION.md`
- **Pre-Gate review:** `ADR-003_PRE_GATE_CONSISTENCY_REVIEW.md`
- **Acceptance audit:** `ADR-003_ACCEPTANCE_AUDIT.md`
- **Gate C evidence:** `ADR-003_GATE_C_DIMENSIONAL_UNIT_CONSISTENCY_AUDIT.md`
- **Gate D evidence:** `ADR-003_GATE_D_SOFTWARE_SEMANTIC_CONSISTENCY_AUDIT.md`
- **Golden reference evidence:** `../science/golden_reference/ADR-003_GOLDEN_REFERENCE_PROBLEMS.md`
- **Boundary/failure evidence:** `ADR-003_BOUNDARY_FAILURE_ANALYSIS.md`
- **Gate F reconciliation:** `ADR-003_GATE_F_AUDIT.md`
- **Final cross-gate reconciliation:** `ADR-003_FINAL_CROSS_GATE_RECONCILIATION.md`
- **Final acceptance record:** `ADR-003_FINAL_ACCEPTANCE_RECORD.md`
- **Golden Reference Problems:** GRP-014 through GRP-017
- **Supersedes:** None
- **Superseded by:** None

> ADR-003 is **Accepted** as the authoritative GeoDOA scientific contract for its declared scope. Acceptance does not activate all nonideal mechanisms in Phase 1; deferred families still require named/versioned bounded implementation profiles and their own verification evidence.

---

## 1. Decision Summary

GeoDOA Studio shall model real sensor-array departures from the ideal propagation model using a **typed physical sensor/receiver operator graph**, not one universal imperfection matrix.

The project shall preserve the distinction among:

\[
\boxed{
\mathbf a_{\rm nom},
\mathbf a_{\rm phys},
\mathbf a_{\rm meas},
\mathbf a_{\rm em},
\mathbf a_{\rm cal}
}
\]

and, when explicitly available in simulation,

\[
\boxed{\mathbf a_{\rm truth}}.
\]

The physical chain is conceptually

```text
scene/source state
    -> propagation on declared physical geometry
    -> element/polarization/open-circuit response
    -> loading/mutual coupling/network response
    -> analog receiver gain/phase/delay/filter/LO/IQ response
    -> stage-specific receiver noise
    -> analog nonlinearity when active
    -> physical sampling epochs/aperture effects
    -> ADC clipping/quantization/code mapping
    -> digital measurement
    -> optional digital selection/deskew/calibration correction/DSP
```

Calibration is a separate inference/correction activity. It does not retroactively become a physical cause of the measurement.

The initial authoritative Phase-1 sensor profile remains deliberately ideal:

\[
\boxed{
\mathcal H_{\rm sensor}^{\rm Phase1}\equiv\mathcal I
}
\]

for deterministic sensor imperfections, with proper-complex spatially white equal-variance additive noise and ordinary classical MUSIC compatibility under ADR-001/ADR-002 assumptions.

Nonideal sensor families are scientifically defined here but remain implementation-deferred until each is activated through a bounded validated profile.

---

## 2. Context and Decision Drivers

An ideal array model is commonly written

\[
\mathbf x[k]=\mathbf A(\boldsymbol\theta)\mathbf s[k]+\mathbf n[k].
\]

Real arrays depart from that model through multiple physically distinct mechanisms. Treating all departures as arbitrary gain/phase noise obscures causality, calibration validity, units, reference planes, uncertainty, identifiability, and estimator consequences.

ADR-003 therefore preserves the complete engineering chain

\[
\boxed{
\text{physical cause}
\rightarrow
\text{manifold/measurement distortion}
\rightarrow
\text{covariance distortion}
\rightarrow
\text{eigenspace distortion}
\rightarrow
\text{DOA consequence}.
}
\]

A parallel calibration chain is

\[
\boxed{
\text{calibration experiment/model}
\rightarrow
\text{estimated parameters/manifold/correction}
\rightarrow
\text{residual mismatch + uncertainty}
\rightarrow
\text{post-calibration DOA consequence}.
}
\]

The principal design drivers are:

- preserve accepted ADR-001/ADR-002 sign, reference, unit, snapshot, and covariance semantics;
- preserve physical cause and reference-plane provenance;
- distinguish exact physical definitions from bounded approximations;
- prevent double counting between parametric, measured, and EM/full-wave models;
- make calibration domain and uncertainty explicit;
- connect sensor mismatch to covariance/eigenspace/MUSIC behavior;
- make estimator compatibility explicit rather than silently coercing unsupported regimes;
- keep the initial implementation profile bounded and testable.

---

## 3. Scope

ADR-003 governs:

- nominal, physical, measured, EM-simulated, calibrated, and simulation-truth manifold semantics;
- physical geometry perturbation and position error;
- electronic gain/phase mismatch;
- element response, orientation, phase-center, and polarization extension semantics;
- mutual coupling, loading, multiport/network semantics, and effective coupling specializations;
- channel delay, fixed sample-time offset, SRO, jitter, receiver-reference phase/frequency error, and digital-latency distinctions;
- receiver noise, gain staging, AGC semantics, DC offset, I/Q imbalance, nonlinearity, compression, clipping, ADC quantization, and dynamic-range semantics;
- typed sensor-imperfection operator/reference-plane ordering;
- calibration taxonomy, identifiability, correction, uncertainty, validity domain, and provenance;
- direct measured/CST/full-wave manifold calibration;
- sensor/calibration error metrics and gauge/equivalence semantics;
- covariance/eigenvalue/eigenspace/MUSIC propagation of sensor mismatch;
- estimator compatibility implications caused by sensor/receiver state;
- the bounded initial Phase-1 sensor profile and deferred profile activation rules.

---

## 4. Explicit Non-Goals

ADR-003 does not define:

- the accepted coordinate/sign conventions themselves — ADR-001 owns them;
- the accepted propagation/snapshot/covariance/source-statistics model itself — ADR-002 owns it;
- formal Monte Carlo policy, pass/fail thresholds, benchmark sweeps, or reproducibility execution — ADR-004 owns them;
- final Python class names, enums, configuration schemas, GUI controls, exception classes, serialization format, or plugin architecture;
- a universal coupling matrix valid for every array;
- a universal calibration algorithm;
- a universal manifold-error threshold;
- a universal MUSIC robustness threshold;
- FPGA/processor fixed-point arithmetic semantics.

ADC acquisition quantization is in scope; downstream FPGA/processor fixed-point quantization is a distinct later implementation domain.

---

## 5. Inherited ADR-001/ADR-002 Conventions

ADR-003 shall inherit without redefining:

### 5.1 Temporal convention

\[
\boxed{e^{-j\omega t}}.
\]

### 5.2 Look and propagation direction

\[
\boxed{\hat{\mathbf u}=\text{array-to-source look direction}}
\]

and

\[
\boxed{\hat{\mathbf k}_{\rm prop}=-\hat{\mathbf u}}.
\]

### 5.3 Geometry-only receive manifold

\[
\boxed{
a_n(\hat{\mathbf u},f)
=\exp[-jk(\mathbf r_n-\mathbf r_{\rm ref})^T\hat{\mathbf u}].
}
\]

### 5.4 Canonical 1-D angular slice

\[
\boxed{
\hat{\mathbf u}(\theta)
=\begin{bmatrix}\sin\theta\\\cos\theta\\0\end{bmatrix}
}
\]

with \(\theta=0\) at \(+y\) broadside and positive angle toward \(+x\).

### 5.5 Delay convention

\[
\boxed{
x(t-\tau)\longleftrightarrow X(\omega)e^{+j\omega\tau}}.
\]

### 5.6 Snapshot/covariance semantics

Snapshot simultaneity, second moment, covariance, centered sample covariance, source covariance rank, observed signal-subspace rank, source count, SNR typing, and physical MIMO Tx/Rx provenance remain those of ADR-002.

---

## 6. Core Response Taxonomy

### 6.1 Nominal manifold

\[
\boxed{\mathbf a_{\rm nom}}
\]

is the response predicted by nominal geometry, propagation, and nominal sensor assumptions.

### 6.2 Physical manifold

\[
\boxed{\mathbf a_{\rm phys}}
\]

is the actual deterministic coherent sensor-system response under a declared physical state.

It may exist physically without being exactly known.

### 6.3 Measured manifold

\[
\boxed{\mathbf a_{\rm meas}}
\]

is an experimental estimate of physical response and carries measurement/calibration uncertainty.

### 6.4 EM-simulated manifold

\[
\boxed{\mathbf a_{\rm em}}
\]

is a numerical electromagnetic/full-wave prediction under declared solver/model conditions.

### 6.5 Calibrated processing manifold

\[
\boxed{\mathbf a_{\rm cal}}
\]

is the response model intentionally supplied to processing after calibration/model construction.

### 6.6 Simulation truth

\[
\boxed{\mathbf a_{\rm truth}}
\]

may be used only when an explicit simulation defines exact truth.

Measured or EM response is never automatically promoted to physical truth.

---

## 7. Typed Sensor/Receiver Operator Graph

GeoDOA shall not define one universal `imperfection_matrix`.

The physical graph may contain the following operator types.

### 7.1 Geometry/propagation state

\[
\boxed{
\mathbf r_n^{\rm phys}
=\mathbf r_n^{\rm nom}+\boldsymbol\varepsilon_n.
}
\]

Geometry perturbation is first a position/path change; phase is a derived effect.

### 7.2 Element/polarization response

For a bounded uncoupled scalar specialization,

\[
\boxed{
\mathbf P(\xi)
=\operatorname{diag}(b_1(\xi),\ldots,b_N(\xi)).
}
\]

The response may depend on direction, frequency, polarization, orientation, and environment.

### 7.3 Cross-channel network/loading response

A bounded linear specialization may use

\[
\boxed{\mathbf z=\mathbf C\mathbf x}
\]

or a declared physical loaded-port transform.

### 7.4 Linear electronics

\[
\boxed{\mathbf z=\mathbf G_{\rm rx}(f,t,\chi)\mathbf x}
\]

with diagonal gain/phase only as a specialization.

### 7.5 Widely-linear electronics

I/Q imbalance may require

\[
\boxed{\mathbf y=\mathbf A\mathbf x+\mathbf B\mathbf x^*+\mathbf d}.
\]

### 7.6 Sampling operator

Sampling acts on a continuous-time waveform at channel-specific epochs and is not generally an \(N\times N\) spatial matrix.

### 7.7 Additive stochastic injection

Noise is injected at physical stages and propagated by downstream operators.

### 7.8 Nonlinear operator

Compression/intermodulation/clipping are nonlinear and cannot be universally collapsed into a linear manifold matrix.

### 7.9 Quantizer/code mapping

ADC quantization changes representation and is fundamentally nonlinear.

### 7.10 Selection/masking

Digital channel selection is distinct from changing physical port/termination state.

---

## 8. Conceptual Reference Planes

ADR-003 adopts the following conceptual scientific reference planes:

```text
RP-0 incident field/source condition
RP-1 geometry/propagation response
RP-2 element/open-circuit array response
RP-3 loaded/coupled port response
RP-4 analog receiver/baseband response
RP-5 continuous-time pre-sampling waveform
RP-6 sampled pre-quantization values
RP-7 ADC code output
RP-8 dequantized digital measurement
RP-9 selected/processed array view
```

These labels constrain scientific composition but are not yet final software enums.

Every operator or calibration artifact shall eventually identify compatible input/output planes, state, included effects, and provenance.

Compatible dimensions alone do not establish valid composition.

---

## 9. Geometry and Position Error

The authoritative physical position model is

\[
\boxed{
\mathbf r_n^{\rm phys}
=\mathbf r_n^{\rm nom}+\boldsymbol\varepsilon_n.
}
\]

For exact source position \(\mathbf r_s\), path perturbation is

\[
\boxed{
\delta R_n
=\|\mathbf r_s-\mathbf r_n^{\rm phys}\|
-\|\mathbf r_s-\mathbf r_n^{\rm nom}\|.
}
\]

Under the far-field first-order approximation, when nominal and physical manifolds use the same fixed ADR-001 spatial phase reference,

\[
\boxed{
\delta\phi_n^{(\mathrm{fixed\ ref})}
\approx
-k\hat{\mathbf u}^T\boldsymbol\varepsilon_n.
}
\]

If a comparison deliberately uses a separately displaced phase reference

\[
\mathbf r_{\rm ref}^{\rm phys}
=\mathbf r_{\rm ref}^{\rm nom}
+\boldsymbol\varepsilon_{\rm ref},
\]

then the corresponding referenced perturbation is

\[
\boxed{
\delta\phi_n^{(\mathrm{moved\ ref})}
\approx
-k\hat{\mathbf u}^T
(\boldsymbol\varepsilon_n-\boldsymbol\varepsilon_{\rm ref}).
}
\]

The reference-invariant pairwise form is

\[
\boxed{
\delta\phi_{nm}
=-k(\boldsymbol\varepsilon_n-\boldsymbol\varepsilon_m)^T\hat{\mathbf u}.
}
\]

A rigid translation may introduce only a common far-field phase relative to the fixed nominal reference; it does not produce far-field relative-manifold distortion.

Mechanical position, global pose, element orientation, and EM phase-center behavior are distinct.

---

## 10. Gain and Phase Mismatch

A bounded narrowband per-channel electronic response is

\[
\boxed{
g_n=\rho_ne^{j\phi_n}}
\]

and

\[
\boxed{\mathbf G=\operatorname{diag}(g_1,\ldots,g_N)}.
\]

Common phase is not spatial distortion and cancels from ordinary covariance.

A common complex gain is projectively irrelevant to manifold direction but may alter physical amplitude, SNR, clipping, quantization, or dynamic-range behavior according to physical stage/noise ordering.

Arbitrary electronic phase shall not be relabeled position error or physical delay without evidence.

---

## 11. Element Pattern, Orientation, and Polarization

A physical element is not merely a point sample.

A scalar response may be

\[
\boxed{b_n=b_n(\hat{\mathbf u},f,\mathbf p,\chi)}.
\]

Element response and electronic gain are distinct semantics even if numerically diagonal at one state.

Mechanical position and EM phase center are distinct.

Polarization requires an explicit transverse basis referenced consistently to the accepted look/propagation-direction convention.

Magnitude-only patterns are insufficient by default for coherent manifold calibration.

The initial Phase-1 profile remains ideal, identical, scalar, unit-response, and polarization-matched.

---

## 12. Mutual Coupling and Loading

Mutual coupling is a cross-element/cross-port electromagnetic phenomenon.

GeoDOA shall not define it universally by

\[
\mathbf a_c=\mathbf C\mathbf a.
\]

A declared physical multiport model may use antenna impedance \(\mathbf Z_A\), load \(\mathbf Z_L\), and open-circuit receive response \(\mathbf v_{\rm oc}\).

Under a declared Thevenin-style specialization,

\[
\boxed{
\mathbf i=(\mathbf Z_A+\mathbf Z_L)^{-1}\mathbf v_{\rm oc}
}
\]

and

\[
\boxed{
\mathbf v_L
=\mathbf Z_L(\mathbf Z_A+\mathbf Z_L)^{-1}\mathbf v_{\rm oc}.
}
\]

Define

\[
\boxed{
\mathbf T_L
=\mathbf Z_L(\mathbf Z_A+\mathbf Z_L)^{-1}.
}
\]

This is a loaded-port transform, not a universal coupling matrix.

The following are typed distinct:

\[
\boxed{
\mathbf Z,
\mathbf S,
\mathbf T_L,
\mathbf C,
\text{embedded pattern},
\text{aggregate manifold}.
}
\]

In particular, \(S_{21}\) is not generically a DOA coupling coefficient.

Reciprocal/symmetric network structure does not imply Hermitian structure.

Toeplitz, circulant, and banded coupling models are approximations requiring evidence; none is a universal finite-array law.

---

## 13. Double-Counting Prevention

An effect already contained in a measured, embedded, or EM/full-wave response shall not be applied again unless explicit de-embedding provenance proves that it has been removed.

This rule applies to:

- element response;
- mutual coupling/loading;
- radome/platform scattering;
- feed/network response;
- receiver electronics;
- fixtures/cables.

The included-effects/de-embedding record is a mandatory scientific part of direct-manifold and hybrid calibration semantics.

---

## 14. Channel Delay, Sampling Time, SRO, and Frequency Error

ADR-003 distinguishes:

```text
static channel phase
physical/electrical channel delay
fixed sampling-time offset
sampling-rate offset (SRO)
sampling jitter
receiver-reference/LO phase offset
receiver-reference/LO frequency offset
post-acquisition digital latency
```

### 14.1 Physical/electrical delay

\[
\boxed{y(t)=x(t-\delta\tau)}
\]

gives

\[
\boxed{H_\tau(\omega)=e^{+j\omega\delta\tau}}.
\]

A pure delay has

\[
\boxed{\frac{d\phi}{d\omega}=\delta\tau}.
}
\]

A static phase offset has no such slope.

### 14.2 Sampling-time model

\[
\boxed{
t_n[k]
=t_0+\beta_n+kT_s(1+\epsilon_{T,n})+\eta_n[k].
}
\]

If

\[
f_{s,n}=f_s(1+\epsilon_{f,n}),
\]

then

\[
\boxed{
1+\epsilon_{T,n}=\frac{1}{1+\epsilon_{f,n}}
}
\]

and for small error

\[
\boxed{\epsilon_{T,n}\approx-\epsilon_{f,n}}.
\]

### 14.3 Later sampling versus physical delay

For \(x(t)=Ae^{-j\omega t}\), sampling later by \(+\delta t\) gives

\[
\boxed{x(t+\delta t)=x(t)e^{-j\omega\delta t}}.
\]

This sign is opposite to a positive physical waveform delay because the operations are physically distinct.

### 14.4 Differential frequency error

A processed-baseband residual reference phase may be represented by

\[
\boxed{e^{j\psi_n(t)}}
\]

with

\[
\boxed{
\delta f_n(t)=\frac{1}{2\pi}\frac{d\psi_n}{dt}.
}
\]

Differential CFO can make the manifold time varying over a covariance window.

A common temporal phase may cancel for truly simultaneous physical snapshots but become relative in TDM/non-simultaneous virtual channels.

---

## 15. Receiver Noise and Stage Ordering

Noise is stage specific.

For a linear chain, a noise source injected at stage \(r\) is transformed only by downstream operators.

Under zero-mean mutual independence,

\[
\boxed{
\mathbf R_y
=\mathbf H\mathbf R_x\mathbf H^H
+\sum_r
\mathbf H_{{\rm down},r}
\mathbf R_{n_r}
\mathbf H_{{\rm down},r}^H.
}
\]

Correlated noise requires cross terms.

A single generic `noise_variance` is insufficient for a general receiver profile.

Spatially white noise before a nonunitary coupling/gain/correction transform may become colored.

---

## 16. Receiver Dynamic Range and ADC Semantics

Let ADC full-scale range be

\[
\boxed{V_{\rm FSR}=V_{\max}-V_{\min}}
\]

and ideal nominal step size

\[
\boxed{\Delta=\frac{V_{\rm FSR}}{2^{N_b}}}.
\]

Exact code-transition/reconstruction conventions shall be declared when code-exact behavior matters.

Under a restricted high-resolution/no-overload quantization-noise approximation,

\[
\boxed{\sigma_q^2\approx\frac{\Delta^2}{12}}.
\]

This is not the definition of quantization and does not hold universally.

For an ideal full-scale sine under the classical ideal-ADC approximation,

\[
\boxed{\mathrm{SNR}_{q,\mathrm{dB}}\approx6.02N_b+1.76}.
\]

ENOB, SNR, SINAD, THD, SFDR, and dynamic range are distinct.

Clipping is nonlinear information loss; post-acquisition scaling cannot reconstruct clipped data.

ADC acquisition quantization shall remain distinct from later FPGA/processor fixed-point arithmetic.

---

## 17. DC Offset, I/Q Imbalance, and Nonlinearity

A constant offset \(\mathbf d\) can add

\[
\boxed{\mathbf d\mathbf d^H}
\]

to an uncentered second moment under appropriate zero-mean assumptions.

I/Q imbalance may require the widely-linear model

\[
\boxed{\mathbf y=\mathbf A\mathbf x+\mathbf B\mathbf x^*+\mathbf d}.
\]

For improper/widely-linear profiles, ordinary covariance may be insufficient and augmented covariance may be required.

Nonlinear response may be represented locally by a declared model such as

\[
 y_n=a_1x+a_3|x|^2x+\cdots
\]

but linear superposition is not preserved generally.

Compression, intermodulation, and clipping remain outside the baseline linear profile.

---

## 18. Calibration Taxonomy

GeoDOA shall distinguish:

1. **characterization** — obtaining evidence about system response;
2. **parameter calibration** — estimating physical/effective model parameters;
3. **model calibration** — constructing the manifold/operator used by the estimator;
4. **data correction/equalization** — transforming measured data;
5. **direct response/manifold calibration** — using measured/EM response without unique causal decomposition;
6. **self-calibration/joint estimation** — estimating sensor and scene/source parameters jointly;
7. **calibration tracking/maintenance** — updating validity as system state drifts.

Calibration is inference/correction, not a forward physical cause.

---

## 19. Calibration State, Residual, and Uncertainty

Let physical state be

\[
\boxed{\boldsymbol\theta_{\rm phys}}
\]

and calibration estimate

\[
\boxed{\hat{\boldsymbol\theta}_{\rm cal}}.
\]

A parameter residual may be

\[
\boxed{
\boldsymbol\varepsilon_\theta^{\rm res}
=\boldsymbol\theta_{\rm phys}-\hat{\boldsymbol\theta}_{\rm cal}
}
\]

when subtraction is meaningful.

A manifold residual may be

\[
\boxed{
\mathbf e_a(\xi)
=\mathbf a_{\rm phys}(\xi)-\mathbf a_{\rm cal}(\xi)
}
\]

under a declared alignment/equivalence rule.

Nominal value, realized value, calibrated estimate, correction, residual, and estimate uncertainty shall remain distinguishable.

A local parameter covariance may be

\[
\boxed{\mathbf P_\theta=\operatorname{Cov}(\hat{\boldsymbol\theta})}.
\]

First-order response uncertainty may be approximated by

\[
\boxed{
\mathbf R_{a,\rm cal}
\approx\mathbf J_a\mathbf P_\theta\mathbf J_a^H
}
\]

under a declared local linearization.

---

## 20. Calibration Identifiability and Gauge Freedom

A calibration problem can converge numerically while remaining physically non-identifiable.

Identifiability is defined relative to a declared experiment/model and modulo declared gauge/equivalence transformations.

Examples of possible gauge/confounding include:

- common complex scale between source amplitude and channel gains;
- common phase reference;
- rigid translation under relative far-field phase;
- static phase versus delay at one frequency;
- element amplitude versus receiver gain;
- coupling versus embedded element response;
- source direction versus geometry error under insufficient calibration diversity;
- source frequency versus receiver frequency error.

A reference-channel normalization fixes a gauge; it does not prove that the physical reference channel is ideal.

Local Jacobian rank can diagnose local observability after gauge handling, but full rank does not prove global uniqueness.

Conditioning, structural identifiability, uncertainty, and optimizer convergence are distinct.

---

## 21. Calibration Correction and Conditioning

For a bounded linear physical model

\[
\boxed{\mathbf y=\mathbf H_{\rm phys}\mathbf x+\mathbf n}
\]

a fixed data correction gives

\[
\boxed{\mathbf y_{\rm corr}=\mathbf C_{\rm corr}\mathbf y}
\]

and

\[
\boxed{
\mathbf R_{n,\rm corr}
=\mathbf C_{\rm corr}\mathbf R_n\mathbf C_{\rm corr}^H.
}
\]

If \(\mathbf H\) is square/nonsingular, exact inverse correction may use

\[
\boxed{\mathbf H^{-1}}.
\]

A singular operator has no exact inverse; information in its null space cannot be reconstructed.

A Moore–Penrose pseudoinverse is a different operation:

\[
\boxed{\mathbf H^\dagger}.
\]

A Tikhonov-type correction may be

\[
\boxed{
\mathbf C_\lambda
=(\mathbf H^H\mathbf H+\lambda\mathbf I)^{-1}\mathbf H^H.
}
\]

Dimensional homogeneity requires

\[
\boxed{[\lambda\mathbf I]=[\mathbf H^H\mathbf H].}
\]

Therefore \(\lambda\) is not universally dimensionless. It is dimensionless only when the corresponding operator/inverse problem has been expressed in compatible dimensionless or explicitly scaled coordinates.

Small singular values can strongly amplify noise/model uncertainty.

Minimum singular value and condition number are distinct diagnostics.

---

## 22. Calibration Domain and Provenance

Calibration validity may depend on:

```text
frequency
direction / source position
range
polarization
time / age
temperature / environment
gain/AGC state
sample rate / LO state
active channels
physical port terminations
radome/platform configuration
hardware/firmware revision
```

Interpolation is part of the calibrated model.

Extrapolation outside calibrated domain is never silent.

Calibration provenance shall eventually preserve reference planes, included/de-embedded effects, channel identities, calibration source/fixture, gauge semantics, method, regularization, interpolation, uncertainty, residuals, hardware/software identity, and validity state.

---

## 23. Direct Measured / CST / Full-Wave Manifolds

A direct measured or EM manifold is an aggregate calibrated response model, not automatically physical truth.

Its scientific dataset shall preserve:

- labeled semantic axes;
- coordinate frame and registration;
- stable physical channel/port identities;
- complex response;
- frequency;
- direction/range;
- polarization basis where relevant;
- spatial origin/reference-plane semantics;
- normalization/gauge semantics;
- included effects/de-embedding state;
- calibration domain;
- uncertainty/quality information;
- measurement or solver/model provenance.

A magnitude-only pattern is insufficient by default for coherent MUSIC calibration.

Transmit far fields shall not be silently relabeled receive steering vectors without a convention-checked reciprocity/normalization transformation.

---

## 24. Direct-Manifold Interpolation and Gauge

At one state,

\[
\mathbf a'(\xi_m)=e^{j\phi_m}\mathbf a(\xi_m)
\]

may be projectively equivalent.

But arbitrary independent phase gauges across calibration nodes can change an interpolated complex manifold.

Therefore GeoDOA shall distinguish:

- pointwise projective equivalence;
- grid-coherent phase gauge required for interpolation/phase-slope use.

Wrapped-phase interpolation is not accepted silently.

Near response nulls, phase can be poorly conditioned and requires quality handling.

A normalized derived manifold shall not destructively replace the raw calibrated amplitude/phase response.

---

## 25. Error-Metric Taxonomy

No universal `manifold_error` scalar exists.

For compatible registered vectors \(\mathbf a\) and \(\mathbf b\), possible metrics include:

### 25.1 Raw Euclidean

\[
\boxed{d_{\rm raw}=\|\mathbf b-\mathbf a\|_2}.
\]

### 25.2 Phase-only aligned

\[
\boxed{
\varepsilon_\phi
=\min_\phi
\frac{\|\mathbf b-e^{j\phi}\mathbf a\|_2}{\|\mathbf a\|_2}.
}
\]

### 25.3 Common-complex-scale aligned

For

\[
\min_c\|\mathbf b-c\mathbf a\|_2^2,
\]

\[
\boxed{
c^*=\frac{\mathbf a^H\mathbf b}{\mathbf a^H\mathbf a}}.
\]

### 25.4 Projective alignment

\[
\boxed{
\rho
=\frac{|\mathbf a^H\mathbf b|}{\|\mathbf a\|_2\|\mathbf b\|_2}
}
\]

and

\[
\boxed{
\alpha=\cos^{-1}\rho,
\qquad
 d_{\rm proj}^2=1-\rho^2.
}
\]

Metric reference/test objects, alignment rule, normalization, units, domain weighting, and null handling are part of the metric definition.

---

## 26. Identifiability, Conditioning, and Error Are Distinct

GeoDOA shall distinguish:

```text
error
uncertainty
repeatability
accuracy/bias
local identifiability
global identifiability
gauge freedom
conditioning
regularization dependence
optimizer convergence
```

A scaled Jacobian may be used for local sensitivity/observability diagnostics, but raw mixed-unit condition numbers are not physically invariant under unit changes.

Fisher information/CRB may be used only under a fully declared probabilistic model, nuisance-parameter treatment, gauge constraints, and regularity assumptions.

---

## 27. Covariance Propagation

For

\[
\boxed{\mathbf A_{\rm phys}=\mathbf A+\Delta\mathbf A}
\]

with fixed \(\mathbf R_s\) and \(\mathbf R_n\),

\[
\boxed{
\begin{aligned}
\Delta\mathbf R_A
={}&
\Delta\mathbf A\mathbf R_s\mathbf A^H
+\mathbf A\mathbf R_s\Delta\mathbf A^H\\
&+\Delta\mathbf A\mathbf R_s\Delta\mathbf A^H.
\end{aligned}}
\]

The first-order term is

\[
\boxed{
\Delta\mathbf R_A^{(1)}
=\Delta\mathbf A\mathbf R_s\mathbf A^H
+\mathbf A\mathbf R_s\Delta\mathbf A^H.
}
\]

For a linear sensor operator \(\mathbf H\),

\[
\boxed{\mathbf R_y=\mathbf H\mathbf R_x\mathbf H^H}
\]

only for the covariance content actually passing through that physical operator.

Downstream noise remains separate.

---

## 28. Sensor Error versus Finite-Sample Covariance Error

Let

\[
\boxed{
\mathbf E_{\rm sensor}
=\mathbf R_{\rm phys}-\mathbf R_{\rm nom}}
\]

and

\[
\boxed{
\mathbf E_{\rm sample}
=\hat{\mathbf R}-\mathbf R_{\rm phys}}.
\]

Then exactly

\[
\boxed{
\hat{\mathbf R}-\mathbf R_{\rm nom}
=\mathbf E_{\rm sensor}+\mathbf E_{\rm sample}.
}
\]

This bookkeeping identity does not imply independence.

More snapshots can reduce finite-sample error but do not remove deterministic manifold mismatch.

Perfect calibration does not eliminate finite-sample subspace variance.

---

## 29. Rank and Time-Varying Sensor State

GeoDOA shall distinguish:

```text
physical source count
source covariance rank
manifold rank
signal covariance rank
observed signal-subspace dimension
sample covariance rank
selected model order
```

A nonsingular sensor transform can preserve rank while rotating eigenspaces.

A rank-deficient transform can reduce observable rank.

A time-varying sensor/manifold state across a covariance window cannot generally be represented by one averaged static operator; averaging differently oriented low-rank covariances can increase apparent covariance rank.

---

## 30. White and Colored Noise Eigenspace Semantics

For

\[
\boxed{
\mathbf R_x=\mathbf R_{\rm sig}+\sigma^2\mathbf I,
}
\]

isotropic white noise shifts population eigenvalues without rotating population eigenvectors.

For general colored/unequal noise,

\[
\boxed{\mathbf R_n\neq\sigma^2\mathbf I},
\]

ordinary covariance eigenspaces can change.

If \(\mathbf R_n\succ0\) and a whitening model is valid,

\[
\boxed{
\mathbf y_w=\mathbf R_n^{-1/2}\mathbf y,
\qquad
\mathbf a_w=\mathbf R_n^{-1/2}\mathbf a.
}
\]

Whitening data without transforming the steering model consistently is invalid.

---

## 31. Eigenspace Perturbation

Hermitian covariance perturbation obeys standard eigenvalue/subspace perturbation principles.

A Weyl-type bound gives

\[
\boxed{
|\tilde\lambda_i-\lambda_i|\le\|\mathbf E\|_2.
}
\]

For a simple eigenvector, first-order mixing scales inversely with eigenvalue separation.

Signal/noise subspace rotation shall be measured using principal angles or projector metrics, not arbitrary eigenvector-column differences.

Davis–Kahan-type bounds scale with covariance perturbation relative to an appropriate reference spectral gap under theorem-specific assumptions.

Population and sample eigengaps shall use distinct notation/semantics.

---

## 32. MUSIC Mismatch Propagation

For population classical MUSIC,

\[
\boxed{
D(\theta)
=\mathbf a_{\rm model}^H(\theta)
\mathbf P_n
\mathbf a_{\rm model}(\theta).
}
\]

For a perfectly matched true source,

\[
\boxed{D(\theta_k)=0}.
\]

For one source with unit physical vector \(\mathbf u\) and unit model vector \(\mathbf v\),

\[
\boxed{
\mathbf v^H(\mathbf I-\mathbf u\mathbf u^H)\mathbf v
=1-|\mathbf u^H\mathbf v|^2
=1-\rho^2.
}
\]

Thus the projective manifold leakage metric is exactly the normalized population MUSIC denominator at the true source in the rank-one case.

Data/noise-subspace perturbation and search-manifold perturbation are distinct mismatch channels.

Local first-order peak-shift formulas are permitted only as explicitly bounded approximations under smooth isolated-peak assumptions.

---

## 33. Estimator Compatibility Is Multi-Axis

Compatibility shall not be one Boolean.

At minimum, compatibility evaluation distinguishes:

```text
manifold representation
reference plane
coordinate/direction convention
narrowband/frequency validity
fixed-manifold/stationarity
snapshot simultaneity/coherence
linear superposition
ordinary-complex vs augmented statistics
noise model
covariance model
quantization regime
calibration state/domain
physical channel/port state
source/subspace rank and model order
manifold/interpolation domain
required preprocessing
```

A run can be manifold-compatible but noise-incompatible, or reference-plane-compatible but calibration-domain-incompatible.

`UNRESOLVED` shall never be silently promoted to `COMPATIBLE`.

---

## 34. Classical MUSIC Compatibility Examples

### 34.1 Static position/gain/coupling mismatch

If fixed, linear, narrowband, and known/calibrated, classical MUSIC can remain compatible using the matched physical/calibrated manifold.

Using the nominal manifold against mismatched physical data is explicitly a mismatched/degraded profile.

### 34.2 Colored noise

Unwhitened baseline MUSIC is not automatically compatible.

A valid whitening/generalized profile may restore compatibility.

### 34.3 SRO/CFO/time variation

A single fixed manifold can become invalid over the covariance window; resampling/synchronization/state-aware processing may be required.

### 34.4 I/Q imbalance

Material conjugate response requires correction or augmented/widely-linear processing.

### 34.5 Nonlinearity/clipping

The baseline linear profile is incompatible outside the validated linear/no-overload regime.

### 34.6 High-resolution quantization

A declared additive quantization-noise approximation may be a degraded compatible profile under its assumptions.

### 34.7 One-bit/coarse quantization

A specialized quantized-statistics estimator profile is required by default.

### 34.8 Measured/CST manifold

A registered, coherent, in-domain, reference-plane-compatible direct manifold can be fully compatible with classical MUSIC.

---

## 35. Digital Mask versus Physical Port State

Digital post-acquisition selection may produce a reduced array when data, covariance, and manifold are selected consistently while preserving stable physical channel identity.

Physically opening, shorting, disabling, or reterminating a port can alter coupling/loading and invalidate calibration for other channels.

Therefore

\[
\boxed{
\text{digital mask}
\neq
\text{physical port-state change}.
}
\]

---

## 36. MIMO Calibration and Compatibility

Physical MIMO provenance remains \((\mathrm{Tx}_i,\mathrm{Rx}_j)\).

A direct virtual-channel calibration shall not erase that provenance.

A separable virtual response such as

\[
 g_{ij}^{\rm virt}=g_{{\rm tx},i}g_{{\rm rx},j}
\]

is only a declared specialization.

TDM/non-simultaneous MIMO requires acquisition-time and evolving phase provenance; a common temporal phase can become relative across virtual channels.

The initial receive-array Phase-1 profile does not automatically claim TDM-MIMO compatibility.

---

## 37. Initial Phase-1 ADR-003 Profile

The accepted initial authoritative profile is:

### 37.1 Geometry/propagation

```text
nominal geometry = physical geometry
far-field narrowband PM-001-compatible propagation
ADR-001 sign/reference conventions
```

### 37.2 Elements

```text
ideal identical scalar elements
unit complex response
no polarization mismatch in bounded scalar profile
```

### 37.3 Coupling/loading

```text
no mutual-coupling distortion
ideal/reference loading
```

### 37.4 Electronics/timing

```text
unity differential gain/phase
zero differential channel delay
common coherent clock/reference
zero differential fixed skew
zero differential SRO
zero differential CFO
zero deterministic timing jitter
simultaneous-equivalent snapshots
```

### 37.5 Receiver/ADC

```text
linear receiver
no DC offset
no I/Q imbalance
no compression/intermodulation
no clipping
unquantized floating acquisition baseline
```

### 37.6 Calibration

```text
no deterministic imperfection calibration required
identity / not-applied calibration state recorded explicitly
```

### 37.7 Noise/statistics

```text
additive proper-complex spatially white equal-variance noise
ordinary covariance/subspace representation
```

Therefore

\[
\boxed{
\mathcal H_{\rm sensor}^{\rm Phase1}\equiv\mathcal I.
}
\]

---

## 38. Explicit Phase-1 Exclusions

The initial authoritative implementation shall not yet activate:

- sensor position perturbation;
- nontrivial gain/phase mismatch;
- channel delay mismatch;
- mutual coupling;
- nonideal element/polarization response;
- measured/CST direct manifold calibration;
- colored-noise whitening;
- sample skew/SRO/CFO/jitter;
- I/Q imbalance;
- receiver nonlinearity;
- clipping;
- ADC quantization;
- near-field sensor-imperfection profile;
- wideband sensor-imperfection profile;
- vector/polarimetric sensors;
- TDM-MIMO synchronization calibration;
- self-calibration;
- adaptive calibration;
- one-bit/coarse-quantized MUSIC.

Scientific semantics are defined now so these later profiles can be added without changing the foundation.

---

## 39. Deferred Profile Activation Rule

A nonideal family becomes authoritative only through a bounded profile defining:

1. physical/operator semantics;
2. units and domain;
3. reference planes;
4. state and provenance;
5. calibration/correction behavior;
6. estimator compatibility;
7. deterministic reference evidence;
8. failure/boundary behavior;
9. validation/reproducibility evidence;
10. downstream covariance/eigenspace/DOA consequences.

An optional software parameter does not activate a scientific profile by itself.

Compound profiles require new validation because individual effects can interact or fail to commute.

---

## 40. No-Silent-Coercion Rules

GeoDOA shall not silently:

- switch among nominal/physical/measured/EM/calibrated response meanings;
- infer units;
- normalize away physically meaningful amplitude without provenance;
- convert colored noise into a white-noise assumption;
- collapse physical delay and sampling-time offset;
- collapse SRO/CFO into one constant phase;
- treat processing latency as acquisition-time error;
- treat ADC bits as FPGA arithmetic word length;
- treat one-bit data as high-resolution float samples;
- treat clipping as additive noise;
- treat I/Q conjugate leakage as ordinary complex gain;
- treat a digital mask as a physical port-state model;
- treat transmit far fields as receive manifolds without conversion;
- extrapolate calibration outside domain silently;
- apply coupling/element/radome/receiver effects twice;
- interpret source count, signal rank, and sample rank as one quantity;
- promote unresolved identifiability/compatibility to a definitive result.

---

## 41. Accepted Golden Reference Problems

Gate E formally accepts GRP-014 through GRP-017 as deterministic reference evidence.

### GRP-014 — Position-error phase distortion

Canonical chain:

\[
\delta d
\rightarrow
\delta\phi
\rightarrow
\hat u
\rightarrow
\Delta\theta
\]

with rigid-translation invariance.

For the accepted numerical reference, `d=lambda/2`, `u0=0.5`, and `delta_d/d=0.02` give

```text
u_hat                     0.51
theta_hat                 30.6638297424 deg
exact angular bias        0.6638297424 deg
exact angular bias        0.01158601468 rad
first-order angular bias  0.6615946745 deg
```

### GRP-015 — Gain/phase mismatch

Includes common-phase covariance invariance and two-sensor relative phase-error DOA bias.

For \(d=\lambda/2\),

\[
\boxed{\Delta u=-\phi_e/\pi}.
\]

### GRP-016 — Mutual-coupling manifold distortion

Use

\[
\mathbf a=\begin{bmatrix}1\\-j\end{bmatrix},
\qquad
\mathbf C=\begin{bmatrix}1&0.5\\0.5&1\end{bmatrix},
\]

so

\[
\boxed{
\mathbf b
=\begin{bmatrix}1-0.5j\\0.5-j\end{bmatrix}.
}
\]

The relative response is

\[
\boxed{b_2/b_1=0.8-0.6j}.
\]

### GRP-017 — Coupling to covariance/eigenspace/MUSIC

\[
\boxed{
\mathbf R_{\rm sig}
=\begin{bmatrix}
1.25&1+0.75j\\
1-0.75j&1.25
\end{bmatrix}
}
\]

with signal eigenvalues

\[
\boxed{\{2.5,0\}}.
\]

Adding \(\mathbf I\) gives

\[
\boxed{\{3.5,1\}}
\]

with unchanged eigenvectors.

The squared nominal/coupled alignment is

\[
\boxed{\rho^2=0.8}
\]

and normalized nominal leakage into the physical rank-one noise subspace is

\[
\boxed{1-\rho^2=0.2}.
\]

Supplemental deterministic references `ADR-003-SRC-01` through `ADR-003-SRC-08` cover timing, SRO/CFO, ADC arithmetic, DC offset, inverse-calibration noise amplification, calibration-grid gauge, and operator noncommutativity.

---

## 42. Scientific Evidence Types

ADR-003 shall preserve whether evidence is:

- exact identity;
- analytical derivation;
- bounded first-order approximation;
- norm/perturbation bound;
- deterministic hand/reference calculation;
- numerical deterministic test;
- Monte Carlo statistic;
- measured validation result;
- EM/full-wave simulation result.

One evidence type shall not be relabeled another.

---

## 43. Consequences

### Positive consequences

- physical cause and processing effect remain traceable;
- calibration and correction are scientifically interpretable;
- CST/measured manifolds can be integrated without double counting;
- mismatch can be propagated into covariance/eigenspace/MUSIC diagnostics;
- future FPGA/SoC work can distinguish ADC acquisition effects from arithmetic quantization;
- later sensor profiles can be added without changing foundational semantics;
- incompatibility becomes explicit instead of silently producing misleading results.

### Costs

- the data model must carry more metadata and provenance;
- calibration artifacts require explicit domains/reference planes;
- implementation cannot rely on one convenience `error_matrix`;
- multiple estimator profiles are required for colored noise, wideband timing, widely-linear receivers, nonlinear/quantized regimes, and other advanced cases;
- validation must be staged by bounded profiles rather than one monolithic `realistic` simulation.

---

## 44. Acceptance Evidence

ADR-003 acceptance is supported by:

```text
Gate A — Physical Consistency                  PASS
Gate B — Mathematical Consistency              PASS
Gate C — Dimensional and Unit Consistency      PASS
Gate D — Software Semantic Consistency         PASS
Gate E — Hand-Calculated Reference Evidence    PASS
Gate F — Boundary and Failure Analysis         PASS
Final cross-gate reconciliation                PASS
Cross-ADR-001 consistency                      PASS
Cross-ADR-002 consistency                      PASS
```

Gate E formally promotes GRP-014 through GRP-017. Gate F defines the detailed boundary/failure taxonomy and 140 explicit cases.

---

## 45. Final Disposition

```text
Explorations 3.1–3.14: COMPLETE
Cross-section reconciliation: COMPLETE
Pre-Gate consistency review: PASS
Gate A — Physical Consistency: PASS
Gate B — Mathematical Consistency: PASS
Gate C — Dimensional and Unit Consistency: PASS
Gate D — Software Semantic Consistency: PASS
Gate E — Hand-Calculated Reference Evidence: PASS
Gate F — Boundary and Failure Analysis: PASS
Final Cross-Gate Reconciliation: PASS
Golden Reference GRP-014–GRP-017: ACCEPTED
ADR-003 acceptance: ACCEPTED
```

The accepted initial Phase-1 deterministic sensor profile remains ideal/identity. Nonideal sensor families are governed by this ADR but remain implementation-deferred until their bounded profiles and verification evidence are established.
