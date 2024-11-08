from pyroll.core import Profile

from .mauk_gottschling_flow_stress import MaukGottschlingFlowStressCoefficients


def is_material(profile: Profile, materials: set[str]):
    if isinstance(profile.material, str):
        return profile.material.lower() in materials
    return materials.intersection([m.lower() for m in profile.material])


@Profile.mauk_gottschling_flow_stress_coefficients
def c15(self: Profile):
    if is_material(self, {"c15"}):
        return MaukGottschlingFlowStressCoefficients(
            k=5050.220 * 1e6,
            m1=-0.003126,
            m2=-0.168624,
            m3=0.359206,
            m4=-0.702119,
            m5=0.000278,
            baseStrain=0.1,
            baseStrainRate=0.1
        )


@Profile.mauk_gottschling_flow_stress_coefficients
def c55(self: Profile):
    if is_material(self, {"c55"}):
        return MaukGottschlingFlowStressCoefficients(
            k=4558.87 * 1e6,
            m1=-0.00321,
            m2=-0.39954,
            m3=0.2592,
            m4=-0.5906,
            m5=0.00017,
            baseStrain=0.1,
            baseStrainRate=0.1
        )


@Profile.mauk_gottschling_flow_stress_coefficients
def onehundertCr6(self: Profile):
    if is_material(self, {"100Cr6"}):
        return MaukGottschlingFlowStressCoefficients(
            k=4089.71 * 1e6,
            m1=-0.00370,
            m2=-0.07889,
            m3=0.2314,
            m4=-0.5059,
            m5=0.00021,
            baseStrain=0.1,
            baseStrainRate=0.1
        )
