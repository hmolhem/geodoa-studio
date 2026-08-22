# ADR-001 — Acceptance Audit

- **ADR:** `ADR-001-coordinate-direction-spatial-conventions.md`
- **Phase:** 0C — Scientific Foundations
- **Audit status:** In progress
- **Purpose:** Preserve explicit evidence for acceptance Gates A–F without conflating draft completion with scientific approval.

## Gate Status Summary

| Gate | Requirement | Status |
|---|---|---|
| A | Physical consistency | PASS |
| B | Mathematical consistency | Pending |
| C | Dimensional and unit consistency | Pending |
| D | Software semantic consistency | Pending |
| E | Hand-calculated reference evidence | Pending |
| F | Boundary and failure analysis | Pending |

## Gate A — Physical Consistency

### A.1 Audit question

Does ADR-001 represent a physically self-consistent ideal 1-D array embedded in 3-D propagation space, with coherent definitions of direction, propagation delay, spatial phase, reference choice, and observability?

### A.2 Findings that pass

1. **Geometry dimension versus propagation-space dimension — PASS.**
   A one-dimensional array may be embedded in three-dimensional propagation space. The ideal scalar linear-array geometry observes only the projection of the source look direction onto the array axis.

2. **3-D broadside set versus canonical 2-D slice — PASS.**
   For an array on the `x` axis, the 3-D broadside set is `u_x = 0`; the `+y` direction is correctly treated as a chosen reference broadside direction only within the selected canonical `xy` slice.

3. **Look direction versus propagation direction — PASS.**
   Defining `u_hat` from array to source and incident propagation as `-u_hat` is physically coherent.

4. **Delay-to-phase derivation — PASS.**
   With temporal convention `exp(-j omega t)`, the first-order far-field delay relation

   ```math
   \Delta\tau_n
   \approx
   -\frac{(\mathbf r_n-\mathbf r_{\mathrm{ref}})^T\hat{\mathbf u}}{v_p}
   ```

   produces the receive coefficient

   ```math
   a_n
   =
   \exp\!\left[-jk(\mathbf r_n-\mathbf r_{\mathrm{ref}})^T\hat{\mathbf u}\right].
   ```

   The steering-vector phase sign therefore follows from the declared physical conventions rather than an arbitrary software preference.

5. **Translation invariance — PASS.**
   Translating the geometry and the spatial phase reference together leaves the relative manifold unchanged. Holding the reference fixed introduces only a common direction-dependent phase factor across channels.

6. **Physical coordinates and channel identity — PASS.**
   Preserving physical coordinates and stable channel identity while treating sorting, translation normalization, and reflection comparison as derived views is physically appropriate and necessary for later calibration and hardware-channel provenance.

7. **Physical units and wavelength normalization — PASS.**
   Storing physical positions in meters and treating wavelength-normalized coordinates as frequency/medium-dependent derived quantities is physically consistent.

8. **Lattice semantics versus physical uncertainty — PASS.**
   Numerical lattice-alignment tolerance is correctly distinguished from physical position uncertainty. Integer coarray lags are physically meaningful only after a lattice relation has been established.

9. **Direction cosine and projected spatial frequency — PASS.**
   `u_x`, `kappa_x = k u_x`, and lattice-normalized `psi = kappa_x Delta` correctly represent distinct levels of the spatial model.

10. **Projection ambiguity versus spatial aliasing — PASS.**
    The ADR correctly treats loss of 3-D directional information caused by 1-D projection as different from aliasing caused by spatial sampling.

### A.3 Finding A-001 — Stable default spatial phase reference — RESOLVED

The original draft used the centroid of the active sensor subset as the default phase reference. This was physically legal but would have caused the default reference to move whenever the active-channel mask changed.

ADR-001 now defines the analytical default as the centroid of the **declared nominal geometry**, not the active subset. The contract explicitly distinguishes:

```text
geometry coordinate origin
spatial phase reference
active-channel mask
```

Channel masking no longer silently changes the default phase reference. Explicit overrides remain allowed when declared as configuration/provenance.

**Resolution status: PASS.**

### A.4 Finding A-002 — Half-wavelength endpoint ambiguity — RESOLVED

ADR-001 now distinguishes the usual no-grating-lobe statement over the open visible interval from strict injectivity over the closed interval.

At

```math
\Delta=\frac{\lambda}{2},
```

`u = +1` and `u = -1` produce `psi = +pi` and `psi = -pi`, which are identical for integer lattice samples:

```math
\exp(-jm\pi)=\exp(+jm\pi).
```

ADR-001 therefore states:

- `Delta <= lambda/2` for the usual no-grating-lobe condition within the open visible interval;
- endpoint ambiguity remains at equality;
- strict injectivity over closed `u in [-1,1]` requires `Delta < lambda/2`.

**Resolution status: PASS.**

### A.5 Finding A-003 — Nominal versus true phase center — RESOLVED

`r_n` is now defined as the **declared nominal sensor phase-center/reference position used by the geometry model**, rather than as an immutable true electromagnetic phase center.

Frequency-, angle-, environment-, installation-, or calibration-dependent deviations are explicitly deferred to ADR-003.

**Resolution status: PASS.**

### A.6 Finding A-004 — Complete canonical frame orientation — RESOLVED

ADR-001 now states that a purely 1-D geometry does not physically determine rotation about its array axis. GeoDOA therefore chooses `+y` as the canonical reference broadside axis, with `+z = +x × +y` completing the right-handed frame.

Any platform/global-to-local transform must remain explicit and provenance-preserving.

**Resolution status: PASS.**

### A.7 Gate A decision

**Gate A status: PASS.**

The re-audited ADR-001 is physically self-consistent within its declared ideal geometry-only scope. No unresolved physical contradiction remains in the coordinate, direction, relative-delay, receive-phase, stable-reference, lattice, or ambiguity conventions governed by ADR-001.

Gate A does not imply mathematical, dimensional, software-semantic, reference-evidence, or failure-boundary acceptance. Gates B–F remain independent and pending.
