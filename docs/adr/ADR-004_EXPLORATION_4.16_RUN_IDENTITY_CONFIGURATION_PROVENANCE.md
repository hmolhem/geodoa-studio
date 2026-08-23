# ADR-004 Exploration 4.16 — Run Identity, Configuration Hash, and Provenance

- **ADR:** ADR-004 — Validation, Reproducibility, and Scientific Evidence
- **Phase:** 0C — Scientific Foundations
- **Exploration:** 4.16
- **Status:** EXPLORATION COMPLETE — CANDIDATE CONTRACT, NOT ACCEPTED
- **Depends on:** Accepted ADR-001, ADR-002, ADR-003; ADR-004 Explorations 4.1–4.15

## 1. Question

> What information shall uniquely identify a GeoDOA scientific run, condition, trial ensemble, configuration, dataset/calibration artifact, software state, and hardware build strongly enough that another engineer can reconstruct what was executed and determine whether two results are scientifically comparable or exact replays?

This exploration defines the provenance backbone for reproducibility, auditability, publication packages, deterministic replay, fair comparison, and float/fixed/FPGA traceability.

---

## 2. Core Principle

A timestamp, folder name, plot filename, Git branch name, or single random seed is not a scientific run identity.

Candidate rule:

> A GeoDOA run shall be identified by a versioned provenance record that separates semantic scientific configuration from execution metadata and links the exact software revision, stochastic contract, external artifacts, calibration state, and hardware build used to produce the evidence.

A result is reproducible only to the extent that its dependencies are themselves identifiable and reconstructable.

---

## 3. Identity Layers

GeoDOA shall distinguish several nested identities.

```text
Study Identity
  └─ Condition Identity
       └─ Trial Identity / Trial Ensemble
            └─ Method/Implementation Identity
                 └─ Run / Execution Identity
                      └─ Derived Artifact Identity
```

These identities answer different questions and shall not be collapsed into one filename.

---

## 4. Study Identity

A study defines the scientific question and benchmark family.

Candidate study identity fields include:

```text
study_id
study_contract_version
scientific objective
profile / ADR versions
condition-grid definition
trial semantics
comparison policy
metric policy
failure policy
uncertainty policy
```

Candidate rule:

> Study identity shall remain stable across reruns that intentionally reproduce the same scientific design, while execution/run identities may differ.

---

## 5. Condition Identity

A condition is a deterministic point or declared distribution within a study.

Examples:

```text
geometry = ULA-8
source DOAs = {-5 deg, +5 deg}
SNR = 0 dB under SNR profile X
snapshots = 100
source correlation = 0
sensor profile = Phase1-Ideal
algorithm profile = MUSIC-vX
```

Candidate rule:

> Condition identity shall derive from canonical semantic fields, not from loop order, row number, plotting order, or human-formatted labels.

---

## 6. Trial Identity

Explorations 4.4–4.5 established that trial identity is scientific, not execution-order identity.

Conceptually:

\[
I_{trial}
=
( I_{study}, I_{condition}, i_{trial}, V_{stoch} ).
\]

Candidate rule:

> Trial identity shall remain stable across resume, parallel execution, algorithm reordering, worker-count changes, and retry of the same realization.

A replacement realization is a new trial identity.

---

## 7. Method / Implementation Identity

The same scientific algorithm may have multiple implementations.

Examples:

```text
MUSIC scientific profile v3
Python float64 implementation
NumPy float32 implementation
fixed-point model Q...
HLS build
RTL implementation
FPGA bitstream
```

Candidate rule:

> Algorithm identity and implementation identity are distinct. A run shall identify both.

This prevents an implementation change from silently masquerading as the same scientific method.

---

## 8. Run / Execution Identity

A run is one concrete execution of a study/condition/method configuration.

A run identity may include a generated unique token for operational convenience, but that token alone is not reproducibility evidence.

Candidate rule:

> Human/operational `run_id` and semantic/content identities shall coexist: the run ID locates one execution; provenance explains what that execution means.

---

## 9. Configuration Identity versus Run Identity

Two separate executions can have the same semantic configuration and therefore the same configuration fingerprint, while differing in:

```text
wall-clock time
host machine
worker count
output directory
execution scheduler
log formatting
```

Candidate rule:

> Configuration identity shall exclude non-semantic execution metadata unless that metadata can affect scientific output.

Conversely, any execution setting known to affect numerical/scientific results must be promoted into semantic provenance.

---

## 10. Canonical Configuration Representation

Hashing is meaningful only if the representation is canonical.

Candidate canonicalization requirements:

```text
stable field names
stable field ordering
explicit schema version
explicit units
explicit numeric representation
explicit categorical values
explicit null/optional semantics
stable list ordering where order is scientific
set canonicalization where order is not scientific
no locale-dependent formatting
no hidden defaults
no environment-dependent implicit values
```

Candidate rule:

> GeoDOA shall hash a canonical semantic configuration representation, not arbitrary YAML/JSON text bytes as authored by a user.

Equivalent scientific configurations should not receive different identities merely because whitespace or key order differs.

---

## 11. Units Are Part of Canonical Semantics

The following shall not be treated as distinct scientific configurations merely because one was entered in another compatible unit:

```text
0.5 m
50 cm
```

if canonical conversion is exact under the profile.

Candidate rule:

> Canonical configuration shall normalize quantity values into declared canonical units before semantic hashing while retaining original user-facing input where useful for audit.

No silent dimensionless coercion is allowed.

---

## 12. Floating-Point Canonicalization

Floating-point values require stable serialization.

Weak approaches include locale-formatted decimal strings or implementation-dependent `repr` assumptions without a versioned rule.

Candidate rule:

> The governing implementation shall define a versioned canonical floating-point serialization sufficient to distinguish scientifically different values and reproduce the exact configured binary/decimal quantity semantics.

Possible implementation strategies include canonical decimal serialization or canonical IEEE binary encoding. The scientific contract requires determinism; the final library mechanism is not frozen here.

---

## 13. Derived Values versus Authoritative Inputs

Some configuration values are derived from others.

Example:

```text
frequency f
wave speed v
wavelength lambda = v/f
```

Candidate rule:

> Authoritative inputs and derived values shall be distinguishable. The semantic configuration identity shall not depend on independently user-entered redundant values unless the profile explicitly treats both as authoritative and checks consistency.

Derived values should be recorded for audit but not create accidental duplicate semantics.

---

## 14. Defaults Must Become Explicit

A hidden software default can change across versions.

Examples:

```text
eigensolver tolerance
search grid
peak threshold
normalization
rounding mode
number of workers
BLAS threading
```

Candidate rule:

> Any default that can affect scientific output shall be materialized into the resolved configuration/provenance record before execution.

A later library default change must not redefine an old run silently.

---

## 15. Configuration Schema Version

Canonical identity semantics may evolve.

Candidate rule:

> Every resolved configuration shall carry a schema/contract version; configuration hashes from different canonicalization schema versions shall not be assumed directly equivalent merely because their field values look similar.

Migration/equivalence requires an explicit compatibility rule.

---

## 16. Configuration Fingerprint

A content fingerprint may be conceptually defined as

\[
H_{config}=H(\mathrm{canonical\_semantic\_config}).
\]

Candidate rule:

> GeoDOA shall use a cryptographic content hash suitable for stable artifact identity; SHA-256 is the candidate baseline unless the governing implementation adopts another versioned cryptographic hash with equivalent provenance properties.

The algorithm name/version is part of provenance.

A hash is an identity aid, not a substitute for retaining the human-readable resolved configuration.

---

## 17. Hashes Are Not Scientific Meaning

Two different hashes prove only that canonicalized content differs; they do not explain whether the difference is scientifically material.

Candidate rule:

> Configuration comparison shall retain field-level semantic diff capability in addition to content hashes.

Similarly, equal hashes under the same schema indicate equal canonical content, not physical validity.

---

## 18. Source-Code Provenance

Publication-grade runs shall identify the exact source state.

Candidate fields include:

```text
repository identity
Git commit SHA
branch/tag as convenience metadata
working-tree clean/dirty status
submodule SHAs if used
patch/diff identity if dirty execution is allowed
```

Candidate rule:

> Branch name alone is insufficient because branches move; Git commit identity is authoritative for committed source provenance.

---

## 19. Dirty Working Tree

Running scientific evidence from uncommitted modifications may be useful during development but weakens reconstructability.

Candidate rule:

> Publication/final benchmark evidence should default to a clean committed source state. If a dirty run is permitted, the exact diff/patch or equivalent content identity shall be captured and the run labeled accordingly.

`dirty=true` without the actual diff is insufficient for exact reconstruction.

---

## 20. Software Environment Provenance

Numerical results may depend on software versions.

Candidate provenance includes, as applicable:

```text
Python version
GeoDOA package version
NumPy/SciPy versions
BLAS/LAPACK backend
compiler version
OS/platform
architecture
critical dependencies
container/environment lock identity
```

Candidate rule:

> Environment provenance shall be proportional to reproducibility risk; critical numerical dependencies shall not be omitted when exact or close numerical replay is claimed.

---

## 21. Dependency Lock versus Full Machine Snapshot

A complete machine image is not always necessary.

Candidate rule:

> GeoDOA shall distinguish minimum scientific environment provenance from stronger exact-environment capture. Reproducibility level claimed shall match the retained environment evidence.

This aligns with Exploration 4.5's exact-realization versus distributional/aggregate reproduction distinction.

---

## 22. Hardware / Host Provenance

For runtime and hardware evidence, additional provenance may include:

```text
CPU model
core/thread settings
RAM where relevant
GPU model if used
FPGA part/board
clock configuration
board revision
host-interface path
```

Candidate rule:

> Hardware environment is mandatory provenance for performance/timing claims and may be optional for purely deterministic mathematical equality when the environment cannot affect the result.

---

## 23. FPGA Build Identity

Exploration 4.15 requires exact hardware-build provenance.

Candidate fields include:

```text
source Git SHA
HLS/RTL source identity
Vivado/Vitis/HLS tool version
IP-core versions
FPGA part/board
constraints identity
clock targets
HLS directives/pragmas
synthesis/implementation settings
build seed where material
bitstream content hash
hardware handoff/XSA or equivalent artifact hash
```

Candidate rule:

> Board evidence shall identify the exact programmed implementation artifact, not merely the project directory or bitstream filename.

---

## 24. Data Artifact Provenance

Input datasets/artifacts shall be content-addressable or otherwise strongly identifiable.

Candidate fields:

```text
artifact_id
content hash
schema/format version
source/origin
creation/acquisition timestamp if meaningful
units/frame/channel ordering
parent lineage
immutable raw artifact identity
transform history
```

Candidate rule:

> Filename and filesystem path are location metadata, not sufficient data identity.

---

## 25. Raw versus Derived Data

Derived data may include filtering, resampling, calibration, channel selection, interpolation, normalization, or format conversion.

Candidate rule:

> Derived artifacts shall preserve lineage to immutable/source artifacts and the exact transformation configuration/software identity used to create them.

A derived CSV exported from a raw binary capture is not the same provenance object as the raw capture.

---

## 26. Calibration Artifact Provenance

Calibration is state/domain dependent under ADR-003.

Candidate calibration provenance includes:

```text
calibration artifact content hash
calibration method/profile version
reference evidence
valid frequency/range/temperature/state domain
reference plane
channel/port identity
creation time and validity interval if applicable
parent raw calibration data
software/tool version
uncertainty metadata
```

Candidate rule:

> A run using calibration shall identify the exact calibration artifact and validity state; `calibrated=true` is not sufficient provenance.

---

## 27. External Tool / CST Provenance

External numerical/model artifacts require provenance such as:

```text
tool name/version
project/model identity
solver settings
mesh/discretization settings
frequency/direction grid
reference plane
export format
export content hash
postprocessing transform lineage
```

Candidate rule:

> External-tool output is an artifact with provenance and epistemic role; it shall not become anonymous `truth` merely by being imported.

---

## 28. Randomness Provenance

Exploration 4.5 requires more than one seed.

Candidate run-level stochastic provenance includes:

```text
root seed / seed-set
stochastic contract version
RNG/bit-generator family
library/version semantics
child-stream derivation policy version
condition identity
trial identities
random-family identities
redraw scopes
CRN/pairing policy
algorithm-internal RNG policy
bootstrap/resampling RNG policy
```

Candidate rule:

> Exact stochastic replay requires the stochastic derivation semantics, not only the root-seed integer.

---

## 29. Canonical Trial Ensemble Identity

A final aggregate metric depends on which trials were included.

Candidate ensemble provenance includes:

```text
requested trial IDs
completed trial IDs
failed trial IDs
excluded trial IDs + reasons
replacement trial IDs if any
canonical ordering for diagnostics
```

Candidate rule:

> Aggregate evidence shall identify its contributing trial ensemble; `N=1000` alone is insufficient.

---

## 30. Failure / Eligibility Provenance

Exploration 4.13 established typed failure states.

Candidate rule:

> Provenance shall preserve the failure taxonomy version, per-trial status, and metric-specific eligibility policy used in aggregation.

Otherwise two identical raw trial sets could produce different reported metrics without an auditable explanation.

---

## 31. Metric / Association / Uncertainty Policy Provenance

Derived results depend on analysis contracts.

Candidate references include:

```text
association policy/version
metric definition/version
resolution event/version
failure mapping policy
aggregation weighting
confidence interval method/level
stopping/adequacy policy
```

Candidate rule:

> Scientific results shall identify the analysis policy versions that transformed trial evidence into reported metrics.

---

## 32. Output Artifact Identity

Plots, tables, JSON summaries, CSV files, reports, and publication figures are derived artifacts.

Candidate rule:

> Important derived outputs shall be linkable to the run/result identity and, where archival integrity matters, have content hashes or equivalent immutable artifact identifiers.

A figure without provenance should not be the only surviving scientific evidence.

---

## 33. Timestamp Role

Timestamps are useful for chronology, acquisition validity, and operational audit.

Candidate rule:

> Wall-clock timestamp is metadata, not scientific identity, unless time itself is a declared physical condition/state variable.

Rerunning the same experiment tomorrow should not change the semantic configuration fingerprint solely because the timestamp changed.

---

## 34. Hostname / Username / Path Role

Hostnames, usernames, and absolute paths can help debugging but are unstable across machines and may expose unnecessary personal/environment information.

Candidate rule:

> Host/path/user metadata shall not enter semantic scientific hashes unless scientifically required; portable artifact identifiers and repository-relative paths are preferred in publication provenance.

Sensitive credentials/secrets shall never be embedded in provenance records.

---

## 35. Secrets and Credentials

API keys, access tokens, passwords, private credentials, and security material are not reproducibility metadata.

Candidate rule:

> Provenance records shall identify required external dependencies/services without storing secrets. Secret values shall be excluded from hashes, logs, reports, and publication artifacts.

---

## 36. Environment Variables

Environment variables may contain either scientific settings or secrets/runtime convenience values.

Candidate rule:

> Environment variables that materially affect scientific output must be resolved into explicit non-secret configuration provenance; unrelated or secret environment variables shall not be captured indiscriminately.

---

## 37. Reproducibility Levels

Candidate reproduction levels:

### R1 — Semantic reconstruction

Reconstruct the scientific configuration, inputs, algorithms, and policies.

### R2 — Exact stochastic realization reconstruction

Additionally reconstruct the same trial random realizations.

### R3 — Numerical implementation replay

Additionally reproduce the software environment/reference implementation closely enough for equivalent numerical results.

### R4 — Exact implementation/build replay

Additionally identify exact fixed/HLS/RTL/FPGA build artifacts and toolchain state.

### R5 — Physical experiment reconstruction

Additionally reconstruct hardware setup, calibration, environment, reference instruments, and acquisition conditions as far as physically possible.

Candidate rule:

> A result shall not claim a stronger reproducibility level than its retained provenance supports.

These labels are candidate conceptual levels, not final public API names.

---

## 38. Exact Replay versus Scientific Reproduction

Exact byte-for-byte output replay may fail across compliant numerical environments because of floating-point library/order differences, while scientific conclusions remain reproducible.

Candidate rule:

> Exact artifact replay, numerical equivalence, statistical reproduction, and scientific conclusion reproduction are distinct claims and shall be labeled accordingly.

---

## 39. Semantic Diff between Runs

A comparison tool should eventually be able to answer:

```text
What changed between Run A and Run B?
```

Candidate diff classes:

```text
scientific condition changed
stochastic ensemble changed
algorithm/hyperparameter changed
sensor/calibration profile changed
analysis policy changed
software revision changed
hardware build changed
execution-only metadata changed
```

Candidate rule:

> Provenance design shall support field-level semantic diff, not only hash comparison.

---

## 40. Immutable Accepted Evidence

Once a result is cited in an accepted ADR/gate/publication artifact, mutable regeneration under the same name can destroy auditability.

Candidate rule:

> Accepted evidence artifacts shall be immutable or versioned/content-addressed; regeneration after code/config changes creates a new evidence identity.

Human-friendly aliases may point to immutable revisions but shall not redefine them silently.

---

## 41. Cached Results

Caching can improve performance but creates reproducibility risk if cache keys omit scientific dependencies.

Candidate rule:

> Scientific caches shall be keyed by all material semantic dependencies or treated only as disposable acceleration artifacts. Cache hits shall not silently reuse results from incompatible configurations/software states.

---

## 42. Partial Resume

Long Monte Carlo studies may resume after interruption.

Candidate rule:

> Resume shall preserve existing trial identities/results, schedule only missing declared trials, and retain the original study/condition/stochastic contract. Resume shall not silently regenerate completed trials with new realizations.

If existing evidence is invalidated by a software/config change, a new run identity is required.

---

## 43. Parallel Execution

Parallel worker count and scheduling should not alter trial semantics under Exploration 4.5.

Candidate rule:

> Execution topology belongs to operational provenance; if changing thread/worker settings can alter numerical results, those settings must also be recorded as numerically material environment provenance.

---

## 44. Nondeterministic Libraries / Hardware

Some algorithms/libraries/hardware operations may be nondeterministic even with identical inputs.

Candidate rule:

> Known nondeterminism shall be declared as an implementation property, with controls/settings recorded when available. An exact-replay claim is invalid if nondeterminism is materially uncontrolled.

Distributional/scientific reproduction may still be possible.

---

## 45. Provenance Completeness versus Practicality

Capturing every machine detail creates noise; capturing too little destroys reproducibility.

Candidate rule:

> Provenance shall follow a dependency principle: retain every input, policy, software/hardware state, and external artifact that can materially affect the claimed evidence, plus enough operational metadata to diagnose execution.

The governing profile may define minimum required fields by evidence type.

---

## 46. Provenance Validation

A provenance record itself can be malformed or incomplete.

Candidate checks include:

```text
schema validity
required-field presence
hash verification
artifact existence
Git SHA resolvability
calibration-domain compatibility
trial-set consistency
no duplicate trial IDs
metric-count reconciliation
hardware build/artifact consistency
```

Candidate rule:

> Publication-grade evidence shall validate its provenance record before acceptance.

---

## 47. Candidate Minimal Scientific Run Record

A conceptual minimal record may include:

```text
run_id
study_id / study_contract_version
resolved_config_schema_version
resolved_config + config_hash
condition identities
method + implementation identity
repository + Git commit SHA + clean/dirty state
software environment summary
root seed + RNG/stream policy version
trial ensemble identities/status
input data/artifact hashes
calibration artifact identity, if used
external-tool artifact identity, if used
association/metric/failure/uncertainty policy versions
output/evidence artifact identities
execution start/end timestamps as metadata
hardware/build identity, if applicable
reproducibility-level claim
```

No final JSON/Python schema is accepted in Phase 0C.

---

## 48. Candidate Phase-1 Provenance Profile

For initial synthetic Phase-1 DOA studies, a conservative candidate minimum is:

```text
accepted ADR/profile versions
resolved scientific config in canonical units
configuration schema version + cryptographic hash
Git commit SHA; clean worktree preferred
Python + critical numerical library versions
geometry/source/noise/SNR/snapshot semantics
algorithm/postprocessor configuration
root seed + RNG derivation policy
condition/trial identities
association/metric/failure policy versions
requested/completed/failed/excluded trial counts + IDs
result summary + evidence artifact identities
```

For fixed/FPGA runs additionally:

```text
fixed-point arithmetic profile
HLS/RTL source revision
toolchain/IP/part/board/clock identities
bitstream/build artifact hash
canonical stimulus identity
hardware timing/resource scope
```

This remains candidate until ADR-004 acceptance.

---

## 49. Invalid / Weak Provenance Practices

The following are scientifically weak or invalid unless explicitly bounded:

1. identify a result only by timestamp or folder name;
2. record only branch name and omit Git commit SHA;
3. run from a dirty tree and record only `dirty=true` without preserving the diff;
4. hash arbitrary YAML/JSON text where whitespace/key order changes identity;
5. omit units/default resolution from configuration identity;
6. use a single root seed as the entire stochastic provenance record;
7. identify datasets/calibration only by filename/path;
8. overwrite a cited result artifact in place after code/config changes;
9. omit failed/excluded trial identities from aggregate provenance;
10. save a figure but not the underlying run/result identity;
11. treat environment timestamps/hostnames as semantic config fields;
12. store credentials/tokens inside provenance or configuration hashes;
13. claim exact replay without numerical-library/toolchain provenance;
14. claim FPGA reproducibility from bitstream filename without content/build identity;
15. reuse cache entries whose keys omit material scientific dependencies;
16. resume a study by regenerating prior trial IDs with new random realizations;
17. compare configuration hashes without retaining human-readable semantic diff capability.

---

## 50. Cross-ADR Reconciliation

### ADR-001

Coordinate, phase-reference, channel-identity, units, geometry, and ordering conventions are semantic configuration dependencies and therefore part of provenance/profile identity.

### ADR-002

Signal, SNR, snapshot, covariance, source/noise, MIMO provenance, and approximation profiles are semantic scientific configuration fields.

### ADR-003

Sensor/calibration/reference-plane/artifact state and calibration-domain validity require explicit artifact/configuration provenance.

### ADR-004 Explorations 4.2–4.3

Truth/reference and deterministic evidence artifacts require lineage and immutable/content-addressed identity.

### ADR-004 Explorations 4.4–4.5

Study/condition/trial identities and stochastic child-stream derivation become first-class provenance dependencies.

### ADR-004 Explorations 4.6–4.14

Association, metrics, eligibility, failure, convergence, uncertainty, and comparison policies are versioned analysis dependencies.

### ADR-004 Exploration 4.15

Fixed-point profiles, canonical stimuli, toolchains, FPGA build artifacts, timing scope, and board identity become hardware provenance dependencies.

**Cross-ADR result: no contradiction identified.**

---

## 51. Candidate Decisions from Exploration 4.16

- **D4.16-01:** Study, condition, trial, method/implementation, run, and derived-artifact identities are distinct provenance layers.
- **D4.16-02:** Operational run IDs locate executions; semantic/content identities establish reproducibility/comparability.
- **D4.16-03:** Condition/configuration identity derives from a versioned canonical semantic representation, not loop order, filenames, or arbitrary source-text serialization.
- **D4.16-04:** Canonical configuration makes units, defaults, numeric representation, ordering/set semantics, and authoritative-versus-derived fields explicit.
- **D4.16-05:** A cryptographic content hash is the candidate configuration/artifact fingerprint mechanism; SHA-256 is the candidate baseline, with algorithm/version provenance.
- **D4.16-06:** Human-readable resolved configuration and semantic field-level diff remain required; hashes do not replace scientific meaning.
- **D4.16-07:** Exact committed Git SHA is authoritative source provenance; branch names are convenience metadata.
- **D4.16-08:** Publication-grade runs should use clean committed source; dirty runs require preserved exact patch/content identity.
- **D4.16-09:** Critical numerical software/dependency versions are provenance whenever they can affect the claimed reproducibility level.
- **D4.16-10:** Data, calibration, external-tool, and derived artifacts require immutable/content-addressed identity and parent transformation lineage where material.
- **D4.16-11:** Exact stochastic replay requires RNG/bit-generator and child-stream derivation semantics plus condition/trial/random-family identities, not only a root seed.
- **D4.16-12:** Aggregate metrics identify the exact contributing trial ensemble, including failed/excluded/replacement identities and reasons.
- **D4.16-13:** Association, metric, failure, aggregation, uncertainty, and stopping-policy versions are analysis provenance dependencies.
- **D4.16-14:** Accepted/cited evidence artifacts are immutable or versioned/content-addressed; regeneration creates a new evidence identity.
- **D4.16-15:** Timestamps, hostnames, usernames, and paths are operational metadata unless scientifically material and shall not normally enter semantic hashes.
- **D4.16-16:** Secrets/credentials are excluded from provenance records and hashes; material non-secret environment settings are resolved explicitly.
- **D4.16-17:** Reproducibility claims shall distinguish semantic reconstruction, exact stochastic replay, numerical replay, exact implementation/build replay, and physical experiment reconstruction.
- **D4.16-18:** Cache/resume/parallel execution shall preserve semantic trial/config identities and must not silently change scientific realizations.
- **D4.16-19:** Known numerical/execution nondeterminism is an implementation property that constrains exact-replay claims and must be declared.
- **D4.16-20:** FPGA evidence identifies exact source/tool/IP/part/constraints/directives/build/bitstream artifacts, not merely project or filename.
- **D4.16-21:** Provenance records themselves require schema/hash/lineage/count/compatibility validation before publication-grade acceptance.

---

## 52. Exploration 4.16 Conclusion

Exploration 4.16 is complete at candidate-contract level.

The central rule is:

> GeoDOA shall make every scientific result traceable through versioned identities for study, condition, trial ensemble, algorithm/implementation, resolved semantic configuration, source revision, stochastic streams, data/calibration/external artifacts, analysis policies, software environment, and hardware build. Content hashes support immutable identity, but human-readable semantic configuration and dependency lineage remain authoritative for interpretation; timestamps, paths, branch names, and single seed values shall never substitute for reproducibility provenance.

No acceptance gate is started or passed by this exploration.

The next exploration is:

```text
4.17 — Publication Evidence and Reproducibility Package
```
