# ADR-001 — Golden Reference Problems

- **Governing ADR:** `docs/adr/ADR-001-coordinate-direction-spatial-conventions.md`
- **Purpose:** Deterministic hand-computable evidence for ADR-001 Gate E
- **Status:** Reference set complete for GRP-001 through GRP-006
- **Role:** Learning artifact, analytical reference, and future software regression-test oracle

## 1. Common Scientific Conventions

Unless a problem explicitly overrides the phase reference, use the ADR-001 conventions:

- linear array axis: `+x`;
- canonical broadside reference in the `xy` slice: `+y`;
- positive angle rotates from `+y` toward `+x`;
- look direction in the canonical slice:

```math
\hat{\mathbf u}(\theta)
=
\begin{bmatrix}
\sin\theta\\
\cos\theta\\
0
\end{bmatrix};
```

- observable direction coordinate: `u = sin(theta)`;
- temporal phasor convention: `exp(-j omega t)`;
- receive geometry-only manifold:

```math
a_n
=
\exp\!\left[
-jk(\mathbf r_n-\mathbf r_{\mathrm{ref}})^T\hat{\mathbf u}
\right];
```

- `k = 2 pi/lambda = 2 pi f/v_p`;
- canonical internal physical units are SI;
- default analytical spatial phase reference is the centroid of the declared nominal geometry unless an explicit override is stated.

For GRP-001 through GRP-005 we deliberately declare

```text
propagation speed v_p = 3.0e8 m/s
frequency f = 1.0e9 Hz
```

so that hand arithmetic is simple:

```math
\lambda
=
\frac{v_p}{f}
=
0.3\ \mathrm{m},
```

```math
k
=
\frac{2\pi}{0.3}
\approx
20.943951\ \mathrm{rad/m},
```

and the carrier period is

```math
T=\frac{1}{f}=1\ \mathrm{ns}.
```

The value `3.0e8 m/s` is a declared model parameter for these reference problems. The problems do not rely on silently substituting an exact free-space constant.

---

# GRP-001 — Two-Sensor Propagation Distance and Relative Delay

## Problem

Consider two sensor phase-center/reference positions on the `x` axis:

```math
x_0=0,
\qquad
x_1=\frac{\lambda}{2}=0.15\ \mathrm{m}.
```

Use an explicit phase/delay reference at sensor 0:

```math
x_{\mathrm{ref}}=x_0=0.
```

Let the source look angle in the canonical `xy` slice be

```math
\theta=30^\circ=\frac{\pi}{6},
```

so that

```math
u=\sin\theta=\frac12.
```

Compute the plane-wave relative path difference and relative delay at sensor 1 with respect to sensor 0.

## Hand solution

The ADR-001 plane-wave relative-distance relation for a 1-D `x`-axis array is

```math
\Delta R_n
=
R_n-R_{\mathrm{ref}}
\approx
-(x_n-x_{\mathrm{ref}})u.
```

Therefore

```math
\Delta R_1
=
-(0.15)(0.5)
=
-0.075\ \mathrm{m}.
```

The negative sign means sensor 1 is closer in the plane-wave path-coordinate sense and therefore receives the incident waveform earlier than the reference sensor.

The relative delay is

```math
\Delta\tau_1
=
\frac{\Delta R_1}{v_p}
=
\frac{-0.075}{3.0\times10^8}
=
-2.5\times10^{-10}\ \mathrm{s}.
```

Hence

```math
\boxed{\Delta\tau_1=-0.25\ \mathrm{ns}}.
```

Since the carrier period is `1 ns`, the relative delay is

```math
\Delta\tau_1=-\frac{T}{4}.
```

## Expected result / future test oracle

```text
relative_path_difference_m = -0.075
relative_delay_s = -2.5e-10
relative_delay_ns = -0.25
```

A future implementation must reproduce the sign as well as the magnitude. Returning `+0.25 ns` under the declared conventions is a failure.

---

# GRP-002 — Two-Sensor Steering Vector and Phase-Reference Semantics

## Problem

Use the same two-sensor geometry and source from GRP-001:

```math
x_0=0,
\qquad
x_1=\frac{\lambda}{2},
\qquad
u=\frac12.
```

Compute the receive steering vector under:

1. the ADR-001 default geometry-centroid phase reference;
2. an explicit sensor-0 phase reference.

Show that the two vectors differ only by a common phase factor.

## Part A — Default centroid reference

The declared nominal geometry centroid is

```math
x_c
=
\frac{x_0+x_1}{2}
=
\frac{\lambda}{4}
=
0.075\ \mathrm{m}.
```

The receive coefficient is

```math
a_n
=
\exp[-jk(x_n-x_c)u].
```

For sensor 0:

```math
x_0-x_c=-\frac{\lambda}{4},
```

so

```math
-k(x_0-x_c)u
=
-\frac{2\pi}{\lambda}
\left(-\frac{\lambda}{4}\right)
\left(\frac12\right)
=
+\frac{\pi}{4}.
```

Thus

```math
a_0=e^{+j\pi/4}.
```

For sensor 1:

```math
x_1-x_c=+\frac{\lambda}{4},
```

so

```math
a_1=e^{-j\pi/4}.
```

Therefore the **default-reference steering vector** is

```math
\boxed{
\mathbf a_c
=
\begin{bmatrix}
e^{+j\pi/4}\\
e^{-j\pi/4}
\end{bmatrix}
=
\frac{1}{\sqrt2}
\begin{bmatrix}
1+j\\
1-j
\end{bmatrix}
}.
```

Numerically,

```text
a_c[0] = 0.70710678 + 0.70710678j
a_c[1] = 0.70710678 - 0.70710678j
```

## Part B — Explicit sensor-0 reference

Now select

```math
x_{\mathrm{ref}}=x_0=0.
```

Then

```math
a_0=1.
```

For sensor 1:

```math
-k(x_1-x_0)u
=
-\frac{2\pi}{\lambda}
\frac{\lambda}{2}
\frac12
=
-\frac{\pi}{2}.
```

Thus

```math
a_1=e^{-j\pi/2}=-j.
```

Therefore

```math
\boxed{
\mathbf a_0
=
\begin{bmatrix}
1\\
-j
\end{bmatrix}
}.
```

## Part C — Reference-change law

ADR-001 gives

```math
\mathbf a_{\mathrm{ref}'}
=
\exp\!\left[
+jk(x_{\mathrm{ref}'}-x_{\mathrm{ref}})u
\right]
\mathbf a_{\mathrm{ref}}.
```

Changing from centroid `x_c = lambda/4` to sensor 0 gives

```math
\alpha
=
\exp\!\left[
+jk\left(0-\frac{\lambda}{4}\right)\frac12
\right]
=
e^{-j\pi/4}.
```

Hence

```math
\mathbf a_0
=
e^{-j\pi/4}\mathbf a_c,
```

which indeed gives `[1, -j]^T`.

## Expected result / future test oracle

Default centroid reference:

```text
[e^(+j*pi/4), e^(-j*pi/4)]
```

Explicit sensor-0 reference:

```text
[1, -j]
```

Reference-change factor:

```text
exp(-j*pi/4)
```

A test must not incorrectly require `[1,-j]` when the configured phase reference is the geometry centroid.

---

# GRP-003 — Translation Invariance and Reference Change

## Problem

Use the GRP-002 two-sensor geometry with default centroid reference and `u = 1/2`.

### Case 1
Translate the physical geometry and its phase reference together by

```math
t=0.03\ \mathrm{m}=\frac{\lambda}{10}.
```

### Case 2
Translate the physical sensors by `t` but deliberately keep the old phase-reference coordinate fixed.

Determine the effect on the manifold.

## Case 1 — Geometry and reference translated together

Original coordinates:

```math
x_0=0,
\qquad
x_1=0.15,
\qquad
x_c=0.075\ \mathrm{m}.
```

Translated coordinates:

```math
x'_0=0.03,
\qquad
x'_1=0.18,
\qquad
x'_c=0.105\ \mathrm{m}.
```

For every sensor,

```math
x'_n-x'_c
=
(x_n+t)-(x_c+t)
=
x_n-x_c.
```

Therefore

```math
\boxed{\mathbf a'=\mathbf a_c}.
```

The numerical manifold remains

```math
\begin{bmatrix}
e^{+j\pi/4}\\
e^{-j\pi/4}
\end{bmatrix}.
```

## Case 2 — Sensors translated, old reference held fixed

ADR-001 gives

```math
\mathbf a'
=
\exp[-jktu]\mathbf a.
```

Here

```math
ktu
=
\frac{2\pi}{\lambda}
\left(\frac{\lambda}{10}\right)
\left(\frac12\right)
=
\frac{\pi}{10}.
```

Thus

```math
\boxed{
\mathbf a'
=
e^{-j\pi/10}\mathbf a_c
}.
```

This is a common phase factor, so all inter-channel phase differences remain unchanged.

## Expected result / future test oracle

```text
translate_geometry_and_reference_together:
    steering_vector unchanged exactly (within numerical tolerance)

translate_geometry_only_with_reference_fixed:
    steering_vector = exp(-j*pi/10) * original
    pairwise relative phase unchanged
```

This GRP protects the distinction between coordinate translation, physical geometry, and phase-reference semantics.

---

# GRP-004 — 3-D Projection Ambiguity of a 1-D Array

## Problem

Use the same ideal two-sensor `x`-axis geometry. Consider two different 3-D look directions:

```math
\hat{\mathbf u}_1
=
\begin{bmatrix}
1/2\\
\sqrt3/2\\
0
\end{bmatrix},
```

and

```math
\hat{\mathbf u}_2
=
\begin{bmatrix}
1/2\\
0\\
\sqrt3/2
\end{bmatrix}.
```

Show that the ideal 1-D geometry-only manifold cannot distinguish them.

## Hand solution

Both are unit vectors because

```math
\left(\frac12\right)^2
+
\left(\frac{\sqrt3}{2}\right)^2
=1.
```

They are physically different directions because

```math
\hat{\mathbf u}_1\neq\hat{\mathbf u}_2.
```

However, both have identical projection on the array axis:

```math
u_{x,1}=u_{x,2}=\frac12.
```

For a 1-D `x`-axis geometry,

```math
(\mathbf r_n-\mathbf r_{\mathrm{ref}})^T\hat{\mathbf u}
=
(x_n-x_{\mathrm{ref}})u_x.
```

Therefore

```math
\mathbf a(\hat{\mathbf u}_1)
=
\mathbf a(\hat{\mathbf u}_2).
```

Using the default centroid phase reference from GRP-002,

```math
\boxed{
\mathbf a(\hat{\mathbf u}_1)
=
\mathbf a(\hat{\mathbf u}_2)
=
\begin{bmatrix}
e^{+j\pi/4}\\
e^{-j\pi/4}
\end{bmatrix}
}.
```

The first direction lies in the canonical `xy` slice and corresponds to `theta = 30 deg`. The second direction does not lie in that slice, yet the ideal 1-D phase-only geometry sees the same `u_x`.

## Expected result / future test oracle

```text
u1 != u2 as 3-D vectors
u1_x == u2_x == 0.5
steering(u1) == steering(u2)
```

A future 1-D geometry-only implementation must not claim unique 3-D direction observability from these data.

---

# GRP-005 — Spatial Aliasing, Half-Wavelength Boundary, and Primitive Periodicity

This problem deliberately contains three subcases because ADR-001 distinguishes three related but different facts.

## GRP-005A — Grating ambiguity for `d = lambda`

Consider a two-sensor ULA with

```math
d=\lambda.
```

The declared-grid normalized spatial frequency is

```math
\psi
=
\frac{2\pi d}{\lambda}u
=2\pi u.
```

Choose

```math
u_1=0.25,
\qquad
u_2=-0.75.
```

Then

```math
\psi_1
=2\pi(0.25)
=\frac{\pi}{2},
```

while

```math
\psi_2
=2\pi(-0.75)
=-\frac{3\pi}{2}.
```

Their difference is

```math
\psi_2-\psi_1=-2\pi.
```

Thus integer-lattice samples have identical relative phase structure.

With the centroid phase reference, the steering vectors are

```math
\mathbf a(u_1)
=
\begin{bmatrix}
e^{+j\pi/4}\\
e^{-j\pi/4}
\end{bmatrix},
```

and

```math
\mathbf a(u_2)
=
-\mathbf a(u_1).
```

They are therefore not necessarily coordinate-by-coordinate identical under this reference, but they are exactly **common-phase equivalent** with common factor `-1`.

Hence

```math
\boxed{u_1=0.25\ \text{and}\ u_2=-0.75\ \text{are spatially aliased}.}
```

In the canonical angle slice,

```math
\theta_1=\arcsin(0.25)\approx14.4775^\circ,
```

```math
\theta_2=\arcsin(-0.75)\approx-48.5904^\circ.
```

## GRP-005B — Endpoint ambiguity at `d = lambda/2`

Now use

```math
d=\frac{\lambda}{2}.
```

At the two endfire endpoints,

```math
u_+=+1,
\qquad
u_-=-1.
```

Then

```math
\psi_+=+\pi,
\qquad
\psi_-=-\pi.
```

For integer lattice differences,

```math
e^{-jm\pi}=e^{+jm\pi}.
```

Therefore the two endfire endpoints are spatially equivalent.

With the two-sensor centroid reference,

```math
\mathbf a(+1)
=
\begin{bmatrix}
+j\\
-j
\end{bmatrix},
```

```math
\mathbf a(-1)
=
\begin{bmatrix}
-j\\
+j
\end{bmatrix}
=
-\mathbf a(+1).
```

Thus `d = lambda/2` is not strictly injective on the closed interval `u in [-1,1]`, even though it satisfies the usual no-grating-lobe condition for distinct directions in the open interval.

## GRP-005C — Declared-grid period versus primitive-grid period

Take declared integer indices

```math
m=[0,2,4]
```

on a declared spacing `Delta`.

Using anchor `m_0=0`,

```math
g=\gcd(2,4)=2.
```

Therefore the primitive spacing is

```math
\Delta_{\mathrm{prim}}=2\Delta.
```

The relative manifold in declared-grid frequency `psi` has fundamental period

```math
\boxed{
\Delta\psi_{\mathrm{fund}}
=
\frac{2\pi}{g}
=
\pi
}.
```

For example, with centroid lattice coordinate `mu_ref = 2`, the relative index offsets are

```math
[-2,0,+2].
```

Changing

```math
\psi\rightarrow\psi+\pi
```

multiplies each coefficient by

```math
e^{-j[-2,0,2]\pi}
=
[1,1,1],
```

so the manifold is unchanged.

If instead we use primitive indices

```math
\tilde m=[0,1,2],
```

and primitive normalized frequency

```math
\psi_{\mathrm{prim}}=2\psi,
```

the fundamental period becomes the familiar `2 pi`.

## Expected result / future test oracle

```text
GRP-005A:
    u1 = 0.25
    u2 = -0.75
    manifolds common-phase equivalent
    common factor with centroid reference = -1

GRP-005B:
    d = lambda/2
    u = +1 and -1 common-phase equivalent
    strict closed-interval injectivity = false

GRP-005C:
    m = [0,2,4]
    g = 2
    declared-grid fundamental period = pi
    primitive-grid fundamental period = 2*pi
```

---

# GRP-006 — Lattice Validation, Residuals, Primitive Reduction, and Difference Coarray

## Problem

Consider authoritative physical positions

```text
x = [
    0.0100000,
    0.0600002,
    0.2099998,
    0.3100001
] m
```

with a **declared design lattice**

```math
x_L=0.01\ \mathrm{m},
\qquad
\Delta=0.025\ \mathrm{m},
```

and candidate integer indices

```math
m=[0,2,8,12].
```

Use dimensionless lattice tolerance

```math
\tau_{\mathrm{lat}}=10^{-5}.
```

Determine:

1. normalized lattice coordinates and residuals;
2. physical residuals;
3. lattice PASS/FAIL;
4. primitive lattice;
5. ordered integer difference lags;
6. primitive difference lags.

## Step 1 — Normalized lattice coordinates

Compute

```math
z_n
=
\frac{x_n-x_L}{\Delta}.
```

This gives

```text
z = [
    0,
    2.000008,
    7.999992,
    12.000004
]
```

and after rounding,

```text
m = [0, 2, 8, 12].
```

The signed normalized residuals are

```math
\varepsilon_n=z_n-m_n,
```

hence

```text
epsilon = [
     0,
     8e-6,
    -8e-6,
     4e-6
]
```

and

```text
rho = abs(epsilon)
    = [0, 8e-6, 8e-6, 4e-6].
```

Therefore

```math
\max\rho_n=8\times10^{-6}<10^{-5}.
```

Thus

```math
\boxed{\text{declared lattice validation: PASS}}.
```

## Step 2 — Physical grid residuals

The signed physical residual is

```math
\eta_n=\varepsilon_n\Delta.
```

Since `Delta = 0.025 m`,

```text
eta_m = [
     0,
     2e-7,
    -2e-7,
     1e-7
] m
```

or

```text
eta_um = [0, +0.2, -0.2, +0.1] micrometers.
```

The allowed physical residual magnitude from the numerical lattice tolerance is

```math
\tau_{\mathrm{lat}}\Delta
=
10^{-5}(0.025)
=
2.5\times10^{-7}\ \mathrm{m}
=
0.25\ \mu\mathrm m.
```

Every residual lies within this numerical grid-alignment bound.

This bound is **not** a manufacturing tolerance or physical position uncertainty.

## Step 3 — Pair-difference residual bound

ADR-001 gives

```math
\left|
(x_i-x_j)-\ell_{ij}\Delta
\right|
\le
2\tau_{\mathrm{lat}}\Delta.
```

Here

```math
2\tau_{\mathrm{lat}}\Delta
=
2(10^{-5})(0.025)
=
5\times10^{-7}\ \mathrm{m}
=
0.5\ \mu\mathrm m.
```

This is the maximum pair-difference deviation implied by the admitted numerical lattice residuals.

## Step 4 — Primitive lattice

Using anchor `m_0=0`, the nonzero relative integer indices are

```text
[2, 8, 12].
```

Therefore

```math
g=\gcd(2,8,12)=2.
```

The primitive spacing is

```math
\boxed{
\Delta_{\mathrm{prim}}
=g\Delta
=2(0.025)
=0.05\ \mathrm{m}
}.
```

The primitive indices are

```math
\tilde m
=
\frac{m-m_0}{g}
=
[0,1,4,6].
```

The declared lattice `Delta = 0.025 m` remains provenance. It is not silently replaced by the derived primitive lattice.

## Step 5 — Ordered declared-grid difference lags

Using

```math
\ell_{ij}=m_i-m_j,
```

the ordered lag matrix is

```text
L_declared =
[[  0,  -2,  -8, -12],
 [  2,   0,  -6, -10],
 [  8,   6,   0,  -4],
 [ 12,  10,   4,   0]]
```

The unique declared-grid lags are

```text
[-12, -10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10, 12].
```

Each declared-grid lag unit corresponds to `0.025 m` in the reconstructed grid model.

## Step 6 — Ordered primitive difference lags

Using primitive indices

```text
[0,1,4,6]
```

the primitive lag matrix is

```text
L_primitive =
[[ 0, -1, -4, -6],
 [ 1,  0, -3, -5],
 [ 4,  3,  0, -2],
 [ 6,  5,  2,  0]]
```

The unique primitive lags are

```text
[-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6].
```

The physical grid-model difference represented by either convention is the same because

```math
\ell_{\mathrm{declared}}\Delta
=
\ell_{\mathrm{primitive}}\Delta_{\mathrm{prim}}.
```

For example,

```math
12(0.025)=6(0.05)=0.30\ \mathrm{m}.
```

## Expected result / future test oracle

```text
lattice_valid = true
max_abs_normalized_residual = 8e-6
physical_residual_um = [0.0, 0.2, -0.2, 0.1]
pair_difference_residual_bound_m = 5e-7

g = 2
declared_spacing_m = 0.025
primitive_spacing_m = 0.05
primitive_indices = [0,1,4,6]

unique_declared_lags = [-12,-10,-8,-6,-4,-2,0,2,4,6,8,10,12]
unique_primitive_lags = [-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6]
```

A future implementation fails this reference if it silently snaps the authoritative `x` values to reconstructed grid coordinates, discards the residuals, replaces the declared lattice with the primitive lattice, or creates integer lags before lattice validation.

---

# 8. Gate-E Coverage Matrix

| ADR-001 contract | Reference evidence |
|---|---|
| relative path and delay sign | GRP-001 |
| temporal-to-spatial phase sign | GRP-001, GRP-002 |
| centroid default phase reference | GRP-002 |
| explicit phase-reference override | GRP-002, GRP-003 |
| common-phase reference equivalence | GRP-002, GRP-003 |
| translation invariance | GRP-003 |
| 1-D geometry in 3-D propagation space | GRP-004 |
| projection ambiguity | GRP-004 |
| direction cosine semantics | GRP-001, GRP-004, GRP-005 |
| spatial aliasing | GRP-005A |
| half-wavelength closed-endpoint ambiguity | GRP-005B |
| declared versus primitive periodicity | GRP-005C, GRP-006 |
| lattice tolerance and normalized residual | GRP-006 |
| normalized versus physical lattice residual | GRP-006 |
| primitive lattice reduction | GRP-006 |
| integer coarray lag validity | GRP-006 |
| preservation of declared-lattice provenance | GRP-006 |

## 9. Acceptance Statement

GRP-001 through GRP-006 provide deterministic, manually inspectable evidence for every material core contract assigned to ADR-001 Gate E.

These results are **analytical reference expectations**, not yet claims that an implementation passes them. During Phase 1, the same values shall become unit/property/regression test oracles for the scientific core.
