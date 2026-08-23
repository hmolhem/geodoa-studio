# ADR-004 — Golden Reference Problems

- **Governing ADR:** `../../adr/ADR-004-validation-reproducibility-scientific-evidence.md`
- **Phase:** 0C — Scientific Foundations
- **Gate:** E — Hand-Calculated Reference Evidence
- **Status:** Complete — deterministic evidence for Gate E audit
- **Canonical reserved problem:** GRP-018
- **Supplemental deterministic references:** `ADR-004-SRC-01` through `ADR-004-SRC-04`

## 1. Purpose

These references provide manually inspectable, implementation-independent evidence for ADR-004. They are intended to serve simultaneously as:

1. scientific-definition checks;
2. hand-computable verification references;
3. future Phase-1 software-test oracles;
4. regression anchors for metric/event semantics.

The Phase 0C roadmap reserves only:

```text
GRP-018 — Bias, Variance, MSE, and RMSE by hand
```

Additional deterministic checks are recorded as `ADR-004-SRC-*` so canonical GRP numbering is not expanded implicitly.

Unless otherwise stated:

```text
angles are real scalar localization quantities
canonical internal angular unit is radian
reported degrees are exact presentation inputs/conversions where stated
probabilities are dimensionless
finite counts are exact integers
all arithmetic is exact until a decimal approximation is explicitly shown
```

The tolerances below are future deterministic regression-oracle tolerances. They are **not** universal scientific acceptance thresholds.

---

# GRP-018 — Bias, Variance, MSE, and RMSE by Hand

## Contract exercised

- real-valued scalar localization error;
- signed error;
- empirical bias;
- divisor-`N` empirical centered second moment `v_N`;
- divisor-`N-1` sample variance `s^2`;
- empirical MSE and RMSE;
- exact finite-sample decomposition;
- squared-unit versus base-unit semantics;
- degree/radian conversion consistency.

## Given

Truth:

\[
q_0=10^\circ.
\]

Four estimates:

\[
\hat q=\{9^\circ,10^\circ,12^\circ,13^\circ\}.
\]

Define the signed error

\[
e_i=\hat q_i-q_0.
\]

Therefore

\[
\boxed{
e=\{-1,0,2,3\}^\circ.
}
\]

The sample count is

\[
N=4.
\]

---

## Path A — Direct Error-Moment Calculation

### Empirical bias

\[
\bar e
=\frac{-1+0+2+3}{4}
=\frac{4}{4}
=\boxed{1^\circ}.
\]

### Empirical MSE

Square the errors:

\[
e_i^2=\{1,0,4,9\}\ \mathrm{deg}^2.
\]

Then

\[
\widehat{MSE}
=\frac{1+0+4+9}{4}
=\frac{14}{4}
=\boxed{3.5\ \mathrm{deg}^2}.
\]

### Empirical RMSE

\[
\widehat{RMSE}
=\sqrt{3.5}\ ^\circ
=\boxed{1.8708286933869707^\circ}.
\]

This is the primary direct path.

---

## Path B — Independent Centered-Moment Decomposition

The centered error deviations are

\[
e_i-\bar e
=\{-2,-1,1,2\}^\circ.
\]

Their squares are

\[
\{4,1,1,4\}\ \mathrm{deg}^2.
\]

Define the divisor-`N` empirical centered second moment

\[
v_N
=\frac1N\sum_i(e_i-\bar e)^2.
\]

Hence

\[
v_N
=\frac{4+1+1+4}{4}
=\frac{10}{4}
=\boxed{2.5\ \mathrm{deg}^2}.
\]

Now evaluate the exact finite-sample decomposition:

\[
v_N+\bar e^2
=2.5+1^2
=\boxed{3.5\ \mathrm{deg}^2}.
\]

Therefore

\[
\boxed{
\widehat{MSE}=v_N+\bar e^2
}
\]

is independently recovered.

The unbiased sample variance estimator is instead

\[
s^2
=\frac{1}{N-1}\sum_i(e_i-\bar e)^2
=\frac{10}{3}
=\boxed{3.333333333333333\ \mathrm{deg}^2}.
\]

Thus

\[
\boxed{s^2\neq v_N}
\]

and `s^2` is not the exact finite-sample decomposition term.

---

## Population-Identity Interpretation

For a fixed real truth `q_0`, the governing population identity is

\[
\operatorname{MSE}
=\operatorname{Var}(\hat q)+\operatorname{Bias}^2.
\]

GRP-018 does **not** claim that `v_N` is an unbiased estimator of the population variance. It verifies the finite empirical identity used by the ADR:

\[
\widehat{MSE}=v_N+\bar e^2.
\]

This distinction is normative.

---

## Canonical Radian Conversion

Use

\[
1^\circ=\frac{\pi}{180}\ \mathrm{rad}.
\]

Therefore the bias is

\[
\boxed{
\bar e
=\frac{\pi}{180}
\approx0.017453292519943295\ \mathrm{rad}.
}
\]

MSE converts quadratically:

\[
\widehat{MSE}_{rad^2}
=3.5\left(\frac{\pi}{180}\right)^2
\]

so

\[
\boxed{
\widehat{MSE}_{rad^2}
\approx0.00106616096925348\ \mathrm{rad}^2.
}
\]

RMSE converts linearly:

\[
\widehat{RMSE}_{rad}
=\sqrt{3.5}\frac{\pi}{180}
\]

so

\[
\boxed{
\widehat{RMSE}_{rad}
\approx0.0326521204403861\ \mathrm{rad}.
}
\]

Similarly,

\[
\boxed{
v_{N,rad^2}
=2.5\left(\frac{\pi}{180}\right)^2
\approx0.0007615435494667714\ \mathrm{rad}^2
}
\]

and

\[
\boxed{
s^2_{rad^2}
=\frac{10}{3}\left(\frac{\pi}{180}\right)^2
\approx0.0010153913992890285\ \mathrm{rad}^2.
}
\]

---

## Expected Results / Oracle

```text
truth                                 10 deg
estimates                             9, 10, 12, 13 deg
errors                                -1, 0, 2, 3 deg
N                                     4
bias                                  1 deg
v_N                                   2.5 deg^2
sample variance s^2                   10/3 deg^2
MSE                                   3.5 deg^2
RMSE                                  sqrt(3.5) deg
RMSE decimal                          1.8708286933869707 deg
bias                                  pi/180 rad
MSE                                   3.5*(pi/180)^2 rad^2
RMSE                                  sqrt(3.5)*pi/180 rad
```

---

## Future Regression Oracle

For a float64 implementation using degree inputs for this explicit test fixture:

```text
errors exactly equal [-1, 0, 2, 3] within float representation
abs(bias_deg - 1.0) < 1e-12
abs(vN_deg2 - 2.5) < 1e-12
abs(sample_variance_deg2 - 10/3) < 1e-12
abs(mse_deg2 - 3.5) < 1e-12
abs(rmse_deg - sqrt(3.5)) < 1e-12
```

For canonical-radian conversion:

```text
abs(bias_rad - pi/180) < 1e-14
abs(mse_rad2 - 3.5*(pi/180)^2) < 1e-14
abs(rmse_rad - sqrt(3.5)*pi/180) < 1e-14
```

Tolerance rationale:

- all degree-domain arithmetic except the square root is exact rational arithmetic;
- square-root and `pi` conversion checks are ordinary float64 transcendental evaluations;
- the stated tolerances are deliberately much tighter than any physical/engineering acceptance threshold and are intended only to catch semantic or implementation mistakes.

---

## Failure Interpretation

The following shall fail this reference:

```text
using absolute errors instead of signed errors for bias
using divisor N-1 in the exact MSE decomposition term
reporting MSE in deg instead of deg^2
reporting RMSE in deg^2 instead of deg
converting MSE from deg^2 to rad^2 with only one power of pi/180
silently dropping one estimate
replacing a missing/failed estimate with an arbitrary angular penalty
```

---

## Scientific Conclusion

GRP-018 establishes the canonical finite-sample localization-error semantics for ADR-004:

\[
\boxed{
\widehat{MSE}=v_N+\bar e^2
}
\]

with `v_N` defined using divisor `N`, while the divisor-`N-1` sample variance is a distinct statistical estimator. Bias and RMSE carry the base angular unit; variance and MSE carry the squared angular unit.

---

# ADR-004-SRC-01 — Multi-Source Association, Spurious Output, and Resolution

## Contract exercised

- unordered multi-source truth;
- one-to-one association;
- association gate;
- unmatched estimate as spurious output;
- pair-resolution event distinct from no-spurious clean resolution;
- matched localization error.

## Given

Truth set:

\[
\Theta=\{0^\circ,10^\circ\}.
\]

Estimate set:

\[
\hat\Theta=\{1^\circ,9^\circ,40^\circ\}.
\]

Use absolute angular cost

\[
C_{ij}=|\theta_i-\hat\theta_j|
\]

with association gate

\[
\tau_{assoc}=3^\circ.
\]

## Cost Table

```text
                estimate 1 deg   estimate 9 deg   estimate 40 deg
truth 0 deg          1                9                40
truth 10 deg         9                1                30
```

Admissible edges are only costs `<=3 deg`:

```text
0 deg truth  <-> 1 deg estimate
10 deg truth <-> 9 deg estimate
```

The `40 deg` estimate is unmatched.

## Association Result

```text
matched pairs:       (0 -> 1), (10 -> 9)
unmatched truth:     none
unmatched estimates: {40}
```

Matched signed errors are

\[
\{+1,-1\}^\circ.
\]

Therefore

\[
\bar e=0^\circ,
\qquad
\widehat{MSE}=1\ \mathrm{deg}^2,
\qquad
\widehat{RMSE}=1^\circ.
\]

Both truth sources have distinct admissible matches, therefore the baseline pair-resolution event is

\[
\boxed{R_{pair}=1}.
\]

But one spurious estimate exists. Therefore a stricter event defined as

```text
pair resolved AND no spurious estimates
```

would have

\[
\boxed{R_{clean}=0}.
\]

## Expected Results / Oracle

```text
matched count              2
missed truth count         0
spurious estimate count    1
matched errors             +1, -1 deg
matched bias               0 deg
matched MSE                1 deg^2
matched RMSE               1 deg
baseline pair resolved     true
clean no-spurious resolved false
```

## Future Regression Oracle

The software shall not:

```text
truncate the estimate list to K=2 before evidence recording
drop the 40-deg estimate silently
reuse one estimate for both truth sources
mark pair resolution false merely because a separate spurious output exists
mark clean no-spurious resolution true
```

## Scientific Conclusion

Association, spurious detection, resolution, and localization accuracy are separate evidence objects. A pair can be truth-based resolved while the estimator still produces an extra spurious output.

---

# ADR-004-SRC-02 — End-to-End `P_res` Denominator and Failure Mapping

## Contract exercised

- fixed eligible compatible trial universe;
- numerical failure retained in the denominator for end-to-end probability;
- conditional valid-output probability is a different estimand;
- typed failure evidence remains visible.

## Given

Five scientifically eligible, method-compatible trials for one fixed condition:

```text
Trial 1   resolved valid output
Trial 2   unresolved valid output
Trial 3   numerical algorithm failure
Trial 4   resolved valid output
Trial 5   missed/unresolved valid output
```

For the VP-001 baseline end-to-end `P_res`, all five trials are in the denominator.

## End-to-End Calculation

Resolved trials:

\[
N_{resolved}=2.
\]

Eligible compatible trials:

\[
N_{eligible,compatible}=5.
\]

Therefore

\[
\boxed{
\widehat P_{res}=\frac25=0.4.
}
\]

The numerical failure contributes event non-success but retains its failure type.

## Conditional Valid-Output Contrast

If one intentionally defines a **different** conditional metric over valid estimator outputs only, the denominator becomes four:

\[
\widehat P_{res\mid valid}
=\frac24
=\boxed{0.5}.
\]

Therefore

\[
\boxed{
P_{res}\neq P_{res\mid valid}
}
\]

for this deterministic example.

## Expected Results / Oracle

```text
eligible compatible trials       5
resolved trials                  2
numerical failures               1
end-to-end P_res                 0.4
valid-output-only denominator    4
conditional P_res|valid          0.5
```

## Future Regression Oracle

A baseline end-to-end aggregator shall return exactly `0.4` for this fixture and shall preserve the numerical-failure count as `1`.

Silently filtering the numerical failure and returning `0.5` under the baseline metric identity is a semantic failure.

## Scientific Conclusion

Failure filtering changes the estimand. End-to-end probability and valid-output conditional probability require different identities and denominators.

---

# ADR-004-SRC-03 — Source-Level `P_D` Opportunity Counting

## Contract exercised

- source-level detection denominator;
- missed source opportunity;
- numerical failure as end-to-end non-detection;
- distinction from valid-output conditional detection probability.

## Given

Three eligible compatible trials, each with exactly two truth sources:

```text
Trial 1: both sources detected                  -> 2 detections
Trial 2: one detected, one missed               -> 1 detection
Trial 3: numerical algorithm failure            -> 0 detections, 2 affected opportunities
```

Total eligible truth-source opportunities:

\[
N_{opp}=3\times2=6.
\]

Total detected truth-source opportunities:

\[
N_{det}=2+1+0=3.
\]

## End-to-End Detection Probability

\[
\boxed{
\widehat P_D=\frac36=0.5.
}
\]

The numerical failure remains a typed trial failure while its two eligible truth opportunities are non-detections for this end-to-end metric.

## Conditional Valid-Output Contrast

If the failed trial is excluded under a separately named valid-output conditional metric:

\[
N_{opp\mid valid}=4,
\qquad
N_{det\mid valid}=3,
\]

hence

\[
\boxed{
\widehat P_{D\mid valid}=\frac34=0.75.
}
\]

Again,

\[
\boxed{P_D\neq P_{D\mid valid}}.
\]

## Expected Results / Oracle

```text
trials                            3
truth opportunities              6
detected opportunities           3
numerical-failure trials         1
end-to-end P_D                   0.5
valid-output opportunities       4
conditional P_D|valid            0.75
```

## Scientific Conclusion

Source-level detection probability is an opportunity-count metric. A numerical failure does not erase the physical/source opportunities that belonged to an otherwise eligible compatible trial under the end-to-end metric definition.

---

# ADR-004-SRC-04 — Projective Manifold Metric and Rank-One Leakage

## Contract exercised

- normalized manifold correlation;
- projective angle;
- projective squared distance;
- rank-one orthogonal-projector leakage identity;
- complex-scale/gauge invariance domain.

## Given

Use two nonzero real vectors as a simple complex-vector special case:

\[
a=\begin{bmatrix}1\\0\end{bmatrix},
\qquad
b=\frac1{\sqrt2}\begin{bmatrix}1\\1\end{bmatrix}.
\]

Both are unit norm:

\[
\|a\|_2=\|b\|_2=1.
\]

## Normalized Correlation

\[
a^Hb=\frac1{\sqrt2}.
\]

Therefore

\[
\boxed{
\rho(a,b)=\frac1{\sqrt2}.
}
\]

## Projective Angle

\[
\alpha=\cos^{-1}\rho
=\cos^{-1}\left(\frac1{\sqrt2}\right)
=\boxed{\frac\pi4\ \mathrm{rad}}
=45^\circ.
\]

## Projective Squared Distance

\[
d_{proj}^2
=1-\rho^2
=1-\frac12
=\boxed{\frac12}.
\]

## Rank-One Projector Leakage

For

\[
P_a^\perp=I-aa^H
=\begin{bmatrix}0&0\\0&1\end{bmatrix},
\]

\[
P_a^\perp b
=\frac1{\sqrt2}\begin{bmatrix}0\\1\end{bmatrix}.
\]

Hence

\[
\boxed{
\|P_a^\perp b\|_2^2=\frac12=1-\rho^2.
}
\]

## Complex-Scale Invariance Check

Let

\[
\tilde a=2e^{j\pi/3}a,
\qquad
\tilde b=5e^{-j\pi/7}b.
\]

Then the nonzero scalar magnitudes/phases cancel from normalized correlation, so

\[
\boxed{
\rho(\tilde a,\tilde b)=\rho(a,b)=\frac1{\sqrt2}.
}
\]

## Expected Results / Oracle

```text
rho                    1/sqrt(2)
alpha                  pi/4 rad
alpha                  45 deg presentation
d_proj^2               1/2
projector leakage      1/2
scaled-vector rho      1/sqrt(2)
```

## Future Regression Oracle

```text
abs(rho - 1/sqrt(2)) < 1e-14
abs(alpha_rad - pi/4) < 1e-14
abs(d_proj2 - 0.5) < 1e-14
abs(projector_leakage - 0.5) < 1e-14
```

The normalized metric is undefined for a zero vector; zero/invalid manifold input must not be forced through this oracle.

## Scientific Conclusion

The projective manifold metric is bounded, gauge invariant to nonzero common complex scale, and exactly equal to rank-one orthogonal leakage through `1-rho^2` in this declared case.

---

# 2. Gate-E Evidence Coverage Summary

| Reference | Primary contract covered |
|---|---|
| GRP-018 | bias / `v_N` / sample variance / MSE / RMSE / units |
| ADR-004-SRC-01 | association / spurious output / pair resolution / matched error |
| ADR-004-SRC-02 | `P_res` denominator / numerical-failure mapping / conditioning |
| ADR-004-SRC-03 | source-level `P_D` opportunity denominator / failure mapping |
| ADR-004-SRC-04 | `rho` / projective angle / `d_proj^2` / projector leakage / gauge invariance |

These supplemental references do not imply that every ADR-004 evidence concept requires a hand-calculated numerical oracle. Provenance, publication immutability, calibration-vs-validation vocabulary, software scheduling semantics, and hardware build identity are primarily semantic/structural contracts verified by other gates and future implementation tests.

---

# 3. Gate-E Readiness Statement

The deterministic evidence in this file is independent of future production implementation and is sufficiently small to verify by hand/basic calculator.

No result in this file is derived from a saved GeoDOA production output.

The references intentionally separate:

```text
exact integer/rational arithmetic
transcendental presentation conversions
scientific metric identity
metric denominator/universe
failure-state preservation
future regression tolerance
```

Formal Gate-E PASS is recorded separately in `../../adr/ADR-004_GATE_E_AUDIT.md` after review of this evidence.
