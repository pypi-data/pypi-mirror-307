import numpy as np

from pyroll.core import DeformationUnit

VERSION = "3.0.0"


@DeformationUnit.Profile.flow_stress
def lee_flow_stress(self: DeformationUnit.Profile):
    if hasattr(self, "chemical_composition"):
        return flow_stress(
            self.chemical_composition,
            self.strain,
            self.unit.strain_rate,
            self.temperature
        )


@DeformationUnit.Profile.flow_stress_function
def lee_flow_stress_function(self: DeformationUnit.Profile):
    if hasattr(self, "chemical_composition"):
        def f(strain: float, strain_rate: float, temperature: float) -> float:
            return flow_stress(self.chemical_composition, strain, strain_rate, temperature)

        return f


def carbon_content(chemical_composition: dict[str, float]):
    key_list = list(chemical_composition.keys())
    key_list_lower = [key.lower() for key in key_list]
    elements_for_equivalent_carbon_content = ['SI', 'MN', 'MO', 'V', 'CU', 'NI', 'CR']
    if all(item in key_list_lower for item in elements_for_equivalent_carbon_content):
        return chemical_composition['C'] + chemical_composition['MN'] / 6 + (
                    chemical_composition['CR'] + chemical_composition['MO'] + chemical_composition['V']) / 5 + (
                    chemical_composition['CU'] + chemical_composition['NI']) / 15
    else:
        return chemical_composition['C']


def flow_stress(chemical_composition: dict[str, float], strain: float, strain_rate: float, temperature: float):
    """
    Calculates the flow stress according to the constitutive equation from S. Shida for the provided
    material composition, strain, strain rate and temperature.

    :param chemical_composition: the chemical composition of the material
    :param strain: the equivalent strain experienced
    :param strain_rate: the equivalent strain rate experienced
    :param temperature: the absolute temperature of the material (K)
    """

    strain = strain + 0.1
    strain_rate = strain_rate + 0.1

    equivalent_carbon_content = carbon_content(chemical_composition)

    transformation_temperature = 0.95 * (equivalent_carbon_content + 0.41) / (
            equivalent_carbon_content + 0.32)
    normalized_temperature = temperature / 1000

    if normalized_temperature <= transformation_temperature:
        temperature_correction = 30 * (equivalent_carbon_content + 0.9) * (
                normalized_temperature - 0.95 * (equivalent_carbon_content + 0.49) / (
                equivalent_carbon_content + 0.42)) ** 2 + (equivalent_carbon_content + 0.06) / (
                                         equivalent_carbon_content + 0.09)
        strain_rate_sensitivity = (0.081 * equivalent_carbon_content - 0.154) * normalized_temperature + (
                -0.019 * equivalent_carbon_content + 0.207) + 0.027 / (equivalent_carbon_content + 0.32)
        deformation_resistance_contribution = 0.28 * temperature_correction * np.exp(
            (equivalent_carbon_content + 0.32) / (0.19 * (equivalent_carbon_content + 0.41)) - 0.01 / (
                    equivalent_carbon_content + 0.05))

    else:
        temperature_correction = 1
        strain_rate_sensitivity = (-0.019 * equivalent_carbon_content + 0.126) * normalized_temperature + (
                0.076 * equivalent_carbon_content - 0.05)
        deformation_resistance_contribution = 0.28 * temperature_correction * np.exp(
            5 / normalized_temperature - 0.01 / (equivalent_carbon_content + 0.05))

    strain_hardening_factor = 0.41 - 0.07 * equivalent_carbon_content
    strain_contribution = 1.3 * (strain / 0.2) ** strain_hardening_factor - 0.3 * (strain / 0.2)
    strain_rate_contribution = ((strain_rate / 10) ** strain_rate_sensitivity) * (
            (strain_rate / 100) ** (strain_rate_sensitivity / 2.4)) * (
                                       (strain_rate / 1000) ** (strain_rate_sensitivity / 15))

    conversion_to_si_units_from_kgf_per_mm_squared = 9806650

    return deformation_resistance_contribution * strain_contribution * strain_rate_contribution * conversion_to_si_units_from_kgf_per_mm_squared
