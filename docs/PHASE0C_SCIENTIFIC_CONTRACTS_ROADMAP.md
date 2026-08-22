# Phase 0C — Scientific Contracts Roadmap

## 1. Purpose

Phase 0C defines the scientific constitution of GeoDOA Studio before material scientific implementation begins.

The governing rule is:

> No scientific implementation is considered authoritative until its governing scientific contract has been explicitly defined, reviewed, and approved.

Phase 0C is therefore not a documentation-only exercise. It establishes the physical, mathematical, statistical, numerical, validation, and provenance rules that all later geometry, sensor modeling, signal processing, DOA, PCA/ICA, MIMO, radar, calibration, and FPGA/SoC work must obey.

## 2. Phase 0C Objective

The objective is to establish a coherent set of scientific Architecture Decision Records (ADRs), supporting scientific notes, and deterministic Golden Reference Problems that together define:

- what physical system GeoDOA models;
- how coordinates, directions, delays, phases, and spatial frequency are represented;
- how source waveforms and propagation media are modeled;
- how measurements and array-processing views are represented;
- how covariance and subspace quantities are interpreted;
- how real sensor imperfections, mutual coupling, and calibration enter the model;
- how ground truth, verification, validation, Monte Carlo experiments, and reproducibility are defined;
- how scientific correctness is demonstrated before implementation is treated as trusted.

### 2.1 Relationship to the Master Start Handoff ADR list

The Master Start Handoff was intentionally written before Phase 0C scientific decomposition was complete. Its Phase 0 roadmap therefore contained a **preliminary recommended ADR numbering** in which, for example, `ADR-002` was suggested for units/normalization and later numbers were suggested for layered architecture, run identity, GUI technology, and comparison fairness.

This Phase 0C roadmap is the later, more specific governing plan for the **scientific ADR series**. It supersedes that preliminary numbering assignment, but it does not discard the underlying subjects.

The authoritative Phase 0C scientific numbering is now:

```text
ADR-001  Coordinate, Direction, and Spatial Conventions
ADR-002  Wave, Propagation, Signal, and Measurement Model
ADR-003  Sensor Imperfections, Mutual Coupling, and Calibration
ADR-004  Validation, Reproducibility, and Scientific Evidence
```

Topics from the Master Start Handoff such as layered architecture, configuration/result identity, GUI technology, and geometry-comparison fairness remain valid planned decisions. They shall receive later non-conflicting ADR numbers or other explicitly governed decision records after the Phase 0C scientific series. No future document should cite the preliminary Master Start Handoff ADR numbers as if they were final identities.

This clarification changes numbering/provenance only; it does not weaken or remove the architectural requirements in the Master Start Handoff.

## 3. Scientific ADR Set

### ADR-001 — Coordinate, Direction, and Spatial Conventions

Primary question:

> How does GeoDOA represent physical geometry and direction, and how does that representation produce relative delay and spatial phase?

Required topics:

- 1-D array geometry versus 3-D propagation space;
- array-axis definition;
- coordinate frame and origin policy;
- physical coordinate preservation;
- phase-reference semantics;
- look direction versus propagation direction;
- broadside and endfire definitions;
- positive-angle convention;
- canonical 2-D angular slice;
- visible-sector convention;
- direction cosine and observable spatial coordinate;
- temporal phasor convention;
- receive-manifold phase sign derived from propagation delay;
- translation invariance;
- sensor/channel identity versus sorted geometric views;
- duplicate-position policy;
- canonical units;
- wavelength-normalized derived representations;
- lattice declaration, validation, and tolerance;
- declared versus primitive lattice semantics;
- integer coarray lag validity;
- spatial angular frequency and normalized lattice spatial frequency;
- 3-D projection ambiguity;
- front/back ambiguity;
- spatial aliasing versus projection ambiguity;
- angle-grid versus direction-cosine/spatial-frequency-grid semantics.

ADR-001 must derive the receive steering vector from geometry and delay rather than adopt a sign convention without derivation.

### ADR-002 — Wave, Propagation, Signal, and Measurement Model

Primary question:

> What signal or waveform propagates through what medium, under what approximations, and how does it become a sensor measurement?

Required topics:

- propagation-medium abstraction;
- homogeneous and nondispersive baseline medium;
- explicit propagation speed;
- exact source-to-sensor distance;
- spherical-wave model;
- plane-wave approximation;
- far-field and near-field regimes;
- aperture-dependent curvature error;
- Fraunhofer-distance diagnostic;
- phase-error-based far-field diagnostic;
- narrowband approximation;
- aperture differential delay;
- bandwidth-delay validity metric;
- wideband frequency-dependent manifold;
- stationary and moving source concepts;
- source position and velocity state;
- range migration, angle migration, and Doppler extension points;
- passive sensing versus active sensing;
- continuous-tone waveform;
- pulsed waveform;
- linear FMCW chirp;
- stepped-frequency waveform;
- arbitrary sampled waveform;
- complex-baseband representation;
- fast-time, slow-time, spatial/channel, frequency, Tx, and Rx axes;
- raw multidimensional measurement versus canonical array-processing view;
- snapshot semantics;
- physical axis semantics versus index and memory layout;
- physical channel versus virtual MIMO channel;
- measurement and processing provenance.

The initial validated processing slice may remain stationary, far-field, narrowband, and homogeneous, but these assumptions must be explicit rather than hidden.

### ADR-003 — Sensor Imperfections, Mutual Coupling, and Calibration

Primary question:

> How does the real sensor system depart from the ideal array model, and how are those departures represented, measured, calibrated, and propagated into DOA performance?

Required topics:

- nominal manifold;
- true/physical manifold;
- calibrated manifold;
- manifold mismatch;
- position error and uncertainty;
- gain mismatch;
- phase mismatch;
- common complex scale versus relative channel mismatch;
- element amplitude/phase pattern;
- polarization and frequency-dependence extension points;
- mutual coupling as a cross-channel operator;
- coupling frequency and geometry dependence;
- channel delay mismatch;
- clock and sampling skew;
- carrier/LO/frequency error;
- active-channel mask and channel dropout;
- quantization and receiver effects;
- ordering of physical sensor effects;
- distinction between diagonal channel effects and cross-channel coupling;
- parameter calibration;
- coupling-model calibration;
- direct measured-manifold calibration;
- CST-derived manifold calibration;
- calibration-domain metadata and interpolation;
- calibration provenance;
- residual calibration error;
- common-phase/scale-aligned manifold-error metrics;
- covariance distortion;
- eigenvalue and eigenspace/subspace distortion;
- propagation of model mismatch to MUSIC and other DOA estimators.

Mutual coupling is a first-class sensor-modeling effect and must not be reduced to a generic per-channel phase/gain perturbation.

### ADR-004 — Validation, Reproducibility, and Scientific Evidence

Primary question:

> Under what evidence can GeoDOA call a model, algorithm, experiment, or hardware result verified, validated, reproducible, or better than another method?

Required topics:

- ground-truth definition and provenance;
- verification versus physical validation;
- analytical reference validation;
- numerical cross-reference validation;
- external-tool validation;
- hardware/experimental validation;
- deterministic Golden Reference Problems;
- random-variable declaration;
- Monte Carlo trial semantics;
- root seed and deterministic child-stream policy;
- common random numbers for fair comparisons;
- trial-count adequacy and convergence diagnostics;
- bias;
- variance;
- MSE and RMSE;
- multi-source truth-to-estimate association;
- missed and false detections;
- resolution versus accuracy;
- probability of resolution;
- failure-state recording;
- spectrum-level diagnostics;
- manifold, covariance, eigenvalue, eigenspace, and DOA error metrics;
- uncertainty/confidence intervals for aggregate metrics;
- fair benchmark requirements;
- data, configuration, calibration, algorithm, software, Git, and seed provenance;
- scientific metrics versus computational/hardware metrics;
- floating-point, fixed-point, and FPGA cross-validation.

## 4. Supporting Scientific Contract Notes

ADRs define decisions and contracts. They should not become textbooks. Longer derivations and explanations belong in supporting scientific notes.

Planned notes include at least:

- measurement data model and axis semantics;
- covariance and eigenstructure contract;
- PCA/subspace/MUSIC relationship;
- signal/noise/source-correlation semantics;
- sample-covariance rank limits and mean-centering proof;
- far-field and narrowband approximation derivations;
- mutual-coupling and manifold-mismatch propagation;
- FMCW/stepped-frequency measurement semantics;
- MIMO physical-channel and virtual-array semantics.

These notes may later form the technical basis of a GeoDOA Engineering Notes / Problem Book.

## 5. Golden Reference Problem Program

Every core scientific model must have at least one deterministic hand-computable reference problem.

Each Golden Reference Problem serves three purposes simultaneously:

1. learning and physical interpretation;
2. analytical reference evidence;
3. software regression-test oracle.

Initial catalog target:

- GRP-001 — Two-sensor propagation delay;
- GRP-002 — Two-sensor steering-vector phase;
- GRP-003 — Translation invariance and phase reference;
- GRP-004 — Direction-cosine / 3-D projection ambiguity;
- GRP-005 — Spatial aliasing for a lattice array;
- GRP-006 — Lattice and difference-coarray lag construction;
- GRP-007 — Far-field curvature error;
- GRP-008 — Narrowband bandwidth-delay diagnostic;
- GRP-009 — FMCW beat frequency and range;
- GRP-010 — Tiny FMCW data cube to range FFT to covariance;
- GRP-011 — 2x2 covariance eigendecomposition;
- GRP-012 — MUSIC noise-subspace orthogonality;
- GRP-013 — Mean-centered sample-covariance rank ceiling;
- GRP-014 — Position-error phase distortion;
- GRP-015 — Gain/phase mismatch;
- GRP-016 — Mutual-coupling manifold distortion;
- GRP-017 — Coupling to covariance to eigenspace distortion;
- GRP-018 — Bias, variance, MSE, and RMSE by hand.

The catalog may expand, but each problem must remain small enough to solve independently with paper, pencil, and a basic calculator.

## 6. ADR Acceptance Gates

No ADR is approved merely because the text is complete. Each ADR must pass all of the following gates.

### Gate A — Physical Consistency

Definitions and equations must match the intended physical system and distinguish model assumptions from physical truth.

### Gate B — Mathematical Consistency

Signs, dimensions, transformations, invariances, rank statements, and approximation boundaries must be internally consistent.

### Gate C — Dimensional and Unit Consistency

Every physical quantity must have explicit units or be explicitly dimensionless. Unit conversion and normalization rules must be unambiguous.

### Gate D — Software Semantic Consistency

The scientific meaning must map cleanly to domain concepts without hidden sorting, implicit normalization, unlabeled axes, silent approximation, or destructive loss of provenance.

### Gate E — Hand-Calculated Reference Evidence

At least one deterministic Golden Reference Problem must exercise each core contract and produce a manually inspectable expected result.

### Gate F — Boundary and Failure Analysis

The ADR must state where the model becomes ambiguous, invalid, underdetermined, aliased, poorly conditioned, or outside its declared domain of validity.

## 7. Phase 0C Working Rule

Phase 0C prioritizes correctness and clarity over implementation speed.

The default sequence for each ADR is:

```text
Question / physical problem
        ↓
Derivation and definitions
        ↓
Alternative conventions considered
        ↓
Decision
        ↓
Boundary / failure analysis
        ↓
Golden Reference Problems
        ↓
Cross-ADR consistency audit
        ↓
Approval
```

Implementation work may use exploratory scratch calculations, but no scientific implementation becomes the authoritative GeoDOA behavior before the governing ADR is approved.

## 8. Phase 0C Completion Criteria

Phase 0C is complete only when:

- ADR-001 through ADR-004 are written and approved;
- all six acceptance gates have been satisfied for each ADR;
- cross-ADR terminology and sign conventions are consistent;
- supporting scientific notes exist for derivations too detailed for ADRs;
- the initial Golden Reference Problem catalog has implemented hand solutions/specifications sufficient to act as test oracles;
- the initial implementation boundary for Phase 1 is explicitly derived from the approved contracts;
- the Phase 0C handoff records decisions, deferred capabilities, unresolved questions, verification evidence, and the material merge identity after closure reconciliation.

## 9. Initial Phase 1 Boundary After Phase 0C

Phase 0C does not require implementation of every capability it defines.

The first implementation slice is expected to remain deliberately narrow and validated, approximately:

```text
Validated 1-D physical geometry
        ↓
Canonical units / reference semantics
        ↓
Direction-cosine and steering-manifold kernel
        ↓
Declared lattice and difference-coarray analysis
        ↓
Stationary far-field narrowband source model
        ↓
Ideal uncoupled sensor baseline
        ↓
Array snapshot matrix
        ↓
Sample covariance
        ↓
Baseline subspace / MUSIC path
        ↓
Golden Reference verification
```

Sensor imperfections, mutual coupling, calibration, active radar waveforms, motion, wideband processing, PCA/ICA, and FPGA/SoC remain governed by Phase 0C contracts and are implemented progressively in later bounded work packages.

## 10. Governing Principle

GeoDOA Studio shall prefer a smaller scientifically defensible capability over a broader capability with ambiguous assumptions.

The persistent engineering principle for Phase 0C is:

> Preserve physical meaning, mathematical consistency, provenance, and verifiability before optimizing for feature count, interface polish, or implementation speed.
