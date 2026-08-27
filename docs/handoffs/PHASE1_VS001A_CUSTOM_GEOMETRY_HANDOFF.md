# GeoDOA Studio — Phase 1 VS-001A Custom Geometry Handoff

## Milestone Identity

- Project: GeoDOA Studio
- Phase: Phase 1 — Authoritative Scientific Implementation
- Planning umbrella: VS-001
- Bounded slice: VS-001A — Canonical Custom 1-D Geometry Creation and Validation
- Branch: `feat/vs001a-custom-geometry-inspection`
- Base commit: `17d0ea942126bd59dcd6e0d58a86b93ed3e2bf40`
- Pull Request: #7
- Merge Commit: Pending
- Status: Implementation complete — PR #7 open (draft)

## Objective

Establish the first executable Phase-1 scientific capability:

> Accept an explicitly declared custom 1-D physical array, preserve stable
> sensor identity and authoritative channel ordering, validate the geometry
> without silent normalization, derive a sorted geometric view and basic
> physical metrics, expose the accepted default phase-reference semantics,
> and provide one headless inspection use case.

This slice is intentionally narrower than the planning-level VS-001 umbrella.

## Governing Scientific Contracts

Primary governing evidence:

- `ADR-001-coordinate-direction-spatial-conventions.md`
- `ADR-001_BOUNDARY_FAILURE_ANALYSIS.md`
- `ADR-001_GOLDEN_REFERENCE_PROBLEMS.md`

Relevant requirement coverage:

- GEO-001 — physical sensor count
- GEO-002 — ordered physical positions
- GEO-003 — explicit position unit at the current boundary
- GEO-014 — authoritative sensor ordering
- GEO-015 — duplicate-position policy
- FAM-001 — initial custom linear-array path
- MET-001 — physical aperture in meters
- MET-002 — centroid
- MET-003 — minimum adjacent spacing
- MET-004 — maximum adjacent spacing
- MET-005 — mean adjacent spacing

## Implemented Scientific Behavior

### Authoritative geometry

The implementation introduces an immutable `LinearArrayGeometry` containing
ordered `SensorChannel1D` entities.

Each channel preserves:

- stable `sensor_id`;
- intrinsic 1-D physical position in meters.

The input channel order remains authoritative.

The implementation does not silently:

- sort;
- translate;
- normalize;
- reflect;
- deduplicate;
- relabel.

### Derived sorted view

`SortedGeometryView` provides a non-destructive geometric ordering together with:

- `sorted_to_authoritative`;
- `authoritative_to_sorted`.

Sorting therefore never changes the authoritative channel representation.

### Boundary validation

The following ADR-001 structural boundaries are enforced:

- empty geometry: rejected;
- nonfinite physical position: rejected;
- duplicate stable sensor identity: rejected;
- accidental duplicate physical position: rejected.

A single-channel geometry remains valid.

### Physical geometry metrics

The initial metric set contains:

- sensor count;
- centroid in meters;
- aperture in meters;
- sorted adjacent spacings in meters;
- minimum adjacent spacing;
- maximum adjacent spacing;
- mean adjacent spacing.

For a single-channel geometry:

- aperture is zero;
- adjacent-spacing sequence is empty;
- min/max/mean adjacent spacing are `None`.

### Diagnostics

A valid zero-aperture geometry produces the typed diagnostic:

`ZERO_APERTURE`

under the current default scalar-channel profile.

### Default spatial phase reference

The inspection result exposes the accepted ADR-001 default policy:

`declared_geometry_centroid`

with the corresponding centroid position in meters.

No explicit phase-reference override or steering computation is implemented in
this slice.

## Independent Oracle

The primary hand-calculated unsorted fixture is:

```text
authoritative channels:
RX2 -> 0.30 m
RX0 -> 0.00 m
RX1 -> 0.15 m
```

Expected derived values:

```text
sensor count = 3
centroid = 0.15 m
aperture = 0.30 m

sorted order:
RX0 -> 0.00 m
RX1 -> 0.15 m
RX2 -> 0.30 m

sorted_to_authoritative = [1, 2, 0]
authoritative_to_sorted = [2, 0, 1]

adjacent spacings = [0.15, 0.15] m
minimum spacing = 0.15 m
maximum spacing = 0.15 m
mean spacing = 0.15 m

default phase reference = 0.15 m
```

## Golden Reference Coverage

This slice uses only the geometry-relevant portions of the accepted ADR-001
Golden Reference set.

Verified:

- GRP-002 geometry-centroid subset:
  positions `[0.00, 0.15] m` produce centroid `0.075 m`;
- GRP-003 translation subset:
  positions `[0.03, 0.18] m` produce centroid `0.105 m` while preserving
  aperture and spacing.

Not claimed as verified by this slice:

- GRP-001 propagation delay;
- GRP-002 steering-vector behavior;
- GRP-003 manifold translation/reference-change behavior;
- GRP-004 projection ambiguity;
- GRP-005 spatial aliasing;
- GRP-006 lattice and difference-coarray behavior.

## Headless Interface

The first executable scientific use case is:

```powershell
geodoa geometry inspect-custom `
  --sensor RX2 0.30 `
  --sensor RX0 0.00 `
  --sensor RX1 0.15
```

The command reports:

- authoritative channel identity/order;
- non-destructive sorted geometric view;
- forward and inverse permutations;
- physical geometry metrics;
- default phase-reference policy and position;
- typed diagnostics.

The JSON output is an inspection result only.

It is not yet a stable canonical configuration, persistence schema, or
cross-version serialization contract.

## Verification Evidence

Current local verification:

```text
pytest: 21 passed
ruff check: PASS
ruff format --check: PASS
mypy src: PASS
manual CLI inspection: PASS
```

The final PR must also pass the configured GitHub Actions matrix for Python
3.12, 3.13, and 3.14.

## Files Introduced or Changed

Implementation:

- `src/geodoa/domain/geometry.py`
- `src/geodoa/domain/__init__.py`
- `src/geodoa/science/geometry_metrics.py`
- `src/geodoa/science/__init__.py`
- `src/geodoa/application/geometry_inspection.py`
- `src/geodoa/application/__init__.py`
- `src/geodoa/cli.py`

Tests:

- `tests/domain/test_geometry.py`
- `tests/science/test_geometry_metrics.py`
- `tests/application/test_geometry_inspection.py`
- `tests/integration/test_cli_geometry_inspection.py`

Supporting changes:

- `pyproject.toml`
- `README.md`
- this handoff
- `HANDOFF_INDEX.md`

## Explicitly Deferred

The following remain outside VS-001A:

- ULA generation;
- canonical configuration persistence;
- geometry SHA-256 identity;
- lattice declaration and validation;
- difference coarray;
- active-channel masking;
- position uncertainty;
- general `ReferenceFrame1D` transforms;
- direction and angle domain objects;
- frequency and propagation modeling;
- steering/manifold computation;
- snapshots;
- covariance;
- eigenspace processing;
- MUSIC;
- GUI;
- measured/CST manifolds;
- sensor imperfections and calibration;
- fixed-point or FPGA implementation.

Expected sequencing:

```text
VS-001A — custom geometry inspection
    ↓
VS-001B — ULA generation/equivalence
    ↓
VS-001C — canonical configuration round trip
    ↓
VS-002 — lattice/difference-coarray analysis
```

The exact future decomposition remains subject to bounded review before each
branch is created.

## Rollback

VS-001A is independently reversible.

Reverting its pull request removes the first custom-geometry scientific
implementation and CLI entry point without modifying:

- ADR-001 through ADR-004;
- GRP-001 through GRP-018;
- VP-001;
- accepted scientific formulas;
- external repositories;
- persistent scientific data formats.

No migration is required because VS-001A does not introduce a canonical
persistence schema.

## Closure Condition

This handoff becomes closed only when:

1. the bounded VS-001A pull request is reviewed and merged;
2. GitHub Actions passes on the supported Python matrix;
3. the PR number is recorded here and in `HANDOFF_INDEX.md`;
4. the merge commit is recorded;
5. the feature branch is removed locally and remotely;
6. local `main` is synchronized with `origin/main`;
7. the final worktree is clean.

Until those conditions are satisfied, status remains:

`Implementation complete — PR #7 open (draft)`.
