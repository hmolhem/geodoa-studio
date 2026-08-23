# GeoDOA Studio — Phase 0C / ADR-003 Continuation Handoff

- **Purpose:** Strong continuation checkpoint for the next ChatGPT engineering session
- **Repository:** `https://github.com/hmolhem/geodoa-studio`
- **Local working copy:** `C:\MyDocument\geodoa-studio`
- **Python package:** `geodoa`
- **CLI:** `geodoa`
- **Current scientific branch:** `docs/phase0c-scientific-conventions`
- **Do not merge without explicit user approval.**
- **Current workstream:** Phase 0C — Scientific Foundations / Scientific Contracts
- **Immediate scientific work item:** ADR-003 — Sensor Imperfections, Mutual Coupling, and Calibration
- **ADR-003 current point:** Explorations 3.1–3.4 complete; start next at 3.5 Mutual Coupling
- **Companion checkpoint:** `../adr/ADR-003_EXPLORATION_CHECKPOINT.md`

---

# 1. What GeoDOA Studio Is

GeoDOA Studio is intended to become a rigorous geometry-aware sensor-array engineering framework spanning:

```text
Physical array geometry
    ↓
Wave / propagation / source / measurement modeling
    ↓
Real sensor imperfections and calibration
    ↓
Covariance / eigenspace / subspace processing
    ↓
DOA estimation and array diagnostics
    ↓
Reproducible benchmarking
    ↓
Floating-point → fixed-point → FPGA/SoC validation
```

The project is not intended to be a collection of disconnected scripts or a cosmetic MUSIC GUI. It is being built as a scientifically governed engineering system with clean software architecture, reproducibility, explicit scientific semantics, testable reference problems, and future hardware/backend portability.

Product positioning:

> **GeoDOA Studio — From array geometry to validated DOA estimation and FPGA/SoC deployment.**

Conceptual subtitle:

> **Geometry-Aware Sensor-Array Modeling, DOA Estimation, and Hardware Co-Design Workbench**

---

# 2. User Intent and Engineering Standard

The user wants this project to strengthen the professional niche:

```text
Sensor Modeling
+ Signal / Array Processing
+ DOA Estimation
+ MIMO / Coarray Processing
+ FPGA / SoC Hardware–Algorithm Co-Design
```

The user explicitly prefers **engineering authenticity** over superficial feature count.

Every material scientific capability should ultimately answer:

1. What physical problem does this model solve?
2. What is its exact mathematical definition?
3. What assumptions and validity domain does it require?
4. How do we know the implementation is correct?
5. What are the engineering failure modes?
6. What reproducible evidence supports the result?

Persistent engineering chain:

\[
\boxed{
\text{Physical meaning}
\rightarrow
\text{Mathematical definition}
\rightarrow
\text{Assumptions / validity}
\rightarrow
\text{Software contract}
\rightarrow
\text{Hand/reference case}
\rightarrow
\text{Implementation}
\rightarrow
\text{Tests}
\rightarrow
\text{Numerical validation}
\rightarrow
\text{Engineering interpretation}
\rightarrow
\text{Reproducible evidence}
}
\]

Do not claim novelty before evidence.

---

# 3. Architecture Philosophy

GeoDOA follows a domain-centric / layered / clean-architecture direction:

```text
Interfaces
(CLI / GUI / Python API / Notebook)
        ↓
Application services / use cases
        ↓
Domain entities / scientific contracts
        ↓
Pure numerical kernels
        ↓
Infrastructure / storage / hardware adapters
```

Dependency direction is toward the scientific/domain core.

Use object-oriented design where it improves domain meaning. Use pure functions for mathematical/numerical kernels where classes add no value. Avoid class inflation.

Notebook, GUI, CLI, and future REST/API layers must consume the same scientific core. Notebook code must not become the source of truth for algorithms.

Source-of-truth implementation path is intended under `src/geodoa`.

Representative conceptual domain entities include:

- `LinearArrayGeometry`
- `MIMOArrayGeometry`
- `ReferenceFrame1D`
- `WaveParameters`
- `AngleConvention`
- `GeometryMetadata`
- `ArrayCalibration`
- `SourceScenario`
- `NoiseModel`
- `ExperimentConfig`
- `ProcessingPipeline`
- `RunIdentity`

Representative contracts include:

- `GeometryGenerator`
- `GeometryAnalyzer`
- `CoarrayAnalyzer`
- `ManifoldProvider`
- `ImperfectionModel`
- `SignalGenerator`
- `CovarianceEstimator`
- `LagAggregator`
- `LagRegularizer`
- `VirtualCovarianceBuilder`
- `DOAEstimator`
- `ModelOrderEstimator`
- `PeakDetector`
- `PerformanceMetric`
- `CompatibilityValidator`
- `ExecutionBackend`
- `ResultRepository`
- `Exporter`

These names remain conceptual until implementation decisions are explicitly made.

---

# 4. Git / Work-Package Governance

The Git repository is the persistent source of truth.

Current local path:

```text
C:\MyDocument\geodoa-studio
```

Current Phase 0C branch:

```text
docs/phase0c-scientific-conventions
```

Do not merge this branch without explicit user approval.

General work-package rhythm:

```text
clean main
    ↓
create bounded branch
    ↓
perform scoped scientific/engineering work
    ↓
verify
    ↓
write/update handoff and evidence
    ↓
explicitly stage intended files only
    ↓
commit
    ↓
push
    ↓
PR
    ↓
review / CI
    ↓
merge only after approval
    ↓
branch cleanup
    ↓
sync local main with origin/main
```

Important rules:

- direct work on `main` is prohibited unless explicitly approved as an exception;
- do not use `git add .`, `git add -A`, or `git add --all` for material work;
- use explicit staging;
- material work packages normally receive handoff evidence;
- `HANDOFF_INDEX.md` is for milestone/work-package closure history, not every micro-checkpoint;
- scientific exploration checkpoints do not automatically create a HANDOFF_INDEX row;
- `Ready for Merge` and `Closed` are different lifecycle states;
- a material WP is fully Closed only after merge and closure metadata reconciliation;
- closure reconciliation is administrative continuation, not a new engineering milestone;
- closure-PR merge identity must not replace the material merge identity;
- avoid recursive closure-reconciliation loops.

The current Phase 0C scientific branch already intentionally contains the roadmap plus multiple scientific ADRs. Continue on this branch unless the user explicitly changes the workflow.

---

# 5. Phase History Before Phase 0C

## Phase 0A — CLOSED

Repository bootstrap completed and merged through PR #1.

Material merge identity:

```text
67e776b11040c33bab28d2cdf4b0ae6742c4bc86
```

## Phase 0B — CLOSED

Python engineering toolchain completed.

Material PR #2 merge:

```text
fac6b1d4208a1d529943b3e5dfb10260b15e7540
```

Closure reconciliation PR #3 merge:

```text
496187c9ebe3baa2a426f81a8f0af3fdd54f7892
```

The current `main` baseline for Phase 0C is therefore:

```text
496187c9ebe3baa2a426f81a8f0af3fdd54f7892
```

Phase 0B established Python >=3.12,<3.15, Hatchling, Ruff, mypy, pytest, CI on 3.12/3.13/3.14, repository text/line-ending discipline, and editable-import verification.

---

# 6. Phase 0C — Scientific Foundations

Phase 0C defines the scientific constitution before material scientific implementation becomes authoritative.

Governing rule:

> **No scientific implementation is considered authoritative until its governing scientific contract has been explicitly defined, reviewed, and approved.**

Authoritative scientific ADR numbering:

```text
ADR-001  Coordinate, Direction, and Spatial Conventions
ADR-002  Wave, Propagation, Signal, and Measurement Model
ADR-003  Sensor Imperfections, Mutual Coupling, and Calibration
ADR-004  Validation, Reproducibility, and Scientific Evidence
```

Current status:

```text
ADR-001 — ACCEPTED — Gates A–F PASS
ADR-002 — ACCEPTED — Gates A–F PASS
ADR-003 — EXPLORATION IN PROGRESS
ADR-004 — NOT STARTED
```

---

# 7. How Each ADR Is Developed

The work should not jump directly from topic name to formal ADR.

Default scientific rhythm:

```text
Primary scientific question
        ↓
Exploration sections
        ↓
Physical derivation and definitions
        ↓
Alternative interpretations / convention checks
        ↓
Candidate decisions
        ↓
Cross-section reconciliation
        ↓
Draft governing ADR
        ↓
Gate A
        ↓
Gate B
        ↓
Gate C
        ↓
Gate D
        ↓
Gate E / Golden Reference Problems
        ↓
Gate F / Boundary and Failure Analysis
        ↓
Cross-gate consistency reconciliation
        ↓
Final Acceptance Record
        ↓
ACCEPTED only if all six gates PASS
```

The governing ADR must not be marked Accepted before this lifecycle is complete.

During exploration, candidate decisions are deliberately preserved so they can later be reconciled rather than reconstructed from memory.

---

# 8. Phase 0C Acceptance Gates

Every scientific ADR must pass all six gates.

## Gate A — Physical Consistency

Questions include:

- Does the model correspond to the intended physical system?
- Are approximations distinguished from physical truth?
- Are passive/active, near/far, sensor/measurement, and similar physical distinctions preserved?

## Gate B — Mathematical Consistency

Audit:

- signs;
- transformations;
- invariances;
- matrix dimensions;
- rank statements;
- approximation derivations;
- equivalence classes;
- identifiability claims.

## Gate C — Dimensional and Unit Consistency

Every physical quantity must be explicitly dimensioned or explicitly dimensionless. No unit inference by magnitude. dB semantics must distinguish amplitude and power meanings. Fixed-point later must retain physical scale/unit/Q-format provenance.

## Gate D — Software Semantic Consistency

Scientific meaning must map into software without:

- hidden flags that silently change model meaning;
- destructive normalization;
- unlabeled axes;
- silent sorting;
- silent model substitution;
- lost channel identity;
- lost calibration/model provenance.

The principle is:

\[
\boxed{
\text{Scientific semantic separability without premature class inflation}
}
\]

## Gate E — Hand-Calculated Reference Evidence

Each core scientific contract must have deterministic hand-computable reference evidence.

Golden Reference philosophy:

\[
\boxed{
\text{Hand Solution}
=
\text{Scientific Reference}
=
\text{Software Test Oracle}
}
\]

A GRP is intentionally small enough for paper, pencil, and calculator verification.

## Gate F — Boundary and Failure Analysis

The ADR must explicitly say when an operation/model is:

- valid;
- diagnostic/warning only;
- incompatible and requires a different model;
- rejected as invalid input/state.

Persistent distinction:

\[
\boxed{
\text{Physical invalidity}
\neq
\text{Profile incompatibility}
\neq
\text{Algorithm incompatibility}
\neq
\text{Interpretation warning}
}
\]

No invented threshold should be used when a tolerance policy has not been declared.

---

# 9. Golden Reference Problem Program

Current roadmap catalog:

```text
GRP-001  Two-sensor propagation delay
GRP-002  Two-sensor steering-vector phase
GRP-003  Translation invariance and phase reference
GRP-004  Direction-cosine / 3-D projection ambiguity
GRP-005  Spatial aliasing for a lattice array
GRP-006  Lattice and difference-coarray lag construction
GRP-007  Far-field curvature error
GRP-008  Narrowband bandwidth-delay diagnostic
GRP-009  FMCW beat frequency and range
GRP-010  Tiny FMCW cube → range FFT → covariance
GRP-011  2x2 covariance eigendecomposition
GRP-012  MUSIC noise-subspace orthogonality
GRP-013  Mean-centered sample-covariance rank ceiling
GRP-014  Position-error phase distortion
GRP-015  Gain/phase mismatch
GRP-016  Mutual-coupling manifold distortion
GRP-017  Coupling → covariance → eigenspace distortion
GRP-018  Bias, variance, MSE, and RMSE
```

ADR mapping:

```text
ADR-001 → GRP-001 through GRP-006
ADR-002 → GRP-007 through GRP-013
ADR-003 → GRP-014 through GRP-017
ADR-004 → GRP-018 plus validation/reproducibility evidence as required
```

ADR-002 also used supplemental source/reference cases named `ADR-002-SRC-01` etc. to avoid stealing reserved GRP numbers.

For ADR-003:

- GRP-014 and GRP-015 now have strong conceptual seeds from explorations 3.2 and 3.3;
- GRP-016 and GRP-017 must wait until mutual-coupling semantics are explored and reconciled;
- formal GRPs belong to Gate E and should not be declared PASS before their governing contracts are stable.

---

# 10. ADR-001 — Accepted Contract Summary

ADR-001 is accepted and must not be casually reopened.

Core locked rules include:

- scientific 1-D physical geometry is embedded in 3-D propagation space;
- canonical frame is right-handed;
- look direction is array → source;
- propagation direction is the negative look direction;
- temporal phasor convention is `exp(-j omega t)`;
- receive spatial phase sign is derived from delay rather than memorized;
- canonical spatial phase reference is the centroid of the declared nominal physical geometry, not the active subset;
- coordinate origin, expansion origin, phase reference, and active mask are distinct;
- common phase caused by reference change is not spatial distortion;
- persistent channel identity, sequence order, and sorted geometric order are distinct;
- active masking does not delete/renumber sensors or recompute the nominal reference;
- angle convention is a boundary representation; internal angular quantities use radians;
- physical coordinates remain authoritative; normalized coordinates are derived/contextual only;
- lattice validity, tolerance, declared vs primitive lattice, and coarray provenance are explicit;
- no silent snapping/rounding of physical positions into integer lags;
- spatial aliasing and projection/front-back ambiguity are separate phenomena;
- half-wave spacing edge semantics are explicitly distinguished from strict closed-domain injectivity.

Official evidence set includes the governing ADR, acceptance audit, boundary/failure analysis, Gate F audit, final acceptance record, and ADR-001 Golden Reference Problems.

---

# 11. ADR-002 — Accepted Contract Summary

ADR-002 is accepted and all Gates A–F pass.

Core inherited sign chain:

```text
exp(-jωt)
    ↓
outgoing field ∝ exp(+jkR)
    ↓
ΔR = -Δrᵀu
    ↓
Δτ = -Δrᵀu / v
    ↓
relative baseband phase exp(+jωcΔτ)
    ↓
receive manifold exp(-jkΔrᵀu)
```

Major locked topics include:

- exact spherical range before plane-wave approximation;
- far-field validity as scene/direction/frequency/tolerance dependent, not intrinsic to array geometry;
- pairwise/common-phase-invariant far-field diagnostics;
- narrowband validity through aperture differential delay and bandwidth-delay metrics;
- propagation and element/waveform assumptions are explicit;
- medium phase/group-delay semantics and nondispersive PM-001 baseline;
- source motion, Doppler, range migration, manifold migration, and quasi-static assumptions distinguished;
- passive versus active propagation and generic bistatic path semantics;
- FMCW dechirp sign and scientific-frequency versus standard forward-FFT coordinate sign explicitly separated;
- physical measurement axes, stored tensor layout, and array-processing snapshot view are distinct;
- snapshot means simultaneous-equivalent coherent channel observation, not arbitrary raw ADC sample;
- general bistatic MIMO uses separate Tx/Rx look directions; virtual displacement sum is only a common-look/colocated far-field specialization;
- covariance, second-moment, centered sample covariance, rank limits, source covariance rank, observed subspace rank, physical source count, and peak count are distinct;
- coherent physical arrivals may collapse source covariance rank;
- noise variance, I/Q variance, SNR, colored noise, interference, and source-noise cross-correlation are explicitly typed/qualified;
- PM-001 is the Reference Far-Field Narrowband Receive-Array Profile and remains compositional/versioned;
- compatibility is checked progressively rather than by one generic boolean.

Official evidence set includes the governing ADR, acceptance audit, boundary/failure analysis, Gate F audit, final acceptance record, and ADR-002 Golden Reference Problems.

---

# 12. ADR-003 — Primary Question

> **How does the real sensor system depart from the ideal array model, and how are those departures represented, measured, calibrated, and propagated into DOA performance?**

Roadmap topics include:

- nominal / physical / calibrated manifold;
- manifold mismatch;
- sensor position error and uncertainty;
- gain mismatch;
- phase mismatch;
- common scale versus relative channel mismatch;
- element amplitude/phase pattern;
- polarization;
- mutual coupling;
- channel delay;
- clock/sampling skew;
- LO/carrier/frequency error;
- active-channel/dropout effects;
- quantization and receiver effects;
- physical ordering of sensor effects;
- diagonal versus cross-channel effects;
- parameter calibration;
- coupling calibration;
- direct measured-manifold calibration;
- CST-derived calibration;
- calibration domain, interpolation, and provenance;
- residual calibration error;
- common-phase/scale-aligned manifold error metrics;
- covariance/eigenvalue/eigenspace distortion;
- DOA-performance propagation.

Roadmap non-negotiable rule:

> **Mutual coupling is a first-class sensor-modeling effect and must not be reduced to a generic per-channel phase/gain perturbation.**

---

# 13. ADR-003 Exploration Plan and Current Position

Use this exact sequence unless scientific findings force a documented change:

```text
3.1  Ideal / Physical / Calibrated Manifold                 COMPLETE
3.2  Position Error and Geometry Perturbation                COMPLETE
3.3  Gain and Phase Mismatch                                 COMPLETE
3.4  Element Pattern and Polarization                        COMPLETE
3.5  Mutual Coupling                                         NEXT
3.6  Channel Delay, Clock Skew, and Frequency Error          PENDING
3.7  Quantization / Receiver / Dynamic-Range Effects         PENDING
3.8  Unified Sensor-Imperfection Operator                    PENDING
3.9  Calibration Models                                      PENDING
3.10 Direct Measured / CST-Derived Manifold Calibration      PENDING
3.11 Error Metrics and Identifiability                       PENDING
3.12 Covariance / Eigenspace / MUSIC Error Propagation       PENDING
3.13 Compatibility and Initial ADR-003 Profile               PENDING
3.14 Cross-Consistency Audit                                 PENDING
```

Do not start Gate A yet. Gates begin only after the exploration sequence is reconciled enough to form the governing ADR.

Detailed candidate decisions from 3.1–3.4 are preserved in:

```text
docs/adr/ADR-003_EXPLORATION_CHECKPOINT.md
```

That file is the authoritative continuation checkpoint for detailed ADR-003 reasoning, but it is **not an accepted ADR**.

---

# 14. ADR-003 3.1 — What Was Established

The following scientific response meanings were separated:

\[
\mathbf a_{\rm nom}
\]
Nominal manifold.

\[
\mathbf a_{\rm phys}
\]
Physical manifold.

\[
\mathbf a_{\rm meas}
\]
Measured estimate of the physical manifold.

\[
\mathbf a_{\rm em}
\]
EM/full-wave simulated manifold.

\[
\mathbf a_{\rm cal}
\]
Calibrated processing manifold.

Simulation may additionally have a declared truth manifold.

Calibration was explicitly separated from the forward physical chain. Model calibration and data correction are different operations. Calibration may change effective noise statistics and can amplify noise. Calibration requires domain/provenance. Generic manifold error is incomplete without specifying common-phase/common-scale alignment semantics.

---

# 15. ADR-003 3.2 — What Was Established

Physical position:

\[
\boxed{
\mathbf r_n^{phys}
=
\mathbf r_n^{nom}+\boldsymbol\varepsilon_n
}
\]

Position error is first a geometry/path perturbation, not random phase noise.

Far-field first-order relative phase error:

\[
\boxed{
\delta\phi_n
\approx
-k\hat{\mathbf u}^{T}
(\boldsymbol\varepsilon_n-\boldsymbol\varepsilon_{ref})
}
\]

Pairwise invariant form:

\[
\boxed{
\delta\phi_{nm}
=
-k(\boldsymbol\varepsilon_n-\boldsymbol\varepsilon_m)^T\hat{\mathbf u}
}
\]

A rigid common translation does not distort the far-field relative manifold. Pose error, internal deformation, and element orientation are different effects.

Two-sensor baseline-error bias relation:

\[
\boxed{
\hat u
=
\left(1+\frac{\delta d}{d}\right)u_0
}
\]

and small-angle bias:

\[
\boxed{
\Delta\theta
\approx
\frac{\delta d}{d}\tan\theta_0
}
\]

This provides the conceptual seed for GRP-014.

---

# 16. ADR-003 3.3 — What Was Established

Per-channel narrowband response:

\[
\boxed{
g_n=\rho_n e^{j\phi_n}}
\]

with

\[
\boxed{
\mathbf G=\operatorname{diag}(g_1,\ldots,g_N)
}
\]

and

\[
\mathbf a_{gp}=\mathbf G\mathbf a_{nom}.
\]

Common gain, common phase, and relative mismatch are different scientific meanings. Common phase is not spatial distortion. Common gain may leave normalized subspace direction unchanged while still changing physical amplitude/power/SNR.

Small-error model:

\[
g_n\approx1+\alpha_n+j\phi_n.
\]

Arbitrary electronic phase error is not position-induced phase error, and constant narrowband phase offset is not the same as physical delay mismatch.

Covariance transformation:

\[
\mathbf R_{sig}^{phys}
=
\mathbf G\mathbf R_{sig}^{nom}\mathbf G^H.
\]

Inverse correction transforms noise covariance and can be ill-conditioned. Dead/zero-gain channels cannot be recovered by simple inversion.

Two-sensor phase-error bias:

\[
\boxed{
\hat u=u_0-\frac{\phi_e}{kd}
}
\]

and for \(d=\lambda/2\),

\[
\boxed{
\Delta u=-\frac{\phi_e}{\pi}
}
\]

This provides the conceptual seed for GRP-015.

---

# 17. ADR-003 3.4 — What Was Established

A physical element is not merely a point sample. In an uncoupled scalar-element specialization:

\[
\boxed{
b_n=b_n(\hat{\mathbf u},f,\mathbf p,\ldots)}
\]

with complex amplitude/phase response and

\[
\mathbf P=\operatorname{diag}(b_1,\ldots,b_N).
\]

Then

\[
\mathbf a_{elem}=\mathbf P\mathbf a_{geom}.
\]

Element response is distinct from electronic gain/phase mismatch because it may depend on direction, frequency, polarization, orientation, and environment.

Mechanical position and EM phase center are distinct. Observed phase/manifold error does not by itself identify the physical cause.

Polarization must use an explicit transverse basis and preserve the ADR-001/002 distinction:

\[
\hat{\mathbf k}_{prop}=-\hat{\mathbf u}.
\]

Element orientation, position error, and global array pose are distinct.

Propagation-narrowband compatibility does not guarantee element-response frequency flatness.

Multiple sources may require different element-response operators because their direction/polarization differ.

The architecture must leave room for vector/polarimetric sensors where one physical location may provide multiple measurement channels.

Most importantly for the next section: isolated-element pattern, embedded-element pattern, full-wave/EM manifold, measured manifold, and separate coupling models must not be double-counted.

Magnitude-only radiation pattern is insufficient for coherent manifold calibration.

---

# 18. Exact Next Scientific Step: Exploration 3.5 — Mutual Coupling

The next session must begin here.

Do **not** restart ADR-003 from 3.1 unless a contradiction is identified.

3.5 must answer, with physical derivation rather than shorthand:

1. What exactly is mutual coupling in the GeoDOA receive-array context?
2. Under what assumptions is a cross-channel linear operator

   \[
   \mathbf a_c=\mathbf C\mathbf a
   \]

   scientifically valid?
3. Is \(\mathbf C\) a physical network operator, an effective manifold operator, or both depending on definition?
4. What is the relationship among impedance matrices \(Z\), scattering matrices \(S\), source/load/reference impedance, port-wave definitions, embedded element patterns, and an effective receive coupling matrix?
5. Which of these quantities can be converted into another only after explicit assumptions/terminations/reference impedances are supplied?
6. How does coupling depend on geometry, spacing, frequency, polarization, active/terminated channels, receiver loading, platform, and configuration?
7. When are symmetric, Toeplitz, circulant, banded, or nearest-neighbor coupling matrices justified approximations, and when are they not?
8. Why is mutual coupling not equivalent to diagonal gain/phase mismatch?
9. How does operator ordering interact with element response \(P\), electronic response \(G\), noise injection, and calibration?
10. How does coupling modify manifold vectors, covariance, eigenvalues, eigenspaces, and MUSIC noise-subspace orthogonality?
11. When does inverse decoupling \(C^{-1}\) amplify noise or become numerically/physically ill-conditioned?
12. How should residual coupling error be represented after calibration?
13. How do channel dropout and changed port terminations alter coupling itself rather than merely masking an already-computed matrix?
14. How does GeoDOA prevent coupling double counting when a CST/full-wave/embedded manifold already contains array interactions?
15. What hand-computable examples should become GRP-016 and GRP-017?

Expected conceptual progression:

```text
Electromagnetic / network interaction
        ↓
Port / embedded-response semantics
        ↓
Effective cross-channel coupling model
        ↓
Manifold distortion
        ↓
Covariance distortion
        ↓
Eigenvalue/eigenspace distortion
        ↓
DOA/MUSIC consequence
        ↓
Calibration / inverse-conditioning tradeoff
```

Do not prematurely lock \(a_c=C a\) as a universal law until the physical assumptions behind \(C\) are resolved.

---

# 19. Work Remaining After 3.5

After mutual coupling:

## 3.6 — Channel Delay, Clock Skew, Frequency Error

Must distinguish:

- static narrowband phase offset;
- physical channel delay / phase slope vs frequency;
- sampling-clock skew;
- inter-channel timing skew;
- LO/carrier offset;
- common versus differential frequency error;
- spatial versus temporal phase effects;
- snapshot coherence implications.

## 3.7 — Quantization / Receiver / Dynamic Range

Must cover ADC/receiver effects without collapsing them into generic noise. Quantization, saturation, clipping, AGC, finite ENOB, receiver nonlinearity, and channel-dependent dynamic range may require different semantics.

## 3.8 — Unified Sensor-Imperfection Operator

Only after the component models are understood should the project define whether an ordered composition such as

\[
\mathcal H_{sensor}
=
\mathcal H_{receiver}
\circ
\mathcal H_{coupling}
\circ
\mathcal H_{element}
\circ
\mathcal H_{geometry}
\]

or a matrix specialization is appropriate.

Ordering is scientifically material and generally noncommutative.

## 3.9 — Calibration Models

Parametric calibration, inverse correction, residual error, calibration observability, uncertainty, conditioning, and provenance.

## 3.10 — Direct Measured / CST-Derived Calibration

Define exactly how measured/full-wave complex manifolds enter the processing model without double counting physical effects.

## 3.11 — Error Metrics and Identifiability

Define common-phase/common-scale aligned manifold metrics, parameter observability, ambiguity, calibration residuals, and condition-dependent validity.

## 3.12 — Covariance / Eigenspace / MUSIC Propagation

Systematically connect sensor-model mismatch to covariance, eigenvalue/eigenvector/subspace perturbations and DOA metrics.

## 3.13 — Compatibility / Initial ADR-003 Profile

Define what remains in the initial ideal baseline versus later imperfection/calibration profiles.

## 3.14 — Cross-Consistency Audit

Reconcile all ADR-003 candidate decisions against ADR-001 and ADR-002 before formal acceptance gates begin.

---

# 20. What Happens When ADR-003 Exploration Is Finished

Do not immediately call ADR-003 accepted.

The next lifecycle is:

```text
Reconcile 3.1–3.14
        ↓
Create governing ADR-003 draft with status Proposed / Under Review
        ↓
Gate A — Physical Consistency
        ↓
Gate B — Mathematical Consistency
        ↓
Gate C — Dimensional / Unit Consistency
        ↓
Gate D — Software Semantic Consistency
        ↓
Gate E — Formalize GRP-014 through GRP-017 as needed
        ↓
Gate F — Boundary and Failure Analysis
        ↓
Gate F reconciliation audit if needed
        ↓
Final cross-gate audit
        ↓
Final Acceptance Record
        ↓
Set governing ADR-003 status to Accepted only after all PASS
```

Expected artifact pattern should mirror ADR-001/002, for example:

```text
docs/adr/ADR-003-sensor-imperfections-mutual-coupling-calibration.md
docs/adr/ADR-003_ACCEPTANCE_AUDIT.md
docs/adr/ADR-003_BOUNDARY_FAILURE_ANALYSIS.md
docs/adr/ADR-003_GATE_F_AUDIT.md
docs/adr/ADR-003_FINAL_ACCEPTANCE_RECORD.md
docs/science/golden_reference/ADR-003_GOLDEN_REFERENCE_PROBLEMS.md
```

Exact names may be reconciled before formalization, but do not collapse the evidence into one opaque file.

---

# 21. ADR-004 After ADR-003

ADR-004 remains not started.

Primary question:

> Under what evidence can GeoDOA call a model, algorithm, experiment, or hardware result verified, validated, reproducible, or better than another method?

It will govern:

- ground-truth provenance;
- verification vs physical validation;
- analytical / external-tool / hardware validation;
- Monte Carlo random-variable semantics;
- root-seed and deterministic child-stream policy;
- common random numbers for fair comparisons;
- bias, variance, MSE, RMSE;
- multi-source association;
- misses/false detections;
- resolution vs accuracy;
- probability of resolution;
- failure recording;
- confidence/uncertainty for aggregate metrics;
- fair benchmark requirements;
- complete run/configuration/calibration/software/Git/seed provenance;
- floating-point / fixed-point / FPGA cross-validation.

GRP-018 is reserved for hand-computed bias/variance/MSE/RMSE.

Only after ADR-004 and cross-ADR closure should Phase 0C be considered complete.

---

# 22. Phase 1 Boundary After Phase 0C

Phase 0C is a scientific-contract phase, not an instruction to implement every capability immediately.

The deliberately narrow first validated implementation slice is approximately:

```text
Validated 1-D physical geometry
        ↓
Canonical units / reference semantics
        ↓
Direction-cosine and steering-manifold kernel
        ↓
Declared lattice / difference coarray
        ↓
Stationary far-field narrowband source model
        ↓
Ideal uncoupled sensor baseline
        ↓
Snapshot matrix
        ↓
Sample covariance
        ↓
Baseline subspace / MUSIC
        ↓
Golden Reference verification
```

Then later bounded work packages progressively implement:

```text
Position error
→ Gain/phase mismatch
→ Element response
→ Mutual coupling
→ Calibration
→ Measured/CST manifold
→ Wideband / motion / active-radar extensions
→ Fixed-point
→ FPGA/SoC backend validation
```

Scientific contracts define extension semantics before implementation; they do not force implementation breadth in the first slice.

---

# 23. FPGA / Hardware-Co-Design Direction

Future hardware path must preserve algorithmic equivalence and physical/numerical meaning:

```text
DOA / Array Theory
    ↓
Floating-Point Python Reference
    ↓
Fixed-Point Python Reference
    ↓
Hardware Architecture
    ↓
HLS / RTL
    ↓
AXI / DMA / SoC Integration
    ↓
Timing Closure
    ↓
Board Validation
```

PYNQ-Z2 conceptual path:

```text
Python
  ↓
ARM / PS
  ↓
AXI / DMA
  ↓
FPGA / PL
  ↓
result back to PS / Python
```

Future backend abstraction may include, for example:

- NumPy reference backend;
- fixed-point emulation backend;
- FPGA backend.

Hardware validation is not only latency/resource reporting. Eventually compare:

- covariance error;
- eigen/eigenspace/subspace error;
- pseudospectrum error;
- DOA error;
- latency;
- initiation interval;
- throughput;
- DSP/BRAM/LUT/FF utilization.

---

# 24. Terminology Rules for the Next Chat

Use these distinctions consistently:

```text
Physical / Scientific Model Profile
    ≠
Algorithm / Benchmark Baseline
    ≠
Numerical / Hardware Reference
```

Examples:

- PM-001 is a physical/scientific model profile.
- Classical MUSIC is an algorithm/estimator baseline.
- Float64, fixed-point, and FPGA are numerical/hardware execution references/backends.

Avoid calling a physical profile a “baseline algorithm.”

Similarly:

```text
Nominal manifold
≠ Physical manifold
≠ Measured manifold
≠ EM-simulated manifold
≠ Calibrated processing manifold
```

and:

```text
Geometry error
≠ Electronic gain/phase mismatch
≠ Element pattern/polarization
≠ Mutual coupling
≠ Measurement noise
```

unless an explicitly declared effective model intentionally aggregates them.

---

# 25. Instructions to the Next Chat

When this handoff is pasted or referenced in a new chat:

1. Treat the Git repository and current branch files as the persistent source of truth.
2. Inspect the branch before writing; do not reconstruct repository state from memory alone.
3. Read:
   - `docs/PHASE0C_SCIENTIFIC_CONTRACTS_ROADMAP.md`
   - `docs/adr/ADR-001-coordinate-direction-spatial-conventions.md`
   - `docs/adr/ADR-002-wave-propagation-signal-measurement-model.md`
   - `docs/adr/ADR-003_EXPLORATION_CHECKPOINT.md`
   - this continuation handoff.
4. Do not modify or merge `main`.
5. Do not mark ADR-003 Accepted.
6. Do not start Gate A yet.
7. Continue directly with **Exploration 3.5 — Mutual Coupling**.
8. Explain the physics and mathematics in depth before proposing software structures.
9. Preserve candidate decisions from each exploration for later reconciliation.
10. Build GRP-016/017 only after the mutual-coupling model is sufficiently stable.
11. After 3.14, perform Gates A–F with the same rigor used for ADR-001/002.
12. Keep all physical approximations explicit and provenance-preserving.
13. When uncertain about a scientific claim, verify it rather than silently guessing.
14. Do not expand scope merely because the architecture could support it; prefer a smaller scientifically defensible capability.

Preferred discussion style with the user:

- Persian explanation;
- English technical terminology retained;
- equations and matrix forms shown explicitly;
- physical interpretation before abstraction;
- detailed engineering examples;
- hand-solvable numerical examples when useful;
- distinguish established decisions from candidate/deferred decisions.

---

# 26. Current Repository Checkpoint at Handoff Creation

Before this handoff was created, the Phase 0C branch was verified as:

```text
branch: docs/phase0c-scientific-conventions
relative to main: ahead, behind_by = 0
main / merge-base: 496187c9ebe3baa2a426f81a8f0af3fdd54f7892
```

ADR-001 and ADR-002 governing files both explicitly report:

```text
Accepted — all Phase 0C acceptance Gates A–F passed
```

ADR-003 exploration checkpoint was then added to the same branch as a non-accepted scientific checkpoint.

No Phase 0C PR or merge has been performed by this handoff.

`HANDOFF_INDEX.md` intentionally remains unchanged because this is a continuation checkpoint, not a closed material milestone.

---

# 27. Resume Command for the Next Chat

The next chat should conceptually resume with:

> **Continue GeoDOA Studio Phase 0C from `docs/phase0c-scientific-conventions`. ADR-001 and ADR-002 are Accepted. ADR-003 explorations 3.1–3.4 are complete and checkpointed. Begin ADR-003 Exploration 3.5 — Mutual Coupling. Do not start acceptance Gates yet and do not merge. Preserve the established scientific-contract / GRP / Gate workflow.**

That is the exact continuation point.
