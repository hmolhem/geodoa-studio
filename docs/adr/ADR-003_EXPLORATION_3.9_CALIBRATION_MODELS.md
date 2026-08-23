# ADR-003 Exploration 3.9 — Calibration Models

- **Phase:** 0C — Scientific Foundations
- **Status:** EXPLORATION COMPLETE — CANDIDATE CONTRACT, NOT ACCEPTED
- **Parent ADR:** ADR-003 — Sensor Imperfections, Mutual Coupling, and Calibration
- **Branch:** `docs/phase0c-scientific-conventions`
- **Depends on:** ADR-001, ADR-002, ADR-003 Explorations 3.1–3.8
- **Acceptance gates:** Not started

> This is the dedicated exploration record for ADR-003 Section 3.9. It is not an accepted governing ADR. Candidate decisions remain subject to 3.10–3.14 reconciliation, Gates A–F, Golden Reference evidence, boundary/failure analysis, and final acceptance.

---

## 1. Primary question

Explorations 3.1–3.8 established that GeoDOA must distinguish nominal, physical, measured, EM-simulated, and calibrated responses; preserve physical effect ordering; and represent real-sensor imperfections using typed operators rather than one generic error matrix.

Exploration 3.9 answers:

> What scientifically distinct meanings of calibration must GeoDOA support, under what observability and reference assumptions can calibration parameters be estimated, how are corrections applied without losing provenance, and how are residual calibration errors and uncertainty represented?

The governing principle is

\[
\boxed{
\text{Calibration estimates or constructs knowledge/corrections about a physical system; it does not change the historical cause of the measurement.}
}
\]

Calibration therefore belongs to a separate estimation/correction graph associated with the physical forward graph defined in 3.8.

---

## 2. Calibration taxonomy

GeoDOA shall not use the word `calibration` as one undifferentiated operation. At minimum, the following meanings are distinct.

### 2.1 Characterization

A measurement campaign may characterize the sensor system without immediately constructing a correction.

Examples include measured channel gain/phase versus frequency, measured coupling/S-parameters, measured array response versus angle, ADC transfer measurements, or clock-skew measurements.

Characterization produces evidence/data about the system.

### 2.2 Parameter calibration

A parameterized physical/electrical model is fitted:

\[
\boxed{
\hat{\boldsymbol\theta}_{\rm cal}
=\mathcal E(\mathcal D_{\rm cal},\mathcal M)
}
\]

where \(\mathcal D_{\rm cal}\) is calibration data and \(\mathcal M\) is a declared model family.

Examples include estimating:

- sensor position offsets;
- per-channel complex gain;
- channel delay;
- sample-time offset;
- oscillator/reference phase or frequency offset;
- coupling-network parameters;
- I/Q imbalance coefficients;
- ADC gain/offset or code-map parameters.

### 2.3 Model calibration

Estimated parameters or directly characterized responses are used to build the response model supplied to the estimator:

\[
\boxed{
\mathbf a_{\rm model}
=\mathbf a_{\rm cal}
}
\]

rather than using the nominal ideal manifold.

The raw measurement data may remain untouched.

### 2.4 Data correction / equalization

A correction operator is applied to data:

\[
\boxed{
\mathbf y_{\rm corr}
=\mathcal C_{\rm corr}(\mathbf y;\hat{\boldsymbol\theta}_{\rm cal}).
}
\]

This operation can transform both signal and noise statistics and may be ill-conditioned or noninvertible.

### 2.5 Direct response/manifold calibration

Measured or EM-simulated array responses may be used directly, without uniquely decomposing them into position, element, coupling, and electronics parameters.

This family is introduced here but is developed in detail in Exploration 3.10.

### 2.6 Self-calibration / joint estimation

When calibration parameters and scene/source parameters are estimated jointly from operational data,

\[
\boxed{
(\hat{\boldsymbol\theta}_{\rm cal},\hat{\boldsymbol\xi})
=\arg\min_{\boldsymbol\theta,\boldsymbol\xi}
J(\mathcal D;\boldsymbol\theta,\boldsymbol\xi),
}
\]

the problem is a self-calibration or joint-estimation problem.

Such a problem requires explicit identifiability/gauge analysis because sensor parameters and source parameters may be confounded.

### 2.7 Calibration tracking / maintenance

A previously established calibration may be monitored or updated over time because temperature, aging, reconfiguration, gain state, cable state, or oscillator state changes.

Offline factory calibration, laboratory calibration, startup calibration, periodic recalibration, and online tracking are different operational modes.

---

## 3. Physical truth, calibration estimate, and residual error are distinct

Let the physical sensor state be parameterized by

\[
\boxed{
\boldsymbol\theta_{\rm phys}.
}
\]

A calibration procedure produces an estimate

\[
\boxed{
\hat{\boldsymbol\theta}_{\rm cal}.
}
\]

The parameter residual is

\[
\boxed{
\boldsymbol\varepsilon_{\theta}^{\rm res}
=\boldsymbol\theta_{\rm phys}
-\hat{\boldsymbol\theta}_{\rm cal}
}
\]

when subtraction is meaningful for the parameterization.

For manifold/response objects, a more general residual is

\[
\boxed{
\mathbf e_a(\xi,\chi)
=\mathbf a_{\rm phys}(\xi,\chi)
-\mathbf a_{\rm cal}(\xi,\chi)
}
\]

subject to the equivalence/alignment semantics later formalized in 3.11.

GeoDOA shall never overwrite nominal design parameters with calibrated estimates in a way that destroys provenance. At minimum, the following remain distinguishable:

```text
nominal design value
physical/realized value if known in simulation
calibrated estimate
correction value/operator
residual error
uncertainty of the estimate
```

---

## 4. Calibration experiment model

A calibration artifact is meaningful only relative to a declared experiment and measurement model.

A generic calibration measurement may be written

\[
\boxed{
\mathbf y_{\rm cal}
=\mathcal F_{\rm cal-exp}
(\boldsymbol\theta_{\rm phys},
\boldsymbol\xi_{\rm ref},
\mathbf s_{\rm ref},
\boldsymbol\nu)
}
\]

where

- \(\boldsymbol\theta_{\rm phys}\) contains sensor-system parameters to be inferred;
- \(\boldsymbol\xi_{\rm ref}\) describes the calibration source/fixture/geometry;
- \(\mathbf s_{\rm ref}\) describes the calibration excitation;
- \(\boldsymbol\nu\) contains noise, nuisance parameters, and experiment uncertainty.

The estimator is then

\[
\boxed{
\hat{\boldsymbol\theta}_{\rm cal}
=\mathcal E_{\rm cal}(\mathbf y_{\rm cal};
\boldsymbol\xi_{\rm ref},\mathbf s_{\rm ref},\mathcal M).
}
\]

Calibration-source location, orientation, polarization, frequency, amplitude/phase knowledge, timing reference, fixture response, and environmental state may themselves be uncertain and must not be silently treated as exact.

---

## 5. Calibration-source classes

GeoDOA shall distinguish at least the following calibration evidence classes.

### 5.1 External known reference

A source/target/fixture with sufficiently known location, direction, waveform, timing, or field response is used to estimate array parameters.

The accuracy of the reference constrains achievable calibration accuracy.

### 5.2 Internal reference / loopback

A coupler, switch matrix, injected tone, internal loop, shared reference channel, or digital/analog test path may characterize a subset of the receiver/transmitter chain.

An internal calibration path does not automatically include antenna, propagation, radome, mutual coupling, or free-space effects unless the physical injection/reference plane proves that it does.

### 5.3 Over-the-air reference

A controlled or opportunistic radiating source excites the physical antenna/array path. This can include more of the end-to-end chain but also introduces propagation, reference-location, multipath, polarization, and environment uncertainties.

### 5.4 Self-calibration from operational data

No fully known external calibrator is assumed. Sensor parameters and scene parameters are inferred jointly using structural redundancy, multiple sources, multiple snapshots, known geometry constraints, or statistical assumptions.

This mode requires the strongest identifiability analysis.

---

## 6. Observability, identifiability, and gauge freedom

A calibration algorithm can return a numerical answer even when the physical parameters are not uniquely identifiable. GeoDOA shall therefore distinguish numerical convergence from scientific identifiability.

### 6.1 Simple complex-scale ambiguity

Consider a single-source narrowband model

\[
\boxed{
\mathbf y
=\mathbf G\mathbf a(\theta)s.
}
\]

If the complex source amplitude \(s\) is unknown, then for any nonzero complex scalar \(c\),

\[
\boxed{
\mathbf G' = c\mathbf G,
\qquad
s'=\frac{s}{c}
}
\]

produces exactly the same \(\mathbf y\):

\[
\mathbf G'\mathbf a s'
=\mathbf G\mathbf a s.
\]

Thus absolute common complex scale is not identifiable from this observation alone.

A calibration must either:

- supply an external amplitude/phase reference;
- choose a gauge/reference convention;
- or report only relative quantities.

### 6.2 Reference-channel gauge

A common relative gain/phase convention may choose channel \(r\) as the reference and impose

\[
\boxed{
g_r=1}
\]

or equivalently

\[
|g_r|=1,
\qquad
\angle g_r=0.
\]

This fixes a representation gauge; it does not imply that the physical reference channel is error-free.

### 6.3 Confounded physical effects

Examples of partial/non-identifiability include:

- static electronic phase versus propagation/position phase at one direction and one frequency;
- static phase versus channel delay at one frequency;
- element pattern amplitude versus electronic gain at one angle;
- coupling versus embedded element response when only aggregate response is observed;
- source direction versus geometry error under insufficient calibration directions;
- source phase versus common receiver phase;
- source frequency offset versus receiver LO offset under insufficient reference information.

GeoDOA shall preserve such confounding instead of reporting a uniquely named physical cause that the experiment cannot distinguish.

---

## 7. Calibration geometry and excitation diversity

Identifiability is improved by selecting calibration conditions that excite independent sensitivities.

A local parametric model may be linearized as

\[
\boxed{
\mathbf y(\boldsymbol\theta)
\approx
\mathbf y(\boldsymbol\theta_0)
+\mathbf J_{\theta}
(\boldsymbol\theta-\boldsymbol\theta_0),
}
\]

where

\[
\mathbf J_{\theta}
=\frac{\partial \mathbf y}{\partial\boldsymbol\theta^T}
\]

is the calibration sensitivity/Jacobian matrix.

If columns of \(\mathbf J_{\theta}\) are linearly dependent or nearly dependent over the calibration dataset, parameters are unidentifiable or poorly conditioned locally.

Therefore calibration experiment design may require diversity over one or more of:

- direction/angle;
- range;
- frequency;
- polarization;
- source position;
- source amplitude;
- gain state;
- temperature;
- time;
- channel/port excitation state;
- known phase/frequency references.

A single calibration condition is not presumed sufficient for a parameter family merely because the number of measurements exceeds the number of unknowns.

---

## 8. Calibration objective functions

A generic residual-based calibration problem may be written

\[
\boxed{
\hat{\boldsymbol\theta}
=\arg\min_{\boldsymbol\theta}
\mathbf r(\boldsymbol\theta)^H
\mathbf W
\mathbf r(\boldsymbol\theta)
}
\]

with

\[
\mathbf r(\boldsymbol\theta)
=\mathbf y_{\rm cal}
-\hat{\mathbf y}(\boldsymbol\theta).
\]

The weighting \(\mathbf W\) and residual domain must be declared.

Under an appropriate Gaussian error model, weighted least squares can coincide with maximum likelihood. That equivalence is conditional on the declared probability model; it is not a universal property of calibration.

GeoDOA may later support least-squares, weighted least-squares, maximum-likelihood, robust, Bayesian, or constrained calibration, but the scientific meaning of the residual and nuisance parameters must precede the optimizer choice.

---

## 9. Parameter-calibration families

### 9.1 Geometry / position calibration

Estimate

\[
\boxed{
\hat{\mathbf r}_n^{\rm phys}
=\mathbf r_n^{\rm nom}
+\hat{\boldsymbol\varepsilon}_n.
}
\]

Calibration must declare coordinate frame, source-location knowledge, array pose, and whether rigid-body translation/rotation are gauge freedoms or externally referenced quantities.

Multiple calibration directions/ranges may be needed to observe different components of three-dimensional position error.

### 9.2 Gain/phase calibration

Estimate a complex channel response

\[
\boxed{
\hat g_n(f,t,\chi)
=\hat\rho_n e^{j\hat\phi_n}.
}
\]

A relative calibration may normalize to a reference channel or a common complex scale. Absolute amplitude/phase requires a stronger reference definition.

### 9.3 Delay calibration

A channel response may contain

\[
\boxed{
H_n(f)
=G_n(f)e^{+j2\pi f\delta\tau_n}
}
\]

under the accepted delay convention.

Delay is identified through frequency-dependent phase slope, not from one-frequency phase alone.

Phase unwrapping, frequency reference, and the division between static phase and delay must be explicit.

### 9.4 Sample-time / clock calibration

Calibration may estimate fixed sample-time offsets, SRO, deterministic clock phase relationships, or other timing parameters.

A fixed deskew correction and an SRO correction are different operations. SRO generally requires resampling/time-base correction rather than one constant phase correction for broadband data.

### 9.5 LO / frequency-reference calibration

Receiver phase and frequency offsets may be estimated relative to a declared reference. Common and differential oscillator terms remain distinct, as established in 3.6.

### 9.6 Coupling/network calibration

Calibration may estimate physical network parameters such as \(\mathbf Z\) or \(\mathbf S\), a declared loaded-port transform, or an effective manifold-domain coupling model.

These objects are not interchangeable merely because each can be represented by a matrix.

Terminations, reference impedance, frequency, port state, and de-embedding plane are mandatory domain information.

### 9.7 I/Q calibration

A widely linear response may require estimates of

\[
\boxed{
\mathbf A_{\rm IQ},\quad
\mathbf B_{\rm IQ},\quad
\mathbf d_{\rm IQ}.
}
\]

A complex-gain-only calibration cannot in general remove a conjugate-image term.

### 9.8 Receiver / ADC calibration

Calibration may include gain, offset, full-scale/code mapping, DNL/INL characterization, channel-to-channel delay, aperture timing, or gain-state dependent corrections.

Code-domain calibration and dequantized-sample calibration must preserve the measurement stage to which they apply.

### 9.9 Nonlinearity calibration

If a nonlinear response is parameterized, coefficients may be estimated only over a declared input-level, frequency, temperature, and operating-state domain.

A small-signal calibration is not automatically valid in compression or clipping.

---

## 10. Model calibration versus data correction

Let a bounded linear physical response be

\[
\boxed{
\mathbf y
=\mathbf H_{\rm phys}\mathbf x
+\mathbf n.
}
\]

### 10.1 Calibrated-model strategy

Use an estimated response

\[
\boxed{
\mathbf H_{\rm cal}
\approx\mathbf H_{\rm phys}
}
\]

inside the estimator, leaving measurements unchanged.

For a source manifold,

\[
\boxed{
\mathbf a_{\rm cal}
=\mathbf H_{\rm cal}\mathbf a_{\rm nom}.
}
\]

The measurement-noise covariance remains the covariance produced by the physical receiver chain.

### 10.2 Data-correction strategy

Apply

\[
\boxed{
\mathbf y_{\rm corr}
=\mathbf C_{\rm corr}\mathbf y.
}
\]

Then

\[
\mathbf y_{\rm corr}
=\mathbf C_{\rm corr}\mathbf H_{\rm phys}\mathbf x
+\mathbf C_{\rm corr}\mathbf n.
\]

The corrected noise covariance becomes

\[
\boxed{
\mathbf R_{n,\rm corr}
=\mathbf C_{\rm corr}
\mathbf R_n
\mathbf C_{\rm corr}^H.
}
\]

Thus model calibration and data correction can be statistically non-equivalent even when both reduce deterministic manifold mismatch.

---

## 11. Exact inverse correction and its limits

If \(\mathbf H_{\rm cal}\) is square and nonsingular, one candidate correction is

\[
\boxed{
\mathbf C_{\rm corr}
=\mathbf H_{\rm cal}^{-1}.
}
\]

The effective corrected response is

\[
\boxed{
\mathbf H_{\rm eff}
=\mathbf H_{\rm cal}^{-1}
\mathbf H_{\rm phys}.
}
\]

Perfect calibration would yield \(\mathbf H_{\rm eff}=\mathbf I\), but only if the estimated model equals the physical model and the inverse is valid.

A singular physical/calibration operator has no exact inverse. Information lost in a null space cannot be reconstructed by calibration.

A nearly singular operator may admit an algebraic inverse while causing unacceptable noise and uncertainty amplification.

---

## 12. Conditioning, singular values, and correction amplification

For a linear correction matrix \(\mathbf C\), noise power along different modes is transformed according to the singular structure of \(\mathbf C\).

If

\[
\mathbf H
=\mathbf U\boldsymbol\Sigma\mathbf V^H,
\]

then

\[
\mathbf H^{-1}
=\mathbf V\boldsymbol\Sigma^{-1}\mathbf U^H
\]

when all singular values are nonzero.

A small singular value \(\sigma_i\) becomes a large inverse factor \(1/\sigma_i\).

Therefore GeoDOA shall distinguish:

\[
\boxed{
\sigma_{\min}(\mathbf H)
}
\]

from

\[
\boxed{
\kappa_2(\mathbf H)
=\frac{\sigma_{\max}(\mathbf H)}{\sigma_{\min}(\mathbf H)}.
}
\]

Both can matter, but they answer different questions.

---

## 13. Pseudoinverse and regularized correction

For nonsquare/rank-deficient/ill-conditioned models, a correction may use a pseudoinverse or regularization rather than an exact inverse.

A Moore-Penrose candidate is

\[
\boxed{
\mathbf C_{\rm pinv}
=\mathbf H^{\dagger}.
}
\]

A Tikhonov-type correction may be

\[
\boxed{
\mathbf C_{\lambda}
=(\mathbf H^H\mathbf H+\lambda\mathbf I)^{-1}\mathbf H^H,
\qquad \lambda>0.
}
\]

Regularization deliberately trades exact inversion against noise/uncertainty amplification and bias.

GeoDOA shall not call a regularized correction `inverse calibration` without recording the regularization rule and parameter.

The calibration artifact must preserve whether correction is exact inverse, pseudoinverse, truncated-SVD, Tikhonov, or another method.

---

## 14. Deterministic two-channel correction check

Let the physical channel response be

\[
\mathbf G
=\operatorname{diag}(1,0.5e^{j20^\circ}).
\]

For a nominal manifold

\[
\mathbf a=\begin{bmatrix}1\\-j\end{bmatrix},
\]

the physical response is

\[
\mathbf a_{\rm phys}
=\mathbf G\mathbf a.
\]

If calibration is exact,

\[
\mathbf C_{\rm corr}=\mathbf G^{-1},
\]

then

\[
\boxed{
\mathbf C_{\rm corr}\mathbf a_{\rm phys}
=\mathbf a.
}
\]

However, if pre-correction receiver noise is white,

\[
\mathbf R_n=\sigma^2\mathbf I,
\]

then after correction

\[
\boxed{
\mathbf R_{n,\rm corr}
=\sigma^2
\operatorname{diag}(1,4).
}
\]

The deterministic gain mismatch is removed, but channel-2 noise variance is amplified by a factor of four.

This is an exploration check, not yet a formal GRP assignment.

---

## 15. Residual calibration operator

For a linear physical system and linear correction, define

\[
\boxed{
\mathbf H_{\rm res}
=\mathbf C_{\rm corr}\mathbf H_{\rm phys}.
}
\]

The ideal corrected target may be identity or another explicitly declared reference response.

If identity is the target,

\[
\boxed{
\mathbf E_{\rm res}
=\mathbf H_{\rm res}-\mathbf I.
}
\]

This residual is a property of both the physical system and the chosen correction. It is not simply the negative of the parameter-estimation error for nonlinear or differently parameterized models.

For model-calibration strategy, the residual mismatch instead compares

\[
\boxed{
\mathbf H_{\rm phys}
\quad\text{with}\quad
\mathbf H_{\rm cal}
}
\]

under an explicitly declared metric/equivalence class.

---

## 16. Sources of residual calibration error

Residual error can contain several scientifically distinct contributions:

```text
calibration measurement noise
reference-source / fixture uncertainty
parameter-estimation uncertainty
model-form error
unmodeled sensor physics
finite calibration grid error
interpolation error
extrapolation error
time drift / temperature drift
hardware state or gain-state mismatch
reconfiguration / active-port mismatch
numerical approximation / regularization bias
reference-plane or de-embedding error
```

GeoDOA shall not report one scalar `calibration_error` without enough provenance to determine which class it represents.

---

## 17. Calibration uncertainty

A calibrated parameter estimate is generally uncertain.

A local covariance representation may be

\[
\boxed{
\mathbf P_{\theta}
=\operatorname{Cov}(\hat{\boldsymbol\theta}_{\rm cal}).
}
\]

If a response depends smoothly on parameters,

\[
\mathbf a(\boldsymbol\theta)
\approx
\mathbf a(\hat{\boldsymbol\theta})
+\mathbf J_a
(\boldsymbol\theta-\hat{\boldsymbol\theta}),
\]

then a first-order response uncertainty may be approximated by

\[
\boxed{
\mathbf R_{a,\rm cal}
\approx
\mathbf J_a
\mathbf P_{\theta}
\mathbf J_a^H.
}
\]

This is a local linear uncertainty propagation, not a universal distributional result.

Calibration uncertainty and subsequent physical drift are separate contributions.

---

## 18. Calibration domain

A calibration artifact is valid only on a declared domain.

Relevant axes may include:

\[
\boxed{
(f,\ \theta/\hat{\mathbf u},\ \text{range},\ \text{polarization},\ T,\ t,
\ \text{gain state},\ \text{sample rate},\ \text{LO state},\ \text{active channels},\ \text{port terminations},\ \text{hardware revision}).
}
\]

Not every calibration depends on every axis, but omitted dependencies must be a deliberate model assumption rather than an absent field interpreted as universality.

---

## 19. Interpolation and extrapolation

Calibration measurements are commonly obtained on a finite grid while operation occurs between grid points.

Let measured calibration states be

\[
\{\chi_m\}_{m=1}^{M}
\]

with corresponding calibration objects

\[
\{\mathcal K_m\}_{m=1}^{M}.
\]

A runtime calibration may require

\[
\boxed{
\mathcal K(\chi)
=\mathcal I_{\rm cal}
(\chi;\{\chi_m,\mathcal K_m\}),
}
\]

where \(\mathcal I_{\rm cal}\) is a declared interpolation model.

Interpolation of complex response must preserve phase/reference semantics. Naive interpolation of wrapped phase can be invalid.

Extrapolation outside the calibrated domain shall never occur silently. It must be:

- rejected;
- explicitly allowed with a warning/status;
- or governed by a validated parametric extrapolation model.

Interpolation method, grid density, and interpolation residual belong to calibration provenance.

---

## 20. Time validity, drift, and recalibration

Calibration has a time/state validity interval.

A system may exhibit

\[
\boxed{
\boldsymbol\theta_{\rm phys}(t,T,\chi)
}
\]

rather than one immutable parameter vector.

GeoDOA shall be able to distinguish:

- calibration acquisition time;
- calibration validity interval;
- hardware/firmware state;
- temperature/environment state;
- most recent validation/check time;
- drift estimate or uncertainty growth;
- recalibration trigger or policy.

A calibration file that is numerically readable but outside its validity state is not automatically scientifically compatible.

---

## 21. Relative versus absolute calibration

Relative calibration removes or estimates differences among channels with respect to a chosen gauge/reference.

Absolute calibration ties quantities to an external physical reference such as an absolute amplitude, phase, position, time, frequency, or field standard.

GeoDOA shall not promote relative calibration results to absolute physical claims.

Examples:

- relative channel phase does not define absolute RF phase without an external phase/time reference;
- relative gain does not establish absolute received field strength;
- relative geometry can define aperture shape while leaving rigid translation unobserved;
- relative delay can align channels while leaving common latency unknown.

---

## 22. Calibration reference planes

Every calibration/correction artifact shall identify the reference planes established in 3.8.

Examples:

- a cable/receiver loopback calibration may map RP-4 to RP-8 while excluding antenna/coupling effects;
- a VNA coupling calibration may apply at a port plane near RP-2/RP-3;
- an over-the-air measured manifold may aggregate RP-0 through RP-8 depending on measurement architecture;
- a digital deskew correction may operate only after RP-8.

Applying a calibration artifact at the wrong plane can double-count, omit, or misattribute effects even when numerical dimensions match.

---

## 23. Calibration composition

Two calibration artifacts may be composed only when their domains and reference planes are compatible.

If

\[
\mathcal C_1:\mathrm{RP}_b\rightarrow\mathrm{RP}_a
\]

and

\[
\mathcal C_2:\mathrm{RP}_c\rightarrow\mathrm{RP}_b,
\]

then a composition

\[
\boxed{
\mathcal C_1\circ\mathcal C_2
}
\]

may be meaningful.

But two independent calibrations that both compensate the same physical effect shall not both be applied unless their de-embedding/included-effects semantics explicitly justify the composition.

`Compatible shapes` is not enough.

---

## 24. Calibration and active-channel state

A calibration artifact has an array/channel state.

Digital removal of a channel after acquisition may allow a subset of an existing calibration to remain valid if upstream physics is unchanged.

Physically disabling, opening, shorting, reterminating, or changing the impedance state of an array port may change coupling/loading and therefore invalidate calibration of other channels.

Calibration compatibility shall therefore depend on physical port/termination state, not only on a channel mask vector.

---

## 25. Calibration of MIMO Tx/Rx systems

For MIMO sensing/radar, physical calibration may involve separate transmit and receive chains.

A separable narrowband physical virtual-channel response may contain

\[
\boxed{
g_{ij}^{\rm virt}
=g_{{\rm tx},i}\,g_{{\rm rx},j}
}
\]

only under the declared separable model.

Additional terms may arise from waveform generation, TDM timing, LO/reference phase evolution, propagation, coupling, and channel-specific processing.

GeoDOA shall preserve \((\mathrm{Tx}_i,\mathrm{Rx}_j)\) provenance and shall not calibrate a virtual channel as if it were an unrelated physical sensor unless that is the declared aggregate calibration strategy.

Tx calibration, Rx calibration, Tx-Rx relative phase calibration, timing calibration, and direct virtual-manifold calibration remain distinguishable.

---

## 26. Calibration and covariance statistics

### 26.1 Model-calibration path

If measurements are not transformed and the estimator uses \(\mathbf a_{\rm cal}\), the physical measurement covariance remains

\[
\boxed{
\mathbf R_y
=\operatorname E[\mathbf y\mathbf y^H].
}
\]

Calibration changes the model used to interpret this covariance, not the covariance itself.

### 26.2 Data-correction path

If

\[
\mathbf y_{\rm corr}=\mathbf C\mathbf y,
\]

then

\[
\boxed{
\mathbf R_{\rm corr}
=\mathbf C\mathbf R_y\mathbf C^H.
}
\]

This transforms signal and noise subspaces, noise color, eigenvalues, and conditioning.

For time-varying \(\mathbf C[k]\), a single congruence transform of one stationary covariance is generally insufficient.

---

## 27. Calibration and MUSIC/DOA estimator compatibility

A calibration is not successful merely because channel residuals are small in one engineering metric.

For classical MUSIC, a useful calibrated state generally requires:

- a manifold model compatible with the physical data-generating response;
- sufficiently fixed response over the covariance window;
- simultaneous-equivalent coherent channel observations;
- compatible complex-statistics model;
- an understood post-correction noise covariance;
- no unmodeled nonlinear/quantization regime that invalidates the linear manifold assumption.

A data correction that whitens one deterministic mismatch while making noise highly unequal/correlated can alter estimator performance.

Therefore calibration quality must ultimately be evaluated through manifold, covariance, eigenspace, and DOA consequences, developed in 3.11–3.12.

---

## 28. Calibration versus validation

Calibration and validation are not synonyms.

Calibration data are used to fit/construct a model or correction.

Validation evidence assesses whether the calibrated model performs acceptably, preferably under independent conditions or an explicitly separated evaluation protocol.

Using the same calibration samples to both fit and claim independent validation shall not be presented as external validation.

Formal validation/reproducibility semantics belong primarily to ADR-004, but ADR-003 shall preserve this boundary.

---

## 29. Calibration artifact provenance

A calibration artifact shall eventually be capable of recording at least:

```text
artifact identity / version
calibration type
characterization vs parameter fit vs direct manifold vs correction
input reference plane
output reference plane
included effects
excluded / de-embedded effects
physical channel identities
Tx/Rx identities where applicable
reference channel / gauge convention
absolute vs relative semantics
calibration source / fixture identity
source location/direction/range/polarization provenance
frequency / bandwidth / sample-rate state
gain / AGC / attenuation state
LO / clock / synchronization state
temperature / environment
active-channel and physical port state
hardware / firmware revision
acquisition time
validity interval/domain
estimation method and objective
regularization / constraints
interpolation method
grid definition
parameter estimates or response data
estimate uncertainty / covariance if available
fit residuals
held-out/check residuals if available
conditioning / singular-value diagnostics when relevant
software/Git provenance
notes on known limitations
```

The final schema belongs to later software design, but these scientific fields define the information that must not be irreversibly lost.

---

## 30. Deterministic gauge check

Consider

\[
\mathbf y
=
\begin{bmatrix}
2\\
0.5e^{j30^\circ}
\end{bmatrix}
s.
\]

If \(s\) is unknown, choose

\[
c=2e^{j10^\circ}.
\]

Then

\[
\mathbf g'
=c\mathbf g,
\qquad
s'=s/c
\]

produces the identical observed \(\mathbf y\).

Therefore the common complex scale of \(\mathbf g\) cannot be identified from that observation without an additional reference/gauge condition.

This check formalizes why relative gain/phase calibration requires a reference convention.

---

## 31. Deterministic ill-conditioning check

Let

\[
\mathbf H
=\begin{bmatrix}
1&0\\
0&0.01
\end{bmatrix}.
\]

Then

\[
\mathbf H^{-1}
=\begin{bmatrix}
1&0\\
0&100
\end{bmatrix}.
\]

For white pre-correction noise

\[
\mathbf R_n=\sigma^2\mathbf I,
\]

post-correction noise is

\[
\boxed{
\mathbf R_{n,\rm corr}
=\sigma^2
\begin{bmatrix}
1&0\\
0&10^4
\end{bmatrix}.
}
\]

The exact inverse removes deterministic attenuation mathematically but amplifies the second-channel noise variance by \(10^4\).

Calibration correctness therefore requires conditioning/noise analysis, not merely existence of an inverse.

This is an exploration check, not yet a formal GRP number.

---

## 32. Initial Phase-1 calibration profile

The initial validated Phase-1 profile may use the ideal sensor baseline from 3.8 with no physical calibration required.

Its calibration state shall be explicit rather than silently absent:

```text
physical sensor profile: ideal baseline
calibration requirement: none for deterministic sensor imperfections
calibration operator: identity / not-applied by declared profile
calibration provenance: baseline scientific profile identity
```

This allows later calibrated profiles to be compared against a clearly defined uncalibrated/ideal baseline without changing semantics.

---

## 33. Boundary and failure conditions reserved for later gates

Calibration must later be stress-tested for at least:

- insufficient calibration directions/frequencies/excitations;
- gauge ambiguity;
- rank-deficient sensitivity/Jacobian;
- ill-conditioned inverse correction;
- singular physical response;
- reference-channel failure;
- uncertain calibrator location/orientation/polarization;
- multipath during OTA calibration;
- calibration outside far-field assumptions;
- phase wrapping and delay ambiguity;
- clock/LO ambiguity;
- coupling model mismatch;
- double counting with measured/embedded manifolds;
- wrong reference plane;
- stale temperature/time/gain-state calibration;
- invalid interpolation/extrapolation;
- active-port state changes;
- nonlinear/clipped calibration measurements;
- calibration-data outliers;
- unmodeled conjugate/IQ response;
- correction-induced noise coloring/amplification;
- source/calibration parameter confounding;
- non-independent calibration and validation evidence.

These are exploration requirements, not yet Gate F PASS evidence.

---

## 34. Candidate decisions from Exploration 3.9

- **3.9-D1** — Calibration is a separate estimation/correction graph associated with, but not physically causal within, the forward sensor graph.
- **3.9-D2** — Characterization, parameter calibration, model calibration, data correction, direct response calibration, self-calibration, and calibration tracking are distinct meanings.
- **3.9-D3** — Nominal value, realized physical value, calibrated estimate, correction value, residual error, and estimate uncertainty shall remain distinguishable.
- **3.9-D4** — Every calibration result is conditional on a declared calibration experiment/model.
- **3.9-D5** — Calibration-source/fixture uncertainty is part of calibration uncertainty and shall not be silently treated as exact truth.
- **3.9-D6** — External reference, internal/loopback reference, OTA reference, and self-calibration are distinct evidence classes with different included effects.
- **3.9-D7** — Internal calibration shall not be assumed to include antenna/free-space/coupling effects beyond its physical injection/reference planes.
- **3.9-D8** — Self-calibration is a joint-estimation problem and requires explicit identifiability analysis.
- **3.9-D9** — Numerical optimizer convergence is not evidence of physical identifiability.
- **3.9-D10** — Common complex scale may be a gauge freedom when source complex amplitude is unknown.
- **3.9-D11** — A reference-channel normalization fixes a representation gauge and does not imply an error-free physical reference channel.
- **3.9-D12** — Static phase, delay, geometry error, source direction, gain, element response, coupling, and oscillator terms may be partially confounded depending on calibration diversity.
- **3.9-D13** — Calibration experiment design shall be judged by sensitivity/observability, not only measurement count.
- **3.9-D14** — Local Jacobian rank/conditioning is a valid diagnostic for local parameter observability under a declared model.
- **3.9-D15** — Calibration diversity may be required over direction, frequency, range, polarization, level, temperature, time, or hardware state.
- **3.9-D16** — Calibration objective/residual domain and weighting must be explicit; optimizer choice does not define the scientific model.
- **3.9-D17** — Weighted least squares/maximum-likelihood equivalence is conditional on the declared probability model.
- **3.9-D18** — Geometry calibration preserves nominal geometry and records estimated physical geometry separately.
- **3.9-D19** — Gain/phase calibration shall declare relative versus absolute semantics and gauge/reference convention.
- **3.9-D20** — Physical delay is calibrated through frequency-dependent phase/time information; one-frequency phase alone cannot uniquely separate delay and static phase.
- **3.9-D21** — Fixed skew correction and SRO correction are distinct; broadband SRO generally requires time-base/resampling semantics.
- **3.9-D22** — Coupling/network calibration shall preserve whether the calibrated object is Z, S, loaded-port transform, effective coupling, or aggregate manifold response.
- **3.9-D23** — I/Q calibration may require widely linear coefficients; complex-gain calibration is not universally sufficient.
- **3.9-D24** — ADC/receiver calibration shall preserve the measurement/code/reference plane to which the correction applies.
- **3.9-D25** — Nonlinearity calibration is valid only over a declared operating-level/state domain.
- **3.9-D26** — Model calibration and data correction are distinct strategies and may have different noise/statistical consequences.
- **3.9-D27** — Data correction transforms noise covariance as \(\mathbf C\mathbf R_n\mathbf C^H\) for linear correction.
- **3.9-D28** — Exact inverse correction requires the relevant calibration operator to be invertible and scientifically compatible with the correction domain.
- **3.9-D29** — A singular/null-space response contains information that calibration cannot reconstruct by inversion.
- **3.9-D30** — Small singular values can cause severe noise/uncertainty amplification even when an algebraic inverse exists.
- **3.9-D31** — Minimum singular value and condition number are distinct diagnostics and shall not be conflated.
- **3.9-D32** — Pseudoinverse/regularized corrections must record their method and parameters; they are not silently labeled exact inverse calibration.
- **3.9-D33** — Regularization trades inversion fidelity against bias/noise/uncertainty amplification.
- **3.9-D34** — Residual calibration error shall be defined in the appropriate parameter/response/operator domain rather than by one generic scalar.
- **3.9-D35** — Calibration residuals may contain measurement, reference, estimation, model-form, interpolation, drift, state-mismatch, regularization, and reference-plane contributions.
- **3.9-D36** — Calibration uncertainty and later physical drift are separate quantities.
- **3.9-D37** — Parameter-estimate uncertainty may be propagated locally to response uncertainty with a declared Jacobian approximation.
- **3.9-D38** — Every calibration artifact has a declared validity domain; absence of a dependency field shall not imply universal validity.
- **3.9-D39** — Calibration interpolation is part of the scientific model and must preserve complex phase/reference semantics.
- **3.9-D40** — Extrapolation outside calibration domain shall never occur silently.
- **3.9-D41** — Calibration has time/state validity and may require recalibration or tracking.
- **3.9-D42** — Relative calibration shall not be promoted to absolute physical claims without an external reference.
- **3.9-D43** — Calibration artifacts must declare input/output reference planes and included/de-embedded effects.
- **3.9-D44** — Calibration composition requires compatible planes/domains/provenance, not merely compatible array dimensions.
- **3.9-D45** — Physical port/termination changes can invalidate coupling/manifold calibration even if the digital channel mask appears similar.
- **3.9-D46** — MIMO calibration shall preserve Tx/Rx physical-channel provenance and distinguish Tx, Rx, relative Tx-Rx, timing, and aggregate virtual-manifold calibration.
- **3.9-D47** — Model-calibration strategy changes estimator response knowledge without directly transforming measured covariance.
- **3.9-D48** — Data correction transforms covariance/eigenspaces/noise statistics and requires compatible downstream estimator assumptions.
- **3.9-D49** — Calibration quality must ultimately propagate to manifold, covariance, eigenspace, and DOA metrics rather than stop at parameter-fit residuals.
- **3.9-D50** — Calibration and validation are distinct; fitting calibration data is not independent validation evidence.
- **3.9-D51** — Calibration provenance must preserve source/fixture, planes, channels, domain, state, method, regularization, interpolation, uncertainty, residuals, and software/hardware identity sufficient for reproducibility.
- **3.9-D52** — The initial Phase-1 ideal-sensor profile may explicitly use identity/no-applied calibration while preserving calibration-state semantics.

---

## 35. Scientific anchors for this exploration

The contract is consistent with established array-calibration literature in which calibration is treated as parameter/response estimation under model ambiguity and limited observability, including self-calibration formulations that jointly estimate sensor errors and DOA and measured-manifold approaches that use finite calibration grids plus interpolation.

Representative anchors include:

- K. N. Ramamohan, S. P. Chepuri, D. F. Comesana, and G. Leus, **Self Calibration of Scalar and Vector Sensor Arrays**, 2021 — joint gain/phase and DOA estimation with identifiability analysis.
- C. M. S. See and B.-K. Poh, **Parametric sensor array calibration using measured steering vectors of uncertain locations**, IEEE Transactions on Signal Processing, 1999, DOI: 10.1109/78.752611.
- B. Yang, T. McKelvey, and M. Viberg, **Array Calibration using Array Response Interpolation and Parametric Modeling**, EUSIPCO 2015, DOI: 10.1109/EUSIPCO.2015.7362601.

These references support the scientific taxonomy; GeoDOA's exact contracts remain project decisions subject to Gates A–F.

---

## 36. Immediate next step

The next work session shall start at **Exploration 3.10 — Direct Measured / CST-Derived Manifold Calibration**.

Exploration 3.10 must reconcile at least:

1. measured manifold versus EM/CST manifold versus physical truth;
2. absolute/relative/common-scale alignment during manifold acquisition;
3. angle/direction, frequency, polarization, range, and state grids;
4. anechoic/OTA measurement reference geometry and phase center;
5. CST/full-wave port/reference-plane definitions;
6. embedded element response, coupling, radome/platform/environment included-effects provenance;
7. de-embedding and double-count prevention;
8. interpolation of complex manifolds between calibrated states;
9. normalization and preservation of physically meaningful amplitude;
10. uncertainty/noise in measured steering vectors;
11. registration between measured coordinate frame and GeoDOA frame;
12. channel identity/ordering and missing channels;
13. extrapolation policy;
14. direct calibrated-manifold use in MUSIC and other estimators;
15. comparison between parametric and direct-manifold calibration;
16. storage/provenance requirements for imported CST/measured data.

Do not start Gate A yet.
