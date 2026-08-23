# ADR-001 — Coordinate, Direction, and Spatial Conventions

- **Status:** Accepted — all Phase 0C acceptance Gates A–F passed
- **Phase:** 0C — Scientific Foundations
- **Scope:** Coordinate, direction, spatial-phase, unit, reference, and lattice conventions
- **Depends on:** `GEODOA_STUDIO_MASTER_START_HANDOFF.md`, `PHASE0C_SCIENTIFIC_CONTRACTS_ROADMAP.md`
- **Acceptance audit:** `ADR-001_ACCEPTANCE_AUDIT.md`
- **Golden reference evidence:** `../science/golden_reference/ADR-001_GOLDEN_REFERENCE_PROBLEMS.md`
- **Boundary/failure evidence:** `ADR-001_BOUNDARY_FAILURE_ANALYSIS.md`
- **Supersedes:** None
- **Superseded by:** None

## 1. Decision Summary

GeoDOA Studio shall treat array-geometry dimension, propagation-space dimension, and identifiable directional dimension as distinct concepts.

The initial physical array scope is one-dimensional: nominal sensor phase centers lie on the local `+x` array axis. The scientific direction model is nevertheless embedded in three-dimensional Euclidean space. For an ideal scalar 1-D array, the geometry-only receive manifold observes only the projection of the source look direction onto the array axis.

The canonical geometry-only receive manifold is derived from propagation delay using the temporal phasor convention `exp(-j omega t)`. For a look-direction unit vector `u_hat`, a propagation speed `v_p`, frequency `f`, wavenumber `k = 2 pi f / v_p`, declared nominal sensor phase-center/reference position `r_n`, and explicit spatial phase-reference point `r_ref`, the nominal receive coefficient is

```math
a_n(\hat{\mathbf u}, f)
=
\exp\!\left[
-j k
(\mathbf r_n-\mathbf r_{\mathrm{ref}})^T
\hat{\mathbf u}
\right].
```

For the canonical 2-D `xy` slice,

```math
\hat{\mathbf u}(\theta)
=
\begin{bmatrix}
\sin\theta\\
\cos\theta\\
0
\end{bmatrix},
\qquad
\theta\in[-\pi/2,\pi/2],
```

so that

```math
a_n(\theta,f)
=
\exp\!\left[
-j k (x_n-x_{\mathrm{ref}})\sin\theta
\right].
```

`theta = 0` is the canonical broadside reference direction `+y` within the `xy` slice; `theta > 0` rotates toward `+x`; `theta = +pi/2` is `+x` endfire and `theta = -pi/2` is `-x` endfire.

Physical coordinates and channel identity are preserved. Sorting, translation normalization, wavelength normalization, primitive-lattice reduction, and reflection comparison are derived views or analyses and shall not destructively replace the physical representation.

Canonical physical units are SI. Physical positions are stored in meters; wavelength-normalized positions are frequency-referenced derived quantities. Integer coarray lag indices are valid only after an explicit lattice has been declared or validated within an explicit numerical tolerance. Arbitrary real-valued position differences shall never be converted into integer lags by blind rounding.

For nearest-integer lattice validation, the admissible numerical tolerance domain is

```math
0\le\tau_{\mathrm{lat}}<\frac12.
```

This bound guarantees that the accepted tolerance does not include the half-grid tie where the nearest integer ceases to be unique. It does not prescribe the eventual default numerical tolerance.

## 2. Context and Decision Drivers

All later steering-vector, manifold, coarray, beamforming, MUSIC, MIMO, calibration, PCA/subspace, fixed-point, and FPGA/SoC work depends on a consistent answer to the following questions:

- What is the array axis?
- What does a positive angle mean?
- Is an angle measured from broadside or endfire?
- Does a direction vector point from the array to the source or in the wave-propagation direction?
- Which temporal phasor convention is used?
- What phase sign follows from that convention?
- What spatial quantity does a 1-D array physically observe?
- Which changes to coordinates are physical changes and which are only coordinate transformations?
- Which sensor/channel ordering is authoritative?
- When is an integer coarray lag mathematically meaningful?
- Which quantities are stored physically and which are normalized derived views?

An implicit or inconsistent answer to any of these questions can produce mirrored DOA estimates, incompatible steering vectors, incorrect coarray construction, invalid calibration association, non-reproducible plots, or silent hardware/software disagreement.

## 3. Scope

ADR-001 governs:

- local coordinate-frame semantics for the initial 1-D array scope;
- the distinction between 1-D geometry and 3-D propagation space;
- look direction and propagation direction;
- broadside, endfire, positive-angle, visible-sector, and canonical-slice conventions;
- the temporal phasor convention relevant to receive spatial phase;
- derivation and sign of the geometry-only receive manifold;
- phase-reference semantics and translation invariance;
- channel identity, physical coordinate preservation, sorting, and derived canonical views;
- canonical units and wavelength-normalized representations;
- lattice declaration, validation, tolerance, primitive reduction, and coarray integer-lag semantics;
- direction cosine, projected spatial angular frequency, and normalized lattice spatial frequency;
- projection ambiguity, front/back ambiguity, and spatial aliasing as distinct phenomena;
- angle-grid versus direction-cosine/spatial-frequency-grid semantics.

## 4. Explicit Non-Goals

The following are deliberately not defined in full by ADR-001:

- far-field versus near-field validity criteria;
- spherical-wave, wideband, FMCW, stepped-frequency, pulse, and moving-source models;
- propagation-medium implementation details beyond the propagation speed used in the spatial-phase relation;
- element patterns, polarization, mutual coupling, gain/phase mismatch, channel delay, clock skew, quantization, or calibration;
- covariance-estimator semantics, PCA, MUSIC implementation, model-order estimation, or peak detection;
- validation hierarchy, Monte Carlo policy, or statistical performance metrics.

These belong respectively to ADR-002, ADR-003, ADR-004, and supporting scientific contract notes.

## 5. Core Terminology

### 5.1 Declared nominal sensor phase-center/reference position

`r_n` denotes the **declared nominal sensor phase-center/reference position** associated with channel `n` in the geometry model and active coordinate frame. It is the position used by the nominal geometry-only spatial-phase model.

This definition does not claim that a real electromagnetic or acoustic element has one immutable physical phase center under all frequencies, arrival directions, loading states, platform configurations, or environmental conditions. Frequency-, angle-, environment-, installation-, or calibration-dependent departures from the nominal reference position or nominal manifold belong to ADR-003.

A sensor identity and its declared nominal position are related but distinct pieces of information.

### 5.2 Array-geometry dimension

The initial GeoDOA geometry is 1-D: nominal phase centers lie on one spatial axis. This does not imply that the physical propagation space is 1-D.

### 5.3 Propagation-space dimension

The direction model is embedded in 3-D Euclidean space. A source look direction is represented by a unit vector

```math
\hat{\mathbf u}
=
\begin{bmatrix}
u_x\\u_y\\u_z
\end{bmatrix},
\qquad
\|\hat{\mathbf u}\|_2=1.
```

### 5.4 Identifiable directional dimension

An ideal scalar linear array on the `x` axis observes only `u_x`. Therefore a 1-D array may model 3-D propagation while identifying only one directional degree of freedom unless additional non-collinear geometry or physical information is supplied.

## 6. Canonical Coordinate Frame

### 6.1 Local array frame

The initial canonical local frame is right-handed. The linear-array axis is `+x`. Because a purely 1-D geometry does not physically determine rotation about its own axis, GeoDOA **chooses** `+y` as the canonical reference broadside axis. The `+z` axis completes the right-handed frame, so that

```math
\hat{\mathbf z}
=
\hat{\mathbf x}\times\hat{\mathbf y}.
```

For an ideal 1-D geometry,

```math
\mathbf r_n
=
\begin{bmatrix}
x_n\\0\\0
\end{bmatrix}.
```

The `+y` reference is therefore a project coordinate convention, not a direction inferred uniquely from the 1-D sensor positions themselves.

The choice of a local array frame does not destroy or replace externally measured global or platform coordinates. Any global-to-local or platform-to-local transform must be explicit and provenance-preserving.

### 6.2 Intrinsic 1-D coordinate versus embedded 3-D position

For the initial software domain, a linear geometry has one intrinsic physical coordinate per channel,

```math
x_n\in\mathbb R,
```

expressed in meters along the declared array axis. A `ReferenceFrame1D`-type domain concept supplies the spatial embedding needed by propagation/manifold code. In the canonical frame,

```math
\mathbf r_n
=
\mathbf r_{\mathrm{origin}}+x_n\hat{\mathbf x}.
```

Therefore `LinearArrayGeometry` does not need to duplicate a second authoritative 3-D coordinate table merely to support 3-D propagation mathematics. The intrinsic coordinates plus explicit frame/embedding are the source from which embedded positions are derived.

If externally measured 3-D/global coordinates are available, their relation to the intrinsic 1-D model must be expressed through an explicit transform or import/projection record. They shall not silently replace the intrinsic geometry or be silently projected onto the array axis.

### 6.3 Broadside in 3-D

For a linear array on the `x` axis, broadside is not one unique 3-D direction. The broadside direction set is

```math
u_x=0,
```

that is, the set of unit look directions lying in the `yz` plane.

### 6.4 Canonical 2-D slice

For initial 1-D DOA visualization and one-parameter angle estimation, GeoDOA defines a canonical `xy` slice with

```math
\hat{\mathbf u}(\theta)
=
\begin{bmatrix}
\sin\theta\\
\cos\theta\\
0
\end{bmatrix},
\qquad
\theta\in[-\pi/2,\pi/2].
```

Within this slice:

- `theta = 0` is the chosen `+y` broadside reference direction;
- `theta > 0` rotates toward `+x`;
- `theta < 0` rotates toward `-x`;
- `theta = +pi/2` is `+x` endfire;
- `theta = -pi/2` is `-x` endfire.

The interval `[-pi/2, pi/2]` is a chosen one-to-one parameterization of the canonical visible half-plane; it is not a claim that the physical 1-D array uniquely resolves the full 3-D direction.

## 7. Look Direction and Propagation Direction

GeoDOA distinguishes the source look direction from the direction in which the incident wave propagates.

For the far-field derivation, introduce an explicit array-localization/expansion origin `r_0` and write the source position as

```math
\mathbf r_s
=
\mathbf r_0+R\hat{\mathbf u},
\qquad R>0.
```

The **look direction** is therefore

```math
\hat{\mathbf u}
=
\frac{\mathbf r_s-\mathbf r_0}{\|\mathbf r_s-\mathbf r_0\|_2}.
```

For an incident wave arriving from that source, the **propagation direction** is

```math
\hat{\mathbf p}=-\hat{\mathbf u}.
```

The localization/expansion origin `r_0`, geometry coordinate origin, and spatial phase-reference point `r_ref` are conceptually distinct. In the far-field plane-wave model, a common `u_hat` is used across the array aperture; the validity of that approximation is governed by ADR-002.

These terms and reference points shall not be used interchangeably in scientific APIs, documentation, or derivations.

## 8. Temporal Phasor Convention and Receive-Phase Derivation

### 8.1 Temporal convention

GeoDOA adopts

```math
\exp(-j\omega t)
```

as the temporal phasor convention for the scientific derivations governed by this ADR.

### 8.2 Relative propagation distance

With

```math
\mathbf r_s
=
\mathbf r_0+R\hat{\mathbf u},
```

let

```math
\boldsymbol\delta_n
=
\mathbf r_n-\mathbf r_0.
```

The exact source-to-sensor distance is

```math
R_n
=
\|\mathbf r_s-\mathbf r_n\|_2
=
\|R\hat{\mathbf u}-\boldsymbol\delta_n\|_2.
```

Under the first-order plane-wave expansion,

```math
R_n
\approx
R-\hat{\mathbf u}^T\boldsymbol\delta_n.
```

Define likewise

```math
\boldsymbol\delta_{\mathrm{ref}}
=
\mathbf r_{\mathrm{ref}}-\mathbf r_0,
```

so that

```math
R_{\mathrm{ref}}
\approx
R-\hat{\mathbf u}^T\boldsymbol\delta_{\mathrm{ref}}.
```

Subtracting eliminates the arbitrary expansion origin:

```math
R_n-R_{\mathrm{ref}}
\approx
-(\mathbf r_n-\mathbf r_{\mathrm{ref}})^T\hat{\mathbf u}.
```

Thus the final relative-distance relation is independent of the choice of `r_0` within the same first-order plane-wave model.

### 8.3 Relative delay

For propagation speed `v_p`,

```math
\Delta\tau_n
=
\tau_n-\tau_{\mathrm{ref}}
\approx
-\frac{(\mathbf r_n-\mathbf r_{\mathrm{ref}})^T\hat{\mathbf u}}{v_p}.
```

A negative relative delay means that channel `n` receives the incident waveform earlier than the reference point.

### 8.4 Receive phase

With temporal factor `exp(-j omega t)`, a relative delay contributes

```math
\exp(+j\omega\Delta\tau_n).
```

Substituting the relative-delay expression gives

```math
\exp\!\left[
-j\frac{\omega}{v_p}
(\mathbf r_n-\mathbf r_{\mathrm{ref}})^T\hat{\mathbf u}
\right].
```

Defining

```math
k
=
\frac{\omega}{v_p}
=
\frac{2\pi f}{v_p}
=
\frac{2\pi}{\lambda},
```

produces the canonical geometry-only receive coefficient

```math
a_n(\hat{\mathbf u},f)
=
\exp\!\left[
-jk
(\mathbf r_n-\mathbf r_{\mathrm{ref}})^T\hat{\mathbf u}
\right].
```

For the canonical `xy` slice and a linear array,

```math
a_n(\theta,f)
=
\exp\!\left[
-jk(x_n-x_{\mathrm{ref}})\sin\theta
\right].
```

The minus sign is therefore a consequence of the declared look-direction and temporal-phasor conventions; it is not an arbitrary software preference.

## 9. Phase Reference and Translation Invariance

### 9.1 Explicit and stable spatial phase reference

The manifold is defined relative to an explicit spatial point `r_ref`.

The standard analytical default is the centroid of the **declared nominal physical geometry**, computed from the full declared geometry definition rather than from the currently active-channel subset:

```math
\mathbf r_{\mathrm{geom}}
=
\frac{1}{N_g}
\sum_{n\in\mathcal G}
\mathbf r_n,
```

where `G` is the declared nominal geometry channel set and `N_g` is its size.

This geometry-level reference is ordering-independent, translates with the physical geometry, and remains stable when an active-channel mask changes. Disabling or enabling a channel shall not silently redefine the default spatial phase reference.

Calibration or measurement workflows may explicitly select a named physical reference channel or another declared spatial point. Such an override is part of configuration/provenance. Core scientific semantics shall never infer the phase reference from whichever channel happens to appear first after sorting.

GeoDOA therefore treats the following as distinct concepts:

```text
geometry coordinate origin
far-field expansion/localization origin
spatial phase reference
active-channel mask
```

### 9.2 Translation invariance

If all physical positions and the phase reference are translated by the same vector `t`,

```math
\mathbf r'_n=\mathbf r_n+\mathbf t,
\qquad
\mathbf r'_{\mathrm{ref}}=\mathbf r_{\mathrm{ref}}+\mathbf t,
```

then

```math
\mathbf r'_n-\mathbf r'_{\mathrm{ref}}
=
\mathbf r_n-\mathbf r_{\mathrm{ref}},
```

and the relative manifold is unchanged.

If sensor positions are translated by `t` while the phase reference is held fixed,

```math
\mathbf a'(\hat{\mathbf u})
=
\exp[-jk\mathbf t^T\hat{\mathbf u}]
\mathbf a(\hat{\mathbf u}).
```

The change is therefore a common direction-dependent phase factor across all channels; relative inter-channel phase remains unchanged.

### 9.3 Phase-reference change law

If the physical geometry is fixed and the phase reference changes from `r_ref` to `r_ref'`, then

```math
\mathbf a_{\mathrm{ref}'}(\hat{\mathbf u})
=
\exp\!\left[
+jk(\mathbf r_{\mathrm{ref}'}-\mathbf r_{\mathrm{ref}})^T\hat{\mathbf u}
\right]
\mathbf a_{\mathrm{ref}}(\hat{\mathbf u}).
```

Thus changing only the spatial phase reference multiplies the steering vector by a common unit-magnitude phasor and does not change relative inter-channel phase.

## 10. Physical Coordinates, Channel Identity, Active Views, and Derived Views

### 10.1 Physical coordinates are authoritative

Input physical coordinates shall be preserved in canonical SI units. GeoDOA shall not silently translate, sort, reflect, normalize, deduplicate, or relabel them in the authoritative physical representation.

### 10.2 Channel identity is persistent

Each physical channel has a stable identity independent of its position in a sorted geometry view. This is required so that later calibration, gain/phase mismatch, channel dropout, measured manifolds, and hardware channel mappings remain attached to the correct physical channel.

Authoritative channel order and `sensor_id`/channel identity are not interchangeable concepts. A stable identity must remain available even when an algorithm consumes a permutation or subset of channels.

### 10.3 Sorting is a derived view

Geometry algorithms may request sorted positions, but sorting must return or preserve the permutation between authoritative channel order and sorted geometric order. A sorting operation shall not mutate the stored channel order of an immutable geometry entity.

### 10.4 Active-channel selection is a derived view/configuration

An active-channel mask selects a processing view of the declared geometry. It does not delete channels, renumber channel identities, recompute the default geometry-level phase reference, or mutate the authoritative geometry.

If a new physical array definition is intended after hardware modification, that change creates a new geometry/configuration identity rather than being represented as an undocumented mask mutation.

### 10.5 Translation-normalized geometry is derived

A translation-normalized representation may be used for geometry comparison, hashing, caching, or catalog search. Such a representation shall not overwrite the physical coordinates. The normalization rule and resulting permutation/reference, if any, must be explicit enough to reconstruct how the derived representation was obtained.

### 10.6 Reflection is not default canonicalization

A reflected geometry can share some geometry/coarray metrics with the original while reversing orientation relative to the declared `+x` axis. Reflection equivalence is therefore an optional analysis, not a default canonicalization rule. A reflected comparison/signature shall identify that reflection equivalence was requested rather than silently replacing the geometry identity.

### 10.7 Colocated channels

GeoDOA shall never silently collapse duplicate positions. Accidental duplicate scalar channels are a validation error by default. Explicitly modeled colocated channels may be supported when their distinct physical identity or sensor response is declared. The detailed sensor-response semantics belong to ADR-003.

## 11. Canonical Units and Normalized Representations

### 11.1 Canonical internal units and dimensional semantics

The scientific core uses the following canonical representations:

- physical position, distance, aperture, lattice spacing, wavelength, and physical lattice residual: meter (`m`);
- frequency `f`: hertz (`Hz = s^-1`);
- temporal angular frequency `omega`: radian per second (`rad/s`);
- propagation speed `v_p`: meter per second (`m/s`);
- time and delay: second (`s`);
- angle and phase: radian (`rad`);
- wavenumber `k` and projected angular spatial frequency `kappa_x`: radian per meter (`rad/m`);
- normalized lattice spatial frequency `psi`: radian of phase increment per unit lattice-index increment; numerically/SI-dimensionally dimensionless but semantically represented as `rad`;
- direction vector components, direction cosine `u`, wavelength-normalized position `q_n`, lattice coordinates `z_n`, lattice residuals `epsilon_n` and `rho_n`, lattice tolerance `tau_lat`, real-valued reference lattice coordinate `mu_ref`, integer indices/lags, and gcd factors: dimensionless;
- ideal geometry-only steering/manifold coefficients: dimensionless complex coefficients of unit magnitude;
- power ratio: dimensionless;
- dB quantities: explicit logarithmic display/metric representations, not hidden linear values.

In SI, plane angle and phase are dimensionless derived quantities. GeoDOA nevertheless retains the semantic labels `rad`, `rad/s`, and `rad/m` because doing so prevents confusion between ordinary cyclic frequency and angular frequency, between cycles-per-meter and angular spatial frequency, and between an arbitrary dimensionless scalar and a phase quantity.

All arguments passed to `exp`, `sin`, `cos`, and other transcendental functions must be dimensionless; phase arguments are interpreted semantically in radians.

### 11.2 Unit conversion belongs at boundaries

Validated GUI, CLI, API, and file-schema boundaries may accept supported display/input units when the unit is explicitly labeled. They convert those values to canonical domain units before constructing authoritative domain objects.

The scientific core shall not infer units from magnitude or naming conventions such as `0.5`, `30`, or `half_lambda`. A bare numerical array entering a low-level numerical kernel is interpreted only according to that kernel's typed/scoped contract, never by heuristic unit detection.

Changing display units must not change the physical domain state or its scientific identity.

### 11.3 Wavelength is derived

```math
\lambda(f)=\frac{v_p}{f}.
```

Dimensionally,

```text
(m/s) / (1/s) = m.
```

The propagation speed is explicit; it is not assumed to be the speed of light by every domain object.

### 11.4 Wavenumber and receive-phase dimensions

With

```math
\omega=2\pi f,
\qquad
k=\frac{\omega}{v_p}=\frac{2\pi}{\lambda},
```

`k` has semantic units `rad/m`. Therefore

```math
k(\mathbf r_n-\mathbf r_{\mathrm{ref}})^T\hat{\mathbf u}
```

has units of radians and is dimensionless in the SI dimensional sense, as required for a complex exponential.

Likewise,

```math
\omega\Delta\tau_n
```

has units of radians and is a valid exponential phase argument.

### 11.5 Wavelength-normalized position

Relative wavelength-normalized position is

```math
q_n(f)
=
\frac{x_n-x_{\mathrm{ref}}}{\lambda(f)}.
```

It is dimensionless and frequency dependent. Therefore `x/lambda` is a property of geometry plus a reference frequency/medium, not a frequency-independent physical coordinate.

If normalized positions are accepted as input, a reference wavelength or enough information to derive it must be provided before conversion to meters. An unlabeled value such as `0.5` shall never be assumed to mean `0.5 lambda`.

## 12. Lattice Semantics

### 12.1 Declared lattice

A declared 1-D lattice consists of:

- a physical lattice origin `x_L` in meters;
- a positive base spacing `Delta` in meters;
- integer sensor indices `m_n`, dimensionless;
- an explicit dimensionless numerical lattice tolerance when numerical validation is required.

The exact declared grid relation is

```math
\tilde x_n=x_L+m_n\Delta,
\qquad
m_n\in\mathbb Z,
```

where `tilde x_n` denotes the grid-reconstructed/design position associated with integer index `m_n`.

A lattice declaration is provenance/configuration: it records the intended grid basis and integer indices when those are known by construction. A lattice-validation result is evidence: it records whether authoritative coordinates are consistent with a candidate/declared lattice under a stated tolerance, together with residuals and diagnostics. These are not the same domain object or semantic state.

If authoritative physical coordinates are numerically represented values of that declared grid, they remain stored as `x_n`; GeoDOA does not silently overwrite them with `tilde x_n`.

### 12.2 Lattice validation

For a candidate lattice,

```math
z_n
=
\frac{x_n-x_L}{\Delta},
\qquad
m_n
=
\operatorname{round}(z_n),
```

and define the dimensionless lattice residual

```math
\varepsilon_n=z_n-m_n,
\qquad
\rho_n=|\varepsilon_n|.
```

Nearest-integer lattice validation requires a finite tolerance satisfying

```math
\boxed{0\le\tau_{\mathrm{lat}}<\frac12}.
```

The strict upper bound excludes the half-grid tie at which a candidate coordinate is equally close to two integer lattice indices. Consequently, the scientific contract does not depend on a programming-language-specific half-integer rounding convention.

The candidate lattice is accepted only if

```math
\max_n\rho_n\le\tau_{\mathrm{lat}}.
```

Equivalently,

```math
x_n
=
x_L+(m_n+\varepsilon_n)\Delta,
\qquad
|\varepsilon_n|\le\tau_{\mathrm{lat}}.
```

The corresponding signed physical grid residual is

```math
\eta_n
=
x_n-\tilde x_n
=
\varepsilon_n\Delta,
```

with units of meters and bound

```math
|\eta_n|
\le
\tau_{\mathrm{lat}}\Delta.
```

Thus `epsilon_n`, `rho_n`, and `tau_lat` are dimensionless normalized-grid quantities, whereas `eta_n` is a physical-distance residual. Numerical grid-alignment residual is not physical manufacturing or survey uncertainty; physical position uncertainty is a separate sensor-model quantity governed by ADR-003.

A successful validation may produce a typed/structured `ValidatedLattice`-style derived result containing the declaration/candidate, integer indices, reconstructed positions, normalized and physical residuals, primitive reduction, and validation status. Downstream coarray integer indexing shall consume this validated result or an exact-by-construction lattice declaration whose validity is part of generator provenance; it shall not reconstruct integer semantics independently from raw coordinates.

### 12.3 No blind integerization

Arbitrary real-valued pair differences shall not be divided by an arbitrary spacing and blindly rounded into integer coarray lags. Integer lag semantics exist only after lattice validity has been established.

### 12.4 Integer difference lags and residual bound

For the exact grid-reconstructed positions,

```math
\tilde x_i-\tilde x_j
=
(m_i-m_j)\Delta,
```

so the associated integer difference lag is

```math
\ell_{ij}=m_i-m_j.
```

For authoritative coordinates admitted through numerical tolerance,

```math
x_i-x_j
=
(m_i-m_j)\Delta
+
(\varepsilon_i-\varepsilon_j)\Delta.
```

Every term in this equation has units of meters. Therefore the deviation from the ideal lattice difference satisfies

```math
\left|
(x_i-x_j)-\ell_{ij}\Delta
\right|
\le
2\tau_{\mathrm{lat}}\Delta,
```

where the right-hand side is also a physical distance in meters.

Physical pair difference, grid-reconstructed pair difference, normalized difference, and integer lag are distinct representations and must remain distinguishable.

### 12.5 Declared versus primitive lattice

The declared lattice preserves design provenance. It shall not be silently replaced by a coarser equivalent lattice.

Choose any anchor index `m_0` and define relative integer indices

```math
d_n=m_n-m_0.
```

For a nondegenerate geometry, define

```math
g
=
\gcd\{|d_n|:\ d_n\neq0\}.
```

Equivalently, `g` is the gcd of the nonzero pairwise integer differences. If all indices are identical, the geometry is degenerate for this purpose and no positive primitive spacing is defined.

A gcd-normalized primitive representation is obtained from

```math
\tilde m_n
=
\frac{m_n-m_0}{g}
\in\mathbb Z,
```

and

```math
\Delta_{\mathrm{prim}}=g\Delta.
```

The integer quantities `m_n`, `m_0`, `d_n`, `g`, and `tilde m_n` are dimensionless; `Delta` and `Delta_prim` have units of meters.

Then the exact grid-reconstructed positions satisfy

```math
\tilde x_n
=
\tilde x_0
+
\tilde m_n\Delta_{\mathrm{prim}}.
```

The relative primitive indices have gcd one. This primitive representation is a derived geometry-analysis view. The originally declared `Delta` remains part of provenance because it may represent a fabrication grid, optimization grid, or published-array construction rule.

### 12.6 Lattice spacing is not nearest-neighbor spacing

`Delta` is a declared grid basis. It is not generally equal to every sensor spacing, the minimum pairwise separation, or the nearest-neighbor distance. Likewise, `Delta_prim` is a derived primitive grid basis and need not equal the declared design-grid spacing.

## 13. Direction Cosine and Spatial Frequency

### 13.1 Observable directional coordinate

For a linear array on `+x`, define

```math
u
\equiv
u_x
=
\hat{\mathbf u}\cdot\hat{\mathbf x},
\qquad
u\in[-1,1].
```

This is the fundamental dimensionless direction coordinate observed by the ideal 1-D geometry-only manifold.

For the canonical `xy` slice,

```math
u=\sin\theta,
\qquad
\theta=\arcsin\nu,
```

with the declared principal domain

```math
\theta\in[-\pi/2,\pi/2].
```

On this interval, `sin(theta)` is one-to-one, so the angle and direction-cosine parameterizations are mutually invertible. `theta` is represented semantically in radians.

### 13.2 Direction representations are distinct value semantics

A 3-D unit look direction, canonical-slice angle, direction cosine, projected spatial angular frequency, and normalized lattice spatial frequency are related but not interchangeable representations.

Software may provide explicit constructors/converters such as conceptually

```text
LookDirection3D
CanonicalSliceAngle
DirectionCosine
ProjectedSpatialAngularFrequency
DeclaredGridSpatialPhaseIncrement
```

but the exact class names are deferred. Conversion functions must validate the required domain and context. A low-level manifold kernel may consume a validated unit look vector directly; convenience interfaces may accept angle or direction-cosine value objects and convert explicitly.

An `AngleConvention`-type boundary/configuration object describes how external/user angle values are interpreted and converted to the canonical internal convention. It does not authorize scientific kernels to switch sign/reference conventions implicitly at runtime.

### 13.3 Projected angular spatial frequency

Define

```math
\kappa_x
=ku
=\frac{2\pi}{\lambda}u,
```

with semantic units `rad/m`. Then

```math
a_n
=
\exp[-j\kappa_x(x_n-x_{\mathrm{ref}})].
```

The product `kappa_x (x_n-x_ref)` is a phase in radians and is dimensionless in the SI dimensional sense.

### 13.4 Normalized lattice spatial frequency

For declared lattice spacing `Delta`, define

```math
\psi
=\kappa_x\Delta
=k\Delta u
=\frac{2\pi\Delta}{\lambda}u.
```

Because `kappa_x` has semantic units `rad/m` and `Delta` has units `m`, `psi` is a phase increment in radians per unit increment of the dimensionless lattice index. In SI dimensional analysis it is dimensionless, but GeoDOA retains the semantic unit `rad`.

For an exact lattice position `x_n = x_L + m_n Delta`, define the real-valued, dimensionless reference lattice coordinate

```math
\mu_{\mathrm{ref}}
=
\frac{x_{\mathrm{ref}}-x_L}{\Delta}.
```

The phase reference need not itself be a lattice point. The exact-lattice manifold can therefore be written

```math
a_n
=
\exp[-j(m_n-\mu_{\mathrm{ref}})\psi].
```

The exponential argument is a phase in radians and is dimensionless in SI dimensional analysis.

If `mu_ref` happens to be an integer, it may be denoted by an integer reference index. For tolerance-admitted coordinates, the authoritative physical-coordinate manifold remains the governing expression and the integer-lattice form is a grid-model representation rather than a silent replacement.

Angle `theta`, direction cosine `u`, physical spatial frequency `kappa_x`, declared-grid normalized spatial frequency `psi`, and primitive-grid normalized spatial frequency are distinct domain concepts and shall not be represented by one ambiguously named variable.

## 14. Ambiguity and Identifiability

### 14.1 3-D projection ambiguity

For an ideal linear array on `x`, any two 3-D unit look directions with the same `u_x` generate the same geometry-only relative phase manifold.

Therefore

```math
\hat{\mathbf u}_1\neq\hat{\mathbf u}_2,
\qquad
u_{x,1}=\nu_{x,2}
```

implies

```math
\mathbf a(\hat{\mathbf u}_1)
=
\mathbf a(\hat{\mathbf u}_2)
```

for the ideal scalar geometry-only model with the same frequency and reference convention.

Thus 3-D propagation capability does not imply unique 3-D DOA observability.

### 14.2 Front/back ambiguity

The canonical `xy` slice selects the half-plane `u_y >= 0`. A direction in the opposite half-plane with the same `u_x` produces the same ideal 1-D geometry-only phase progression. The canonical visible sector resolves the parameterization, not the underlying physical ambiguity.

Directional element patterns, polarization, non-collinear geometry, or other physical information may alter this conclusion; those effects are outside the geometry-only model and belong to ADR-003.

### 14.3 Manifold equivalence and spatial aliasing

Spatial aliasing is defined by indistinguishable **relative inter-channel phase structure**, not by literal equality of steering-vector coordinates under every arbitrary phase-reference choice.

For geometry-only unit-magnitude steering vectors, two direction parameters `u_1` and `u_2` are spatially equivalent when there exists a common phase `phi` such that

```math
\mathbf a(u_2)
=
e^{j\phi}\mathbf a(u_1).
```

Equivalently, for every sensor pair `i,j`,

```math
k(x_i-x_j)(u_2-u_1)
\in
2\pi\mathbb Z.
```

The left-hand side is a phase in radians and is dimensionless in the SI dimensional sense. This pair-difference criterion is invariant to the spatial phase-reference choice.

For an exact declared integer lattice with relative-index gcd `g`, the relative phase structure is periodic in the declared-grid normalized spatial frequency `psi` with fundamental period

```math
\Delta\psi_{\mathrm{fund}}
=
\frac{2\pi}{g}.
```

`Delta psi_fund` is a phase increment in radians. Equivalently, using the primitive spacing

```math
\Delta_{\mathrm{prim}}=g\Delta,
```

and primitive normalized spatial frequency

```math
\psi_{\mathrm{prim}}
=
k\Delta_{\mathrm{prim}}u
=
g\psi,
```

the fundamental period is `2 pi` radians.

Thus the familiar identity

```math
\exp[-jm(\psi+2\pi q)]
=
\exp[-jm\psi]
```

is always a valid `2 pi` periodicity statement for integer `m`, but `2 pi` need not be the **fundamental** period of the relative manifold when all relative indices share a gcd greater than one.

For a conventional ULA with consecutive primitive indices, `g = 1` and `Delta_prim = Delta`. In that case:

- `Delta <= lambda/2` gives the usual no-grating-lobe condition for distinct directions in the **open** visible interval `u in (-1,1)`;
- at exactly `Delta = lambda/2`, the two endfire endpoints `u = +1` and `u = -1` are spatially equivalent;
- strict injectivity over the entire **closed** interval `u in [-1,1]` requires

```math
\Delta<\frac{\lambda}{2}.
```

For a general exact lattice geometry, ambiguity is governed by the primitive spacing and the full pair-difference structure. For arbitrary nonuniform real geometries, ambiguity shall be diagnosed directly from the full pair-difference/manifold criterion rather than inferred from a nearest-neighbor rule.

### 14.4 Projection ambiguity is not spatial aliasing

Projection ambiguity occurs when physically distinct 3-D directions have the same observable projection `u_x`. Spatial aliasing occurs when distinct observable `u` values produce spatially equivalent sampled manifolds. These are different mechanisms and must be diagnosed separately.

### 14.5 Lattice validity is not spatial unambiguity

A geometry may be perfectly lattice-valid and still spatially aliased. Lattice validation is a geometric/numerical statement; spatial unambiguity is an observability statement.

### 14.6 Ambiguity diagnostics are results, not silent canonicalization

Software may return ambiguity/equivalence diagnostics, equivalence classes, or warnings. It shall not silently collapse two distinct requested directions into one canonical value, nor silently alter a scan grid to remove an ambiguity. Any reduction to a representative value is a separate explicit analysis operation and must preserve the original requested values and diagnostic reason.

## 15. Scan-Grid Semantics

A uniform angle grid is not a uniform direction-cosine grid because

```math
u=\sin\theta,
\qquad
\frac{du}{d\theta}=\cos\theta.
```

With `theta` expressed in radians, the derivative is dimensionless per radian; since radians are SI-dimensionless, the relation is dimensionally consistent. Numerical differentiation or grid-spacing conversion must not silently substitute degrees into this relation without conversion.

Likewise, a uniform direction-cosine grid maps to a uniform `kappa_x` grid only at fixed frequency/medium, and to a uniform `psi` grid only for fixed declared lattice spacing.

GeoDOA shall therefore distinguish conceptual scan domains such as:

- angle grid;
- direction-cosine grid;
- projected-spatial-frequency grid;
- declared-grid normalized-spatial-frequency grid;
- primitive-grid normalized-spatial-frequency grid.

A scan grid is a typed domain/view object with an explicit coordinate domain and context. It is not merely an unlabeled NumPy vector. Conversion between scan domains creates a new derived grid or view; it does not mutate the source grid or discard the mapping/provenance needed to interpret results.

Conversions must be explicit and carry the frequency, medium, lattice, and convention context required to make them meaningful.

## 16. Deterministic Reference Expectations

ADR-001 approval is supported by deterministic hand-computable Golden Reference Problems covering at least the following contracts:

- **GRP-001:** two-sensor propagation-distance and relative-delay calculation;
- **GRP-002:** two-sensor steering-vector phase, including the `d = lambda/2`, `theta = 30 deg` result;
- **GRP-003:** translation invariance and phase-reference change;
- **GRP-004:** two distinct 3-D directions with identical `u_x` and therefore identical ideal 1-D manifolds;
- **GRP-005:** spatial aliasing for a lattice array, including a `d = lambda` example, the `d = lambda/2` endfire-endpoint boundary case, and a gcd-greater-than-one lattice periodicity example;
- **GRP-006:** lattice validation, residual bound, primitive-lattice reduction, and integer difference-coarray lag construction.

The accepted hand solutions and expected values are recorded in:

```text
docs/science/golden_reference/ADR-001_GOLDEN_REFERENCE_PROBLEMS.md
```

These problems are independently solvable using paper, pencil, and a basic calculator and shall later serve as software regression-test oracles.

## 17. Required Software Semantics Implied by This ADR

ADR-001 constrains software meaning without fixing final class names or implementation details.

### 17.1 Concept-to-domain mapping

The implementation must provide unambiguous domain representations for at least the following roles:

| Scientific concept | Required software semantic role |
|---|---|
| Intrinsic 1-D physical coordinates and stable channel identity | Immutable `LinearArrayGeometry`-style entity |
| Local array axis/origin/broadside orientation and embedding into 3-D | `ReferenceFrame1D`-style value object |
| External angle interpretation/sign/reference | `AngleConvention`-style boundary/configuration value |
| Canonical 3-D look direction | Validated unit-direction value |
| Spatial phase reference | Explicit reference-point/reference-policy value, distinct from coordinate origin |
| Frequency and propagation speed context | Typed `WaveParameters`-style value object; detailed medium semantics deferred to ADR-002 |
| Declared design lattice | Immutable lattice-declaration value with origin, spacing, and integer indices |
| Lattice validation evidence | Typed validation result with residuals/status; not the same object as the declaration |
| Active-channel selection | Immutable mask/subset view or configuration referencing stable channel identities |
| Sorted/normalized/reflected representations | Derived views/results preserving source identity and transformation metadata |
| Angle/u/kappa/psi scan domains | Distinct typed grid/value semantics with explicit conversions |
| Manifold output | Typed result that records reference/convention/context rather than a context-free complex vector |
| Ambiguity/equivalence analysis | Diagnostic result; never silent canonicalization |

Exact Python names are deferred, but collapsing semantically distinct rows of this table into one ambiguous scalar/array field is not permitted.

### 17.2 Geometry and frame responsibilities

`LinearArrayGeometry` owns intrinsic 1-D coordinates, stable channel identities, and immutable geometry provenance. It does not own propagation-wave assumptions and does not need to store a redundant authoritative 3-D position table for the initial 1-D scope.

`ReferenceFrame1D`-style semantics own the local embedding/orientation needed to derive 3-D positions and transform to/from platform/global frames. Geometry-family generators produce the same geometry contract and shall not invent family-specific angle or phase conventions.

### 17.3 Boundary conventions versus canonical core convention

External schemas may support named angle conventions or degree-valued input, but conversion to the canonical internal convention occurs before scientific kernels are called. A manifold kernel shall not branch on UI-specific labels such as `degrees`, `broadside_sine`, or `endfire_cosine` and silently reinterpret raw numeric arrays.

Likewise, normalized-position input may be accepted only at a validated boundary with explicit wavelength/frequency/medium context and shall be converted to canonical physical coordinates before construction of the authoritative geometry.

### 17.4 Derived views shall not become hidden state

Sorting, active masking, translation normalization, reflection comparison, primitive-lattice reduction, wavelength normalization, and scan-domain conversion are explicit derived operations. They shall either return typed derived values/results or produce a new immutable configuration/entity when the operation represents a genuinely new physical definition.

They shall not mutate an existing authoritative geometry/configuration in place.

### 17.5 Lattice consumer rule

Coarray and other integer-lag consumers shall require validated integer-lattice semantics. They must consume either:

- an exact-by-construction lattice declaration whose generator provenance establishes exactness; or
- a successful lattice-validation result containing the accepted indices, residuals, tolerance, and source geometry identity.

A downstream component shall not independently call `round((x_i-x_j)/Delta)` on raw coordinates to manufacture integer lags.

### 17.6 Reference and identity propagation

A manifold/result produced under a spatial phase reference, coordinate frame, active-channel view, or scan-domain mapping must retain enough metadata to interpret that output and compare it correctly with another output.

Common-phase-equivalent manifolds may be compared with a reference-invariant metric when appropriate, but software shall not erase the original reference convention before provenance is recorded.

### 17.7 Scientific kernels versus adapters

Pure numerical kernels may operate on canonical NumPy arrays and scalars after domain validation/conversion. They do not need to carry GUI/schema objects internally. The application/domain layer is responsible for providing canonical arrays plus the metadata/result contract needed to reconstruct scientific meaning.

This preserves both efficient numerical code and semantic correctness.

### 17.8 Forbidden implicit behavior

Later implementation governed by ADR-001 shall not:

- hard-code a 2-D `sin(theta)` representation where the general direction-vector inner product is appropriate;
- silently shift the coordinate origin;
- silently select the first sorted channel as phase reference;
- recompute the default phase reference from an active subset;
- mutate sensor/channel identity during sorting or masking;
- infer physical units from numeric magnitude;
- pass degree-valued raw numbers to radian-expecting scientific kernels;
- silently replace physical coordinates with wavelength-normalized coordinates;
- accept a nonfinite, negative, or `tau_lat >= 0.5` nearest-integer lattice tolerance;
- silently snap tolerance-admitted coordinates to a reconstructed lattice;
- reuse numerical lattice tolerance as physical position uncertainty;
- infer an integer lattice inside a coarray consumer from arbitrary real coordinates;
- use one unlabeled scalar/vector type for angle, direction cosine, `kappa_x`, and `psi` without explicit semantic context;
- silently choose declared versus primitive lattice spatial frequency;
- silently canonicalize reflected geometries or aliased directions;
- classify a common phase-reference factor as physical manifold distortion.

## 18. Alternatives Considered and Rejected

### 18.1 Hard-code a 2-D steering formula

Rejected because a 1-D array can exist in 3-D propagation space, and the inner-product formulation generalizes cleanly to later 2-D/3-D geometries.

### 18.2 Use propagation direction as the primary source-direction variable

Rejected for the public scientific convention because array-processing users commonly reason about the direction from which a source is observed. GeoDOA instead defines an explicit look direction and separately records that incident propagation is `-u_hat`.

### 18.3 Use `exp(+j omega t)`

Mathematically valid if all spatial signs are changed consistently, but rejected to preserve one explicit project-wide convention. The chosen `exp(-j omega t)` convention is not claimed to be universally superior.

### 18.4 Measure the canonical angle from endfire

Rejected for the initial human-facing slice because broadside-referenced angle is natural for the intended array-processing workflow and gives `u = sin(theta)` with `theta = 0` at broadside.

### 18.5 Use the first sorted sensor as the implicit phase reference

Rejected because sorting is a derived geometry operation and must not change the scientific phase reference or calibration association.

### 18.6 Recompute the default phase reference from the active-channel subset

Rejected as the default policy because channel masking would silently rephase the manifold and complicate cross-run comparison and calibration provenance. Active subsets use the stable geometry-level default reference unless an explicit override is declared.

### 18.7 Store geometry only in wavelengths

Rejected because physical sensors do not move when operating frequency changes. Wavelength normalization is a frequency-referenced derived view.

### 18.8 Store independent authoritative 1-D and 3-D coordinate tables for the same initial linear geometry

Rejected because duplicated authoritative state can diverge. The 1-D intrinsic coordinates plus explicit frame/embedding derive the 3-D positions required by propagation calculations.

### 18.9 Silently snap tolerance-admitted positions to a lattice

Rejected because numerical validation of intended grid membership does not authorize destruction of the authoritative physical coordinates or concealment of residuals.

### 18.10 Round arbitrary pair differences into integer lags

Rejected because it manufactures lattice structure that may not physically or mathematically exist.

### 18.11 Reflection-normalize every geometry

Rejected because reflection changes orientation relative to the declared array axis even when some geometry metrics are equivalent.

### 18.12 Define spatial aliasing by exact steering-vector equality only

Rejected because the literal vector representation changes by a common phasor when the spatial phase reference changes. Relative inter-channel phase equivalence is the reference-invariant mathematical criterion relevant to geometry-only DOA observability.

### 18.13 Let each estimator or GUI interpret angle conventions independently

Rejected because it creates mirrored or inconsistent results across simulator, manifold, estimator, plots, and hardware backends. External conventions are converted explicitly to one canonical core convention.

### 18.14 Allow lattice tolerance to include the half-grid tie

Rejected because a coordinate at a half-integer normalized grid location is equally close to two candidate integer indices. The accepted nearest-integer validation contract therefore requires `tau_lat < 0.5` and remains independent of language-specific tie-breaking rules.

## 19. Consequences

### 19.1 Positive consequences

- steering-vector sign is traceable to physical delay and temporal convention;
- the far-field derivation no longer conflates expansion origin with spatial phase reference;
- intrinsic 1-D geometry and 3-D propagation embedding have non-overlapping software responsibilities;
- the initial 1-D implementation remains compatible with later 2-D/3-D spatial extensions;
- calibration and hardware channel identity are protected from geometry sorting;
- active-channel masking does not silently redefine geometry or the default phase reference;
- phase-reference changes have an explicit common-phasor transformation law;
- canonical units and dimensionless normalized quantities are explicitly separated;
- semantic radian metadata is preserved for phase and angular/spatial angular frequency;
- normalized and physical lattice residuals are explicitly distinguished;
- lattice declaration and lattice validation evidence are different semantic objects;
- nearest-integer lattice validation has a unique admissible tolerance domain;
- tolerance-admitted lattice coordinates retain explicit residuals rather than false exact equalities;
- coarray integer lags cannot be fabricated by downstream rounding;
- declared and primitive lattice periodicities are mathematically distinguished;
- spatial aliasing is defined in a phase-reference-invariant manner;
- scan domains cannot silently change meaning through an unlabeled array;
- physical and wavelength-normalized geometry remain unambiguous;
- projection ambiguity and spatial aliasing can be diagnosed separately;
- the half-wavelength endfire endpoint condition is represented explicitly;
- future Dash, CLI, notebook, fixed-point, and FPGA paths can share the same scientific definitions.

### 19.2 Costs and constraints

- APIs must carry more explicit context than a minimal `steering_vector(theta)` function;
- unit, reference, lattice, residual, frame, and channel-identity metadata must be preserved;
- boundary layers must perform explicit unit and convention conversion;
- derived views need explicit result/metadata contracts;
- some convenient automatic normalization operations become explicit transformations;
- later validation must test invariance, identity preservation, round-trip conversions, projective manifold equivalence, dimensional consistency, and ambiguity behavior, not only nominal numerical outputs.

These costs are intentional because GeoDOA prioritizes scientific traceability over convenience shortcuts.

## 20. Deferred Implementation-Level Decisions

The following do not block the accepted scientific convention but are deferred to implementation design:

- exact numerical default value and scale policy for `tau_lat`, subject to the accepted scientific bound `0 <= tau_lat < 0.5`;
- exact Python class names and module placement for direction, reference, lattice, mask, and grid value objects;
- serialization schema for coordinate frames and phase references;
- exact shape convention for canonical internal NumPy arrays used by low-level kernels;
- geometry-hash encoding and numerical quantization policy;
- user-interface defaults for degree/radian display;
- detailed explicit-colocation configuration for non-scalar sensors.

These are implementation decisions, not permission to collapse distinct scientific semantics. Any implementation-level choice must remain consistent with the roles and forbidden behaviors defined above.

## 21. Acceptance-Gate Status

ADR-001 is **Accepted**. All six Phase 0C acceptance gates passed with explicit evidence.

| Gate | Requirement | Current Status |
|---|---|---|
| A | Physical consistency | PASS — `ADR-001_ACCEPTANCE_AUDIT.md` |
| B | Mathematical consistency | PASS — `ADR-001_ACCEPTANCE_AUDIT.md` |
| C | Dimensional and unit consistency | PASS — `ADR-001_ACCEPTANCE_AUDIT.md` |
| D | Software semantic consistency | PASS — `ADR-001_ACCEPTANCE_AUDIT.md` |
| E | Hand-calculated reference evidence | PASS — `../science/golden_reference/ADR-001_GOLDEN_REFERENCE_PROBLEMS.md` |
| F | Boundary and failure analysis | PASS — `ADR-001_BOUNDARY_FAILURE_ANALYSIS.md` and `ADR-001_ACCEPTANCE_AUDIT.md` |

Acceptance means that ADR-001 is the authoritative GeoDOA scientific contract for its declared scope. It does **not** claim that Phase 1 software has already implemented or verified the contract; later implementation must reproduce the Golden Reference expectations and obey the boundary/failure behaviors.

## 22. Relationships to Later Scientific Contracts

ADR-001 defines the spatial language used by later contracts.

- **ADR-002** will define wave, propagation, waveform, source motion, FMCW/pulse/stepped-frequency, passive/active sensing, and measurement-axis semantics.
- **ADR-003** will define nominal/true/calibrated manifolds, element response, position error, gain/phase mismatch, mutual coupling, channel delay/skew, quantization, and calibration provenance.
- **ADR-004** will define verification, validation, ground truth, Golden Reference Problem evidence, Monte Carlo reproducibility, failure handling, and benchmark fairness.

Supporting scientific notes may derive individual results at greater pedagogical depth without changing the decisions in this ADR.

## 23. Governing Principles Captured by ADR-001

1. **Never destroy physical provenance for mathematical convenience.**
2. **Never infer physical meaning from an unlabeled number.**
3. **Never manufacture an integer coarray by rounding arbitrary geometry.**
4. **Never confuse an angular coordinate with the spatial quantity actually observed by the array.**
5. **Never treat 3-D propagation capability as proof of unique 3-D DOA observability.**
6. **Never choose a steering-vector sign without declaring the direction and temporal-phasor conventions that produce it.**
7. **Never call two manifolds distinguishable merely because they differ by a common phase-reference factor.**
8. **Never use a dimensionless numerical representation to erase the semantic distinction between angle, phase, normalized position, and lattice index.**
9. **Never let a derived software view silently become authoritative physical state.**
10. **Never turn an ambiguity, incompatibility, or model-boundary condition into an apparently unique valid result by silence.**

## 24. Accepted Boundary and Failure Contract

The detailed Gate F analysis is recorded in:

```text
docs/adr/ADR-001_BOUNDARY_FAILURE_ANALYSIS.md
```

ADR-001 adopts the following response classes for later software/API design:

- **REJECT** — the requested object or operation is scientifically undefined or violates an invariant of this ADR;
- **INCOMPATIBLE / REQUIRE OTHER MODEL** — the scenario is meaningful but requires ADR-002, ADR-003, or another provider rather than the nominal geometry-only contract;
- **DIAGNOSTIC / WARN** — the calculation may proceed, but ambiguity, conditioning, aliasing, or interpretation limits must remain explicit;
- **VALID** — the condition lies within the declared scientific contract.

Material accepted boundaries include:

- finite nonempty declared geometry and stable unique channel identity;
- explicit treatment of zero/insufficient directional aperture;
- valid finite coordinate frame and unit look direction;
- physical `u in [-1,1]` and canonical `theta in [-pi/2, pi/2]` unless an explicit external convention is converted at a boundary;
- positive finite physical frequency and propagation speed for this manifold contract;
- explicit incompatibility rather than silent use when near-field/wideband physics exceeds the selected model;
- projection ambiguity, front/back ambiguity, spatial aliasing, and half-wavelength endpoint equivalence as first-class diagnostics;
- angle-conditioning sensitivity near endfire;
- finite positive lattice spacing and `0 <= tau_lat < 0.5` for nearest-integer validation;
- failed lattice validation prohibiting integer-lag consumers while leaving real physical pair-difference analysis valid;
- preservation of declared versus primitive lattice provenance;
- active-channel masking as a view that cannot silently redefine geometry or the default phase reference;
- traceable sorting/normalization/reflection operations;
- exact-vector and common-phase-equivalent manifold comparisons as distinct metrics;
- nonideal propagation/sensor effects requiring the appropriate later scientific contract or an explicit nominal-baseline label.

These boundary rules are normative consequences of ADR-001 and must be reflected in later compatibility validators, domain constructors, diagnostics, and regression tests.
