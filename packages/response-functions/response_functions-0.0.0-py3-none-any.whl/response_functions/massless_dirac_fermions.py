import numpy as np
from warnings import warn
from scipy.optimize import root_scalar
from scipy.special import loggamma

import response_functions.common as cm


class Massless_Dirac_Fermions:
    def __init__(
        self,
        hv,
        degeneracy,
        density,
        temperature,
        dimension=2,
        maldague_sampling=None,
        maldague_weights=None,
        maldague_num=101,
        maldague_quadrature="gauss-legendre",
    ):
        if dimension != 2:
            raise NotImplementedError("Only 2D Dirac Fermions available")
        self._dimension = dimension
        self._degeneracy = degeneracy
        self._hv = hv

        self._density = density
        self._temperature = temperature
        self._chemical_potential = self.compute_chemical_potential(density, temperature)

        self._kf = self.compute_fermi_wavevector(density)
        self._ef = self.compute_fermi_energy(density)

        self.maldague_num = maldague_num
        self.maldague_quadrature = maldague_quadrature
        self.maldague_sampling = maldague_sampling
        self.maldague_weights = maldague_weights

    # static properties
    @property
    def dimension(self):
        return self._dimension

    @dimension.setter
    def dimension(self, value):
        warn("dimension cannot be changed")

    @property
    def degeneracy(self):
        return self._degeneracy

    @degeneracy.setter
    def degeneracy(self, value):
        warn("degeneracy cannot be changed")

    #
    @property
    def hv(self):
        return self._hv

    @hv.setter
    def hv(self, value):
        warn("hv cannot be changed")

    ### dynamic properties
    @property
    def density(self):
        return self._density

    @density.setter
    def density(self, value):
        self._density = value
        self._chemical_potential = self.compute_chemical_potential(
            value, self._temperature
        )
        self._kf = self.compute_fermi_wavevector(self._density)
        self._ef = self.compute_fermi_energy(self._density)

    @property
    def chemical_potential(self):
        return self._chemical_potential

    @chemical_potential.setter
    def chemical_potential(self, value):
        self._chemical_potential = value
        self._density = self.compute_density(value, self._temperature)
        self._kf = self.compute_fermi_wavevector(self._density)
        self._ef = self.compute_fermi_energy(self._density)

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, value):
        self._temperature = value
        self._chemical_potential = self.compute_chemical_potential(self._density, value)

    @property
    def kf(self):
        return self._kf

    @kf.setter
    def kf(self, value):
        warn("kf cannot be changed, change density instead")

    @property
    def ef(self):
        return self._ef

    @ef.setter
    def ef(self, value):
        warn("ef cannot be changed, change density instead")

    ### functions
    def compute_fermi_wavevector(self, density):
        return (
            2.0
            * np.pi
            * np.power(
                abs(density)
                / (self._degeneracy * cm.unit_sphere_volume(self._dimension)),
                1.0 / self._dimension,
            )
        )

    def compute_fermi_energy(self, density):
        return self._hv * np.sign(density) * self.compute_fermi_wavevector(density)

    def compute_chemical_potential(self, density, temperature):
        if temperature == 0.0:
            return self.compute_fermi_energy(density)
        else:
            sol = root_scalar(
                lambda mu: self.compute_density(mu, temperature) - density,
                bracket=[0, self.compute_fermi_energy(density)],
            )
            return sol.root

    def compute_density(self, chemical_potential, temperature):
        if temperature == 0.0:
            return (
                (
                    self._degeneracy
                    * cm.unit_sphere_volume(self._dimension)
                    / ((2.0 * np.pi) ** self._dimension)
                )
                * np.sign(chemical_potential)
                * (abs(chemical_potential) / self._hv) ** self._dimension
            )
        else:
            ne = (
                (self._degeneracy / (2.0 * np.pi * self._hv**2))
                * temperature**2
                * cm.fermi_dirac_int(1, chemical_potential / temperature)
            )
            nh = (
                (self._degeneracy / (2.0 * np.pi * self._hv**2))
                * temperature**2
                * cm.fermi_dirac_int(1, -chemical_potential / temperature)
            )
            return ne - nh

    def dos(self, energy):
        return (self._degeneracy / (2.0 * np.pi * self._hv**2)) * abs(energy)

    @staticmethod
    def G(z):
        z = z + 0.0j
        sz2m1 = np.sqrt(z - 1.0) * np.sqrt(z + 1.0)
        return z * sz2m1 - np.log(z + sz2m1)

    def polarization(self, omega, q, chemical_potential=None, temperature=None):
        """polarization bubble. Identical to \chi_nn for \gamma=0"""
        if temperature is None:
            temperature = self.temperature
        if chemical_potential is None:
            chemical_potential = self.chemical_potential
            kf = self._kf
        else:
            kf = self.compute_fermi_wavevector(
                self.compute_density(chemical_potential, temperature)
            )
        if temperature == 0.0:
            omega = np.expand_dims(np.atleast_1d(omega), 0)
            q = np.expand_dims(np.atleast_1d(q), 1)
            Dplus = (omega / self._hv + 2.0 * kf) / q
            Dminus = (omega / self._hv - 2.0 * kf) / q

            it1 = 8.0 * kf / (self._hv * q**2)
            it2 = (
                np.where(
                    np.real(Dminus) < -1.0,
                    self.G(-Dminus),  # low w and low k
                    self.G(Dminus) + 1.0j * np.pi,  # high w or high k
                )
                - self.G(Dplus)
            ) / np.sqrt(0.0j + omega**2 - self._hv**2 * q**2)

            return np.squeeze(-self.degeneracy / (16 * np.pi) * (it1 + it2) * q**2)
        else:
            return cm.average_maldague(
                lambda mu: self.polarization(
                    omega=omega, q=q, chemical_potential=mu, temperature=0.0
                ),
                chemical_potential=chemical_potential,
                temperature=temperature,
                num=self.maldague_num,
                quadrature=self.maldague_quadrature,
                sampling=self.maldague_sampling,
                weights=self.maldague_weights,
            )

    def chi_nn(self, omega, q, gamma=0, chemical_potential=None, temperature=None):
        """Density response. Decay rate \gamma taken into account via Mermin approximation"""
        assert np.all(np.imag(omega) == 0.0)
        if gamma == 0.0:
            return self.polarization(
                omega=omega,
                q=q,
                chemical_potential=chemical_potential,
                temperature=temperature,
            )
        else:
            chi1 = self.polarization(
                omega=omega + 1j * gamma,
                q=q,
                chemical_potential=chemical_potential,
                temperature=temperature,
            )
            chi2 = self.polarization(
                omega=0,
                q=q,
                chemical_potential=chemical_potential,
                temperature=temperature,
            )
            omega = np.expand_dims(np.atleast_1d(omega), 0)
            q = np.expand_dims(np.atleast_1d(q), 1)
            chi2 = np.expand_dims(np.atleast_1d(chi2), 1)
            return (omega + 1j * gamma) / (omega / chi1 + 1j * gamma / chi2)

    def chi_L(self, omega, q, chemical_potential=None, temperature=None):
        """\chi_L(q,\omega) = \omega^2/q^2 \Pi(q,\omega)"""
        omega_ = np.expand_dims(np.atleast_1d(omega), 0)
        q_ = np.expand_dims(np.atleast_1d(q), 1)
        return np.squeeze(omega_**2 / q_**2) * self.polarization(
            omega=omega,
            q=q,
            chemical_potential=chemical_potential,
            temperature=temperature,
        )

    @staticmethod
    def G_T(z):
        z = z + 0.0j
        sz2m1 = np.sqrt(z - 1.0) * np.sqrt(z + 1.0)
        return z * sz2m1 + np.log(z + sz2m1)

    def chi_T(self, omega, q, chemical_potential=None, temperature=None):
        if temperature is None:
            temperature = self.temperature
        if chemical_potential is None:
            chemical_potential = self.chemical_potential
            kf = self._kf
        else:
            kf = self.compute_fermi_wavevector(
                self.compute_density(chemical_potential, temperature)
            )
        if temperature == 0.0:
            omega = np.expand_dims(np.atleast_1d(omega), 0)
            q = np.expand_dims(np.atleast_1d(q), 1)
            Dplus = (omega / self._hv + 2.0 * kf) / q
            Dminus = (omega / self._hv - 2.0 * kf) / q

            it1 = 8.0 * kf / (self._hv * q**2) * omega**2
            it2 = (
                np.where(
                    np.real(Dminus) < -1.0,
                    self.G_T(-Dminus),  # low w and low k
                    self.G_T(Dminus) - 1.0j * np.pi,  # high w or high k
                )
                - self.G_T(Dplus)
            ) * np.sqrt(0.0j + omega**2 - self._hv**2 * q**2)

            return np.squeeze(self._degeneracy / (16 * np.pi) * (it1 + it2))
        else:
            return cm.average_maldague(
                lambda mu: self.chi_T(
                    omega=omega, q=q, chemical_potential=mu, temperature=0.0
                ),
                chemical_potential=chemical_potential,
                temperature=temperature,
                num=self.maldague_num,
                quadrature=self.maldague_quadrature,
                sampling=self.maldague_sampling,
                weights=self.maldague_weights,
            )

    @staticmethod
    def theta(x, eta):
        if eta == 0.0:
            return np.heaviside(x, 0.5)
        else:
            return 0.5 + 1 / np.pi * np.arctan(x / eta)

    def conductivity(self, omega, gamma, chemical_potential=None, temperature=None):
        if temperature is None:
            temperature = self.temperature
        if chemical_potential is None:
            chemical_potential = self.chemical_potential
            ef = self._ef
        else:
            ef = self.compute_fermi_energy(
                self.compute_density(chemical_potential, temperature)
            )
        if temperature == 0.0:
            intraband = 1j / 4.0 * abs(ef) / (omega + 1j * gamma)
            interband = (
                np.pi / 16.0 * self.theta(omega / (2.0 * abs(ef)) - 1, gamma)
                + np.pi / 16.0 * self.theta(-omega / (2.0 * abs(ef)) - 1, gamma)
                + 1j
                / 32.0
                * np.log(
                    ((2.0 * abs(ef) - omega) ** 2 + gamma**2)
                    / ((2.0 * abs(ef) + omega) ** 2 + gamma**2)
                )
            )
            return (intraband + interband) * self._degeneracy
        else:
            return cm.average_maldague(
                lambda mu: self.conductivity(
                    omega=omega, gamma=gamma, chemical_potential=mu, temperature=0.0
                ),
                chemical_potential=chemical_potential,
                temperature=temperature,
                num=self.maldague_num,
                quadrature=self.maldague_quadrature,
                sampling=self.maldague_sampling,
                weights=self.maldague_weights,
            )

    def non_local_conductivity(
        self, q, omega, gamma, chemical_potential=None, temperature=None
    ):
        raise NotImplementedError("only local conductivity")


class Massless_Dirac_Fermions_B:
    """Class for Massless Dirac Fermions in perpendicular magnetic field"""

    def __init__(
        self,
        hv,
        k,
        degeneracy,
        density,
        temperature,
        magnetic_field,
        eta,
        N_cutoff,
        dimension=2,
        maldague_sampling=None,
        maldague_weights=None,
        maldague_num=101,
        maldague_quadrature="uniform",
    ):
        """Initialize an insatnce of Dirac Fermions in magnetic field.

        Args:
            hv (float): \hbar * v_D [energy * length]
            k (float): k in $\ell_B = k / \sqrt{B}$ [lenght * magnetic field**1/2]
            degeneracy (float): degeneracy of MDFs (4 for graphene if Zeeman splitting is neglected)
            density (float): electronic density [length**-2]
            temperature (float): temperature (k_B T) in energy units [energy]
            magnetic_field (float): perpendicular component of the magnetic field [magnetic field]
            eta (float): energy broadening of the levels [energy]
            N_cutoff (int): maximum order of Landau Level retained in the calculations
            dimension (int, optional): Spatial dimensionality. Defaults to 2. Only 2 is implemented.
            maldague_sampling (1darray, optional): quadrature points for Maldague integral. Defaults to None.
            maldague_weights (1darray, optional): quadrature weights for Maldague integral. Defaults to None.
            maldague_num (int, optional): number of points for Maldague integral. Defaults to 101.
            maldague_quadrature (str, optional): type of quadrature for Maldague integral. Defaults to 'gauss-legendre'.

        Raises:
            NotImplementedError: if dimension != 2 is inserted
        """
        # constants
        if dimension != 2:
            raise NotImplementedError("Only 2D Dirac Fermions available")
        self._dimension = dimension
        self._degeneracy = degeneracy
        self._hv = hv
        self._k = k
        # thermodynamic variables
        self._density = density
        self._temperature = temperature
        self._magnetic_field = magnetic_field
        # computational variables
        self.eta = eta
        self.N_cutoff = N_cutoff
        # auxiliary variables
        self._chemical_potential = self.compute_chemical_potential(
            density, temperature, magnetic_field
        )
        self._lb = self.compute_magnetic_length(magnetic_field)
        self._el = self.compute_ll_energy(magnetic_field)
        self._nl = self.compute_ll_degeneracy(magnetic_field)
        self._filling_factor = self.compute_filling_factor(density, magnetic_field)
        self._cyclotron_frequency = self.compute_cyclotron_frequency(
            density, magnetic_field
        )
        # Maldague integral settings
        self.maldague_num = maldague_num
        self.maldague_quadrature = maldague_quadrature
        self.maldague_sampling = maldague_sampling
        self.maldague_weights = maldague_weights

    # static properties
    @property
    def dimension(self):
        return self._dimension

    @dimension.setter
    def dimension(self, value):
        warn("dimension cannot be changed")

    @property
    def degeneracy(self):
        return self._degeneracy

    @degeneracy.setter
    def degeneracy(self, value):
        warn("degeneracy cannot be changed")

    #
    @property
    def hv(self):
        return self._hv

    @hv.setter
    def hv(self, value):
        warn("hv cannot be changed")

    @property
    def k(self):
        return self._k

    @k.setter
    def k(self, value):
        warn("hv cannot be changed")

    ### dynamic properties
    @property
    def density(self):
        return self._density

    @density.setter
    def density(self, value):
        self._density = value
        self._chemical_potential = self.compute_chemical_potential(
            density=self._density,
            temperature=self._temperature,
            magnetic_field=self._magnetic_field,
        )
        self._filling_factor = self.compute_filling_factor(
            self._density, self._magnetic_field
        )
        self._cyclotron_frequency = self.compute_cyclotron_frequency(
            self._density, self._magnetic_field
        )

    @property
    def chemical_potential(self):
        return self._chemical_potential

    @chemical_potential.setter
    def chemical_potential(self, value):
        self._chemical_potential = value
        self._density = self.compute_density(
            chemical_potential=self._chemical_potential,
            temperature=self._temperature,
            magnetic_field=self._magnetic_field,
        )
        self._filling_factor = self.compute_filling_factor(
            self._density, self._magnetic_field
        )
        self._cyclotron_frequency = self.compute_cyclotron_frequency(
            self._density, self._magnetic_field
        )

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, value):
        self._temperature = value
        self._chemical_potential = self.compute_chemical_potential(
            density=self._density,
            temperature=self._temperature,
            magnetic_field=self._magnetic_field,
        )

    @property
    def magnetic_field(self):
        return self._magnetic_field

    @magnetic_field.setter
    def magnetic_field(self, value):
        self._magnetic_field = value
        self._chemical_potential = self.compute_chemical_potential(
            density=self._density,
            temperature=self._temperature,
            magnetic_field=self._magnetic_field,
        )
        self._lb = self.compute_magnetic_length(self._magnetic_field)
        self._el = self.compute_ll_energy(self._magnetic_field)
        self._nl = self.compute_ll_degeneracy(self._magnetic_field)
        self._filling_factor = self.compute_filling_factor(
            self._density, self._magnetic_field
        )
        self._cyclotron_frequency = self.compute_cyclotron_frequency(
            self._density, self._magnetic_field
        )

    # Auxiliary properties
    @property
    def lb(self):
        """magnetic length

        Returns:
            float: magnetic length
        """
        return self._lb

    @lb.setter
    def lb(self, value):
        warn("lb cannot be changed, change density instead")

    @property
    def el(self):
        """landau levels energy el
        The energies of the levels are given by
        E_n = el * sqrt(abs(n))sgn(n)
        Returns:
            float: el
        """
        return self._el

    @el.setter
    def el(self, value):
        warn("el cannot be changed, change density instead")

    @property
    def nl(self):
        """landau level degeneracy nl
        It does not include spin or valley degeneracy nl = 1/(2 pi l_b**2)
        Returns:
            float: nl
        """
        return self._nl

    @nl.setter
    def nl(self, value):
        warn("nl cannot be changed, change density instead")

    @property
    def filling_factor(self):
        """filling factor nu
            nu = n/nl
        Returns:
            float: nu
        """
        return self._filling_factor

    @filling_factor.setter
    def filling_factor(self, value):
        warn(
            "filling_factor cannot be changed, change density or magnetic field instead"
        )

    @property
    def cyclotron_frequency(self):
        """Semiclassical cyclotron frequency
        omega_c = eBv_F/(c \hbar k_F)

        Returns:
            float: omega_c
        """
        return self._cyclotron_frequency

    @cyclotron_frequency.setter
    def cyclotron_frequency(self, value):
        warn("cyclotron_frequency cannot be changed, change density instead")

    ### functions
    def compute_magnetic_length(self, magnetic_field):
        return self._k / np.sqrt(abs(magnetic_field))

    def compute_ll_energy(self, magnetic_field):
        return np.sqrt(2) * self._hv / self.compute_magnetic_length(magnetic_field)

    def compute_ll_degeneracy(self, magnetic_field):
        return abs(magnetic_field) / (2 * np.pi * self._k**2)

    def compute_cyclotron_frequency(self, density, magnetic_field):
        return self._hv / (
            self.compute_magnetic_length(magnetic_field) ** 2
            * np.sqrt(4 * np.pi * np.abs(density) / self._degeneracy)
        )

    def compute_filling_factor(self, density, magnetic_field):
        return density / self.compute_ll_degeneracy(magnetic_field)

    def compute_density(self, chemical_potential, temperature, magnetic_field):
        el = self.compute_ll_energy(magnetic_field)
        nl = self.compute_ll_degeneracy(magnetic_field)
        return (
            self._degeneracy
            * nl
            * np.sum(
                [
                    cm.fermi_function(
                        el * np.sign(i) * np.sqrt(abs(i)) - chemical_potential,
                        temperature,
                    )
                    - np.heaviside(-i, 0.5)
                    for i in range(-self.N_cutoff, self.N_cutoff + 1)
                ]
            )
        )

    def compute_chemical_potential(self, density, temperature, magnetic_field):
        el = self.compute_ll_energy(magnetic_field)
        nl = self.compute_ll_degeneracy(magnetic_field)
        if temperature == 0.0:
            nu = density / nl
            return np.sum(
                [
                    el
                    * np.sign(i)
                    * np.sqrt(abs(i))
                    * np.heaviside(nu - (i - 0.5) * self._degeneracy, 0.5)
                    * np.heaviside(-nu + (i + 0.5) * self._degeneracy, 0.5)
                    for i in range(-self.N_cutoff, self.N_cutoff + 1)
                ]
            )
        else:
            sol = root_scalar(
                lambda mu: self.compute_density(mu, temperature, magnetic_field)
                - density,
                bracket=[-el * np.sqrt(self.N_cutoff), el * np.sqrt(self.N_cutoff)],
            )
            return sol.root

    def dos(self, energy):
        """Density of states per unit area of massless Dirac fermions in Magnetic field.
        Each Landau level contributes with a Wigner semicircle distribution of witdth 2\eta.
        Args:
            energy (float or array of floats): energy values where density is calculated

        Returns:
            array of floats same dimension as energy: density of states per unit area.
        """
        d = np.zeros_like(energy)
        for i in range(-self.N_cutoff, self.N_cutoff + 1):
            d += cm.delta_function(
                energy - self._el * np.sign(i) * np.sqrt(abs(i)), self.eta, "wigner"
            )
        return self._degeneracy * self._nl * d

    def conductivity(
        self, omega, chemical_potential=None, temperature=None, magnetic_field=None
    ):
        """Optical conductivity (sigma_xx = sigma_yy) of massless Dirac Fermions in magnetic field.
           Implements Eq. (11) in arXiv:0705.3783v1 with \Delta = 0 and 2\Gamma = \eta.
        Args:
            omega (float or array of floats): frequency in energy units (\hbar \omega)
            chemical_potential (float, optional): Chemical potential. If None uses the stored value. Defaults to None.
            temperature (float, optional): Temperature. If None uses the stored value. Defaults to None.
            magnetic_field (float, optional): Magnetic field. If None uses the stored value. Defaults to None.

        Returns:
            complex array same dimensions as omega: sigma(omega) in units of G_0 =2e^2/h
        """
        if temperature is None:
            temperature = self.temperature
        if chemical_potential is None:
            chemical_potential = self.chemical_potential
        if magnetic_field is None:
            magnetic_field = self.magnetic_field
        el = self.compute_ll_energy(magnetic_field)
        index = np.arange(0, self.N_cutoff + 1)
        M = el * np.sign(index) * np.sqrt(abs(index))
        f = cm.fermi_function(M - chemical_potential, temperature)
        h = cm.fermi_function(-M - chemical_potential, temperature)
        s = np.zeros_like(omega, dtype=complex)
        for i in range(0, self.N_cutoff - 1):
            s += (f[i] - f[i + 1] + h[i + 1] - h[i]) / (
                (M[i + 1] - M[i])
                * ((M[i + 1] - M[i]) ** 2 - (omega + 1j * self.eta) ** 2)
            ) + (h[i] - f[i + 1] + h[i + 1] - f[i]) / (
                (M[i + 1] + M[i])
                * ((M[i + 1] + M[i]) ** 2 - (omega + 1j * self.eta) ** 2)
            )
        return -1j * el**2 * (omega + 1j * self.eta) / 2 * s

    def hall_conductivity(
        self, omega, chemical_potential=None, temperature=None, magnetic_field=None
    ):
        """Optical conductivity (sigma_xy = -sigma_yx) of massless Dirac Fermions in magnetic field.
           Implements Eq. (12) in arXiv:0705.3783v1 with \Delta = 0 and 2\Gamma = \eta.
        Args:
            omega (float or array of floats): frequency in energy units (\hbar \omega)
            chemical_potential (float, optional): Chemical potential. If None uses the stored value. Defaults to None.
            temperature (float, optional): Temperature. If None uses the stored value. Defaults to None.
            magnetic_field (float, optional): Magnetic field. If None uses the stored value. Defaults to None.

        Returns:
            complex array same dimensions as omega: sigma_H(omega) in units of G_0 =2e^2/h
        """
        if temperature is None:
            temperature = self.temperature
        if chemical_potential is None:
            chemical_potential = self.chemical_potential
        if magnetic_field is None:
            magnetic_field = self.magnetic_field
        el = self.compute_ll_energy(magnetic_field)
        index = np.arange(0, self.N_cutoff + 1)
        M = el * np.sign(index) * np.sqrt(abs(index))
        f = cm.fermi_function(M - chemical_potential, temperature)
        h = cm.fermi_function(-M - chemical_potential, temperature)
        s = np.zeros_like(omega, dtype=complex)
        for i in range(0, self.N_cutoff - 1):
            s += (f[i] - f[i + 1] - h[i + 1] + h[i]) * (
                1 / ((M[i + 1] - M[i]) ** 2 - (omega + 1j * self.eta) ** 2)
                + 1 / ((M[i + 1] + M[i]) ** 2 - (omega + 1j * self.eta) ** 2)
            )
        return -(el**2) * np.sign(magnetic_field) / 2 * s

    def drude_conductivity(
        self, omega, chemical_potential=None, temperature=None, magnetic_field=None
    ):
        """Optical conductivity (sigma_xx = sigma_yy) of massless Dirac Fermions in magnetic field in the Drude
        approximation (\epsilon_L << Gamma, Intraband only).

        Args:
            omega (float or array of floats): frequency in energy units (\hbar \omega)
            chemical_potential (float, optional): Chemical potential. If None uses the stored value. Defaults to None.
            temperature (float, optional): Temperature. If None uses the stored value. Defaults to None.
            magnetic_field (float, optional): Magnetic field. If None uses the stored value. Defaults to None.

        Raises:
            NotImplementedError: Does not work at finite temperature
        Returns:
            complex array same dimensions as omega: sigma(omega) in units of G_0 =2e^2/h
        """
        if temperature is None:
            temperature = self.temperature
        if chemical_potential is None:
            chemical_potential = self.chemical_potential
        if magnetic_field is None:
            magnetic_field = self.magnetic_field
        if temperature == 0.0:
            density = self.compute_density(
                chemical_potential, temperature, magnetic_field
            )
            omega_c = (
                self.compute_cyclotron_frequency(density, magnetic_field)
                * np.sign(magnetic_field)
                * np.sign(density)
            )
            return (
                1j
                * (self._hv * np.sqrt(np.pi / 4 * self._degeneracy * abs(density)))
                * (omega + 1j * self.eta)
                / ((omega + 1j * self.eta) ** 2 - omega_c**2)
            )
        else:
            raise NotImplementedError
            # return average_maldague(lambda mu :
            #                         self.drude_conductivity(omega = omega, chemical_potential= mu, temperature=0., magnetic_field = magnetic_field),
            # chemical_potential=chemical_potential, temperature=temperature,
            # num = self.maldague_num, quadrature=self.maldague_quadrature, sampling = self.maldague_sampling, weights = self.maldague_weights)

    def drude_hall_conductivity(
        self, omega, chemical_potential=None, temperature=None, magnetic_field=None
    ):
        """Optical conductivity (sigma_xy = -sigma_yx) of massless Dirac Fermions in magnetic field in the Drude
        approximation (\epsilon_L << Gamma, Intraband only).

        Args:
            omega (float or array of floats): frequency in energy units (\hbar \omega)
            chemical_potential (float, optional): Chemical potential. If None uses the stored value. Defaults to None.
            temperature (float, optional): Temperature. If None uses the stored value. Defaults to None.
            magnetic_field (float, optional): Magnetic field. If None uses the stored value. Defaults to None.
        Raises:
            NotImplementedError: Does not work at finite temperature

        Returns:
            complex array same dimensions as omega: sigma_H(omega) in units of G_0 =2e^2/h
        """
        if temperature is None:
            temperature = self.temperature
        if chemical_potential is None:
            chemical_potential = self.chemical_potential
        if magnetic_field is None:
            magnetic_field = self.magnetic_field
        if temperature == 0.0:
            density = self.compute_density(
                chemical_potential, temperature, magnetic_field
            )
            omega_c = (
                self.compute_cyclotron_frequency(density, magnetic_field)
                * np.sign(magnetic_field)
                * np.sign(density)
            )
            return (
                (self._hv * np.sqrt(np.pi / 4 * self._degeneracy * abs(density)))
                * omega_c
                / ((omega + 1j * self.eta) ** 2 - omega_c**2)
            )
        else:
            raise NotImplementedError
            # return average_maldague(lambda mu : self.drude_hall_conductivity(omega = omega, chemical_potential= mu, temperature=0., magnetic_field = magnetic_field),
            # chemical_potential=chemical_potential, temperature=temperature,
            # num = self.maldague_num, quadrature=self.maldague_quadrature, sampling = self.maldague_sampling, weights = self.maldague_weights)

    ####################################################################################################################
    #################### NONLOCAL RESPONSE #############################################################################
    # Riccardo's functions as static methods, prepended an _
    @staticmethod
    def _X(AB, qx, qy, omega, gamma, mu, T, NC):
        assert abs(mu) < np.sqrt(2 * NC)
        x = 0
        for l1, N1 in ((-1, np.arange(1, NC + 1)), (+1, np.arange(0, NC + 1))):
            for l2, N2 in ((-1, np.arange(1, NC + 1)), (+1, np.arange(0, NC + 1))):
                for n1 in N1:
                    for n2 in N2:
                        # f1 = np.reciprocal(np.exp((l1 * np.sqrt(2*n1) - mu) / T) + 1)
                        # f2 = np.reciprocal(np.exp((l2 * np.sqrt(2*n2) - mu) / T) + 1)
                        f1 = cm.fermi_function(l1 * np.sqrt(2 * n1) - mu, T)
                        f2 = cm.fermi_function(l2 * np.sqrt(2 * n2) - mu, T)
                        x += (
                            (f1 - f2)
                            * AB(n1, l1, n2, l2, qx, qy)
                            / (
                                omega
                                + 1j * gamma
                                + l1 * np.sqrt(2 * n1)
                                - l2 * np.sqrt(2 * n2)
                            )
                        )
        return 2 / np.pi * np.exp(-(qx**2 + qy**2) / 2) * x

    @staticmethod
    def _G(n1, n2, qx, qy):
        q = (qx if n1 < n2 else -qx) + 1j * qy
        n2, n1 = min(n1, n2), max(n1, n2)
        return (
            np.exp((loggamma(n2 + 1) - loggamma(n1 + 1)) / 2)
            * (q / np.sqrt(2)) ** (n1 - n2)
            * Massless_Dirac_Fermions_B._laguerre(n2, n1 - n2, (qx**2 + qy**2) / 2)
        )

    @staticmethod
    def _nqnq(n1, l1, n2, l2, qx, qy):
        F1 = (
            Massless_Dirac_Fermions_B._G(n1 - 1, n2 - 1, qx, qy)
            if (n1 != 0 and n2 != 0)
            else 0
        )
        F2 = (
            l1
            * l2
            * (1 + (n1 == 0))
            * (1 + (n1 == 0))
            * Massless_Dirac_Fermions_B._G(n1, n2, qx, qy)
        )
        return (F1 + F2) * np.conj(F1 + F2) / 4

    @staticmethod
    def _jxqjxq(n1, l1, n2, l2, qx, qy):
        F1 = (
            l2 * (1 + (n2 == 0)) * Massless_Dirac_Fermions_B._G(n1 - 1, n2, qx, qy)
            if (n1 != 0)
            else 0
        )
        F2 = (
            l1 * (1 + (n1 == 0)) * Massless_Dirac_Fermions_B._G(n1, n2 - 1, qx, qy)
            if (n2 != 0)
            else 0
        )
        return (F1 + F2) * np.conj(F1 + F2) / 4

    @staticmethod
    def _jxqjyq(n1, l1, n2, l2, qx, qy):
        F1 = (
            l2 * (1 + (n2 == 0)) * Massless_Dirac_Fermions_B._G(n1 - 1, n2, qx, qy)
            if (n1 != 0)
            else 0
        )
        F2 = (
            l1 * (1 + (n1 == 0)) * Massless_Dirac_Fermions_B._G(n1, n2 - 1, qx, qy)
            if (n2 != 0)
            else 0
        )
        return 1j * (F1 + F2) * np.conj(F1 - F2) / 4

    @staticmethod
    def _laguerre(n, alpha, x):
        L0, L1, L2 = 1, 1 + alpha - x, 0
        for k in np.arange(2, n + 1):
            L2 = ((2 * k - 1 + alpha - x) * L1 - (k - 1 + alpha) * L0) / k
            L0, L1 = L1, L2
        return L0 * (n == 0) + L1 * (n == 1) + L2

    ########################## NONLOCAL CONDUCTIVITY FUNCTIONS #########################################################
    def nonlocal_conductivity_L(
        self, omega, q, chemical_potential=None, temperature=None, magnetic_field=None
    ):
        if temperature is None:
            temperature = self.temperature
        if chemical_potential is None:
            chemical_potential = self.chemical_potential
        if magnetic_field is None:
            magnetic_field = self.magnetic_field

        omega = np.expand_dims(np.atleast_1d(omega), 0)
        q = np.expand_dims(np.atleast_1d(q), 1)

        return (
            (1j * np.pi / omega)
            * self.hv
            / self.lb
            * np.squeeze(
                self._X(
                    AB=self._jxqjxq,
                    qx=q * self.lb,
                    qy=0e0,
                    omega=omega * self.lb / self.hv,
                    gamma=self.eta * self.lb / self.hv,
                    mu=self.chemical_potential * self.lb / self.hv,
                    T=self.temperature * self.lb / self.hv,
                    NC=self.N_cutoff,
                )
            )
        )

    def nonlocal_conductivity_T(
        self, omega, q, chemical_potential=None, temperature=None, magnetic_field=None
    ):
        if temperature is None:
            temperature = self.temperature
        if chemical_potential is None:
            chemical_potential = self.chemical_potential
        if magnetic_field is None:
            magnetic_field = self.magnetic_field

        omega = np.expand_dims(np.atleast_1d(omega), 0)
        q = np.expand_dims(np.atleast_1d(q), 1)

        return (
            (1j * np.pi / omega)
            * self.hv
            / self.lb
            * np.squeeze(
                self._X(
                    AB=self._jxqjxq,
                    qx=0e0,
                    qy=q * self.lb,
                    omega=omega * self.lb / self.hv,
                    gamma=self.eta * self.lb / self.hv,
                    mu=self.chemical_potential * self.lb / self.hv,
                    T=self.temperature * self.lb / self.hv,
                    NC=self.N_cutoff,
                )
            )
        )

    def nonlocal_conductivity_H(
        self, omega, q, chemical_potential=None, temperature=None, magnetic_field=None
    ):
        if temperature is None:
            temperature = self.temperature
        if chemical_potential is None:
            chemical_potential = self.chemical_potential
        if magnetic_field is None:
            magnetic_field = self.magnetic_field

        omega = np.expand_dims(np.atleast_1d(omega), 0)
        q = np.expand_dims(np.atleast_1d(q), 1)

        return (
            (1j * np.pi / omega)
            * self.hv
            / self.lb
            * np.squeeze(
                self._X(
                    AB=self._jxqjyq,
                    qx=q * self.lb,
                    qy=0e0,
                    omega=omega * self.lb / self.hv,
                    gamma=self.eta * self.lb / self.hv,
                    mu=self.chemical_potential * self.lb / self.hv,
                    T=self.temperature * self.lb / self.hv,
                    NC=self.N_cutoff,
                )
            )
        )

    ####################################################################################################################
