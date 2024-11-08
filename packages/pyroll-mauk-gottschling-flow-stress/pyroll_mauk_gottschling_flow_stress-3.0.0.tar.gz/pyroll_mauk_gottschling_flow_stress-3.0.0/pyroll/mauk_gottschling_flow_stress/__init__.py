from pyroll.core import Profile, DeformationUnit, Hook

from .mauk_gottschling_flow_stress import MaukGottschlingFlowStressCoefficients, flow_stress

VERSION = "3.0.0"

Profile.mauk_gottschling_flow_stress_coefficients = Hook[MaukGottschlingFlowStressCoefficients]()


@DeformationUnit.Profile.flow_stress
def mauk_gottschling_flow_stress(self: DeformationUnit.Profile):
    if hasattr(self, "mauk_gottschling_flow_stress_coefficients"):
        return flow_stress(
            self.mauk_gottschling_flow_stress_coefficients,
            self.strain,
            self.unit.strain_rate,
            self.temperature
        )


@DeformationUnit.Profile.flow_stress_function
def mauk_gottschling_flow_stress_function(self: DeformationUnit.Profile):
    if hasattr(self, "mauk_gottschling_flow_stress_coefficients"):
        def f(strain: float, strain_rate: float, temperature: float) -> float:
            return flow_stress(self.mauk_gottschling_flow_stress_coefficients, strain, strain_rate, temperature)

        return f


from . import materials
