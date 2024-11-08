import numpy as np

from pyroll.core import DeformationUnit

VERSION = "3.0.0"


@DeformationUnit.Profile.flow_stress
def misaka_flow_stress(self: DeformationUnit.Profile):
    if hasattr(self, "chemical_composition"):
        return flow_stress(
            self.chemical_composition,
            self.strain,
            self.unit.strain_rate,
            self.temperature
        )


@DeformationUnit.Profile.flow_stress_function
def misaka_flow_stress_function(self: DeformationUnit.Profile):
    if hasattr(self, "chemical_composition"):
        def f(strain: float, strain_rate: float, temperature: float) -> float:
            return flow_stress(self.chemical_composition, strain, strain_rate, temperature)

        return f


def flow_stress(chemical_composition: dict[str, float], strain: float, strain_rate: float, temperature: float):
    """
    Calculates the flow stress according to the constitutive equation from Y. Misaka for the provided
    material composition, strain, strain rate and temperature.

    :param chemical_composition: the chemical composition of the material
    :param strain: the equivalent strain experienced
    :param strain_rate: the equivalent strain rate experienced
    :param temperature: the absolute temperature of the material (K)
    """

    strain = strain + 0.1
    strain_rate = strain_rate + 0.1

    conversion_to_si_units_from_kgf_per_mm_squared = 9806650

    misaka_mean_flow_stress = np.exp(
        0.126 - 1.75 * chemical_composition["C"] + 0.594 * chemical_composition["C"] ** 2 + (
                2851 + 2968 * chemical_composition["C"] - 1120 * chemical_composition["C"] ** 2) / temperature) * strain ** 0.21 * strain_rate ** 0.13

    return misaka_mean_flow_stress * conversion_to_si_units_from_kgf_per_mm_squared
