# ADR-003 — Golden Reference Problems

- **Governing ADR:** `../../adr/ADR-003-sensor-imperfections-mutual-coupling-calibration.md`
- **Phase:** 0C — Scientific Foundations
- **Gate:** E — Hand-Calculated Reference Evidence
- **Status:** Complete — candidate evidence for Gate E PASS
- **Canonical reserved problems:** GRP-014 through GRP-017
- **Supplemental deterministic references:** `ADR-003-SRC-01` through `ADR-003-SRC-08`

## 1. Purpose

These deterministic reference problems provide manually inspectable evidence for ADR-003. Each reference is intended to serve simultaneously as:

1. a physical/mathematical interpretation example;
2. a hand-computable verification reference;
3. a future regression-test oracle.

The canonical roadmap reserves GRP-014 through GRP-017 for ADR-003. Additional deterministic checks needed to cover timing, ADC/receiver, calibration, and operator-composition contracts are recorded as `ADR-003-SRC-*` so that canonical GRP numbering is not changed.

Unless otherwise stated:

```text
propagation speed v = 3.0e8 m/s
angles are scientific radians internally
reported degrees are presentation conversions
complex steering vectors use ADR-001 / ADR-002 receive sign conventions
floating calculations are exact/analytical until a decimal value is explicitly reported
```

Numerical tolerances listed below are future regression-oracle recommendations, not general physical acceptance thresholds.

---

# GRP-014 — Position-Error Phase Distortion and Rigid-Translation Invariance

## Contract exercised

- nominal versus physical geometry;
- stable nominal phase reference;
- position-error phase sign;
- pairwise/reference-invariant distortion;
- nominal-manifold DOA bias under spacing error;
- rigid-translation common-phase invariance.

## Given

Two receive sensors on the `x` axis at `f = 1.0 GHz`:

```text
v = 3.0e8 m/s
lambda = v/f = 0.30 m
k = 2 pi/lambda = 20.9439510239 rad/m
nominal spacing d = lambda/2 = 0.15 m
true direction cosine u0 = 0.5
true angle theta0 = asin(0.5) = 30 deg
spacing error delta_d = +0.003 m
relative spacing error delta_d/d = 0.02
physical spacing = 0.153 m
```

Use sensor 1 as the origin for the two-sensor phase-difference calculation, or equivalently use any fixed ADR-001 phase reference and then take the pairwise phase difference.

## Nominal pairwise phase

For a half-wave nominal spacing,

\[
\Delta\phi_{\rm nom}
=-kdu_0
=-\pi(0.5)
=-\frac{\pi}{2}
=-90^\circ.
\]

## Physical pairwise phase

The physical spacing is `d + delta_d`, hence

\[
\Delta\phi_{\rm phys}
=-k(d+\delta d)u_0.
\]

Since

\[
\frac{d+\delta d}{d}=1.02,
\]

\[
\Delta\phi_{\rm phys}
=-1.02\frac{\pi}{2}
=-0.51\pi
=-91.8^\circ.
\]

The pairwise phase perturbation is therefore

\[
\boxed{
\delta\phi_{21}
=\Delta\phi_{\rm phys}-\Delta\phi_{\rm nom}
=-1.8^\circ
=-0.03141592654\ \mathrm{rad}.
}
\]

This agrees with

\[
\delta\phi_{21}
=-k\,\delta d\,u_0.
\]

## Nominal-model inferred direction cosine

If the physical phase is fitted with the nominal spacing `d`,

\[
-kd\hat u=-k(d+\delta d)u_0,
\]

so

\[
\boxed{
\hat u
=\left(1+\frac{\delta d}{d}\right)u_0
=1.02(0.5)
=0.51.
}
\]

Thus

\[
\boxed{
\hat\theta=\sin^{-1}(0.51)=30.6638297424^\circ.
}
\]

The exact angular bias is

\[
\boxed{
\Delta\theta
=0.6638297424^\circ
=0.011585033\ \mathrm{rad}\ \text{(approximately)}.
}
\]

## Small-error angular approximation

For `u=sin(theta)`,

\[
\Delta\theta
\approx
\frac{\Delta u}{\cos\theta_0}
=\frac{(\delta d/d)u_0}{\cos\theta_0}
=\frac{\delta d}{d}\tan\theta_0.
\]

Therefore

\[
\Delta\theta_{\rm first}
=0.02\tan 30^\circ
=0.01154700538\ \mathrm{rad}
=0.6615946745^\circ.
\]

The difference from the exact angle conversion is about `0.002235 deg`, demonstrating the bounded first-order nature of the approximation.

## Rigid-translation check

Now translate **both** physical sensors by

```text
t = +0.06 m = +0.2 lambda
```

while retaining the same fixed nominal ADR-001 phase reference.

The common far-field phase added to every channel is

\[
\delta\phi_{\rm common}
=-ktu_0
=-\frac{2\pi}{0.30}(0.06)(0.5)
=-0.2\pi
=-36^\circ.
\]

Because both channels receive the same additional phase,

\[
\boxed{
\delta\phi_{21}^{\rm translation}=0.
}
\]

Thus the pairwise manifold and DOA information are unchanged.

## Expected results / oracle

```text
lambda                              0.30 m
k                                   20.9439510239 rad/m
nominal pairwise phase              -90.0 deg
physical pairwise phase             -91.8 deg
position-induced pair phase error   -1.8 deg
inferred u with nominal spacing     0.51
exact inferred theta                30.6638297424 deg
exact angular bias                  +0.6638297424 deg
first-order angular bias            +0.6615946745 deg
rigid-translation common phase      -36.0 deg
rigid-translation pairwise change   0
```

## Future regression oracle

Recommended deterministic assertions:

```text
abs(u_hat - 0.51) < 1e-12
abs(theta_hat_deg - 30.6638297424) < 1e-9
abs(pair_phase_error_deg + 1.8) < 1e-10
abs(rigid_translation_pair_phase_change) < 1e-12 rad
```

## Scientific conclusion

A relative spacing error produces deterministic manifold/DOA bias when the estimator retains the nominal geometry. A common rigid translation only changes common phase under the far-field model and does not change pairwise spatial information.

---

# GRP-015 — Gain/Phase Mismatch and Two-Sensor DOA Bias

## Contract exercised

- diagonal electronic gain/phase response;
- relative versus common phase;
- nominal-manifold phase-mismatch bias;
- common-phase covariance invariance.

## Given

Use the same half-wave two-sensor array:

```text
f = 1.0 GHz
lambda = 0.30 m
d = lambda/2 = 0.15 m
kd = pi
u0 = 0.5
theta0 = 30 deg
```

Nominal steering vector:

\[
\mathbf a
=\begin{bmatrix}
1\\
e^{-j\pi/2}
\end{bmatrix}
=\begin{bmatrix}
1\\-j
\end{bmatrix}.
\]

Apply a `+10 deg` electronic phase error to channel 2 only:

\[
\phi_e=10^\circ=\frac{\pi}{18}.
\]

Take unit amplitudes:

\[
\mathbf G
=\operatorname{diag}(1,e^{j\phi_e}).
\]

## Physical relative phase

The channel-2 phase becomes

\[
-90^\circ+10^\circ=-80^\circ.
\]

If an estimator still fits the nominal half-wave phase law,

\[
-\pi\hat u=-\pi u_0+\phi_e.
\]

Therefore

\[
\boxed{
\hat u
=u_0-\frac{\phi_e}{\pi}
=0.5-\frac{10}{180}
=0.444444444444.
}
\]

The inferred angle is

\[
\boxed{
\hat\theta
=\sin^{-1}(0.444444444444)
=26.3877999612^\circ.
}
\]

Thus

\[
\boxed{
\Delta\theta
=-3.6122000388^\circ.
}
\]

The direction-cosine bias is exactly

\[
\boxed{
\Delta u=-\frac{\phi_e}{\pi}=-0.055555555556.
}
\]

## Common-phase invariance

Now multiply the entire array response by an additional common phase

\[
e^{j25^\circ}.
\]

Let

\[
\mathbf b=e^{j25^\circ}\mathbf a.
\]

Then

\[
\boxed{
\mathbf b\mathbf b^H
=e^{j25^\circ}\mathbf a
\mathbf a^H e^{-j25^\circ}
=\mathbf a\mathbf a^H.
}
\]

Thus common phase changes neither the ordinary rank-one covariance nor relative DOA phase.

## Expected results / oracle

```text
relative electronic phase error     +10 deg on channel 2
physical channel-2 phase            -80 deg
inferred u with nominal model       0.4444444444444444
Delta u                             -0.0555555555555556
inferred theta                      26.3877999612 deg
angular bias                        -3.6122000388 deg
common phase example                +25 deg
common-phase covariance difference  exactly zero analytically
```

## Future regression oracle

```text
abs(u_hat - 4/9) < 1e-12
abs(theta_hat_deg - 26.3877999612) < 1e-9
||R_common_phase - R_nom||_F < 1e-12
```

## Scientific conclusion

Relative electronic phase error can bias nominal-manifold DOA even with perfect geometry. Common phase is a different equivalence class and cancels from ordinary covariance.

---

# GRP-016 — Mutual-Coupling Manifold Distortion

## Contract exercised

- cross-channel rather than diagonal mismatch;
- effective linear coupling specialization;
- nontrivial change in pairwise phase;
- nominal-manifold DOA consequence.

## Given

Use the normalized two-sensor steering seed

\[
\boxed{
\mathbf a
=\begin{bmatrix}1\\-j\end{bmatrix}
}
\]

corresponding to a half-wave array at `u0 = 0.5`.

Use the declared effective coupling matrix

\[
\boxed{
\mathbf C
=\begin{bmatrix}
1&0.5\\
0.5&1
\end{bmatrix}.
}
\]

This is intentionally a simple effective-manifold operator seed, not a universal electromagnetic coupling law.

## Coupled steering vector

\[
\mathbf b
=\mathbf C\mathbf a
=\begin{bmatrix}
1&0.5\\0.5&1
\end{bmatrix}
\begin{bmatrix}1\\-j\end{bmatrix}.
\]

Therefore

\[
\boxed{
\mathbf b
=\begin{bmatrix}
1-0.5j\\
0.5-j
\end{bmatrix}.
}
\]

## Relative coupled response

\[
\frac{b_2}{b_1}
=\frac{0.5-j}{1-0.5j}.
\]

Multiply numerator and denominator by `1+0.5j`:

\[
\frac{(0.5-j)(1+0.5j)}{1+0.25}
=\frac{1-0.75j}{1.25}
=0.8-0.6j.
\]

Thus

\[
\boxed{
\frac{b_2}{b_1}=0.8-0.6j.
}
\]

Its magnitude is exactly one:

\[
\sqrt{0.8^2+0.6^2}=1,
\]

and its phase is

\[
\boxed{
\angle(b_2/b_1)
=-\tan^{-1}(0.6/0.8)
=-36.8698976458^\circ.
}
\]

The nominal uncoupled phase difference was `-90 deg`.

## Nominal-model inferred direction cosine

For a nominal half-wave model,

\[
\angle(a_2/a_1)=-\pi u.
\]

Therefore fitting the coupled response with the nominal uncoupled model gives

\[
\boxed{
\hat u
=\frac{36.8698976458^\circ}{180^\circ}
=0.204832764699\ \text{(approximately)}.
}
\]

and

\[
\boxed{
\hat\theta
=\sin^{-1}(\hat u)
\approx11.8197094310^\circ.
}
\]

This example deliberately produces a large mismatch so the coupling effect is unambiguous by hand.

## Expected results / oracle

```text
b[0]                    1 - 0.5j
b[1]                    0.5 - 1j
b2/b1                   0.8 - 0.6j
|b2/b1|                 1
relative phase          -36.8698976458 deg
nominal phase           -90 deg
nominal inferred u      about 0.204832764699
nominal inferred theta  about 11.8197094310 deg
```

## Future regression oracle

```text
||b - [1-0.5j, 0.5-1j]||_2 < 1e-12
abs((b2/b1) - (0.8-0.6j)) < 1e-12
abs(relative_phase_deg + 36.8698976458) < 1e-9
abs(u_hat - 0.204832764699) < 1e-9
```

## Scientific conclusion

A cross-channel coupling operator can rotate the effective spatial response in a way that cannot be represented as independent channel phase offsets without losing its physical/operator semantics. Nominal uncoupled MUSIC can therefore suffer deterministic manifold mismatch.

---

# GRP-017 — Coupling to Covariance, Eigenspace, and MUSIC Leakage

## Contract exercised

- deterministic coupled manifold;
- rank-one covariance construction;
- isotropic white-noise eigenvalue shift;
- matched versus nominal subspace geometry;
- projective alignment;
- exact rank-one MUSIC leakage identity.

## Given

Use the GRP-016 coupled vector

\[
\mathbf b
=\begin{bmatrix}
1-0.5j\\
0.5-j
\end{bmatrix}
\]

and nominal vector

\[
\mathbf a
=\begin{bmatrix}1\\-j\end{bmatrix}.
\]

Assume a unit source variance and initially no additive noise.

## Coupled signal covariance

\[
\mathbf R_{\rm sig}
=\mathbf b\mathbf b^H.
\]

The diagonal entries are

\[
|1-0.5j|^2=1.25,
\qquad
|0.5-j|^2=1.25.
\]

The upper-right entry is

\[
(1-0.5j)(0.5+j)=1+0.75j.
\]

Therefore

\[
\boxed{
\mathbf R_{\rm sig}
=\begin{bmatrix}
1.25&1+0.75j\\
1-0.75j&1.25
\end{bmatrix}.
}
\]

Because `R_sig = b b^H` is rank one,

\[
\lambda_1=\|\mathbf b\|^2
=1.25+1.25
=2.5,
\]

and

\[
\lambda_2=0.
\]

Hence

\[
\boxed{\operatorname{eig}(R_{\rm sig})=\{2.5,0\}.}
\]

## Add unit white noise

Let

\[
\mathbf R_x
=\mathbf R_{\rm sig}+\mathbf I.
\]

Then each eigenvalue shifts by one while eigenvectors remain unchanged:

\[
\boxed{\operatorname{eig}(R_x)=\{3.5,1\}.}
\]

## Nominal/coupled projective alignment

First,

\[
\|\mathbf a\|^2=2,
\qquad
\|\mathbf b\|^2=2.5.
\]

Also

\[
\mathbf a^H\mathbf b
=\begin{bmatrix}1&j\end{bmatrix}
\begin{bmatrix}1-0.5j\\0.5-j\end{bmatrix}
=2.
\]

Therefore

\[
\rho^2
=\frac{|\mathbf a^H\mathbf b|^2}
{\|\mathbf a\|^2\|\mathbf b\|^2}
=\frac{4}{2(2.5)}
=0.8.
\]

Thus

\[
\boxed{\rho^2=0.8}
\]

and

\[
\boxed{1-\rho^2=0.2.}
\]

## Exact physical noise-subspace projector

Define the unit coupled signal vector

\[
\mathbf u=\frac{\mathbf b}{\sqrt{2.5}}.
\]

Then the physical rank-one noise projector is

\[
\mathbf P_n=\mathbf I-\mathbf u\mathbf u^H.
\]

Using `b b^H / 2.5`,

\[
\boxed{
\mathbf P_n
=\begin{bmatrix}
0.5&-0.4-0.3j\\
-0.4+0.3j&0.5
\end{bmatrix}.
}
\]

Let the unit nominal steering vector be

\[
\mathbf v=\frac{\mathbf a}{\sqrt 2}.
\]

Then

\[
\boxed{
\mathbf v^H\mathbf P_n\mathbf v
=1-|\mathbf u^H\mathbf v|^2
=1-\rho^2
=0.2.
}
\]

By contrast, the matched coupled vector gives

\[
\boxed{
\mathbf u^H\mathbf P_n\mathbf u=0.
}
\]

exactly in population arithmetic.

## Expected results / oracle

```text
R_sig = [[1.25, 1+0.75j],
         [1-0.75j, 1.25]]
signal covariance eigenvalues       {2.5, 0}
with I noise eigenvalues             {3.5, 1}
a^H b                                2
||a||^2                              2
||b||^2                              2.5
rho^2                                0.8
projective leakage                   0.2
nominal normalized MUSIC denominator 0.2
matched normalized denominator       0
```

## Future regression oracle

```text
||R_sig - expected_matrix||_F < 1e-12
sorted_eig(R_sig) == [0, 2.5] within 1e-12
sorted_eig(R_sig + I) == [1, 3.5] within 1e-12
abs(rho2 - 0.8) < 1e-12
abs(v^H Pn v - 0.2) < 1e-12
abs(u^H Pn u) < 1e-12
```

## Scientific conclusion

The coupling seed preserves rank one but rotates the physical signal subspace. Isotropic white noise shifts eigenvalues but not eigenvectors. A nominal uncoupled steering vector then has exact nonzero population MUSIC leakage `0.2`, while the matched coupled steering vector remains exactly orthogonal to the physical noise subspace.

---

# Supplemental Deterministic References

The following references extend Gate-E coverage without changing the reserved GRP numbering.

---

## ADR-003-SRC-01 — Physical Delay versus Later Sampling Sign

### Contract exercised

- physical/electrical delay sign;
- sample-time offset sign;
- phase is dimensionless/angular;
- distinct physical operations must not share one untyped parameter.

### Given

```text
f = 100 MHz
omega = 2 pi f
delta = +100 ps = 1.0e-10 s
x(t) = A exp(-j omega t)
```

### Physical waveform delay

\[
y(t)=x(t-\delta)
=x(t)e^{+j\omega\delta}.
\]

The phase is

\[
\omega\delta
=2\pi(10^8)(10^{-10})
=0.02\pi
=0.06283185307\ \mathrm{rad}
=+3.6^\circ.
\]

### Later sampling

\[
x(t+\delta)=x(t)e^{-j\omega\delta}
\]

so the phase is `-3.6 deg`.

### Expected results / oracle

```text
+100 ps physical delay at 100 MHz   +3.6 deg
+100 ps later sampling at 100 MHz   -3.6 deg
```

At `1 GHz`, the corresponding magnitudes are `36 deg`, preserving opposite signs.

**Status: PASS reference.**

---

## ADR-003-SRC-02 — SRO Fractional Period Error and Accumulated Epoch Drift

### Contract exercised

- sampling-rate error versus sampling-period error;
- exact reciprocal relation;
- time-accumulating drift.

### Given

```text
nominal fs = 10.0 MHz
actual fs,n = fs (1 + 10 ppm)
epsilon_f = +1.0e-5
nominal Ts = 1.0e-7 s
k = 10,000,000 nominal sample intervals
```

### Exact fractional period error

\[
1+\epsilon_T
=\frac{1}{1+10^{-5}},
\]

so

\[
\boxed{
\epsilon_T
=\frac{1}{1.00001}-1
=-9.999900001\times10^{-6}\ \text{approximately}.
}
\]

After `k=10,000,000` nominal intervals, the nominal epoch is

\[
kT_s=1\ \mathrm s.
\]

The actual channel epoch is

\[
1(1+\epsilon_T)
=0.9999900001\ \mathrm s.
\]

Thus the channel is early relative to nominal by approximately

\[
\boxed{-9.999900001\ \mu\mathrm s.}
\]

### Expected results / oracle

```text
epsilon_f                    +1.0e-5
epsilon_T                    about -9.999900001e-6
actual epoch after nominal 1 s  0.9999900001 s
epoch difference             about -9.999900001 us
```

**Status: PASS reference.**

---

## ADR-003-SRC-03 — Differential CFO Coherence Loss over a Finite Window

### Contract exercised

- differential CFO creates time-varying relative phase;
- finite-window covariance coherence reduction;
- common static phase and frequency drift are distinct.

### Given

Two channels have differential residual frequency

```text
Delta f = 1 Hz
observation duration T = 0.5 s
```

For continuous uniform averaging over `[0,T]`,

\[
\Gamma
=\frac{1}{T}\int_0^T e^{j2\pi\Delta f t}dt
=e^{j\pi\Delta f T}
\operatorname{sinc}(\Delta f T),
\]

where

\[
\operatorname{sinc}(x)=\frac{\sin(\pi x)}{\pi x}.
\]

With `Delta f T = 0.5`,

\[
|\Gamma|
=\frac{\sin(\pi/2)}{\pi/2}
=\frac{2}{\pi}
=0.6366197724.
\]

The phase factor is

\[
e^{j\pi/2}=j.
\]

Hence

\[
\boxed{
\Gamma=j\frac{2}{\pi}
}
\]

for this declared time origin.

### Expected results / oracle

```text
Delta f * T       0.5
|Gamma|           2/pi = 0.6366197724
arg(Gamma)        +90 deg for averaging over [0,T]
```

**Status: PASS reference.**

---

## ADR-003-SRC-04 — Ideal ADC Step, Quantization Noise, and SNR

### Contract exercised

- ADC input full-scale range;
- ideal code width;
- high-resolution additive quantization-noise approximation;
- ideal full-scale sine quantization SNR.

### Given

```text
N_b = 12 bits
V_min = -1 V
V_max = +1 V
V_FSR = 2 V
```

### Step size

\[
\boxed{
\Delta
=\frac{2}{4096}
=0.00048828125\ \mathrm V
=488.28125\ \mu\mathrm V.
}
\]

### Quantization-noise standard deviation

Under the declared high-resolution uniform-error approximation,

\[
\sigma_q
=\frac{\Delta}{\sqrt{12}}
=1.40954656\times10^{-4}\ \mathrm V
\approx140.954656\ \mu\mathrm V.
\]

### Ideal full-scale sine SNR

\[
\boxed{
\mathrm{SNR}_{q,\mathrm{dB}}
\approx6.02(12)+1.76
=74.00\ \mathrm{dB}.
}
\]

### Expected results / oracle

```text
Delta              488.28125 uV
sigma_q             about 140.954656 uV
ideal SNR_q         74.00 dB
```

This reference is invalid once clipping/overload or coarse-quantization assumptions invalidate the additive uniform model.

**Status: PASS reference.**

---

## ADR-003-SRC-05 — Stable DC Offset in an Uncentered Second Moment

### Contract exercised

- DC offset versus source mode;
- second moment versus centered covariance;
- rank-one offset contribution.

### Given

Let zero-mean measurement covariance be

\[
\mathbf R_x=\mathbf I_2
\]

and stable offset

\[
\mathbf d
=\begin{bmatrix}0.5\\0.5\end{bmatrix}.
\]

Then

\[
\mathbf d\mathbf d^H
=\begin{bmatrix}
0.25&0.25\\
0.25&0.25
\end{bmatrix}.
\]

The uncentered second moment is

\[
\boxed{
\mathbf R_y^{(2)}
=\mathbf I_2+\mathbf d\mathbf d^H
=\begin{bmatrix}
1.25&0.25\\
0.25&1.25
\end{bmatrix}.
}
\]

The rank-one offset term has eigenvalues `{0.5,0}`, so the total second moment has eigenvalues

\[
\boxed{\{1.5,1\}.}
\]

If the exact stable mean is removed before covariance formation, the offset term disappears and the centered covariance returns to `I_2` under the declared ideal assumptions.

**Status: PASS reference.**

---

## ADR-003-SRC-06 — Inverse Calibration and Noise Amplification

### Contract exercised

- model correction versus data correction;
- exact inverse limitation;
- singular values and noise amplification;
- correction changes covariance/noise.

### Given

Use a simple diagonal physical response

\[
\boxed{
\mathbf H
=\begin{bmatrix}
1&0\\
0&0.1
\end{bmatrix}
}
\]

with pre-correction white noise

\[
\mathbf R_n=\mathbf I_2.
\]

The exact inverse exists:

\[
\boxed{
\mathbf C=\mathbf H^{-1}
=\begin{bmatrix}
1&0\\0&10
\end{bmatrix}.
}
\]

The corrected noise covariance is

\[
\boxed{
\mathbf R_{n,\rm corr}
=\mathbf C\mathbf R_n\mathbf C^H
=\begin{bmatrix}
1&0\\0&100
\end{bmatrix}.
}
\]

The singular values of `H` are `{1,0.1}`:

```text
sigma_max = 1
sigma_min = 0.1
condition number = 10
```

The weak channel's noise variance is amplified by `10^2 = 100`.

**Status: PASS reference.**

---

## ADR-003-SRC-07 — Calibration-Grid Phase Gauge and Interpolation Failure

### Contract exercised

- pointwise projective equivalence versus grid-coherent gauge;
- direct measured/EM manifold interpolation;
- no destructive independent phase normalization across calibration nodes.

### Given

Suppose the true calibrated complex response is constant at two adjacent grid nodes:

\[
\mathbf a_0
=\begin{bmatrix}1\\1\end{bmatrix},
\qquad
\mathbf a_1
=\begin{bmatrix}1\\1\end{bmatrix}.
\]

Pointwise, multiplying the second node by an arbitrary common phase `-1=e^{j pi}` preserves its one-dimensional projective subspace:

\[
\mathbf a_1'
=-\mathbf a_1
=\begin{bmatrix}-1\\-1\end{bmatrix}.
\]

At either endpoint, `a_1` and `a_1'` are projectively equivalent.

But direct linear interpolation at the midpoint gives:

### Coherent gauge

\[
\frac{\mathbf a_0+\mathbf a_1}{2}
=\begin{bmatrix}1\\1\end{bmatrix}.
\]

### Arbitrarily flipped gauge

\[
\frac{\mathbf a_0+\mathbf a_1'}{2}
=\begin{bmatrix}0\\0\end{bmatrix}.
\]

Thus an arbitrary independent per-node phase gauge can destroy interpolated coherent response even though every endpoint is individually projectively equivalent.

### Expected result / oracle

```text
endpoint projective equivalence       true
coherent-gauge midpoint               [1, 1]^T
flipped-gauge midpoint                [0, 0]^T
interpolation invariance to arbitrary per-node gauge  false
```

**Status: PASS reference.**

---

## ADR-003-SRC-08 — Noncommuting Gain and Coupling Operators

### Contract exercised

- physical/operator ordering matters;
- matrix dimensions alone do not authorize reordering;
- diagonal gain and cross-channel coupling need not commute.

### Given

\[
\mathbf C
=\begin{bmatrix}
1&0.5\\
0.5&1
\end{bmatrix},
\qquad
\mathbf G
=\begin{bmatrix}
1&0\\
0&2
\end{bmatrix}.
\]

Then

\[
\boxed{
\mathbf C\mathbf G
=\begin{bmatrix}
1&1\\
0.5&2
\end{bmatrix}
}
\]

while

\[
\boxed{
\mathbf G\mathbf C
=\begin{bmatrix}
1&0.5\\
1&2
\end{bmatrix}.
}
\]

Therefore

\[
\boxed{\mathbf C\mathbf G\neq\mathbf G\mathbf C.}
\]

The difference is

\[
\boxed{
\mathbf C\mathbf G-\mathbf G\mathbf C
=\begin{bmatrix}
0&0.5\\
-0.5&0
\end{bmatrix}.
}
\]

**Status: PASS reference.**

---

# Coverage Matrix

| ADR-003 contract family | Canonical / supplemental evidence |
|---|---|
| Position error and physical geometry | GRP-014 |
| Stable phase reference / rigid translation | GRP-014 |
| Electronic relative phase mismatch | GRP-015 |
| Common-phase covariance invariance | GRP-015 |
| Cross-channel coupling | GRP-016 |
| Coupled covariance/eigenspace | GRP-017 |
| MUSIC projective leakage | GRP-017 |
| Physical delay versus sampling-time sign | ADR-003-SRC-01 |
| SRO exact/approximate relation and drift | ADR-003-SRC-02 |
| Differential CFO finite-window coherence | ADR-003-SRC-03 |
| ADC full scale / quantization approximation | ADR-003-SRC-04 |
| DC offset / uncentered second moment | ADR-003-SRC-05 |
| Calibration inverse / noise amplification | ADR-003-SRC-06 |
| Direct-manifold gauge/interpolation | ADR-003-SRC-07 |
| Operator ordering / noncommutativity | ADR-003-SRC-08 |

Element/polarization response, I/Q imbalance, nonlinear clipping, one-bit quantization, measured/CST provenance, physical port-state changes, and out-of-domain calibration are primarily boundary/profile semantics rather than compact canonical numerical identities. They are covered by ADR-003's governing contract and shall receive explicit Gate-F boundary/failure cases; future bounded implementation profiles may add dedicated reference problems when those capabilities become authoritative.

---

# Evidence Classification

The evidence in this file is classified as follows:

```text
GRP-014   analytical exact + bounded first-order angle approximation
GRP-015   analytical exact narrowband two-sensor specialization
GRP-016   deterministic linear-algebra reference
GRP-017   deterministic exact covariance/eigenspace/projector reference
SRC-01    exact tone-delay/sampling identity
SRC-02    exact reciprocal SRO relation + deterministic elapsed-time calculation
SRC-03    exact continuous-window coherence integral for declared window
SRC-04    ideal ADC arithmetic + explicitly approximate high-resolution noise/SNR model
SRC-05    exact second-moment identity under declared zero-mean assumptions
SRC-06    exact linear correction/noise covariance calculation
SRC-07    exact interpolation counterexample
SRC-08    exact matrix noncommutativity example
```

Approximate results are never labeled exact.

---

# Gate-E Candidate Conclusion

All canonical GRP-014 through GRP-017 calculations are manually reproducible and internally consistent with ADR-003, ADR-001, and ADR-002.

Supplemental deterministic references provide coverage for material timing, receiver/ADC, calibration, direct-manifold, and operator-ordering contracts without consuming the roadmap's reserved GRP numbering.

This file is candidate evidence. Formal Gate-E PASS is recorded separately by the ADR-003 Gate-E acceptance audit after cross-checking the reference values and coverage.
