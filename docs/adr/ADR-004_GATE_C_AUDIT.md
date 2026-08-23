# ADR-004 Gate C — Dimensional and Unit Consistency Audit

- **ADR:** ADR-004 — Validation, Reproducibility, and Scientific Evidence
- **Phase:** 0C — Scientific Foundations
- **Gate:** C — Dimensional and Unit Consistency
- **Gate result:** **PASS**
- **Governing draft:** `ADR-004-validation-reproducibility-scientific-evidence.md`
- **Reviewed governing content SHA:** `8cca2e3ac514cd031bee1d8c9e4c0347694ecb53`
- **Pre-Gate review:** PASS
- **Gate A:** PASS
- **Gate B:** PASS
- **Gates D–F:** Not evaluated by this audit
- **ADR-004 acceptance:** NOT ACCEPTED

> Gate C verifies that every physical or scientific quantity used by ADR-004 either inherits an explicit unit contract or is explicitly dimensionless/logarithmic/count-valued, and that derived metrics transform units consistently. Gate C does not establish software type/API semantics, formal Golden Reference acceptance, or boundary/failure acceptance.

---

## 1. Gate C Criterion

The Phase 0C roadmap defines Gate C as:

> Every physical quantity must have explicit units or be explicitly dimensionless. Unit conversion and normalization rules must be unambiguous.

ADR-004 is primarily an evidence contract, so it inherits the canonical physical units of ADR-001/ADR-002 rather than creating a second unit system.

The accepted upstream unit baseline includes:

```text
position / range / aperture        m
time / delay                       s
frequency / bandwidth / Doppler    Hz
angular frequency                  rad/s
phase / angle                      rad
wavelength                         m
wavenumber                         rad/m
propagation speed                  m/s
direction cosine                   dimensionless
geometry-only steering coefficient dimensionless complex
snapshot value                     declared measurement unit U
covariance / eigenvalue            U^2
correlation coefficient            dimensionless
SNR                                 dimensionless ratio, optionally dB representation
indices / counts                   dimensionless integer
```

External degree, GHz/MHz, ns, cm, or dB representations are permitted only through explicit conversion/representation semantics.

---

## 2. Audit Scope

Gate C checks:

```text
C1   angle / direction-coordinate units
C2   localization error / bias / RMSE units
C3   variance / MSE squared units
C4   degree-versus-radian conversion
C5   probability / confidence quantities
C6   association cost and gate units
C7   covariance / eigenvalue units
C8   normalized matrix / subspace metrics
C9   manifold/projective metrics
C10  spectrum / dB representation semantics
C11  SNR ratio / dB semantics
C12  Monte Carlo counts / sample counts
C13  fixed-point / quantization scaling
C14  hardware latency / II / throughput / resource / power units
C15  configuration canonicalization and unit conversion
C16  external/calibration artifact unit provenance
```

---

## 3. Canonical Angle and Direction Coordinates

ADR-001/ADR-002 establish canonical physical angle semantics in radians and direction cosine as dimensionless.

For VP-001,

\[
\theta\;[\mathrm{rad}],
\qquad
u=\sin\theta\;[1].
\]

Therefore an error in angle and an error in direction cosine are not merely numerically different; they have different semantic unit domains:

```text
Delta theta    angular quantity, canonical rad
Delta u        dimensionless
```

A result in degrees is a valid presentation/export representation only when explicitly labeled and converted.

### Gate-C finding

**PASS.** ADR-004 requires coordinate and units to be part of metric identity and does not collapse `theta` and `u` metrics.

---

## 4. Steering Exponent Dimensionality

VP-001 inherits

\[
a_n(\theta,f)
=\exp[-jk(x_n-x_{ref})\sin\theta].
\]

With

```text
k                 rad/m
x_n - x_ref       m
sin(theta)        dimensionless
```

the exponent has semantic angular unit `rad`, which is the required dimensionless phase argument of the exponential.

The steering coefficient is therefore dimensionless complex.

### Gate-C finding

**PASS.** The inherited manifold equation is dimensionally consistent.

---

## 5. Localization Error, Bias, Variance, MSE, and RMSE

For real scalar quantity `q` with unit `[Q]`,

\[
e=\hat q-q
\]

has unit `[Q]`.

Therefore:

```text
error e           [Q]
bias              [Q]
standard deviation [Q]
variance           [Q]^2
MSE                [Q]^2
RMSE               [Q]
```

For angular DOA in the canonical profile:

```text
error / bias / RMSE    rad
variance / MSE         rad^2
```

If an analysis is performed in degrees for human-readable reporting:

```text
error / bias / RMSE    deg
variance / MSE         deg^2
```

The two presentations shall never be numerically mixed without conversion.

### Gate-C finding

**PASS.** The governing metric rule requiring coordinate + units is dimensionally sufficient and consistent with the formulas.

---

## 6. GRP-018 Unit Cross-Check

GRP-018 uses a hand-friendly degree representation:

```text
truth      10 deg
estimates  9, 10, 12, 13 deg
errors     -1, 0, 2, 3 deg
bias       1 deg
MSE        3.5 deg^2
RMSE       sqrt(3.5) = 1.870828693... deg
v_N        2.5 deg^2
s^2        10/3 deg^2
```

Conversion to the canonical radian representation is:

\[
1\ \mathrm{deg}=\frac{\pi}{180}\ \mathrm{rad}.
\]

Thus

\[
3.5\ \mathrm{deg}^2
=3.5\left(\frac{\pi}{180}\right)^2\mathrm{rad}^2
\approx 1.066160969\times10^{-3}\ \mathrm{rad}^2,
\]

and

\[
1.870828693\ \mathrm{deg}
\approx 0.03265212044\ \mathrm{rad}.
\]

Squaring the converted RMSE reproduces the converted MSE.

### Gate-C finding

**PASS at audit level.** Degree presentation and canonical-radian semantics are mutually consistent. Formal GRP-018 PASS remains Gate E.

---

## 7. Empirical MSE Decomposition Units

In

\[
\widehat{MSE}=v_N+\bar e^2,
\]

both terms have unit `[Q]^2`:

```text
v_N          [Q]^2
bar(e)^2     [Q]^2
MSE          [Q]^2
```

Likewise the divisor-`N-1` sample variance `s^2` has `[Q]^2`.

### Gate-C finding

**PASS.** No mixed first-order/squared units occur in the decomposition.

---

## 8. Event Probabilities and Confidence Levels

The quantities

\[
P_D,
\qquad
P_{res},
\qquad
\widehat P_D,
\qquad
\widehat P_{res}
\]

are probabilities and therefore dimensionless numbers in `[0,1]`.

Their numerators and denominators are counts of compatible opportunities/trials and are dimensionless integers.

Confidence level, coverage probability, miss probability, and failure rate are likewise dimensionless probabilities.

Percentage representation is a display transform:

```text
0.90    probability
90 %    equivalent percentage representation
```

and must not be numerically mixed without explicit conversion.

### Gate-C finding

**PASS.** Probability metrics and event counts are dimensionally coherent.

---

## 9. Association Cost and Gate Units

Association cost inherits the coordinate/metric used by the study.

Examples:

```text
C_ij = |theta_i - theta_hat_j|    -> rad (or explicitly deg at a boundary)
C_ij = |u_i - u_hat_j|            -> dimensionless
normalized mixed-feature cost     -> dimensionless only after declared scaling
```

An association gate `tau_assoc` must have the same unit/domain as the cost it thresholds.

A mixed-dimensional cost cannot add angular, frequency, range, and amplitude discrepancies directly without declared scaling/normalization that makes the combined quantity dimensionally meaningful.

### Gate-C finding

**PASS.** ADR-004 requires cost coordinate and metric semantics to be declared; no universal unitless gate is assumed.

---

## 10. Snapshot and Measurement Units

Let a snapshot entry have declared measurement unit `[U]`.

Then

\[
X\;[U].
\]

The VP-001 uncentered sample second moment

\[
\hat R^{(2)}=\frac1LXX^H
\]

has unit

\[
[U]^2,
\]

because `L` is a dimensionless count.

Under normalized complex-baseband simulation, `U` may itself be dimensionless normalized amplitude. Such normalized data shall not be mislabeled volts, electric field, pressure, or calibrated power without a physical measurement model.

### Gate-C finding

**PASS.** The covariance/second-moment unit follows directly from the declared snapshot unit.

---

## 11. Covariance and Eigenvalue Units

For covariance/second-moment matrix

\[
R\;[U^2],
\]

its eigenvalues have the same unit `[U^2]` because

\[
Rv=\lambda v
\]

with eigenvectors treated as dimensionless coordinate vectors under the matrix representation.

Therefore:

```text
absolute covariance Frobenius norm      U^2
absolute spectral norm                  U^2
absolute eigenvalue error               U^2
eigengap                                U^2
trace / total second moment             U^2
```

A relative covariance error such as

\[
\frac{\|\tilde R-R\|_F}{\|R\|_F}
\]

is dimensionless when the denominator is nonzero.

### Gate-C finding

**PASS.** Absolute and relative matrix diagnostics have consistent units.

---

## 12. Hermitian / PSD Structural Diagnostics

A normalized Hermitian residual such as

\[
\frac{\|R-R^H\|_F}{\|R\|_F}
\]

is dimensionless.

Minimum eigenvalue has unit `[U^2]`; whether a negative value is significant requires a unit-aware numerical tolerance or scaling policy.

A PSD Boolean/status is categorical rather than a physical quantity.

### Gate-C finding

**PASS.** Structural diagnostics do not silently mix dimensional and normalized quantities.

---

## 13. Manifold Correlation and Projective Metrics

For nonzero manifold vectors of the same representation/unit,

\[
\rho(a,b)=\frac{|a^Hb|}{\|a\|\|b\|}
\]

is dimensionless because numerator and denominator carry the same squared vector-unit factor.

For the geometry-only VP-001 manifold, `a` and `b` are already dimensionless complex vectors.

Then

```text
rho                  dimensionless
rho^2                dimensionless
d_proj^2 = 1-rho^2   dimensionless
```

The principal/projective angle

\[
\alpha=\cos^{-1}\rho
\]

is an angular quantity with canonical semantic representation in radians.

### Gate-C finding

**PASS.** Projective metric units are consistent.

---

## 14. Projectors and Principal Angles

A normalized eigenvector/subspace basis is dimensionless under the chosen coordinate representation. Therefore projectors

\[
P=UU^H
\]

are dimensionless matrices.

Consequently:

```text
projector Frobenius error      dimensionless
projector operator error       dimensionless
singular values of U^H V       dimensionless
principal angles               rad
```

### Gate-C finding

**PASS.** Subspace diagnostics are unit consistent.

---

## 15. MUSIC Leakage and Spectrum Units

The normalized MUSIC truth-direction leakage

\[
\eta(\theta)
=\frac{a^H P_n a}{a^Ha}
\]

is dimensionless.

A reciprocal MUSIC pseudospectrum based on that normalized denominator is likewise dimensionless, although its numerical scale depends on the exact representation/floor/normalization.

Other spectra such as Bartlett or MVDR/Capon may carry power/second-moment units or may be normalized to a dimensionless representation depending on the declared formula.

Therefore ADR-004 correctly requires spectrum representation and normalization semantics to be part of metric provenance rather than assigning one universal spectrum unit.

### Gate-C finding

**PASS.** No universal unit is incorrectly imposed on all spectrum families.

---

## 16. dB Semantics

`dB` is a logarithmic representation of a dimensionless ratio, not an independent physical base unit.

Examples include:

```text
SNR_dB = 10 log10(P_s/P_n)
spectrum relative dB = 10 log10(P/P_ref)
amplitude-ratio dB = 20 log10(|a|/|a_ref|)
```

The factor `10` versus `20` depends on whether the declared ratio is power-like or amplitude-like.

An absolute physical quantity shall not be converted to dB without a declared reference quantity/unit system such as dBV, dBm, or another explicit reference convention.

### Gate-C finding

**PASS.** ADR-004's requirement to preserve representation/normalization prevents unlabeled dB quantities.

---

## 17. SNR Semantics

ADR-002 establishes SNR as a dimensionless ratio with optional dB representation.

For the PM-001 reference example,

\[
\mathrm{SNR}_{ch}=\frac{P_s}{\sigma_n^2}
\]

is dimensionless because numerator and denominator represent compatible power/second-moment quantities.

ADR-004 requires the SNR definition/profile to be part of condition/comparison provenance; a bare number such as `0 dB` is insufficient.

### Gate-C finding

**PASS.** Fair-comparison evidence cannot mix incompatible SNR definitions solely because the dB number matches.

---

## 18. Monte Carlo Counts, Ranks, and IDs

The following are dimensionless integer/count-valued quantities:

```text
L                  snapshot count
N                  Monte Carlo trial count
K                  source count
K_hat              output cardinality
rank               matrix/subspace rank
condition count
matched-pair count
failure count
resource counts such as LUT/DSP/BRAM blocks
```

They are semantically distinct despite sharing the same dimensional class.

IDs, hashes, Git SHAs, run IDs, and artifact IDs are identifiers, not physical quantities.

### Gate-C finding

**PASS.** Dimensionless does not imply semantic interchangeability.

---

## 19. Fixed-Point Representation and Scaling

A raw fixed-point word is fundamentally a digital code/number representation. Scientific unit interpretation requires a declared scaling contract.

For a fixed-point quantity representing physical/signal quantity `x`, a conceptual relation may be

\[
x_{phys}=q\,\Delta_x,
\]

where `q` is a dimensionless integer code and `Delta_x` carries the physical/scientific unit of `x`.

Accordingly, fixed-point provenance must preserve:

```text
word format
binary-point / scale
LSB size or equivalent scale
physical/scientific unit represented
rounding / saturation semantics
cast/rescaling points
```

An internal dimensionless normalized amplitude may remain dimensionless; it shall not acquire volts or watts merely because it is stored in fixed point.

### Gate-C finding

**PASS.** ADR-004 F11's scaling/provenance contract is compatible with dimensional analysis.

---

## 20. ADC Quantization versus FPGA Fixed-Point Units

ADC quantization belongs to the acquisition/sensor chain and may use physical full-scale/voltage units. FPGA internal quantization may instead represent normalized or rescaled digital values.

Therefore identical bit widths do not imply identical quantization step or physical unit.

Example distinction:

```text
ADC code LSB        V/code or declared acquisition unit/code
FPGA internal LSB   declared normalized/algorithm unit/code
```

### Gate-C finding

**PASS.** The two quantization layers remain unit- and role-distinct.

---

## 21. Hardware Latency, II, and Throughput

ADR-004 distinguishes:

```text
latency in cycles                 cycle count
latency in time                   s
clock frequency                   Hz = cycles/s
initiation interval               cycles/transaction or cycles/item
throughput                        item/s, sample/s, frame/s, estimate/s, etc.
```

Conversion requires the relevant clock frequency and definition of the transaction/item:

\[
T_{latency}
=\frac{N_{cycles}}{f_{clk}}.
\]

This produces seconds when `N_cycles` is a count and `f_clk` is in s^-1.

II is not throughput until the processed item and clock are declared. In an ideal one-item-per-II pipeline,

\[
\mathrm{throughput}\approx\frac{f_{clk}}{II}
\]

with units items/s under the declared item semantics.

### Gate-C finding

**PASS.** Hardware timing quantities are not dimensionally conflated.

---

## 22. Resource, Power, and Energy Units

Hardware resource utilization may be represented as:

```text
LUT / FF / DSP / BRAM count       dimensionless integer
resource utilization percentage   dimensionless percentage
power                              W
energy                             J
energy per frame/estimate          J/frame or J/estimate
clock frequency                    Hz
WNS/TNS timing slack               s, typically reported ns by tools
```

A synthesis power estimate and a measured board power use the same physical dimension but remain different evidence roles.

### Gate-C finding

**PASS.** Scientific and hardware metrics preserve both unit and evidence-role distinctions.

---

## 23. Runtime and Speedup

Runtime has unit seconds (or an explicitly converted time unit).

Speedup

\[
S=\frac{T_{ref}}{T_{acc}}
\]

is dimensionless because numerator and denominator must have compatible timing units/scopes.

A ratio of incomparable scopes is numerically dimensionless but scientifically invalid; unit cancellation alone does not establish comparison fairness.

### Gate-C finding

**PASS.** Dimensional consistency and scope comparability remain separate requirements.

---

## 24. Canonical Configuration Unit Normalization

ADR-004 F12 requires canonical configuration identity to normalize compatible units before semantic hashing while preserving the scientific meaning and original/audit representation where useful.

Thus:

```text
0.5 m
50 cm
```

may canonicalize to the same physical quantity, whereas

```text
0.5 m
0.5 wavelength
```

are not silently identical because wavelength normalization depends on frequency/medium context.

Likewise:

```text
30 deg
pi/6 rad
```

may canonicalize to the same angle under an exact unit conversion, while their original input representation may remain in provenance.

### Gate-C finding

**PASS.** Unit conversion supports semantic identity without erasing contextual normalization semantics.

---

## 25. External Data / Calibration / CST Unit Provenance

External artifacts shall preserve units and reference semantics at import boundaries.

Examples include:

```text
position grid                 m
frequency grid                Hz
angle grid                    rad after canonical conversion
complex field/manifold        declared normalization/unit
calibration gain              declared amplitude/complex-scale convention
channel delay                 s
phase                         rad
```

Magnitude-only dB exports, normalized field exports, or arbitrary tool units cannot be interpreted as calibrated physical quantities without explicit reference/normalization metadata.

### Gate-C finding

**PASS.** External artifact provenance prevents unit-free scientific import.

---

## 26. Relative Error and Near-Zero Denominators

A relative error such as

\[
\epsilon_{rel}=\frac{\|\tilde x-x\|}{\|x\|}
\]

is dimensionless only when numerator and denominator use compatible units and the denominator is nonzero.

If the reference norm approaches zero, a profile-specific floor, absolute metric, or typed invalid/inapplicable state is required. The floor must carry the same unit as the denominator before normalization.

### Gate-C finding

**PASS.** This is a dimensional/domain boundary already compatible with Gate-B and later Gate-F handling.

---

## 27. Weighted Metrics and Mixed Units

If a weighted quadratic metric uses

\[
(x-\mu)^H W(x-\mu),
\]

the weight `W` must carry the inverse units required to make the intended result dimensionally meaningful, or the variables must first be nondimensionalized by declared scales.

This matters for future mixed-angle/range/frequency association or validation metrics.

ADR-004 does not currently freeze such a mixed metric, so no dimensional inconsistency is introduced.

### Gate-C finding

**PASS.** Future mixed-unit metrics are correctly deferred to explicit scaled/profile definitions.

---

## 28. Gate-C Boundary Conditions Carried Forward

The following are explicit unit/domain conditions for Gate F and software implementation:

1. canonical internal angle/phase representation is radians unless a boundary explicitly converts another representation;
2. direction cosine and probabilities are dimensionless but semantically distinct;
3. bias/RMSE share the base metric unit; variance/MSE use its square;
4. covariance/eigenvalue units derive from the declared snapshot measurement unit;
5. normalized matrix/manifold/subspace metrics are dimensionless only when numerator/denominator units match and denominator is nonzero;
6. principal/projective angles use radians canonically;
7. dB requires a dimensionless ratio or an explicit absolute reference convention;
8. SNR is a typed dimensionless ratio before dB representation;
9. association gate units must match the declared cost;
10. fixed-point codes require explicit scale to acquire scientific/physical units;
11. latency cycles require clock frequency for conversion to time;
12. throughput requires an explicit processed-item semantic;
13. normalized simulation amplitudes do not silently become physical volts/fields/powers;
14. canonical unit conversion shall not erase wavelength/frequency/reference-plane dependencies.

No Gate-C blocker remains from these conditions.

---

## 29. Gate C Checklist

```text
Upstream SI/canonical unit authority preserved                 PASS
Steering exponent dimensionally valid                         PASS
Theta vs direction-cosine units                               PASS
Error / bias / RMSE units                                     PASS
Variance / MSE squared units                                  PASS
GRP-018 degree/radian conversion                              PASS (audit only; Gate E pending)
Event probabilities dimensionless                             PASS
Association cost/gate unit consistency                        PASS
Snapshot -> covariance unit propagation                       PASS
Covariance / eigenvalue units                                 PASS
Relative covariance / Hermitian residual dimensionless        PASS
Manifold correlation/projective distance dimensionless         PASS
Principal angles in radians                                   PASS
Spectrum normalization/unit semantics                         PASS
dB/logarithmic representation                                 PASS
SNR ratio / dB semantics                                      PASS
Counts/ranks/IDs dimensional class                            PASS
Fixed-point scale/LSB unit semantics                          PASS
ADC vs FPGA quantization unit separation                      PASS
Latency / II / throughput dimensional consistency             PASS
Resource / power / energy units                               PASS
Runtime / speedup units                                       PASS
Canonical config unit normalization                           PASS
External/calibration artifact unit provenance                 PASS
Relative-error denominator/unit domain                        PASS
Mixed-unit metric scaling rule                                PASS
Blocking dimensional/unit contradiction                       NONE
```

---

## 30. Gate C Decision

### **Gate C — Dimensional and Unit Consistency: PASS**

ADR-004 is dimensionally coherent at the governing-contract level.

It correctly inherits canonical SI-compatible physical units from ADR-001/ADR-002, requires every metric to preserve coordinate and unit identity, transforms localization units correctly through bias/variance/MSE/RMSE, keeps probabilities and normalized/projective metrics dimensionless, preserves measurement-unit-squared covariance/eigenvalue semantics, distinguishes logarithmic dB representations from physical units, and keeps fixed-point/hardware quantities tied to explicit scaling and timing scopes.

No correction to the governing ADR is required for Gate-C PASS. The detailed unit rules in this audit operationalize the existing governing requirements and shall inform Gate D software semantics and Gate F boundary behavior.

---

## 31. Status after Gate C

```text
Pre-Gate consistency review                PASS
Gate A — Physical Consistency              PASS
Gate B — Mathematical Consistency          PASS
Gate C — Dimensional / Unit Consistency    PASS
Gate D — Software Semantic Consistency      NEXT
Gate E — Hand Reference Evidence            NOT STARTED
Gate F — Boundary / Failure Analysis         NOT STARTED
ADR-004 acceptance                          NOT ACCEPTED
Authoritative Phase-1 implementation        NOT YET AUTHORIZED
```

The next work item is:

```text
ADR-004 Gate D — Software Semantic Consistency Audit
```
