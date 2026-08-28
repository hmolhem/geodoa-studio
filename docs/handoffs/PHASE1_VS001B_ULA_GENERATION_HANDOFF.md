# GeoDOA Studio — Phase 1 VS-001B ULA Generation Handoff

## Milestone Identity

* Project: GeoDOA Studio
* Phase: Phase 1 — Authoritative Scientific Implementation
* Planning umbrella: VS-001
* Bounded slice: VS-001B — ULA Generation and Equivalence
* Branch: `feat/vs001b-ula-generation`
* Base commit: `f6b4b755d495fbefb9243f0db5f752aaaed65c59`
* Pull Request: #9
* Merge Commit: `4c87ce8b196a93d7d6d79756d64411a6321fefbf`
* Status: Closed — merged via PR #9

Implementation checkpoints:

* `09cf51b` — deterministic ULA geometry generation
* `8a25485` — ULA geometry inspection application flow
* `ae4d558` — ULA geometry inspection CLI

## Objective

Extend the accepted VS-001A physical-geometry foundation with a deterministic Uniform Linear Array generator while preserving the same authoritative `LinearArrayGeometry` representation and inspection semantics.

The engineering question for this slice is:

> Can GeoDOA generate a Uniform Linear Array from explicit physical parameters without hidden centering, translation, normalization, order reversal, or relabeling, and demonstrate that the generated physical geometry is equivalent to the corresponding explicitly declared custom geometry?

The resulting ULA must enter the same geometry inspection path already established by VS-001A.

## Governing Scientific Contracts

Primary governing evidence:

* `ADR-001-coordinate-direction-spatial-conventions.md`
* `ADR-001_BOUNDARY_FAILURE_ANALYSIS.md`
* `ADR-001_GOLDEN_REFERENCE_PROBLEMS.md`
* accepted Phase-1 validation profile `VP-001`

Relevant requirement coverage includes:

* GEO-001 — physical sensor count
* GEO-002 — ordered physical positions
* GEO-003 — explicit physical position unit
* GEO-014 — authoritative sensor ordering
* FAM-002 — Uniform Linear Array generation
* MET-001 — physical aperture
* MET-002 — centroid
* MET-003 — minimum adjacent spacing
* MET-004 — maximum adjacent spacing
* MET-005 — mean adjacent spacing

VS-001B does not claim implementation of the general GEO-019 geometry-equivalence signature.

Equivalence is demonstrated only through explicit deterministic fixtures.

## ULA Construction Contract

A ULA generation request is represented by `ULAGenerationSpec` with:

* `sensor_count`
* `spacing_m`
* `anchor_m`
* `placement_policy`

Physical positions remain expressed in meters.

Two explicit construction policies are supported.

### First-sensor placement

For

`placement_policy = first_sensor`

the physical coordinates are

```text
x_n = anchor_m + n * spacing_m
```

for

```text
n = 0, ..., N - 1
```

The construction anchor therefore identifies the first physical sensor position.

### Centroid placement

For

`placement_policy = centroid`

the coordinates are

```text
x_n = anchor_m + (n - (N - 1)/2) * spacing_m
```

for

```text
n = 0, ..., N - 1
```

The construction anchor therefore identifies the physical centroid of the generated ULA.

## Construction Anchor Versus Phase Reference

ULA construction semantics remain separate from spatial phase-reference semantics.

In particular:

```text
ULA construction anchor
    != coordinate-frame origin
    != default spatial phase reference
```

The accepted ADR-001 default spatial phase reference remains:

`declared_geometry_centroid`

regardless of which ULA construction policy generated the geometry.

The first-sensor manual oracle explicitly verifies this distinction.

## Authoritative Geometry Representation

ULA generation produces the existing immutable:

`LinearArrayGeometry`

rather than introducing a separate incompatible ULA geometry hierarchy.

Generated channels use deterministic identities:

```text
RX0
RX1
...
RX(N-1)
```

For the current strictly positive-spacing contract, authoritative generation order is also geometric ascending order.

Therefore, for a valid generated ULA:

```text
sorted_to_authoritative = identity permutation
authoritative_to_sorted = identity permutation
```

No silent sorting or order repair is required.

## Boundary Validation

ULA-specific input failures are separated from general physical-geometry validation failures.

The typed ULA generation codes are:

* `INVALID_SENSOR_COUNT`
* `NONFINITE_SPACING`
* `NONPOSITIVE_SPACING`
* `NONFINITE_ANCHOR`
* `INVALID_PLACEMENT_POLICY`

Current behavior:

* sensor count less than one: rejected;
* non-integer sensor count at the domain boundary: rejected;
* nonfinite spacing: rejected;
* zero spacing: rejected;
* negative spacing: rejected;
* nonfinite construction anchor: rejected;
* unsupported placement policy: rejected.

Negative physical positions are valid.

A single-sensor ULA is valid when its spacing parameter is positive.

For a single sensor:

* its position equals the declared anchor under either construction policy;
* aperture is zero;
* adjacent spacing sequence is empty;
* the existing `ZERO_APERTURE` diagnostic is produced by the inspection layer.

## Deterministic Scientific Oracles

### Oracle A — Centroid placement

Input:

```text
sensor_count = 4
spacing_m = 0.25
anchor_m = 0.0
placement_policy = centroid
```

Expected authoritative positions:

```text
RX0 -> -0.375 m
RX1 -> -0.125 m
RX2 ->  0.125 m
RX3 ->  0.375 m
```

Expected physical metrics:

```text
sensor count = 4
centroid = 0.0 m
aperture = 0.75 m
adjacent spacings = [0.25, 0.25, 0.25] m
minimum spacing = 0.25 m
maximum spacing = 0.25 m
mean spacing = 0.25 m
```

Expected permutations:

```text
sorted_to_authoritative = [0, 1, 2, 3]
authoritative_to_sorted = [0, 1, 2, 3]
```

Expected default spatial phase reference:

```text
policy = declared_geometry_centroid
position = 0.0 m
```

### Oracle B — First-sensor placement

Input:

```text
sensor_count = 4
spacing_m = 0.25
anchor_m = -0.50
placement_policy = first_sensor
```

Expected authoritative positions:

```text
RX0 -> -0.50 m
RX1 -> -0.25 m
RX2 ->  0.00 m
RX3 ->  0.25 m
```

Expected physical metrics:

```text
centroid = -0.125 m
aperture = 0.75 m
adjacent spacings = [0.25, 0.25, 0.25] m
```

The construction anchor is:

```text
-0.50 m
```

but the accepted default spatial phase reference is:

```text
-0.125 m
```

This independently demonstrates that ULA construction anchor and default phase reference are distinct concepts.

### Oracle C — Typed failure

Input:

```text
sensor_count = 4
spacing_m = 0
anchor_m = 0
placement_policy = centroid
```

Expected typed failure:

```text
code = nonpositive_spacing
process exit code = 2
```

Manual CLI execution produced exactly this result.

## Custom-Versus-Generated Equivalence Evidence

VS-001B verifies that a deterministic generated ULA is equal to a manually constructed `LinearArrayGeometry` fixture with the same:

* sensor identities;
* authoritative channel order;
* physical positions.

Application-level inspection then verifies agreement in:

* sensor count;
* centroid;
* aperture;
* adjacent spacings;
* sorted view;
* permutations;
* default phase-reference semantics;
* diagnostics.

This is fixture-level physical-geometry equivalence evidence.

It is not yet a general geometry-equivalence API, canonical geometry signature, or persistent identity mechanism.

## Application Flow

The implemented application path is:

```text
ULAGenerationSpec
    ->
generate_ula()
    ->
LinearArrayGeometry
    ->
existing geometry inspection
    ->
ULAInspectionResult
```

The existing VS-001A metric computation and phase-reference logic are reused rather than reimplemented.

This preserves one authoritative interpretation of physical geometry.

## Headless Interface

A centroid-anchored ULA can be inspected with:

```powershell
geodoa geometry inspect-ula `
  --sensor-count 4 `
  --spacing-m 0.25 `
  --anchor-m 0.0 `
  --placement centroid
```

A first-sensor-anchored ULA can be inspected with:

```powershell
geodoa geometry inspect-ula `
  --sensor-count 4 `
  --spacing-m 0.25 `
  --anchor-m -0.50 `
  --placement first_sensor
```

The command reports:

* ULA generation parameters;
* deterministic authoritative channels;
* physical positions in meters;
* sorted geometric view;
* forward and inverse permutations;
* physical geometry metrics;
* default phase-reference policy and position;
* typed diagnostics.

Its JSON output remains an inspection result.

It is not a stable canonical configuration or persistence schema.

## CLI Boundary Failures

The CLI distinguishes adapter-level literal parsing failures from domain-level ULA generation failures.

Examples of CLI adapter errors include:

* `invalid_sensor_count_literal`
* `invalid_spacing_literal`
* `invalid_anchor_literal`

Domain ULA failures retain their typed generation codes such as:

`nonpositive_spacing`

This distinction prevents textual command-line parsing failures from being confused with scientific-domain validation failures.

## Verification Evidence

Local verification after implementation:

```text
ULA domain tests: 18 passed
domain tests: 27 passed
ULA application tests: 5 passed
application tests: 9 passed
domain + application tests: 36 passed
ULA CLI integration tests: 4 passed
all integration tests: 6 passed
full pytest suite: 48 passed

ruff check src tests: PASS
ruff format --check src tests: PASS
mypy src: PASS
git diff --check: PASS
```

Manual scientific CLI verification:

```text
Oracle A — centroid placement: PASS
Oracle B — first-sensor placement: PASS
Oracle C — typed nonpositive-spacing failure: PASS
```

The final pull request must also pass the configured GitHub Actions matrix for Python 3.12, 3.13, and 3.14.

## Files Introduced or Changed

Domain:

* `src/geodoa/domain/ula.py`
* `src/geodoa/domain/__init__.py`

Application:

* `src/geodoa/application/ula_inspection.py`
* `src/geodoa/application/__init__.py`

Interface:

* `src/geodoa/cli.py`

Tests:

* `tests/domain/test_ula.py`
* `tests/application/test_ula_inspection.py`
* `tests/integration/test_cli_ula_inspection.py`

Supporting documentation for final review:

* `README.md`
* this handoff
* `docs/handoffs/HANDOFF_INDEX.md`

## Explicitly Deferred

The following remain outside VS-001B:

* canonical configuration persistence;
* save/load round trip;
* canonical serialization;
* geometry SHA-256 identity;
* general GEO-019 geometry-equivalence signature;
* spacing expressed in wavelengths;
* operating frequency;
* wavelength normalization;
* propagation speed configuration;
* lattice declaration;
* difference coarray;
* active-channel masks;
* position uncertainty;
* general `ReferenceFrame1D` transforms;
* direction and angle objects;
* steering-vector computation;
* array manifold computation;
* grating-lobe analysis;
* spatial-aliasing implementation;
* snapshots;
* covariance;
* eigenspace processing;
* MUSIC;
* GUI;
* measured or CST-derived manifolds;
* sensor coupling and calibration;
* arbitrary generated sensor-ID prefixes;
* fixed-point or FPGA implementation.

Expected sequencing remains:

```text
VS-001A — custom geometry inspection
    ->
VS-001B — ULA generation and equivalence
    ->
VS-001C — canonical configuration round trip
    ->
VS-002 — lattice/difference-coarray analysis
```

Future slices remain subject to bounded review before implementation.

## Rollback

VS-001B is independently reversible.

Reverting its pull request removes:

* ULA generation;
* ULA-specific application inspection;
* ULA CLI inspection;
* ULA tests and documentation;

without removing the VS-001A custom geometry capability.

Rollback does not modify:

* ADR-001 through ADR-004;
* GRP-001 through GRP-018;
* VP-001;
* accepted scientific formulas;
* persistent scientific data formats;
* external repositories.

No migration is required because VS-001B does not introduce a canonical persistence schema.

## Closure Condition

This handoff becomes closed only when:

1. the bounded VS-001B pull request is reviewed and merged;
2. GitHub Actions passes on Python 3.12, 3.13, and 3.14;
3. the actual PR number is recorded here and in `HANDOFF_INDEX.md`;
4. the merge commit is recorded;
5. the feature branch is removed locally and remotely;
6. local `main` is synchronized with `origin/main`;
7. the final post-merge worktree is clean.

All VS-001B closure conditions were satisfied after PR #9 merged.

Closure evidence:

- PR #9: merged;
- merge commit: `4c87ce8b196a93d7d6d79756d64411a6321fefbf`;
- GitHub Actions: PASS on the supported Python matrix;
- feature branch: removed locally and remotely;
- local `main`: synchronized with `origin/main` at the merge commit before
  creation of the documentation-only closeout branch;
- post-merge worktree: verified clean before closeout work began.

Final VS-001B status:

`Closed — merged via PR #9`.
