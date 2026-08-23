# ADR-004 — Pre-Gate Consistency Review

- **ADR:** ADR-004 — Validation, Reproducibility, and Scientific Evidence
- **Phase:** 0C — Scientific Foundations
- **Review status:** **PASS**
- **Governing draft reviewed:** `ADR-004-validation-reproducibility-scientific-evidence.md`
- **Reviewed draft content SHA:** `8cca2e3ac514cd031bee1d8c9e4c0347694ecb53`
- **Reviewed correction commit:** `4675f312214ebc0eaaa64a2041bb582931cf2332`
- **Initial governing-draft commit:** `54d87708297883d153990ad11b7c85ac4dc9761b`
- **Cross-section reconciliation:** `ADR-004_EXPLORATION_4.20_CROSS_SECTION_RECONCILIATION.md`
- **Roadmap:** `../PHASE0C_SCIENTIFIC_CONTRACTS_ROADMAP.md`
- **Upstream accepted ADRs:** ADR-001, ADR-002, ADR-003
- **Acceptance gates:** NOT STARTED by this review

> This review determines whether the reconciled governing ADR-004 draft is internally and cross-ADR consistent enough to begin Gate A. It does **not** accept ADR-004 and does not count as any Gate A–F PASS.

---

## 1. Review Objective

The pre-Gate review answers:

> Does the governing ADR-004 draft faithfully represent the reconciled Exploration 4.20 decision families F1–F14, preserve accepted ADR-001/002/003 authority, cover the ADR-004 roadmap requirements, and eliminate terminology/denominator/failure/profile ambiguities before formal Gate A begins?

The review was intentionally performed before any acceptance gate so that drafting omissions could be corrected without contaminating Gate evidence.

---

## 2. Inputs Reviewed

The review used the following authoritative inputs:

```text
ADR-004 governing draft
ADR-004 Exploration 4.20 cross-section reconciliation
ADR-004 Exploration checkpoint
Phase 0C Scientific Contracts Roadmap
Accepted ADR-001
Accepted ADR-002
Accepted ADR-003
ADR-004 Explorations 4.1–4.19 as supporting rationale
```

The accepted upstream ADR roles remain:

```text
ADR-001 -> geometry / coordinate / direction / receive phase / phase reference / channel identity
ADR-002 -> propagation / snapshots / source-noise / covariance / rank / SNR / MIMO provenance
ADR-003 -> sensor imperfections / calibration / compatibility / identifiability / ADC / measured-EM manifolds
ADR-004 -> scientific evidence semantics
```

---

## 3. Initial Review Findings and Corrections

The initial governing draft was structurally sound but the pre-Gate audit identified four omissions that were small in scope yet blocking for a clean PASS because they were explicitly required by Exploration 4.20 or the roadmap.

### PG-004-01 — Event-probability denominator not sufficiently explicit

**Initial issue:** the draft stated VP-001 numerical-failure mapping for `P_D` and `P_res`, but did not define their baseline eligible universes/denominators as explicitly as Exploration 4.20 required.

**Correction:** Section F6 now defines:

\[
\widehat P_{res}
=\frac{N_{resolved}}{N_{eligible,compatible}}
\]

for the VP-001 baseline end-to-end resolution universe and defines source-level `P_D` using eligible truth-source opportunities in compatible trials. It explicitly states how valid misses, numerical failures, invalid/outside-profile states, and incompatibility affect or do not affect the ordinary denominator.

**Status:** RESOLVED.

### PG-004-02 — Population variance semantics omitted from compact draft

**Initial issue:** bias/MSE/RMSE and finite empirical variance were present, but population variance was not explicitly written despite variance being a roadmap requirement and an Exploration 4.7 contract.

**Correction:** F6 now defines, for fixed truth,

\[
\operatorname{Var}(\hat q)
=E[(\hat q-E\hat q)^2]
=E[(e-Ee)^2]
\]

and explicitly states

\[
\operatorname{MSE}
=\operatorname{Var}(\hat q)+\operatorname{Bias}^2.
\]

Random-truth averaging/conditioning is also required to be declared.

**Status:** RESOLVED.

### PG-004-03 — Source count / rank / model-order distinctions needed explicit preservation

**Initial issue:** the draft preserved trial-versus-snapshot semantics but did not explicitly enumerate all rank/cardinality distinctions from ADR-002 and Exploration 4.20.

**Correction:** F4 now explicitly distinguishes:

```text
snapshot count L
Monte Carlo trial count N
physical/source count K
source-covariance rank
observed signal-subspace rank
estimator model order
estimated-output cardinality K_hat
matched-pair/source-opportunity count
condition count
```

**Status:** RESOLVED.

### PG-004-04 — External-tool / independent numerical evidence role needed explicit wording

**Initial issue:** the roadmap requires numerical cross-reference and external-tool validation evidence, while the compact draft could have been read as treating only hand references and production software comparison explicitly.

**Correction:** F3 now explicitly includes independent numerical/cross-tool reference evidence and states that CST/external-tool agreement is verification/model-reference evidence unless a separate physical-validation contract supplies traceable physical evidence.

**Status:** RESOLVED.

### Correction provenance

All four corrections were incorporated in:

```text
4675f312214ebc0eaaa64a2041bb582931cf2332
```

No new scientific scope or universal threshold was introduced by these corrections; they make previously reconciled semantics explicit in the governing draft.

---

## 4. F1–F14 Coverage Audit

| Family | Governing content | Result |
|---|---|---|
| F1 | Verification / physical validation / calibration / reproducibility / comparison / implementation cross-validation separation | PASS |
| F2 | Typed truth/reference authority, provenance, uncertainty, oracle-information boundary | PASS |
| F3 | Deterministic GRP/reference ladder, independent numerical/cross-tool evidence, regression limits | PASS |
| F4 | Study/condition/trial/snapshot hierarchy, random declaration, RNG child streams, CRN | PASS |
| F5 | Unordered multi-source association, miss/spurious, formal false-alarm distinction, resolution event | PASS |
| F6 | Bias, variance, MSE, RMSE, empirical decomposition, denominators, event-probability universes | PASS |
| F7 | Monte Carlo adequacy, dependence/hierarchy, uncertainty, stopping, Wilson scope | PASS |
| F8 | Fair algorithm/geometry comparison, tuning leakage, resource controls, effect/margin semantics | PASS |
| F9 | Compatibility vs execution vs metric eligibility; typed failures/retries | PASS |
| F10 | Manifold/covariance/eigenspace/spectrum/DOA diagnostics and causal-attribution boundary | PASS |
| F11 | Float/fixed/bit-accurate/HLS/RTL/FPGA/physical-validation ladder and hardware metrics | PASS |
| F12 | Canonical config, Git/software/data/calibration/external-tool/hardware-build provenance | PASS |
| F13 | Claim-traceable immutable publication/reproducibility package | PASS |
| F14 | VP-001 bounded initial validation profile | PASS |

**Result:** all reconciled decision families F1–F14 are represented without blocking omission.

---

## 5. ADR-004 Roadmap Coverage Audit

The Phase 0C roadmap requires ADR-004 to cover all of the following. The governing draft contains each topic at the appropriate normative level:

| Roadmap requirement | Governing location / treatment | Result |
|---|---|---|
| Ground-truth definition/provenance | F2 | PASS |
| Verification vs physical validation | F1 | PASS |
| Analytical reference validation | F3 | PASS |
| Numerical cross-reference validation | F3 | PASS |
| External-tool evidence | F2/F3/F12 | PASS |
| Hardware/experimental validation | F1/F11/F14 | PASS |
| Golden Reference Problems | F3 / GRP-018 reservation | PASS |
| Random-variable declaration | F4 | PASS |
| Monte Carlo trial semantics | F4 | PASS |
| Root seed / child streams | F4 | PASS |
| Common random numbers | F4/F8 | PASS |
| Trial-count adequacy / convergence diagnostics | F7 | PASS |
| Bias | F6 | PASS |
| Variance | F6 | PASS |
| MSE/RMSE | F6 | PASS |
| Multi-source association | F5 | PASS |
| Missed/false/spurious detection semantics | F5/F6 | PASS |
| Resolution vs accuracy | F5/F6 | PASS |
| Probability of resolution | F6/F9/F14 | PASS |
| Failure-state recording | F9 | PASS |
| Spectrum diagnostics | F10 | PASS |
| Manifold/covariance/eigen/eigenspace/DOA metrics | F10 | PASS |
| Uncertainty/confidence intervals | F7 | PASS |
| Fair benchmark requirements | F8 | PASS |
| Data/config/calibration/algorithm/software/Git/seed provenance | F12 | PASS |
| Scientific vs computational/hardware metrics | F10/F11 | PASS |
| Float/fixed/FPGA cross-validation | F11 | PASS |

**Roadmap coverage result:** PASS.

---

## 6. Cross-ADR Authority Audit

### 6.1 ADR-001

The draft inherits rather than redefines:

```text
1-D geometry semantics
canonical theta/direction convention
receive steering sign
phase-reference semantics
physical positions in meters
stable channel identity
```

Gauge-aware evidence transforms do not move the physical phase reference or authorize silent geometry normalization/reindexing.

**Result:** PASS.

### 6.2 ADR-002

The draft preserves:

```text
snapshot semantics
source/noise/SNR authority
uncentered second moment vs centered covariance distinction
source count vs source-covariance rank vs observed subspace rank
far-field and narrowband profile authority
MIMO physical-channel provenance
```

VP-001 uses `XX^H/L` explicitly as the uncentered sample second moment under the declared zero-mean baseline.

**Result:** PASS.

### 6.3 ADR-003

The draft preserves:

```text
sensor operator/profile authority
calibration != validation
compatibility != identifiability
ADC quantization != FPGA fixed point
measured/CST artifact != automatic truth
Phase-1 ideal H_sensor = I
```

Synthetic FPGA replay remains implementation/integration evidence rather than physical sensor validation.

**Result:** PASS.

### Cross-ADR result

No blocking redefinition, sign conflict, reference-plane conflict, or authority collision was identified after the correction commit.

---

## 7. Mandatory Terminology Audit

| Term / distinction | Required meaning | Result |
|---|---|---|
| truth vs reference | epistemic role explicit | PASS |
| calibration vs validation | distinct evidence roles | PASS |
| trial vs snapshot | separate hierarchy levels | PASS |
| `K` vs ranks/model order/`K_hat` | distinct structural quantities | PASS |
| uncentered second moment vs centered covariance | explicitly distinct | PASS |
| `v_N` vs `s^2` | divisor-N decomposition vs divisor-(N-1) estimator | PASS |
| spurious estimate vs formal false alarm | distinct event semantics | PASS |
| resolution vs beamwidth/grid spacing | distinct | PASS |
| compatibility vs execution failure vs metric eligibility | three authoritative layers | PASS |
| physical delay vs sampling offset vs hardware latency | no ADR-004 redefinition/collapse | PASS |
| board implementation evidence vs physical validation | distinct | PASS |
| reproducibility vs correctness | distinct | PASS |

**Terminology result:** PASS.

---

## 8. Metric-Universe and Failure-Mapping Audit

### 8.1 Localization RMSE

- computed on its declared associated/matched universe;
- no arbitrary angular penalty for numerical/incompatibility failures;
- matched-only RMSE requires coverage/miss/failure evidence.

**Result:** PASS.

### 8.2 End-to-end `P_res`

VP-001 baseline denominator is explicitly method-compatible, scientifically eligible trials.

```text
resolved valid trial                 -> R=1
valid miss/unresolved resolution     -> R=0
numerical/algorithm failure          -> R=0 + typed failure preserved
invalid/outside-profile              -> excluded + separately accounted
method incompatible                  -> separately reported, not ordinary P_res trial
```

**Result:** PASS.

### 8.3 End-to-end source-level `P_D`

VP-001 denominator is eligible truth-source opportunities in compatible trials.

```text
admissibly matched truth source      -> detected
valid unmatched truth source         -> missed
numerical/algorithm failure          -> affected eligible truth opportunities are non-detections + failure preserved
invalid/outside-profile              -> excluded + separately accounted
```

**Result:** PASS.

### 8.4 Conditional variants

Conditional valid-output probability metrics require distinct metric identities and explicit conditioning/coverage/failure reporting.

**Result:** PASS.

---

## 9. Monte Carlo / Uncertainty Audit

The draft correctly preserves:

- no universal trial count;
- condition/metric-specific adequacy;
- tail/failure/dependence awareness;
- fixed-`N` preference for initial confirmatory VP-001 studies without setting a universal numeric `N`;
- Wilson only as VP-001 default for ordinary IID fixed-`N` Bernoulli event reporting;
- no universal RMSE CI formula;
- paired comparison uncertainty for paired designs;
- hierarchical dependence requiring compatible methods.

No outcome-driven universal stopping rule was accidentally promoted.

**Result:** PASS.

---

## 10. Fair-Comparison Audit

The governing draft requires the comparison contract to preserve/decorate:

```text
task/domain
truth/reference
source/noise/SNR/L semantics
sensor/calibration profile
oracle information
tuning data/budget
pre/postprocessing
association/metric/failure policy
CRN/pairing
geometry resources
comparison uncertainty
runtime scope
```

Geometry superiority is explicitly resource-conditional; tuning leakage invalidates confirmatory interpretation; lack of statistical significance is not equivalence.

**Result:** PASS.

---

## 11. Hardware / FPGA Boundary Audit

The draft preserves the evidence ladder:

```text
scientific contract
-> verified float64
-> float32 where used
-> fixed-point model
-> bit-accurate model
-> HLS/RTL
-> synthesis/place-route/timing
-> FPGA board replay
-> physical sensor/system validation
```

It distinguishes bit-exactness from bounded numerical equivalence and latency from II/throughput/timing/resource metrics.

Synthetic/frozen board replay is not physical sensor validation.

**Result:** PASS.

---

## 12. Provenance / Publication Audit

The draft preserves distinct identities for study, condition, trial ensemble, algorithm, implementation, run, data/calibration/external artifact, derived result, and hardware build.

It requires canonical resolved configuration, Git commit provenance, RNG derivation semantics, artifact lineage, environment/build identity, immutable evidence, and claim-to-package traceability.

A hash supports identity but does not replace human-readable semantic meaning. A figure/table is derived evidence, not the sole scientific source. Corrections create new evidence identities rather than overwrite cited evidence.

**Result:** PASS.

---

## 13. VP-001 Scope Audit

The governing draft correctly limits VP-001 to the deliberate Phase-1 baseline:

```text
1-D receive array
ADR-001 canonical steering/reference semantics
ADR-002 PM-001 far-field narrowband profile
K=1 / K=2 primary cases
proper-complex zero-mean stationary source baseline
white equal-variance additive noise
ADR-003 ideal Phase-1 sensor, H_sensor = I
L snapshots inside each Monte Carlo trial
uncentered sample second moment XX^H/L
Bartlett / MVDR / MUSIC candidate baselines
oracle-K only when explicitly labeled
explicit search/peak/association configuration
fixed-N confirmatory preference + achieved uncertainty
Wilson default only for ordinary IID fixed-N Bernoulli P_D/P_res
float -> fixed/HLS/RTL/FPGA implementation path
```

Near field, wideband, coupling, sensor mismatch, colored noise, ADC effects, measured/CST manifold substitution, unknown-K benchmarking, TDM-MIMO temporal phase, and physical acquisition remain outside plain VP-001.

**Result:** PASS.

---

## 14. Implementation-Detail Promotion Audit

The governing draft does not freeze nonessential implementation details such as:

```text
Python class names
software enum spellings
serialization library
Hungarian solver package
bootstrap library
HLS automation package
artifact archive/DOI provider
UUID/run-id format
```

The Phase-1 SHA-256 configuration/artifact fingerprint baseline and VP-001 Wilson reporting default are retained because Exploration 4.20 explicitly reconciled them as bounded profile-level choices rather than universal scientific constants.

**Result:** PASS.

---

## 15. Pre-Gate Checklist Result

```text
F1–F14 represented                                      PASS
ADR-001/002/003 authority preserved                     PASS
Roadmap ADR-004 topics covered                          PASS
Truth/reference/calibration terminology                 PASS
Snapshot/trial/source-count/rank terminology            PASS
Uncentered second moment vs centered covariance         PASS
v_N vs s^2                                               PASS
Association/detection/resolution ordering               PASS
P_D/P_res denominator + failure mapping                 PASS
Compatibility/failure/metric eligibility                PASS
Metric vs acceptance threshold                          PASS
VP-001 fixed-N/Wilson scope                              PASS
Hardware implementation vs physical validation          PASS
Provenance/publication immutability                      PASS
No blocking implementation detail accidentally frozen   PASS
Blocking contradiction                                  NONE
```

---

## 16. Final Review Decision

### Pre-Gate Consistency Review: **PASS**

The corrected governing ADR-004 draft is internally coherent at the pre-Gate level, covers the Phase 0C ADR-004 roadmap, preserves upstream ADR authority, and faithfully represents the reconciled Exploration 4.20 decision families.

No blocking open drafting issue remains before Gate A.

This decision means:

```text
Governing draft exists                  YES
Pre-Gate consistency review             PASS
Gate A may begin next                   YES
Gate A itself                           NOT STARTED
Gates B–F                               NOT STARTED
GRP-018 formal Gate-E evidence          NOT STARTED
ADR-004 accepted                        NO
Authoritative Phase-1 implementation    NOT YET AUTHORIZED
```

The next work item is:

```text
ADR-004 Gate A — Physical Consistency Audit
```

Gate A shall evaluate whether the governing evidence semantics and VP-001 profile correctly distinguish physical/model assumptions, truth/reference roles, physical validation boundaries, and hardware/software evidence claims without contradicting ADR-001/002/003.
