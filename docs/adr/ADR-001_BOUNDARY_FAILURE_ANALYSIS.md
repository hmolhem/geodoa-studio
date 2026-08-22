# ADR-001 — Boundary and Failure Analysis

- **Governing ADR:** `ADR-001-coordinate-direction-spatial-conventions.md`
- **Phase:** 0C — Scientific Foundations
- **Gate:** F — Boundary and Failure Analysis
- **Status:** Complete — candidate evidence for Gate F PASS

## 1. Purpose

ADR-001 defines a geometry-only spatial contract. Gate F identifies where that contract is invalid, underdetermined, ambiguous, aliased, numerically delicate, or outside its declared scope.

The goal is not to force every nonideal condition to fail. The goal is to prevent GeoDOA from silently converting a scientifically meaningful limitation into an apparently valid unique result.

## 2. Required Response Classes

GeoDOA shall distinguish the following behaviors:

- **REJECT** — the requested domain object or operation is not scientifically well-defined under ADR-001 and shall not execute as if valid.
- **INCOMPATIBLE / REQUIRE OTHER MODEL** — the requested scenario is meaningful, but ADR-001's geometry-only model is insufficient; another scientific contract/provider is required.
- **DIAGNOSTIC / WARN** — the computation may proceed, but the result is ambiguous, non-unique, poorly conditioned, or assumption-sensitive and the condition must be retained in diagnostics/provenance.
- **VALID** — the condition is within the declared contract and requires no exceptional handling beyond ordinary validation.

A warning is not permission to make a uniqueness or physical-validity claim that the model does not support.

## 3. Structural Geometry Boundaries

### F-001 — Empty geometry

A declared geometry with zero channels has no centroid, no default phase reference, and no manifold dimension.

**Required behavior:** `REJECT` construction of an authoritative linear-array geometry with zero declared channels.

### F-002 — Single channel or zero spatial aperture

A single active channel, or multiple active scalar channels at one identical nominal phase-center position, has no relative geometry-only spatial phase information.

The manifold may be mathematically evaluated as a direction-independent common coefficient, but geometry-only DOA is unobservable.

**Required behavior:**

- geometry representation may remain valid when there is at least one declared channel;
- algorithms requiring directional discrimination must report `INCOMPATIBLE` when fewer than two distinct active nominal phase-center positions are available;
- zero-aperture/one-distinct-position state must be explicit in diagnostics.

### F-003 — Nonfinite positions or duplicate stable identities

NaN/Inf coordinates cannot define physical geometry. Two channels may not silently share one stable `sensor_id`.

**Required behavior:** `REJECT` nonfinite authoritative positions and duplicate channel identities.

### F-004 — Duplicate physical positions

ADR-001 already distinguishes accidental duplicate scalar channels from explicitly modeled colocated channels.

**Required behavior:**

- accidental duplicate scalar positions: `REJECT` under the default duplicate policy;
- explicitly modeled colocated channels: permitted only under an explicit sensor-response contract governed by ADR-003;
- never call `unique()` or otherwise collapse them silently.

## 4. Coordinate-Frame and Direction Boundaries

### F-005 — Invalid 1-D frame

A `ReferenceFrame1D`-style embedding must have finite spatial origin and a valid nonzero unit array-axis direction. If a full local triad is represented, it must be mutually orthonormal and right-handed within the declared numerical tolerance.

**Required behavior:** `REJECT` zero-length, nonfinite, non-orthogonal, or left-handed frame definitions unless an explicit transformation operation is used to construct a valid frame.

### F-006 — Invalid 3-D look direction

A look-direction object must represent a finite unit vector.

**Required behavior:**

- zero vector or nonfinite vector: `REJECT`;
- arbitrary non-unit vector: do not silently normalize inside a scientific kernel; either reject or require an explicit validated normalization constructor/conversion;
- the exact normalization tolerance is an implementation-level numerical policy, not a change to this scientific rule.

### F-007 — Direction cosine outside the physical interval

Physical 1-D direction cosine satisfies

```math
u\in[-1,1].
```

**Required behavior:** a physical `DirectionCosine` value or grid outside this interval is `REJECT` unless the user explicitly requests a nonphysical mathematical spatial-frequency diagnostic domain with a different typed semantic.

### F-008 — Canonical angle outside its principal interval

ADR-001's canonical slice uses

```math
\theta\in[-\pi/2,\pi/2].
```

Angles outside this interval are not silently wrapped through `sin(theta)` because doing so would erase which physical half-plane/convention was supplied.

**Required behavior:**

- canonical-angle input outside the principal interval: `REJECT`;
- externally defined angle conventions may be accepted only through an explicit boundary conversion that preserves the source convention/provenance.

## 5. Wave-Parameter Boundaries Needed by the Spatial Contract

ADR-002 owns the full wave/propagation model, but ADR-001 requires a minimal valid phase context to evaluate its manifold.

### F-009 — Nonpositive or nonfinite frequency

The physical wavelength relation `lambda = v_p/f` and the intended receive phase contract require positive finite physical frequency.

**Required behavior:** `REJECT` `f <= 0` or nonfinite `f` for this physical manifold contract. Negative-frequency/baseband spectral semantics belong to ADR-002 and shall not be inferred here.

### F-010 — Nonpositive or nonfinite propagation speed

**Required behavior:** `REJECT` `v_p <= 0` or nonfinite propagation speed.

### F-011 — Plane-wave/far-field applicability not established

ADR-001 derives the relative phase using the first-order plane-wave relation. It does not define when a real scenario is sufficiently far field.

**Required behavior:**

- an explicitly declared ideal plane-wave simulation is valid by model declaration;
- a physical/near-field scenario shall not silently use ADR-001's far-field manifold when ADR-002 compatibility checks indicate curvature is material;
- such a case is `INCOMPATIBLE / REQUIRE OTHER MODEL`, not a geometry error.

### F-012 — Wideband use of a single-frequency manifold

ADR-001's manifold is frequency-specific. Applying one carrier-frequency steering vector to data whose bandwidth makes differential delay material is outside this contract.

**Required behavior:** `INCOMPATIBLE / REQUIRE ADR-002 wideband model` when the scenario violates the narrowband usage assumptions of the selected processing chain.

## 6. Fundamental 1-D Observability Boundaries

### F-013 — 3-D projection ambiguity

Distinct 3-D directions with the same `u_x` produce the same ideal geometry-only manifold.

**Required behavior:**

- manifold computation: allowed;
- unique 3-D DOA claim from the ideal 1-D phase-only geometry: `REJECT` as underdetermined;
- return a projection-ambiguity diagnostic when a requested interpretation exceeds the identifiable directional dimension.

GRP-004 is the deterministic reference case.

### F-014 — Front/back ambiguity

The canonical `xy` slice chooses a half-plane parameterization. It does not create physical front/back information that the ideal 1-D phase-only geometry does not possess.

**Required behavior:** `DIAGNOSTIC / WARN` when results are interpreted as physical full-plane direction. A unique front/back claim requires additional element response, polarization, non-collinear geometry, or other information governed outside ADR-001.

### F-015 — Spatial aliasing

Distinct observable direction cosines may produce common-phase-equivalent manifolds.

**Required behavior:**

- computation may proceed;
- ambiguity must be reported by a reference-invariant pair-difference/manifold-equivalence diagnostic;
- a unique-DOA claim is invalid over a scan domain containing equivalent directions unless additional information resolves the ambiguity.

GRP-005A is the deterministic reference case.

### F-016 — Half-wavelength endpoint boundary

At conventional ULA primitive spacing

```math
\Delta=\lambda/2,
```

the open visible interval has the usual no-grating-lobe property, but `u=+1` and `u=-1` remain equivalent at the two closed-interval endfire endpoints.

**Required behavior:** `DIAGNOSTIC / WARN`; do not report strict injectivity on the closed interval.

GRP-005B is the deterministic reference case.

### F-017 — Frequency-dependent ambiguity

Spatial ambiguity is not a geometry-only Boolean independent of wave context because

```math
k=2\pi/\lambda
```

changes with frequency and medium.

**Required behavior:** ambiguity/unaliased diagnostics must identify the frequency/propagation context under which they were evaluated. A geometry shall not be globally labeled `unaliased` without that context.

## 7. Angle/Direction-Cosine Conditioning Boundary

### F-018 — Endfire inverse-map ill-conditioning

Although

```math
u=\sin\theta
```

is one-to-one on the canonical interval, the inverse sensitivity is

```math
\frac{d\theta}{du}
=
\frac{1}{\sqrt{1-u^2}},
```

which diverges as `|u| -> 1`.

Therefore a fixed error or grid spacing in direction cosine can correspond to a very large angular error near endfire.

**Required behavior:** `DIAGNOSTIC / WARN` for angle-domain conditioning near `|u| = 1`; do not interpret uniform `u` resolution as uniform angular resolution.

This is a conditioning boundary, not an invalid direction.

## 8. Phase-Reference Boundaries

### F-019 — Arbitrary finite spatial phase reference

The phase reference need not lie on a sensor or lattice point. Any finite declared spatial point is mathematically valid.

**Required behavior:** `VALID`, provided the reference is explicit/provenanced.

### F-020 — Invalid named reference channel

If configuration selects a named physical reference channel, that channel identity must exist in the declared geometry. It need not be active if the policy intentionally allows an inactive physical reference, but that choice must be explicit.

**Required behavior:** unknown/nonexistent named channel: `REJECT`.

### F-021 — Common phase is not physical distortion

Changing phase reference changes the steering vector by a common unit-magnitude phasor.

**Required behavior:** comparison code shall use an appropriate common-phase-invariant diagnostic when physical manifold shape is the target. A common reference factor alone is not a sensor mismatch or DOA failure.

The source-signal phase bookkeeping required to preserve an entire `x = A s` signal model under reference changes belongs to ADR-002.

## 9. Lattice Boundaries

### F-022 — Invalid lattice spacing

Declared lattice spacing must be finite and strictly positive.

**Required behavior:** `REJECT` `Delta <= 0` or nonfinite `Delta`.

### F-023 — Lattice-tolerance uniqueness bound

With

```math
m_n=\operatorname{round}(z_n),
```

a half-integer `z_n = q + 1/2` is equally distant from two integers. Therefore an accepted nearest-integer lattice relation must not allow the tolerance to include the half-grid boundary.

GeoDOA requires

```math
\boxed{0\le\tau_{\mathrm{lat}}<\frac12}.
```

**Required behavior:** `REJECT` negative, nonfinite, or `tau_lat >= 0.5` lattice tolerances.

This condition does not select the project's eventual default tolerance; it only establishes the scientifically admissible range for this nearest-integer validation semantics.

### F-024 — Lattice validation failure

If

```math
\max_n\rho_n>\tau_{\mathrm{lat}},
```

the candidate integer lattice is not established.

**Required behavior:**

- preserve the real physical coordinates and real pair differences;
- return failed lattice-validation evidence with residuals;
- `REJECT` downstream integer-lag/coarray operations requiring that lattice;
- do not round anyway.

### F-025 — Exact-by-construction versus tolerance-admitted lattice

An exact generator-defined lattice and a numerically tolerance-admitted external geometry are different provenance states even when they yield the same integer indices.

**Required behavior:** preserve which state produced the integer semantics. Do not rewrite a tolerance-admitted imported geometry as exact-by-construction.

### F-026 — Degenerate primitive lattice

If all accepted integer indices are identical, all pairwise integer differences are zero and no positive primitive spacing is defined.

**Required behavior:** return a degenerate/zero-aperture diagnostic; do not invent `g` or a primitive spacing.

### F-027 — Declared versus primitive lattice

When relative integer indices have `g > 1`, the declared grid and primitive grid are both valid representations with different provenance and normalized-frequency coordinates.

**Required behavior:** `DIAGNOSTIC`; never silently replace declared spacing by primitive spacing. GRP-005C and GRP-006 provide reference cases.

### F-028 — Real difference coarray versus integer-lag coarray

A non-lattice geometry still has physically valid real-valued pair differences.

**Required behavior:** failure to establish an integer lattice does **not** prohibit physical real-difference analysis; it prohibits only representations/algorithms whose contract requires integer lag indexing.

## 10. Active-Channel Boundaries

### F-029 — Empty active subset

A processing view containing no active channels cannot produce an array manifold or relative spatial observable.

**Required behavior:** `REJECT` such processing execution.

### F-030 — Active subset destroys directional aperture

A declared geometry may be valid while a selected active subset leaves fewer than two distinct active positions.

**Required behavior:** preserve the geometry and mask provenance, but report the selected processing chain as `INCOMPATIBLE` with phase-only DOA.

### F-031 — Active mask must not redefine the default phase reference

**Required behavior:** changing the active subset alone is `VALID` as a view operation but must not silently recompute the geometry-level default reference.

## 11. Derived-View and Identity Boundaries

### F-032 — Sorting

Sorting is valid only as a traceable permutation.

**Required behavior:** `REJECT` any implementation behavior that loses the mapping between authoritative channel identity/order and sorted order.

### F-033 — Translation normalization

Translation-normalized geometry is a valid derived representation for invariant comparison.

**Required behavior:** `VALID` only as an explicit derived view; destructive replacement of authoritative physical coordinates is forbidden.

### F-034 — Reflection equivalence

Reflection may preserve selected geometry/coarray metrics but reverses orientation relative to the declared frame.

**Required behavior:** return reflection equivalence as a `DIAGNOSTIC`, not as default identity or silent canonicalization.

### F-035 — Wavelength-normalized geometry

Normalized coordinates are frequency/medium dependent.

**Required behavior:** `REJECT` any attempt to treat unlabeled normalized numbers as authoritative physical positions. Explicit normalized input requires enough wave context to convert to meters.

## 12. Numerical Comparison Boundaries

### F-036 — Wrapped phase and exact floating-point equality

The physical manifold is a complex phasor object; phase values differing by integer multiples of `2 pi` are equivalent. Floating-point calculations also require tolerance-aware comparison.

**Required behavior:** future verification shall compare complex values or wrapped/reference-invariant phase quantities using a centrally declared numerical tolerance. Raw unwrapped phase equality is not an authoritative scientific criterion.

The exact tolerance profile remains an implementation/verification-policy decision.

### F-037 — Common-phase-equivalent manifold comparison

Two manifolds may be scientifically equivalent for geometry-only DOA while not being component-wise equal because of phase-reference choice.

**Required behavior:** preserve both exact-vector comparison and common-phase-aligned comparison as different metrics. Do not substitute one silently for the other.

## 13. Outside-Scope Physical Effects

The following conditions do not invalidate ADR-001 as a definition of the nominal geometry-only manifold; they invalidate using that nominal manifold as an unqualified model of physical truth:

- near-field curvature;
- wideband differential delay;
- dispersive or spatially varying medium;
- moving source or moving array;
- direction/frequency-dependent element pattern;
- polarization;
- mutual coupling;
- channel gain/phase/delay mismatch;
- clock/sampling skew;
- position uncertainty/error beyond the nominal geometry definition;
- quantization and receiver nonlinearities.

**Required behavior:** `INCOMPATIBLE / REQUIRE ADR-002 or ADR-003 model` when the selected use case requires these effects and the active model does not represent them. The nominal manifold may still be intentionally computed as a baseline if labeled as such.

## 14. Boundary Classification Matrix

| Condition | Required classification |
|---|---|
| zero declared channels | REJECT |
| one channel / one distinct active position for DOA | INCOMPATIBLE + diagnostic |
| nonfinite position or duplicate `sensor_id` | REJECT |
| invalid reference frame | REJECT |
| invalid/zero/nonfinite look vector | REJECT |
| physical `u` outside `[-1,1]` | REJECT |
| canonical `theta` outside `[-pi/2,pi/2]` without explicit conversion | REJECT |
| nonpositive/nonfinite physical `f` or `v_p` | REJECT |
| near-field/wideband use with incompatible plane-wave/single-frequency model | REQUIRE ADR-002 |
| unique 3-D DOA claim from ideal 1-D geometry | REJECT as underdetermined |
| front/back ambiguity | DIAGNOSTIC/WARN |
| spatial aliasing | DIAGNOSTIC/WARN; uniqueness claim invalid |
| `Delta=lambda/2`, `u=±1` | DIAGNOSTIC/WARN endpoint equivalence |
| near-endfire `u -> ±1` angle sensitivity | DIAGNOSTIC/WARN |
| `Delta <= 0` | REJECT |
| `tau_lat < 0`, nonfinite, or `tau_lat >= 0.5` | REJECT |
| lattice validation fails | integer-lag operation REJECT; real differences remain valid |
| degenerate primitive lattice | DIAGNOSTIC / no primitive spacing |
| `g > 1` declared versus primitive grid | DIAGNOSTIC; preserve both |
| empty active subset | REJECT |
| mask leaves no directional aperture | INCOMPATIBLE for phase-only DOA |
| reflection equivalence | DIAGNOSTIC, not identity |
| common phase-reference factor | VALID equivalence, not physical mismatch |
| nonideal physical sensor effects | REQUIRE ADR-003 or explicit nominal-baseline label |

## 15. Gate F Decision

The boundary/failure analysis finds no unresolved contradiction that prevents ADR-001 from serving as the project-wide coordinate/direction/spatial convention.

The analysis adds one material scientific constraint that must be propagated into ADR-001:

```math
0\le\tau_{\mathrm{lat}}<\frac12.
```

It also formalizes the distinction between invalid input, incompatible model scope, scientifically meaningful ambiguity, and numerically delicate but valid conditions.

**Gate F candidate status: PASS, subject to reconciliation of the ADR-001 summary/contract text and acceptance audit.**
