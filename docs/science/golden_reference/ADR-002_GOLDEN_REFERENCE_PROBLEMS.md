# ADR-002 — Golden Reference Problems

- **Governing ADR:** `../../adr/ADR-002-wave-propagation-signal-measurement-model.md`
- **Phase:** 0C — Scientific Foundations
- **Gate:** E — Hand-Calculated Reference Evidence
- **Status:** Complete — candidate evidence for Gate E PASS

## 1. Purpose

These deterministic reference problems provide hand-computable analytical evidence for ADR-002. Each problem is simultaneously:

1. a learning/interpretation example;
2. a scientific reference calculation;
3. a future Phase 1 software regression-test oracle.

The canonical roadmap already reserves GRP-007 through GRP-013 for ADR-002. Additional ADR-002 evidence developed during exploration is recorded here as `ADR-002-SRC-01` through `ADR-002-SRC-05` so that the existing GRP-014 through GRP-018 assignments for ADR-003/ADR-004 are not renumbered.

Unless otherwise stated, simple electromagnetic-style examples use `v = 3.0e8 m/s` purely to keep arithmetic transparent. This is a declared reference-model choice, not a universal propagation-speed assumption for GeoDOA.

---

## GRP-007 — Far-Field Curvature Error

### Contract exercised

- exact spherical path length;
- first/second-order plane-wave approximation;
- phase-curvature error;
- Fraunhofer distance as a diagnostic scale rather than an exact boundary.

### Given

Three sensors on the `x` axis:

```text
x = [-0.15, 0, +0.15] m
D = 0.30 m
f = 1.0 GHz
v = 3.0e8 m/s
lambda = 0.30 m
k = 2 pi / lambda = 20.9439510239 rad/m
```

A source is exactly broadside (`u = 0`) at center-reference range

```text
R_ref = 0.60 m.
```

### Exact outer-sensor path

```math
R_1
=
\sqrt{0.60^2+0.15^2}
=
\sqrt{0.3825}
=
0.6184658438\ \mathrm m.
```

Therefore

```math
\Delta R_{\mathrm{exact}}
=
R_1-R_{\mathrm{ref}}
=
0.0184658438\ \mathrm m.
```

The first-order broadside plane-wave prediction is zero relative path, hence

```text
plane-wave path error = 18.4658438 mm.
```

### Exact phase error

```math
\delta\phi
=
k\Delta R
=
0.3867477\ \mathrm{rad}
\approx
22.16^\circ.
```

### Second-order approximation

At broadside,

```math
\Delta R^{(2)}
\approx
\frac{x^2}{2R}
=
\frac{0.15^2}{2(0.60)}
=
0.01875\ \mathrm m.
```

Thus

```math
k\Delta R^{(2)}
=
0.3926991\ \mathrm{rad}
=
22.5^\circ.
```

### Fraunhofer scale

```math
R_F
=
\frac{2D^2}{\lambda}
=
\frac{2(0.30)^2}{0.30}
=
0.60\ \mathrm m.
```

Thus this example sits at `R = R_F` while retaining roughly `22.2 deg` of exact outer-sensor phase curvature.

### Expected results / oracle

```text
outer exact range          0.6184658438 m
outer relative path        0.0184658438 m
exact phase mismatch       about 0.38675 rad
second-order path          0.01875 m
second-order phase         pi/8 = 0.3926990817 rad
Fraunhofer scale           0.60 m
```

### Scientific conclusion

`R = R_F` does not mean zero plane-wave error. The Fraunhofer formula is a reference scale; compatibility should be expressed through an explicit error metric and acceptance policy.

---

## GRP-008 — Narrowband Bandwidth-Delay Diagnostic

### Contract exercised

- aperture delay spread;
- array narrowband metric;
- fractional bandwidth versus electrical aperture.

### Given

```text
f_c = 3 GHz
v   = 3.0e8 m/s
lambda_c = 0.10 m
D   = 1.0 m = 10 lambda_c
B   = 30 MHz (declared full two-sided occupied width)
nu_max = B/2 = 15 MHz
u direction = endfire, |u| = 1
```

### Aperture delay

```math
\Delta\tau_{\mathrm{ap}}
=
\frac{D}{v}
=
3.333333333\ \mathrm{ns}.
```

### Bandwidth-delay metrics

```math
B\Delta\tau_{\mathrm{ap}}
=
0.10.
```

```math
\eta_{\mathrm{NB}}
=
2\pi\nu_{\max}\Delta\tau_{\mathrm{ap}}
=
0.3141592654\ \mathrm{rad}
=
18^\circ.
```

The exact edge-component multiplicative error incurred by replacing the delayed envelope factor by unity has magnitude

```math
|e^{j\eta}-1|
=
2|\sin(\eta/2)|
\approx
0.31287.
```

### Expected results / oracle

```text
fractional bandwidth       0.01 = 1%
electrical aperture        10 wavelengths
aperture delay             3.333333333 ns
B * delay                  0.10
edge spectral phase        pi/10 = 0.3141592654 rad = 18 deg
```

### Scientific conclusion

A `1%` fractional bandwidth is not sufficient by itself to establish array-narrowband compatibility. Electrical projected aperture matters.

---

## GRP-009 — FMCW Beat Frequency and Range

### Contract exercised

- chirp slope units;
- dechirp convention;
- scientific signed beat frequency versus standard FFT coordinate;
- stationary monostatic range recovery.

### Given

```text
B   = 150 MHz
T_c = 50 us
mu  = B/T_c = 3.0e12 Hz/s
R   = 30 m
v   = 3.0e8 m/s
mixer = y = s_rx * conj(s_tx)
positive up-chirp: mu > 0
```

### Round-trip delay

```math
\tau
=
\frac{2R}{v}
=
200\ \mathrm{ns}.
```

### Beat frequency

Under the GeoDOA scientific `exp(-j2 pi f t)` convention,

```math
f_{b,\mathrm{sci}}
=
-\mu\tau
=
-600\ \mathrm{kHz}.
```

For the resulting sampled exponential, the standard forward NumPy/MATLAB FFT coordinate places the peak at

```text
+600 kHz.
```

### Range recovery

```math
R
=
\frac{v|f_b|}{2|\mu|}
=
30\ \mathrm m.
```

Ideal range resolution:

```math
\Delta R
=
\frac{v}{2B}
=
1\ \mathrm m.
```

### Expected results / oracle

```text
chirp slope                3.0e12 Hz/s
round-trip delay           200 ns
scientific beat frequency  -600 kHz
standard FFT coordinate    +600 kHz
recovered range            30 m
ideal range resolution     1 m
```

### Scientific conclusion

Scientific signed frequency, dechirp/mixer ordering, chirp-slope sign, and software FFT coordinate must remain explicit and separately testable.

---

## GRP-010 — Tiny FMCW Data Cube to Range-Selected Snapshot Matrix and Covariance

### Contract exercised

- raw measurement tensor versus spatial snapshot matrix;
- explicit FFT/bin-selection transformation;
- scientific axis semantics;
- known-zero-mean versus estimated-mean covariance normalization.

### Given

A synthetic cube has shape

```text
[channel, chirp, fast_time] = [2, 2, 4].
```

Let the fast-time sequence be

```math
\mathbf q=[1,\ j,\ -1,\ -j],
```

which is a standard forward-DFT bin-1 complex exponential. Use normalized FFT output (`1/N_FFT`) after the forward DFT so selected-bin amplitude is unity.

Let spatial steering and chirp coefficients be

```math
\mathbf a
=
\begin{bmatrix}1\\-j\end{bmatrix},
\qquad
s[1]=1,
\qquad
s[2]=-1.
```

Construct raw chirps as `a q` and `-a q`.

### Explicit processing

After fast-time FFT and explicit selection of bin `k = 1`, the spatial snapshot matrix is

```math
\mathbf X_r
=
\begin{bmatrix}
1 & -1\\
-j & j
\end{bmatrix}.
```

The sample mean is exactly zero.

### Known-zero-mean second-moment estimate

```math
\hat{\mathbf R}_0
=
\frac12\mathbf X_r\mathbf X_r^H
=
\begin{bmatrix}
1 & j\\
-j & 1
\end{bmatrix}.
```

### Estimated-mean centered estimator

Because `L = 2`, `L-1 = 1`. With the same numerically zero sample mean,

```math
\hat{\mathbf R}_c
=
\frac1{L-1}\mathbf X_c\mathbf X_c^H
=
\begin{bmatrix}
2 & 2j\\
-2j & 2
\end{bmatrix}.
```

### Expected results / oracle

```text
raw cube shape             (2, 2, 4)
selected snapshot shape    (2, 2)
X_r                        [[1,-1],[-j,j]]
known-zero estimate        [[1,j],[-j,1]]
estimated-mean estimate    [[2,2j],[-2j,2]]
```

### Scientific conclusion

A raw cube is not a spatial snapshot matrix by shape. Also, `1/L` and `1/(L-1)` represent distinct estimator conventions even when the observed sample mean happens to be zero.

---

## GRP-011 — 2x2 Covariance Eigendecomposition

### Contract exercised

- population covariance construction;
- white-noise eigenstructure;
- eigenvalue/eigenvector interpretation.

### Given

```math
\mathbf a=\begin{bmatrix}1\\1\end{bmatrix},
\qquad
P_s=2,
\qquad
\sigma^2=1.
```

Then

```math
\mathbf R_x
=
P_s\mathbf a\mathbf a^H+\sigma^2\mathbf I
=
\begin{bmatrix}3&2\\2&3\end{bmatrix}.
```

### Eigendecomposition

The characteristic polynomial is

```math
(3-\lambda)^2-4=0,
```

so

```math
\lambda_1=5,
\qquad
\lambda_2=1.
```

Normalized eigenvectors may be chosen as

```math
\mathbf u_s
=
\frac1{\sqrt2}\begin{bmatrix}1\\1\end{bmatrix},
\qquad
\mathbf u_n
=
\frac1{\sqrt2}\begin{bmatrix}1\\-1\end{bmatrix}.
```

### Expected results / oracle

```text
R_x                         [[3,2],[2,3]]
eigenvalues                 [5,1]
signal eigenvector          [1,1]/sqrt(2)
noise eigenvector           [1,-1]/sqrt(2)
```

---

## GRP-012 — MUSIC Noise-Subspace Orthogonality

### Contract exercised

- classical white-noise MUSIC subspace relation;
- true-manifold orthogonality;
- pseudospectrum interpretation under the declared unnormalized steering convention.

Use GRP-011's noise eigenvector

```math
\mathbf u_n
=
\frac1{\sqrt2}\begin{bmatrix}1\\-1\end{bmatrix}.
```

For the true steering vector

```math
\mathbf a_{\mathrm{true}}
=
\begin{bmatrix}1\\1\end{bmatrix},
```

```math
\mathbf u_n^H\mathbf a_{\mathrm{true}}=0.
```

Therefore

```math
\mathbf a_{\mathrm{true}}^H
\mathbf u_n\mathbf u_n^H
\mathbf a_{\mathrm{true}}=0,
```

and the ideal mathematical MUSIC pseudospectrum has a singular/infinite peak at the true steering vector.

For the false candidate

```math
\mathbf a_f
=
\begin{bmatrix}1\\-j\end{bmatrix},
```

```math
\mathbf u_n^H\mathbf a_f
=
\frac{1+j}{\sqrt2},
```

so

```math
|\mathbf u_n^H\mathbf a_f|^2=1
```

and under this unnormalized steering convention the pseudospectrum value is `1`.

### Expected results / oracle

```text
true noise-subspace projection    0
false projection magnitude^2      1
```

---

## GRP-013 — Mean-Centered Sample-Covariance Rank Ceiling

### Contract exercised

- estimated sample mean;
- `1/(L-1)` centered covariance construction;
- rank ceiling `min(N,L-1)`.

### Given

```math
N=3,\qquad L=2,
```

```math
\mathbf x_1
=
\begin{bmatrix}1\\0\\1\end{bmatrix},
\qquad
\mathbf x_2
=
\begin{bmatrix}0\\1\\1\end{bmatrix}.
```

Sample mean:

```math
\bar{\mathbf x}
=
\begin{bmatrix}0.5\\0.5\\1\end{bmatrix}.
```

Centered snapshots:

```math
\mathbf c_1
=
\begin{bmatrix}0.5\\-0.5\\0\end{bmatrix},
\qquad
\mathbf c_2=-\mathbf c_1.
```

Thus `rank(X_c) = 1`.

The centered sample covariance is

```math
\hat{\mathbf R}
=
\begin{bmatrix}
0.5 & -0.5 & 0\\
-0.5 & 0.5 & 0\\
0 & 0 & 0
\end{bmatrix}.
```

Its eigenvalues are

```text
1, 0, 0
```

so

```math
\operatorname{rank}(\hat{\mathbf R})=1
=
\min(3,2-1).
```

### Expected results / oracle

```text
sample mean                [0.5,0.5,1]
centered rank              1
sample covariance          [[0.5,-0.5,0],[-0.5,0.5,0],[0,0,0]]
eigenvalues                [1,0,0]
rank                       1
```

---

## ADR-002-SRC-01 — Doppler Sign Reference

### Given

```text
f_c = 10 GHz
v = 3.0e8 m/s
lambda = 0.03 m
monostatic range rate dot(R) = -15 m/s (approaching)
```

Under ADR-002,

```math
f_D=-\frac{2\dot R}{\lambda}
=+1000\ \mathrm{Hz}.
```

The scientific positive-Doppler complex exponential is therefore

```math
e^{-j2\pi(1000)t}.
```

Under the standard forward FFT coordinate, this appears at `-1000 Hz`.

### Oracle

```text
scientific Doppler         +1000 Hz
standard FFT coordinate    -1000 Hz
```

---

## ADR-002-SRC-02 — Complex Noise and SNR Scaling

### Given

```text
P_s = 2
SNR = 13 dB
```

Linear ratio:

```math
\rho=10^{13/10}=19.95262315\ldots
```

Per-channel complex noise variance:

```math
\sigma_n^2
=
\frac{2}{\rho}
\approx
0.10023745.
```

Circular complex Gaussian real/imaginary component variance:

```math
\sigma_I^2=\sigma_Q^2=\frac{\sigma_n^2}{2}
\approx
0.05011872.
```

Component standard deviation:

```math
\sigma_I=\sigma_Q\approx0.2238721.
```

### Oracle

```text
linear SNR                  about 19.952623
complex variance            about 0.10023745
I/Q variance                about 0.05011872
I/Q std                     about 0.2238721
```

---

## ADR-002-SRC-03 — Perfectly Coherent Two-Arrival Rank Collapse

### Given

```math
s_2=2e^{j\pi/3}s_1,
\qquad
\mathbb E|s_1|^2=1.
```

Define

```math
\mathbf c
=
\begin{bmatrix}1\\2e^{j\pi/3}\end{bmatrix}.
```

Then

```math
\mathbf R_s
=
\mathbf c\mathbf c^H
=
\begin{bmatrix}
1 & 1-j\sqrt3\\
1+j\sqrt3 & 4
\end{bmatrix}.
```

Its determinant is zero and trace is five, so eigenvalues are

```text
5, 0
```

and

```math
\operatorname{rank}(\mathbf R_s)=1
```

although `Q_arr = 2`.

### Oracle

```text
determinant                 0
eigenvalues                 [5,0]
rank                        1
arrival count               2
```

---

## ADR-002-SRC-04 — General Bistatic Versus Virtual-Sum Geometry

### Given

```text
Delta x_Tx = 0.10 m
Delta x_Rx = 0.20 m
```

### Common-look case

With

```text
u_Tx = u_Rx = 0.5
```

```math
\Delta\mathcal P
=-(0.10)(0.5)-(0.20)(0.5)
=-0.15\ \mathrm m.
```

The virtual displacement is `0.30 m`, and

```math
-(0.30)(0.5)=-0.15\ \mathrm m.
```

Thus virtual-sum geometry reproduces the physical two-leg first-order path in the common-look specialization.

### General bistatic case

With

```text
u_Tx = +0.5
u_Rx = -0.25
```

```math
\Delta\mathcal P
=-(0.10)(0.5)-(0.20)(-0.25)
=0.
```

A single coordinate sum `0.30 m` does not encode this result without the two separate look directions.

### Oracle

```text
common-look physical path difference      -0.15 m
common-look virtual-sum result             -0.15 m
general bistatic physical path difference   0 m
```

### Scientific conclusion

`r_v = r_Tx + r_Rx` is a common-look/colocated far-field specialization, not a universal bistatic rule.

---

## ADR-002-SRC-05 — Nondispersive Phase and Group Delay

### Given

```text
v = 2.0e8 m/s
f = 1.0 GHz
R = 0.4 m
```

Then

```math
\lambda=\frac{v}{f}=0.2\ \mathrm m,
```

```math
\beta=\frac{2\pi}{\lambda}=10\pi\ \mathrm{rad/m},
```

and

```math
\tau=\frac{R}{v}=2\ \mathrm{ns}.
```

Propagation carrier phase is

```math
\beta R=4\pi,
```

so the wrapped complex phase factor is unity even though physical delay is `2 ns`.

For a nondispersive medium,

```math
\beta(\omega)=\frac{\omega}{v},
\qquad
\frac{d\beta}{d\omega}=\frac1v,
```

so

```math
\tau_g
=R\frac{d\beta}{d\omega}
=2\ \mathrm{ns}.
```

### Oracle

```text
lambda                       0.2 m
beta                         10 pi rad/m
absolute delay               2 ns
wrapped carrier phase        1 + 0j
group delay                  2 ns
v_phase = v_group            2.0e8 m/s
```

### Scientific conclusion

Wrapped single-frequency phase does not determine absolute propagation delay. In the nondispersive baseline, phase and group velocities coincide.

---

## 2. Gate-E Coverage Summary

| Contract | Reference evidence |
|---|---|
| spherical versus plane wave | GRP-007 |
| phase-error/Fraunhofer interpretation | GRP-007 |
| narrowband aperture delay | GRP-008 |
| fractional bandwidth × electrical aperture | GRP-008 |
| FMCW sign/range | GRP-009 |
| scientific frequency versus FFT coordinate | GRP-009, SRC-01 |
| raw tensor -> spatial snapshots | GRP-010 |
| covariance normalization semantics | GRP-010 |
| population covariance eigensystem | GRP-011 |
| MUSIC orthogonality | GRP-012 |
| centered sample-covariance rank ceiling | GRP-013 |
| Doppler sign | SRC-01 |
| complex-noise/SNR scaling | SRC-02 |
| coherent-arrival rank collapse | SRC-03 |
| general bistatic/common-look MIMO | SRC-04 |
| phase/group delay consistency | SRC-05 |

## 3. Future Software-Test Principle

These references are not only scalar-number oracles. They also define semantic regression requirements. Examples include:

- GRP-007: changing spatial phase reference must not change the reference-invariant pairwise plane-wave compatibility result;
- GRP-009/SRC-01: scientific signed frequency and standard FFT coordinates must not be silently equated;
- GRP-010: a raw tensor shall not become a snapshot matrix merely because its shape is compatible;
- SRC-03: arrival count shall not be inferred from covariance rank;
- SRC-04: arbitrary bistatic channels shall not be assigned a fabricated common-look virtual coordinate.

Gate E evidence is therefore both numerical and semantic.
