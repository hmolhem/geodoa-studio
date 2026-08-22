# GeoDOA Studio — Phase 0B Python Engineering Toolchain Handoff

## Milestone Identity

- Project: GeoDOA Studio
- Milestone: Phase 0B — Python Engineering Toolchain
- Branch: `chore/phase0-python-toolchain`
- Pull Request: #2
- Merge Commit: `fac6b1d4208a1d529943b3e5dfb10260b15e7540`
- Status: Closed ? merged via PR #2
- Scientific implementation: None

## Objective

Establish a reproducible, typed, testable, cross-platform Python engineering
toolchain before introducing scientific geometry, array-processing, DOA, GUI,
or FPGA implementation.

Phase 0B converts the repository from a structural bootstrap into an executable
Python software project with explicit packaging, quality gates, text policies,
testing, and continuous integration.

## Scope Completed

- Python package build configuration established through `pyproject.toml`.
- Hatchling selected as the initial build backend.
- `src/geodoa` explicitly configured as the wheel package.
- Python support policy established as `>=3.12,<3.15`.
- Editable installation validated with `python -m pip install -e .`.
- Package import validated from the repository source tree.
- Ruff configured for linting and formatting.
- mypy configured for static type checking.
- pytest configured with strict project-level test discovery and validation.
- Initial package-import infrastructure test added.
- `.gitignore` established for Python, tooling, build, IDE, OS, and local
  PowerShell artifacts.
- `.gitattributes` established for cross-platform text normalization.
- Repository text files normalized to LF, with explicit Windows-script and
  binary-file exceptions.
- Reusable PowerShell repository tooling introduced through
  `scripts/powershell/GeoDOA.DevTools.psm1`.
- GitHub Actions CI introduced for pull requests and pushes to `main`.
- CI validates all declared Python minor versions: 3.12, 3.13, and 3.14.
- No scientific implementation introduced.

## Python Engineering Contract

The repository-level Python contract is defined in `pyproject.toml`.

Current project metadata:

- Distribution name: `geodoa`
- Package namespace: `geodoa`
- Version: `0.1.0`
- Python policy: `>=3.12,<3.15`
- Build backend: Hatchling
- Source layout: `src/geodoa`

Current development tooling:

- Ruff
- mypy
- pytest

Scientific runtime dependencies are deliberately not declared yet because
Phase 0B contains no scientific numerical implementation requiring them.

The local Conda environment is a development environment only. It is not the
project dependency contract. The repository configuration remains the
authoritative software-engineering specification.

## Ruff Policy

Ruff is configured with:

- Python target: 3.12
- Line length: 88
- Source roots: `src`, `tests`
- Rule families:
  - `E`
  - `F`
  - `I`
  - `UP`
  - `B`
- Double-quoted formatting
- Space indentation

Validated commands:

```text
ruff check .
ruff format --check .
```

Both pass.

## Static Type Policy

mypy is configured for Python 3.12 with explicit type-quality checks including:

- `warn_unused_configs = true`
- `warn_return_any = true`
- `disallow_untyped_defs = true`
- `check_untyped_defs = true`
- `no_implicit_optional = true`

Validated command:

```text
mypy src
```

Result:

```text
Success: no issues found in 1 source file
```

## Test Policy

pytest is configured to use:

```text
testpaths = ["tests"]
```

with:

```text
-ra
--strict-markers
--strict-config
```

Initial infrastructure test:

```text
tests/test_package_import.py
```

The test verifies that the installed project package can be imported.

Local result:

```text
1 passed
```

## Editable Installation Verification

The project was successfully installed in editable mode with:

`python -m pip install -e .`

The package import was then verified with:

`import geodoa`

The resolved package path was:

`C:\MyDocument\geodoa-studio\src\geodoa\__init__.py`

This confirms that the development environment is using the repository source
tree directly.

## Text and Line-Ending Policy

The repository uses `.gitattributes` to establish a consistent cross-platform
text policy.

Canonical repository text files use LF line endings.

Windows-native command scripts may use CRLF where explicitly configured, while
binary files are excluded from text normalization.

This policy supports consistent behavior across Windows development,
GitHub Actions on Linux, and future PYNQ/Linux environments.

## PowerShell Development Utilities

Reusable repository utilities are stored in:

`scripts/powershell/GeoDOA.DevTools.psm1`

The module currently exports:

- `Test-TextWhitespace`
- `Test-FinalNewline`
- `Repair-FinalNewline`

`Test-TextWhitespace` detects unintended trailing spaces and tabs while allowing
exactly two trailing spaces in Markdown as an intentional hard line break.

During validation, a PowerShell single-line-file edge case was discovered and
corrected by forcing `Get-Content` output into array semantics.

The corrected implementation uses:

`$lines = @(Get-Content -LiteralPath $Path -Encoding UTF8)`

A negative test containing three trailing spaces correctly returned FAIL.

`Test-FinalNewline` validates the presence of a final LF character.

`Repair-FinalNewline` provides explicit remediation when the final newline is
missing.

## Local Verification Gate

The Phase 0B local engineering gate passed:

- Python configuration: PASS
- Editable package installation: PASS
- `import geodoa`: PASS
- Ruff lint: PASS
- Ruff format: PASS
- mypy: PASS
- pytest: PASS
- Trailing-whitespace validation: PASS
- Final-newline validation: PASS
- Git staged whitespace check: PASS

Local validation environment included Python 3.12.12 and pytest 9.0.3.

## Continuous Integration

GitHub Actions workflow:

`.github/workflows/ci.yml`

The workflow executes for:

- pushes to `main`
- pull requests targeting `main`

The declared CI matrix validates:

- Python 3.12
- Python 3.13
- Python 3.14

Each CI job performs:

- repository checkout
- Python setup
- pip upgrade
- editable installation with development dependencies
- Ruff lint
- Ruff format validation
- mypy
- pytest

Pull Request #2 passed CI on Python 3.12, Python 3.13, and Python 3.14.

## Repository Scope Audit

Phase 0B contains engineering-toolchain and infrastructure changes only.

Primary implementation files are:

- `.gitattributes`
- `.github/workflows/ci.yml`
- `.gitignore`
- `pyproject.toml`
- `scripts/powershell/GeoDOA.DevTools.psm1`
- `tests/test_package_import.py`

No geometry implementation, DOA estimator, coarray algorithm, scientific
numerical kernel, GUI, FPGA kernel, ALSS implementation, or scientific
benchmark was introduced.

## Deliberately Deferred

The following remain outside Phase 0B:

- NumPy/SciPy scientific runtime dependency declaration
- Pydantic domain models
- Typer CLI implementation
- Dash GUI implementation
- geometry domain entities
- geometry-family generators
- physical geometry metrics
- steering-vector and manifold implementation
- covariance processing
- MUSIC and other DOA estimators
- coarray processing
- MIMO virtual-array processing
- ALSS integration
- fixed-point modeling
- FPGA/SoC integration
- Monte Carlo benchmarking
- scientific convention ADRs

Dependencies and scientific capabilities will be introduced only when an
approved bounded engineering work package requires them.

## Phase 0A Historical Reconciliation

During the Phase 0B closure audit, the repository handoff history was found to
still describe Phase 0A Pull Request #1 as open.

GitHub history confirms that PR #1 was merged.

Phase 0A merge commit:

`67e776b11040c33bab28d2cdf4b0ae6742c4bc86`

The Phase 0A handoff and `HANDOFF_INDEX.md` are therefore reconciled during
Phase 0B closeout so that repository history remains authoritative.

## Closure Condition

Phase 0B becomes fully closed when:

1. this handoff is committed to the Phase 0B branch;
2. `HANDOFF_INDEX.md` is updated;
3. stale Phase 0A closure metadata is reconciled;
4. the updated branch passes local quality gates;
5. Pull Request #2 passes GitHub Actions after the documentation update;
6. Pull Request #2 is reviewed and merged;
7. the remote Phase 0B branch is removed;
8. the local Phase 0B branch is removed;
9. local `main` is synchronized with `origin/main`;
10. the repository working tree is clean.

All repository lifecycle conditions for the material Phase 0B work package
were satisfied. Pull Request #2 was merged into `main` at merge commit
`fac6b1d4208a1d529943b3e5dfb10260b15e7540`. The local and remote feature branches were removed, local
`main` was synchronized with `origin/main`, and a clean working tree was
verified.

The final merge metadata is recorded through the project's post-merge closure
reconciliation procedure.

**Final Status: Closed.**
