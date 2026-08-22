# ADR-001 — Coordinate, Direction, and Spatial Conventions

- **Status:** Proposed — scientific review in progress
- **Phase:** 0C — Scientific Foundations
- **Scope:** Coordinate, direction, spatial-phase, unit, reference, and lattice conventions
- **Depends on:** `GEODOA_STUDIO_MASTER_START_HANDOFF.md`, `PHASE0C_SCIENTIFIC_CONTRACTS_ROADMAP.md`
- **Supersedes:** None
- **Superseded by:** None

## 1. Decision Summary

GeoDOA Studio shall treat array-geometry dimension, propagation-space dimension, and identifiable directional dimension as distinct concepts.

The initial physical array scope is one-dimensional: nominal sensor phase centers lie on the local `+x` array axis. The scientific direction model is nevertheless embedded in three-dimensional Euclidean space. For an ideal scalar 1-D array, the geometry-only receive manifold observes only the projection of the source look direction onto the array axis.

The canonical geometry-only receive manifold is derived from propagation delay using the temporal phasor convention `exp(-j omega t)`. For a look-direction unit vector `u_hat`, a propagation speed `v_p`, frequency `f`, wavenumber `k = 2 pi f / v_p`, sensor phase-center position `r_n`, and explicit phase-reference point `r_ref`, the nominal receive coefficient is

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

### 5.1 Sensor phase center

`r_n` denotes the physical phase-center position associated with channel `n` in the active coordinate frame. A sensor identity and its position are related but distinct pieces of information.

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

The initial canonical local frame is right-handed with the linear-array axis along `+x`.

For an ideal 1-D geometry,

```math
\mathbf r_n
=
\begin{bmatrix}
x_n\\0\\0
\end{bmatrix}.
```

The choice of a local array frame does not destroy or replace externally measured global coordinates. Global-to-local transforms, when introduced, must be explicit and provenance-preserving.

### 6.2 Broadside in 3-D

For a linear array on the `x` axis, broadside is not one unique 3-D direction. The broadside direction set is

```math
u_x=0,
```

that is, the set of unit look directions lying in the `yz` plane.

### 6.3 Canonical 2-D slice

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

- `theta = 0` is the `+y` broadside reference direction;
- `theta > 0` rotates toward `+x`;
- `theta < 0` rotates toward `-x`;
- `theta = +pi/2` is `+x` endfire;
- `theta = -pi/2` is `-x` endfire.

The interval `[-pi/2, pi/2]` is a chosen one-to-one parameterization of the canonical visible half-plane; it is not a claim that the physical 1-D array uniquely resolves the full 3-D direction.

## 7. Look Direction and Propagation Direction

GeoDOA distinguishes the direction from the array reference toward the source from the direction in which the incident wave propagates.

The **look direction** is

```math
\hat{\mathbf u}
=
\text{unit vector from the array reference toward the source}.
```

For an incident wave arriving from that source, the **propagation direction** is

```math
\hat{\mathbf p}=-\hat{\mathbf u}.
```

These terms shall not be used interchangeably in scientific APIs, documentation, or derivations.

## 8. Temporal Phasor Convention and Receive-Phase Derivation

### 8.1 Temporal convention

GeoDOA adopts

```math
\exp(-j\omega t)
```

as the temporal phasor convention for the scientific derivations governed by this ADR.

### 8.2 Relative propagation distance

Let a far source be located at

```math
\mathbf r_s=R\hat{\mathbf u}.
```

The exact source-to-sensor distance is

```math
R_n
=
\|R\hat{\mathbf u}-\mathbf r_n\|_2.
```

Under the first-order plane-wave expansion,

```math
R_n
\approx
R-\hat{\mathbf u}^T\mathbf r_n.
```

Relative to an explicit spatial phase-reference point `r_ref`,

```math
R_n-R_{\mathrm{ref}}
\approx
-(\mathbf r_n-\mathbf r_{\mathrm{ref}})^T\hat{\mathbf u}.
```

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

### 9.1 Explicit spatial phase reference

The manifold is defined relative to an explicit spatial point `r_ref`.

The standard analytical default policy is the centroid of the active sensor phase centers,

```math
\mathbf r_c
=
\frac{1}{N_a}
\sum_{n\in\mathcal A}
\mathbf r_n,
```

where `A` is the active-channel set and `N_a` is its size.

The centroid default is ordering-independent and translates with the array. Calibration or measurement workflows may explicitly select a named physical reference channel or another spatial reference point. Core scientific semantics shall never infer the phase reference from whichever channel happens to appear first after sorting.

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

If the reference is not translated, translation changes the steering vector only by a common direction-dependent complex phase factor. Relative inter-channel phase remains unchanged.

## 10. Physical Coordinates, Channel Identity, and Derived Views

### 10.1 Physical coordinates are authoritative

Input physical coordinates shall be preserved in canonical SI units. GeoDOA shall not silently translate, sort, reflect, normalize, deduplicate, or relabel them in the authoritative physical representation.

### 10.2 Channel identity is persistent

Each physical channel has a stable identity independent of its position in a sorted geometry view. This is required so that later calibration, gain/phase mismatch, channel dropout, measured manifolds, and hardware channel mappings remain attached to the correct physical channel.

### 10.3 Sorting is a derived view

Geometry algorithms may request sorted positions, but sorting must preserve the permutation between authoritative channel order and sorted geometric order.

### 10.4 Translation-normalized geometry is derived

A translation-normalized representation may be used for geometry comparison, hashing, caching, or catalog search. Such a representation shall not overwrite the physical coordinates.

### 10.5 Reflection is not default canonicalization

A reflected geometry can share some geometry/coarray metrics with the original while reversing orientation relative to the declared `+x` axis. Reflection equivalence is therefore an optional analysis, not a default canonicalization rule.

### 10.6 Colocated channels

GeoDOA shall never silently collapse duplicate positions. Accidental duplicate scalar channels are a validation error by default. Explicitly modeled colocated channels may be supported when their distinct physical identity or sensor response is declared. The detailed sensor-response semantics belong to ADR-003.

## 11. Canonical Units and Normalized Representations

### 11.1 Canonical internal units

The scientific core uses:

- physical distance: meter (`m`);
- frequency: hertz (`Hz`);
- propagation speed: meter per second (`m/s`);
- wavelength: meter (`m`);
- time and delay: second (`s`);
- angle: radian (`rad`);
- phase: radian (`rad`);
- projected angular spatial frequency: radian per meter (`rad/m`);
- power ratio: dimensionless;
- dB quantities: explicit logarithmic display/metric representations, not hidden linear values.

### 11.2 Wavelength is derived

```math
\lambda(f)=\frac{v_p}{f}.
```

The propagation speed is explicit; it is not assumed to be the speed of light by every domain object.

### 11.3 Wavelength-normalized position

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

- a physical lattice origin `x_L`;
- a positive base spacing `Delta` in meters;
- integer sensor indices `m_n`;
- an explicit numerical lattice tolerance.

The ideal relation is

```math
x_n=x_L+m_n\Delta,
\qquad
m_n\in\mathbb Z.
```

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

and the dimensionless residual is

```math
\rho_n=|z_n-m_n|.
```

The lattice is accepted only if

```math
\max_n\rho_n\le\tau_{\mathrm{lat}},
```

for an explicitly declared numerical tolerance `tau_lat`.

The tolerance is a numerical grid-alignment tolerance, not a physical manufacturing or survey uncertainty. Physical position uncertainty is a separate sensor-model quantity governed by ADR-003.

### 12.3 No blind integerization

Arbitrary real-valued pair differences shall not be divided by an arbitrary spacing and blindly rounded into integer coarray lags. Integer lag semantics exist only after lattice validity has been established.

### 12.4 Integer difference lags

For a validated lattice,

```math
x_i-x_j=(m_i-m_j)\Delta,
```

and the integer difference lag is

```math
\ell_{ij}=m_i-m_j.
```

Physical lag, normalized lag, and integer lag are distinct representations and must remain distinguishable.

### 12.5 Declared versus primitive lattice

The declared lattice preserves design provenance. It shall not be silently replaced by a coarser equivalent lattice.

For integer indices, let

```math
g
=
\gcd\{m_i-m_j\;|\; i,j\},
```

with `g > 0` for a nondegenerate geometry. A gcd-normalized primitive representation may be derived using

```math
\Delta_{\mathrm{prim}}=g\Delta,
```

and correspondingly reduced translated integer indices whose pairwise gcd is one.

This primitive representation is a derived geometry-analysis view. The originally declared `Delta` remains part of provenance because it may represent a fabrication grid, optimization grid, or published-array construction rule.

### 12.6 Lattice spacing is not nearest-neighbor spacing

`Delta` is a grid basis. It is not generally equal to every sensor spacing, the minimum pairwise separation, or the nearest-neighbor distance.

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

This is the fundamental direction coordinate observed by the ideal 1-D geometry-only manifold.

For the canonical `xy` slice,

```math
u=\sin\theta,
\qquad
\theta=\arcsin\nu.
```

### 13.2 Projected angular spatial frequency

Define

```math
\kappa_x
=ku
=\frac{2\pi}{\lambda}u,
```

with units `rad/m`. Then

```math
a_n
=
\exp[-j\kappa_x(x_n-x_{\mathrm{ref}})].
```

### 13.3 Normalized lattice spatial frequency

For lattice spacing `Delta`, define

```math
\psi
=\kappa_x\Delta
=k\Delta u
=\frac{2\pi\Delta}{\lambda}u.
```

For a lattice position `m_n`, the relative manifold is

```math
a_n
=
\exp[-j(m_n-m_{\mathrm{ref}})\psi]
```

when the phase reference is represented on the same lattice. More generally, the physical-reference formulation remains authoritative.

Angle `theta`, direction cosine `u`, physical spatial frequency `kappa_x`, and normalized lattice spatial frequency `psi` are distinct domain concepts and shall not be represented by one ambiguously named variable.

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

for the ideal scalar geometry-only model.

Thus 3-D propagation capability does not imply unique 3-D DOA observability.

### 14.2 Front/back ambiguity

The canonical `xy` slice selects the half-plane `u_y >= 0`. A direction in the opposite half-plane with the same `u_x` produces the same ideal 1-D geometry-only phase progression. The canonical visible sector resolves the parameterization, not the underlying physical ambiguity.

Directional element patterns, polarization, non-collinear geometry, or other physical information may alter this conclusion; those effects are outside the geometry-only model and belong to ADR-003.

### 14.3 Spatial aliasing

Projection ambiguity and spatial aliasing are distinct.

Spatial aliasing occurs when different observable directional coordinates produce equivalent sampled spatial manifolds. For an integer lattice,

```math
\exp[-jm(\psi+2\pi q)]
=
\exp[-jm\psi],
\qquad q\in\mathbb Z.
```

For a conventional ULA with primitive spacing `Delta`, the full visible `u` interval maps inside the principal spatial-frequency interval when

```math
\Delta\le\frac{\lambda}{2}.
```

For sparse or nonuniform geometries, ambiguity shall be diagnosed from the full geometry/manifold rather than inferred solely from a nearest-neighbor rule.

### 14.4 Lattice validity is not spatial unambiguity

A geometry may be perfectly lattice-valid and still spatially aliased. Lattice validation is a geometric/numerical statement; spatial unambiguity is an observability statement.

## 15. Scan-Grid Semantics

A uniform angle grid is not a uniform direction-cosine grid because

```math
u=\sin\theta,
\qquad
\frac{du}{d\theta}=\cos\theta.
```

Likewise, a uniform direction-cosine grid maps to a uniform `kappa_x` grid only at fixed frequency/medium, and to a uniform `psi` grid only for fixed lattice spacing.

GeoDOA shall therefore distinguish conceptual scan domains such as:

- angle grid;
- direction-cosine grid;
- projected-spatial-frequency grid;
- normalized-lattice-spatial-frequency grid.

Conversions must be explicit and carry the frequency, medium, and lattice context required to make them meaningful.

## 16. Deterministic Reference Expectations

ADR-001 is not eligible for approval until deterministic hand-computable Golden Reference Problems cover at least the following contracts:

- **GRP-001:** two-sensor propagation-distance and relative-delay calculation;
- **GRP-002:** two-sensor steering-vector phase, including the `d = lambda/2`, `theta = 30 deg` result;
- **GRP-003:** translation invariance and phase-reference change;
- **GRP-004:** two distinct 3-D directions with identical `u_x` and therefore identical ideal 1-D manifolds;
- **GRP-005:** spatial aliasing for a lattice array, including a `d = lambda` example;
- **GRP-006:** lattice validation and integer difference-coarray lag construction.

The Golden Reference Problems shall be independently solvable using paper, pencil, and a basic calculator and shall later serve as software regression-test oracles.

## 17. Required Software Semantics Implied by This ADR

Later implementation governed by this ADR must satisfy the following constraints:

- scientific kernels shall not hard-code a 2-D `sin(theta)` representation when the general direction-vector inner product is appropriate;
- physical channel identity shall survive sorting and derived views;
- no core algorithm shall silently shift the coordinate origin;
- phase-reference policy shall be explicit and reproducible;
- unit conversion shall occur at defined boundaries rather than being inferred from numerical magnitude;
- lattice integerization shall require explicit lattice context and validation;
- numerical lattice tolerance shall not be reused as physical position uncertainty;
- angle, direction cosine, `kappa_x`, and `psi` shall remain semantically distinguishable;
- ambiguity diagnostics shall distinguish projection ambiguity from spatial aliasing;
- common phase changes caused only by reference choice shall not be misclassified as physical manifold distortion.

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

### 18.6 Store geometry only in wavelengths

Rejected because physical sensors do not move when operating frequency changes. Wavelength normalization is a frequency-referenced derived view.

### 18.7 Silently sort or translation-normalize input positions

Rejected because it destroys physical/channel provenance and can misassociate calibration and hardware channels.

### 18.8 Round arbitrary pair differences into integer lags

Rejected because it manufactures lattice structure that may not physically or mathematically exist.

### 18.9 Reflection-normalize every geometry

Rejected because reflection changes orientation relative to the declared array axis even when some geometry metrics are equivalent.

## 19. Consequences

### 19.1 Positive consequences

- steering-vector sign is traceable to physical delay and temporal convention;
- the initial 1-D implementation remains compatible with later 2-D/3-D spatial extensions;
- calibration and hardware channel identity are protected from geometry sorting;
- coarray integer lags cannot be fabricated by numerical rounding;
- physical and wavelength-normalized geometry remain unambiguous;
- projection ambiguity and spatial aliasing can be diagnosed separately;
- future Dash, CLI, notebook, fixed-point, and FPGA paths can share the same scientific definitions.

### 19.2 Costs and constraints

- APIs must carry more explicit context than a minimal `steering_vector(theta)` function;
- unit, reference, and lattice metadata must be preserved;
- some convenient automatic normalization operations become explicit derived transformations;
- later validation must test invariance and ambiguity behavior, not only nominal numerical outputs.

These costs are intentional because GeoDOA prioritizes scientific traceability over convenience shortcuts.

## 20. Deferred Implementation-Level Decisions

The following do not block the scientific convention but are deferred to implementation design:

- exact numerical default value and scale policy for `tau_lat`;
- serialization schema for coordinate frames and phase references;
- exact API name for direction objects and grid objects;
- geometry-hash encoding and numerical quantization policy;
- user-interface defaults for degree/radian display;
- detailed explicit-colocation configuration for non-scalar sensors.

Any implementation-level choice must remain consistent with the scientific decisions above.

## 21. Acceptance-Gate Status

ADR-001 remains **Proposed** until all Phase 0C acceptance gates pass.

| Gate | Requirement | Current Status |
|---|---|---|
| A | Physical consistency | Pending formal audit |
| B | Mathematical consistency | Pending formal audit |
| C | Dimensional and unit consistency | Pending formal audit |
| D | Software semantic consistency | Pending formal audit |
| E | Hand-calculated reference evidence | Pending GRP-001 through GRP-006 |
| F | Boundary and failure analysis | Pending formal audit |

Approval requires explicit evidence for all six gates. Completion of this Markdown file alone is not approval.

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
