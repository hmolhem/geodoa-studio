# ADR-001 — Final Acceptance Record

- **ADR:** `ADR-001-coordinate-direction-spatial-conventions.md`
- **Phase:** 0C — Scientific Foundations
- **Final status:** ACCEPTED
- **Acceptance date:** 2026-08-22
- **Purpose:** Final reconciliation of ADR-001 scientific acceptance evidence after Gates A–F.

## 1. Acceptance Decision

ADR-001 — Coordinate, Direction, and Spatial Conventions is **ACCEPTED** as the authoritative GeoDOA scientific contract for its declared scope.

All six Phase 0C acceptance gates have passed:

| Gate | Requirement | Final Status | Primary Evidence |
|---|---|---|---|
| A | Physical consistency | PASS | `ADR-001_ACCEPTANCE_AUDIT.md` |
| B | Mathematical consistency | PASS | `ADR-001_ACCEPTANCE_AUDIT.md` |
| C | Dimensional and unit consistency | PASS | `ADR-001_ACCEPTANCE_AUDIT.md` |
| D | Software semantic consistency | PASS | `ADR-001_ACCEPTANCE_AUDIT.md` |
| E | Hand-calculated reference evidence | PASS | `../science/golden_reference/ADR-001_GOLDEN_REFERENCE_PROBLEMS.md` |
| F | Boundary and failure analysis | PASS | `ADR-001_BOUNDARY_FAILURE_ANALYSIS.md` |

The earlier `ADR-001_ACCEPTANCE_AUDIT.md` remains preserved as the detailed progressive audit record for Gates A–E and the pre-reconciliation state of Gate F. This final record supersedes only its **status summary**, not its historical findings or evidence.

## 2. Gate F Reconciliation

Gate F identified one material normative constraint that was not yet present in the governing ADR:

```math
0\le\tau_{\mathrm{lat}}<\frac12.
```

This constraint has now been incorporated into ADR-001.

The bound is required because nearest-integer lattice validation becomes non-unique at a half-grid tie. The scientific contract therefore excludes `tau_lat >= 0.5` independently of any programming-language-specific rounding rule.

After this correction, no unresolved Gate F finding remains.

**Gate F final status: PASS.**

## 3. Cross-Gate Consistency Check

The final reconciliation checked the Gate F constraint and boundary taxonomy against the previously accepted Gate A–E decisions.

### 3.1 Physical consistency

The added lattice-tolerance uniqueness bound does not change the physical geometry model. It prevents an ambiguous numerical grid assignment from being misrepresented as physical lattice truth.

**Cross-check: PASS.**

### 3.2 Mathematical consistency

The strict upper bound is consistent with the nearest-integer definition

```math
m_n=\operatorname{round}(z_n)
```

because points at exactly one-half grid spacing are equally close to two integer candidates.

**Cross-check: PASS.**

### 3.3 Dimensional consistency

`tau_lat` is dimensionless, so the accepted range introduces no dimensional inconsistency. The physical residual remains

```math
\eta_n=\varepsilon_n\Delta
```

with units of meters.

**Cross-check: PASS.**

### 3.4 Software semantic consistency

The bound maps cleanly to boundary/domain validation. Invalid tolerances are rejected before lattice integer semantics are constructed, so downstream coarray consumers never depend on ambiguous half-grid tie-breaking.

**Cross-check: PASS.**

### 3.5 Golden Reference consistency

GRP-006 uses

```text
tau_lat = 1e-5
```

which lies safely inside the accepted domain. No Golden Reference expected result changes.

**Cross-check: PASS.**

## 4. Accepted Boundary Taxonomy

ADR-001 adopts four response classes for later implementation:

- **REJECT** — scientifically invalid or undefined input/operation under ADR-001;
- **INCOMPATIBLE / REQUIRE OTHER MODEL** — meaningful scenario requiring ADR-002, ADR-003, or another scientific provider;
- **DIAGNOSTIC / WARN** — valid computation with ambiguity, conditioning, aliasing, or interpretation limits that must remain explicit;
- **VALID** — condition lies inside the declared contract.

This taxonomy is normative. Later APIs may choose concrete exception/result/warning types, but they may not silently convert a `REJECT`, `INCOMPATIBLE`, or `DIAGNOSTIC` condition into an apparently unique valid result.

## 5. Final Accepted Scientific Decisions

ADR-001 now locks the following core decisions for GeoDOA:

- intrinsic 1-D array geometry is distinct from 3-D propagation space and from identifiable directional dimension;
- the canonical array axis is `+x`;
- `+y` is the chosen canonical broadside reference axis and `+z` completes the right-handed frame;
- canonical slice direction is `u_hat(theta) = [sin(theta), cos(theta), 0]^T` for `theta in [-pi/2, pi/2]`;
- look direction points from array localization reference toward the source; incident propagation direction is its negative;
- temporal phasor convention is `exp(-j omega t)`;
- nominal receive geometry-only manifold is

```math
a_n
=
\exp[-jk(\mathbf r_n-\mathbf r_{\mathrm{ref}})^T\hat{\mathbf u}];
```

- the default analytical spatial phase reference is the centroid of the declared nominal geometry, not the active subset;
- phase-reference changes produce only a common phasor in the ideal geometry-only manifold;
- physical coordinates, stable channel identity, and provenance are authoritative; sorting/normalization/reflection/masking are derived operations;
- canonical physical geometry is stored in meters; wavelength-normalized geometry is a frequency/medium-dependent derived representation;
- `u`, `kappa_x`, declared-grid `psi`, and primitive-grid spatial frequency are distinct concepts;
- integer coarray lags require an exact-by-construction or successfully validated lattice;
- nearest-integer lattice validation requires finite positive `Delta` and `0 <= tau_lat < 0.5`;
- declared lattice and primitive lattice remain distinct provenance-bearing representations;
- 3-D projection ambiguity, front/back ambiguity, spatial aliasing, and half-wavelength endfire endpoint equivalence are explicitly distinct conditions;
- spatial manifold equivalence for geometry-only DOA is assessed up to a common phase using reference-invariant pair differences;
- scan domains are typed semantic objects rather than unlabeled numeric arrays;
- boundaries and failures are surfaced through explicit rejection, incompatibility, or diagnostics rather than silent canonicalization.

## 6. Evidence Set

The accepted ADR-001 evidence set consists of:

```text
docs/adr/ADR-001-coordinate-direction-spatial-conventions.md
docs/adr/ADR-001_ACCEPTANCE_AUDIT.md
docs/adr/ADR-001_BOUNDARY_FAILURE_ANALYSIS.md
docs/adr/ADR-001_FINAL_ACCEPTANCE_RECORD.md
docs/science/golden_reference/ADR-001_GOLDEN_REFERENCE_PROBLEMS.md
```

Together these separate:

```text
Governing scientific decision
        ↓
Progressive audit evidence
        ↓
Hand-calculated analytical evidence
        ↓
Boundary/failure evidence
        ↓
Final acceptance reconciliation
```

## 7. What Acceptance Does Not Mean

ADR-001 acceptance does **not** mean that the Phase 1 scientific implementation already exists or has passed software verification.

The accepted Golden Reference expected values become future test oracles. Phase 1 implementations governed by ADR-001 must reproduce those values and satisfy the accepted boundary behavior before the implementation is considered verified.

Likewise, acceptance of ADR-001 does not approve ADR-002, ADR-003, or ADR-004. Each remains an independent scientific contract requiring its own Gates A–F.

## 8. Closure Statement

ADR-001 has no unresolved scientific acceptance finding within its declared scope.

```text
ADR-001 STATUS: ACCEPTED
Gate A: PASS
Gate B: PASS
Gate C: PASS
Gate D: PASS
Gate E: PASS
Gate F: PASS
```

The next scientific-contract work item in Phase 0C is ADR-002 — Wave, Propagation, Signal, and Measurement Model.
