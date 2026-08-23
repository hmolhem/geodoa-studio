# GeoDOA Studio — Phase 0C Scientific Foundations Handoff

## Milestone Identity

- Project: GeoDOA Studio
- Milestone: Phase 0C — Scientific Foundations and Contracts
- Material branch: `docs/phase0c-scientific-conventions`
- Material Pull Request: #4
- Material Merge Commit: `eb91cdf1c09fab316a56b10ec39bde475b235657`
- Closure reconciliation branch: `docs/phase0c-closure-reconciliation`
- Status: Closed — material work merged via PR #4; post-merge closure reconciliation recorded separately
- Authoritative Phase-1 scientific implementation introduced in Phase 0C: None

## Objective

Establish and accept the scientific conventions, measurement models, sensor/calibration semantics, validation rules, reproducibility rules, Golden Reference evidence, and boundary/failure behavior required before authoritative GeoDOA scientific implementation begins.

Phase 0C intentionally precedes Phase 1 implementation so that later geometry, steering, covariance, DOA, Monte Carlo, fixed-point, and FPGA work consumes accepted scientific contracts rather than reconstructing conventions from code or memory.

## Accepted Scientific Contracts

Phase 0C completed and accepted:

```text
ADR-001 — Coordinate, Direction, and Spatial Conventions
ADR-002 — Wave Propagation, Signal, and Measurement Model
ADR-003 — Sensor Imperfections, Mutual Coupling, and Calibration
ADR-004 — Validation, Reproducibility, and Scientific Evidence
```

Each ADR completed its required scientific acceptance process, including applicable exploration/reconciliation work, physical consistency, mathematical consistency, dimensional/unit consistency, software-semantic consistency, hand/Golden Reference evidence, boundary/failure analysis, and final cross-gate reconciliation.

Final ADR status:

```text
ADR-001  ACCEPTED
ADR-002  ACCEPTED
ADR-003  ACCEPTED
ADR-004  ACCEPTED
```

## Core Phase 0C Scientific Baseline

The accepted initial implementation target is:

```text
VP-001 — Phase-1 Ideal Far-Field Narrowband 1-D DOA Validation Profile
```

VP-001 inherits:

- ADR-001 geometry, direction, phase, phase-reference, and stable channel-identity semantics;
- ADR-002 propagation, far-field/narrowband, snapshot, source/noise, covariance/second-moment, rank, and SNR semantics;
- ADR-003 ideal Phase-1 sensor profile, with nonideal sensor mechanisms governed but deferred unless explicitly activated through later profiles;
- ADR-004 evidence, stochastic-trial, association, metric, failure, uncertainty, provenance, reproducibility, and float/fixed/FPGA cross-validation semantics.

The first authoritative scientific implementation may therefore begin from accepted contracts rather than provisional conventions.

## Golden Reference Program

Phase 0C established the Golden Reference evidence family through GRP-018.

Accepted ADR-linked Golden Reference artifacts are stored under:

```text
docs/science/golden_reference/
```

They cover the deterministic reference chain required for future software verification, including geometry/steering/propagation, covariance/eigenstructure/MUSIC, sensor imperfections/coupling/calibration, and bias/variance/MSE/RMSE evidence.

The Golden Reference suite is independent scientific reference evidence and shall not be replaced by regression against production outputs alone.

## Accepted Engineering / Scientific Separation

Phase 0C locks several distinctions that later implementation must preserve, including:

```text
nominal geometry != physical geometry
coordinate origin != expansion origin != phase reference
look direction != propagation direction
exact path model != far-field approximation
far field != narrowband
sample second moment != centered sample covariance
source count != source-covariance rank != observed subspace rank != model order
sensor-model error != finite-sample error
calibration != validation
compatibility != performance != identifiability
ADC quantization != FPGA fixed-point arithmetic
software/FPGA agreement != physical validation
association != detection != resolution != localization error
metric computation != acceptance threshold
reproducibility != correctness
```

## Phase-1 Authorization Consequence

With ADR-001 through ADR-004 accepted, the scientific contracts required for the initial VP-001 implementation are sufficiently governed to begin authoritative Phase-1 implementation planning and implementation.

This authorization does not pre-accept any implementation.

Phase-1 software must still demonstrate compliance with:

- accepted Golden Reference oracles;
- ADR-004 Gate-D software-semantic obligations;
- ADR-004 Gate-F boundary/failure behavior;
- repository engineering quality gates;
- reproducibility and provenance requirements;
- later implementation-specific acceptance criteria.

## Deliberately Deferred from Phase 0C

Phase 0C governs many later capabilities but does not claim they are implemented. Deferred work includes, among others:

- production geometry domain models and generators;
- steering/manifold software kernels;
- Bartlett, MVDR/Capon, MUSIC, ESPRIT, sparse estimators, PCA/SVD processing;
- Monte Carlo execution engine and publication evidence packages;
- GUI implementation;
- measured/CST manifold ingestion;
- nonideal sensor/coupling/calibration software profiles;
- near-field and wideband profiles;
- fixed-point arithmetic models;
- HLS/RTL kernels;
- PYNQ/FPGA integration;
- physical sensor validation.

These belong to later bounded work packages.

## Material Pull Request Verification

Material Pull Request #4:

```text
Title: Phase 0C: Establish and accept scientific foundation contracts
Base: main
Head: docs/phase0c-scientific-conventions
Material head: 3c477d6b96e397a0e1742e7c2d577c5af5970e0c
Material merge: eb91cdf1c09fab316a56b10ec39bde475b235657
Changed files: 67
Scope: documentation/scientific-contract artifacts only
```

Before merge, PR #4 was verified as mergeable and GitHub Actions passed on Python 3.12, 3.13, and 3.14, including Ruff lint, Ruff format validation, mypy, and pytest.

No authoritative Phase-1 scientific implementation was introduced by the material pull request.

## Branch Cleanup and Main Synchronization

After material PR #4 was merged:

- local `main` was synchronized to `origin/main` at `eb91cdf1c09fab316a56b10ec39bde475b235657`;
- the local `docs/phase0c-scientific-conventions` branch was deleted;
- the remote `origin/docs/phase0c-scientific-conventions` branch was deleted;
- `git fetch --prune` removed stale remote-tracking state;
- local branch listing returned only `main` and its `origin/main` remote tracking state;
- the working tree was clean before this administrative closure-reconciliation branch was created.

## Post-Merge Closure Reconciliation

Per the repository governance policy, the final material merge commit cannot be authoritatively recorded before the material PR is actually merged.

This documentation-only closure reconciliation therefore records:

```text
Material PR              #4
Material merge commit    eb91cdf1c09fab316a56b10ec39bde475b235657
Material milestone       Phase 0C — Scientific Foundations and Contracts
Final material status    Closed
```

This reconciliation is an administrative continuation of Phase 0C, not a new engineering milestone. It receives no independent sequential milestone entry and does not trigger another post-merge closure-reconciliation cycle.

## Closure Condition

Phase 0C is considered repository-closed when:

1. ADR-001 through ADR-004 are accepted;
2. Golden Reference and boundary/failure evidence is preserved;
3. material PR #4 is reviewed, passes required CI, and is merged;
4. the authoritative material merge commit is recorded;
5. local and remote material feature branches are removed;
6. local `main` is synchronized with `origin/main`;
7. this Phase 0C handoff is recorded;
8. `HANDOFF_INDEX.md` records Phase 0C as Closed;
9. the closure-reconciliation PR is merged;
10. local `main` is synchronized once more and the working tree is clean.

The closure-reconciliation PR does not itself become a new milestone and does not recursively require another closure reconciliation.

**Final Material Status: Closed.**
