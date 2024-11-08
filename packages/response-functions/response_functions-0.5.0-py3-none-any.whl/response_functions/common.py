import numpy as np
from scipy.special import gamma, erf
from mpmath import polylog
from mpmath import exp as mpexp


def unit_sphere_volume(dim):
    r"""returns \Omega_D such that the volume of a D-dimensional sphere
    of radius r is \Omega_D r^D"""
    return (np.pi ** (dim / 2.0)) / (gamma(1 + dim / 2.0))


def unit_sphere_surface(dim):
    r"""returns S_D such that the surface of a D-dimensional sphere
    of radius r is S_D r^(D-1)"""
    return dim * unit_sphere_volume(dim)


def fermi_dirac_int(s, x):
    r"""returns $F_s(x) = 1/\Gamma(1+s) \int_0^\infty t^s/(1+e^(t-x))dt
    = -Li_{s+1}(-e^x)"""
    return -float(polylog(s + 1, -mpexp(x)))


def fermi_function(E, T):
    """
    Returns Fermi-Dirac function $f(E, T)=\frac{1}{1+\exp[E/T]}$
    correctly handling T=0
    """
    if T != 0.0:
        return 0.5 - 0.5 * np.tanh(0.5 * E / T)
    else:
        return 0.5 - 0.5 * np.sign(E)


def delta_function(x, eta, shape="fermi"):
    """returns different types of function converging to a Dirac delta
    function as the parameter eta goes to 0"""
    if shape == "fermi":
        return 1.0 / eta * 0.25 * (1.0 - (np.tanh(x / (2.0 * eta))) ** 2)
    if shape == "lorentz":
        return eta / (np.pi * (x**2 + eta**2))
    if shape == "gauss":
        return np.exp(-(x**2) / (2.0 * eta**2)) / (eta * np.sqrt(2.0 * np.pi))
    if shape == "wigner":
        return 2.0 / (np.pi * eta**2) * np.real(np.sqrt(eta**2 - x**2 + 0.0j))


def theta_function(x, eta, shape="fermi"):
    """returns different types of function converging to a Dirac delta
    function as the parameter eta goes to 0"""
    if shape == "fermi":
        return 0.5 * (1 + np.tanh(x / (2.0 * eta)))
    if shape == "lorentz":
        return 0.5 + 1 / np.pi * np.arctan(x / eta)
    if shape == "gauss":
        return 0.5 * (1 + erf(x / (np.sqrt(2) * eta)))
    if shape == "wigner":
        return 0.5 + 1 / np.pi * np.real(
            np.arcsin(x / eta + 0.0j) + x / eta**2 * np.sqrt(eta**2 - x**2 + 0.0j)
        )


def average_maldague(
    funct,
    chemical_potential,
    temperature,
    sampling=None,
    weights=None,
    num=51,
    quadrature="uniform",
):
    """
    Performs the Maldague integral

    $$I(f, \mu, T) = \int_{-\infty}^\infty dx/(4 \cosh^2 (x/2)) f(\mu + k_B T x)$$

    by approxximating it as

    $$I(f, \mu, T)\approx \sum_i f(\mu + k_B T *sampling_i) weights_i $$

    If sampling and weights are not provided they will be calculated from a
    quadrature of the transformed integral
    $$ I(f, \mu, T) = \frac{1}{2}\int_{-1}^1 dy f(\mu + k_B T * 2*\artanh(y))$$
    using num sampling points.

    Available quadrature are
        - 'gauss_legendre'
            Gauss-Legendre quadrature of order num on [-1,1]
        - 'uniform'
            num uniformely spaced points in [-1+1/num, 1-1/num],
            i.e -1+1/num +2i/num with i = 0...num-1

    """
    if (sampling is None) and (weights is None):
        if quadrature == "gauss-legendre":
            y, w = np.polynomial.legendre.leggauss(num)
            sampling = 2 * np.arctanh(y)
            weights = 0.5 * w
        elif quadrature == "uniform":
            y = np.linspace(-1 + 1.0 / num, 1 - 1.0 / num, num)
            sampling = 2 * np.arctanh(y)
            weights = np.ones([num]) / num
        else:
            raise ValueError("Unknown quadrature type {}".format(quadrature))
    return np.tensordot(
        weights,
        np.array([funct(chemical_potential + temperature * xi) for xi in sampling]),
        axes=1,
    )


# def _average_maldague(funct, chemical_potential, temperature, num = 101, sampling = None):
#     if sampling is None:
#         y, w = np.polynomial.legendre.leggauss(num)
#         x = 2*np.arctanh(y)
#         I =0.5 * np.tensordot(w, np.array([funct(chemical_potential + temperature * xi) for xi in x]), axes = 1)
#         return I
#     else:
#         chi_sample = np.array([funct(chemical_potential + y) for y in sampling])
#         factor = np.expand_dims(1./(4. * temperature * np.cosh(0.5 * sampling /temperature)**2), axis = [i for i in range(1, chi_sample.ndim)])
#         return np.trapz(chi_sample * factor, x = sampling, axis = 0)


def lor(omega, omega_r, gamma):
    """
    Lorentz shape - damped oscillator. (see source for definition)
    Used for vibrational modes in permittivities.
    """
    return (omega_r**2) / (omega_r**2 - 1.0j * omega * gamma - omega**2)
