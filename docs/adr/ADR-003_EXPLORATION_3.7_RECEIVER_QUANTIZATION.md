# ADR-003 Exploration 3.7 — Quantization / Receiver / Dynamic-Range Effects

- **Phase:** 0C — Scientific Foundations
- **Status:** EXPLORATION COMPLETE — CANDIDATE CONTRACT, NOT ACCEPTED
- **Parent ADR:** ADR-003 — Sensor Imperfections, Mutual Coupling, and Calibration
- **Branch:** `docs/phase0c-scientific-conventions`
- **Depends on:** ADR-001, ADR-002, ADR-003 Explorations 3.1–3.6
- **Acceptance gates:** Not started

> This is the dedicated exploration record for ADR-003 Section 3.7. It is not an accepted governing ADR. Candidate decisions remain subject to 3.8–3.14 reconciliation, Gates A–F, Golden Reference evidence, boundary/failure analysis, and final acceptance.

---

## 1. Receiver-chain scope and semantic boundaries

Exploration 3.7 covers imperfections that arise in the analog receive chain, data conversion, and finite-resolution measurement representation. It does **not** collapse all hardware imperfections into one additive-noise term.

A useful conceptual chain is

```text
physical sensor / coupled port response
    ↓
analog receiver gain, filtering, noise, offset, I/Q conversion, nonlinearity
    ↓
sampling instant / aperture uncertainty
    ↓
ADC input and full-scale constraint
    ↓
quantizer / code mapping / overrange behavior
    ↓
digital measurement samples
    ↓
subsequent DSP / FPGA arithmetic
```

ADC quantization and FPGA/processor fixed-point arithmetic are separate scientific stages. ADC quantization changes the measurement representation at acquisition; FPGA arithmetic quantization occurs later inside an implementation and has its own scaling, rounding, saturation, and word-length semantics.

## 2. Ideal uniform ADC quantizer

For an explicitly declared ideal uniform \(N_b\)-bit quantizer with analog full-scale input span

\[
\boxed{V_{\rm FSR}=V_{\max}-V_{\min}},
\]

and \(2^{N_b}\) quantization intervals, define the ideal step size

\[
\boxed{\Delta=\frac{V_{\rm FSR}}{2^{N_b}}}.
\]

This formula assumes the declared uniform idealization. The exact transition levels, reconstruction levels, endpoint behavior, signed/unsigned code mapping, two's-complement/offset-binary encoding, and mid-rise versus mid-tread convention must be explicit when code-exact behavior matters.

For an in-range nearest-level idealization,

\[
y=Q(x),
\qquad
e_q=Q(x)-x,
\]

and away from endpoint ambiguities,

\[
\boxed{|e_q|\le\frac{\Delta}{2}}.
\]

This deterministic in-range error bound is different from a stochastic quantization-noise model.

For a complex baseband sample, GeoDOA shall not assume that a physical ADC directly quantizes a complex number. A physical I/Q receiver usually has two real converter paths or another explicitly declared architecture. An abstract complex quantizer may be used only when its relationship to physical I/Q conversion is stated.

## 3. Exact quantization error versus additive quantization-noise approximation

The quantizer is nonlinear:

\[
\boxed{y=Q(x)}.
\]

Writing

\[
Q(x)=x+e_q
\]

is an identity if \(e_q\equiv Q(x)-x\), but treating \(e_q\) as independent, white, zero-mean noise is an **additional statistical approximation**.

Under the classical high-resolution/no-overload conditions in which the quantization error is effectively distributed uniformly over one quantization cell,

\[
\boxed{e_q\sim\mathcal U\left(-\frac{\Delta}{2},\frac{\Delta}{2}\right)}
\]

is a useful model, giving

\[
\boxed{\operatorname E[e_q]=0,
\qquad
\sigma_q^2=\frac{\Delta^2}{12}}.
\]

GeoDOA shall not assume this model blindly. Quantization error can be signal-correlated, spectrally structured, periodic, or strongly non-Gaussian for low-level, deterministic, coherent, low-resolution, or overloaded inputs. Dither or naturally occurring receiver noise may make additive-noise assumptions more accurate, but dither itself is a declared physical/algorithmic condition.

## 4. Ideal quantization SNR and ENOB

For a full-scale sinusoid applied to an ideal \(N_b\)-bit uniform ADC, with only the classical uniform quantization-noise model and no overload, thermal noise, jitter, distortion, or nonlinearity, the familiar result is

\[
\boxed{\operatorname{SNR}_{q,\rm dB}
\approx6.02N_b+1.76\ \text{dB}}.
\]

This result is not a universal SNR law for arbitrary waveforms, amplitudes, bandwidths, or converters. Its signal definition and full-scale convention must be stated.

For practical converters, **nominal resolution** \(N_b\) and **effective number of bits** are different. Under the conventional sinusoidal dynamic-test definition,

\[
\boxed{\operatorname{ENOB}
\approx\frac{\operatorname{SINAD}_{\rm dB}-1.76}{6.02}}.
\]

ENOB depends on test conditions such as input frequency, amplitude, sample rate, analog front-end, clock quality, and which distortion/noise components enter SINAD. ENOB shall not be used as a drop-in replacement for nominal code width or DC accuracy.

Likewise, SNR, SINAD, THD, SFDR, ENOB, dynamic range, and noise-free resolution are distinct metrics and must not be reported under one generic `adc_quality` field.

## 5. Full scale, dBFS, headroom, saturation, and clipping

The ADC has a finite allowed input region. If the analog input exceeds the declared conversion range, the in-range quantization bound \(|e_q|\le\Delta/2\) no longer applies.

A saturating quantizer can be represented abstractly as

\[
\boxed{y=Q_{\rm sat}(x;V_{\min},V_{\max})}.
\]

Clipping/overrange is a nonlinear information-loss event, not ordinary quantization noise. It can create harmonics, intermodulation, biased amplitudes, covariance distortion, and false spatial/statistical structure.

GeoDOA shall preserve an overrange/clipping diagnostic where the modeled converter supplies one. Samples or frames containing overrange events shall not silently be treated as statistically equivalent to valid in-range samples.

`dBFS` requires an explicit full-scale reference convention. Peak full-scale, RMS full-scale sine, full-scale span, and code-span references are not interchangeable without a declaration.

## 6. Receiver thermal/electronic noise versus quantization error

Receiver noise is generated physically before and/or within acquisition electronics. Quantization error is generated by the discrete amplitude mapping of the ADC. They are different phenomena.

A simple declared chain may be

\[
\boxed{\mathbf z[k]=\mathbf G_{\rm rx}\mathbf x[k]+\mathbf n_{\rm rx}[k]}
\]

followed by

\[
\boxed{\mathbf y[k]=\mathcal Q(\mathbf z[k])}.
\]

The receiver-noise covariance

\[
\mathbf R_{n,\rm rx}
=\operatorname E[\mathbf n_{\rm rx}\mathbf n_{\rm rx}^H]
\]

need not be spatially white, equal-variance, or independent across channels. Shared supplies, clock feedthrough, coupling, common references, and receiver architecture can create correlated noise.

Under a bounded additive-quantization approximation, one may write

\[
\mathbf y\approx\mathbf z+\mathbf e_q
\]

and then, only with the required independence assumptions,

\[
\mathbf R_y
\approx
\mathbf R_z+\mathbf R_q.
\]

Analog receiver noise may also act as natural dither, changing quantizer statistics. This does not make receiver noise and quantization noise the same physical source.

## 7. Gain staging, dynamic range, and AGC

Analog gain before the ADC controls how the available converter range is used. Too little gain can make weak signals occupy only a small number of codes and increase the relative importance of downstream ADC noise/quantization. Too much gain can reduce headroom and drive analog compression or ADC clipping.

Therefore receiver gain staging is a tradeoff among at least

\[
\boxed{\text{sensitivity / noise figure}
\leftrightarrow
\text{ADC utilization}
\leftrightarrow
\text{headroom / compression / clipping}
\leftrightarrow
\text{linearity / SFDR}}.
\]

Analog gain applied before quantization is not equivalent to digital scaling applied after quantization. Digital scaling cannot recover information already lost to clipping or coarse quantization.

An AGC state shall be treated as part of measurement provenance. For an ideal common gain

\[
\mathbf G_{\rm AGC}[k]=g_c[k]\mathbf I,
\]

all channels receive the same instantaneous scale, which can preserve normalized spatial direction at each snapshot. However, time-varying common gain still weights snapshots differently and changes absolute signal/noise levels.

Channel-dependent AGC or unequal gain control has

\[
\mathbf G_{\rm AGC}[k]
=\operatorname{diag}(g_1[k],\ldots,g_N[k]),
\]

which can directly distort relative manifold amplitude and make the covariance process time varying.

Gain-control state, settling/transient state, update timing, and whether gain is analog or digital must be explicit.

## 8. Aperture jitter as a receiver/acquisition error

Exploration 3.6 defined sample-time jitter semantically. Here its receiver-performance consequence is made explicit.

For a small sampling-time error \(\delta t\),

\[
\boxed{x(t+\delta t)
\approx x(t)+x'(t)\delta t}.
\]

Thus jitter-induced amplitude error scales with signal slew rate, not merely with signal amplitude.

For a sinusoid of frequency \(f_{\rm in}\) and uncorrelated RMS aperture jitter \(\sigma_t\), the classical jitter-limited SNR approximation is

\[
\boxed{\operatorname{SNR}_{\rm jitter,dB}
\approx-20\log_{10}(2\pi f_{\rm in}\sigma_t)}.
\]

This is a specialized sinusoidal/RMS result, not a universal stochastic model for arbitrary waveforms.

Common and differential jitter must remain distinguishable. A common narrowband sample-time fluctuation may appear as a common instantaneous phase perturbation, while channel-specific or partially correlated jitter can create relative spatial error. Clock-tree topology and jitter correlation therefore belong to provenance.

## 9. DC offset, mean removal, and spurious covariance modes

Let a receiver add a deterministic or slowly varying offset vector \(\mathbf d\):

\[
\boxed{\mathbf y=\mathbf x+\mathbf d}.
\]

The uncentered second moment is

\[
\mathbf R_y^{(2)}
=\operatorname E[\mathbf y\mathbf y^H].
\]

If \(\operatorname E[\mathbf x]=\mathbf0\), then

\[
\boxed{\mathbf R_y^{(2)}
=\mathbf R_x+\mathbf d\mathbf d^H}.
\]

A constant channel-offset vector can therefore create an additional rank-one term in the uncentered second moment.

An ideal centered covariance removes a truly constant offset when the mean is exactly known/estimated under compatible stationarity conditions. Finite-sample mean estimation, drifting offsets, DC leakage, LO feedthrough, and source components at/near DC can leave residual structure.

GeoDOA shall preserve the ADR-002 distinction between uncentered second moment and centered sample covariance; `DC offset removed` is not an automatic property of every covariance computation.

## 10. I/Q imbalance is a widely linear impairment

In a quadrature/direct-conversion receiver, I/Q amplitude mismatch, phase mismatch, and DC offset can mix the desired complex signal with its conjugate image.

A useful per-array widely linear model is

\[
\boxed{\mathbf y
=\mathbf A_{\rm IQ}\mathbf x
+\mathbf B_{\rm IQ}\mathbf x^*
+\mathbf d_{\rm IQ}}.
\]

For independent per-channel I/Q imbalance, \(\mathbf A_{\rm IQ}\) and \(\mathbf B_{\rm IQ}\) may be diagonal. Ideal quadrature balance corresponds to the conjugate-image coefficient vanishing:

\[
\boxed{\mathbf B_{\rm IQ}=\mathbf0}.
\]

Thus I/Q imbalance is not generally equivalent to an ordinary complex gain matrix \(\mathbf G\mathbf x\).

For centered data define covariance and pseudocovariance

\[
\mathbf R_x=\operatorname E[\mathbf x\mathbf x^H],
\qquad
\mathbf P_x=\operatorname E[\mathbf x\mathbf x^T].
\]

Ignoring offset for this expression,

\[
\boxed{
\begin{aligned}
\mathbf R_y
={}&\mathbf A\mathbf R_x\mathbf A^H
+\mathbf A\mathbf P_x\mathbf B^H\\
&+\mathbf B\mathbf P_x^*\mathbf A^H
+\mathbf B\mathbf R_x^*\mathbf B^H.
\end{aligned}}
\]

Consequently, ordinary covariance alone may be insufficient to describe an improper/noncircular complex receiver process. Future I/Q-aware estimation may require augmented/widely linear statistics.

## 11. Analog nonlinearity, compression, and intermodulation

Receiver amplifiers, mixers, and ADC front ends can depart from linear superposition before hard clipping occurs.

A memoryless complex-envelope specialization may be represented locally as

\[
\boxed{y_n
=a_{1,n}x_n+a_{3,n}|x_n|^2x_n+a_{5,n}|x_n|^4x_n+\cdots}.
\]

This is a behavioral model, not a universal transistor-level law.

Once the receiver is nonlinear,

\[
F(x_1+x_2)\neq F(x_1)+F(x_2),
\]

so multiple sources/interferers can create harmonics and intermodulation products not present in the linear array model. A strong blocker can therefore influence a weak-source DOA estimate even when the blocker itself lies outside the ideal signal model.

P1dB, IIP2/IIP3, THD, and SFDR are receiver/converter characterization metrics; they are not interchangeable and are not themselves direct coefficients of the polynomial model without an explicit mapping.

Analog compression and ADC clipping are distinct nonlinear stages, although both may occur in the same receiver under excessive level.

## 12. Covariance and eigenspace consequences

For exact quantization or nonlinear receiver response,

\[
\boxed{\mathbf R_y
=\operatorname E[\mathcal F(\mathbf x)\mathcal F(\mathbf x)^H]}
\]

is the primary definition. In general it cannot be reduced to \(\mathbf R_x+\sigma^2\mathbf I\).

Under the restricted additive, spatially white quantization approximation,

\[
\mathbf R_y\approx\mathbf R_x+\sigma_q^2\mathbf I,
\]

ideal quantization noise only shifts eigenvalues and preserves eigenvectors. This special result is frequently useful, but it must not be generalized to unequal channel steps, channel-dependent gain, correlated quantization error, clipping, I/Q imbalance, or nonlinear compression.

If

\[
\mathbf R_q=\operatorname{diag}(\sigma_{q,1}^2,\ldots,\sigma_{q,N}^2)
\]

with unequal entries, even an additive approximation can rotate eigenspaces relative to the ideal equal-noise case.

Clipping/nonlinearity can also make the effective response source-amplitude dependent, violating the fixed linear manifold assumption used by classical MUSIC. The correct question is therefore not merely `how many bits?` but whether the complete receiver/quantizer model remains compatible with the estimator's covariance/manifold assumptions.

## 13. Coarse and one-bit quantization as a separate estimator regime

Very coarse quantization shall not be justified through the high-resolution \(\Delta^2/12\) approximation by default.

For example, for zero-mean jointly Gaussian **real** variables \(x_i,x_j\), one-bit sign quantization obeys the classical arcsine relationship

\[
\boxed{\operatorname E[\operatorname{sgn}(x_i)\operatorname{sgn}(x_j)]
=\frac{2}{\pi}\arcsin(\rho_{ij})},
\]

where \(\rho_{ij}\) is the normalized unquantized correlation coefficient.

Complex one-bit array models have corresponding real/imaginary correlation relations under their declared Gaussian/properness/normalization assumptions. This illustrates a crucial point: severe quantization transforms covariance **nonlinearly**, but under special statistical assumptions enough correlation structure can sometimes be recovered or exploited for DOA estimation.

One-bit/coarse-ADC MUSIC and arcsine-law covariance recovery are therefore future specialized estimator profiles, not evidence that ordinary unquantized MUSIC is automatically compatible with one-bit data.

## 14. Floating-point samples, ADC codes, dequantized values, and FPGA fixed point

GeoDOA shall distinguish at least four numerical meanings:

1. **Analog-equivalent / pre-ADC sample value** represented numerically in floating point for simulation.
2. **ADC output code** with declared code width, coding, full-scale map, and saturation semantics.
3. **Dequantized numerical value** obtained by mapping the code back to declared physical/normalized units.
4. **DSP/FPGA fixed-point value** created later by digital arithmetic with its own word length, scaling, rounding, overflow, and saturation behavior.

A Python `float64` array can represent an ideal analog-equivalent sampled model; its machine precision is not the ADC resolution. Conversely, converting ADC codes to `float64` does not undo acquisition quantization.

FPGA arithmetic effects belong to implementation/numerical realization and must not be double counted as ADC quantization. The final hardware co-design flow may contain both effects, but their provenance and insertion stages remain separate.

## 15. Calibration, characterization, and provenance

Receiver/ADC calibration and characterization may include, as applicable:

- ADC gain and offset error;
- transition-level / DNL / INL characterization;
- channel full-scale range and code mapping;
- channel gain/phase response and gain-state tables;
- I/Q amplitude/phase imbalance and DC/LO leakage;
- clipping/overrange statistics;
- ENOB/SINAD/SNR/THD/SFDR test condition;
- P1dB/IIP2/IIP3 or another receiver-linearity characterization;
- aperture jitter/clock source and correlation topology;
- temperature, sample rate, center frequency, bandwidth, analog gain/AGC state, and supply/reference conditions.

A calibration artifact shall state whether it corrects raw ADC codes, dequantized values, complex baseband samples, covariance, or a processing manifold. Corrections at different stages need not commute.

A receiver characterized at one gain state, sample rate, center frequency, or temperature shall not silently be assumed valid in another state.

## 16. Small deterministic checks

### Ideal 12-bit quantizer

For an ideal \(12\)-bit uniform converter with \(V_{\rm FSR}=2\ \text{V}\),

\[
\boxed{\Delta=\frac{2}{4096}
=4.8828125\times10^{-4}\ \text{V}
\approx488.28\ \mu\text{V}}.
\]

Under the classical uniform-error approximation,

\[
\boxed{\sigma_q=\frac{\Delta}{\sqrt{12}}
\approx140.95\ \mu\text{V}}.
\]

For an ideal full-scale sinusoid,

\[
\boxed{\operatorname{SNR}_q
\approx6.02(12)+1.76=74.0\ \text{dB}}.
\]

These values are ideal-reference calculations, not a prediction of a real 12-bit ADC's ENOB.

### Jitter-limited SNR

For \(\sigma_t=1\ \text{ps RMS}\),

\[
\operatorname{SNR}_{\rm jitter}(100\ \text{MHz})
\approx64.04\ \text{dB},
\]

while

\[
\operatorname{SNR}_{\rm jitter}(1\ \text{GHz})
\approx44.04\ \text{dB}.
\]

The same clock jitter therefore becomes much more restrictive as analog input frequency increases.

### Constant DC offset and second moment

Let

\[
\mathbf R_x=\mathbf I_2,
\qquad
\mathbf d=\begin{bmatrix}0.5\\0.5\end{bmatrix}.
\]

Then the uncentered second moment is

\[
\mathbf R_y^{(2)}
=\mathbf I_2+
\begin{bmatrix}0.25&0.25\\0.25&0.25\end{bmatrix}
=
\begin{bmatrix}1.25&0.25\\0.25&1.25\end{bmatrix},
\]

with eigenvalues \(1.5\) and \(1.0\). A common constant offset has therefore created a rank-one second-moment mode even though the underlying covariance was identity. Exact centering removes this deterministic offset in the ideal stationary case.

These are exploration checks, not new formal GRP numbers.

## 17. Scientific origin and verification lineage

The 3.7 contract is grounded in several established technical lineages:

- classical quantization theory, including Bennett's analysis of quantized-signal spectra and the later Widrow quantization-noise framework that explains when a nonlinear uniform quantizer may be approximated by additive noise;
- IEEE ADC terminology/test practice, particularly the IEEE 1241 family for sampled/quantized converter characterization;
- standard ADC engineering results for \(\Delta^2/12\), ideal full-scale sine \(6.02N+1.76\) dB, SINAD/ENOB, overrange behavior, and aperture-jitter limitations;
- classical RF receiver theory for cascaded noise, gain staging, compression, intercept points, and dynamic-range tradeoffs;
- quadrature-receiver impairment theory in which I/Q imbalance is naturally widely linear and can introduce conjugate-image terms and pseudocovariance dependence;
- quantized array-processing literature, including arcsine-law covariance relations and one-bit MUSIC/DOA methods, demonstrating that severe quantization is an estimator-model issue rather than merely an additive-noise penalty.

These sources justify the contract boundaries and candidate models. Formal ADR-003 evidence and acceptance still require Explorations 3.8–3.14 followed by Gates A–F.

## 18. Candidate decisions from Exploration 3.7

- **3.7-D1** — Analog receiver impairments, ADC sampling/quantization, and downstream DSP/FPGA arithmetic are separate stages with explicit provenance.
- **3.7-D2** — An ideal uniform ADC profile shall declare full-scale span, nominal bit resolution, code/coding semantics, quantizer convention, and overload behavior.
- **3.7-D3** — For the declared ideal uniform specialization, \(\Delta=V_{\rm FSR}/2^{N_b}\).
- **3.7-D4** — The in-range nearest-level error bound \(|e_q|\le\Delta/2\) is distinct from a stochastic quantization-noise model.
- **3.7-D5** — Treating quantization error as independent white uniform noise is an approximation with validity assumptions, not a universal property of quantizers.
- **3.7-D6** — The variance \(\Delta^2/12\) is used only under the declared classical uniform-error assumptions.
- **3.7-D7** — The \(6.02N+1.76\) dB result is an ideal full-scale-sine quantization reference, not a generic SNR law.
- **3.7-D8** — Nominal ADC bits and ENOB are distinct; ENOB is a test-condition-dependent dynamic metric tied to SINAD under its declared convention.
- **3.7-D9** — SNR, SINAD, THD, SFDR, ENOB, and dynamic range remain distinct metrics.
- **3.7-D10** — `dBFS` requires an explicit full-scale reference convention.
- **3.7-D11** — Saturation/clipping is a nonlinear overrange condition and shall not be modeled as ordinary in-range quantization noise.
- **3.7-D12** — Overrange/clipping diagnostics and affected-sample provenance should be retained when available.
- **3.7-D13** — Receiver thermal/electronic noise and ADC quantization error are different physical/statistical sources.
- **3.7-D14** — Receiver noise covariance need not be spatially white or channel independent.
- **3.7-D15** — Analog gain before quantization and digital scaling after quantization are not equivalent operations.
- **3.7-D16** — Gain staging explicitly trades sensitivity/noise figure, ADC utilization, headroom, compression/clipping, and linearity/SFDR.
- **3.7-D17** — AGC state is measurement provenance; common, channel-dependent, static, and time-varying AGC modes have different spatial/statistical consequences.
- **3.7-D18** — Common scalar AGC can preserve instantaneous normalized manifold direction but can still alter temporal weighting and absolute signal/noise levels.
- **3.7-D19** — Channel-dependent/time-varying AGC can create relative manifold distortion and covariance nonstationarity.
- **3.7-D20** — Small sampling jitter produces an error proportional to waveform derivative; jitter sensitivity therefore grows with signal frequency/slew rate.
- **3.7-D21** — The classical sinusoidal jitter-limited SNR formula is a specialized RMS result, not a universal jitter model.
- **3.7-D22** — Common, differential, and correlated jitter remain distinguishable through clock-tree provenance.
- **3.7-D23** — Constant receiver DC offset contributes a rank-one term to an uncentered second moment when the underlying signal is zero mean.
- **3.7-D24** — Centered covariance can remove a truly constant offset ideally, but finite-sample/drifting/DC-near-signal cases require explicit handling.
- **3.7-D25** — I/Q imbalance is generally a widely linear impairment involving both \(\mathbf x\) and \(\mathbf x^*\), not merely an ordinary complex gain.
- **3.7-D26** — I/Q-imbalanced covariance can depend on pseudocovariance; augmented/widely linear statistics remain a future compatible extension.
- **3.7-D27** — Receiver compression/nonlinearity violates linear superposition and can create source-dependent intermodulation products.
- **3.7-D28** — P1dB, IIP2/IIP3, THD, and SFDR are distinct characterization metrics and are not direct interchangeable model coefficients.
- **3.7-D29** — Analog compression and ADC clipping are different nonlinear stages.
- **3.7-D30** — Exact nonlinear/quantized covariance is defined by \(E[\mathcal F(\mathbf x)\mathcal F(\mathbf x)^H]\); an additive white-noise reduction requires explicit assumptions.
- **3.7-D31** — Equal spatially white additive quantization noise may preserve eigenvectors in a restricted model; unequal/correlated/signal-dependent quantization need not.
- **3.7-D32** — Very coarse and one-bit quantization shall not default to the high-resolution \(\Delta^2/12\) model.
- **3.7-D33** — Arcsine-law/one-bit covariance methods are specialized statistical estimator regimes with explicit Gaussian/normalization assumptions.
- **3.7-D34** — Floating-point analog-equivalent samples, raw ADC codes, dequantized values, and FPGA/DSP fixed-point values are distinct numerical meanings.
- **3.7-D35** — Converting ADC codes to floating point does not recover information lost during acquisition quantization.
- **3.7-D36** — FPGA fixed-point quantization shall not be double counted as ADC quantization; each insertion stage retains separate scaling/rounding/overflow semantics.
- **3.7-D37** — Receiver/ADC calibration must state the data stage it corrects and the operating domain over which it is valid.
- **3.7-D38** — Calibration/characterization provenance may include gain state, sample rate, center frequency, bandwidth, clock, full scale, coding, temperature, I/Q state, linearity, and overrange conditions as applicable.
- **3.7-D39** — The initial Phase-1 validated profile may remain an ideal unquantized linear receiver represented in floating point while preserving explicit receiver/ADC extension contracts.
- **3.7-D40** — Later receiver profiles must declare estimator compatibility rather than silently feeding clipped, nonlinear, or severely quantized data into algorithms derived for an ideal linear covariance model.

---

## 19. Continuation state

Exploration 3.7 is complete as a candidate scientific contract. The next ADR-003 exploration section is:

```text
3.8 — Unified Sensor-Imperfection Operator
```

Do not start Gate A yet. The authoritative ADR-003 checkpoint remains subject to later reconciliation so that 3.1–3.7 are preserved without destructive rewriting.
