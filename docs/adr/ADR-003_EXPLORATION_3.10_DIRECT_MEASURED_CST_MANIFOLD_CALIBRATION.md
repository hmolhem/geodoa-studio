# ADR-003 Exploration 3.10 — Direct Measured / CST-Derived Manifold Calibration

- **Phase:** 0C — Scientific Foundations
- **Status:** EXPLORATION COMPLETE — CANDIDATE CONTRACT, NOT ACCEPTED
- **Parent ADR:** ADR-003 — Sensor Imperfections, Mutual Coupling, and Calibration
- **Branch:** `docs/phase0c-scientific-conventions`
- **Depends on:** ADR-001, ADR-002, ADR-003 Explorations 3.1–3.9
- **Acceptance gates:** Not started

> This is the dedicated exploration record for ADR-003 Section 3.10. It is not an accepted governing ADR. Candidate decisions remain subject to 3.11–3.14 reconciliation, Gates A–F, Golden Reference evidence, boundary/failure analysis, and final acceptance.

---

## 1. Primary question

Exploration 3.9 established parameter calibration, model calibration, data correction, calibration domains, identifiability, reference planes, conditioning, uncertainty, and provenance.

Exploration 3.10 answers:

> How shall GeoDOA use a directly measured or full-wave/CST-derived array response as a calibrated manifold, while preserving coordinate, phase, amplitude, polarization, frequency, range, port, channel, included-effect, interpolation, uncertainty, and provenance semantics?

The governing principle is

\[
\boxed{
\text{A measured or EM-simulated manifold is an aggregate calibrated response model, not automatically physical truth and not automatically decomposable into unique imperfection causes.}
}
\]

Direct manifold calibration is therefore a first-class alternative to parametric imperfection calibration.

---

## 2. Core manifold taxonomy

The taxonomy introduced in 3.1 remains authoritative:

\[
\mathbf a_{\rm nom},\quad
\mathbf a_{\rm phys},\quad
\mathbf a_{\rm meas},\quad
\mathbf a_{\rm em},\quad
\mathbf a_{\rm cal},\quad
\mathbf a_{\rm truth}\ \text{(simulation only when explicitly declared)}.
\]

Their meanings remain distinct.

### 2.1 Measured manifold

\[
\boxed{
\mathbf a_{\rm meas}(\xi,\chi)
}
\]

is an experimental estimate of an array response under declared calibration conditions.

It contains measurement noise, calibration-reference uncertainty, fixture/chamber effects not removed, alignment uncertainty, finite-grid effects, and possible residual systematic errors.

### 2.2 EM/CST-derived manifold

\[
\boxed{
\mathbf a_{\rm em}(\xi,\chi)
}
\]

is the response predicted by a declared electromagnetic simulation setup.

It is conditional on geometry, materials, ports, terminations, excitation/normalization, solver, mesh, boundary conditions, frequency sampling, and other simulation assumptions.

### 2.3 Calibrated processing manifold

\[
\boxed{
\mathbf a_{\rm cal}(\xi,\chi)
}
\]

is the response actually supplied to a downstream estimator.

It may be constructed from measured data, EM data, a hybrid of measured/EM/parametric models, or another accepted calibration model.

GeoDOA shall not silently equate

\[
\mathbf a_{\rm meas}=\mathbf a_{\rm phys}
\]

or

\[
\mathbf a_{\rm em}=\mathbf a_{\rm phys}.
\]

---

## 3. Direct-manifold calibration as an aggregate path

A direct calibrated manifold can bypass an explicit factorization of upstream sensor effects.

Conceptually:

```text
Parametric path
--------------
physical geometry
  -> element response
  -> coupling/loading
  -> receiver response
  -> calibrated model

Direct aggregate path
---------------------
measured or EM response at a declared reference plane
  -> registration / interpolation / allowed downstream stages
  -> calibrated model
```

A direct manifold may already include geometry perturbation, element pattern, polarization sensitivity, mutual coupling, phase-center behavior, radome/platform scattering, feed effects, and possibly receiver effects.

Therefore every direct manifold requires an explicit **included-effects contract**.

---

## 4. Independent variables and manifold domain

A direct manifold is not merely a matrix indexed by angle.

A general response may depend on

\[
\boxed{
\mathbf a
=\mathbf a(
\hat{\mathbf u},
 f,
 r,
 \mathbf p,
 t,
 T,
 \chi,
 \text{channel state},
 \text{hardware state}
).
}
\]

Depending on the profile, relevant variables include:

- azimuth/elevation or a full look-direction vector;
- frequency;
- source range for near-field calibration;
- polarization state/basis;
- orientation/pose;
- temperature;
- time/age;
- gain state;
- sample rate;
- LO/reference state;
- active physical ports;
- termination/load state;
- radome/platform configuration;
- hardware revision.

A stored calibration grid is a finite sampling of this domain, not a claim of continuous exact knowledge.

---

## 5. Canonical manifold dataset concept

A direct calibration dataset shall preserve semantic axes, not rely on unlabeled array dimensions.

A conceptual tensor may have axes such as

```text
response[channel, direction, frequency, polarization, range, state]
```

with only the axes relevant to a specific calibration profile instantiated.

The numerical storage order is not the scientific axis order.

Each axis shall have explicit coordinate values, units, frame/basis semantics, and channel identities.

---

## 6. Coordinate-frame registration

Measured/EM directions must be registered into the accepted GeoDOA coordinate convention from ADR-001.

Let a measurement/simulation frame be \(\mathcal F_M\) and the GeoDOA frame be \(\mathcal F_G\). For a proper rotation

\[
\boxed{
\hat{\mathbf u}_G
=\mathbf R_{GM}\hat{\mathbf u}_M,
\qquad
\mathbf R_{GM}^T\mathbf R_{GM}=\mathbf I,
\quad
\det(\mathbf R_{GM})=+1.
}
\]

A reflection/handedness change is not silently treated as an ordinary rotation; it requires an explicit convention transformation.

The registration artifact shall identify:

- measurement/simulation coordinate axes;
- azimuth/elevation definitions;
- broadside/endfire definitions;
- positive-angle convention;
- handedness;
- array pose;
- transformation into GeoDOA coordinates.

No imported angle column shall be interpreted by column name alone.

---

## 7. Direction parameterization and interpolation coordinate

The calibration dataset may be acquired on an angle grid, but GeoDOA shall preserve the underlying physical look direction.

For the accepted canonical 1-D slice,

\[
\hat{\mathbf u}(\theta)
=\begin{bmatrix}\sin\theta\\\cos\theta\\0\end{bmatrix}.
\]

Interpolation performed in \(\theta\), direction cosine \(u=\sin\theta\), or a full unit-vector coordinate is not mathematically identical.

The interpolation coordinate shall therefore be declared.

GeoDOA shall not silently interpolate through a coordinate singularity, front/back ambiguity, or invalid angular wrap.

---

## 8. Reference origin, phase center, and far-field phase

A complex far-field pattern has phase relative to a declared spatial origin/reference convention.

Changing the common spatial origin used to describe a coherent far-field dataset can introduce a direction-dependent common phase factor. Under the accepted receive-manifold sign convention, a translation of the common response reference by \(\Delta\mathbf r\) produces a phase relation whose sign shall be derived consistently from ADR-001/ADR-002 rather than guessed from a tool export convention.

A common direction-dependent phase factor may not alter a projective steering direction at one grid point, but it matters for:

- phase-coherent interpolation across direction;
- delay/group-delay interpretation across frequency;
- comparison against another manifold with a different origin;
- MIMO Tx/Rx composition;
- any downstream algorithm retaining absolute phase semantics.

GeoDOA shall therefore preserve the declared spatial origin and shall not call arbitrary origin changes harmless in every use case.

---

## 9. Channel identity and port identity

Every manifold component shall map to a stable physical channel/port identity.

The mapping shall preserve at least:

```text
manifold component index
physical sensor/channel ID
EM port ID where applicable
receiver channel ID where applicable
Tx/Rx pair identity for MIMO where applicable
selected/missing/invalid state
```

Sorting channels by coordinate during import shall not silently change physical channel identity.

Missing channels are not represented by fabricated zero responses unless a declared model explicitly requires that representation.

---

## 10. Complex response is required for coherent DOA calibration

A magnitude-only radiation pattern is generally insufficient for coherent array-manifold calibration.

A DOA manifold requires relative complex channel response:

\[
\boxed{
\mathbf a(\xi)
=\begin{bmatrix}
a_1(\xi)&\cdots&a_N(\xi)
\end{bmatrix}^T,
\qquad
a_n\in\mathbb C.
}
\]

Therefore a direct calibration intended for MUSIC or related coherent estimators must preserve channel-relative phase in addition to amplitude.

Power/gain/directivity-only exports do not by themselves define the receive steering manifold.

---

## 11. Coherent phase reference across channels

At each calibration state, channel responses must share a declared coherent phase reference if relative phase is to be interpreted physically.

Examples of acceptable concepts include:

- one coherent multi-channel receiver/reference;
- repeated measurements tied to a stable phase reference;
- calibrated switching with known transfer phase;
- simulation outputs sharing a common phase/excitation convention.

If each channel measurement has an unknown independent phase reset, the resulting vector is not a physically calibrated coherent steering vector until those resets are estimated/removed.

---

## 12. Coherent gauge across calibration grid points

A subtler requirement exists across direction/frequency grid points.

At an individual grid point,

\[
\boxed{
\mathbf a'(\xi_m)
=e^{j\phi_m}\mathbf a(\xi_m)
}
\]

represents the same projective spatial direction for many normalized narrowband DOA uses.

However, if \(\phi_m\) is chosen independently at every grid point, ordinary interpolation need not be invariant:

\[
\mathcal I\{e^{j\phi_m}\mathbf a_m\}
\neq
 e^{j\phi(\xi)}\mathcal I\{\mathbf a_m\}
\]

for a generic interpolation rule.

Therefore GeoDOA shall distinguish:

1. **pointwise projective equivalence** for metrics/estimators that ignore common phase; and
2. **grid-coherent phase gauge** required for physically meaningful interpolation or phase-slope analysis.

Per-angle arbitrary phase normalization shall not be applied silently.

---

## 13. Common complex scale and amplitude normalization

Likewise, at one grid point

\[
\mathbf a'(\xi_m)
=c_m\mathbf a(\xi_m),
\qquad c_m\neq0,
\]

may be projectively equivalent for a normalized pseudospectrum.

But allowing an arbitrary \(|c_m|\) at each direction destroys physically meaningful direction-dependent array sensitivity/gain information.

GeoDOA shall preserve the raw/calibrated amplitude response and may additionally expose a derived normalized manifold view.

A normalization policy shall declare whether it removes:

- common phase only;
- common complex scale;
- Euclidean norm;
- reference-channel response;
- power normalization;
- another declared quantity.

Normalized data shall not destructively replace the unnormalized calibration artifact.

---

## 14. Relative versus absolute manifold calibration

A direct manifold may be calibrated only up to an equivalence class.

### 14.1 Relative manifold

A relative manifold preserves inter-channel ratios/phase but may not define absolute voltage, field strength, power, or RF phase.

### 14.2 Absolute manifold

An absolute manifold requires traceability to a declared physical field/power/voltage and phase/time reference at a declared plane.

GeoDOA shall not infer absolute sensitivity from a normalized chamber/CST pattern without the necessary normalization/reference metadata.

---

## 15. Receive versus transmit manifold semantics

EM software frequently computes transmit radiation quantities. DOA processing uses a receive response.

For a linear reciprocal antenna system, transmit and receive characteristics are related by electromagnetic reciprocity, but the exact mapping depends on:

- temporal phasor convention;
- complex field convention;
- polarization basis;
- port voltage/wave normalization;
- source/load/reference impedance;
- spatial phase origin;
- whether embedded/active patterns are used.

GeoDOA shall therefore not silently import a transmitted far-field vector and label it a receive steering vector.

A transmit-to-receive manifold conversion must be an explicit, convention-checked transformation derived against ADR-001/ADR-002.

---

## 16. Polarization semantics

A direct manifold can be polarization-specific.

Let \(\mathbf E_{\perp}\) be represented in a declared transverse polarization basis. A receive response can depend on source polarization \(\mathbf p\):

\[
\boxed{
\mathbf a(\hat{\mathbf u},f,\mathbf p)
}
\]

or may be represented by multiple basis responses from which arbitrary polarization response is constructed.

The calibration artifact shall preserve:

- polarization basis vectors;
- basis ordering;
- handedness convention for circular polarization;
- field component convention;
- source polarization used during measurement;
- whether cross-polar response is available.

A scalar manifold measured for one polarization shall not be promoted to universal polarization validity.

---

## 17. Frequency-domain manifold

A broadband/wideband direct manifold is frequency dependent:

\[
\boxed{
\mathbf a_{\rm cal}(\xi,f).
}
\]

Frequency metadata shall include physical frequency values/units and the calibration/simulation reference state.

Interpolation of wrapped phase is not generally valid. Delay-like response appears as a phase slope versus frequency, so frequency interpolation must preserve phase continuity or use an equivalent complex/parametric representation.

GeoDOA shall not collapse a multi-frequency manifold to one center-frequency vector without an explicit narrowband approximation.

---

## 18. Range dependence and near-field manifolds

A far-field manifold may depend only on direction under its declared model.

A near-field manifold generally depends on source position/range:

\[
\boxed{
\mathbf a_{\rm NF}(\mathbf r_s,f,\mathbf p,\chi).
}
\]

A far-field measured/CST calibration shall not be used as a near-field calibration merely because the angle matches.

If a near-field chamber measurement is transformed to an equivalent far-field response, the near-field-to-far-field transformation method and reference geometry belong to provenance.

---

## 19. Measured manifold acquisition semantics

A measured manifold calibration shall record the physical acquisition configuration sufficiently to interpret the response.

Relevant information may include:

- chamber/OTA environment;
- calibrator source/antenna identity;
- source-to-array geometry;
- far-field/near-field regime;
- positioning system and angle convention;
- polarization;
- transmitted waveform/frequency;
- source power/reference stability;
- receiver chain and gain state;
- coherent phase reference architecture;
- cables/switches/fixtures;
- temperature/environment;
- channel acquisition order;
- repetition/averaging protocol;
- background/noise measurement;
- de-embedding applied;
- calibration date/state.

A chamber dataset is evidence, not automatically a noise-free manifold.

---

## 20. Measurement uncertainty and repeated acquisition

If repeated coherent manifold estimates are available at state \(\xi_m\), GeoDOA may represent

\[
\boxed{
\hat{\mathbf a}_m
=\frac{1}{K}\sum_{k=1}^{K}\mathbf a_m^{(k)}
}
\]

and a sample covariance/uncertainty statistic of the repeated response estimates.

Measurement variation and systematic reference uncertainty remain distinct.

A small repeatability variance does not prove small absolute calibration bias.

---

## 21. CST/EM manifold provenance

A CST/full-wave-derived manifold shall preserve enough simulation provenance to establish what response was actually computed.

At minimum, future artifacts shall be able to identify:

```text
EM tool / version
project/model identity or immutable content hash
solver type
simulation frequency/frequency grid
geometry revision
material models
boundary conditions
environment/platform/radome state
mesh / refinement / convergence evidence reference
port definitions and numbering
reference impedance / port normalization
port termination/loading state
excitation definition
far-field monitor/output definition
field component/polarization basis
coordinate system and origin
normalization quantity
de-embedding/reference-plane settings
post-processing steps
export script/version
```

This is scientific provenance; the exact serialization format is deferred.

---

## 22. Isolated, embedded, active, and full-array responses

The following EM response concepts are not interchangeable.

### 22.1 Isolated element pattern

Pattern of an element modeled/measured outside the final coupled array environment.

### 22.2 Embedded element pattern

Response associated with one element/port embedded in the finite array under declared termination/loading of the other ports.

Embedded response can contain mutual-coupling and finite-array/environment effects.

### 22.3 Active element pattern

Response under a declared simultaneous array excitation/scan condition. It depends on excitation weights and coupling environment.

### 22.4 Full-array aggregate response

Response of the complete multiport/array system under a declared excitation or receive condition.

GeoDOA shall preserve which response family a CST export represents.

An `element_pattern` field shall not accept these meanings without an explicit subtype.

---

## 23. Embedded-pattern termination semantics

An embedded element response depends on the electrical state of non-driven/non-observed ports.

Therefore the manifold artifact shall preserve termination/load conditions such as the relevant reference impedances or connected network state.

Changing physical loads can change embedded patterns and coupling even when geometry is unchanged.

A calibration derived under one termination state is not universally valid for another state.

---

## 24. Mutual coupling and double-count prevention

Suppose an EM/measurement manifold already includes coupling:

\[
\boxed{
\mathbf a_{\rm aggregate}
=\mathbf C\mathbf a_{\rm uncoupled}
}
\]

under some valid linear specialization.

Applying an explicit coupling matrix again gives

\[
\boxed{
\mathbf C\mathbf a_{\rm aggregate}
=\mathbf C^2\mathbf a_{\rm uncoupled},
}
\]

which is generally wrong.

Therefore imported direct manifolds require included-effects metadata such as:

```text
geometry phase/path effects
isolated/embedded element response
mutual coupling/loading
feed network
radome/platform scattering
receiver electronics
cables/fixtures
ADC/digital chain
```

An explicit downstream block may be applied only if its reference plane and included-effects record prove it is not already present.

---

## 25. Deterministic double-counting check

Reuse the 3.5 coupling example

\[
\mathbf a
=\begin{bmatrix}1\\-j\end{bmatrix},
\qquad
\mathbf C
=\begin{bmatrix}1&0.5\\0.5&1\end{bmatrix}.
\]

The coupled manifold is

\[
\boxed{
\mathbf b
=\mathbf C\mathbf a
=\begin{bmatrix}1-0.5j\\0.5-j\end{bmatrix}.
}
\]

If \(\mathbf b\) is imported as a direct aggregate coupled manifold and coupling is mistakenly applied again,

\[
\boxed{
\mathbf C\mathbf b
=\begin{bmatrix}1.25-j\\1-1.25j\end{bmatrix}
\neq\mathbf b.
}
\]

Thus double counting is not a documentation issue; it changes the scientific response.

This is an exploration check, not a new formal GRP number.

---

## 26. De-embedding

A measured/EM response may be de-embedded from one reference plane to another.

Let

\[
\mathcal D_{b\rightarrow a}
\]

be a declared de-embedding transformation from plane \(b\) to plane \(a\). Then

\[
\boxed{
\mathbf a^{(a)}
=\mathcal D_{b\rightarrow a}[\mathbf a^{(b)}].
}
\]

De-embedding shall record:

- source/reference plane;
- destination plane;
- network/model used;
- frequency dependence;
- normalization/reference impedance;
- uncertainty;
- whether the operation is exact, estimated, regularized, or approximate.

A label such as `antenna-only` is insufficient without a plane/effect definition.

---

## 27. Hybrid measured/EM/parametric calibration

GeoDOA shall support a hybrid composition when scientifically valid.

Example:

```text
CST aggregate antenna/array manifold
    includes geometry + element + coupling + radome
        ↓
measured receiver gain/delay calibration
        ↓
calibrated processing manifold at digital baseband plane
```

Another valid profile could use measured OTA manifold and no explicit upstream parametric array model at all.

Hybrid composition is governed by the 3.8 reference-plane/type rules and 3.9 calibration-domain/provenance rules.

---

## 28. Interpolation is part of the calibrated model

Measurements/simulations occur at finite grid points

\[
\{\xi_m\}_{m=1}^{M},
\qquad
\mathbf a_m=\mathbf a(\xi_m).
\]

Operation usually requires response at off-grid \(\xi\):

\[
\boxed{
\hat{\mathbf a}(\xi)
=\mathcal I_{\rm manifold}
\left(\xi;\{\xi_m,\mathbf a_m\}\right).
}
\]

The interpolation method is therefore part of the calibrated manifold definition, not a display/UI convenience.

Possible future approaches include:

- interpolation of complex components under a coherent gauge;
- magnitude plus unwrapped phase interpolation;
- local polynomial/spline interpolation;
- Fourier/manifold-separation representations;
- parametric-plus-residual interpolation;
- other validated basis/surrogate methods.

No method is accepted universally in Phase 0C.

---

## 29. Phase wrapping and interpolation

For phase \(\phi\), values differing by \(2\pi m\) represent the same complex phasor at a point but not the same raw numerical phase trajectory.

Interpolating wrapped phase directly can create artificial discontinuities.

GeoDOA shall either:

- interpolate complex response directly under suitable sampling/gauge conditions;
- unwrap phase using a declared algorithm/reference;
- or use another representation that avoids ambiguous wrapped-phase interpolation.

Phase unwrapping is itself a processing decision with failure modes near nulls/noisy samples.

---

## 30. Interpolation near response nulls

When \(|a_n(\xi)|\) approaches zero, phase becomes poorly defined/noise sensitive.

Therefore magnitude-phase interpolation can become unstable near element/array nulls.

The calibration system shall not assume that every sample has a meaningful high-confidence phase simply because a complex number is stored.

Null/low-SNR regions require quality/confidence diagnostics and may need alternative interpolation representations.

---

## 31. Grid density and spatial bandwidth

A calibration grid that is too coarse can miss rapid direction/frequency variation caused by aperture phase progression, coupling, pattern nulls, platform scattering, or resonances.

Grid adequacy is therefore a model-validation question.

GeoDOA shall preserve grid spacing and shall eventually evaluate interpolation error on held-out or independently sampled states.

A dense theoretical MUSIC scan grid cannot recover manifold information that was never captured by the calibration grid/model.

---

## 32. Extrapolation policy

A direct manifold shall have an explicit calibrated domain.

Outside that domain, GeoDOA shall not silently use nearest-neighbor or unconstrained interpolation as if it were calibrated response.

The permitted behaviors are:

1. reject as out-of-domain;
2. allow explicitly with warning/status and marked extrapolation;
3. use a separately validated parametric extrapolation model.

This applies to angle, frequency, range, polarization, temperature, and hardware state.

---

## 33. Cross-validation of interpolation

A defensible interpolation assessment separates fit/calibration points from check points.

For held-out states \(\xi_h\), define a response prediction error such as

\[
\boxed{
\mathbf e_h
=\mathbf a_{\rm observed}(\xi_h)
-\hat{\mathbf a}_{\rm interp}(\xi_h),
}
\]

with alignment/equivalence semantics from 3.11.

Interpolation error shall not be estimated only from the same points used exactly by the interpolant when that construction forces zero residual at those nodes.

---

## 34. Noise/uncertainty-aware manifold interpolation

If calibration points have unequal uncertainty, an interpolation/fitting method may use confidence weights rather than treating all nodes equally.

GeoDOA shall preserve per-node quality indicators where available.

A smoothed calibration model may intentionally trade node-by-node fit against noise suppression. That model shall not be labeled as the raw measured manifold.

---

## 35. Registration between measured and nominal array models

Comparing \(\mathbf a_{\rm meas}\) with \(\mathbf a_{\rm nom}\) requires common:

- physical channel identity;
- direction coordinate/frame;
- frequency;
- polarization;
- spatial origin/reference;
- phase convention;
- reference plane;
- normalization/equivalence class.

Only after registration can a manifold mismatch be interpreted.

An apparent phase slope may be coordinate/origin misregistration rather than physical sensor error.

---

## 36. Projective comparison metrics versus physical comparison

For some DOA purposes, two manifold vectors are equivalent up to common complex scale.

A projective residual may be based on

\[
\boxed{
\min_{c\in\mathbb C}
\|\mathbf a_2-c\mathbf a_1\|_2.
}
\]

A phase-only alignment instead uses

\[
\boxed{
\min_{\phi}
\|\mathbf a_2-e^{j\phi}\mathbf a_1\|_2.
}
\]

These answer different questions and neither replaces a physically absolute amplitude/phase comparison when absolute calibration is intended.

Formal metrics are deferred to 3.11.

---

## 37. Direct calibrated manifold in MUSIC

For a calibrated response \(\mathbf a_{\rm cal}(\xi)\) compatible with the data reference plane, a classical MUSIC pseudospectrum may use

\[
\boxed{
P_{\rm MUSIC}(\xi)
=\frac{1}
{\mathbf a_{\rm cal}^H(\xi)
\mathbf E_n\mathbf E_n^H
\mathbf a_{\rm cal}(\xi)}
}
\]

or a normalized variant under a declared normalization policy.

The key contract is not that `measured` is better than `nominal` by definition. The estimator manifold must match the physical response represented in the data within the estimator's assumptions.

If data have been corrected to another reference plane, the manifold used by MUSIC must correspond to that corrected plane.

---

## 38. Measured-manifold uncertainty in subspace estimators

The standard MUSIC expression treats \(\mathbf a_{\rm cal}\) as a deterministic model input.

In reality, a measured/interpolated manifold has uncertainty.

GeoDOA shall preserve this distinction so later robust/uncertainty-aware estimators can distinguish

\[
\boxed{
\hat{\mathbf a}_{\rm cal}
}
\]

from

\[
\boxed{
\mathbf a_{\rm phys}.
}
\]

Ordinary MUSIC may initially use the point estimate, but the calibration artifact shall not discard available uncertainty information.

---

## 39. Parametric versus direct manifold calibration

Neither strategy universally dominates.

### Parametric calibration

Advantages:

- physical interpretability;
- compact parameter representation;
- potential extrapolation when physics is valid;
- direct link to manufacturing/receiver causes.

Risks:

- model-form error;
- identifiability/confounding;
- omitted physics;
- incorrect operator ordering.

### Direct manifold calibration

Advantages:

- can absorb complicated aggregate physics;
- does not require unique decomposition into causes;
- can naturally include embedded element/coupling/platform effects.

Risks:

- large multidimensional data requirements;
- finite-grid/interpolation error;
- measurement/simulation bias;
- poor extrapolation;
- difficult physical attribution;
- strong provenance/reference-plane requirements.

### Hybrid calibration

A hybrid can combine physically meaningful parametric structure with measured/EM residual or aggregate blocks.

GeoDOA shall support scientific comparison among these families rather than declaring one universally preferred.

---

## 40. CST-derived manifold is not automatically validated measurement

EM simulation can provide highly useful array responses, but it remains a numerical model.

A CST-derived manifold may differ from hardware because of:

- geometry/manufacturing tolerances;
- unknown material properties;
- connector/cable/feed details;
- platform/environment differences;
- mesh/discretization error;
- solver/convergence limitations;
- inaccurate port/load models;
- temperature/state mismatch;
- missing receiver electronics;
- chamber/hardware effects absent from simulation.

Therefore GeoDOA shall label it `EM-simulated` or `CST-derived`, not `measured truth`.

Comparison with independent measurement belongs to validation evidence, not semantic relabeling.

---

## 41. Full-wave inclusion of coupling and finite-array effects

CST and other full-wave tools can model finite arrays in which neighboring elements, edge effects, platform structures, radomes, and coupling modify response relative to isolated-element pattern multiplication.

This is precisely why direct EM manifolds are useful.

The same benefit creates the double-counting risk: once the full-wave response includes these effects, downstream parametric blocks for the same physics shall not be applied again unless the data have been explicitly de-embedded to a plane where those blocks are absent.

---

## 42. Active element patterns versus receive-source manifold

An active element pattern under one beamforming excitation is not automatically the receive manifold for arbitrary DOA estimation.

It depends on the declared excitation vector and network state.

GeoDOA shall distinguish:

- basis/embedded port responses that can be combined into another response under linear assumptions;
- scan-specific active patterns;
- aggregate full-array beam patterns;
- receive manifold vectors indexed by incident source state.

A beam pattern and an array steering manifold are related but not interchangeable scientific objects.

---

## 43. MIMO direct manifold calibration

For MIMO systems, direct calibration may be indexed by physical Tx/Rx pair:

\[
\boxed{
\mathbf a_{\rm virt}(\xi)
=\{a_{ij}(\xi)\}_{(i,j)}.
}
\]

GeoDOA shall preserve \((\mathrm{Tx}_i,\mathrm{Rx}_j)\) provenance.

A direct virtual-channel manifold may include Tx pattern, Rx pattern, Tx/Rx electronics, waveform timing, TDM phase evolution, and propagation effects depending on the calibration setup.

It shall not be forced into an ideal virtual-position model unless that factorization has been justified.

---

## 44. Frequency and TDM state in MIMO calibration

For TDM-MIMO or stepped-frequency operation, virtual channels may not correspond to one simultaneous physical epoch.

A direct manifold calibration must therefore state whether timing/LO phase evolution has been included, removed, or separately corrected.

A spatial calibration measured with simultaneous excitation cannot automatically calibrate a TDM acquisition chain whose differential temporal phase is not included.

---

## 45. Calibration artifact immutability and derived views

The raw imported measurement/EM dataset shall remain distinguishable from derived transformations such as:

```text
raw imported response
registered-coordinate response
phase-gauge-aligned response
normalized response
interpolated/surrogate model
de-embedded response
channel-selected response
final calibrated estimator manifold
```

Derived products shall reference their parent artifact and transformation provenance.

A convenient normalized/interpolated array shall not overwrite the source calibration evidence.

---

## 46. Data integrity and import validation

An import path shall eventually validate at least:

- finite numerical values;
- expected channel count/IDs;
- unique axis coordinates where required;
- monotonicity/order metadata where relevant;
- units;
- coordinate-frame declaration;
- frequency consistency;
- polarization/basis declaration;
- shape/axis labels;
- duplicate states;
- missing states;
- normalization/reference-plane metadata;
- provenance identity.

Scientific import failure shall be explicit rather than silently reshaping/transposing data until dimensions happen to fit.

---

## 47. Deterministic coordinate-registration check

Let the measurement frame be rotated by \(+90^\circ\) about \(+z\) relative to the GeoDOA frame, with

\[
\mathbf R_{GM}
=\begin{bmatrix}
0&-1&0\\
1&0&0\\
0&0&1
\end{bmatrix}.
\]

For

\[
\hat{\mathbf u}_M
=\begin{bmatrix}1\\0\\0\end{bmatrix},
\]

the registered direction is

\[
\boxed{
\hat{\mathbf u}_G
=\begin{bmatrix}0\\1\\0\end{bmatrix}.
}
\]

Interpreting the original coordinate triplet directly in GeoDOA would assign the wrong physical look direction.

This is an exploration check, not a formal GRP number.

---

## 48. Deterministic phase-gauge interpolation check

Suppose two calibration nodes contain projectively equivalent responses

\[
\mathbf a_0
=\begin{bmatrix}1\\1\end{bmatrix},
\qquad
\mathbf a_1
=\begin{bmatrix}1\\-j\end{bmatrix}.
\]

Now replace the second node by an arbitrary common-phase-equivalent vector

\[
\mathbf a_1'=-\mathbf a_1.
\]

At the node itself, \(\mathbf a_1\) and \(\mathbf a_1'\) define the same projective manifold direction.

But simple midpoint interpolation gives

\[
\frac{\mathbf a_0+\mathbf a_1}{2}
\neq
c\frac{\mathbf a_0+\mathbf a_1'}{2}
\]

for any generic common scalar \(c\).

Therefore arbitrary independent common-phase choices at calibration nodes can change the interpolated manifold even when every stored node is individually projectively equivalent.

A coherent interpolation gauge is required.

---

## 49. Initial Phase-1 profile implication

The initial Phase-1 validated profile may continue to use the ideal nominal manifold from ADR-001/ADR-002 and therefore requires no measured/CST direct calibration.

However, the scientific contract established here allows a later bounded profile such as:

```text
far-field narrowband 1-D array
fixed frequency
one declared polarization
CST-derived finite-array complex manifold
registered to GeoDOA coordinates
included coupling + embedded element response
no receiver electronics included
complex interpolation inside calibrated visible sector
classic MUSIC using matching manifold
```

Such a profile must be introduced as a new bounded validated capability, not as a silent replacement of the ideal baseline.

---

## 50. Software-semantic implications

Phase 0C does not accept a concrete storage/API implementation, but the scientific contract implies future support for:

- typed manifold source: nominal / measured / EM / hybrid;
- explicit labeled axes;
- stable channel/port identities;
- coordinate frame and registration transform;
- complex response values;
- polarization basis;
- reference plane/origin;
- normalization/gauge semantics;
- included-effects/de-embedding record;
- interpolation model identity;
- calibrated-domain bounds;
- uncertainty/quality fields;
- parent/derived artifact lineage;
- tool/project/hardware provenance;
- compatibility status with estimator/data reference plane.

One opaque `calibration.npy` file without metadata cannot satisfy the scientific contract.

---

## 51. Boundary and failure conditions reserved for later gates

Direct manifold calibration must later be stress-tested for at least:

- wrong coordinate-frame registration;
- left/right-handed convention mismatch;
- look-direction versus propagation-direction mismatch;
- wrong temporal phasor/phase sign;
- transmit far-field imported as receive manifold without conversion;
- unknown common phase resets across channels;
- arbitrary per-grid phase gauges that corrupt interpolation;
- destructive normalization of direction-dependent sensitivity;
- magnitude-only pattern imports;
- polarization basis mismatch;
- phase ambiguity near response nulls;
- insufficient angular/frequency grid density;
- wrapped-phase interpolation failures;
- interpolation outside convex/local calibrated support;
- extrapolation outside domain;
- far-field data used for near-field source state;
- wrong channel/port ordering;
- missing or disabled channels;
- physical port-state mismatch;
- embedded/active/isolated pattern confusion;
- wrong termination/reference impedance;
- coupling double counting;
- radome/platform double counting;
- wrong de-embedding plane;
- solver/mesh/convergence insufficiency;
- measurement multipath/chamber contamination;
- reference-source position/orientation error;
- untracked hardware/gain/temperature drift;
- MIMO Tx/Rx provenance loss;
- TDM timing phase omitted from calibration;
- calibration/validation data leakage.

These are exploration requirements, not Gate F PASS evidence.

---

## 52. Candidate decisions from Exploration 3.10

- **3.10-D1** — Measured, EM/CST-derived, physical, nominal, and calibrated manifolds remain distinct scientific objects.
- **3.10-D2** — A direct measured/EM manifold is an aggregate calibrated response model, not automatically physical truth.
- **3.10-D3** — Direct manifold calibration is a first-class alternative to parametric imperfection calibration.
- **3.10-D4** — A direct manifold may bypass explicit upstream factorization only at a declared reference plane and with included-effects provenance.
- **3.10-D5** — Manifold domain variables may include direction, frequency, range, polarization, time, temperature, hardware/gain/port state, and other declared conditions.
- **3.10-D6** — Stored numerical dimensions require labeled semantic axes; memory order is not scientific axis meaning.
- **3.10-D7** — Imported directions must be registered from the source measurement/simulation frame into the accepted GeoDOA coordinate frame.
- **3.10-D8** — Handedness/reflection changes require explicit convention handling and are not silently treated as ordinary rotations.
- **3.10-D9** — The interpolation coordinate (angle, direction cosine, unit vector, etc.) shall be declared.
- **3.10-D10** — Spatial origin/phase-center/reference conventions shall be preserved because common direction-dependent phase may matter across grid/frequency/use cases.
- **3.10-D11** — Stable physical channel/port identity shall be preserved through import, registration, selection, and interpolation.
- **3.10-D12** — Magnitude-only radiation data are insufficient by default for coherent DOA manifold calibration.
- **3.10-D13** — Channel-relative complex phase requires a coherent measurement/simulation reference.
- **3.10-D14** — Pointwise common-phase equivalence does not imply arbitrary per-grid phase gauges are safe for interpolation.
- **3.10-D15** — A phase-coherent gauge across calibration nodes is required for interpolation/phase-slope uses that are not gauge invariant.
- **3.10-D16** — Common complex-scale normalization may be a derived view but shall not destructively replace physical amplitude response.
- **3.10-D17** — Relative and absolute manifold calibration are distinct; normalized patterns shall not be promoted to absolute sensitivity without a physical reference.
- **3.10-D18** — Transmit EM far fields shall not be silently relabeled as receive steering manifolds; reciprocity/convention conversion must be explicit.
- **3.10-D19** — Polarization basis, handedness, and source polarization are part of manifold semantics.
- **3.10-D20** — A scalar manifold calibrated for one polarization is not universally valid for arbitrary polarization.
- **3.10-D21** — Wideband direct calibration preserves frequency-dependent manifold response rather than silently collapsing to center frequency.
- **3.10-D22** — Wrapped-phase interpolation is not accepted by default; phase continuity/representation must be declared.
- **3.10-D23** — Near-field direct manifolds are source-position/range dependent and distinct from far-field directional manifolds.
- **3.10-D24** — Near-field-to-far-field transformed measurement requires transformation/reference provenance.
- **3.10-D25** — Measured manifold acquisition shall preserve source, geometry, polarization, receiver, coherent-reference, fixture, environment, and de-embedding provenance.
- **3.10-D26** — Repeatability uncertainty and systematic calibration bias are distinct.
- **3.10-D27** — CST/EM manifold artifacts shall preserve tool/model/solver/mesh/port/excitation/reference/field/export provenance sufficient to interpret the response.
- **3.10-D28** — Isolated element, embedded element, active element, and full-array aggregate responses are distinct meanings.
- **3.10-D29** — Embedded response validity depends on non-driven port termination/loading state.
- **3.10-D30** — Included-effects provenance is mandatory to prevent mutual-coupling, element-pattern, radome/platform, feed, or receiver double counting.
- **3.10-D31** — Applying explicit coupling to an aggregate manifold that already includes coupling is scientifically invalid unless prior de-embedding removed that effect.
- **3.10-D32** — De-embedding must declare source/destination reference planes, network/model, frequency dependence, normalization, and uncertainty.
- **3.10-D33** — Hybrid measured/EM/parametric calibration is permitted only through compatible typed reference-plane composition.
- **3.10-D34** — Manifold interpolation is part of the calibrated scientific model, not a UI/display operation.
- **3.10-D35** — No one interpolation method is universally accepted at Phase 0C; its representation, gauge, grid, and validation domain must be explicit.
- **3.10-D36** — Phase interpolation near response nulls requires special quality handling because phase is poorly conditioned there.
- **3.10-D37** — Calibration-grid density limits recoverable manifold detail; a denser estimator scan grid cannot create missing calibration information.
- **3.10-D38** — Extrapolation outside direct-manifold calibration domain shall never occur silently.
- **3.10-D39** — Interpolation accuracy should be evaluated on held-out/independent states where feasible rather than inferred only from interpolation nodes.
- **3.10-D40** — Unequal manifold-node uncertainty may be retained and used by later weighted/smoothed calibration models.
- **3.10-D41** — Registration is required before interpreting measured-versus-nominal manifold mismatch.
- **3.10-D42** — Projective, phase-only, and physically absolute manifold comparisons are distinct and are formalized in 3.11.
- **3.10-D43** — MUSIC may directly use a calibrated measured/EM manifold only when its reference plane/state is compatible with the data covariance.
- **3.10-D44** — Measured/interpolated manifold uncertainty shall not be discarded merely because an estimator currently consumes a deterministic point estimate.
- **3.10-D45** — Parametric, direct, and hybrid calibration each have distinct strengths/failure modes; none is universally preferred.
- **3.10-D46** — CST/full-wave response remains a simulation prediction and shall not be semantically promoted to measured physical truth.
- **3.10-D47** — Full-wave modeling can legitimately include coupling/finite-array/platform effects; this strengthens the need for double-count prevention.
- **3.10-D48** — Scan-specific active beam patterns, embedded port responses, full-array patterns, and receive-source manifolds are not interchangeable.
- **3.10-D49** — Direct MIMO calibration shall preserve physical Tx/Rx pair provenance and shall not force an ideal virtual-array factorization without evidence.
- **3.10-D50** — MIMO/TDM manifold calibration must declare timing/LO phase evolution included, removed, or separately corrected.
- **3.10-D51** — Raw imported manifold evidence shall remain immutable/distinguishable from registered, normalized, interpolated, de-embedded, selected, or estimator-ready derived views.
- **3.10-D52** — Import validation must reject ambiguous axes/units/channel mapping rather than silently reshape or reorder until dimensions fit.
- **3.10-D53** — A later bounded CST-derived manifold profile may be added without replacing the ideal Phase-1 baseline.
- **3.10-D54** — An opaque calibration array without semantic/provenance metadata is insufficient for GeoDOA scientific use.

---

## 53. Scientific anchors for this exploration

The contract is consistent with established array-processing and EM practice in which practical DOA arrays are calibrated from finite measured response grids and require interpolation, while embedded/active element patterns capture coupling-dependent array behavior under declared loading/excitation states.

Representative scientific anchors include:

- A. J. Weiss and B. Friedlander, **Array manifold interpolation for diversely polarized arrays**, Asilomar Conference, 1992 — measured finite-direction manifolds and interpolation for DOA/polarization estimation.
- F. Belloni, A. Richter, and V. Koivunen, **DoA Estimation Via Manifold Separation for Arbitrary Array Structures**, IEEE Transactions on Signal Processing, 2007 — manifold-separation representation and calibration-noise implications.
- B. Yang, T. McKelvey, and M. Viberg, **Array Calibration using Array Response Interpolation and Parametric Modeling**, EUSIPCO 2015 — interpolation combined with parametric array modeling.
- **Array response interpolation and DOA estimation with array response decomposition**, Signal Processing, vol. 125, 2016 — measured/simulated response interpolation with coupling/correction decomposition.
- SIMULIA/CST antenna-array documentation and technical material — full-array/finite-array simulation, active-element patterns, mutual-coupling-aware array analysis, far-field and S-parameter outputs.

These sources support the scientific taxonomy; GeoDOA's exact import, reference-plane, gauge, and provenance contracts remain project decisions subject to Gates A–F.

---

## 54. Immediate next step

The next work session shall start at **Exploration 3.11 — Error Metrics and Identifiability**.

Exploration 3.11 must reconcile at least:

1. parameter error versus manifold error versus operator error;
2. raw Euclidean manifold error;
3. phase-only aligned error;
4. common-complex-scale/projective error;
5. normalized inner product / coherence / principal-angle metrics;
6. amplitude and phase residual metrics;
7. position/gain/delay/coupling parameter metrics;
8. calibration fit residual versus held-out prediction error;
9. uncertainty/confidence reporting;
10. identifiability versus numerical conditioning;
11. local Jacobian/Fisher-information concepts where appropriate;
12. observable equivalence classes / gauge freedoms;
13. source-dependent identifiability;
14. frequency/direction aggregated metrics;
15. metric weighting and domain integration;
16. thresholds and engineering interpretation;
17. linkage from manifold mismatch metrics to covariance/eigenspace analysis in 3.12.

Do not start Gate A yet.
