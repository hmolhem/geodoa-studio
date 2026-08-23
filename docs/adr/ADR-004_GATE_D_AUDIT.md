# ADR-004 Gate D — Software Semantic Consistency Audit

- **ADR:** ADR-004 — Validation, Reproducibility, and Scientific Evidence
- **Phase:** 0C — Scientific Foundations
- **Gate:** D — Software Semantic Consistency
- **Gate result:** **PASS**
- **Governing draft:** `ADR-004-validation-reproducibility-scientific-evidence.md`
- **Reviewed governing content SHA:** `8cca2e3ac514cd031bee1d8c9e4c0347694ecb53`
- **Pre-Gate review:** PASS
- **Gate A:** PASS
- **Gate B:** PASS
- **Gate C:** PASS
- **Gates E–F:** Not evaluated by this audit
- **ADR-004 acceptance:** NOT ACCEPTED

> Gate D evaluates whether the scientific contract can be implemented without software behavior silently changing scientific meaning. Because authoritative Phase-1 implementation is intentionally blocked until ADR-004 acceptance, this Gate is a semantic-contract audit, not a production-code acceptance test.

---

## 1. Gate D Criterion

Gate D asks whether software boundaries, object identities, defaults, transformations, random-state behavior, failure handling, caching/resume logic, implementation comparison, and evidence storage can preserve the scientific semantics accepted by ADR-001/002/003 and defined by ADR-004.

A software system fails Gate D conceptually if a scientifically important distinction exists in documentation but can disappear silently in execution.

Examples of forbidden semantic collapse include:

```text
source count == model order == detected peak count
sample covariance == uncentered second moment
root seed == full stochastic provenance
NaN == scientific failure type
successful-trial subset == original Monte Carlo population
same filename == same artifact
same branch == same source revision
same numeric array == same units/frame/reference role
same FPGA output == physical validation
```

---

## 2. Audit Scope

Gate D evaluates:

```text
D1   domain identity and typed scientific roles
D2   authoritative inputs vs derived values
D3   canonical units / boundary conversion
D4   stable channel and source/trial identities
D5   configuration resolution and hidden defaults
D6   RNG ownership / deterministic child streams / parallel execution
D7   association and event-evaluation ordering
D8   failure/status/metric-eligibility separation
D9   denominator preservation and no silent filtering
D10  covariance/second-moment object distinction
D11  numerical repair / normalization / sorting behavior
D12  cache/resume/retry semantics
D13  algorithm information/oracle provenance
D14  software implementation/version identity
D15  data/calibration/external-artifact identity
D16  fixed-point/HLS/RTL/FPGA boundary semantics
D17  publication artifact immutability and lineage
D18  API/schema implementation freedom without scientific drift
```

---

## 3. No Authoritative Implementation Yet

ADR-004 explicitly states that authoritative Phase-1 implementation is not authorized before final ADR acceptance.

Therefore Gate D does not certify current production classes, APIs, schemas, or CLI behavior.

It certifies that the governing contract contains enough semantic constraints for later implementation reviews/tests to distinguish compliant from noncompliant behavior.

### Gate-D finding

**PASS.** Gate D is correctly scoped as a software-semantic contract audit rather than premature code acceptance.

---

## 4. Domain Identity Must Survive Software Representation

ADR-004 requires distinct identity layers for:

```text
study
condition
trial / trial ensemble
algorithm
implementation
run / execution
data / calibration / external artifact
derived result / figure / table
hardware build
```

It also preserves distinct structural quantities:

```text
snapshot count L
Monte Carlo trial count N
source count K
source-covariance rank
observed subspace rank
model order
estimated-output cardinality K_hat
matched-pair/source-opportunity count
```

### Software rule

These distinctions may share compact internal data structures, but software shall not use one overloaded integer/string/status field whose meaning depends implicitly on call context.

### Gate-D finding

**PASS.** The contract supports explicit domain identity and rejects semantic overloading.

---

## 5. Authoritative Inputs versus Derived Values

ADR-001/002 establish authoritative physical quantities such as geometry positions, frequency/medium context, channel identity, and declared model/profile state.

ADR-004 configuration canonicalization preserves authoritative-versus-derived semantics.

Examples:

```text
frequency + propagation speed -> derived wavelength
resolved source/noise model -> derived SNR realization parameters
trial identity + RNG policy -> derived child streams
run + metric policy -> derived aggregate result
```

### Software rule

A derived value shall not silently become a second independent authoritative input if inconsistency can arise.

### Gate-D finding

**PASS.** The provenance/configuration contract supports one-source-of-truth semantics for dependent quantities.

---

## 6. Units and Boundary Conversion

Gate C established canonical unit semantics. Gate D requires these units to survive software boundaries.

### Software rule

External values such as:

```text
deg
GHz
MHz
cm
ns
dB
```

may be accepted only through validated conversion boundaries. Numerical kernels should operate on canonical resolved quantities rather than infer units from magnitude or field names.

Canonical configuration hashing occurs after declared unit normalization, while the original user-facing representation may remain in audit metadata.

### Forbidden behavior

```text
angle=30 interpreted sometimes as degrees and sometimes radians
0.5 geometry interpreted as meters or wavelengths based on magnitude
10 dB passed into a linear-ratio computation without conversion
```

### Gate-D finding

**PASS.** Unit conversion is a boundary concern and no hidden unit inference is authorized.

---

## 7. Stable Channel Identity and Ordering

ADR-001 makes channel identity authoritative and rejects silent reindexing/sorting.

ADR-004 extends this requirement into data, FPGA, and publication provenance.

### Software rule

Matrix row order, visualization order, sorted geometry order, active-channel mask order, DMA packing order, and physical channel identity are separate concepts unless an explicit mapping establishes equivalence.

Any permutation shall be:

```text
explicit
invertible where required
provenance-preserving
applied consistently to geometry/manifold/data/calibration
```

### Gate-D finding

**PASS.** Silent channel reorder cannot be considered a cosmetic software transform.

---

## 8. Configuration Resolution and Hidden Defaults

ADR-004 requires a resolved canonical configuration containing all defaults that can affect scientific output.

### Software rule

Before execution, material defaults such as:

```text
search grid
peak threshold/prominence
association gate
oracle-K mode
normalization
mean-centering policy
RNG family/stream policy
confidence method
failure mapping
fixed-point rounding/saturation
```

shall be materialized into resolved configuration/provenance.

Changing a library default in a later software version shall not silently reinterpret an old run.

### Gate-D finding

**PASS.** Hidden scientific defaults are explicitly forbidden by the configuration/provenance contract.

---

## 9. Canonical Configuration Identity

ADR-004 requires a versioned canonical semantic representation before hashing.

### Software rule

Semantically equivalent representations may canonicalize together when upstream ADRs permit it, for example:

```text
0.5 m == 50 cm
```

but scientifically distinct states shall remain distinct, for example:

```text
0.5 m != 0.5 wavelength without frequency context
centered covariance != uncentered second moment
far-field profile != near-field profile
calibration artifact A != calibration artifact B
```

Whitespace/key-order changes shall not create scientific differences; scientific-field differences shall not be erased by serializer convenience.

### Gate-D finding

**PASS.** Hashing is tied to semantic configuration rather than arbitrary text serialization.

---

## 10. RNG Ownership and Global-State Prohibition

ADR-004 defines stochastic identity through root seed, RNG family/version, semantic child-stream derivation, condition identity, trial identity, random-family identity, and redraw scope.

### Software rule

Scientific random generation shall not rely on process-global mutable RNG state whose output depends on unrelated call order.

Conceptually valid software behavior is:

```text
trial_id + random_family -> deterministic child RNG stream
```

rather than:

```text
np.random.seed(root)
then trust execution order forever
```

### Gate-D finding

**PASS.** The contract is compatible with parallel/resumable deterministic execution and rejects global call-order semantics.

---

## 11. Parallel Execution Independence

Worker count, batching, scheduler order, and method execution order are operational details unless a declared implementation is numerically nondeterministic.

### Software rule

Changing:

```text
1 worker -> 8 workers
algorithm A before B -> B before A
batch size 100 -> 25
resume from interruption
```

shall not change which scientific random realization belongs to an existing trial identity.

If a numerical backend itself is nondeterministic, that implementation property must be declared rather than hidden inside the trial generator.

### Gate-D finding

**PASS.** Scientific trial identity is independent of scheduling topology.

---

## 12. CRN Software Semantics

CRN sharing is based on semantic latent-randomness identity, not incidental reuse of a NumPy array.

### Software rule

For method comparisons, common exogenous streams are referenced by shared trial/random-family identities. Method-internal randomness uses separate stream roles unless pairing is intentional.

For different geometry dimensions, software shall not force impossible same-shape noise arrays merely to claim CRN; it shall use the declared semantic mapping.

### Gate-D finding

**PASS.** CRN can be implemented without coupling scientific fairness to one array shape or function-call pattern.

---

## 13. Association Is Evaluation-Side Software

ADR-004 establishes:

```text
estimator output
-> execution status
-> association
-> detection/miss/spurious
-> resolution
-> localization metrics
```

### Software rule

An estimator shall not silently use ground-truth association to reorder/select its own outputs unless the algorithm profile explicitly defines oracle behavior.

Evaluation software may associate truth and estimates after output production.

### Gate-D finding

**PASS.** Truth leakage into estimator execution is prevented by the evidence-role separation.

---

## 14. Unequal Cardinality Must Survive APIs

If `K_hat != K`, software shall preserve:

```text
matched pairs
unmatched truth
unmatched estimates
ambiguity/tie diagnostics where relevant
```

### Forbidden behavior

```text
truncate estimate list to K
pad missing outputs with zero-degree estimates
reuse one estimate for multiple truths
silently drop extra peaks
```

unless a specifically declared algorithm/postprocessor contract intentionally does so and that behavior is evaluated as part of the complete pipeline.

### Gate-D finding

**PASS.** The association contract supports lossless unequal-cardinality evidence.

---

## 15. Failure Status versus Numeric Payload

ADR-004 requires typed outcome/failure state separate from numeric output.

### Software rule

The following shall not be treated as equivalent:

```text
NaN
empty estimate list
valid no-detection
algorithm nonconvergence
invalid input
incompatible method/profile
hardware timeout
unresolved scientific state
```

A numeric payload may be absent or NaN, but scientific status must carry the cause/meaning.

### Gate-D finding

**PASS.** `NaN` cannot become a universal failure enum.

---

## 16. Compatibility, Execution Status, and Metric Eligibility

The three-layer model is:

```text
compatibility -> can this method/profile answer the question?
execution status -> what happened in this run/trial?
metric eligibility -> is this outcome in this metric universe?
```

### Software rule

These shall not be collapsed into one boolean such as:

```python
success: bool
```

when that boolean would erase the distinction needed by scientific metrics.

A convenience boolean may exist only as a derived view whose definition is explicit and metric/context specific.

### Gate-D finding

**PASS.** The contract is implementable with typed status layers and forbids semantic boolean collapse.

---

## 17. Denominator Preservation and No Silent Filtering

VP-001 end-to-end `P_D` and `P_res` explicitly include numerical algorithm failure as non-success for otherwise eligible compatible trials.

### Software rule

Metric aggregation shall operate from retained trial statuses and a declared metric-eligibility policy.

Forbidden pattern:

```python
valid = results[~isnan(results)]
metric = mean(valid)
```

when `NaN` removal changes the scientific denominator without a typed eligibility rule.

### Gate-D finding

**PASS.** Silent survivor-only filtering is incompatible with ADR-004.

---

## 18. Localization Metrics and Missing Outputs

Ordinary angular RMSE requires actual declared matched angular errors.

### Software rule

A miss, incompatible trial, or numerical failure shall not be converted automatically into an arbitrary numeric angle penalty such as:

```text
180 deg
90 deg
association gate value
search-sector width
```

unless a separate explicitly defined loss function intentionally uses such a penalty.

Matched-only RMSE must expose its coverage/conditioning.

### Gate-D finding

**PASS.** Missing outputs cannot be silently coerced into localization error values.

---

## 19. Covariance / Second-Moment Object Identity

VP-001 baseline uses:

\[
\hat R^{(2)}=XX^H/L
\]

as the uncentered sample second moment.

ADR-002 defines centered covariance separately.

### Software rule

Software APIs/storage shall preserve which object is represented. A generic field named only `covariance` is insufficient if it can contain either centered covariance or uncentered second moment without metadata/type semantics.

Software shall not silently:

```text
subtract sample mean
switch denominator L <-> L-1
Hermitian-symmetrize
PSD-clip
normalize trace
```

unless the transform is explicitly part of the declared pipeline and provenance.

### Gate-D finding

**PASS.** Matrix-object identity and transforms remain explicit.

---

## 20. Numerical Repair Is a Transformation, Not Validation

ADR-004/ADR-002 reject presenting a repaired matrix/value as evidence that the original input was valid.

### Software rule

Transforms such as:

```text
Hermitian symmetrization
PSD projection
regularization
diagonal loading
whitening
normalization
interpolation
outlier deletion
```

shall produce a derived state/artifact or declared pipeline stage with provenance.

### Gate-D finding

**PASS.** Software repair cannot erase the original diagnostic state.

---

## 21. Sorting / Normalization / Snapping

ADR-001 physical geometry is authoritative in meters and stable channel identity is preserved.

### Software rule

The following may exist as derived views but shall not mutate authoritative geometry silently:

```text
sort by position
center geometry
normalize by wavelength
snap to lattice
reduce primitive lattice
reflect geometry
apply active mask
```

### Gate-D finding

**PASS.** Derived geometry views are separable from source-of-truth geometry.

---

## 22. Cache-Key Scientific Completeness

ADR-004 allows caching only when scientific dependencies are represented in the cache identity or the cache is treated as disposable acceleration.

### Software rule

A cache key for scientific output must not omit material dependencies such as:

```text
resolved scientific configuration
algorithm/implementation version
input/trial identity
calibration artifact
metric/association policy where derived results are cached
```

### Gate-D finding

**PASS.** Stale cache reuse cannot be considered scientifically transparent.

---

## 23. Resume Semantics

A resumed study shall preserve existing trial identities and execute only missing declared work.

### Forbidden behavior

```text
resume -> regenerate prior trial IDs with new random draws
resume -> change algorithm/config while preserving same run identity
resume -> silently discard failed trials and replace until target successful N reached
```

### Gate-D finding

**PASS.** Resume is operational continuation, not scientific resampling/redefinition.

---

## 24. Retry versus Replacement

ADR-004 distinguishes:

```text
retry same trial = same realization + retained failure history
replacement = new trial identity
```

### Software rule

Retry infrastructure may rerun transport/hardware execution against the same canonical stimulus, but shall not sample a new source/noise realization while retaining the old trial identity.

### Gate-D finding

**PASS.** Retry semantics preserve the scientific population.

---

## 25. Oracle Information Must Be Typed

Known `K` in `MUSIC_ORACLE_K` is algorithm information, not merely an implementation convenience.

### Software rule

Resolved method configuration shall identify oracle inputs such as:

```text
true K
true noise covariance
true manifold
true SNR
true calibration parameters
```

where applicable.

Comparison code cannot infer fairness from method names alone; the information contract is part of the method identity.

### Gate-D finding

**PASS.** Oracle-information asymmetry can be represented and audited.

---

## 26. Algorithm versus Implementation Identity

The same scientific method may have implementations such as:

```text
Python float64
Python/NumPy float32
fixed-point software model
HLS C
RTL
FPGA bitstream
```

### Software rule

Algorithm profile and implementation/build identity remain separate fields. Changing implementation without changing algorithm identity is allowed only when the evidence claim is implementation equivalence/cross-validation; it shall not erase the implementation revision.

### Gate-D finding

**PASS.** Scientific method identity does not hide numerical/hardware implementation state.

---

## 27. Fixed-Point Software Semantics

A fixed-point implementation is not identified by a label such as `16-bit`.

### Software rule

Material stage semantics include:

```text
signedness
word length
integer/fractional width
scale / represented physical quantity
rounding/truncation
saturation/wrap
cast locations
accumulator widths
coefficient quantization
operation ordering where relevant
```

A bit-accurate software model must mirror these semantics before bit-exact HLS/RTL claims are made.

### Gate-D finding

**PASS.** Fixed-point software cannot silently differ from hardware arithmetic while claiming bit-accuracy.

---

## 28. Host / FPGA Interface Semantics

Scientific data identity must survive transport through host/DMA/AXI/FPGA boundaries.

### Software/hardware interface provenance includes:

```text
channel order
sample order
frame length
complex packing
endianness
word alignment
scaling
TLAST/frame-boundary semantics
reset/restart state
```

### Gate-D finding

**PASS.** Interface formatting cannot be treated as scientifically irrelevant when it changes sample/channel meaning.

---

## 29. Board Result Identity

Board output shall reference:

```text
canonical input/stimulus identity
host software revision
FPGA bitstream/build identity
board/part/clock profile
fixed-point arithmetic profile
```

### Software rule

A file named `design.bit` or a project folder name is not sufficient build identity.

### Gate-D finding

**PASS.** Board evidence is content/build identified rather than filename identified.

---

## 30. Data / Calibration / External Artifact Identity

ADR-004 requires content identity and lineage for scientific artifacts.

### Software rule

The following are insufficient as sole identities:

```text
C:\data\capture.bin
calibration.csv
cst_export.txt
latest_results.json
```

because files/paths can be replaced.

Artifact metadata/content hash/schema/reference-frame/reference-plane/units/parent lineage are required according to evidence role.

### Gate-D finding

**PASS.** File location is metadata, not scientific identity.

---

## 31. Publication Figure/Table Generation

Figures and tables are derived artifacts.

### Software rule

Scientific-value transformations such as:

```text
condition filtering
normalization
smoothing
interpolation
aggregation
confidence-band calculation
ranking
```

shall be scripted or deterministically recorded.

Manual cosmetic editing may occur outside scientific-value generation; manual value modification requires explicit lineage and creates a new derived artifact.

### Gate-D finding

**PASS.** Publication rendering cannot become an undocumented scientific computation layer.

---

## 32. Immutable Accepted Evidence

Once an artifact is cited by an accepted gate/publication package, it is immutable/versioned.

### Software rule

Regenerating a result after changing:

```text
source code
configuration
trial ensemble
metric policy
calibration
hardware build
```

creates a new evidence identity.

Aliases such as `latest` may point to an immutable artifact but cannot redefine the old content silently.

### Gate-D finding

**PASS.** Mutable filenames/paths cannot overwrite scientific history.

---

## 33. Secrets Are Not Provenance

Credentials, tokens, passwords, and private authentication material are explicitly excluded from scientific configuration/provenance capture.

### Software rule

If an environment variable affects scientific semantics, its nonsecret resolved value belongs in configuration/provenance. Secret values remain outside hashes/logs/publication manifests.

### Gate-D finding

**PASS.** Reproducibility requirements do not create unsafe secret capture semantics.

---

## 34. Response Semantics

ADR-004 inherits the project principle that meaningful invalidity/incompatibility should be typed rather than silently repaired.

At software boundaries, outcomes should support distinctions conceptually equivalent to:

```text
REJECT / INVALID INPUT
INCOMPATIBLE / REQUIRE OTHER PROFILE
DIAGNOSTIC / DEGRADED / UNRESOLVED
VALID RESULT / VALID NO DETECTION
EXECUTION FAILURE
NOT ASSESSED
```

Final software enum names are not frozen by this ADR.

### Gate-D finding

**PASS.** Scientific response semantics are frozen while API naming remains implementation-flexible.

---

## 35. No Premature API Freeze

ADR-004 deliberately does not freeze:

```text
class hierarchy
enum spellings
YAML/JSON package structure
UUID format
specific assignment solver
specific bootstrap library
specific artifact storage technology
```

### Software rule

Implementations may choose these mechanisms provided the scientific invariants above are preserved and testable.

### Gate-D finding

**PASS.** Software architecture remains evolvable without weakening scientific semantics.

---

## 36. Required Phase-1 Software Tests Derived from Gate D

After ADR-004 acceptance and before implementation evidence is promoted, the Phase-1 software test program should include at least:

```text
unit conversion boundary tests
stable channel-order tests
resolved-default/config-hash tests
trial RNG order/worker invariance tests
resume/retry/replacement tests
CRN pairing tests
unequal-cardinality association tests
failure/eligibility/denominator tests
uncentered-second-moment identity tests
no-silent-centering/normalization tests
cache-key dependency tests
artifact hash/lineage tests
oracle-information provenance tests
fixed-point cast/round/saturation tests
host/FPGA packing-order tests where applicable
publication recompute-lineage tests
```

These are implementation obligations derived from the accepted semantic contract; they are not executed by Gate D because authoritative implementation does not yet exist.

---

## 37. Gate-D Boundary Conditions Carried Forward

The following require explicit later implementation tests or Gate-F boundary treatment:

1. duplicate physical channel identifiers;
2. duplicate trial IDs or condition IDs;
3. invalid/noncanonical unit strings;
4. missing required resolved defaults;
5. unknown RNG family/version during replay;
6. configuration hashes generated under different schema versions;
7. cache artifact whose dependency manifest is incomplete;
8. resume after configuration/source change;
9. equal-cost association ties;
10. empty/zero manifold input for normalized metrics;
11. `N=0` metric universe and `N=1` sample-variance boundary;
12. missing/invalid calibration artifact;
13. stale calibration outside validity domain;
14. hardware packing/endianness mismatch;
15. bitstream/source-build mismatch;
16. missing raw artifact referenced by publication manifest;
17. numerical backend nondeterminism under an exact-replay claim.

No Gate-D blocker remains from these boundary conditions; Gate F shall classify required response behavior.

---

## 38. Gate D Checklist

```text
Domain identities preserved                                  PASS
Authoritative vs derived values                              PASS
Unit conversion at validated boundaries                      PASS
Stable channel identity / explicit permutations              PASS
Resolved scientific defaults                                 PASS
Canonical semantic configuration hashing                     PASS
No process-global scientific RNG dependence                  PASS
Worker/order-independent trial identity                      PASS
CRN semantic pairing                                         PASS
Evaluation-side truth association                            PASS
Unequal-cardinality evidence preservation                    PASS
Typed failure separate from numeric payload                  PASS
Compatibility / execution / eligibility separation           PASS
No silent denominator filtering                              PASS
No arbitrary RMSE penalty for missing outputs                PASS
Covariance/second-moment object identity                     PASS
No silent centering/symmetrization/PSD repair                PASS
No silent physical geometry sorting/normalization/snapping   PASS
Scientific cache dependency completeness                     PASS
Resume/retry/replacement semantics                           PASS
Oracle-information provenance                                PASS
Algorithm vs implementation identity                         PASS
Fixed-point arithmetic semantics                             PASS
Host/FPGA transport semantics                                PASS
Build/artifact content identity                              PASS
Publication scripted lineage / immutable evidence            PASS
Secrets excluded from provenance                             PASS
API flexibility without scientific semantic drift            PASS
Blocking software-semantic contradiction                     NONE
```

---

## 39. Gate D Decision

### **Gate D — Software Semantic Consistency: PASS**

ADR-004 defines a software-semantic contract strong enough to prevent the main classes of silent scientific drift during later implementation.

The contract requires typed scientific identities, explicit resolved configuration, deterministic semantic RNG streams, stable channel/trial identity, lossless failure and unequal-cardinality evidence, metric-specific denominator policies, explicit matrix-object semantics, provenance-preserving transformations, immutable artifacts, and separate algorithm/implementation/hardware identities.

No governing-draft correction was required for Gate D.

The future software implementation remains unaccepted until it is built and tested against these obligations after ADR-004 acceptance.

---

## 40. Status after Gate D

```text
Pre-Gate consistency review                PASS
Gate A — Physical Consistency              PASS
Gate B — Mathematical Consistency          PASS
Gate C — Dimensional / Unit Consistency     PASS
Gate D — Software Semantic Consistency      PASS
Gate E — Hand Reference Evidence            NEXT
Gate F — Boundary / Failure Analysis         NOT STARTED
ADR-004 acceptance                          NOT ACCEPTED
Authoritative Phase-1 implementation        NOT YET AUTHORIZED
```

The next work item is:

```text
ADR-004 Gate E — Golden Reference / Hand Reference Evidence
```

Gate E shall create and formally verify GRP-018 and any required deterministic supplemental reference checks without using exploratory calculations alone as accepted evidence.
