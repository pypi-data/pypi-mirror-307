import numpy as np
from scipy.special import wofz


class Dielectric_Function:
    def __init__(self, model):
        self._model = model

    def __call__(self, omega):
        eps = np.zeros_like(omega, dtype=complex)
        for peak in self._model:
            eps += self.peak_dielectric(omega, peak)
        return eps

    @staticmethod
    def peak_dielectric(omega, peak):
        if peak["type"] == "constant":
            return np.ones_like(omega) * peak["parameters"]["constant"]
        elif peak["type"] == "power":
            return (omega ** peak["parameters"]["power"]) * peak["parameters"]["factor"]
        elif peak["type"] == "drude":
            return Dielectric_Function.drude_dielectric(omega, **peak["parameters"])
        elif peak["type"] == "lorentz":
            return Dielectric_Function.lorentz_dielectric(omega, **peak["parameters"])
        elif peak["type"] == "gauss":
            return Dielectric_Function.gaussian_dielectric(omega, **peak["parameters"])
        elif peak["type"] == "brendel":
            return Dielectric_Function.brendel_dielectric(omega, **peak["parameters"])
        elif peak["type"] == "modified_brendel":
            return Dielectric_Function.modified_brendel_dielectric(
                omega, **peak["parameters"]
            )
        else:
            raise ValueError("unknown peak type")

    @staticmethod
    def drude_dielectric(omega, omega_p, gamma):
        return 1 - omega_p / (omega * (omega + 1j * gamma))

    @staticmethod
    def lorentz_dielectric(omega, s, omega_0, gamma):
        return s * omega_0**2 / (omega_0**2 - 1.0j * omega * gamma - omega**2)

    @staticmethod
    def gaussian_dielectric(omega, s, omega_0, sigma):
        return (
            s
            * omega_0**2
            * 1j
            * np.sqrt(np.pi / 8)
            / (omega * sigma)
            * (
                wofz((omega - omega_0) / (np.sqrt(2) * sigma))
                + wofz((omega + omega_0) / (np.sqrt(2) * sigma))
            )
        )

    @staticmethod
    def brendel_dielectric(omega, s, omega_0, gamma, sigma):
        a = 1j * np.sqrt(-(omega**2) - 1j * gamma * omega)
        return (
            s
            * omega_0**2
            * 1j
            * np.sqrt(np.pi / 8)
            / (a * sigma)
            * (
                wofz((a - omega_0) / (np.sqrt(2) * sigma))
                + wofz((a + omega_0) / (np.sqrt(2) * sigma))
            )
        )

    @staticmethod
    def modified_brendel_dielectric(omega, s, omega_0, gamma, sigma):
        a = 1j * np.sqrt(-(omega**2) - 1j * gamma * omega)
        return s * (
            1
            + 1j
            * np.sqrt(np.pi / 8)
            * a
            / (sigma)
            * (
                wofz((a - omega_0) / (np.sqrt(2) * sigma))
                + wofz((a + omega_0) / (np.sqrt(2) * sigma))
            )
        )
