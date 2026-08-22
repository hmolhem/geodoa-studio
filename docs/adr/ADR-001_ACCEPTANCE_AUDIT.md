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
| D | Software semantic consistency | PASS |
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
5. **Phase-reference transformation law — PASS after correction.** Changing the phase reference multiplies the manifold by a common phasor.
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

The ADR explicitly separates physical SI quantities, semantic angular quantities, dimensionless normalized quantities, integer/grid quantities, and dimensionless complex manifold coefficients.

### C.3 Wavelength relation — PASS

`lambda = v_p/f` has dimensions `(m/s)/(1/s)=m`.

### C.4 Delay relation — PASS

The relative-distance projection divided by `v_p` has units of seconds.

### C.5 Temporal phase argument — PASS

`omega Delta tau` has semantic units radians and is SI-dimensionless, as required by `exp()`.

### C.6 Wavenumber and spatial phase — PASS

`k = omega/v_p = 2 pi/lambda` has semantic units `rad/m`; multiplying by projected distance yields a phase in radians.

### C.7 Direction cosine and wavelength-normalized position — PASS

Both `u` and `q_n` are dimensionless.

### C.8 Projected angular spatial frequency — PASS

`kappa_x = k u` has semantic units `rad/m`.

### C.9 Normalized lattice spatial frequency — PASS after semantic tightening

`psi = kappa_x Delta` is SI-dimensionless but semantically a phase increment in radians per unit lattice-index increment.

### C.10 Lattice normalized residual versus physical residual — PASS after tightening

`epsilon_n`, `rho_n`, and `tau_lat` are dimensionless; `eta_n = epsilon_n Delta` is a physical residual in meters.

### C.11 Pair-difference residual bound — PASS

Both sides of the residual bound have units of meters.

### C.12 Primitive-lattice quantities — PASS

Integer/gcd quantities are dimensionless; declared and primitive spacings are meters.

### C.13 Reference lattice coordinate — PASS

`mu_ref` is real-valued and dimensionless.

### C.14 Alias criterion — PASS

The pair-difference alias phase criterion is dimensionally valid.

### C.15 Angle-grid derivative — PASS after clarification

The derivative `du/dtheta = cos(theta)` assumes internal radian representation; degree-valued boundaries require conversion.

### C.16 Gate C decision

**Gate C status: PASS.**

No unresolved dimensional inconsistency remains in ADR-001.

---

## Gate D — Software Semantic Consistency

### D.1 Audit question

Can every scientific distinction in ADR-001 map into the GeoDOA domain architecture without hidden unit inference, silent convention switching, destructive canonicalization, duplicated authoritative state, identity loss, or implementation-specific reinterpretation?

### D.2 Cross-document architecture compatibility — PASS after clarification

The Master Start Handoff defines a clean/domain-centric architecture with immutable domain entities, typed value objects, pure numerical kernels, replaceable behavior contracts, boundary validation, and typed results. ADR-001 is compatible with that architecture after making the following semantic responsibilities explicit:

- `LinearArrayGeometry` represents intrinsic 1-D physical geometry and stable channel identity;
- `ReferenceFrame1D`-style semantics embed that 1-D geometry into 3-D propagation space;
- `AngleConvention`-style semantics belong at configuration/import boundaries rather than altering canonical scientific-kernel behavior;
- `ManifoldProvider` consumes canonical validated geometry/direction/wave context and returns a typed result;
- coarray consumers require validated lattice semantics rather than raw-coordinate rounding.

### D.3 Finding D-001 — Intrinsic 1-D geometry versus embedded 3-D positions — RESOLVED

The Master Start Handoff describes the initial geometry domain as one-dimensional, while the physical manifold derivation uses 3-D vectors `r_n`. Storing independent authoritative 1-D and 3-D coordinate tables would create duplicated state that could diverge.

ADR-001 now states that the authoritative linear geometry contains intrinsic coordinates `x_n` plus stable channel identity, while a `ReferenceFrame1D`-style object provides the explicit spatial embedding

```math
\mathbf r_n=\mathbf r_{\mathrm{origin}}+x_n\hat{\mathbf x}.
```

External/global 3-D coordinates require an explicit transform/import relation rather than silent projection.

**Resolution status: PASS.**

### D.4 Finding D-002 — Angle convention boundary versus canonical core — RESOLVED

A configurable `AngleConvention` can be useful for file/UI/import compatibility, but allowing every estimator or kernel to interpret raw numeric angles under its own convention would violate the project-wide scientific contract.

ADR-001 now requires explicit conversion at validated boundaries to the canonical internal representation. Scientific kernels operate on canonical radians, direction cosines, or validated unit look vectors and do not infer angle semantics from UI labels.

**Resolution status: PASS.**

### D.5 Finding D-003 — Stable channel identity versus ordering/masking — RESOLVED

ADR-001 now distinguishes persistent channel identity from authoritative sequence order, sorted geometric order, and active-channel selection. Sorting and masking are derived views/configurations and may not renumber or delete physical identities in the authoritative geometry.

**Resolution status: PASS.**

### D.6 Finding D-004 — Active mask versus geometry mutation/reference mutation — RESOLVED

An active-channel mask is a processing view/configuration over the declared geometry. It does not mutate the geometry, recompute the default geometry-level phase reference, or silently create a new physical array identity.

A genuine hardware/physical-array change creates a new geometry/configuration identity.

**Resolution status: PASS.**

### D.7 Finding D-005 — Lattice declaration versus lattice validation evidence — RESOLVED

A declared lattice records design/provenance semantics. A lattice-validation result records whether authoritative coordinates satisfy a candidate/declared lattice under a tolerance and preserves residuals/diagnostics.

ADR-001 now requires downstream integer-lag consumers to receive validated lattice semantics or exact-by-construction generator provenance. They may not independently reconstruct integer lags by rounding raw coordinates.

**Resolution status: PASS.**

### D.8 Finding D-006 — Derived geometry views versus authoritative state — RESOLVED

Sorting, translation normalization, reflection comparison, primitive-lattice reduction, wavelength normalization, and scan-domain conversion are explicit derived operations. They preserve source identity/transformation metadata and may not silently mutate authoritative geometry/configuration.

**Resolution status: PASS.**

### D.9 Finding D-007 — Direction-domain type ambiguity — RESOLVED

Angle, direction cosine, 3-D unit look direction, projected spatial angular frequency, and declared/primitive-grid phase increments are mathematically related but semantically distinct. ADR-001 now requires explicit value/grid semantics and conversions rather than an unlabeled scalar or array whose meaning depends on caller convention.

**Resolution status: PASS.**

### D.10 Finding D-008 — Scan-grid semantic loss — RESOLVED

A scan grid must preserve whether it is uniform in angle, direction cosine, `kappa_x`, declared-grid `psi`, or primitive-grid frequency. Conversion creates a derived grid/view and retains the context needed to interpret output.

**Resolution status: PASS.**

### D.11 Finding D-009 — Manifold/result provenance — RESOLVED

A complex manifold vector alone is not a sufficient high-level scientific result. The domain/application result contract must retain enough frame, phase-reference, direction/convention, active-channel, frequency/medium, and provenance context to interpret or compare it correctly. Pure low-level kernels may remain NumPy-oriented after canonicalization.

**Resolution status: PASS.**

### D.12 Finding D-010 — Ambiguity diagnostic versus silent canonicalization — RESOLVED

Projection ambiguity, spatial aliasing, reflection equivalence, or common-phase manifold equivalence may be reported through diagnostics/results. They must not silently collapse user-requested directions or geometries into a representative value without preserving the original values and the transformation/equivalence rationale.

**Resolution status: PASS.**

### D.13 ADR-numbering reconciliation — PASS

The Master Start Handoff contained preliminary recommended ADR numbers before the Phase 0C scientific decomposition was complete. The Phase 0C roadmap now explicitly records that ADR-001 through ADR-004 are the authoritative scientific numbering and that architecture/run-identity/GUI/fairness decisions retain their subject matter but will receive later non-conflicting identifiers.

This prevents two documents from assigning different meanings to the same ADR number.

### D.14 Domain mapping summary — PASS

ADR-001 now requires semantic roles for:

```text
LinearArrayGeometry-style intrinsic geometry
ReferenceFrame1D-style 3-D embedding
AngleConvention-style boundary conversion
validated 3-D look direction
explicit phase-reference value/policy
WaveParameters-style frequency/speed context
lattice declaration
lattice validation result
active-channel view/mask
sorted/normalized/reflected derived views
angle/u/kappa/psi typed scan domains
typed manifold result
ambiguity/equivalence diagnostic result
```

Exact Python class names remain an implementation-level decision. The gate requires semantic separability, not premature class proliferation.

### D.15 Pure numerical kernel compatibility — PASS

The semantic requirements do not force numerical kernels to manipulate heavyweight domain objects. Boundary/application/domain layers may validate and convert to canonical NumPy arrays/scalars, call pure numerical kernels, and then package outputs into typed results with preserved metadata.

This is consistent with the Master Start Handoff's object-oriented-without-class-inflation principle.

### D.16 Forbidden implicit behavior audit — PASS

ADR-001 now explicitly prohibits silent:

- unit guessing;
- degree/radian reinterpretation;
- origin shifting;
- reference-channel selection after sorting;
- active-mask reference recomputation;
- channel identity mutation;
- wavelength normalization as physical-state replacement;
- lattice snapping;
- physical-uncertainty/tolerance conflation;
- integer coarray manufacture by rounding;
- angle/u/kappa/psi semantic collapse;
- declared/primitive-grid ambiguity;
- reflection/alias canonicalization;
- common-phase-factor misclassification as physical manifold distortion.

### D.17 Gate D decision

**Gate D status: PASS.**

After cross-document reconciliation, ADR-001 maps cleanly to the GeoDOA layered/domain architecture without requiring duplicated authoritative geometry state, hidden convention switches, destructive derived views, unlabeled scientific arrays at public boundaries, or downstream reconstruction of scientific semantics.

Gate D does not imply Golden Reference or boundary/failure acceptance. Gates E and F remain independent and pending.
