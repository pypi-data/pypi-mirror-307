import numpy as np
from warnings import warn
from scipy.optimize import root_scalar
import response_functions.common as cm


class Electron_Liquid:
    def __init__(
        self,
        m,
        degeneracy,
        density,
        temperature,
        dimension=2,
        maldague_num=101,
        maldague_sampling=None,
    ):
        if dimension not in (1, 2, 3):
            raise NotImplementedError("Only 1-2-3D")
        self._dimension = dimension
        self._degeneracy = degeneracy
        self._m = m
        assert density >= 0.0
        self._density = density
        self._temperature = temperature
        self._chemical_potential = self.compute_chemical_potential(density, temperature)

        self._kf = self.compute_fermi_wavevector(density)
        self._ef = self.compute_fermi_energy(density)

        self.maldague_num = maldague_num
        self.maldague_sampling = maldague_sampling

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
    def m(self):
        return self._m

    @m.setter
    def m(self, value):
        warn("m cannot be changed")

    ### dynamic properties
    @property
    def density(self):
        return self._density

    @density.setter
    def density(self, value):
        assert value >= 0.0
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
        assert np.all(density >= 0.0)
        return (
            2.0
            * np.pi
            * np.power(
                density / (self._degeneracy * cm.unit_sphere_volume(self._dimension)),
                1.0 / self._dimension,
            )
        )

    def compute_fermi_energy(self, density):
        assert np.all(density >= 0.0)
        return self.compute_fermi_wavevector(density) ** 2 / (2.0 * self._m)

    def compute_chemical_potential(self, density, temperature):
        assert np.all(density >= 0.0)
        if temperature == 0.0:
            return self.compute_fermi_energy(density)
        else:
            sol = root_scalar(
                lambda mu: self.compute_density(mu, temperature) - density,
                # change braketing
                bracket=[
                    temperature
                    * np.log(
                        density
                        / self._degeneracy
                        * (2 * np.pi / (self._m * temperature)) ** (self._dimension / 2)
                    ),
                    self.compute_fermi_energy(density),
                ],
            )
            return sol.root

    ## change
    def compute_density(self, chemical_potential, temperature):
        if temperature == 0.0:
            return (
                (
                    self._degeneracy
                    * cm.unit_sphere_volume(self._dimension)
                    / ((2.0 * np.pi) ** self._dimension)
                )
                * (2 * chemical_potential * self._m) ** (self._dimension / 2)
                * np.heaviside(chemical_potential, 0.5)
            )
        else:
            return (
                self._degeneracy
                * (self._m * temperature / (2.0 * np.pi)) ** (self._dimension / 2)
                * cm.fermi_dirac_int(
                    self._dimension / 2 - 1, chemical_potential / temperature
                )
            )

    def dos(self, energy):
        # done
        return (
            self._degeneracy
            * self._m ** (self._dimension / 2)
            * cm.unit_sphere_surface(self._dimension)
            / (2.0 * np.pi) ** self._dimension
            * np.heaviside(energy, 0.5)
            * (2 * energy) ** (self._dimension / 2 - 1)
        )
