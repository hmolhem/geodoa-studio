# ADR-001 — Gate F Acceptance Audit

- **ADR:** `ADR-001-coordinate-direction-spatial-conventions.md`
- **Gate:** F — Boundary and Failure Analysis
- **Status:** CONDITIONAL — one normative ADR reconciliation required
- **Evidence:** `ADR-001_BOUNDARY_FAILURE_ANALYSIS.md`

## 1. Audit Question

Does ADR-001 explicitly identify where the geometry-only spatial model is invalid, underdetermined, ambiguous, aliased, numerically delicate, or outside its declared domain, and does it distinguish invalid inputs from valid-but-nonunique scientific conditions?

## 2. Boundary Taxonomy — PASS

The boundary analysis defines four required response classes:

```text
REJECT
INCOMPATIBLE / REQUIRE OTHER MODEL
DIAGNOSTIC / WARN
VALID
```

This distinction is necessary because, for example, an invalid zero look vector is not the same scientific condition as a valid but spatially aliased direction pair.

## 3. Structural Geometry Boundaries — PASS

The analysis covers:

- zero declared channels;
- single-channel/zero-aperture directional unobservability;
- nonfinite coordinates;
- duplicate stable channel identities;
- accidental versus explicitly modeled colocated channels.

The geometry entity may represent some degenerate configurations, but algorithms that require directional discrimination must reject or report incompatibility when the active geometry has fewer than two distinct spatial phase centers.

## 4. Coordinate and Direction Boundaries — PASS

The analysis covers:

- invalid/nonfinite frame definitions;
- zero/nonfinite/non-unit look direction semantics;
- physical direction cosine outside `[-1,1]`;
- canonical angle outside `[-pi/2, pi/2]` without explicit boundary conversion.

The scientific core must not silently normalize or wrap inputs in ways that erase provenance or convention meaning.

## 5. Minimal Wave-Context Boundaries — PASS

ADR-002 owns the complete wave model, but ADR-001 requires a valid frequency/speed context for spatial phase. The boundary analysis therefore rejects nonpositive/nonfinite physical frequency and propagation speed and identifies near-field or wideband misuse as model incompatibility rather than geometry failure.

## 6. Identifiability and Ambiguity Boundaries — PASS

The analysis explicitly covers:

- 3-D projection ambiguity;
- front/back ambiguity;
- spatial aliasing;
- the `Delta = lambda/2`, `u = ±1` endpoint equivalence;
- frequency-dependent ambiguity;
- invalid uniqueness claims from an underdetermined 1-D geometry.

These conditions are not silently canonicalized away.

## 7. Conditioning Boundary Near Endfire — PASS

The inverse map

```math
\frac{d\theta}{du}
=
\frac{1}{\sqrt{1-u^2}}
```

becomes ill-conditioned as `|u| -> 1`. This is classified as a valid but numerically/interpretively delicate condition, not an invalid physical direction.

## 8. Phase-Reference Boundaries — PASS

The analysis confirms that:

- a finite phase-reference point need not coincide with a sensor or lattice point;
- a named reference channel must exist;
- common phase-reference factors are not physical manifold distortion;
- full source-signal phase bookkeeping under reference changes belongs to ADR-002.

## 9. Lattice Boundaries — CONDITIONAL FINDING

All major lattice failure modes are covered:

- `Delta <= 0` or nonfinite spacing;
- lattice validation failure;
- exact-by-construction versus tolerance-admitted provenance;
- degenerate primitive lattice;
- declared versus primitive grid;
- real-valued difference analysis versus integer-lag coarray analysis.

### F-CORR-001 — Lattice-tolerance uniqueness bound

For nearest-integer lattice validation,

```math
m_n=\operatorname{round}(z_n),
```

a half-integer point lies equally close to two integers. Therefore the scientific contract must require

```math
\boxed{0\le\tau_{\mathrm{lat}}<1/2}.
```

Negative, nonfinite, or `tau_lat >= 0.5` values must be rejected.

This is a material scientific constraint and must be incorporated into the governing ADR before Gate F receives final PASS.

**Status: REQUIRED ADR RECONCILIATION.**

## 10. Active-Channel Boundaries — PASS

The analysis covers:

- empty active subset;
- masks that destroy directional aperture;
- preservation of the stable geometry-level phase reference under masking.

## 11. Derived-View and Identity Boundaries — PASS

Sorting, translation normalization, reflection equivalence, and wavelength normalization are classified without allowing destructive replacement of authoritative physical state.

## 12. Numerical Comparison Boundaries — PASS

The analysis distinguishes:

- complex/wrapped phase equivalence from raw unwrapped phase equality;
- exact-vector comparison from common-phase-aligned manifold comparison;
- scientific tolerance policy from the underlying physical contract.

## 13. Outside-Scope Sensor/Propagation Effects — PASS

Near-field curvature, wideband differential delay, dispersive medium, motion, element pattern, polarization, mutual coupling, channel mismatch, position error, sampling skew, and quantization are classified as requiring ADR-002 or ADR-003 when materially relevant.

Computing the ADR-001 nominal manifold remains valid as an explicitly labeled baseline; treating it as unqualified physical truth does not.

## 14. Gate F Decision

**Gate F status: CONDITIONAL — NOT YET PASS.**

The boundary/failure model is scientifically complete enough for acceptance, but one normative constraint discovered by the audit must first be reconciled into ADR-001:

```math
0\le\tau_{\mathrm{lat}}<\frac12.
```

After that correction, the ADR summary must also be reconciled so that:

- Gate E is marked PASS;
- Gate F is marked PASS;
- the acceptance audit summary reports all six gates consistently;
- ADR-001 status may then be changed from `Proposed` to `Accepted` only after a final cross-gate consistency check.
