# ADR-003 Exploration 3.12 — Covariance / Eigenspace / MUSIC Error Propagation

- **Phase:** 0C — Scientific Foundations
- **Status:** EXPLORATION COMPLETE — CANDIDATE CONTRACT, NOT ACCEPTED
- **Parent ADR:** ADR-003 — Sensor Imperfections, Mutual Coupling, and Calibration
- **Branch:** `docs/phase0c-scientific-conventions`
- **Depends on:** ADR-001, ADR-002, ADR-003 Explorations 3.1–3.11
- **Acceptance gates:** Not started

> This is the dedicated exploration record for ADR-003 Section 3.12. It is not an accepted governing ADR. Candidate decisions remain subject to 3.13–3.14 reconciliation, Gates A–F, Golden Reference evidence, boundary/failure analysis, and final acceptance.

---

## 1. Primary question

Explorations 3.1–3.11 established the physical sensor-imperfection chain, calibration taxonomy, direct measured/EM manifolds, gauge/reference-plane semantics, manifold metrics, and identifiability concepts.

Exploration 3.12 answers:

> How do deterministic and stochastic sensor-model errors propagate into covariance, eigenvalues, signal/noise eigenspaces, and ultimately the MUSIC pseudospectrum and DOA estimate, and how shall GeoDOA distinguish those effects from finite-sample covariance error?

The central chain is

\[
\boxed{
\text{sensor/manifold mismatch}
\rightarrow
\text{population covariance distortion}
\rightarrow
\text{eigenvalue/eigenspace distortion}
\rightarrow
\text{noise-subspace leakage}
\rightarrow
\text{MUSIC spectrum/peak distortion}
\rightarrow
\text{DOA consequence}
}
\]

with a separate stochastic path

\[
\boxed{
\text{finite snapshots / random realization}
\rightarrow
\text{sample-covariance error}
\rightarrow
\text{sample eigenspace error}
\rightarrow
\text{MUSIC variability}.
}
\]

These two paths may coexist but shall not be conflated.

---

## 2. Population and sample covariance remain distinct

For a stationary narrowband linear array model

\[
\boxed{
\mathbf x[k]
=\mathbf A\mathbf s[k]+\mathbf n[k],
}
\]

with zero mean,

\[
\boxed{
\mathbf R_x
=\operatorname E[\mathbf x\mathbf x^H]
=\mathbf A\mathbf R_s\mathbf A^H+\mathbf R_n.
}
\]

For \(L\) snapshots, the uncentered sample second moment is

\[
\boxed{
\hat{\mathbf R}^{(2)}
=\frac{1}{L}\sum_{k=1}^{L}\mathbf x[k]\mathbf x[k]^H,
}
\]

while the centered sample covariance follows the ADR-002 mean-centering contract.

GeoDOA shall keep at least three concepts separate:

```text
nominal population covariance
physical population covariance
finite-sample covariance estimate
```

The difference between nominal and physical population covariance is sensor/model distortion; the difference between physical population covariance and its finite-sample estimate is sampling/estimation error.

---

## 3. Exact decomposition of sensor and finite-sample covariance error

Let

\[
\mathbf R_{\rm nom}
\]

be the nominal population covariance and

\[
\mathbf R_{\rm phys}
\]

be the physical population covariance under a realized sensor state.

Define

\[
\boxed{
\mathbf E_{\rm sensor}
=\mathbf R_{\rm phys}-\mathbf R_{\rm nom}.
}
\]

For a sample estimate

\[
\hat{\mathbf R}
=\mathbf R_{\rm phys}+\mathbf E_{\rm sample},
\]

where

\[
\boxed{
\mathbf E_{\rm sample}
=\hat{\mathbf R}-\mathbf R_{\rm phys}.
}
\]

Therefore exactly

\[
\boxed{
\hat{\mathbf R}-\mathbf R_{\rm nom}
=\mathbf E_{\rm sensor}+\mathbf E_{\rm sample}.
}
\]

This additive bookkeeping identity does not imply statistical independence. The distribution of \(\mathbf E_{\rm sample}\) depends on the physical data-generating covariance and therefore can itself change when sensor imperfections change the physical system.

---

## 4. Manifold perturbation to covariance perturbation

Let the physical manifold matrix be

\[
\boxed{
\mathbf A_{\rm phys}
=\mathbf A+\Delta\mathbf A.
}
\]

Assume for this subsection that source covariance \(\mathbf R_s\) and additive noise covariance \(\mathbf R_n\) are unchanged.

Then

\[
\mathbf R_{\rm phys}
=(\mathbf A+\Delta\mathbf A)
\mathbf R_s
(\mathbf A+\Delta\mathbf A)^H
+\mathbf R_n.
\]

Expanding,

\[
\boxed{
\begin{aligned}
\Delta\mathbf R_A
={}&
\Delta\mathbf A\mathbf R_s\mathbf A^H
+\mathbf A\mathbf R_s\Delta\mathbf A^H\\
&+\Delta\mathbf A\mathbf R_s\Delta\mathbf A^H.
\end{aligned}}
\]

The first-order covariance perturbation is therefore

\[
\boxed{
\Delta\mathbf R_A^{(1)}
=
\Delta\mathbf A\mathbf R_s\mathbf A^H
+\mathbf A\mathbf R_s\Delta\mathbf A^H.
}
\]

The quadratic term shall not be discarded outside an explicitly small-mismatch regime.

---

## 5. Linear sensor operator to covariance

For a deterministic linear sensor transform

\[
\boxed{
\mathbf y=\mathbf H\mathbf x,
}
\]

the covariance is

\[
\boxed{
\mathbf R_y
=\mathbf H\mathbf R_x\mathbf H^H.
}
\]

If

\[
\mathbf H=\mathbf I+\Delta\mathbf H,
\]

then

\[
\boxed{
\Delta\mathbf R_H
=
\Delta\mathbf H\mathbf R
+\mathbf R\Delta\mathbf H^H
+\Delta\mathbf H\mathbf R\Delta\mathbf H^H.
}
\]

The first-order term is

\[
\boxed{
\Delta\mathbf R_H^{(1)}
=
\Delta\mathbf H\mathbf R
+\mathbf R\Delta\mathbf H^H.
}
\]

This formula applies only when the same \(\mathbf H\) truly transforms the covariance content being modeled. Noise injected after \(\mathbf H\) must be added at its own physical stage, as established in 3.8.

---

## 6. Reconciliation with position-error phase perturbation

For a small diagonal phase perturbation

\[
\mathbf D
\approx\mathbf I+j\mathbf\Phi,
\qquad
\mathbf\Phi=\mathbf\Phi^H
\]

with real diagonal phase-error entries,

\[
\Delta\mathbf H=j\mathbf\Phi.
\]

Substitution into the first-order congruence relation gives

\[
\boxed{
\Delta\mathbf R
\approx
j(\mathbf\Phi\mathbf R-\mathbf R\mathbf\Phi),
}
\]

which reconciles exactly with the structured covariance perturbation already established in Exploration 3.2.

Thus geometry-derived phase error is not modeled as additive white covariance noise.

---

## 7. Noise covariance changes are a separate perturbation term

If sensor/receiver effects also change noise covariance,

\[
\mathbf R_{n,\rm phys}
=\mathbf R_n+\Delta\mathbf R_n,
\]

then

\[
\boxed{
\Delta\mathbf R
=\Delta\mathbf R_{\rm sig}
+\Delta\mathbf R_n.
}
\]

Examples include:

- unequal channel gain applied to pre-gain receiver noise;
- coupling transforming pre-coupling noise;
- inverse calibration coloring/amplifying noise;
- correlated receiver noise;
- channel-dependent quantization approximation;
- common reference/feedthrough noise.

Signal-manifold mismatch and noise-covariance mismatch shall be separately reportable.

---

## 8. Isotropic additive noise is a special eigenspace-preserving case

If

\[
\boxed{
\mathbf R_x
=\mathbf R_{\rm sig}+\sigma^2\mathbf I,
}
\]

then \(\mathbf R_x\) and \(\mathbf R_{\rm sig}\) share eigenvectors because adding \(\sigma^2\mathbf I\) shifts every eigenvalue by the same amount.

Thus spatially white equal-variance noise changes the eigenvalue floor but does not rotate population eigenvectors.

This statement is restricted to the population covariance and the exact isotropic term. Finite-sample covariance still exhibits random eigenspace error.

---

## 9. Unequal or colored noise can rotate ordinary covariance eigenspaces

If

\[
\mathbf R_n\neq\sigma^2\mathbf I,
\]

ordinary eigenvectors of

\[
\mathbf R_x
=\mathbf A\mathbf R_s\mathbf A^H+\mathbf R_n
\]

need not span the same signal/noise decomposition used by standard white-noise MUSIC.

Unequal diagonal noise is already sufficient to break the common-eigenvector property in general.

Therefore `additive noise` does not imply `eigenvectors unchanged`; isotropy is the essential special condition.

---

## 10. Whitening for positive-definite known noise covariance

If

\[
\mathbf R_n\succ0,
\]

define a whitening operator

\[
\boxed{
\mathbf W_n=\mathbf R_n^{-1/2}.
}
\]

Then

\[
\boxed{
\mathbf R_w
=\mathbf W_n\mathbf R_x\mathbf W_n^H
=\mathbf A_w\mathbf R_s\mathbf A_w^H+\mathbf I,
}
\]

where

\[
\boxed{
\mathbf A_w=\mathbf W_n\mathbf A.
}
\]

The steering/manifold used by a whitened MUSIC formulation must be transformed consistently.

Whitening based on an estimated or stale \(\mathbf R_n\) introduces its own calibration/model error.

If \(\mathbf R_n\) is singular or ill-conditioned, ordinary inverse-square-root whitening may be undefined or unstable and requires separate treatment.

---

## 11. Rank of the signal covariance

Let

\[
\mathbf R_{\rm sig}
=\mathbf A\mathbf R_s\mathbf A^H.
\]

Then

\[
\boxed{
\operatorname{rank}(\mathbf R_{\rm sig})
\le
\min\{\operatorname{rank}(\mathbf A),
\operatorname{rank}(\mathbf R_s)\}.
}
\]

If \(\mathbf A\) has full column rank and \(\mathbf R_s\) is full rank for \(K\) sources, then the signal-subspace dimension is \(K\).

If sources are coherent so that \(\mathbf R_s\) is rank deficient, signal-subspace rank can be smaller than source count.

GeoDOA shall preserve the distinctions among source count, source-covariance rank, signal-covariance rank, observed signal-subspace dimension, and sample-covariance rank.

---

## 12. Rank preservation under nonsingular sensor transforms

For nonsingular \(\mathbf H\),

\[
\boxed{
\operatorname{rank}
(\mathbf H\mathbf R_{\rm sig}\mathbf H^H)
=\operatorname{rank}(\mathbf R_{\rm sig}).
}
\]

Therefore a nonsingular mutual-coupling/gain transform can preserve rank while substantially rotating the signal subspace and changing eigenvalues/conditioning.

A rank-deficient transform can reduce observable signal rank.

Rank preservation does not imply subspace preservation.

---

## 13. Unitary versus general nonsingular transforms

If \(\mathbf H\) is unitary,

\[
\mathbf H^H\mathbf H=\mathbf I,
\]

then \(\mathbf H\mathbf R\mathbf H^H\) has the same eigenvalues as \(\mathbf R\), while its eigenvectors are rotated by \(\mathbf H\).

For a general nonsingular nonunitary \(\mathbf H\), rank is preserved but eigenvalues need not be.

For a common scalar \(c\mathbf I\), signal covariance scales by \(|c|^2\); a common phase alone has \(|c|=1\) and cancels from covariance.

---

## 14. Time-varying sensor operators can increase apparent covariance rank

If the effective response changes across snapshots,

\[
\mathbf x[k]
=\mathbf H[k]\mathbf A\mathbf s[k],
\]

then even for a stationary source covariance the time-averaged population-like second moment over a finite state sequence is

\[
\boxed{
\bar{\mathbf R}
=\frac{1}{L}\sum_{k=1}^{L}
\mathbf H[k]\mathbf A\mathbf R_s\mathbf A^H\mathbf H[k]^H
}
\]

under the corresponding deterministic-state assumptions.

In general,

\[
\boxed{
\bar{\mathbf R}
\neq
\bar{\mathbf H}\mathbf A\mathbf R_s\mathbf A^H\bar{\mathbf H}^H.
}
\]

A mixture of differently oriented rank-one covariances can have rank greater than one.

Thus time-varying gain/phase, CFO, AGC, deformation, or timing state can create additional apparent covariance modes even when the instantaneous source model is low rank.

---

## 15. Deterministic time-varying rank example

Consider one source whose instantaneous unit response alternates between

\[
\mathbf a_1
=\begin{bmatrix}1\\0\end{bmatrix},
\qquad
\mathbf a_2
=\begin{bmatrix}0\\1\end{bmatrix}.
\]

Each instantaneous signal covariance has rank one:

\[
\mathbf R_1=\mathbf a_1\mathbf a_1^H,
\qquad
\mathbf R_2=\mathbf a_2\mathbf a_2^H.
\]

Their equal average is

\[
\boxed{
\bar{\mathbf R}
=\frac12(\mathbf R_1+\mathbf R_2)
=\frac12\mathbf I,
}
\]

which has rank two.

This example does not claim that every time-varying sensor error increases rank. It demonstrates that covariance-window variation can create extra modes and invalidate a static-manifold source-count interpretation.

---

## 16. Eigenvalue perturbation — Weyl-type bound

Let \(\mathbf R\) and

\[
\tilde{\mathbf R}=\mathbf R+\mathbf E
\]

be Hermitian, with eigenvalues ordered consistently.

A standard Hermitian perturbation result gives

\[
\boxed{
|\tilde\lambda_i-\lambda_i|
\le\|\mathbf E\|_2.
}
\]

Thus operator-norm covariance error bounds each eigenvalue displacement.

This bound does not determine the sign of the shift and does not by itself quantify eigenvector/subspace rotation.

---

## 17. First-order simple-eigenvalue perturbation

For a simple normalized eigenpair

\[
\mathbf R\mathbf u_i
=\lambda_i\mathbf u_i,
\]

with phase gauge

\[
\mathbf u_i^H\Delta\mathbf u_i=0,
\]

the first-order eigenvalue perturbation is

\[
\boxed{
\Delta\lambda_i^{(1)}
=\mathbf u_i^H\mathbf E\mathbf u_i.
}
\]

The first-order eigenvector perturbation is

\[
\boxed{
\Delta\mathbf u_i^{(1)}
=\sum_{j\neq i}
\mathbf u_j
\frac{\mathbf u_j^H\mathbf E\mathbf u_i}
{\lambda_i-\lambda_j}.
}
\]

The denominator makes the dependence on eigenvalue separation explicit.

This expansion is not valid without care for repeated/clustered eigenvalues; subspace perturbation is the correct object there.

---

## 18. Eigenspace perturbation and eigengap

Let the reference Hermitian covariance have signal subspace \(\mathcal S\) separated from the complementary subspace by an eigenvalue gap

\[
\boxed{
\delta_{\rm gap}>0.
}
\]

Davis–Kahan-type sin-\(\Theta\) results bound subspace rotation by a quantity of the general form

\[
\boxed{
\|\sin\mathbf\Theta(\tilde{\mathcal S},\mathcal S)\|
\lesssim
\frac{\|\mathbf E\|}{\delta_{\rm gap}},
}
\]

under the theorem's spectral-separation assumptions and with the precise constant/denominator depending on the selected theorem variant and norm.

GeoDOA shall not hard-code one informal version as an exact universal equality.

The scientific implication is robust:

\[
\boxed{
\text{the same covariance perturbation can cause much larger subspace rotation when the eigengap is small.}
}
\]

---

## 19. Population eigengap and sample eigengap are distinct

GeoDOA shall distinguish a population eigengap computed from \(\mathbf R_{\rm phys}\) or \(\mathbf R_{\rm nom}\) from a sample eigengap computed from \(\hat{\mathbf R}\).

Finite snapshots perturb both eigenvalues and the observed gap.

A large sample gap in one realization is not proof of a large population gap, and a theorem requiring population spectral separation shall not silently substitute an unrelated sample quantity.

The exact notation for these gaps will be reconciled in the final ADR draft.

---

## 20. Signal/noise subspace projectors

Let

\[
\mathbf U_s\in\mathbb C^{N\times q},
\qquad
\mathbf U_n\in\mathbb C^{N\times(N-q)}
\]

be orthonormal bases for the signal and noise subspaces.

Define projectors

\[
\boxed{
\mathbf P_s
=\mathbf U_s\mathbf U_s^H,
\qquad
\mathbf P_n
=\mathbf U_n\mathbf U_n^H
=\mathbf I-\mathbf P_s.
}
\]

Projectors remove arbitrary basis rotations within a subspace and are often more meaningful than comparing eigenvector columns one by one.

---

## 21. Principal angles between subspaces

For two \(q\)-dimensional subspaces with orthonormal bases \(\mathbf U\) and \(\tilde{\mathbf U}\), the singular values of

\[
\boxed{
\mathbf U^H\tilde{\mathbf U}
}
\]

are

\[
\cos\theta_i,
\qquad
0\le\theta_i\le\pi/2.
\]

The principal angles \(\theta_i\) characterize subspace rotation.

Useful derived metrics include

\[
\boxed{
\|\sin\mathbf\Theta\|_2
=\sin\theta_{\max}
}
\]

and

\[
\boxed{
\|\sin\mathbf\Theta\|_F
=\left(\sum_i\sin^2\theta_i\right)^{1/2}.
}
\]

For one-dimensional subspaces this reduces to the projective-angle concept established in 3.11.

---

## 22. Projector-difference metric

For equal-dimensional subspaces,

\[
\boxed{
\|\tilde{\mathbf P}_s-\mathbf P_s\|_2
=\sin\theta_{\max}.
}
\]

The Frobenius projector distance satisfies

\[
\boxed{
\|\tilde{\mathbf P}_s-\mathbf P_s\|_F^2
=2\sum_i\sin^2\theta_i.
}
\]

These metrics are invariant to the arbitrary orthonormal basis chosen inside each subspace.

---

## 23. First-order subspace mixing structure

In an eigenbasis partitioned into signal and noise subspaces, the perturbation block

\[
\boxed{
\mathbf U_n^H\mathbf E\mathbf U_s
}
\]

drives first-order mixing between the two subspaces.

Perturbations confined purely within signal-signal or noise-noise blocks primarily perturb eigenvalues/bases inside the same subspaces at first order; cross-block components are what rotate the signal/noise decomposition.

This distinction is important because two covariance errors with the same Frobenius norm can have very different MUSIC consequences.

---

## 24. Exact MUSIC orthogonality under the matched population model

For classical narrowband MUSIC with spatially white noise and signal-subspace dimension \(q\), the physical steering vector for a true source lies in the population signal subspace:

\[
\boxed{
\mathbf P_n\mathbf a_{\rm phys}(\theta_k)=\mathbf0.
}
\]

The population MUSIC denominator is

\[
\boxed{
D(\theta)
=\mathbf a_{\rm model}^H(\theta)
\mathbf P_n
\mathbf a_{\rm model}(\theta).
}
\]

For a perfectly matched model at a true DOA,

\[
\boxed{
D(\theta_k)=0.
}
\]

The practical finite-sample denominator is generally nonzero even under a matched physical model because the estimated noise subspace is perturbed.

---

## 25. Exact rank-one link from manifold mismatch to MUSIC denominator

For a one-source population model, let the unit physical steering vector be

\[
\mathbf u
=\frac{\mathbf a_{\rm phys}}{\|\mathbf a_{\rm phys}\|}
\]

and let the unit model steering vector at the true source state be

\[
\mathbf v
=\frac{\mathbf a_{\rm model}}{\|\mathbf a_{\rm model}\|}.
\]

The physical noise projector is

\[
\mathbf P_n=\mathbf I-\mathbf u\mathbf u^H.
\]

Then

\[
\boxed{
\mathbf v^H\mathbf P_n\mathbf v
=1-|\mathbf u^H\mathbf v|^2
=1-\rho^2
=\sin^2\alpha.
}
\]

Therefore the 3.11 projective manifold leakage is exactly the normalized MUSIC denominator at the true source for the rank-one population case.

This is one of the central reconciliation results of ADR-003.

---

## 26. GRP-017 reconciliation

For the reserved coupling example,

\[
\mathbf a
=\begin{bmatrix}1\\-j\end{bmatrix},
\qquad
\mathbf b
=\begin{bmatrix}1-0.5j\\0.5-j\end{bmatrix},
\]

Explorations 3.5 and 3.11 established

\[
\boxed{
\rho^2=0.8,
\qquad
1-\rho^2=0.2.
}
\]

If \(\mathbf b\) is the physical coupled steering vector and \(\mathbf a\) is the nominal unit-normalized model direction, then the nominal model has normalized MUSIC denominator

\[
\boxed{D_{\rm nom}(\theta_0)=0.2}
\]

against the exact physical rank-one noise subspace.

Thus the coupling mismatch creates nonzero noise-subspace leakage even with infinite snapshots and no finite-sample covariance error.

Formal GRP-017 evidence remains reserved for Gate E.

---

## 27. GRP-017 covariance eigenstructure

The coupled response

\[
\mathbf b
=\begin{bmatrix}1-0.5j\\0.5-j\end{bmatrix}
\]

gives

\[
\boxed{
\mathbf R_{\rm sig}
=\mathbf b\mathbf b^H
=\begin{bmatrix}
1.25&1+0.75j\\
1-0.75j&1.25
\end{bmatrix}.
}
\]

Its eigenvalues are

\[
\boxed{2.5,\ 0.}
\]

Adding unit spatially white noise yields

\[
\boxed{
\mathbf R_x
=\mathbf R_{\rm sig}+\mathbf I,
}
\]

with eigenvalues

\[
\boxed{3.5,\ 1.0}
\]

and unchanged eigenvectors relative to \(\mathbf R_{\rm sig}\).

This example cleanly separates manifold/subspace rotation from isotropic noise-floor elevation.

---

## 28. Data-subspace error versus model-manifold error

MUSIC can suffer from two distinct mismatch channels.

### 28.1 Data/eigenspace perturbation

The estimated/physical noise projector differs from the nominal ideal projector:

\[
\boxed{
\tilde{\mathbf P}_n
=\mathbf P_n+\Delta\mathbf P_n.
}
\]

Causes include physical sensor covariance distortion, colored noise, time variation, finite samples, and correction error.

### 28.2 Search-manifold perturbation

The steering vector supplied to MUSIC differs from the matched response:

\[
\boxed{
\tilde{\mathbf a}(\theta)
=\mathbf a(\theta)+\Delta\mathbf a(\theta).
}
\]

Both effects can coexist and shall be separately diagnosable.

---

## 29. First-order MUSIC denominator expansion

Define

\[
D(\theta)
=\tilde{\mathbf a}^H(\theta)
\tilde{\mathbf P}_n
\tilde{\mathbf a}(\theta).
\]

With

\[
\tilde{\mathbf a}=\mathbf a+\Delta\mathbf a,
\qquad
\tilde{\mathbf P}_n=\mathbf P_n+\Delta\mathbf P_n,
\]

the expansion is

\[
\begin{aligned}
D
={}&
\mathbf a^H\mathbf P_n\mathbf a
+2\operatorname{Re}\{\mathbf a^H\mathbf P_n\Delta\mathbf a\}
+\mathbf a^H\Delta\mathbf P_n\mathbf a\\
&+\text{higher-order/cross terms}.
\end{aligned}
\]

At a true matched population source, \(\mathbf P_n\mathbf a=0\), so several first-order value terms vanish. Consequently the denominator value at the exact true direction can be second-order in small angular/subspace misalignment even though the **location of the minimum/peak can shift at first order**.

GeoDOA shall distinguish spectrum-value perturbation from peak-location perturbation.

---

## 30. First-order scalar DOA peak-shift relation

Let \(\theta_0\) be an isolated true source direction under a smooth one-dimensional manifold and assume the ideal denominator has a nondegenerate local minimum:

\[
D_0'(\theta_0)=0,
\qquad
D_0''(\theta_0)>0.
\]

For a small perturbed denominator,

\[
\boxed{
\Delta\theta
\approx
-\frac{\Delta D'(\theta_0)}{D_0''(\theta_0)}.
}
\]

For the ideal matched projector,

\[
\boxed{
D_0''(\theta_0)
=2\|\mathbf P_n\mathbf a_{\theta}\|_2^2
}
\]

with

\[
\mathbf a_{\theta}
=\frac{\partial\mathbf a}{\partial\theta}.
\]

To first order in search-manifold and noise-projector errors,

\[
\boxed{
\Delta D'(\theta_0)
\approx
2\operatorname{Re}
\left\{
\mathbf a_{\theta}^H
\left(
\mathbf P_n\Delta\mathbf a
+\Delta\mathbf P_n\mathbf a
\right)
\right\}.
}
\]

Hence

\[
\boxed{
\Delta\theta
\approx
-
\frac{
\operatorname{Re}\left\{
\mathbf a_{\theta}^H
(\mathbf P_n\Delta\mathbf a
+\Delta\mathbf P_n\mathbf a)
\right\}
}
{\|\mathbf P_n\mathbf a_{\theta}\|_2^2}.
}
\]

This is a local first-order specialization, not a universal MUSIC bias formula. It requires a smooth isolated minimum, small perturbations, and a one-parameter direction model.

It reconciles the projective tangent concept from 3.11 with MUSIC peak sensitivity.

---

## 31. Interpretation of the first-order peak-shift formula

The numerator contains two different mechanisms:

\[
\boxed{
\mathbf P_n\Delta\mathbf a
}
\]

— error in the search/calibrated manifold projected into the ideal noise subspace;

and

\[
\boxed{
\Delta\mathbf P_n\mathbf a
}
\]

— rotation/error of the data-derived noise subspace acting on the ideal steering vector.

The denominator

\[
\boxed{
\|\mathbf P_n\mathbf a_{\theta}\|^2
}
\]

measures local projective manifold sensitivity to DOA.

A direction where this denominator is small is intrinsically more sensitive to a given structured perturbation.

---

## 32. Closely spaced sources and eigengap sensitivity

As sources become difficult to resolve, covariance eigenstructure can become poorly separated and the effective signal/noise eigengap can shrink.

Davis–Kahan-type scaling then predicts greater subspace sensitivity for the same covariance perturbation.

Additionally, MUSIC peak curvature can weaken or adjacent minima can interact, invalidating a simple isolated-peak first-order approximation.

Therefore small sensor mismatch can be disproportionately damaging near resolution limits.

GeoDOA shall not derive global robustness conclusions from single-source broadside examples alone.

---

## 33. Source correlation and coherent sources

Source correlation changes \(\mathbf R_s\), eigenvalues, and potentially signal-subspace rank.

For full-rank correlated \(\mathbf R_s\), the signal subspace may retain the same dimension but eigenvalue spread/gap can change.

For coherent sources, \(\mathbf R_s\) can become rank deficient so classical covariance MUSIC may no longer expose one independent signal eigenvector per source.

Spatial smoothing or other decorrelation processing changes the covariance model and belongs to an explicitly declared estimator profile.

Sensor imperfection and source coherence shall not be conflated as one `rank problem`.

---

## 34. Finite-sample subspace error

Even with a perfectly calibrated physical manifold,

\[
\hat{\mathbf R}
=\mathbf R+\mathbf E_{\rm sample}
\]

produces eigenvalue/eigenspace perturbation.

The size/distribution of \(\mathbf E_{\rm sample}\) depends on snapshot count, source/noise distributions, temporal dependence, centering, and the physical covariance.

Therefore finite-sample MUSIC variability is a separate error family from deterministic calibration mismatch.

ADR-004 will govern Monte Carlo/statistical validation; ADR-003 preserves the physical distinction.

---

## 35. Mean-centering and sample-rank implications

The ADR-002 distinction between centered and uncentered covariance is inherited.

For a mean-centered data matrix with \(L\) snapshots, sample covariance rank cannot exceed \(L-1\) and also cannot exceed the number of sensor channels.

This algebraic rank ceiling is distinct from physical source-subspace rank and can affect eigenspace estimation at small snapshot counts.

Sensor calibration cannot recover sample rank that is absent because of the finite observation geometry/statistics.

---

## 36. Correction-before-covariance path

For linear data correction

\[
\mathbf y_{\rm corr}
=\mathbf C\mathbf y,
\]

the sample or population covariance transforms as

\[
\boxed{
\mathbf R_{\rm corr}
=\mathbf C\mathbf R_y\mathbf C^H
}
\]

when \(\mathbf C\) is fixed over the covariance window.

This changes signal subspace, noise covariance, eigenvalues, and conditioning according to \(\mathbf C\).

If \(\mathbf C\) is estimated with error, regularized, or time-varying, those effects require separate propagation.

---

## 37. Model-calibration path

If measured data are not transformed but MUSIC uses a calibrated manifold

\[
\mathbf a_{\rm cal}(\theta),
\]

then the data covariance remains the physical covariance.

Calibration affects the search-manifold term rather than directly applying a congruence transform to covariance.

Thus model calibration and data correction can yield different covariance/noise-subspace behavior even if both reduce nominal-manifold mismatch.

---

## 38. Inverse correction and subspace consequences

An inverse calibration may make the corrected deterministic manifold closer to nominal while amplifying or coloring noise:

\[
\mathbf R_{n,\rm corr}
=\mathbf C\mathbf R_n\mathbf C^H.
\]

If classical MUSIC then assumes white noise without whitening/model update, a deterministic calibration improvement can coexist with a statistical model violation.

Calibration quality must therefore be judged end-to-end, not only by steering-vector residual before/after correction.

---

## 39. Widely linear / improper complex covariance

For I/Q imbalance or improper complex processes, ordinary covariance may be insufficient.

Define

\[
\mathbf R_x=\operatorname E[\mathbf x\mathbf x^H],
\qquad
\mathbf P_x=\operatorname E[\mathbf x\mathbf x^T].
\]

The augmented vector

\[
\tilde{\mathbf x}
=\begin{bmatrix}\mathbf x\\\mathbf x^*\end{bmatrix}
\]

has augmented covariance

\[
\boxed{
\mathbf R_{\rm aug}
=\operatorname E[
\tilde{\mathbf x}\tilde{\mathbf x}^H]
=
\begin{bmatrix}
\mathbf R_x&\mathbf P_x\\
\mathbf P_x^*&\mathbf R_x^*
\end{bmatrix}.
}
\]

A widely-linear estimator may operate on this augmented eigenspace.

Classical ordinary-covariance MUSIC shall not silently claim compatibility when a declared receiver model requires augmented statistics.

---

## 40. Nonlinear receiver covariance

For a nonlinear sensor/receiver operator

\[
\mathbf y=\mathcal F(\mathbf x),
\]

the covariance is fundamentally

\[
\boxed{
\mathbf R_y
=\operatorname E[
\mathcal F(\mathbf x)
\mathcal F(\mathbf x)^H].
}
\]

No universal linear congruence transform exists.

Compression/intermodulation can also make the effective response depend on source amplitudes and joint source state, invalidating a fixed superposition manifold.

Any linearized covariance approximation shall declare its operating point and validity regime.

---

## 41. Quantized covariance

For exact ADC quantization

\[
\mathbf y=\mathcal Q(\mathbf z),
\]

covariance is

\[
\boxed{
\mathbf R_y
=\operatorname E[
\mathcal Q(\mathbf z)
\mathcal Q(\mathbf z)^H].
}
\]

Under a restricted high-resolution additive white quantization-noise approximation,

\[
\mathbf R_y
\approx
\mathbf R_z+\sigma_q^2\mathbf I,
\]

population eigenvectors are preserved.

For unequal, correlated, coarse, clipped, or one-bit quantization, that result does not hold generally.

One-bit/arcsine covariance methods belong to a specialized estimator profile rather than ordinary MUSIC by default.

---

## 42. Common phase, common gain, and covariance

For common scalar \(c\),

\[
\mathbf y=c\mathbf x
\]

gives

\[
\boxed{
\mathbf R_y
=|c|^2\mathbf R_x.
}
\]

Thus common phase cancels entirely from covariance, while common amplitude rescales covariance eigenvalues but does not rotate eigenvectors when it multiplies the entire vector uniformly.

However, common gain can still alter physical SNR, clipping, quantization, or nonlinear operating point before covariance is formed, so this covariance invariance does not make common gain universally irrelevant.

---

## 43. Differential phase/gain mismatch and eigenspaces

A diagonal non-scalar gain/phase matrix

\[
\mathbf G=\operatorname{diag}(g_1,\ldots,g_N)
\]

generally yields

\[
\mathbf R'_{\rm sig}
=\mathbf G\mathbf R_{\rm sig}\mathbf G^H
\]

with a rotated signal subspace relative to the nominal channel basis.

If \(\mathbf G\) is nonsingular, signal rank is preserved, but ideal steering vectors no longer lie in the physical signal subspace unless the model includes \(\mathbf G\).

---

## 44. Mutual coupling and eigenspaces

A nonsingular coupling/loading transform \(\mathbf C\) yields

\[
\boxed{
\mathbf R'_{\rm sig}
=\mathbf C\mathbf R_{\rm sig}\mathbf C^H.
}
\]

The column space becomes

\[
\boxed{
\mathcal R(\mathbf C\mathbf A)
}
\]

rather than \(\mathcal R(\mathbf A)\).

Therefore coupling can preserve source-signal rank while rotating the signal/noise subspaces enough to break nominal-manifold MUSIC orthogonality.

This is precisely the mechanism exercised by GRP-016/017.

---

## 45. Sensor location error and covariance

Position perturbations modify each source steering vector in a direction/frequency-dependent manner.

Consequently

\[
\Delta\mathbf A
\]

is generally structured and source dependent rather than one arbitrary random matrix.

Small deterministic location errors can therefore induce deterministic MUSIC bias even as snapshot count tends to infinity.

Finite-snapshot variance and deterministic asymptotic bias shall be reported separately.

---

## 46. Population mismatch can survive infinite snapshots

If

\[
L\rightarrow\infty
\]

under suitable stationarity/ergodicity assumptions, sample covariance can converge toward the physical population covariance.

But if the estimator continues using the wrong manifold/model,

\[
\boxed{
\mathbf a_{\rm model}
eq\mathbf a_{\rm phys},
}

the model mismatch does not vanish with more snapshots.

Therefore `more snapshots` reduces finite-sample error but does not calibrate a systematically incorrect array manifold.

---

## 47. Conversely, calibration does not eliminate finite-sample error

Even if

\[
\mathbf a_{\rm cal}=\mathbf a_{\rm phys}
\]

exactly, a finite sample covariance yields imperfect eigenspace estimates.

Thus perfect model calibration does not imply zero MUSIC RMSE at finite SNR/snapshot count.

This separation is essential for later fair validation experiments.

---

## 48. Spectrum-level diagnostics

A DOA audit shall not rely only on final peak locations.

Useful spectrum-level diagnostics can include:

- MUSIC denominator at true direction;
- normalized noise-subspace leakage;
- peak height/depth under declared normalization;
- local curvature near true/estimated peak;
- secondary/spurious peak structure;
- peak separation;
- grid/interpolation effects;
- out-of-domain manifold states.

Formal validation metrics and thresholds belong to ADR-004.

---

## 49. Grid error versus physical mismatch

A discrete MUSIC scan can introduce angle-grid error even with perfect covariance/manifold knowledge.

GeoDOA shall distinguish:

```text
physical sensor/manifold mismatch
covariance/eigenspace error
search-manifold interpolation error
MUSIC scan-grid discretization error
peak-refinement error
```

A coarse search grid shall not be mislabeled as sensor-calibration error.

---

## 50. Direction-coordinate dependence of peak sensitivity

The local curvature and tangent depend on the chosen search coordinate.

A derivative with respect to \(\theta\) differs from a derivative with respect to

\[
u=\sin\theta.
\]

Therefore first-order peak-shift formulas shall state the coordinate in which the derivative and bias are expressed.

Near endfire, conversion between \(u\)-error and angle error can strongly magnify angular bias because

\[
\frac{d\theta}{du}
=\frac{1}{\sqrt{1-u^2}}.
\]

---

## 51. Subspace dimension/model-order error

MUSIC requires a selected signal-subspace dimension or source count/model order.

If the chosen \(\hat q\) differs from the appropriate observed signal-subspace dimension, the resulting noise projector is structurally wrong even with an otherwise perfect manifold.

Model-order estimation belongs to estimator design/validation, but ADR-003 shall not attribute such errors automatically to sensor calibration.

---

## 52. Eigengap collapse and failure state

When signal/noise eigenvalue clusters overlap or the effective gap becomes too small relative to covariance perturbation, the subspace decomposition can become unstable.

Rather than returning a falsely precise `subspace_error`, GeoDOA shall be able to mark states such as

```text
well separated
weak eigengap / sensitive
cluster ambiguity
subspace dimension unresolved
outside perturbative regime
```

The exact software enum is deferred.

---

## 53. Perturbation bounds are diagnostics, not substitutes for validation

Davis–Kahan/Weyl/first-order formulas provide analytical insight and bounds, but they do not replace direct computation or Monte Carlo/experimental validation.

Bounds may be conservative, asymptotic expansions may fail for large mismatch, and real sensor effects can be nonlinear/time varying.

GeoDOA shall preserve whether a result is:

- exact identity;
- first-order approximation;
- norm bound;
- empirical estimate;
- Monte Carlo statistic;
- measured validation result.

---

## 54. Deterministic first-order covariance check

Let

\[
\mathbf a
=\begin{bmatrix}1\\1\end{bmatrix},
\qquad
\Delta\mathbf a
=\begin{bmatrix}0\\\epsilon\end{bmatrix},
\qquad
R_s=1.
\]

Then

\[
\mathbf R_{\rm sig}
=\mathbf a\mathbf a^H
=\begin{bmatrix}1&1\\1&1\end{bmatrix}.
\]

The first-order covariance perturbation is

\[
\Delta\mathbf R^{(1)}
=\Delta\mathbf a\mathbf a^H
+\mathbf a\Delta\mathbf a^H.
\]

For real \(\epsilon\),

\[
\boxed{
\Delta\mathbf R^{(1)}
=\begin{bmatrix}
0&\epsilon\\
\epsilon&2\epsilon
\end{bmatrix}.
}
\]

The exact covariance contains the additional second-order term

\[
\boxed{
\Delta\mathbf a\Delta\mathbf a^H
=\begin{bmatrix}
0&0\\0&\epsilon^2
\end{bmatrix}.
}
\]

This check makes the approximation boundary explicit.

---

## 55. Deterministic eigengap-sensitivity check

Consider two Hermitian matrices with the same off-diagonal perturbation magnitude \(\varepsilon\):

\[
\mathbf R_1
=\begin{bmatrix}10&0\\0&1\end{bmatrix},
\qquad
\mathbf R_2
=\begin{bmatrix}2&0\\0&1\end{bmatrix}.
\]

Apply

\[
\mathbf E
=\begin{bmatrix}0&\varepsilon\\\varepsilon&0\end{bmatrix}.
\]

For the dominant eigenvector, the small-angle first-order mixing coefficient scales as

\[
\boxed{
\frac{\varepsilon}{\lambda_1-\lambda_2}.
}
\]

Thus the corresponding scales are approximately

\[
\frac{\varepsilon}{9}
\quad\text{and}\quad
\varepsilon,
\]

showing nine-times larger first-order rotation scale for the smaller-gap example.

This is an exploration check, not a formal GRP number.

---

## 56. Deterministic model-versus-data mismatch check

Suppose the data covariance is perfectly known and generated by unit physical steering vector \(\mathbf u\), but MUSIC searches with unit model vector \(\mathbf v\).

Even with infinite snapshots,

\[
\boxed{
D(\theta_0)
=\mathbf v^H
(\mathbf I-\mathbf u\mathbf u^H)
\mathbf v
=1-|\mathbf u^H\mathbf v|^2.
}
\]

Hence nonzero denominator at the true direction can be caused by deterministic model mismatch alone.

No sample-covariance error is required.

---

## 57. Scientific anchors for this exploration

The contract is consistent with classical subspace perturbation and MUSIC sensitivity theory.

Representative anchors include:

- C. Davis and W. M. Kahan, **The Rotation of Eigenvectors by a Perturbation. III**, SIAM Journal on Numerical Analysis, vol. 7, no. 1, pp. 1–46, 1970, DOI: 10.1137/0707001 — invariant-subspace rotation and sin-\(\Theta\) bounds under spectral separation.
- R. O. Schmidt, **Multiple Emitter Location and Signal Parameter Estimation**, IEEE Transactions on Antennas and Propagation, vol. 34, no. 3, pp. 276–280, 1986, DOI: 10.1109/TAP.1986.1143830 — MUSIC signal/noise-subspace formulation.
- B. Friedlander, **A Sensitivity Analysis of the MUSIC Algorithm**, IEEE Transactions on Acoustics, Speech, and Signal Processing, vol. 38, no. 10, pp. 1740–1751, 1990, DOI: 10.1109/29.60105 — first-order MUSIC sensitivity to mismatch between true and assumed array manifolds.
- M. Wang, Z. Zhang, and A. Nehorai, **Performance Analysis of Coarray-Based MUSIC in the Presence of Sensor Location Errors**, IEEE Transactions on Signal Processing, 2018 — deterministic sensor-location mismatch propagated to MUSIC performance.
- Classical Hermitian eigenvalue perturbation theory, including Weyl-type eigenvalue bounds and principal-angle/projector formulations.

These references support the scientific structure; GeoDOA's exact profile semantics, metrics, approximation boundaries, and acceptance thresholds remain project decisions subject to Gates A–F.

---

## 58. Candidate decisions from Exploration 3.12

- **3.12-D1** — Nominal population covariance, physical population covariance, and finite-sample covariance are distinct scientific objects.
- **3.12-D2** — Sensor covariance distortion \(\mathbf E_{\rm sensor}\) and finite-sample covariance error \(\mathbf E_{\rm sample}\) shall be separately represented even though their sum equals total sample-versus-nominal error.
- **3.12-D3** — Additive bookkeeping of covariance errors does not imply statistical independence; sample-error statistics depend on the physical covariance.
- **3.12-D4** — Manifold perturbation propagates exactly through quadratic covariance expansion and admits a first-order form only in a declared small-error regime.
- **3.12-D5** — Linear sensor transforms propagate covariance by congruence only for the stages they physically transform; downstream noise injection remains separate.
- **3.12-D6** — The 3.2 commutator form for small phase error is reconciled as a specialization of linear covariance perturbation.
- **3.12-D7** — Signal-covariance distortion and noise-covariance distortion are separate terms and shall be independently diagnosable.
- **3.12-D8** — Exact isotropic additive noise \(\sigma^2\mathbf I\) shifts population eigenvalues without rotating population eigenvectors.
- **3.12-D9** — Unequal/colored noise generally changes ordinary covariance eigenspaces and may invalidate standard white-noise MUSIC assumptions.
- **3.12-D10** — Whitening requires positive-definite/compatible noise covariance and consistent transformation of both data covariance and steering manifold.
- **3.12-D11** — Source count, source-covariance rank, signal-covariance rank, observed signal-subspace dimension, and sample-covariance rank remain distinct.
- **3.12-D12** — Nonsingular deterministic sensor transforms preserve signal-covariance rank but can rotate subspaces and alter eigenvalues/conditioning.
- **3.12-D13** — Rank-deficient sensor transforms can reduce observable signal rank.
- **3.12-D14** — Unitary sensor transforms preserve covariance eigenvalues while rotating eigenvectors; general nonsingular congruence does not preserve eigenvalues in general.
- **3.12-D15** — Common phase cancels from covariance; common amplitude scales covariance but does not by itself rotate eigenspaces in the linear common-scalar specialization.
- **3.12-D16** — A time-varying sensor/manifold state across a covariance window cannot generally be represented by one averaged static operator.
- **3.12-D17** — Time averaging of differently oriented low-rank covariances can increase apparent covariance rank and create additional modes.
- **3.12-D18** — Hermitian covariance eigenvalue error is bounded in operator norm by Weyl-type perturbation results.
- **3.12-D19** — First-order simple-eigenvector perturbation is inversely proportional to eigenvalue separation and is not the correct object for repeated/clustered eigenvalues.
- **3.12-D20** — Signal/noise eigenspace perturbation shall be measured using principal-angle/projector concepts rather than arbitrary eigenvector-column differences.
- **3.12-D21** — Davis–Kahan-type subspace bounds scale with perturbation magnitude relative to an appropriate spectral gap, subject to theorem-specific assumptions.
- **3.12-D22** — Population and sample eigengaps are distinct and shall not be silently substituted for one another.
- **3.12-D23** — Cross-block covariance perturbation \(\mathbf U_n^H\mathbf E\mathbf U_s\) is the first-order driver of signal/noise subspace mixing.
- **3.12-D24** — Projector metrics remove arbitrary basis rotations within equal-dimensional subspaces and are first-class eigenspace diagnostics.
- **3.12-D25** — Under matched population classical MUSIC, physical steering vectors lie in the signal subspace and are orthogonal to the noise subspace.
- **3.12-D26** — In the rank-one population case, normalized MUSIC denominator at the true source equals the 3.11 projective leakage \(1-\rho^2\).
- **3.12-D27** — GRP-016/017 coupling seeds reconcile to normalized nominal-manifold leakage 0.2 against the physical coupled noise subspace and remain reserved for formal Gate-E evidence.
- **3.12-D28** — Isotropic white-noise addition in GRP-017 raises eigenvalues from \(\{2.5,0\}\) to \(\{3.5,1\}\) without changing the coupled population eigenvectors.
- **3.12-D29** — Data/noise-subspace perturbation and search-manifold perturbation are distinct MUSIC mismatch channels.
- **3.12-D30** — MUSIC denominator value perturbation and MUSIC peak-location perturbation are distinct; the denominator at the exact true point can be second-order while peak bias is first-order.
- **3.12-D31** — Under a smooth isolated one-dimensional peak, first-order DOA shift may be expressed through the derivative perturbation divided by ideal local curvature.
- **3.12-D32** — The first-order MUSIC peak-shift numerator separates search-manifold leakage from data-derived noise-projector rotation.
- **3.12-D33** — Local MUSIC sensitivity depends on the projective manifold tangent/curvature and therefore on direction/search coordinate.
- **3.12-D34** — Closely spaced sources/small eigengaps can amplify subspace sensitivity and invalidate simple isolated-peak approximations.
- **3.12-D35** — Source correlation and coherent-source rank loss are distinct from sensor imperfection and require explicit covariance/estimator treatment.
- **3.12-D36** — Finite-sample eigenspace error remains even under perfect calibration and is a separate stochastic error family.
- **3.12-D37** — Mean-centered sample-covariance rank ceilings are algebraic finite-sample constraints, not physical source-count statements.
- **3.12-D38** — Fixed linear data correction transforms covariance by \(\mathbf C\mathbf R\mathbf C^H\) and therefore transforms both signal and noise subspaces/statistics.
- **3.12-D39** — Model calibration changes the search manifold without directly changing the measured covariance; it is not statistically identical to data correction.
- **3.12-D40** — Inverse correction can reduce deterministic manifold mismatch while worsening noise color/amplification; downstream estimator compatibility must be re-evaluated.
- **3.12-D41** — Widely-linear/IQ-impaired profiles may require augmented covariance with pseudocovariance and are not automatically compatible with ordinary MUSIC.
- **3.12-D42** — Nonlinear receiver covariance is defined through direct expectation of the nonlinear output and cannot generally be reduced to linear congruence.
- **3.12-D43** — Exact/coarse/one-bit quantization requires quantized-statistics treatment; white additive quantization noise is only a restricted approximation.
- **3.12-D44** — Differential channel gain/phase and mutual coupling can preserve rank while rotating the physical signal subspace away from the nominal manifold subspace.
- **3.12-D45** — Position errors induce structured direction/frequency-dependent manifold and covariance perturbations and can cause deterministic asymptotic MUSIC bias.
- **3.12-D46** — Increasing snapshot count can reduce finite-sample error but does not remove deterministic sensor/manifold mismatch.
- **3.12-D47** — Perfect calibration does not eliminate finite-sample MUSIC variance at finite SNR/snapshot count.
- **3.12-D48** — Spectrum-level diagnostics shall complement final peak/DOA metrics so failure mechanisms remain observable.
- **3.12-D49** — MUSIC scan-grid/interpolation error shall remain distinct from physical calibration and covariance/eigenspace errors.
- **3.12-D50** — First-order DOA sensitivity/bias formulas shall state the direction coordinate (angle, direction cosine, etc.) used by derivatives.
- **3.12-D51** — Incorrect signal-subspace dimension/model order is a separate estimator failure source and shall not automatically be attributed to calibration.
- **3.12-D52** — Eigengap collapse/cluster overlap shall permit structured sensitive/ambiguous/outside-perturbative-regime status rather than false precision.
- **3.12-D53** — Perturbation identities, first-order approximations, norm bounds, Monte Carlo results, and measured validation evidence are distinct evidence types.
- **3.12-D54** — The initial ideal Phase-1 profile shall use matched white-noise population/subspace semantics while preserving explicit finite-sample covariance behavior.

---

## 59. Immediate next step

The next work session shall start at **Exploration 3.13 — Compatibility and Initial ADR-003 Profile**.

Exploration 3.13 must reconcile at least:

1. complete estimator-compatibility matrix across 3.1–3.12;
2. ideal versus imperfect sensor profiles;
3. which imperfections remain compatible with classical MUSIC after model update;
4. which require data correction/whitening;
5. which require augmented/widely-linear processing;
6. which require wideband/time-varying processing;
7. which invalidate linear superposition or covariance MUSIC;
8. measured/CST manifold compatibility;
9. calibration-domain and reference-plane compatibility;
10. active-channel/port-state compatibility;
11. quantization-resolution regimes;
12. source/noise/statistical compatibility;
13. explicit initial Phase-1 ADR-003 sensor profile;
14. deferred imperfection profiles and implementation boundaries;
15. warning/reject/degraded-mode semantics;
16. candidate compatibility tests to be promoted to formal Gate evidence later.

Do not start Gate A yet.
