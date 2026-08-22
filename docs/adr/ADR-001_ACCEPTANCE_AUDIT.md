# ADR-001 — Acceptance Audit

- **ADR:** `ADR-001-coordinate-direction-spatial-conventions.md`
- **Phase:** 0C — Scientific Foundations
- **Audit status:** In progress
- **Purpose:** Preserve explicit evidence for acceptance Gates A–F without conflating draft completion with scientific approval.

## Gate Status Summary

| Gate | Requirement | Status |
|---|---|---|
| A | Physical consistency | PASS |
| B | Mathematical consistency | PASS |
| C | Dimensional and unit consistency | PASS |
| D | Software semantic consistency | Pending |
| E | Hand-calculated reference evidence | Pending |
| F | Boundary and failure analysis | Pending |

## Gate A — Physical Consistency

### A.1 Audit question

Does ADR-001 represent a physically self-consistent ideal 1-D array embedded in 3-D propagation space, with coherent definitions of direction, propagation delay, spatial phase, reference choice, and observability?

### A.2 Findings that pass

1. **Geometry dimension versus propagation-space dimension — PASS.** A one-dimensional array may be embedded in three-dimensional propagation space. The ideal scalar linear-array geometry observes only the projection of the source look direction onto the array axis.
2. **3-D broadside set versus canonical 2-D slice — PASS.** For an array on the `x` axis, the 3-D broadside set is `u_x = 0`; the `+y` direction is correctly treated as a chosen reference broadside direction only within the selected canonical `xy` slice.
3. **Look direction versus propagation direction — PASS.** Defining `u_hat` from array to source and incident propagation as `-u_hat` is physically coherent.
4. **Delay-to-phase derivation — PASS.** With temporal convention `exp(-j omega t)`, the first-order far-field delay relation produces the declared negative spatial exponent.
5. **Translation invariance — PASS.** Translating the geometry and spatial phase reference together leaves the relative manifold unchanged.
6. **Physical coordinates and channel identity — PASS.** Physical coordinates and stable channel identity are preserved while sorting and canonicalization remain derived views.
7. **Physical units and wavelength normalization — PASS.** Positions remain physical SI quantities; wavelength-normalized coordinates remain frequency/medium-dependent derived quantities.
8. **Lattice semantics versus physical uncertainty — PASS.** Numerical lattice tolerance is distinguished from physical position uncertainty.
9. **Direction cosine and projected spatial frequency — PASS.** `u_x`, `kappa_x`, and normalized spatial frequency remain distinct.
10. **Projection ambiguity versus spatial aliasing — PASS.** The two mechanisms remain explicitly separated.

### A.3 Finding A-001 — Stable default spatial phase reference — RESOLVED

The default analytical reference is the centroid of the declared nominal geometry rather than the active subset. Channel masking therefore does not silently rephase the default manifold.

**Resolution status: PASS.**

### A.4 Finding A-002 — Half-wavelength endpoint ambiguity — RESOLVED

The ADR distinguishes the usual no-grating-lobe condition on the open visible interval from strict injectivity on the closed interval. The `Delta = lambda/2`, `u = ±1` endpoint equivalence is explicit.

**Resolution status: PASS.**

### A.5 Finding A-003 — Nominal versus true phase center — RESOLVED

`r_n` is the declared nominal sensor phase-center/reference position used by the geometry model. Frequency-, angle-, environment-, installation-, or calibration-dependent departures are deferred to ADR-003.

**Resolution status: PASS.**

### A.6 Finding A-004 — Complete canonical frame orientation — RESOLVED

A purely 1-D geometry does not physically determine rotation about the array axis. `+y` is a chosen canonical broadside reference and `+z = +x × +y` completes the right-handed frame.

**Resolution status: PASS.**

### A.7 Gate A decision

**Gate A status: PASS.**

The re-audited ADR-001 is physically self-consistent within its declared ideal geometry-only scope.

---

## Gate B — Mathematical Consistency

### B.1 Audit question

Are the coordinate mappings, far-field expansion, delay/phase signs, reference transformations, lattice relations, spatial-frequency mappings, periodicity statements, and injectivity/ambiguity conditions mathematically self-consistent?

### B.2 Findings that pass

1. **Canonical direction parameterization — PASS.** On `theta in [-pi/2, pi/2]`, `u_hat(theta) = [sin(theta), cos(theta), 0]^T` has unit norm and `u = sin(theta)` is one-to-one with inverse `theta = arcsin(u)`.
2. **Far-field first-order expansion — PASS after correction.** The derivation now introduces an explicit localization/expansion origin `r_0`, writes `r_s = r_0 + R u_hat`, and shows that `r_0` cancels from the final relative-distance relation.
3. **Delay-to-phase sign chain — PASS.** Under `exp(-j omega t)`, delay contributes `exp(+j omega Delta tau)` and therefore produces the declared negative receive spatial exponent after substitution.
4. **Translation invariance — PASS.** Translating sensor positions and phase reference together leaves the manifold unchanged; translating only the sensor positions multiplies it by a common phasor `exp[-j k t^T u_hat]`.
5. **Phase-reference transformation law — PASS after correction.** Changing the phase reference from `r_ref` to `r_ref'` multiplies the manifold by a common phasor.
6. **Direction-cosine and spatial-frequency mapping — PASS.** `u`, `kappa_x = k u`, and `psi = kappa_x Delta` are mutually consistent under their declared context.
7. **Noninteger phase-reference lattice coordinate — PASS after correction.** `mu_ref = (x_ref-x_L)/Delta` is real-valued, so the reference need not lie on a lattice point.
8. **Tolerance-admitted lattice algebra — PASS after correction.** Exact grid-reconstructed positions are distinguished from authoritative coordinates and the residual bound is preserved.
9. **Primitive lattice reduction — PASS after clarification.** Relative-index gcd reduction gives primitive indices and primitive spacing `Delta_prim = g Delta`.
10. **Reference-invariant manifold equivalence — PASS after correction.** Spatial equivalence is defined up to a common phase with an invariant pair-difference criterion.
11. **Fundamental lattice periodicity — PASS after correction.** The declared-grid fundamental period is `2 pi/g`; the primitive-grid period is `2 pi`.
12. **Half-wavelength endpoint statement — PASS.** The open-interval and closed-interval injectivity statements are distinguished.
13. **Projection ambiguity versus sampling aliasing — PASS.** The two mathematical equivalence mechanisms remain distinct.

### B.3 Finding B-001 — Expansion origin/reference conflation — RESOLVED

The ADR now introduces `r_0` explicitly and proves its cancellation in the relative-distance relation.

**Resolution status: PASS.**

### B.4 Finding B-002 — Tolerance versus exact lattice equality — RESOLVED

Authoritative coordinates and reconstructed grid positions are now distinguished, with explicit residual terms and bounds.

**Resolution status: PASS.**

### B.5 Finding B-003 — Noninteger phase-reference lattice coordinate — RESOLVED

The geometry centroid generally need not coincide with a lattice point. ADR-001 now uses real-valued `mu_ref`.

**Resolution status: PASS.**

### B.6 Finding B-004 — Fundamental periodicity of sparse integer geometries — RESOLVED

The ADR now distinguishes a valid `2 pi` periodicity from the potentially smaller fundamental period `2 pi/g` in declared-grid coordinates.

**Resolution status: PASS.**

### B.7 Finding B-005 — Exact vector equality versus projective manifold equivalence — RESOLVED

Spatial indistinguishability is now defined by common-phase equivalence and the reference-invariant pair-difference criterion.

**Resolution status: PASS.**

### B.8 Gate B decision

**Gate B status: PASS.**

No unresolved mathematical contradiction remains in the relations governed by ADR-001.

---

## Gate C — Dimensional and Unit Consistency

### C.1 Audit question

Are all physical quantities, normalized quantities, angular quantities, lattice quantities, and transcendental-function arguments dimensionally consistent, with explicit canonical units and no hidden degree/radian or physical/normalized-unit ambiguity?

### C.2 Canonical dimensional inventory — PASS

The re-audited ADR now makes the dimensional inventory explicit:

- positions, distances, wavelength, aperture, lattice spacings, and physical residuals: `m`;
- frequency `f`: `Hz = s^-1`;
- temporal angular frequency `omega`: semantic `rad/s`;
- propagation speed `v_p`: `m/s`;
- time and delay: `s`;
- angle and phase: semantic `rad`;
- wavenumber `k` and projected angular spatial frequency `kappa_x`: semantic `rad/m`;
- normalized lattice spatial frequency `psi`: semantic `rad` per unit dimensionless lattice-index increment;
- direction cosine, normalized position, lattice coordinates/residuals/tolerance, reference lattice coordinate, integer indices/lags, and gcd factors: dimensionless;
- ideal steering coefficients: dimensionless complex coefficients.

Radians are SI-dimensionless but are retained as semantic unit labels so angular quantities are not confused with arbitrary scalars or cyclic frequency.

### C.3 Wavelength relation — PASS

```math
\lambda=\frac{v_p}{f}
```

has dimensions

```text
(m/s)/(1/s)=m.
```

### C.4 Delay relation — PASS

```math
\Delta\tau_n
=
-\frac{(\mathbf r_n-\mathbf r_{\mathrm{ref}})^T\hat{\mathbf u}}{v_p}
```

has dimensions

```text
m / (m/s) = s.
```

### C.5 Temporal phase argument — PASS

`omega Delta tau` has semantic units

```text
(rad/s) * s = rad,
```

and is SI-dimensionless, as required by `exp()`.

### C.6 Wavenumber and spatial phase — PASS

```math
k=\frac{\omega}{v_p}=\frac{2\pi}{\lambda}
```

has semantic units `rad/m`. Therefore

```math
k(\mathbf r_n-\mathbf r_{\mathrm{ref}})^T\hat{\mathbf u}
```

has semantic units `rad` and is a valid exponential argument.

### C.7 Direction cosine and wavelength-normalized position — PASS

`u = u_hat dot x_hat` is dimensionless. Likewise

```math
q_n=\frac{x_n-x_{\mathrm{ref}}}{\lambda}
```

is dimensionless.

### C.8 Projected angular spatial frequency — PASS

```math
\kappa_x=ku=\frac{2\pi}{\lambda}u
```

has semantic units `rad/m`. Hence `kappa_x (x_n-x_ref)` is a phase in radians and is SI-dimensionless.

### C.9 Normalized lattice spatial frequency — PASS after semantic tightening

```math
\psi=\kappa_x\Delta
```

has semantic units `rad`. It represents phase increment per one-unit change of the dimensionless lattice index. The ADR now states this explicitly instead of leaving `psi` as an unlabeled dimensionless number.

**Resolution status: PASS.**

### C.10 Lattice normalized residual versus physical residual — PASS after tightening

```math
z_n=\frac{x_n-x_L}{\Delta},
\qquad
\varepsilon_n=z_n-m_n,
\qquad
\rho_n=|\varepsilon_n|
```

are dimensionless. The numerical tolerance `tau_lat` is also dimensionless.

The ADR now separately defines

```math
\eta_n=x_n-\tilde x_n=\varepsilon_n\Delta,
```

which has units `m`, with

```math
|\eta_n|\le\tau_{\mathrm{lat}}\Delta.
```

This prevents normalized numerical residual from being confused with a physical distance error.

**Resolution status: PASS.**

### C.11 Pair-difference residual bound — PASS

```math
|(x_i-x_j)-\ell_{ij}\Delta|
\le
2\tau_{\mathrm{lat}}\Delta
```

has meters on both sides.

### C.12 Primitive-lattice quantities — PASS

`m_n`, `m_0`, `d_n`, `g`, and primitive integer indices are dimensionless; `Delta` and `Delta_prim = g Delta` are meters.

### C.13 Reference lattice coordinate — PASS

```math
\mu_{\mathrm{ref}}=\frac{x_{\mathrm{ref}}-x_L}{\Delta}
```

is real-valued and dimensionless. Therefore `(m_n-mu_ref) psi` is a phase in radians and a valid exponential argument.

### C.14 Alias criterion — PASS

```math
k(x_i-x_j)(u_2-u_1)\in2\pi\mathbb Z
```

has semantic units of radians on the left and right, with both SI-dimensionless.

### C.15 Angle-grid derivative — PASS after clarification

```math
\frac{du}{d\theta}=\cos\theta
```

assumes `theta` is expressed in radians. The ADR now explicitly prohibits silent substitution of degree-valued numerical inputs into this differential relation.

### C.16 Gate C decision

**Gate C status: PASS.**

No unresolved dimensional inconsistency remains in ADR-001. Physical SI quantities, normalized dimensionless quantities, integer/grid quantities, and semantic angular quantities are explicitly separated. Every declared exponential and trigonometric argument is dimensionally valid, and degree/radian conversion is constrained to explicit boundaries.

Gate C does not imply software-semantic, Golden Reference, or boundary/failure acceptance. Gates D–F remain independent and pending.
