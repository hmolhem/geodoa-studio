# ADR-004 Exploration 4.17 — Publication Evidence and Reproducibility Package

- **ADR:** ADR-004 — Validation, Reproducibility, and Scientific Evidence
- **Phase:** 0C — Scientific Foundations
- **Exploration:** 4.17
- **Status:** EXPLORATION COMPLETE — CANDIDATE CONTRACT, NOT ACCEPTED
- **Depends on:** Accepted ADR-001, ADR-002, ADR-003; ADR-004 Explorations 4.1–4.16

## 1. Question

> What evidence artifacts, manifests, configuration records, trial summaries, figures/tables, software/hardware provenance, and replay instructions shall GeoDOA preserve so that a publication-grade result can be independently audited, reproduced, compared, and traced back to the exact scientific run that generated it?

This exploration defines the publication/reproducibility package assembled from the provenance, metric, uncertainty, failure, and validation contracts developed earlier in ADR-004.

---

## 2. Core Principle

A paper figure or table is not the scientific evidence package.

Candidate rule:

> Every publication-grade claim shall be traceable from manuscript figure/table/text claim to an immutable evidence package containing the resolved scientific configuration, exact run/provenance identity, trial-level or sufficient intermediate evidence, analysis policies, uncertainty, failures, and software/hardware dependencies needed to reconstruct the result at the claimed reproducibility level.

The package should allow another engineer to answer:

```text
What exactly was run?
With which assumptions and conventions?
On which trials/data/hardware?
Using which code/config/calibration/build?
How were failures and exclusions handled?
How was the plotted/table value computed?
Can I recreate the same scientific result?
```

---

## 3. Publication Evidence Is Layered

Candidate package layers:

```text
P0 — claim/index layer
P1 — resolved study/run configuration
P2 — provenance + environment + artifact lineage
P3 — trial/condition evidence and aggregate metrics
P4 — figure/table generation inputs and scripts
P5 — deterministic reference / verification evidence
P6 — hardware/build evidence when applicable
P7 — human-readable reproduction instructions
```

Candidate rule:

> A reproducibility package shall preserve enough of each applicable layer to support the stated claim; one exported PDF/PNG shall never be the sole evidence object.

---

## 4. Claim-to-Evidence Traceability

A publication may contain claims such as:

```text
Algorithm A reduces RMSE by 18%
Geometry B achieves P_res >= 0.9 at 2.5 deg separation
Fixed-point implementation is noninferior within delta
FPGA kernel achieves 4.2 us latency
```

Candidate rule:

> Each material quantitative claim should map to one or more stable evidence identifiers that resolve to the exact metric definition, condition domain, trial ensemble, comparison policy, uncertainty result, and source artifacts supporting the claim.

A claim ID may be a lightweight human-readable alias, but its evidence identity must be immutable/versioned.

---

## 5. Publication Manifest

A top-level manifest is the package entry point.

Candidate manifest fields include:

```text
package_id
package_schema_version
publication/study title or alias
repository + Git commit SHA
accepted ADR/profile versions
run IDs / result IDs included
config hashes
trial ensemble IDs
input/calibration/external artifact hashes
metric/association/failure/uncertainty policy versions
figure/table artifact IDs
software environment identity
hardware build identities, if applicable
reproducibility-level claim
known limitations / unresolved states
package content hashes
```

Candidate rule:

> The manifest shall identify package contents by semantic/content identity, not only relative filenames.

No final YAML/JSON schema is accepted in Phase 0C.

---

## 6. Immutable Resolved Configuration

The package shall include the resolved scientific configuration used for each result.

Candidate rule:

> Publication packages shall preserve resolved configuration after defaults, unit normalization, derived-profile resolution, and semantic canonicalization—not only the abbreviated user input file.

The resolved configuration should be human-readable and linked to its configuration hash from Exploration 4.16.

---

## 7. Original Input Configuration May Also Be Preserved

The original user-authored configuration can be useful for workflow understanding.

Candidate rule:

> Original configuration may be included as a convenience artifact, but the resolved canonical configuration is authoritative for reproduction.

Differences introduced by defaults/resolution should be auditable.

---

## 8. Run Provenance Record

Each publication run/result shall include the applicable Exploration 4.16 provenance record:

```text
study / condition / trial ensemble identities
algorithm + implementation identity
Git SHA / dirty-state evidence
software environment
RNG / stream policy
input artifact lineage
calibration artifact identity
external tool artifact identity
analysis policy versions
hardware build identity
```

Candidate rule:

> Publication packaging shall not create a second independent provenance system; it shall reference/freeze the authoritative run provenance.

---

## 9. Trial-Level Evidence versus Aggregate-Only Evidence

Full trial-level evidence is strongest when practical.

For each trial, candidate retained fields may include:

```text
trial identity
condition identity
truth/reference
method output
association outcome
matched errors
miss/false/resolution status
failure state
selected intermediate diagnostics
runtime/hardware metrics where relevant
```

Candidate rule:

> When storage allows, publication-grade stochastic results should preserve trial-level evidence sufficient to recompute aggregate metrics and uncertainty without rerunning the scientific estimator.

---

## 10. When Full Trial-Level Data Cannot Be Shared

Constraints may include:

```text
privacy
licensing
export restrictions
proprietary data size
instrument/vendor restrictions
large raw data volume
```

Candidate rule:

> If raw/trial-level data cannot be distributed, the package shall state the restriction and preserve the strongest legally/technically shareable derived evidence, metadata, hashes, schemas, and regeneration instructions without pretending full reproducibility is available.

Reproducibility level must be downgraded accordingly.

---

## 11. Aggregate Metric Record

For every reported aggregate metric, preserve at least:

```text
metric identity/version
point estimate
units/coordinate
condition/domain
aggregation weighting
requested/eligible/matched/failed counts
association/event policy
failure mapping policy
uncertainty method/level
confidence/bound result
adequacy/convergence status
trial ensemble identity
```

Candidate rule:

> A manuscript number without its metric contract, denominator, and uncertainty provenance is insufficient publication evidence.

---

## 12. Failure Evidence Must Be Included

Exploration 4.13 established that failure is scientific evidence.

Candidate package elements include:

```text
failure count by reason/stage
excluded trial identities + reasons
incompatibility states
unresolved states
retry/replacement history
survivor-only metric conditioning
```

Candidate rule:

> Publication packages shall not hide failure evidence merely because the main figure plots successful trials.

---

## 13. Comparison Evidence Package

For comparative claims, preserve:

```text
comparison contract
methods/geometries and versions
resource constraints
oracle information policy
same/different preprocessing
same/different postprocessing
CRN/pairing design
paired trial identities
per-condition effects
comparison uncertainty
practical margin/effect threshold
claim class: superiority / noninferiority / equivalence / tradeoff / inconclusive
```

Candidate rule:

> A headline `X% improvement` is not self-sufficient evidence; the absolute baseline, paired/condition-wise effects, uncertainty, and benchmark domain must remain available.

---

## 14. Deterministic Reference Evidence

Publication-grade software/hardware claims should preserve the deterministic verification evidence relevant to the released implementation.

Candidate elements include:

```text
GRP identifiers
inputs
expected exact/rounded results
actual results
pass/fail/tolerance evidence
reference derivations
independent arithmetic/checks
software version used
```

Candidate rule:

> Golden Reference Problems and deterministic implementation checks remain separate from Monte Carlo performance results but should be linked in the package when they support trust in the implementation.

---

## 15. Figure Provenance

Every publication figure should be reproducible from identified inputs.

Candidate figure record:

```text
figure_id
source result/run IDs
input data artifact hashes
generation script/module + Git SHA
plot configuration
axis units/scales/limits
normalization
filtering/aggregation
confidence band method
export format/version
final figure content hash
```

Candidate rule:

> A figure shall be treated as a derived artifact with lineage, not as an independent source of truth.

---

## 16. Table Provenance

Likewise, each table should identify:

```text
table_id
source metric/result IDs
row/column condition definitions
rounding/display precision
aggregation policy
uncertainty representation
sorting/ranking rule
final artifact hash
```

Candidate rule:

> Display rounding shall not alter the underlying stored metric values used for statistical or ranking decisions.

---

## 17. Manuscript Display Precision

Showing too many decimal places creates false precision; showing too few can hide relevant differences.

Candidate rule:

> Manuscript display precision shall reflect metric uncertainty, measurement/reference precision, and engineering relevance; the underlying machine-readable values shall retain sufficient precision for recomputation.

No universal decimal-place rule is accepted here.

---

## 18. Plot Normalization and Cropping

Publication plots often normalize or crop data.

Examples:

```text
spectrum normalized to 0 dB peak
error axis clipped to visible range
selected SNR range shown
smoothed curve plotted
```

Candidate rule:

> Any normalization, filtering, smoothing, clipping, interpolation, or condition selection used for publication visualization shall be explicit and reproducible from retained evidence.

Visualization transforms shall not redefine the underlying scientific metric silently.

---

## 19. Raw Data and Derived Data Separation

The package should preserve separation between:

```text
raw acquisition / generative source artifact
derived/preprocessed data
trial outputs
aggregate result tables
publication figures/tables
```

Candidate rule:

> Publication artifacts should be regenerable from the nearest authoritative upstream evidence without requiring reverse engineering of a figure image or manually edited spreadsheet.

---

## 20. No Manual Spreadsheet Edits as Hidden Scientific Steps

Manual spreadsheet cleanup can break reproducibility.

Candidate rule:

> Publication-grade metric transformation, filtering, aggregation, and table generation shall be scripted or otherwise captured as a deterministic documented transform; manual edits that affect scientific values require explicit recorded lineage.

Cosmetic layout edits are separate from scientific-value edits.

---

## 21. Reproduction Entry Points

A package should provide clear entry points such as:

```text
reproduce deterministic references
recompute aggregate metrics from retained trial evidence
regenerate figures/tables
rerun full simulation from configuration/seeds
rerun fixed/FPGA comparison where hardware available
```

Candidate rule:

> Reproduction instructions shall distinguish lightweight analysis replay from expensive full scientific rerun.

---

## 22. One-Command Reproduction Is Desirable but Not Mandatory

A robust command may eventually support:

```text
geodoa reproduce <package-id>
```

but not every physical/hardware experiment can be one-command reproducible.

Candidate rule:

> Automation level shall match the evidence type; lack of one-command automation does not invalidate a physical experiment if all required setup/calibration/procedure provenance is explicit.

---

## 23. Environment Reconstruction

Candidate package elements may include:

```text
pyproject/lockfile
requirements/environment export
container definition/image digest
compiler/toolchain versions
BLAS backend
OS/platform notes
```

Candidate rule:

> The package shall include enough environment information to support its claimed reproducibility level without implying that an environment lock alone proves scientific correctness.

---

## 24. Container Images

Containers can strengthen computational reproducibility.

Candidate rule:

> A container/image digest is useful environment provenance but shall not replace source/config/trial/artifact provenance, and a containerized incorrect implementation remains incorrect.

No container technology is mandated in Phase 0C.

---

## 25. Data/Artifact Checksums

Package validation should verify content identity.

Candidate rule:

> Publication packages should include cryptographic hashes for immutable evidence artifacts where practical and verify them during reproduction/audit.

A mismatch is a data-integrity failure, not an ignorable warning.

---

## 26. Package Self-Consistency Checks

Candidate checks include:

```text
manifest references all required artifacts
all listed artifacts exist
content hashes match
Git/config/run identities agree
trial counts reconcile
aggregate metrics recompute from trial evidence
figure/table source IDs resolve
failure counts reconcile
hardware build IDs match reported device evidence
```

Candidate rule:

> A package shall pass internal consistency validation before being called publication-ready.

---

## 27. Recompute-versus-Rerun Test

Two important package tests are distinct.

### 27.1 Recompute test

Recompute metrics/figures from retained trial/intermediate evidence.

### 27.2 Rerun test

Re-execute the scientific simulation/implementation from config, code, data, seeds, and environment.

Candidate rule:

> Publication-grade computational evidence should support at least recomputation and, where feasible, full rerun; passing recomputation alone does not prove the upstream simulation can be reproduced.

---

## 28. Independent Reproduction

Strong evidence may include a clean-environment or independent-machine reproduction.

Candidate rule:

> Independent reproduction is stronger than self-replay on the original development environment and should be recorded when performed, but it is not required for every exploratory result.

Final publication-critical results should prioritize it where practical.

---

## 29. Reproduction Discrepancy Classification

If reproduction differs, classify the discrepancy:

```text
IDENTICAL_ARTIFACT
NUMERICALLY_EQUIVALENT
STATISTICALLY_CONSISTENT
SCIENTIFIC_CONCLUSION_REPRODUCED
MATERIAL_DISCREPANCY
REPRODUCTION_BLOCKED_BY_MISSING_DEPENDENCY
UNRESOLVED
```

Candidate rule:

> Reproduction should not be reduced to a single `pass/fail`; discrepancy level must match the reproducibility claim.

These are conceptual statuses, not final software enums.

---

## 30. Publication Freeze

At manuscript/result freeze, the following should be locked:

```text
Git commit/source identity
resolved configurations
trial ensembles
analysis policies
metric outputs
figures/tables
hardware build identities
manifest
```

Candidate rule:

> Once a publication package is frozen, later regeneration under changed code/config creates a new package/version; existing cited evidence is not overwritten in place.

---

## 31. Corrections after Freeze

If a bug or interpretation error is discovered after freeze:

Candidate rule:

> The original package remains immutable for audit, a corrected package receives a new identity/version, affected claims are explicitly marked superseded/corrected, and the reason plus evidence impact is recorded.

Silent replacement is forbidden.

---

## 32. Publication Package versus Repository Working State

The repository may continue evolving after a paper result is frozen.

Candidate rule:

> A publication package shall refer to exact immutable source/artifact identities so later `main` development does not alter the meaning of previously published evidence.

Tags/releases may be useful aliases but commit/content identities remain authoritative.

---

## 33. Large Artifact Strategy

Large raw datasets or bitstreams may not belong directly in Git history.

Candidate rule:

> Large artifacts may live in an external archival/object store, release asset, institutional repository, or data archive, but the GeoDOA package shall retain immutable identifiers, hashes, retrieval metadata, schema, and lineage.

The storage technology is not the scientific identity.

---

## 34. DOI / Archival Release

For external publication, a DOI-backed archival snapshot may strengthen permanence.

Candidate rule:

> DOI/release archival identifiers are publication convenience/persistence metadata and shall point to a frozen evidence package; they do not replace internal content hashes/provenance.

No specific archive is mandated here.

---

## 35. Licensing and Redistribution Metadata

Reproducibility may depend on whether code/data/tool artifacts can legally be redistributed.

Candidate rule:

> Publication packages shall state relevant licensing/redistribution constraints for external datasets, calibration artifacts, CST exports, IP cores, or vendor-generated files when those constraints affect reproduction.

---

## 36. Proprietary Tool Dependencies

Some results may depend on CST, MATLAB, Vivado/Vitis, or vendor IP.

Candidate rule:

> Proprietary tool dependence shall be explicit, including tool/version and the strongest shareable intermediate artifacts needed for audit; publication wording shall not imply unrestricted reproduction when licenses are required.

---

## 37. Hardware Reproducibility Package

For FPGA/SoC results, candidate package additions include:

```text
board/part/revision
clock configuration
HLS/RTL source identity
tool/IP versions
constraints/directives
synthesis/place-route reports
bitstream/hash
canonical stimulus artifact
host software identity
interface/packing semantics
latency/II/throughput scope
resource utilization
power methodology if claimed
board-run logs/results
```

Candidate rule:

> Hardware package shall enable another engineer to distinguish scientific numerical equivalence from synthesis/timing/resource/integration evidence.

---

## 38. Physical Experiment Package

For real-array validation, candidate additions include:

```text
array physical geometry and serial/state identity where appropriate
sensor/receiver hardware configuration
calibration artifact + validity domain
reference instrument/procedure
environmental conditions
acquisition settings
raw capture identity
uncertainty/reference model
operator procedure deviations
```

Candidate rule:

> Physical experiment reproducibility records the experimental state and procedure even when exact physical recreation is impossible.

---

## 39. Negative and Null Results

Publication packages should not preserve only favorable conditions.

Candidate rule:

> Failed conditions, negative results, incompatibilities, and unresolved evidence that belong to the declared benchmark domain shall remain in the package or be explicitly accounted for.

Selective publication packaging must not silently rewrite the benchmark universe.

---

## 40. Exploratory versus Confirmatory Evidence

Exploration 4.12 distinguished tuning/development from final evaluation.

Candidate rule:

> Publication packages shall label whether results are exploratory, tuning/calibration, confirmatory/held-out, regression, or physical-validation evidence.

A final figure assembled from exploratory tuning runs should not be presented as independent held-out validation without disclosure.

---

## 41. Reproducibility Package Does Not Prove Correctness

A perfectly reproducible wrong result is still wrong.

Candidate rule:

> Reproducibility packages establish traceability/reconstruction of evidence; verification, validation, uncertainty, and scientific correctness remain separate claim dimensions.

This preserves Exploration 4.1.

---

## 42. Minimal Publication Package Candidate

For a synthetic algorithm/geometry paper result, a conservative minimum is:

```text
MANIFEST
resolved canonical configs + hashes
Git commit/source provenance
software environment record
RNG/trial ensemble provenance
input/artifact identities
association/metric/failure/uncertainty policy versions
trial-level or recomputable intermediate result data
aggregate metric tables
failure/exclusion summaries
figure/table generation scripts/configs
final figure/table hashes
README reproduction instructions
known limitations / reproducibility level
```

For hardware work, add the 4.15/4.16 hardware build package.

---

## 43. Recommended Package Directory Concept

A future implementation might use a structure conceptually like:

```text
publication_package/
  manifest.*
  README_REPRODUCE.md
  configs/
  provenance/
  trials/
  metrics/
  failures/
  figures/
  tables/
  scripts/
  references/
  environment/
  hardware/          # optional
  physical/          # optional
```

Candidate rule:

> Directory layout is implementation detail; semantic manifest/identity/lineage is authoritative.

No folder schema is accepted as final in Phase 0C.

---

## 44. Publication Readiness Status

Candidate conceptual statuses:

```text
EXPLORATORY_ONLY
TRACEABLE_NOT_REPRODUCIBLE
RECOMPUTABLE
RERUN_REPRODUCIBLE
INDEPENDENTLY_REPRODUCED
HARDWARE_REPLAYABLE
PHYSICAL_EXPERIMENT_TRACEABLE
PUBLICATION_READY
BLOCKED_BY_MISSING_EVIDENCE
UNRESOLVED
```

Candidate rule:

> `publication_ready` shall not be a bare boolean; the evidence basis and blocked dimensions should be visible.

---

## 45. Candidate Package Acceptance Checks

Before publication-ready status, candidate checks include:

```text
source/config provenance complete
trial counts reconcile
failures/exclusions explicit
metric definitions resolve
uncertainty/adequacy present for stochastic claims
comparison fairness record complete
figures/tables regenerate
artifact hashes validate
no mutable hidden dependency required
hardware build identity complete if applicable
known limitations documented
reproducibility level justified
```

Candidate rule:

> Publication readiness is evidence completeness/consistency, not proof that every result is favorable.

---

## 46. Invalid / Weak Publication Practices

The following are scientifically weak or invalid unless explicitly bounded:

1. publish only PNG/PDF figures with no underlying result data;
2. report aggregate RMSE without trial/eligibility/failure evidence;
3. store only the user-authored config while relying on hidden defaults;
4. regenerate a published figure from a newer Git commit without changing evidence identity;
5. manually edit scientific values in a spreadsheet with no transform record;
6. omit failed/excluded trials from the publication package;
7. give `95% CI` without preserving method, level, denominator, and conditioning;
8. publish hardware speedup without timing-scope/build/device provenance;
9. archive a bitstream filename but not its content/build identity;
10. imply physical validation from synthetic FPGA replay;
11. overwrite frozen evidence after bug correction;
12. claim full reproducibility when proprietary/raw data dependencies cannot be shared and no limitation is stated;
13. keep only favorable SNR/separation conditions from a declared benchmark;
14. treat a container image as sufficient evidence without source/config/data lineage;
15. rely on filesystem paths or timestamps as evidence identities;
16. include secrets or credentials in publication manifests;
17. produce figures from exploratory/tuning data while labeling them independent final validation without disclosure.

---

## 47. Cross-ADR Reconciliation

### ADR-001

Geometry, coordinate, phase-reference, channel-order, and unit conventions become frozen profile/config dependencies in publication evidence.

### ADR-002

Signal/source/noise/SNR/snapshot/covariance semantics must be visible in resolved configurations and condition records.

### ADR-003

Sensor/calibration/reference-plane/CST/measured-manifold artifacts require explicit identity, validity domain, and lineage.

### ADR-004 Explorations 4.2–4.3

Truth/reference provenance and deterministic reference evidence become publication package dependencies rather than implicit assumptions.

### ADR-004 Explorations 4.4–4.5

Stochastic trial identity, root/child stream policy, and CRN pairing must remain reconstructable.

### ADR-004 Explorations 4.6–4.14

Association, metrics, detection/resolution, failures, adequacy, uncertainty, comparisons, and multi-level diagnostics define the analysis evidence stored or referenced by the package.

### ADR-004 Exploration 4.15

Hardware packages preserve fixed-point/HLS/RTL/FPGA implementation and timing/resource evidence separately from physical validation.

### ADR-004 Exploration 4.16

Run/config/artifact identity, hashes, source/environment provenance, immutability, and reproducibility levels provide the package backbone.

**Cross-ADR result: no contradiction identified.**

---

## 48. Candidate Decisions from Exploration 4.17

- **D4.17-01:** Publication-grade claims require traceable evidence packages; figures/tables alone are not authoritative scientific evidence.
- **D4.17-02:** Each material quantitative claim should resolve to stable run/result/metric evidence identifiers.
- **D4.17-03:** A top-level manifest identifies frozen configs, runs, trial ensembles, artifacts, policies, environment, figures/tables, and hardware builds where applicable.
- **D4.17-04:** Resolved canonical configuration is authoritative; original user-authored configuration is optional supporting provenance.
- **D4.17-05:** Stochastic publication results should preserve trial-level evidence sufficient to recompute metrics/uncertainty when practical.
- **D4.17-06:** If full data cannot be shared, restrictions and reduced reproducibility level shall be explicit while preserving hashes/metadata/derived evidence.
- **D4.17-07:** Aggregate metric records preserve metric semantics, units, conditions, counts, failure/association policy, uncertainty, adequacy, and trial ensemble identity.
- **D4.17-08:** Failure/incompatibility/unresolved evidence belongs in the publication package and shall not be hidden by successful-trial figures.
- **D4.17-09:** Comparative packages preserve the full comparison contract, pairing, absolute/relative effects, uncertainty, resource constraints, and claim class.
- **D4.17-10:** Deterministic GRP/verification evidence remains linked but distinct from stochastic performance results.
- **D4.17-11:** Figures and tables are derived artifacts with source IDs, scripts, transformations, display semantics, and content identities.
- **D4.17-12:** Scientific-value transformations shall be scripted or fully recorded; hidden manual spreadsheet edits are not acceptable publication workflow.
- **D4.17-13:** Recompute, full rerun, and independent reproduction are distinct reproducibility tests.
- **D4.17-14:** Reproduction discrepancy status shall distinguish exact, numerical, statistical, conclusion-level, blocked, and unresolved outcomes.
- **D4.17-15:** Publication freeze makes evidence immutable/versioned; corrections create new package identities and preserve superseded history.
- **D4.17-16:** Large/proprietary artifacts may be external, but immutable identifiers, hashes, retrieval metadata, licensing constraints, and lineage remain required.
- **D4.17-17:** Hardware publication packages preserve exact build/tool/device/stimulus/timing/resource evidence; physical validation requires additional acquisition/reference/calibration/environment evidence.
- **D4.17-18:** Exploratory/tuning/confirmatory/regression/physical-validation evidence roles shall be labeled.
- **D4.17-19:** A reproducibility package supports reconstruction/audit but does not itself prove scientific correctness or physical validity.
- **D4.17-20:** Publication readiness is a typed evidence-completeness state, not a bare boolean or a measure of whether results are favorable.

---

## 49. Exploration 4.17 Conclusion

Exploration 4.17 is complete at candidate-contract level.

The central rule is:

> GeoDOA shall make every publication-grade quantitative claim traceable to a frozen, internally consistent, versioned evidence package containing authoritative resolved configuration, run/trial/artifact provenance, failure and uncertainty evidence, recomputable metrics, figure/table lineage, software/hardware dependencies, and explicit reproduction instructions. Publication artifacts shall be immutable once cited, corrections shall create new evidence identities, and the claimed reproducibility level shall never exceed what the retained package can actually reconstruct.

No acceptance gate is started or passed by this exploration.

The next exploration is:

```text
4.18 — Cross-ADR Compatibility with ADR-001/002/003
```
