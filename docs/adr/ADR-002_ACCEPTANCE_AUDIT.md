# ADR-002 — Acceptance Audit

- **ADR:** `ADR-002-wave-propagation-signal-measurement-model.md`
- **Phase:** 0C — Scientific Foundations
- **Audit status:** Complete — Gates A–F passed in design; final repository reconciliation pending
- **Purpose:** Preserve the explicit physical, mathematical, dimensional, software-semantic, analytical-reference, and boundary evidence supporting ADR-002 acceptance.

## Gate Status Summary

| Gate | Requirement | Status |
|---|---|---|
| A | Physical consistency | PASS |
| B | Mathematical consistency | PASS |
| C | Dimensional and unit consistency | PASS |
| D | Software semantic consistency | PASS |
| E | Hand-calculated reference evidence | PASS |
| F | Boundary and failure analysis | PASS — see dedicated boundary artifact |

---

## Gate A — Physical Consistency

### A.1 Audit question

Does ADR-002 represent wave propagation, delay, bandwidth, medium, motion, active/passive sensing, FMCW, MIMO, snapshot, covariance, source/noise, and model-order concepts as physically distinct quantities with explicit domains of validity?

### A.2 Findings that pass

1. **Temporal phasor and outgoing propagation — PASS.** `exp(-j omega t)` is consistent with an outgoing scalar field `exp(+j k R) exp(-j omega t)`.
2. **Look versus propagation direction — PASS.** ADR-001 look direction points array-to-source while incident propagation is its negative.
3. **Exact path geometry — PASS.** `R_n = ||r_s-r_n||` is physically meaningful independently of later approximations.
4. **Expansion validity — PASS after clarification.** The spherical-to-plane-wave expansion is explicitly asymptotic in aperture/range ratio rather than universally exact.
5. **Far-field semantics — PASS after clarification.** Far-field compatibility is a relation among scene, direction, frequency, and required accuracy, not an intrinsic Boolean property of an array/source.
6. **Reference-relative curvature — PASS.** The primary path residual compares exact relative spherical paths against the declared plane-wave model.
7. **Fraunhofer interpretation — PASS.** `2D^2/lambda` is treated as a diagnostic scale, not a universal binary boundary.
8. **Near-field amplitude — PASS after clarification.** `R_ref/R_n exp[jk(R_n-R_ref)]` is identified as an ideal 3-D scalar spherical-spreading specialization, not a universal near-field law.
9. **Lossless versus geometric spreading — PASS.** Zero medium absorption does not imply constant field amplitude with range.
10. **Phase versus group velocity — PASS.** They coincide in PM-001 but remain separate in general dispersive media.
11. **Narrowband compatibility — PASS after clarification.** The general aperture delay is built from path/group delays; `D_u/v` is the far-field nondispersive specialization.
12. **Narrowband is scene/direction-specific — PASS.** It is not a waveform-only Boolean.
13. **Static pure-delay baseband relation — PASS after wording correction.** Its exactness is limited to the declared scalar pure-delay model.
14. **Motion/Doppler — PASS after domain labeling.** `f_D = -f_c dot(tau)` is a slowly varying/narrowband path approximation.
15. **Quasi-static versus zero velocity — PASS.** Nonzero Doppler does not automatically invalidate a constant spatial manifold.
16. **Active multi-leg path — PASS after clarification.** Generic active sensing uses Tx-target and target-Rx legs; monostatic `2R` is a specialization.
17. **Moving active target — PASS after clarification.** A common-epoch two-leg path is recognized as stop-and-hop/quasi-static rather than universally exact.
18. **FMCW stationary model — PASS.** The derived beat relation is explicitly limited to the stated chirp/dechirp/static-delay model.
19. **Measurement/snapshot semantics — PASS.** Simultaneous-equivalent refers to a common receiver observation state, not identical source emission time.
20. **MIMO bistatic physics — PASS after material correction.** General bistatic Tx and Rx legs use separate look directions; virtual-sum geometry is only a common-look/colocated far-field specialization.
21. **Source/path/arrival semantics — PASS.** Multiple arrivals may arise from one physical source, including coherent multipath.
22. **Noise versus medium loss — PASS.** A lossless propagation medium may coexist with receiver/background measurement noise.
23. **Ideal scalar PM-001 channels — PASS after definition tightening.** PM-001 excludes direction-dependent element response, polarization effects, coupling, and relative channel mismatch from its ideal reference channel model.

### A.3 Resolved refinements

The physical audit produced the following governing refinements, all incorporated into ADR-002:

- A-R1 — far-field compatibility is scene/direction/frequency specific;
- A-R2 — ideal `R_ref/R_n` spherical amplitude is only a declared specialization;
- A-R3 — general relative amplitude/response diagnostics are path-response based;
- A-R4 — the pure-delay baseband relation is exact only under its declared channel model;
- A-R5 — narrowband delay is generally defined from actual/group delays;
- A-R6 — Doppler relations carry an explicit slow-motion/narrowband domain;
- A-R7 — moving active path uses stop-and-hop only as an explicit approximation;
- A-R8 — general bistatic MIMO keeps independent Tx/Rx look directions;
- A-R9 — `r_Tx+r_Rx` virtual geometry is common-look/colocated specialization only;
- A-R10 — ideal scalar channel semantics are explicit;
- A-R11 — simultaneous snapshot semantics refer to receiver-observation simultaneity/equivalence.

### A.4 Gate A decision

**Gate A status: PASS.**

No unresolved physical contradiction remains within ADR-002's declared scope.

---

## Gate B — Mathematical Consistency

### B.1 Audit question

Are Fourier/delay signs, spherical expansions, relative-path equations, narrowband bounds, group-delay relations, Doppler/FMCW algebra, bistatic MIMO equations, covariance identities, rank statements, and MUSIC subspace relations mathematically self-consistent?

### B.2 Findings that pass

1. **Fourier delay theorem — PASS.** Under `X(omega)=integral x(t) exp(+j omega t) dt`, delay contributes `exp(+j omega tau)`.
2. **Spherical distance Taylor expansion — PASS.** The retained second-order term is the squared transverse aperture offset divided by `2R`.
3. **Relative second-order distance — PASS.** Reference subtraction produces the difference `q_n-q_ref` rather than absolute `q_n` alone.
4. **Far-field error metric — PASS after refinement.** A reference-specific residual and a pairwise common-phase/reference-invariant residual are distinguished.
5. **ULA specialization — PASS.** `R_n approximately R-x_n sin(theta)+x_n^2 cos^2(theta)/(2R)` follows from the vector expansion.
6. **Delay-to-steering chain — PASS.** Substitution recovers the accepted ADR-001 steering exponent exactly.
7. **Narrowband approximation bound — PASS.** `|exp(j phi)-1| <= |phi|` in the relevant first-order bound supports `2 pi nu_max Delta tau_ap` as the phase-excursion metric.
8. **Fractional-bandwidth identity — PASS.** `B Delta tau_ap = (B/f_c)(D_u/lambda_c)` in the far-field nondispersive specialization.
9. **Group delay/velocity — PASS.** Units/signs and nondispersive limit are consistent.
10. **Complex wavenumber — PASS.** `beta+j alpha` yields `exp(-alpha R) exp(j beta R)` under the adopted temporal convention.
11. **Relative response denominator — PASS after boundary addition.** `H_n/H_ref` requires nonzero reference response.
12. **Doppler derivation — PASS.** `f_D=-f_c dot(tau)` follows directly from the carrier phase under the scientific frequency convention.
13. **FMCW algebra — PASS.** For `y=s_rx conj(s_tx)`, up-chirp/static delay produces scientific signed beat `-mu tau`; the standard forward FFT coordinate has the opposite sign mapping for the resulting exponential.
14. **Stationary monostatic range formula — PASS.** `R=v|f_b|/(2|mu|)` follows from `tau=2R/v`.
15. **General bistatic derivation — PASS.** First-order two-leg path retains independent Tx/Rx projections.
16. **Virtual-sum specialization — PASS.** It follows algebraically only when Tx and Rx look directions are common/equivalent.
17. **Snapshot matrix dimensions — PASS.** `A(NxQ) S(QxL)` yields `X(NxL)`.
18. **Population covariance expansion — PASS.** Cross terms vanish only under declared signal/noise uncorrelated assumptions.
19. **Hermitian PSD covariance — PASS.** Covariance is Hermitian positive semidefinite by quadratic-form construction.
20. **Known-zero-mean sample second moment — PASS.** `1/L XX^H` is unbiased for a common zero-mean second moment without requiring sample independence for expectation, although dependence affects estimator variance.
21. **Centered `1/(L-1)` covariance — PASS after statistical clarification.** Calling it unbiased requires the relevant iid/common covariance assumptions; the denominator alone is insufficient for correlated snapshots.
22. **`L=1` boundary — PASS.** Known-zero second moment exists; estimated-mean `1/(L-1)` covariance does not.
23. **Centered rank ceiling — PASS.** The centering matrix has rank `L-1`, giving `rank(R_hat)<=min(N,L-1)`.
24. **Signal covariance rank — PASS.** `rank(A R_s A^H)<=min(rank(A),rank(R_s))`.
25. **Coherent-source rank collapse — PASS.** Perfect proportionality produces rank-one `R_s` despite multiple arrivals.
26. **Partial-correlation eigenvalues — PASS.** Equal-power two-source covariance eigenvalues are `P(1+|rho|)` and `P(1-|rho|)`.
27. **MUSIC subspace relation — PASS.** `span(A)` equals the population signal subspace only under the required full-rank source covariance/manifold assumptions.
28. **White-noise eigenstructure — PASS.** Population noise-subspace eigenvalues equal `sigma^2`; finite-sample eigenvalues need not.
29. **Complex Gaussian scaling — PASS.** Real/imaginary component variances are half the declared complex variance.
30. **Beamforming SNR example — PASS.** A matched normalized weight yields ideal array gain `N` in white noise.
31. **Generic projective distance — deferred deliberately.** No undefined `d_proj` is made normative; exact equivalence semantics must be declared before adoption.
32. **Model-order/rank semantics — PASS.** Observable rank, physical source count, and peak count are mathematically independent quantities.
33. **Sample-rank feasibility — PASS.** `L-1>=r` is only a necessary centered rank-feasibility condition.

### B.3 Resolved refinements

- B-R1 — include a reference-invariant pairwise plane-wave compatibility metric;
- B-R2 — identify reference-relative plane-wave error as reference dependent;
- B-R3 — relative response division requires `H_ref != 0`;
- B-R4 — `1/(L-1)` unbiasedness requires statistical assumptions;
- B-R5 — estimated-mean covariance requires `L>=2`;
- B-R6 — `L-1>=r` is necessary, not sufficient, for adequate estimation;
- B-R7 — generic `d_proj` remains deferred until precisely defined;
- B-R8 — general bistatic MIMO uses independent Tx/Rx look directions;
- B-R9 — exact/group-delay aperture spread is canonical; `D_u/v` is a specialization.

### B.4 Gate B decision

**Gate B status: PASS.**

No unresolved mathematical/sign/rank contradiction remains.

---

## Gate C — Dimensional and Unit Consistency

### C.1 Audit question

Are physical, angular, spectral, propagation, FMCW, amplitude, covariance, SNR, and index quantities dimensionally and semantically explicit?

### C.2 Canonical inventory — PASS

ADR-002 now declares canonical internal semantics including:

```text
m       position/range/aperture
s       time/delay
Hz      frequency/bandwidth/Doppler
rad/s   angular frequency
rad     phase/angle
m/s     propagation speed
rad/m   phase constant/wavenumber
Hz/s    chirp slope
Np/m or typed inverse length  attenuation
```

Direction cosines, correlation coefficients, and normalized ratios are dimensionless.

### C.3 Findings that pass

- `omega t`, `kR`, and `beta R` are phase/radian arguments of complex exponentials;
- `lambda=v/f` gives meters;
- `tau=R/v` gives seconds;
- `d beta/d omega` gives seconds per meter and its inverse gives meters per second;
- dispersion coefficients have the required higher-order time/length dimensions;
- `mu=B/T_c` has `Hz/s` and `mu tau` has `Hz`;
- `f_D=-dot(P)/lambda` has `Hz`;
- aperture delay is seconds and `B Delta tau` is dimensionless;
- plane-wave phase-error metrics carry semantic radians;
- absolute path-response units depend on response normalization and are not universally dimensionless;
- same-unit relative path-response ratios are dimensionless when defined;
- geometry-only steering coefficients are dimensionless complex values;
- snapshot units are declared by the measurement representation;
- covariance and covariance eigenvalues carry measurement-unit squared semantics;
- source amplitude, source power, noise standard deviation, and noise variance remain distinct;
- SNR is a dimensionless ratio, optionally represented logarithmically;
- RCS (`m^2`) is not a generic complex reflectivity coefficient;
- FFT/sample/channel indices are dimensionless integers and are not physical coordinates;
- normalized geometry/time/frequency are derived context-bearing quantities rather than authoritative physical state.

### C.4 Resolved refinements

The Gate C audit produced C-R1 through C-R15, all incorporated conceptually into the governing ADR: explicit canonical units; typed distinction of Hz/rad/s and beta/alpha; response-unit semantics; measurement/covariance units; amplitude versus variance; quantity-aware dB; RCS/reflectivity separation; index/coordinate separation; unit-aware tolerances; and canonical SI-compatible kernel boundaries.

### C.5 Gate C decision

**Gate C status: PASS.**

No unresolved dimensional inconsistency remains.

---

## Gate D — Software Semantic Consistency

### D.1 Audit question

Can the ADR-002 scientific distinctions map into the GeoDOA domain/layered architecture without silent model switching, unit inference, axis guessing, identity loss, destructive normalization, or premature class inflation?

### D.2 Findings that pass

1. Physical model profile, statistical configuration, and algorithm configuration are separate layers.
2. PM-001 is a compositional/versioned scientific profile, not a bag of independent Boolean flags.
3. Primitive authoritative quantities are stored once; wavelength/wavenumber and similar quantities are derived.
4. Medium semantics are behavioral rather than merely `speed = 3e8`.
5. Absolute path response, relative path response, and geometry-only manifold remain distinct.
6. Phase-reference/manifold construction need not divide by an absolute reference response.
7. Coordinate origin, propagation expansion origin, and spatial phase reference stay semantically distinct.
8. Far-field, narrowband, and quasi-static are compatibility/model relations, not intrinsic object properties.
9. Compatibility metrics are distinct from acceptance policies/thresholds.
10. Scientific frequency and software FFT-coordinate transformations are explicit.
11. `fftshift` cannot silently become a physical sign conversion.
12. FMCW mixer convention and signed chirp slope are provenance-bearing inputs.
13. Raw measurement tensors have explicit axis semantics; shape alone is insufficient.
14. Derived range/Doppler/snapshot views retain transformation provenance.
15. Spatial snapshots are semantic/provenance-bearing views, not anonymous matrices at public boundaries.
16. Persistent channel identity is distinct from row ordering.
17. Physical and virtual MIMO channels are distinct; virtual channels retain `(Tx,Rx)` lineage.
18. Virtual coordinate creation is allowed only under its common-look compatibility condition.
19. Source, target/scatterer, path, and arrival semantics are separate.
20. Physical source count, arrival count, covariance rank, estimated order, and peak count remain distinct.
21. Population covariance, sample covariance, and uncentered second moment remain distinguishable.
22. Covariance construction records snapshot count, mean handling, normalization, and source snapshot set.
23. `unbiased=True` is not inferred merely from denominator selection.
24. Validation and numerical repair are separate; Hermitian/PSD corrections are never silent.
25. Noise variance semantics are explicit and not hidden in a generic `sigma`.
26. Calibrated/full manifolds are never silently normalized.
27. Generic projective manifold distance remains deferred until its equivalence class is explicit.
28. Intrinsic geometry is not mutated by platform motion; pose/embedding provides time-varying global positions.
29. Generic active-radar `delay *= 2` is forbidden.
30. Silent model promotion/degradation after compatibility failure is forbidden.
31. Canonical units are converted at validated boundaries, not guessed by kernels.
32. Scientific profile identity/revision is required in reproducible run provenance.
33. Pure numerical kernels remain compatible with these requirements; rich semantics at boundaries do not force class-heavy numerical code.

### D.3 Gate D decision

**Gate D status: PASS.**

ADR-002 maps cleanly to the project's domain-centric architecture while preserving the existing principle: semantic separability without premature class proliferation.

---

## Gate E — Hand-Calculated Reference Evidence

### E.1 Audit question

Do deterministic hand-solvable references exercise the material ADR-002 contracts strongly enough to become future regression-test oracles?

### E.2 Evidence artifact

```text
docs/science/golden_reference/ADR-002_GOLDEN_REFERENCE_PROBLEMS.md
```

contains canonical GRP-007 through GRP-013 plus supplemental source-reference cases `ADR-002-SRC-01` through `ADR-002-SRC-05`.

### E.3 Coverage

- GRP-007 — exact spherical versus plane-wave curvature/Fraunhofer interpretation;
- GRP-008 — aperture delay and narrowband bandwidth-delay metric;
- GRP-009 — FMCW dechirp sign, FFT-coordinate distinction, and range;
- GRP-010 — raw FMCW cube -> range-selected snapshots -> covariance normalization semantics;
- GRP-011 — `2x2` covariance eigendecomposition;
- GRP-012 — MUSIC noise-subspace orthogonality;
- GRP-013 — mean-centered sample-covariance rank ceiling;
- SRC-01 — Doppler sign and FFT-coordinate mapping;
- SRC-02 — complex-noise/SNR scaling;
- SRC-03 — coherent-arrival covariance-rank collapse;
- SRC-04 — general bistatic versus common-look virtual MIMO geometry;
- SRC-05 — nondispersive phase/group delay and wrapped-phase ambiguity.

### E.4 Gate E decision

**Gate E status: PASS.**

The evidence set includes both numerical expected values and semantic test oracles.

---

## Gate F — Boundary and Failure Analysis

### F.1 Audit question

Does ADR-002 explicitly distinguish malformed inputs, physically meaningful scenarios outside PM-001, measurement/statistical incompatibilities, structural identifiability limitations, algorithm-applicability failures, and interpretation warnings?

### F.2 Evidence artifact

Detailed evidence is recorded in:

```text
docs/adr/ADR-002_BOUNDARY_FAILURE_ANALYSIS.md
```

with a dedicated reconciliation summary in:

```text
docs/adr/ADR-002_GATE_F_AUDIT.md
```

### F.3 Gate F decision

**Gate F status: PASS.**

The accepted four-class response taxonomy is:

- `REJECT`;
- `INCOMPATIBLE / REQUIRE OTHER MODEL`;
- `DIAGNOSTIC / WARN`;
- `VALID`.

The core rule is that physical scene validity, PM-001 compatibility, measurement/statistical compatibility, and estimator applicability are independent layers.

---

## Final Progressive Audit Conclusion

All six acceptance gates pass after incorporation of the recorded refinements.

This file preserves the progressive findings. Final acceptance is recorded separately only after the governing ADR, Golden Reference evidence, boundary/failure evidence, Gate F reconciliation, and cross-gate consistency are confirmed on the repository branch.
