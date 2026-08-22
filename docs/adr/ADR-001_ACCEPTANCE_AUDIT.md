# ADR-001 — Acceptance Audit

- **ADR:** `ADR-001-coordinate-direction-spatial-conventions.md`
- **Phase:** 0C — Scientific Foundations
- **Audit status:** In progress
- **Purpose:** Preserve explicit evidence for acceptance Gates A–F without conflating draft completion with scientific approval.

## Gate Status Summary

| Gate | Requirement | Status |
|---|---|---|
| A | Physical consistency | CONDITIONAL — corrections required |
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
   For an array on the `x` axis, the 3-D broadside set is `u_x = 0`; the `+y` direction is correctly treated as a reference broadside direction only within the selected canonical `xy` slice.

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

10. **Projection ambiguity versus spatial aliasing — PASS in principle.**
    The ADR correctly treats loss of 3-D directional information caused by 1-D projection as different from aliasing caused by spatial sampling.

### A.3 Required correction A-001 — Stable default spatial phase reference

Current draft defines the standard analytical default phase reference as the centroid of the **active** sensor phase centers.

This is physically legal but undesirable as the default project contract because changing an active-channel mask changes the reference point even though the underlying physical array coordinate frame has not changed. The resulting manifold is rephased by a direction-dependent common factor. That factor is harmless for many relative-phase DOA calculations, but it complicates direct manifold comparison, calibration provenance, coherent-source conventions, and cross-run reproducibility.

**Required correction:** define the default analytical spatial phase reference as a stable geometry-level reference that does not change merely because channels are disabled. A suitable baseline is the centroid of the declared nominal physical geometry, computed from the full geometry definition and preserved as geometry metadata. Active-channel processing may use the same fixed reference. Explicit calibration or measurement workflows may override the default with a named reference channel or another declared spatial point.

The ADR should explicitly distinguish:

```text
geometry coordinate origin
spatial phase reference
active-channel mask
```

Changing the active-channel mask must not silently redefine the default phase reference.

### A.4 Required correction A-002 — Half-wavelength endpoint ambiguity

The current draft states that, for a conventional ULA with primitive spacing `Delta`, the full visible `u` interval maps inside the principal spatial-frequency interval when

```math
\Delta\le\frac{\lambda}{2}.
```

This requires a boundary clarification. At exactly

```math
\Delta=\frac{\lambda}{2},
```

the two closed-interval endfire coordinates `u = +1` and `u = -1` produce `psi = +pi` and `psi = -pi`, which are identical on an integer lattice:

```math
\exp(-j m \pi)=\exp(+j m \pi),
\qquad m\in\mathbb Z.
```

Therefore:

- `Delta <= lambda/2` is appropriate for the usual statement that no distinct grating-lobe replica occurs in the **open** visible interval;
- at equality, the two endfire endpoints remain aliased;
- strict injectivity over the **closed** `u in [-1,1]` interval requires `Delta < lambda/2`.

**Required correction:** state this endpoint condition explicitly so that GeoDOA does not later label the `Delta = lambda/2`, `u = ±1` case as strictly unambiguous.

### A.5 Required clarification A-003 — Nominal phase center versus true electromagnetic phase center

The draft calls `r_n` the physical phase-center position associated with channel `n`. For the ideal geometry contract this should be tightened to avoid implying that a real antenna element has one immutable phase center under all frequency, angle, loading, and platform conditions.

**Required clarification:** ADR-001 should define `r_n` as the **declared nominal sensor phase-center/reference position used by the geometry model**. Frequency-, angle-, environment-, or calibration-dependent deviations from that nominal representation belong to ADR-003 and the true/calibrated manifold model.

This preserves the usefulness of a clean geometry coordinate without overclaiming physical exactness.

### A.6 Required clarification A-004 — Complete canonical frame orientation

The draft declares a right-handed local frame with the array axis along `+x` and later chooses `+y` as the canonical broadside reference in the `xy` slice. For a 1-D array, rotation about the array axis is not determined by geometry alone.

**Required clarification:** state explicitly that `+y` is a **chosen canonical reference broadside axis**, not a direction physically determined by the 1-D geometry, and that `+z` completes the right-handed frame. Any mapping from a global/platform frame into this local canonical frame must be explicit and provenance-preserving.

### A.7 Gate A decision

**Gate A status: CONDITIONAL — NOT YET PASS.**

The core physical model is sound. No fundamental steering-vector or direction-sign error was found. Gate A can become PASS after corrections A-001 and A-002 and clarifications A-003 and A-004 are incorporated into ADR-001 and re-audited.

No later acceptance gate is automatically implied by Gate A; Gates B–F remain independent audits.
