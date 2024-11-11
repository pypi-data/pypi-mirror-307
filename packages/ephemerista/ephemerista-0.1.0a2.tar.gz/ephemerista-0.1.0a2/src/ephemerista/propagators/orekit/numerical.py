from typing import Literal

from pydantic import Field

from ephemerista.propagators.orekit import OrekitPropagator


class NumericalPropagator(OrekitPropagator):
    propagator_type: Literal["numerical"] = Field(
        default="numerical", frozen=True, repr=False, alias="type", description="The type of the propagator"
    )

    def setup_propagator(self, orbit_sample):
        from org.orekit.propagation.numerical import NumericalPropagator as OrekitNumericalPropagator  # type: ignore

        tol = OrekitNumericalPropagator.tolerances(self.prop_position_error, orbit_sample, orbit_sample.getType())
        from org.hipparchus.ode.nonstiff import DormandPrince853Integrator  # type: ignore

        integrator = DormandPrince853Integrator(self.prop_min_step, self.prop_max_step, tol[0], tol[1])
        integrator.setInitialStepSize(self.prop_init_step)

        # Set up propagator and force models
        self._orekit_prop = OrekitNumericalPropagator(integrator)
        self._orekit_prop.setOrbitType(orbit_sample.getType())

        self.setup_force_models()

    def setup_force_models(self):
        from org.orekit.forces.gravity import NewtonianAttraction  # type: ignore
        from org.orekit.utils import Constants as OrekitConstants  # type: ignore

        self._orekit_prop.addForceModel(NewtonianAttraction(OrekitConstants.EIGEN5C_EARTH_MU))

        if self.grav_degree_order:
            from org.orekit.forces.gravity.potential import GravityFieldFactory  # type: ignore

            gravity_provider = GravityFieldFactory.getNormalizedProvider(
                self.grav_degree_order[0], self.grav_degree_order[1]
            )
            from org.orekit.forces.gravity import HolmesFeatherstoneAttractionModel  # type: ignore

            gravity_attraction_model = HolmesFeatherstoneAttractionModel(
                self._wgs84_ellipsoid.getBodyFrame(), gravity_provider
            )
            self._orekit_prop.addForceModel(gravity_attraction_model)

        from java.lang import NullPointerException  # type: ignore
        from org.orekit.bodies import CelestialBodyFactory  # type: ignore
        from org.orekit.forces.gravity import ThirdBodyAttraction  # type: ignore

        for body in self.third_bodies:
            try:  # CelestialBodyFactory.getBody throws a NullPointerException if the body is not supported by Orekit
                body_orekit = CelestialBodyFactory.getBody(body.name)
                self._orekit_prop.addForceModel(ThirdBodyAttraction(body_orekit))
            except NullPointerException as exc:
                msg = f"Body {body.name} unsupported for Orekit third-body attraction"
                raise ValueError(msg) from exc

        if self.enable_srp:
            from org.orekit.forces.radiation import IsotropicRadiationSingleCoefficient  # type: ignore

            isotropic_rad = IsotropicRadiationSingleCoefficient(self.cross_section, self.c_r)
            from org.orekit.bodies import CelestialBodyFactory  # type: ignore
            from org.orekit.forces.radiation import SolarRadiationPressure  # type: ignore

            self._orekit_prop.addForceModel(SolarRadiationPressure(self._sun, self._wgs84_ellipsoid, isotropic_rad))

        if self.enable_drag:
            from org.orekit.models.earth.atmosphere.data import CssiSpaceWeatherData  # type: ignore

            cswl = CssiSpaceWeatherData("SpaceWeather-All-v1.2.txt")

            from org.orekit.models.earth.atmosphere import NRLMSISE00  # type: ignore

            atmosphere = NRLMSISE00(cswl, self._sun, self._wgs84_ellipsoid)

            from org.orekit.forces.drag import IsotropicDrag  # type: ignore

            isotropic_drag = IsotropicDrag(self.cross_section, self.c_d)
            from org.orekit.forces.drag import DragForce  # type: ignore

            self._orekit_prop.addForceModel(DragForce(atmosphere, isotropic_drag))
