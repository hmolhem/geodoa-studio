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
| C | Dimensional and unit consistency | Pending |
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

5. **Phase-reference transformation law — PASS after correction.** Changing the phase reference from `r_ref` to `r_ref'` multiplies the manifold by the common phasor

   ```math
   \exp\!\left[+jk(\mathbf r_{\mathrm{ref}'}-\mathbf r_{\mathrm{ref}})^T\hat{\mathbf u}\right].
   ```

6. **Direction-cosine and spatial-frequency mapping — PASS.** `u`, `kappa_x = k u`, and `psi = kappa_x Delta` are mutually consistent under their declared context.

7. **Noninteger phase-reference lattice coordinate — PASS after correction.** `mu_ref = (x_ref-x_L)/Delta` is real-valued, so the reference need not lie on a lattice point. The exact-grid representation `a_n = exp[-j(m_n-mu_ref) psi]` is valid.

8. **Tolerance-admitted lattice algebra — PASS after correction.** Exact grid-reconstructed positions `tilde x_n = x_L + m_n Delta` are distinguished from authoritative coordinates `x_n = x_L + (m_n + epsilon_n) Delta`, and the pair-difference residual satisfies

   ```math
   |(x_i-x_j)-\ell_{ij}\Delta|\le 2\tau_{\mathrm{lat}}\Delta.
   ```

9. **Primitive lattice reduction — PASS after clarification.** For relative integer indices `d_n = m_n-m_0`, the gcd `g` yields primitive indices `(m_n-m_0)/g` and primitive spacing `Delta_prim = g Delta`.

10. **Reference-invariant manifold equivalence — PASS after correction.** Spatial equivalence is defined up to a common phase, `a(u_2) = exp(j phi) a(u_1)`, with the equivalent pair-difference criterion

   ```math
   k(x_i-x_j)(u_2-u_1)\in2\pi\mathbb Z.
   ```

11. **Fundamental lattice periodicity — PASS after correction.** For an exact integer lattice with relative-index gcd `g`, the fundamental period in declared-grid `psi` is `2 pi / g`; using the primitive spacing gives primitive normalized frequency with fundamental period `2 pi`.

12. **Half-wavelength endpoint statement — PASS.** For a consecutive-index ULA, `Delta <= lambda/2` avoids distinct grating-lobe replicas in the open visible interval; equality leaves the two endfire endpoints equivalent, so strict injectivity on the closed interval requires `Delta < lambda/2`.

13. **Projection ambiguity versus sampling aliasing — PASS.** Equal `u_x` from physically distinct 3-D directions and equal relative manifolds from distinct observable `u` values are represented as different mathematical equivalence mechanisms.

### B.3 Finding B-001 — Expansion origin/reference conflation — RESOLVED

The earlier draft implicitly tied the distant-source expansion to the coordinate origin while describing look direction relative to an array reference. ADR-001 now introduces `r_0` explicitly and proves its cancellation in the relative-distance relation.

**Resolution status: PASS.**

### B.4 Finding B-002 — Tolerance versus exact lattice equality — RESOLVED

The earlier draft accepted coordinates within numerical tolerance but then used an exact pair-difference equality. ADR-001 now distinguishes authoritative coordinates from reconstructed grid positions and preserves the residual term and bound.

**Resolution status: PASS.**

### B.5 Finding B-003 — Noninteger phase-reference lattice coordinate — RESOLVED

The geometry centroid generally need not coincide with a lattice point. ADR-001 now uses real-valued `mu_ref` rather than implying an integer `m_ref` is always available.

**Resolution status: PASS.**

### B.6 Finding B-004 — Fundamental periodicity of sparse integer geometries — RESOLVED

The earlier `2 pi` periodicity statement was valid but not necessarily fundamental. ADR-001 now derives the fundamental declared-grid period `2 pi/g` and the equivalent primitive-grid representation.

**Resolution status: PASS.**

### B.7 Finding B-005 — Exact vector equality versus projective manifold equivalence — RESOLVED

Exact steering-vector equality is reference-dependent because a phase-reference change introduces a common phasor. ADR-001 now uses common-phase equivalence and the invariant pair-difference criterion for spatial indistinguishability.

**Resolution status: PASS.**

### B.8 Gate B decision

**Gate B status: PASS.**

After correction and re-audit, no unresolved mathematical contradiction remains in the coordinate parameterization, relative-distance expansion, temporal/spatial phase sign chain, reference transformations, lattice residual algebra, primitive-lattice reduction, spatial-frequency mapping, manifold-equivalence criterion, or aliasing/injectivity statements governed by ADR-001.

Gate B does not imply dimensional/unit, software-semantic, Golden Reference, or boundary/failure acceptance. Gates C–F remain independent and pending.
