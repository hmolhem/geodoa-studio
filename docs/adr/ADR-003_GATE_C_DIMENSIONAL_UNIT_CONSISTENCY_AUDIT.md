# ADR-003 — Gate C Dimensional and Unit Consistency Audit

- **ADR:** `ADR-003-sensor-imperfections-mutual-coupling-calibration.md`
- **Phase:** 0C — Scientific Foundations
- **Gate:** C — Dimensional and Unit Consistency
- **Status:** PASS
- **Prior gates:** Gate A PASS, Gate B PASS
- **Acceptance status:** ADR-003 remains NOT ACCEPTED

> This audit verifies dimensional homogeneity, SI-unit semantics, dimensionless arguments, covariance/eigenspace units, ADC quantities, dB usage, and unit-sensitive calibration/regularization statements. It does not constitute Gate D, E, or F evidence.

---

## 1. Audit question

Are the physical quantities and mathematical expressions in ADR-003 dimensionally homogeneous, with unit-bearing quantities, dimensionless ratios, logarithmic quantities, normalized manifolds, covariance units, and unit-sensitive operators distinguished sufficiently to support an engineering implementation without silent unit inference?

---

## 2. Governing unit policy

ADR-003 inherits ADR-001/ADR-002 physical-unit policy and adds the following Gate-C interpretation:

1. physical positions and path lengths are authoritative in SI meters;
2. physical delays, sample-time offsets, and jitter are authoritative in seconds;
3. ordinary frequency is in hertz and angular frequency in radians per second;
4. wavenumber is in radians per meter;
5. radians are SI-dimensionless but shall remain semantically labeled as angular quantities;
6. sensor/operator coefficients may be dimensionless or unit-bearing depending on their declared input/output reference planes;
7. matrix shape alone never establishes unit compatibility;
8. covariance entries carry the product units of the corresponding channel quantities;
9. logarithms and dB conversions apply only to dimensionless ratios with a declared reference;
10. any normalization that changes physical units or scale must be explicit and provenance-preserving.

---

## 3. Spatial manifold and geometry — PASS

The inherited receive phase is

\[
\exp\!\left[-jk(\mathbf r_n-\mathbf r_{\rm ref})^T\hat{\mathbf u}\right].
\]

Units are

\[
[k]=\mathrm{rad/m},
\qquad
[\mathbf r]=\mathrm m,
\qquad
[\hat{\mathbf u}]=1.
\]

Therefore

\[
[k\,\mathbf r^T\hat{\mathbf u}]=\mathrm{rad},
\]

and the exponential argument is dimensionless in the SI sense.

**Result: PASS.**

The same dimensional structure holds for

\[
\delta\phi_n^{(\mathrm{fixed\ ref})}
=-k\hat{\mathbf u}^T\boldsymbol\varepsilon_n
\]

and

\[
\delta\phi_{nm}
=-k(\boldsymbol\varepsilon_n-\boldsymbol\varepsilon_m)^T\hat{\mathbf u},
\]

because position errors are in meters and phase errors are in radians.

---

## 4. Exact path perturbation — PASS

\[
\delta R_n
=\|\mathbf r_s-\mathbf r_n^{\rm phys}\|
-\|\mathbf r_s-\mathbf r_n^{\rm nom}\|
\]

has units of meters.

No normalized wavelength or direction-cosine quantity is silently substituted for physical position.

**Result: PASS.**

---

## 5. Angle and direction-cosine semantics — PASS

The direction vector and direction cosine are dimensionless.

Angular quantities such as

\[
\theta,\phi,\delta\phi
\]

are semantically radians unless an explicit presentation conversion to degrees is declared.

For small-angle conversions such as

\[
\Delta\theta\approx(\delta d/d)\tan\theta_0,
\]

`delta d/d` and `tan(theta_0)` are dimensionless and `Delta theta` is an angular quantity in radians.

**Result: PASS.**

---

## 6. Gain and element-response units — PASS WITH TYPED-PLANE RULE

For a same-quantity electronic channel mapping, a voltage or complex-envelope gain

\[
g_n=\rho_ne^{j\phi_n}
\]

is a dimensionless ratio such as V/V.

However, ADR-003's more general typed operator graph may cross reference planes with different physical quantities. For example, an element/open-circuit operator can map incident electric field in V/m to an open-circuit voltage in V, in which case an effective response can carry dimensions of length.

Therefore:

\[
\boxed{\text{not every sensor/operator coefficient is universally dimensionless}.}
\]

The operator's units are determined by its declared input and output reference planes and normalization.

This interpretation is consistent with the ADR's reference-plane and direct-manifold provenance rules.

**Result: PASS.**

---

## 7. Multiport/network units — PASS

For the declared Thevenin specialization:

\[
[\mathbf Z_A]=[\mathbf Z_L]=\Omega,
\qquad
[\mathbf v_{\rm oc}]=\mathrm V.
\]

Then

\[
[(\mathbf Z_A+\mathbf Z_L)^{-1}]=\Omega^{-1}
\]

and

\[
\mathbf i=(\mathbf Z_A+\mathbf Z_L)^{-1}\mathbf v_{\rm oc}
\]

has units A.

Likewise,

\[
\mathbf T_L
=\mathbf Z_L(\mathbf Z_A+\mathbf Z_L)^{-1}
\]

is dimensionless, and

\[
\mathbf v_L=\mathbf T_L\mathbf v_{\rm oc}
\]

has units V.

Scattering parameters are dimensionless normalized wave ratios, while impedance matrices carry ohms. This further supports ADR-003's prohibition on treating `S21`, `Z`, `T_L`, and an effective manifold `C` as interchangeable merely because all are matrices.

**Result: PASS.**

---

## 8. Delay and phase-slope units — PASS

For

\[
H_\tau(\omega)=e^{j\omega\delta\tau},
\]

\[
[\omega]=\mathrm{rad/s},
\qquad
[\delta\tau]=\mathrm s,
\]

so the exponent is radians/dimensionless.

For

\[
\frac{d\phi}{d\omega}=\delta\tau,
\]

the left-hand side has units

\[
\frac{\mathrm{rad}}{\mathrm{rad/s}}=\mathrm s.
\]

**Result: PASS.**

---

## 9. Sampling-time model — PASS

\[
t_n[k]
=t_0+\beta_n+kT_s(1+\epsilon_{T,n})+\eta_n[k].
\]

The terms satisfy

```text
t_n[k]       seconds
 t_0          seconds
 beta_n       seconds
 k            dimensionless integer index
 T_s          seconds
 epsilon_T,n  dimensionless fractional period error
 eta_n[k]     seconds
```

so every additive term has units seconds.

The exact relation

\[
1+\epsilon_{T,n}=\frac{1}{1+\epsilon_{f,n}}
\]

requires both fractional errors to be dimensionless.

**Result: PASS.**

---

## 10. Frequency-offset relation — PASS

\[
\delta f_n(t)
=\frac{1}{2\pi}\frac{d\psi_n}{dt}.
\]

With phase in radians and time in seconds,

\[
[d\psi/dt]=\mathrm{rad/s}.
\]

Division by one cycle `2 pi rad` gives cycles/s, i.e. hertz.

The project shall not numerically mix hertz with radians per second without an explicit `2 pi` conversion.

**Result: PASS.**

---

## 11. Receiver noise and covariance units — PASS

If a channel vector `x` carries units `U`, then

\[
\mathbf R_x=E[\mathbf x\mathbf x^H]
\]

carries units `U^2` for same-unit channels.

More generally, covariance entry `(m,n)` carries the product units of channel `m` and channel `n`.

For a dimensionless same-plane gain/coupling matrix `H`,

\[
\mathbf H\mathbf R_x\mathbf H^H
\]

retains covariance units.

For a unit-bearing cross-plane operator, output covariance units follow from the operator's input/output unit mapping.

All covariance terms summed in one equation must therefore be expressed at the same physical reference plane and in compatible units.

This is already enforced conceptually by ADR-003's stage-specific noise/reference-plane model.

**Result: PASS.**

---

## 12. DC offset and second-moment units — PASS

If

\[
[\mathbf d]=U,
\]

then

\[
[\mathbf d\mathbf d^H]=U^2,
\]

which matches the units of an uncentered second moment/covariance-like matrix at that measurement plane.

**Result: PASS.**

---

## 13. ADC full-scale and quantization units — PASS

\[
V_{\rm FSR}=V_{\max}-V_{\min}
\]

and

\[
\Delta=\frac{V_{\rm FSR}}{2^{N_b}}
\]

carry volts when expressed at the ADC input plane.

`N_b` is a dimensionless bit count.

Under the high-resolution additive-error approximation,

\[
\sigma_q^2\approx\frac{\Delta^2}{12}
\]

has units V^2 at the ADC input-equivalent plane.

If a later representation uses raw integer codes, dequantized volts, or another engineering unit, covariance units change accordingly and the representation shall be declared.

**Result: PASS.**

---

## 14. dB and logarithmic semantics — PASS

The ideal ADC relation

\[
\mathrm{SNR}_{q,\mathrm{dB}}
\approx6.02N_b+1.76
\]

produces a dB value from a dimensionless signal-power/noise-power ratio.

Gate C establishes the general rule:

\[
\boxed{\text{No dimensional physical quantity is passed directly into a logarithm.}}
\]

Any dB quantity must be a ratio to a declared same-unit reference.

Power ratios use `10 log10`; amplitude ratios use `20 log10` only when the corresponding squared-power relation is valid and the same impedance/reference convention applies.

`dB`, `dBFS`, gain dB, SNR dB, SINAD dB, THD dB, and SFDR dB shall not be treated as interchangeable references.

**Result: PASS.**

---

## 15. Nonlinear receiver coefficient units — PASS WITH EXPLICIT INTERPRETATION

For a local model

\[
y=a_1x+a_3|x|^2x+\cdots,
\]

every term must have the same units as `y`.

If `x` and `y` share units `U`, then

\[
[a_1]=1,
\qquad
[a_3]=U^{-2},
\]

and higher-order coefficients carry the corresponding inverse powers of `U`.

Thus polynomial coefficients are not universally dimensionless.

This is a normative interpretation of the typed nonlinear operator and introduces no contradiction in the governing ADR.

**Result: PASS.**

---

## 16. Calibration parameter covariance — PASS

A calibration-state vector may mix parameters with different units, e.g. meters, radians, seconds, and dimensionless gain.

Therefore `P_theta` is a mixed-unit covariance matrix: each entry carries the product units of its corresponding parameter pair.

For

\[
\mathbf R_{a,\rm cal}
\approx\mathbf J_a\mathbf P_\theta\mathbf J_a^H,
\]

the Jacobian column associated with parameter `theta_i` carries response-units per unit of `theta_i`. The mixed units cancel correctly in the matrix product, leaving response-covariance units.

The ADR already warns that raw mixed-unit Jacobian condition numbers are not invariant under unit changes and require declared parameter scaling.

**Result: PASS.**

---

## 17. Tikhonov regularization — PASS WITH NORMATIVE UNIT RULE

The governing ADR gives

\[
\mathbf C_\lambda
=(\mathbf H^H\mathbf H+\lambda\mathbf I)^{-1}\mathbf H^H.
\]

For dimensional homogeneity,

\[
\boxed{[\lambda\mathbf I]=[\mathbf H^H\mathbf H].}
\]

Therefore `lambda` is **not universally dimensionless**. It must carry the same units as `H^H H` under the chosen physical scaling, or the inverse problem must first be expressed in an explicitly nondimensionalized/scaled coordinate system where both are dimensionless.

When `H` is a same-unit dimensionless channel operator, `lambda` is dimensionless.

This is a required unit contract for later software/configuration design.

The current formula is dimensionally consistent under this required interpretation and therefore does not constitute a Gate-C failure.

**Result: PASS.**

---

## 18. Singular values and condition numbers — PASS WITH SCALING RULE

A condition number is dimensionless when formed from a consistently scaled linear operator whose singular values share the same units.

For mixed-unit state/Jacobian problems, raw condition numbers can change under unit conversion and shall not be interpreted physically without declared characteristic scaling/nondimensionalization.

This is consistent with ADR-003 Section 26.

**Result: PASS.**

---

## 19. Manifold error metrics — PASS WITH UNIT-COMPATIBILITY RULE

For raw Euclidean error

\[
d_{\rm raw}=\|\mathbf b-\mathbf a\|_2,
\]

`a` and `b` must be expressed in compatible physical units and normalization; the result carries those response units.

For the phase-only relative metric

\[
\varepsilon_\phi
=\min_\phi
\frac{\|\mathbf b-e^{j\phi}\mathbf a\|}{\|\mathbf a\|},
\]

the numerator and denominator have the same units, so the result is dimensionless.

For common-complex-scale alignment, the fitted `c` carries whatever ratio units are required to map the units/normalization of `a` to those of `b`; it is dimensionless only when the vectors share the same units.

Normalized coherence

\[
\rho
=\frac{|\mathbf a^H\mathbf b|}{\|\mathbf a\|\|\mathbf b\|}
\]

is dimensionless because numerator and denominator have identical product units.

The projective angle and `1-rho^2` are therefore dimensionless.

**Result: PASS.**

---

## 20. Direct measured/CST manifold units — PASS

A direct measured or EM manifold is not assumed to be dimensionless by default.

Its physical units depend on exported quantity, normalization, excitation, reference impedance, de-embedding, and chosen reference plane.

Therefore a measured/CST manifold may be compared or substituted into a processing path only after its units/normalization are compatible with the expected estimator manifold semantics.

Magnitude normalization shall not silently destroy the raw physical calibration scale.

**Result: PASS.**

---

## 21. Covariance perturbation units — PASS

In

\[
\Delta\mathbf R_A
=
\Delta\mathbf A\mathbf R_s\mathbf A^H
+\mathbf A\mathbf R_s\Delta\mathbf A^H
+\Delta\mathbf A\mathbf R_s\Delta\mathbf A^H,
\]

all terms have the same units as the sensor-domain signal covariance when `A` and `Delta A` describe the same source-to-sensor response mapping.

Similarly,

\[
\mathbf E_{\rm sensor}
=\mathbf R_{\rm phys}-\mathbf R_{\rm nom}
\]

and

\[
\mathbf E_{\rm sample}
=\hat{\mathbf R}-\mathbf R_{\rm phys}
\]

are valid only for covariances represented at the same plane and with the same units.

The governing ADR's object/reference-plane semantics satisfy this requirement.

**Result: PASS.**

---

## 22. Whitening units — PASS

If sensor data carry units `U`, then

\[
[\mathbf R_n]=U^2
\]

and

\[
[\mathbf R_n^{-1/2}]=U^{-1}.
\]

Thus

\[
\mathbf y_w=\mathbf R_n^{-1/2}\mathbf y
\]

is dimensionless for same-unit channels, and the whitened noise covariance becomes the dimensionless identity.

The steering/manifold must be transformed by the same whitening operator; its resulting units depend on the source-amplitude convention, but the whitened measurement equation remains dimensionally homogeneous.

**Result: PASS.**

---

## 23. Eigenvalue and perturbation-bound units — PASS

Covariance eigenvalues, covariance perturbation norm `||E||_2`, and signal/noise eigengaps all carry covariance units.

Therefore the Weyl bound

\[
|\tilde\lambda_i-\lambda_i|
\le\|\mathbf E\|_2
\]

is dimensionally homogeneous.

Davis–Kahan-type ratios of perturbation norm to eigengap are dimensionless, as required for a sine/principal-angle quantity.

Population and sample eigengaps may differ statistically but share the same physical covariance units when computed at the same measurement plane.

**Result: PASS.**

---

## 24. MUSIC denominator units — PASS WITH NORMALIZATION RULE

\[
D(\theta)
=\mathbf a^H(\theta)\mathbf P_n\mathbf a(\theta)
\]

has the squared units of the steering vector because `P_n` is dimensionless.

Therefore a generic MUSIC denominator is not automatically dimensionless unless the steering vector is dimensionless or normalized.

In the exact rank-one identity used by ADR-003, `u` and `v` are explicitly unit-norm vectors, so

\[
\mathbf v^H(\mathbf I-\mathbf u\mathbf u^H)\mathbf v
=1-\rho^2
\]

is dimensionless.

Any plotted pseudospectrum scaling/dB normalization must therefore declare its steering normalization/reference; DOA peak location shall not be confused with an absolute physical power unit.

**Result: PASS.**

---

## 25. MIMO gain/product units — PASS

A separable virtual-channel response

\[
g_{ij}^{\rm virt}=g_{{\rm tx},i}g_{{\rm rx},j}
\]

is dimensionless when both component gains are dimensionless same-domain complex ratios.

If a future MIMO profile uses unit-bearing Tx/Rx response operators, units follow typed operator composition rather than this dimensionless specialization.

**Result: PASS.**

---

## 26. Golden Reference unit checks — PASS

Gate C checks only dimensions; formal numerical evidence remains Gate E.

### GRP-014

- `delta d/d`: dimensionless;
- `u0`, `u_hat`: dimensionless direction cosine;
- `Delta theta`: radians.

**PASS.**

### GRP-015

\[
\Delta u=-\phi_e/(kd).
\]

`phi_e` and `kd` are both angular/dimensionless quantities, so `Delta u` is dimensionless.

For `d=lambda/2`, `kd=pi` is dimensionless.

**PASS.**

### GRP-016

`a`, `C`, and `b` are used as a normalized/effective dimensionless steering-response seed. Ratios such as `b2/b1` are dimensionless complex quantities and their arguments are angles.

**PASS.**

### GRP-017

The seed uses normalized response units, so `R_sig=b b^H` carries squared normalized-response units; adding `I` implicitly declares unit noise variance in the same normalized covariance units. The alignment `rho^2` and leakage `1-rho^2` are dimensionless.

**PASS.**

---

## 27. No-silent-unit-coercion requirements

Gate C makes the following requirements normative for later implementation:

```text
no implicit meters <-> wavelengths conversion
no implicit Hz <-> rad/s conversion
no implicit seconds <-> samples conversion
no implicit radians <-> degrees conversion in scientific kernels
no implicit volts <-> ADC codes conversion
no implicit covariance normalization
no implicit physical-manifold <-> unit-norm steering conversion
no dB conversion without a dimensionless ratio and declared reference
no cross-reference-plane matrix composition without compatible physical units
no dimensionless regularization assumption unless the inverse problem has been scaled accordingly
```

---

## 28. Non-blocking notes for later gates

1. Gate D should encode units/domain semantics in software types, configuration fields, validation rules, and artifact metadata without forcing one representation on all future sensor profiles.
2. Gate E should state the unit system and normalization explicitly for every Golden Reference input and expected result.
3. Gate F should test unit/domain errors such as negative/zero sample rate, inconsistent ADC range, calibration artifacts expressed in incompatible units, and out-of-domain normalization/reference mismatches.
4. The governing ADR top-level status metadata can be synchronized during later cross-gate reconciliation; this does not affect dimensional correctness.

---

## 29. Blocking findings

```text
Dimensionally invalid equation:              NONE FOUND
Dimensional quantity inside logarithm:       NONE FOUND
Hz / rad/s silent substitution:              NONE FOUND
seconds / samples silent substitution:       NONE FOUND
meters / wavelengths silent substitution:    NONE FOUND
ADC volts / digital-code conflation:         NONE FOUND
Covariance-unit contradiction:               NONE FOUND
Unit-incompatible GRP seed:                  NONE FOUND
```

The Tikhonov regularization parameter and unit-bearing sensor operators require explicit unit interpretation, but the equations are dimensionally consistent under the typed/reference-plane semantics documented above. These are normative unit rules, not Gate-C failures.

---

## 30. Gate C decision

\[
\boxed{\text{Gate C — Dimensional and Unit Consistency: PASS}}
\]

No unresolved dimensional or unit contradiction remains in ADR-003's declared scope.

Gate C confirms that the governing equations are dimensionally homogeneous under their declared reference-plane semantics and that unit-bearing versus dimensionless quantities can be represented without silent conversion.

ADR-003 remains **NOT ACCEPTED** because Gates D–F and final cross-gate reconciliation have not passed.

The next formal work item is:

\[
\boxed{\text{Gate D — Software Semantic Consistency}}
\]
