A. Complete model
=================

A.1 Description
---------------

Suppose the value function is :math:`V`. State variable:
:math:`x = (\log k, z, y, n)` (realization of
:math:`\log K, \log N, Y, Z`), control variable : :math:`(\tilde e, i)`.
Suppose the value function is separable as follows:

.. math::


       V(\log k, n, y, z) = v_k \log k + \zeta(z) + \phi(y) + v_n n

Consider the model without jump misspecification with damage function

.. math::


   \Lambda (y)  = \gamma_1 y + \frac{\gamma_2}{2}y^2 + \frac{\gamma_3}{2} (y - \bar y)^2 \mathbb{I}\{y > \bar y\}

For models with jump misspecification, the modification can be make to
:math:`(y,n)` without affecting :math:`(\log k, z)`, as the HJB is
separable. The complete HJB is as follows:

.. math::


   \begin{aligned}
    0 = \max_{\tilde e, i }\min_{\omega_\ell:\sum_{\ell=1}^L \omega_\ell = 1} \min_{h}\quad & - \delta V + (1 - \eta) [\log(\alpha - i) + \log k - n] + \eta \log \tilde e \\ 
    & + v_k \cdot \left[\mu_k(z) + i  - \frac{\kappa}{2} i^2  - \frac{|\sigma_k(z)|^2}{2} + \sigma_k(z)' h \right] \\ 
    & + \frac{\partial \zeta }{\partial z}(z)\cdot \left[\mu_z(z) + \sigma_z(z)'h \right] + \frac{1}{2} trace\left[\sigma_z(z)' \frac{\partial^2 \zeta(z)}{\partial z\partial z'} \sigma_z(z)'\right] \\
    & + \frac{d \phi(y)}{dy} \sum_{\ell=1}^L \omega_\ell\cdot \tilde e\cdot\theta_\ell + \frac12 \frac{d^2 \phi(y)}{dy^2} (\tilde e)^2 |\varsigma|^2\\
    & + v_n \left[(\gamma_1 + \gamma_2 y + \gamma_3 (y-\bar y)\mathbb{I}\{y > \bar y\}) (\sum_{\ell=1}^L \omega_\ell \theta_\ell \tilde e  + \tilde e \varsigma' h )+ \frac12 \left(\gamma_2 + \gamma_3 \mathbb{I}\{y > \bar y\} \right)\cdot |\varsigma|^2 (\tilde e)^2 \right]  \\
    & + \frac{\xi_b}{2} h'h + \xi_a \sum_{\ell=1}^L \omega_\ell \left( \log \omega_\ell - \log \pi^a_\ell \right)
   \end{aligned}

A.2 Consumption-capital dynamics
--------------------------------

The undamaged version of consumption capital model has a straightforward
solution. The HJB equation for this component is:

.. math::


   \begin{aligned}
    0 = \max_{ i } \min_{h}\quad & - \delta \left[ v_k \log k + \zeta(z)\right] + (1 - \eta) [\log(\alpha - i) + \log k - n] +  \frac{\xi_b}{2} h'h \\ 
    & + v_k \cdot \left[\mu_k(z) + i  - \frac{\kappa}{2} i^2  - \frac{|\sigma_k(z)|^2}{2} + \sigma_k(z)' h \right] \\ 
    & + \frac{\partial \zeta }{\partial z}(z)\cdot \left[\mu_z(z) + \sigma_z(z)'h \right] + \frac{1}{2} trace\left[\sigma_z(z)' \frac{\partial^2 \zeta(z)}{\partial z\partial z'} \sigma_z(z)'\right] \\
   \end{aligned}

Coefficients of :math:`\log k` satisfy that

.. math::


   -\delta v_k + (1 - \eta) = 0 \quad \Longrightarrow \quad v_k = \frac{1 - \eta}{\delta}

The first order condition for the investment-capital ratio is

.. math::


    - (1 - \eta) \frac{1}{\alpha - i} + v_k (1 - \kappa i) = 0\quad \Longrightarrow \quad - \frac{1}{\alpha -i} + \frac{1 - \kappa i}{\delta} = 0

The first order condition for :math:`h` is:

.. math::


   \xi_b h + \sigma_k v_k + \sigma_z \frac{\partial \zeta}{\partial z} = 0

and is therefore:

.. math::


   h = - \frac{1}{\xi_b} \left[ \sigma_k v_k + \sigma_k \frac{\partial \zeta}{\partial z}\right]

B. Computation methods
======================

The HJB for :math:`(y, n)` component does not has a straightforward
solution. We use **false transient method** to solve the ODEs concerning
:math:`(y,n)` in this paper.

Take a general HJB that takes into consideration smooth ambiguity and
brownian misspecification. Here we leave out the subscription :math:`m`
in :math:`\phi(y)` as well as the upscription in :math:`\gamma_3`.

Recall that one HJB of interest for a damage specification
:math:`\gamma_3` is:

.. math::


   \begin{aligned}
   0 = \max_{\tilde e} \min_{\omega^a_\ell : \sum_{\ell=1}^L \omega^a_\ell = 1}  &- \delta \phi(y) +  \eta \log\tilde e \\
   & + \frac{1}{2} \left(\frac{d^2 \phi}{dy^2} + \frac{ (\eta - 1)}{\delta} \left(\gamma_2 + \gamma_3\mathbb{I}\{y>\bar y\} \right) \right)(\tilde e)^2 |\varsigma|^2  \\
   & - \frac{1}{2\xi_b} \left[ \frac{d\phi}{dy}    + \frac{(\eta -1)}{\delta}(\gamma_1 + \gamma_2 y + \gamma_3 (y-\bar y)\mathbb{I}\{y > \bar y\})\right]^2 \cdot |\varsigma|^2 (\tilde e)^2 \\
   \\
   & + \sum_{\ell=1}^{L} \omega_\ell^a \left(\frac{d\phi}{dy}+ \frac{(\eta -1)}{\delta}(\gamma_1 + \gamma_2 y + \gamma_3 (y - \bar y)\mathbb{I}\{y > \bar y\} ) \right)\theta_\ell \tilde e   \\
   \\
   & + \xi_a \sum_i \omega^a_\ell(\log \omega^a_\ell - \log \pi^a_\ell)
   \end{aligned}

The problem satisfies condition to switch max and min problem. In the
code, we first compute the optimal :math:`\tilde e` and then the
optimizing :math:`\omega_\ell`, so we follow this order here.

The settup includes a tolerance level, :math:`tolerance`, that defines
*convergence* and a constant step size, :math:`\epsilon`, for updating
the value function.

We start with an initial guess of value function :math:`\phi_0(y)` and
initial values of :math:`\{ \omega_\ell\}_{\ell=1}^L`, and update the
value function according to the following way: 1. For a given
:math:`\color{blue}{\phi_i(y)}`, compute the optimizing :math:`\tilde e`
according to its first order condition:

.. math::


   \begin{aligned}
   0 = &\frac{\eta}{\color{blue}{\tilde e}} + \sum_{\ell=1}^{L} \omega_\ell^a \left(\color{blue}{\frac{d\phi_i}{dy}}+ \frac{(\eta -1)}{\delta}(\gamma_1 + \gamma_2 y + \gamma_3 (y - \bar y)\mathbb{I}\{y > \bar y\} ) \right)\theta_\ell  \\
    & +  \left(\color{blue}{\frac{d^2 \phi_i}{dy^2}} + \frac{ (\eta - 1)}{\delta} \left(\gamma_2 + \gamma_3 \mathbb{I}\{y>\bar y\} \right)  - \frac{1}{\xi_b} \left[ \color{blue}{\frac{d\phi_i}{dy}} + \frac{(\eta -1)}{\delta}(\gamma_1 + \gamma_2 y + \gamma_3 (y-\bar y)\mathbb{I}\{y > \bar y\})\right]^2 \right)|\varsigma|^2 \color{blue}{\tilde e} 
   \end{aligned}

2. After compute the optimizing :math:`\tilde e` from above, we compute
   the optimizing :math:`\omega_\ell` according to its first order
   condition:

.. math::


    \color{blue}{\omega_\ell} = \frac{\pi_\ell^a \exp\left( -\frac{1}{\xi_a}\left[ \color{blue}{\frac{d\phi_i}{dy}} + \frac{(\eta -1)}{\delta}(\gamma_1 + \gamma_2 y + \gamma_3 (y - \bar y)\mathbb{I}\{y > \bar y\} )\right] \color{blue}{\tilde e} \cdot \theta_\ell \right)}{\sum_{\ell=1}^L \pi_\ell^a \exp\left( -\frac{1}{\xi_a}\left[ \color{blue}{\frac{d\phi_i}{dy}}+ \frac{(\eta -1)}{\delta}(\gamma_1 + \gamma_2 y + \gamma_3 (y - \bar y)\mathbb{I}\{y > \bar y\} )\right]\color{blue}{\tilde e} \cdot \theta_\ell \right)}, \quad \ell = 1,2,\dots,L

3. Plug the above computed :math:`\tilde e` and
   :math:`\{\omega_\ell\}_{\ell=1}^L` back into the above HJB. Update
   :math:`\phi_i(y)` to :math:`\phi_{i+1}(y)` by solving the following
   ODE:

   .. math::


       \begin{aligned}
       \frac{\color{red}{\phi_{i+1}(y)} - \color{blue}{\phi_i(y)}}{\epsilon} =   &- \delta \color{red}{\phi_{i+1}(y)} +  \eta \log\color{blue}{\tilde e} \\
       & + \frac{1}{2} \left(\color{red}{\frac{d^2 \phi_{i+1}}{dy^2}} + \frac{ (\eta - 1)}{\delta} \left(\gamma_2 + \gamma_3\mathbb{I}\{y>\bar y\} \right) \right)(\color{blue}{\tilde e})^2 |\varsigma|^2  \\
       & - \frac{1}{2\xi_b} \left[ \color{red}{\frac{d\phi_{i+1}}{dy}}    + \frac{(\eta -1)}{\delta}(\gamma_1 + \gamma_2 y + \gamma_3 (y-\bar y)\mathbb{I}\{y > \bar y\})\right]^2 \cdot |\varsigma|^2 (\color{blue}{\tilde e})^2 \\
       \\
       & + \sum_{\ell=1}^{L} \color{blue}{\omega_\ell^a} \left(\color{red}{\frac{d\phi_{i+1}}{dy}} + \frac{(\eta -1)}{\delta}(\gamma_1 + \gamma_2 y + \gamma_3 (y - \bar y)\mathbb{I}\{y > \bar y\} ) \right)\theta_\ell \color{blue}{\tilde e}   \\
       \\
       & + \xi_a \sum_i \color{blue}{\omega^a_\ell}(\log\color{blue}{\omega^a_\ell} - \log \pi^a_\ell)
       \end{aligned}
       

   Blued :math:`\color{blue}{\tilde e}` and
   :math:`\color{blue}{\omega_\ell}` indicate they are computed using
   :math:`\color{blue}{\phi_i(y)}`.

   The method we use to solve the ODE is **biconjugate-gradient
   method**. Use ``?scipy.sparse.linalg.bicg`` for document. See also
   wiki page for `biconjugate gradient
   method <https://en.wikipedia.org/wiki/Biconjugate_gradient_method>`__.

4. Check whether the convergence condition is satisfied. We call
   left-hand side formula *left-hand side error*. Set a tolerance level,
   :math:`tolerance`. We say that the algorithm converges, if:

   .. math::


       \frac{|\color{red}{\phi_{i+1}(y)} - \color{blue}{\phi_i(y)}| }{\epsilon} < tolerance
       

   and we get the solution :math:`\phi(y) = \phi_{i+1}(y)`. Otherwise,
   assign :math:`\phi_{i+1}(y)` to :math:`\phi_i(y)`, and repeat step
   1-4.

.. code:: ipython3

    # core loop in functions in `source/` can be described as follows
    An initial guess: ϕ
    Intial values of distorted probabibity of ω_ℓ: πc_o
    constant step size: ϵ
    tolerance level: tol
    left hand error = 1 # random value larger than tol
    report numbers of iteration: episode = 0
    while left hand side error > tol:
        compute  dϕdy # first crder derivative
        compute dϕdyy # second order derivative
        compute e_tilde
        compute optimizing ω_ℓ: πc
        solve the ODE by conjugate gradient to get ϕ_new
        update left hand error
        compute right hand error
        ϕ = ϕ_new
        episode += 1
