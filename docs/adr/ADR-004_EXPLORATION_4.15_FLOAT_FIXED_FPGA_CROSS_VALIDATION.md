# ADR-004 Exploration 4.15 — Floating-Point, Fixed-Point, and FPGA Cross-Validation

- **ADR:** ADR-004 — Validation, Reproducibility, and Scientific Evidence
- **Phase:** 0C — Scientific Foundations
- **Exploration:** 4.15
- **Status:** EXPLORATION COMPLETE — CANDIDATE CONTRACT, NOT ACCEPTED
- **Depends on:** Accepted ADR-001, ADR-002, ADR-003; ADR-004 Explorations 4.1–4.14

## 1. Question

> What evidence shall GeoDOA require before claiming that a fixed-point, HLS/RTL, or FPGA/SoC implementation faithfully preserves an accepted floating-point scientific algorithm, and how shall numerical degradation, implementation correctness, timing/resource behavior, and physical hardware validation remain distinct?

This exploration defines the cross-validation chain that connects scientific array/DOA algorithms to real-time embedded implementation without allowing hardware agreement alone to substitute for scientific correctness.

---

## 2. Core Principle

Hardware implementation evidence is layered.

Candidate chain:

```text
accepted scientific model / algorithm contract
        ↓
verified floating-point reference implementation
        ↓
fixed-point numerical model
        ↓
bit-accurate implementation model
        ↓
HLS / RTL implementation
        ↓
post-synthesis / post-route implementation
        ↓
FPGA/SoC board execution
        ↓
physical sensor/system validation
```

Candidate rule:

> Each layer shall be validated against the nearest accepted upstream scientific reference, while preserving enough internal diagnostics to localize disagreement; agreement between two downstream implementations does not establish correctness if their common upstream reference is wrong.

---

## 3. Scientific Correctness Precedes Hardware Equivalence

Before float output may serve as an implementation reference, the floating-point scientific kernel must itself be supported by accepted evidence such as:

```text
scientific contract
analytical derivation
Golden Reference Problems
independent/cross-tool evidence where appropriate
unit/property/regression verification
accepted conventions from ADR-001/002/003
```

Candidate rule:

> FPGA-vs-Python agreement proves implementation consistency only relative to the Python reference; it does not by itself verify the underlying physics or mathematics.

---

## 4. Floating-Point Reference Role

A floating-point implementation may be promoted to a downstream reference only after its scope is declared.

Example:

```text
reference role: accepted software implementation reference
precision: float64
algorithm/profile: MUSIC Phase-1 profile vX
input semantics: canonical digital snapshots
output semantics: covariance/eigenspace/spectrum/DOA
```

Candidate rule:

> `float reference` is a versioned evidence role, not an eternal or universal truth object.

If the scientific contract changes, the reference must be re-audited.

---

## 5. Float32 versus Float64

Float32 and float64 are distinct numerical implementations.

Candidate rule:

> If float32 is used as the hardware-oriented reference, its degradation relative to the accepted float64/scientific reference shall be measured first rather than assumed negligible.

This may be especially important for covariance conditioning, eigendecomposition, small eigengaps, or narrow peak localization.

---

## 6. Fixed-Point Numerical Contract

A fixed-point number requires more than total word length.

Candidate fixed-point provenance includes:

```text
signed/unsigned
word length W
integer width I or fractional width F
binary-point convention
rounding mode
truncation mode
saturation vs wraparound
overflow behavior
underflow/subnormal-equivalent behavior if any
intermediate accumulator widths
cast locations
coefficient quantization
complex real/imag formats
```

Candidate rule:

> Fixed-point format is a numerical contract at every material internal state, not a single global `Q-format` label.

---

## 7. Quantization Error versus Algorithm Error

For a scalar quantizer with step `Delta`, local deterministic quantization error may satisfy

\[
e_q=x_q-x
\]

with a bound determined by the rounding/truncation rule when no saturation occurs.

But downstream DOA degradation is generally nonlinear:

\[
\text{quantization error}
\rightarrow
\Delta R
\rightarrow
\Delta U_s
\rightarrow
\Delta P(\theta)
\rightarrow
\Delta\hat\theta.
\]

Candidate rule:

> A small per-sample quantization error does not by itself establish acceptable DOA degradation; numerical effects shall be propagated and evaluated through the scientific outputs.

---

## 8. Rounding and Truncation Are Scientifically Relevant

Rounding and truncation can introduce different bias/noise behavior.

Candidate rule:

> Rounding mode shall be part of fixed-point provenance wherever it can affect covariance bias, accumulated power, eigenspace, threshold crossing, or final DOA output.

Stochastic rounding, if used, introduces algorithmic/numerical randomness and shall use a separate RNG role under Exploration 4.5.

---

## 9. Saturation versus Wraparound

Overflow handling can dominate numerical behavior.

Candidate rule:

> Saturation and modular wraparound are different numerical systems and shall never be treated as interchangeable implementation details.

For scientific DSP pipelines, any saturation/wrap event that affects accepted output must be counted and classified under the failure/degradation policy from Exploration 4.13.

---

## 10. Dynamic Range Analysis

Fixed-point design shall be supported by range evidence.

Candidate range evidence may include:

```text
analytical bounds
Golden Reference extrema
Monte Carlo observed extrema
stress-test extrema
headroom margins
per-stage histogram / quantile diagnostics
saturation counts
```

Candidate rule:

> Word-length selection shall not rely only on one favorable data trace; expected and boundary dynamic ranges shall be analyzed at material pipeline stages.

---

## 11. Analytical Bound versus Empirical Range

Analytical bounds may be conservative, while empirical Monte Carlo ranges may miss rare extremes.

Candidate rule:

> Analytical range bounds and empirical observed ranges are complementary evidence and shall be labeled separately.

A fixed-point design may use both to balance safety margin and resource efficiency.

---

## 12. Covariance Accumulation Requires Special Care

For snapshots `x[l]`, covariance accumulation contains products and sums:

\[
\hat R
=
\frac{1}{L}\sum_{l=1}^{L}x[l]x^H[l].
\]

Accumulator width can require substantially more dynamic range than input width.

Candidate rule:

> Fixed-point covariance design shall declare product width, accumulator width, scaling/division policy, Hermitian handling, and cast points separately from input sample format.

Overflow-free inputs do not guarantee overflow-free covariance accumulation.

---

## 13. Matrix Scaling and Normalization

Hardware implementations may scale matrices to fit numeric range.

Examples:

```text
block normalization
power-of-two shifts
trace normalization
maximum-magnitude normalization
```

Candidate rule:

> Scaling transforms shall be scientifically explicit and shall preserve or intentionally alter the downstream algorithm semantics in a documented way.

Scale invariance may exist for some subspace/eigenvector operations but not for all diagnostics/thresholds.

---

## 14. Eigensolver Cross-Validation

Eigendecomposition is particularly sensitive to:

```text
finite precision
matrix conditioning
eigengap
iteration count
deflation/ordering
normalization
complex arithmetic
```

Candidate rule:

> Hardware/fixed-point eigensolver validation shall compare eigenvalues, relevant eigengaps, signal/noise subspace projectors, and principal angles—not only individual eigenvector entries.

This inherits Exploration 4.14.

---

## 15. Eigenvector Phase and Basis Gauge

Even correct eigensolvers may return eigenvectors differing by arbitrary complex phase; repeated eigenvalues permit basis rotation within a subspace.

Candidate rule:

> Bitwise or elementwise eigenvector equality is not a valid universal correctness requirement; gauge-aware projector/principal-angle comparisons are authoritative where the scientific object is the subspace.

---

## 16. Spectrum Cross-Validation

For algorithms such as MUSIC, fixed/FPGA cross-validation should retain:

```text
truth-direction leakage
spectrum representation/normalization
common angle grid
peak locations
peak ordering
peak prominence/threshold crossings
resolution event
final associated DOAs
```

Candidate rule:

> Two implementations may have similar global spectrum norms yet different peak/detection outputs, so spectrum and event-level comparisons shall both be retained.

---

## 17. Earliest-Divergence Principle

When FPGA output disagrees with float output, debug should seek the earliest scientifically meaningful divergence.

Candidate sequence:

```text
input samples
→ preprocessing
→ covariance
→ eigenvalues/eigenspace
→ spectrum/objective
→ peak extraction
→ association/event
→ final DOA
```

Candidate rule:

> Cross-validation shall compare available intermediate checkpoints before attributing error to the final estimator stage.

This prevents terminal RMSE from obscuring the actual hardware/numerical failure mechanism.

---

## 18. Bit-Accurate Model

A bit-accurate software model reproduces the fixed-point arithmetic semantics intended for hardware.

Candidate requirements:

```text
same word lengths
same casts
same rounding
same saturation/wrap behavior
same coefficient quantization
same operation ordering where it affects results
same reset/state semantics where relevant
```

Candidate rule:

> A fixed-point model that only approximates word lengths but differs in cast/order/overflow semantics is not sufficient evidence for bit-accurate hardware equivalence.

---

## 19. Bit-Exact versus Numerically Equivalent

Two valid evidence targets exist.

### 19.1 Bit-exact equivalence

Every declared output bit matches the bit-accurate reference for a deterministic test vector.

### 19.2 Numerically equivalent / bounded degradation

Outputs differ numerically but remain within accepted metric tolerances.

Candidate rule:

> GeoDOA shall state which target is required at each interface; bit-exactness is strongest for deterministic integer datapaths but may be inappropriate across mathematically equivalent floating/HLS implementations with reordered operations.

---

## 20. Operation Reordering

Associativity does not hold exactly in finite-precision arithmetic.

For example,

\[
(a+b)+c
\ne
 a+(b+c)
\]

numerically in finite precision.

Pipelining, tree reduction, unrolling, or HLS scheduling can change operation order.

Candidate rule:

> HLS/RTL transformations that alter operation ordering may legitimately alter low-order numerical bits; such differences shall be evaluated under the declared numerical-equivalence contract rather than assumed to be bugs or ignored silently.

---

## 21. HLS Reference Hierarchy

A candidate HLS verification hierarchy is:

```text
C/C++ functional model
↓
fixed-point/bit-accurate C simulation
↓
HLS C simulation
↓
HLS co-simulation / generated RTL
↓
post-synthesis/post-route simulation where required
↓
on-board execution
```

Candidate rule:

> Each transition shall preserve deterministic test vectors and comparable internal/output evidence where practical.

Exact tool-specific workflow remains an implementation decision, not a Phase 0C scientific contract.

---

## 22. RTL Reference Hierarchy

For hand-written RTL, comparable stages may include:

```text
bit-accurate software oracle
RTL simulation
post-synthesis simulation
post-route/timing-aware simulation where needed
FPGA board execution
```

Candidate rule:

> RTL simulation agreement is implementation verification evidence; board execution additionally validates integration under actual clocking, interfaces, reset, transport, and device behavior.

---

## 23. Deterministic Test Vectors before Monte Carlo

Before large stochastic hardware campaigns, deterministic vectors should test:

```text
zero/min/max values
sign changes
known covariance structures
Golden Reference Problems where applicable
boundary word-length cases
overflow/saturation boundaries
simple eigenspace cases
known peak cases
```

Candidate rule:

> Deterministic reference vectors establish implementation semantics first; Monte Carlo performance evidence does not replace these boundary/verification tests.

---

## 24. Canonical Digital Stimulus

For float/fixed/FPGA comparison, all implementations should receive the same canonical digital stimulus when sample-for-sample equivalence is intended.

Candidate forms:

```text
frozen binary/hex stimulus artifact
content-addressed snapshot matrix
reconstructable RNG/trial identity with declared quantization
```

Candidate rule:

> Input transport/reformatting shall not silently change the scientific stimulus.

Any host-side preprocessing must be included in the pipeline scope or frozen upstream.

---

## 25. Host–FPGA Boundary

On SoC systems, the algorithm may be split between host/PS and FPGA/PL.

Candidate rule:

> Cross-validation shall declare which operations occur on host versus programmable logic and which boundary representation is authoritative.

Examples:

```text
Python builds covariance, FPGA performs spectrum
FPGA builds covariance and eigenspace, PS performs peak extraction
full streaming pipeline in PL
```

These are different implementation profiles.

---

## 26. Interface Semantics

AXI-Stream, AXI memory-mapped, DMA, FIFOs, and packetized transports can introduce engineering failure modes independent of scientific arithmetic.

Candidate provenance includes:

```text
sample order
channel order
frame length
TLAST / packet boundary semantics
endianness
complex packing
word alignment
scaling metadata
DMA transfer size
reset/restart state
```

Candidate rule:

> Interface semantics are part of hardware implementation validity and shall be separated from kernel numerical correctness.

---

## 27. Channel Ordering Is Scientific Semantics

Sensor/channel permutation changes the relationship between samples and manifold rows.

Candidate rule:

> Host/FPGA channel ordering must preserve the stable channel identity established by ADR-001; silent hardware reorder is a scientific data-integrity failure, not a cosmetic formatting issue.

---

## 28. Latency, Initiation Interval, and Throughput

Hardware timing metrics are distinct.

For a pipelined block:

- **latency** = cycles/time from accepted input event to corresponding output;
- **initiation interval (II)** = minimum cycles between accepted new transactions/iterations;
- **throughput** = sustained output/input processing rate under declared conditions.

Candidate rule:

> Latency, II, and throughput shall not be used interchangeably.

Clock frequency is required to convert cycles to time/rate.

---

## 29. Deterministic Latency

Many real-time sensing systems value bounded/deterministic latency.

Candidate rule:

> If deterministic latency is claimed, GeoDOA shall record latency distribution/bounds under the declared pipeline, host transfer, buffering, and scheduling scope rather than quote only average kernel latency.

---

## 30. Timing Closure Is Implementation Evidence

Post-route timing evidence may include:

```text
requested clock period
achieved timing
WNS/TNS or equivalent timing diagnostics
clock domains
critical path
```

Candidate rule:

> Functional simulation success does not establish that an FPGA design meets its intended real-time clock requirement.

Conversely, timing closure does not establish numerical/scientific correctness.

---

## 31. Resource Metrics

Hardware resource metrics may include:

```text
LUT
FF
DSP blocks
BRAM
URAM where available
on-chip memory bandwidth
external memory bandwidth
```

Candidate rule:

> Resource use shall be reported with device/part, tool version, synthesis settings, and implementation scope.

Comparing resource percentages across different FPGA families without context is weak evidence.

---

## 32. Power and Energy

If measured/estimated, distinguish:

```text
static power
dynamic power
total board power
kernel energy per estimate/frame
instrument-estimated vs measured power
```

Candidate rule:

> Power/energy evidence shall declare measurement/estimation method and scope; synthesis power estimate is not the same evidence as board power measurement.

---

## 33. Scientific Accuracy versus Hardware Efficiency

A hardware implementation may trade accuracy for resources or throughput.

Candidate rule:

> Word-length/resource optimization shall be treated as a multi-objective design problem with scientific-error constraints, not as resource minimization alone.

A useful Pareto space may include:

```text
DOA degradation
P_res degradation
failure/saturation rate
latency
throughput
DSP/BRAM/LUT
power
```

---

## 34. Fixed-Point Acceptance Margin

An implementation may be considered scientifically acceptable if degradation stays within a declared practical margin.

Examples:

```text
|ΔRMSE| <= delta_RMSE
P_res_fixed >= P_res_float - delta_P
max principal angle <= delta_subspace
no unacceptable saturation
```

Candidate rule:

> Acceptance margins are profile/application decisions and shall be predeclared or transparently justified; `not statistically different` is not sufficient evidence of equivalence.

This inherits Exploration 4.11.

---

## 35. Deterministic Bounds versus Statistical Equivalence

For deterministic test suites, evidence may use:

```text
max absolute error
max relative error
ULP/LSB difference
exact mismatch count
worst-case projector/spectrum/DOA deviation
```

For stochastic trial populations, evidence may use:

```text
paired RMSE degradation
paired P_res difference
failure-rate difference
confidence/equivalence intervals
```

Candidate rule:

> Deterministic regression bounds and stochastic population equivalence are different evidence classes and shall not be conflated.

---

## 36. Fixed-Point Error through the DOA Chain

Candidate cross-validation record per trial/condition may include:

```text
input quantization error
covariance relative error
Hermitian/PSD diagnostics
eigenvalue error
eigengap
projector/principal-angle error
MUSIC truth leakage
spectrum error
peak/event mismatch
associated DOA error
resolution outcome
saturation/overflow diagnostics
```

Candidate rule:

> Numerical degradation shall be traced through the multi-level chain from Exploration 4.14 so that final DOA disagreement has a diagnosable mechanism.

---

## 37. Threshold Crossing Sensitivity

Small numeric perturbations can change discrete decisions:

```text
peak above/below threshold
model-order estimate K
peak ordering
minimum-distance suppression
resolution success/failure
```

Candidate rule:

> Cross-validation shall include event-level agreement, not only continuous numeric-error norms, when discrete postprocessing decisions are present.

---

## 38. Model-Order Sensitivity

If fixed-point perturbation changes eigenvalue ordering or model-order selection, the downstream subspace dimension can change abruptly.

Candidate rule:

> Model-order mismatch is a typed cross-validation event and shall not be hidden inside a large final RMSE.

---

## 39. Reproducibility of Hardware Builds

Exact bitstream reproduction may depend on:

```text
toolchain version
IP versions
part/board definition
constraints
synthesis/place-route seeds
compiler flags
HLS directives
source revision
```

Candidate rule:

> Hardware provenance shall be sufficient to reproduce or at least identify the exact implementation build used for scientific evidence.

Exact bit-for-bit bitstream reproducibility is a separate claim from functional reproduction.

---

## 40. HLS Pragmas / Architecture Are Performance Decisions

Pipeline, unroll, array partition, resource binding, dataflow, loop restructuring, and memory architecture affect:

```text
latency
II
resource use
operation ordering
sometimes numerical behavior
```

Candidate rule:

> Architecture directives are implementation provenance and shall not be allowed to silently change the accepted scientific semantics.

If they change finite-precision arithmetic order, the resulting numerical difference must remain inside the declared cross-validation contract.

---

## 41. Software-Hardware Co-Design Iteration

A valid design loop may be:

```text
float scientific reference
→ fixed-point sensitivity study
→ architecture candidate
→ HLS/RTL implementation
→ cross-validation
→ resource/timing analysis
→ revise word lengths/architecture
→ revalidate scientific behavior
```

Candidate rule:

> Every architecture/precision change that can affect scientific output shall trigger the relevant cross-validation subset before evidence is accepted.

---

## 42. Physical Board Validation Is a Different Layer

Running the design successfully on an FPGA board confirms actual integration under real hardware interfaces and clocks.

But if synthetic vectors are injected, this is still digital implementation validation rather than physical sensor validation.

Candidate rule:

> Board execution with synthetic/frozen stimuli validates implementation/integration; physical array/sensor validation requires real sensor/acquisition/reference evidence under the accepted validation contract.

---

## 43. Hardware-in-the-Loop

Hardware-in-the-loop may use synthetic/generated samples delivered through actual board interfaces.

Candidate rule:

> HIL evidence lies between pure simulation and full physical sensor validation; its claim scope shall state which physical components/interfaces are real and which are simulated.

---

## 44. Real Sensor Validation

A complete sensor/FPGA system study may include:

```text
physical array
RF/analog chain
ADC/acquisition
FPGA/SoC processing
external DOA reference
calibration/environment provenance
```

Candidate rule:

> End-to-end physical validation shall report both scientific DOA performance and implementation/system metrics; success on synthetic FPGA vectors cannot substitute for this evidence.

---

## 45. Timing and Numerical Validation Are Orthogonal

A design can be:

```text
numerically correct but too slow
fast but numerically inaccurate
both correct and fast
neither
```

Candidate rule:

> Timing/resource acceptance and scientific numerical acceptance are separate gates/axes of evidence.

---

## 46. Hardware Failure Taxonomy Integration

Exploration 4.13 hardware states apply, including:

```text
DMA timeout
frame mismatch
stream under/overflow
AXI/protocol error
bitstream mismatch
fixed-point overflow
saturation policy violation
timing requirement failure
resource-limit failure
board reset/transport failure
```

Candidate rule:

> These implementation failures shall remain distinct from scientific estimator misses/resolution failures.

---

## 47. Comparison Fairness across Implementations

When comparing float, fixed, and FPGA performance:

```text
same canonical stimulus
same algorithm/profile
same truth/reference
same evaluation metrics
same association/event semantics
same failure accounting
```

shall be preserved unless the comparison intentionally studies a changed pipeline.

Candidate rule:

> Cross-validation shall isolate implementation/precision effects from unrelated changes in preprocessing, calibration, search grid, or estimator configuration.

---

## 48. Performance Timing Scope

Possible timing scopes include:

```text
FPGA kernel latency only
DMA + kernel
PS preprocessing + DMA + kernel + postprocessing
end-to-end frame acquisition-to-DOA
steady-state streaming throughput
single-shot cold-start latency
```

Candidate rule:

> Every latency/throughput claim shall name its timing scope; kernel-only speedup shall not be presented as end-to-end system speedup.

---

## 49. Speedup Definition

For reference time `T_ref` and accelerated time `T_acc`,

\[
S=\frac{T_{ref}}{T_{acc}}.
\]

Candidate rule:

> Speedup is meaningful only when numerator and denominator cover comparable work and timing scope.

A CPU float64 full pipeline versus FPGA kernel-only timing is not a valid direct speedup claim.

---

## 50. Throughput versus Source Count / Problem Size

Hardware throughput may depend on:

```text
N sensors
L snapshots
K/model order
angle grid size
matrix dimension
precision
batch size
```

Candidate rule:

> Hardware performance shall be reported against declared problem dimensions and shall not be generalized across sizes without evidence.

---

## 51. Candidate Phase-1 Cross-Validation Profile

For an initial GeoDOA/EE6800-style narrowband DOA hardware prototype, a conservative candidate is:

```text
1. establish accepted float64 scientific reference
2. quantify float32 degradation if used
3. define per-stage fixed-point formats and arithmetic semantics
4. build bit-accurate software model
5. use deterministic canonical test vectors
6. compare input/preprocessing/covariance/eigenspace/spectrum/DOA checkpoints where accessible
7. require explicit saturation/overflow diagnostics
8. compare HLS/RTL against bit-accurate model
9. compare FPGA board outputs against the same frozen stimuli
10. separately report latency, II, throughput, resources, and timing closure
11. run stochastic paired trials for end-task degradation only after deterministic equivalence is established
12. treat physical array/sensor validation as a later distinct layer
```

This remains candidate until ADR-004 acceptance.

---

## 52. Invalid / Weak Cross-Validation Practices

The following are scientifically weak or invalid unless explicitly justified:

1. claim FPGA correctness because it matches an unverified Python script;
2. compare only final DOA and ignore earlier covariance/eigenspace divergence;
3. use one global fixed-point word length without documenting intermediate formats/casts;
4. ignore rounding/saturation policy;
5. treat no observed overflow in a small test as proof overflow cannot occur;
6. require raw eigenvector equality despite arbitrary phase/basis rotation;
7. use different input realizations for float and FPGA and call differences quantization error;
8. change search grid/preprocessing simultaneously with fixed-point conversion and attribute all degradation to precision;
9. claim equivalence because a difference is not statistically significant;
10. compare kernel FPGA latency to end-to-end CPU runtime as direct speedup;
11. report II as latency or latency as throughput;
12. treat timing closure as evidence of numerical correctness;
13. treat HLS simulation agreement as full board/system validation;
14. treat synthetic board input as physical array validation;
15. omit tool/bitstream/source provenance from hardware evidence;
16. erase saturation/overflow/failure trials before aggregate metrics;
17. optimize resources after changing word lengths without revalidating scientific behavior;
18. compare resource percentages across different FPGA parts without device context.

---

## 53. Cross-ADR Reconciliation

### ADR-001

Stable channel identity, coordinate order, phase reference, and no-silent-reindexing govern hardware sample/manifold interfaces.

### ADR-002

Snapshot, covariance, source/noise, and signal-model semantics define the canonical digital stimulus and reference outputs.

### ADR-003

ADC quantization remains distinct from FPGA fixed-point arithmetic; calibration/sensor mismatch/colored-noise semantics remain upstream scientific model variables rather than implementation artifacts.

### ADR-004 Exploration 4.3

Accepted float software may become a downstream reference only after deterministic scientific verification; saved outputs from unverified code are not scientific oracles.

### ADR-004 Explorations 4.5 and 4.12

Canonical trial identity and CRN/fairness preserve identical stochastic stimuli for implementation comparisons.

### ADR-004 Exploration 4.13

Overflow, saturation, protocol, timing, and transport states remain typed hardware failures/degradations.

### ADR-004 Exploration 4.14

Cross-validation uses the multi-level manifold/covariance/eigenspace/spectrum/DOA diagnostic chain.

**Cross-ADR result: no contradiction identified.**

---

## 54. Candidate Decisions from Exploration 4.15

- **D4.15-01:** Scientific correctness, floating-point reference verification, fixed-point equivalence, RTL/HLS implementation verification, board integration, and physical sensor validation are distinct evidence layers.
- **D4.15-02:** A floating-point implementation may serve as a downstream reference only after accepted scientific/deterministic verification within a declared scope/version.
- **D4.15-03:** Float32 degradation relative to the accepted reference shall be measured when float32 is used as an implementation baseline.
- **D4.15-04:** Fixed-point provenance includes per-stage word format, rounding, saturation/wrap, casts, accumulator width, coefficient quantization, and operation semantics.
- **D4.15-05:** Input-level quantization error alone is insufficient; degradation shall be evaluated through covariance, eigenspace, spectrum, event, and DOA outputs.
- **D4.15-06:** Dynamic-range evidence shall combine declared analytical/boundary and empirical diagnostics; lack of observed overflow alone is not proof of safety.
- **D4.15-07:** Covariance accumulation requires explicit product/accumulator/scaling/cast semantics.
- **D4.15-08:** Eigensolver cross-validation shall prefer eigenvalue/eigengap/projector/principal-angle metrics over raw eigenvector equality when gauge/nonuniqueness applies.
- **D4.15-09:** Spectrum and event-level outputs shall be validated in addition to continuous numerical norms.
- **D4.15-10:** The earliest-divergence principle shall guide implementation diagnosis through accessible internal checkpoints.
- **D4.15-11:** Bit-accurate reference models must reproduce hardware arithmetic semantics, not merely approximate word lengths.
- **D4.15-12:** Bit-exact and bounded numerical-equivalence targets are distinct and shall be declared per interface/test.
- **D4.15-13:** Operation reordering from pipelining/unrolling/HLS may change low-order finite-precision results and must remain inside the declared numerical-equivalence contract.
- **D4.15-14:** Deterministic canonical digital stimuli precede stochastic performance campaigns for implementation verification.
- **D4.15-15:** Host/FPGA partition and interface/channel-order semantics are part of implementation validity.
- **D4.15-16:** Latency, initiation interval, throughput, timing closure, resource use, and power are distinct engineering metrics and separate from scientific-error metrics.
- **D4.15-17:** Fixed-point/hardware acceptance requires explicit engineering/scientific margins; absence of statistical significance does not prove equivalence.
- **D4.15-18:** Deterministic regression bounds and stochastic population degradation/equivalence are distinct evidence classes.
- **D4.15-19:** Hardware architecture/precision changes that can affect scientific outputs require revalidation.
- **D4.15-20:** FPGA board execution on synthetic/frozen vectors establishes digital implementation/integration evidence, not physical sensor validation.
- **D4.15-21:** HIL evidence shall state which components are physical and which are simulated.
- **D4.15-22:** End-to-end physical array/FPGA validation requires real acquisition/reference/calibration/environment evidence beyond synthetic board tests.
- **D4.15-23:** Timing/resource acceptance and numerical/scientific acceptance are orthogonal evidence axes.
- **D4.15-24:** Hardware build provenance shall identify source revision, tool/IP versions, target part/board, constraints, directives/settings, and bitstream/build identity.
- **D4.15-25:** Speedup claims require comparable timing scopes and problem dimensions; kernel-only acceleration shall not be mislabeled end-to-end speedup.

---

## 55. Exploration 4.15 Conclusion

Exploration 4.15 is complete at candidate-contract level.

The central rule is:

> GeoDOA shall validate the path from scientific algorithm to FPGA as a layered, traceable equivalence chain: accepted scientific reference → verified floating-point software → explicit fixed-point arithmetic model → bit-accurate/HLS/RTL implementation → FPGA/SoC execution → physical sensor/system validation. Numerical degradation shall be diagnosed through intermediate scientific states, hardware timing/resources shall remain separate engineering evidence, and board-level agreement with synthetic stimuli shall never be promoted silently to physical validation.

No acceptance gate is started or passed by this exploration.

The next exploration is:

```text
4.16 — Run Identity, Configuration Hash, and Provenance
```
