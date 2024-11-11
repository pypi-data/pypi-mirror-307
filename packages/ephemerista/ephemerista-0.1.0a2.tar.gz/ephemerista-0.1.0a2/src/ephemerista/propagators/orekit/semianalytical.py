from typing import Literal

from pydantic import Field

from ephemerista.propagators.orekit import OrekitPropagator


class SemiAnalyticalPropagator(OrekitPropagator):
    propagator_type: Literal["semianalytical"] = Field(
        default="semianalytical", frozen=True, repr=False, alias="type", description="The type of the propagator"
    )

    def setup_propagator(self, orbit_sample):
        from org.orekit.propagation.semianalytical.dsst import DSSTPropagator  # type: ignore

        tol = DSSTPropagator.tolerances(self.prop_position_error, orbit_sample)
        from org.hipparchus.ode.nonstiff import DormandPrince853Integrator  # type: ignore

        integrator = DormandPrince853Integrator(self.prop_min_step, self.prop_max_step, tol[0], tol[1])
        integrator.setInitialStepSize(self.prop_init_step)

        # Set up propagator and force models
        self._orekit_prop = DSSTPropagator(integrator)

        self.setup_force_models()

    def setup_force_models(self):
        from org.orekit.propagation.semianalytical.dsst.forces import DSSTNewtonianAttraction  # type: ignore
        from org.orekit.utils import Constants as OrekitConstants  # type: ignore

        self._orekit_prop.addForceModel(DSSTNewtonianAttraction(OrekitConstants.EIGEN5C_EARTH_MU))

        if self.grav_degree_order:
            from org.orekit.forces.gravity.potential import GravityFieldFactory  # type: ignore

            gravity_provider = GravityFieldFactory.getUnnormalizedProvider(
                self.grav_degree_order[0], self.grav_degree_order[1]
            )
            from org.orekit.propagation.semianalytical.dsst.forces import DSSTTesseral, DSSTZonal  # type: ignore

            zonal = DSSTZonal(gravity_provider)
            self._orekit_prop.addForceModel(zonal)

            tesseral = DSSTTesseral(
                self._wgs84_ellipsoid.getBodyFrame(), self._wgs84_ellipsoid.getSpin(), gravity_provider
            )
            self._orekit_prop.addForceModel(tesseral)

        from java.lang import NullPointerException  # type: ignore
        from org.orekit.bodies import CelestialBodyFactory  # type: ignore
        from org.orekit.propagation.semianalytical.dsst.forces import DSSTThirdBody  # type: ignore

        for body in self.third_bodies:
            try:  # CelestialBodyFactory.getBody throws a NullPointerException if the body is not supported by Orekit
                body_orekit = CelestialBodyFactory.getBody(body.name)
                self._orekit_prop.addForceModel(DSSTThirdBody(body_orekit, OrekitConstants.EIGEN5C_EARTH_MU))
            except NullPointerException as exc:
                msg = f"Body {body.name} unsupported for Orekit third-body attraction"
                raise ValueError(msg) from exc

        if self.enable_srp:
            from org.orekit.forces.radiation import IsotropicRadiationSingleCoefficient  # type: ignore

            isotropic_rad = IsotropicRadiationSingleCoefficient(self.cross_section, self.c_r)
            from org.orekit.bodies import CelestialBodyFactory  # type: ignore
            from org.orekit.propagation.semianalytical.dsst.forces import DSSTSolarRadiationPressure  # type: ignore

            self._orekit_prop.addForceModel(
                DSSTSolarRadiationPressure(
                    self._sun, self._wgs84_ellipsoid, isotropic_rad, OrekitConstants.EIGEN5C_EARTH_MU
                )
            )

        if self.enable_drag:
            from org.orekit.models.earth.atmosphere.data import CssiSpaceWeatherData  # type: ignore

            cswl = CssiSpaceWeatherData("SpaceWeather-All-v1.2.txt")

            from org.orekit.models.earth.atmosphere import NRLMSISE00  # type: ignore

            atmosphere = NRLMSISE00(cswl, self._sun, self._wgs84_ellipsoid)

            from org.orekit.forces.drag import IsotropicDrag  # type: ignore

            isotropic_drag = IsotropicDrag(self.cross_section, self.c_d)
            from org.orekit.propagation.semianalytical.dsst.forces import DSSTAtmosphericDrag  # type: ignore

            self._orekit_prop.addForceModel(
                DSSTAtmosphericDrag(atmosphere, isotropic_drag, OrekitConstants.EIGEN5C_EARTH_MU)
            )
