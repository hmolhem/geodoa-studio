# ADR-003 Exploration 3.8 — Unified Sensor-Imperfection Operator

- **Phase:** 0C — Scientific Foundations
- **Status:** EXPLORATION COMPLETE — CANDIDATE CONTRACT, NOT ACCEPTED
- **Parent ADR:** ADR-003 — Sensor Imperfections, Mutual Coupling, and Calibration
- **Branch:** `docs/phase0c-scientific-conventions`
- **Depends on:** ADR-001, ADR-002, ADR-003 Explorations 3.1–3.7
- **Acceptance gates:** Not started

> This is the dedicated exploration record for ADR-003 Section 3.8. It is not an accepted governing ADR. Candidate decisions remain subject to 3.9–3.14 reconciliation, Gates A–F, Golden Reference evidence, boundary/failure analysis, and final acceptance.

---

## 1. Primary question

Explorations 3.1–3.7 introduced geometry perturbation, element response, mutual coupling/loading, electronic gain/phase, delay, synchronization errors, oscillator/reference errors, receiver noise, I/Q imbalance, nonlinear response, sampling, and ADC quantization.

Exploration 3.8 answers:

> How can GeoDOA compose these effects in one scientifically coherent sensor-system model without falsely treating every imperfection as one matrix, losing physical ordering, or double counting effects already embedded in measured/full-wave manifolds?

The governing answer is:

\[
\boxed{
\text{GeoDOA uses a typed sensor-imperfection operator graph, not one universal imperfection matrix.}
}
\]

A matrix product is a valid specialization only for a subset of compatible deterministic linear effects defined on the same scientific domain and reference plane.

---

## 2. Two distinct modeling levels

GeoDOA shall distinguish two related but different objects.

### 2.1 Manifold / response-level model

This level answers how a declared source condition produces a deterministic coherent sensor response before random sample realization.

Conceptually,

\[
\boxed{
\mathbf a_{\rm nom}(\xi)
\longrightarrow
\mathbf a_{\rm phys}(\xi,\chi)
}
\]

where \(\xi\) denotes source/scene variables and \(\chi\) denotes sensor-system state/configuration.

### 2.2 Sample / measurement-level model

This level answers how time-varying source waveforms, receiver noise, timing, sampling, nonlinearities, and quantization produce digital measurements:

\[
\boxed{
\{s_q(t),\xi_q\}_{q=1}^{Q}
\longrightarrow
\mathbf y[k]
}
\]

The sample-level model is strictly more general. Not every sample-level effect has a meaningful static steering-vector representation.

Therefore a `physical_manifold` object and a `physical_measurement_pipeline` object shall not be conflated.

---

## 3. Scientific operator taxonomy

GeoDOA shall preserve the type of each imperfection. The following categories are distinct.

### 3.1 Geometry / propagation-state transformation

Position error and deformation change physical geometry before steering/manifold evaluation:

\[
\boxed{
\mathbf r_n^{\rm phys}
=\mathbf r_n^{\rm nom}+\boldsymbol\varepsilon_n.
}
\]

The primary model is therefore

\[
\boxed{
\mathbf a_{\rm geo}^{\rm phys}(\xi)
=\mathcal A_{\rm prop}(\{\mathbf r_n^{\rm phys}\},\xi),
}
\]

not universally

\[
\mathbf a_{\rm geo}^{\rm phys}=\mathbf D\mathbf a_{\rm nom}.
\]

A diagonal phase perturbation is only a derived far-field/narrowband specialization.

### 3.2 Source-condition-dependent element operator

For an uncoupled scalar-element specialization,

\[
\boxed{
\mathbf P(\xi,\chi)
=\operatorname{diag}(b_1,\ldots,b_N)
}
\]

may represent complex element response. Because \(b_n\) can depend on direction, frequency, polarization, orientation, and environment, \(\mathbf P\) may be source-specific.

### 3.3 Cross-channel linear network/loading operator

A declared loaded-port or effective coupling operator may act as

\[
\boxed{
\mathbf z=\mathbf C(\chi,f)\mathbf x
}
\]

or, for the multiport specialization established in 3.5,

\[
\mathbf v_L=\mathbf T_L\mathbf v_{\rm oc}.
\]

This is ordinary complex linear cross-channel mixing only within its declared domain.

### 3.4 Diagonal or general linear electronic response

Electronic gain/phase/delay/filtering may be represented locally in frequency/time domain by a linear operator such as

\[
\boxed{
\mathbf G_{\rm rx}(f,t,\chi).
}
\]

A diagonal model is a specialization, not a universal receiver law.

### 3.5 Widely linear operator

I/Q imbalance may require

\[
\boxed{
\mathbf y=\mathbf A\mathbf x+\mathbf B\mathbf x^*.
}
\]

This is not complex-linear in \(\mathbf x\) alone. In an augmented representation,

\[
\tilde{\mathbf x}
=\begin{bmatrix}\mathbf x\\\mathbf x^*\end{bmatrix},
\qquad
\tilde{\mathbf y}
=\begin{bmatrix}\mathbf y\\\mathbf y^*\end{bmatrix},
\]

it can be written as

\[
\boxed{
\tilde{\mathbf y}
=
\begin{bmatrix}
\mathbf A&\mathbf B\\
\mathbf B^*&\mathbf A^*
\end{bmatrix}
\tilde{\mathbf x}.
}
\]

Thus an impairment may be linear in an augmented space without being representable by an ordinary \(N\times N\) complex matrix.

### 3.6 Sampling / time-grid operator

Channel-specific sampling acts on continuous-time or reconstructed waveforms at declared physical epochs:

\[
\boxed{
[\mathcal S_{\mathbf t}\{\mathbf z\}]_n[k]
=z_n(t_n[k]).
}
\]

Fixed skew, SRO, and jitter alter the time grid. This is not generally an \(N\times N\) spatial-channel matrix.

### 3.7 Additive stochastic injection

Noise is introduced at a declared physical stage:

\[
\boxed{
\mathbf z_{r}^{+}
=\mathbf z_{r}^{-}+\mathbf n_r.
}
\]

Noise injection is not a deterministic manifold operator. Its covariance and cross-stage transformations depend on where it enters.

### 3.8 Nonlinear operator

Compression, clipping, intermodulation, and other nonlinearities require

\[
\boxed{
\mathbf y=\mathcal F_{\rm nl}(\mathbf x;\chi)
}
\]

with no assumption of superposition.

### 3.9 Quantization / discrete code mapping

ADC conversion requires a declared quantizer/code map

\[
\boxed{
\mathbf c[k]=\mathcal Q(\mathbf z[k];\chi_{\rm ADC}).
}
\]

A quantizer is nonlinear and changes the numerical representation/domain. An additive quantization-noise model is an approximation, not the primary operator type.

### 3.10 Selection / masking operator

A digital active-channel view may use a selection matrix

\[
\boxed{
\mathbf y_{\rm sel}=\mathbf S_{\rm mask}\mathbf y,
}
\]

where \(\mathbf S_{\rm mask}\) preserves stable source channel identity and records the mapping from physical channels to the selected processing view.

This post-acquisition selection is distinct from a physical port-state or termination change, which can alter upstream coupling/loading and therefore requires a different physical-system state.

---

## 4. Reference planes and scientific domains

Composition is meaningful only if output and input domains match. GeoDOA shall therefore preserve reference-plane semantics.

A conceptual receive chain may contain the following planes:

```text
RP-0  incident field / source condition
RP-1  geometry/propagation response
RP-2  element/open-circuit array response
RP-3  loaded/coupled port response
RP-4  analog receiver/baseband response
RP-5  continuous-time pre-sampling waveform
RP-6  sampled pre-quantization values
RP-7  ADC code output
RP-8  dequantized digital measurement
RP-9  selected/processed array view
```

These identifiers are conceptual exploration labels, not yet final API enum names.

Every operator/calibration artifact shall eventually declare at least:

\[
\boxed{
\text{input plane},
\text{output plane},
\text{domain variables},
\text{included effects},
\text{configuration state},
\text{provenance}.
}
\]

An operator cannot be composed merely because its matrix dimensions happen to match.

---

## 5. Canonical physical ordering

A defensible generic physical chain is

```text
scene/source state
    ↓
propagation evaluated on physical geometry
    ↓
element / polarization / open-circuit response
    ↓
port loading / mutual coupling / cross-channel network interaction
    ↓
analog receiver transfer: gain / phase / delay / filtering / LO-IQ effects
    ↓
receiver-noise injections at their physical stages
    ↓
analog nonlinearity / compression as applicable
    ↓
physical sampling epochs / aperture effects
    ↓
ADC range / clipping / quantization / code mapping
    ↓
digital measurement
    ↓
digital masking / deskew / calibration / DSP
```

This chain is a semantic skeleton, not an assertion that every real receiver contains exactly one block of each type.

The governing rule is:

\[
\boxed{
\text{physical ordering follows cause and reference plane, not algebraic convenience.}
}
\]

Exploration 3.9 will govern calibration/correction. Calibration is not inserted into the physical forward chain as if it caused the measurement.

---

## 6. A bounded linear-manifold specialization

For a single source under a fixed frequency/time/state where all selected effects are ordinary complex linear and source-compatible, one specialization may be

\[
\boxed{
\mathbf a_{\rm phys}
=
\mathbf G_{\rm rx}
\mathbf C
\mathbf P
\mathbf a_{\rm geo}^{\rm phys}.
}
\]

If channel delay is represented at one declared narrowband frequency,

\[
\mathbf G_{\rm rx}
\rightarrow
\mathbf G_{\rm gp}\mathbf D_{\tau},
\]

and a time-frozen receiver-reference factor may also enter.

This product is valid only if:

1. all factors refer to compatible reference planes;
2. their included-effects provenance proves no double counting;
3. source dependence is compatible with the chosen factorization;
4. time/frequency variation is negligible or frozen under a declared approximation;
5. no nonlinear, quantizing, time-warp, or conjugate term is being hidden inside the product.

Thus

\[
\boxed{
\mathbf H_{\rm lin}
=\mathbf G_{\rm rx}\mathbf C\mathbf P
}
\]

may be a useful effective operator, but it is not the universal definition of sensor imperfection.

---

## 7. Noncommutativity and ordering

Cross-channel and diagonal operators generally do not commute:

\[
\boxed{
\mathbf C\mathbf G\neq\mathbf G\mathbf C.
}
\]

Two diagonal matrices expressed in the same channel basis commute algebraically, but that does not erase their different physical semantics or calibration provenance.

A common scalar factor \(c\mathbf I\) commutes with ordinary linear matrices, but may still matter before nonlinearities or quantization because it changes absolute signal level, headroom, clipping probability, and quantizer utilization.

Therefore projective irrelevance to an ideal linear DOA manifold does not imply physical irrelevance to the full receiver chain.

### 7.1 Deterministic two-channel check

Let

\[
\mathbf G=
\begin{bmatrix}1&0\\0&2\end{bmatrix},
\qquad
\mathbf C=
\begin{bmatrix}1&0.5\\0.5&1\end{bmatrix}.
\]

Then

\[
\boxed{
\mathbf C\mathbf G
=
\begin{bmatrix}1&1\\0.5&2\end{bmatrix}
}
\]

while

\[
\boxed{
\mathbf G\mathbf C
=
\begin{bmatrix}1&0.5\\1&2\end{bmatrix}.
}
\]

The matrices differ. Reordering physical gain and cross-channel mixing without derivation changes the model.

This is an exploration check, not a new formal GRP number.

---

## 8. Multi-source source-dependence

For multiple sources, a single common sensor matrix is not always valid.

A general deterministic pre-noise receive model may require

\[
\boxed{
\mathbf x(t)
=
\sum_{q=1}^{Q}
\mathcal H_{\rm rx}
\left[
\mathbf a_{q}^{\rm pre}(t;\xi_q,\chi)s_q(t)
\right]
}
\]

or, in a linear specialization,

\[
\boxed{
\mathbf x(t)
=
\sum_{q=1}^{Q}
\mathbf H_q(t,f,\chi)
\mathbf a_{\rm nom}(\xi_q,f)s_q(t).
}
\]

The subscript \(q\) matters when element response, polarization, direction-dependent effective coupling, near-field geometry, or another effect is source-condition dependent.

A shared \(\mathbf H\) may be used only when the declared model proves that the same operator applies to all sources in the scene.

---

## 9. Time-varying and frequency-dependent composition

A receiver operator may depend on frequency, time, temperature, gain state, clock state, or array configuration:

\[
\boxed{
\mathcal H=\mathcal H(f,t,\chi).
}
\]

A fixed-manifold covariance model requires more than narrowband propagation. It also requires that relevant sensor-system state be sufficiently constant over the declared snapshot/covariance window.

Examples that can invalidate a fixed operator include:

- differential CFO or phase drift;
- differential SRO;
- time-varying AGC;
- thermal drift of channel gain/phase;
- switching/reconfiguration;
- motion-dependent or source-dependent response;
- time-varying nonlinear operating point.

GeoDOA shall not silently time-average a changing sensor operator and call the result one static manifold without a declared approximation and error diagnostic.

---

## 10. Noise-injection ordering

Suppose a purely linear chain contains operators

\[
\mathbf H_1,\mathbf H_2,\ldots,\mathbf H_M
\]

and independent additive noise \(\mathbf n_r\) is injected after stage \(r\).

Then the final measurement is

\[
\boxed{
\mathbf y
=
\mathbf H_M\cdots\mathbf H_1\mathbf x
+
\sum_{r=0}^{M}
\mathbf H_{M:r+1}\mathbf n_r,
}
\]

where \(\mathbf H_{M:r+1}\) denotes the product of downstream operators after the injection point and equals identity when no downstream operator exists.

Under zero-mean mutual independence assumptions,

\[
\boxed{
\mathbf R_y
=
\mathbf H\mathbf R_x\mathbf H^H
+
\sum_r
\mathbf H_{M:r+1}
\mathbf R_{n_r}
\mathbf H_{M:r+1}^H,
}
\]

with

\[
\mathbf H=\mathbf H_M\cdots\mathbf H_1.
\]

If noises are correlated, cross-covariance terms must be retained; the sum-of-independent-covariances form is not valid by default.

Thus one generic `noise_variance` attached to the end of a receiver chain is insufficient when physical noise sources enter at different stages.

---

## 11. Nonlinear and quantized chains cannot be collapsed into one matrix

If a nonlinear or quantizing stage exists,

\[
\mathbf y
=\mathcal Q\left(
\mathcal F_{\rm nl}\left(
\mathbf H\mathbf x+\mathbf n
\right)
\right),
\]

then in general there is no matrix \(\mathbf H_{\rm total}\) such that

\[
\mathbf y=\mathbf H_{\rm total}\mathbf x
\]

for all inputs.

Likewise, the order

\[
\mathcal Q(\mathbf G\mathbf x)
\]

is not equivalent to

\[
\mathbf G\mathcal Q(\mathbf x)
\]

in general, and analog gain before clipping/quantization cannot be moved after the ADC as an algebraic convenience.

The primary covariance definition must therefore remain

\[
\boxed{
\mathbf R_y
=\operatorname E[\mathbf y\mathbf y^H]
}
\]

for the actual declared measurement operator. Simplified covariance propagation is a specialization with explicit assumptions.

---

## 12. Sampling and channel-space transformations do not share the same domain

Spatial matrices act on channel vectors at a declared time/frequency state. Sampling operators act on continuous-time waveforms or reconstructed functions to create discrete-time samples.

Therefore an expression such as

\[
\mathbf D_{\rm skew}\mathbf a
\]

may be a valid narrowband single-frequency approximation to fixed skew, but it is not the general definition of sampling-time mismatch.

For broadband or SRO cases, the correct semantics remain a channel-dependent time grid and, if corrected, a declared interpolation/resampling operation.

This prevents the unified model from falsely treating timing errors as ordinary static channel gains.

---

## 13. Direct measured / EM manifold as a bypass or aggregate response

A measured or full-wave manifold may already include several upstream effects:

\[
\boxed{
\mathbf a_{\rm meas/em}(\xi,\chi)
=
\mathcal H_{\rm aggregate}[\mathbf a_{\rm nominal}]
}
\]

without exposing a unique factorization into \(\mathbf P\), \(\mathbf C\), geometry error, phase center, and other causes.

GeoDOA shall allow such an aggregate manifold to replace the corresponding parametric upstream chain at a declared reference plane.

For example:

```text
Option A — parametric path
geometry -> isolated element -> coupling/loading -> receiver

Option B — full-wave/manifold path
measured/CST aggregate array response -> receiver stages not already included
```

The aggregate path must carry an `included effects` record. Downstream effects may be appended only when the calibration/simulation reference plane proves they are not already included.

There shall be no automatic decomposition of an aggregate measured manifold into physical causes without an identifiability model.

---

## 14. Model calibration versus data correction

The forward physical operator graph and the calibration/correction graph remain distinct.

If the forward system is

\[
\mathbf y=\mathcal F_{\rm phys}(\mathbf x),
\]

calibration may estimate parameters

\[
\hat\theta_{\rm cal}
\]

and produce either:

1. a calibrated processing model \(\mathcal F_{\rm cal}\), or
2. a correction operator \(\mathcal C_{\rm corr}\) applied to measurements.

GeoDOA shall not write

\[
\mathcal F_{\rm phys}=\mathcal C_{\rm corr}\mathcal F_{\rm nom}
\]

merely because a correction happens to numerically invert some effect.

Exploration 3.9 will govern invertibility, regularization, reference planes, parameter calibration, and residual error.

---

## 15. Common versus relative effects across the full chain

A common complex scalar can be projectively irrelevant to a normalized linear manifold while remaining relevant to the physical receiver.

Examples:

- common phase before an instantaneous linear covariance may cancel;
- common gain can change received SNR and ADC utilization;
- common gain before a nonlinear stage changes compression/clipping;
- common time shift can preserve spatial simultaneity while altering absolute epoch;
- common CFO can cancel in simultaneous spatial covariance but become relative phase in TDM-MIMO.

Therefore the unified contract shall never use `common = harmless` as a general rule.

The correct statement is:

\[
\boxed{
\text{relevance of a common effect depends on the downstream observable and operator chain.}
}
\]

---

## 16. Physical state versus stochastic uncertainty

An imperfection parameter may have a probability distribution for simulation/uncertainty analysis, but the physical system at one realization has a realized state.

For parameter vector \(\boldsymbol\theta\), distinguish

\[
\boxed{
p(\boldsymbol\theta)}
\]

from

\[
\boxed{
\boldsymbol\theta^{(r)}.
}
\]

The realized operator graph is conditional on \(\boldsymbol\theta^{(r)}\). Randomizing a parameter across Monte Carlo trials is not equivalent to adding white measurement noise within each trial.

This distinction applies to position error, gain/phase mismatch, delay, coupling uncertainty, clock offset, receiver offset, and calibration residuals.

---

## 17. Channel identity, masking, and dimensionality

Stable physical channel identity is inherited from ADR-001/ADR-002.

A digital selection matrix may reduce a processing vector from \(N\) physical channels to \(N_a\) active processing channels:

\[
\boxed{
\mathbf y_a=\mathbf S_{\rm mask}\mathbf y,
\qquad
\mathbf S_{\rm mask}\in\{0,1\}^{N_a\times N}.
}
\]

The selected view shall retain the mapping to original physical channel IDs.

A physically disabled/open/shorted/reterminated port is not represented solely by \(\mathbf S_{\rm mask}\); it changes sensor-system state and may require recomputation/recalibration of the upstream network/manifold.

---

## 18. Estimator-compatibility contract

The unified model shall expose which estimator assumptions remain valid. Compatibility is progressive and multi-axis, not one generic Boolean.

At minimum, future compatibility metadata must be able to distinguish:

1. **linear-manifold compatibility** — can the source response be represented as a linear superposition of source steering/manifold vectors?
2. **fixed-manifold compatibility** — is the response sufficiently constant over the processing window?
3. **simultaneous-snapshot compatibility** — do channels form a simultaneous-equivalent coherent observation?
4. **narrowband compatibility** — can differential delays be represented as phase over the declared band?
5. **ordinary-complex covariance compatibility** — is covariance alone sufficient, or is augmented/pseudocovariance processing required?
6. **unquantized/high-resolution compatibility** — is classical continuous-amplitude covariance processing appropriate?
7. **noise-model compatibility** — are white/equal/independent noise assumptions justified?
8. **source-superposition compatibility** — do nonlinear receiver effects invalidate linear source addition?
9. **calibration-domain compatibility** — is the operating state inside the calibration validity domain?

A classical narrowband MUSIC pipeline requires a specific compatible subset; GeoDOA shall reject or explicitly warn on incompatible profiles rather than silently coerce them into an ideal model.

---

## 19. Initial Phase-1 validated profile

The unified contract permits a deliberately small initial implementation.

The initial validated profile may use:

```text
nominal physical geometry
    ↓
ideal scalar identical elements
    ↓
no mutual coupling / ideal loading
    ↓
unity channel gain and zero relative phase/delay
    ↓
common coherent clock/reference
    ↓
zero differential skew / SRO / CFO / jitter
    ↓
linear receiver
    ↓
ideal additive noise model already governed by ADR-002
    ↓
ideal simultaneous sampling semantics
    ↓
unquantized floating-point measurement representation
    ↓
no I/Q imbalance / clipping / compression
```

For this profile, the deterministic sensor-imperfection portion reduces to identity relative to the ADR-001/ADR-002 nominal model:

\[
\boxed{
\mathcal H_{\rm sensor}^{\rm Phase1}
\equiv\mathcal I
}
\]

within the declared baseline assumptions.

This does not delete the richer 3.1–3.8 contract. It establishes a validated baseline from which later profiles can activate one bounded imperfection family at a time.

---

## 20. Software-semantic implications

Although Phase 0C does not yet authorize implementation, the scientific contract implies several future architecture constraints:

- do not expose one untyped `imperfection_matrix` for all effects;
- use typed model components with explicit input/output semantic planes;
- preserve physical units for geometry, delay, sample time, frequency, gain, ADC range, and other dimensional quantities;
- preserve source dependence, frequency dependence, time dependence, and system-state dependence;
- preserve included-effects/de-embedding provenance;
- preserve channel identity through selection/reordering views;
- keep forward physical modeling separate from calibration/correction;
- permit aggregate measured/EM manifolds without forcing a fictitious parametric decomposition;
- expose estimator compatibility and approximation status;
- distinguish stochastic parameter generators from realized imperfection states;
- distinguish analog acquisition quantization from later DSP/FPGA fixed-point arithmetic.

No particular Python class hierarchy is accepted by this exploration; that belongs to implementation architecture after scientific contracts are accepted.

---

## 21. Boundary and failure considerations reserved for later gates

The unified framework must later be stress-tested for at least:

- incompatible reference planes;
- double counting between embedded/full-wave response and explicit coupling/element models;
- singular/ill-conditioned inverse calibration;
- time-varying operators inside covariance windows;
- source-dependent operators incorrectly forced into one shared matrix;
- nonlinear operating regions;
- quantizer overload/coarse quantization;
- improper complex statistics from I/Q imbalance;
- differential sampling grids;
- active-port state changes;
- zero/null channel responses;
- missing calibration provenance;
- invalid extrapolation outside calibration domain;
- unsupported operator compositions.

These are not yet Gate F PASS evidence.

---

## 22. Small deterministic composition checks

### 22.1 Linear composition

With

\[
\mathbf a=\begin{bmatrix}1\\-j\end{bmatrix},
\quad
\mathbf P=\begin{bmatrix}1&0\\0&0.8\end{bmatrix},
\quad
\mathbf C=\begin{bmatrix}1&0.2\\0.2&1\end{bmatrix},
\]

first

\[
\mathbf P\mathbf a
=\begin{bmatrix}1\\-0.8j\end{bmatrix},
\]

then

\[
\boxed{
\mathbf C\mathbf P\mathbf a
=\begin{bmatrix}1-0.16j\\0.2-0.8j\end{bmatrix}.
}
\]

Using \(\mathbf P\mathbf C\mathbf a\) generally gives a different result, demonstrating that physical ordering matters.

### 22.2 Common scalar before clipping

Let scalar quantization input be limited to \([-1,1]\). For \(x=0.8\):

- common gain \(g=1\) leaves the sample in range;
- common gain \(g=2\) produces analog value \(1.6\), which clips before ADC output.

Thus a common scalar that is projectively irrelevant to an ideal normalized manifold is not irrelevant to the full measurement chain.

These are exploration checks, not new formal GRP numbers.

---

## 23. Candidate decisions from Exploration 3.8

- **3.8-D1** — GeoDOA shall model sensor imperfections as a typed operator graph, not one universal imperfection matrix.
- **3.8-D2** — Manifold/response-level modeling and sample/measurement-level modeling are distinct scientific levels.
- **3.8-D3** — Position error primarily modifies physical geometry/propagation arguments; diagonal phase error is only a bounded specialization.
- **3.8-D4** — Element response may be source-condition dependent and therefore need not be one source-independent matrix.
- **3.8-D5** — Mutual coupling/loading is a cross-channel linear operator only within an explicitly declared port/manifold domain.
- **3.8-D6** — Electronic response may be diagonal or general linear and may depend on frequency, time, and receiver state.
- **3.8-D7** — I/Q imbalance is generally widely linear and requires conjugate terms or an augmented-domain representation.
- **3.8-D8** — Sampling/time-grid effects are not generally representable by a static spatial-channel matrix.
- **3.8-D9** — Additive noise injection is a stochastic stage, not a deterministic manifold operator.
- **3.8-D10** — Compression, clipping, intermodulation, and other nonlinearities require nonlinear operator semantics.
- **3.8-D11** — ADC quantization/code mapping is nonlinear and changes measurement representation; additive quantization noise is only a declared approximation.
- **3.8-D12** — Digital masking/selection is distinct from a physical port-state/termination change.
- **3.8-D13** — Scientific composition requires compatible input/output reference planes, not merely matching matrix dimensions.
- **3.8-D14** — Operator artifacts must preserve domain variables, included effects, configuration state, and provenance.
- **3.8-D15** — Physical ordering follows causal/reference-plane meaning rather than algebraic convenience.
- **3.8-D16** — Calibration/correction is not part of the physical forward causal chain.
- **3.8-D17** — A product \(\mathbf H_{\rm lin}=\mathbf G\mathbf C\mathbf P\) is a bounded linear specialization, not the universal sensor model.
- **3.8-D18** — A linear matrix product is valid only when reference planes, provenance, source dependence, time/frequency state, and operator types are compatible.
- **3.8-D19** — Cross-channel and diagonal operators generally do not commute; ordering must not be silently changed.
- **3.8-D20** — Algebraic commutation of two diagonal matrices does not erase their different physical semantics or calibration provenance.
- **3.8-D21** — Common scalar factors may commute algebraically with linear operators while remaining physically relevant before nonlinear/quantizing stages.
- **3.8-D22** — A shared sensor matrix across multiple sources requires evidence that the same operator applies to every source condition.
- **3.8-D23** — Sensor-system time/frequency/state dependence must be explicit and can independently invalidate a fixed-manifold approximation.
- **3.8-D24** — A changing sensor operator shall not be silently averaged into one static manifold without declared approximation/error semantics.
- **3.8-D25** — Noise covariance propagation depends on the physical injection stage and all downstream operators.
- **3.8-D26** — Sum-of-transformed-noise-covariances requires the corresponding independence assumptions; correlated noise needs cross terms.
- **3.8-D27** — Nonlinear/quantized chains cannot generally be collapsed into one matrix or one additive white-noise term.
- **3.8-D28** — Analog gain before clipping/quantization cannot generally be moved to the digital side of the ADC.
- **3.8-D29** — Sampling operators and spatial-channel matrices act on different scientific domains even when a narrowband approximation makes their numerical effects look similar.
- **3.8-D30** — Direct measured/EM manifolds may replace an upstream parametric subgraph at a declared reference plane.
- **3.8-D31** — Aggregate measured/EM manifolds require included-effects provenance to prevent double counting.
- **3.8-D32** — GeoDOA shall not automatically decompose an aggregate measured manifold into physical causes without an identifiability model.
- **3.8-D33** — Model calibration and data correction remain distinct from the forward physical operator graph and are developed in 3.9.
- **3.8-D34** — Whether a common effect is harmless depends on the downstream observable/operator chain; `common` is not synonymous with `irrelevant`.
- **3.8-D35** — A stochastic parameter distribution and a realized physical imperfection state are distinct objects.
- **3.8-D36** — Monte Carlo variation of an imperfection parameter is not equivalent to additive measurement noise within a realization.
- **3.8-D37** — Digital active-channel selection must retain stable physical-channel identity/provenance.
- **3.8-D38** — Estimator compatibility is multi-axis and progressive, not one generic Boolean.
- **3.8-D39** — Future compatibility metadata must distinguish linearity, fixed-manifold, simultaneity, narrowband, complex-statistics, quantization, noise-model, source-superposition, and calibration-domain compatibility.
- **3.8-D40** — Classical MUSIC shall not silently accept a profile whose declared sensor/receiver effects violate its governing assumptions.
- **3.8-D41** — The initial Phase-1 profile may instantiate the deterministic sensor-imperfection graph as identity under explicit ideal-sensor assumptions.
- **3.8-D42** — Later bounded profiles should activate imperfection families incrementally so each effect remains independently verifiable.
- **3.8-D43** — The scientific contract constrains future software semantics but does not yet accept a concrete class hierarchy or implementation design.
- **3.8-D44** — ADC acquisition quantization and downstream FPGA/DSP fixed-point arithmetic remain separate operator stages and shall not be double counted.

---

## 24. Immediate next step

The next work session shall start at **Exploration 3.9 — Calibration Models**.

Exploration 3.9 must reconcile at least:

1. parameter calibration versus direct response/manifold calibration;
2. model calibration versus data correction;
3. calibration reference planes and domains;
4. absolute versus relative calibration;
5. gain/phase, delay, coupling, timing/frequency, I/Q, receiver, and aggregate calibration families;
6. invertible versus noninvertible correction models;
7. pseudoinverse/regularized correction and conditioning;
8. calibration experiment design and observability;
9. uncertainty in calibration parameters;
10. residual calibration error and attribution;
11. interpolation/extrapolation across frequency, direction, polarization, temperature, configuration, and time;
12. calibration versioning/provenance and compatibility with estimator/data state.

Do not start Gate A yet.
