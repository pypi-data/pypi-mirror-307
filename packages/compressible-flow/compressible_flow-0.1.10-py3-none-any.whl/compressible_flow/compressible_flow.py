import numpy as np
import scipy.optimize as opt


class Ideal_Gas:
    """
    Class that includes the functions for calculating the properties of the inviscid compressible flow of an ideal gas.
    """

    def __init__(self, R=287.0, gamma=1.4):
        """
        Creates an Ideal_Gas instance given the parameters of the ideal gas.
        Default values are for air in SI units.

        Parameters
        ----------
        R : float, optional
            specific gas constant of the gas (R/M where R is the ideal gas constant and M Is the molar mass), by default 287.
        gamma : float, optional
            adiabatic ratio (C_p/C_v) of the gas, by default 1.4
        """
        self.R = R
        self.gamma = gamma
        self.C_v = R / (gamma - 1)
        self.C_p = R * gamma / (gamma - 1)
        self.TstarT0 = 1.0 / self.T0T(1)
        self.pstarp0 = 1.0 / self.p0p(1)
        self.rhostarrho0 = 1.0 / self.rho0rho(1)

    # isoentropic flow
    def T0T(self, M: float) -> float:
        """
        Returns the total temperature to temperature ratio T_0/T as a function of the Mach number

        Parameters
        ----------
        M : float
            Mach number

        Returns
        -------
        float
            T_0/T
        """
        return 1 + 0.5 * (self.gamma - 1) * M**2

    def p0p(self, M: float) -> float:
        """
        Returns the total pressure to pressure ratio P_0/P as a function of the Mach number

        Parameters
        ----------
        M : float
            Mach number

        Returns
        -------
        float
            P_0/P
        """
        return (1 + 0.5 * (self.gamma - 1) * M**2) ** (self.gamma / (self.gamma - 1))

    def rho0rho(self, M: float) -> float:
        """
        Returns the total density to density ratio rho_0/rho as a function of the Mach number

        Parameters
        ----------
        M : float
            Mach number

        Returns
        -------
        float
            rho_0/rho
        """
        return (1 + 0.5 * (self.gamma - 1) * M**2) ** (1 / (self.gamma - 1))

    def M_star(self, M: float) -> float:
        """
        Returns the characteristic Mach number M*

        Parameters
        ----------
        M : float
            Mach number

        Returns
        -------
        float
            M*
        """
        return np.sqrt(((self.gamma + 1) * M**2) / (2 + (self.gamma - 1) * M**2))

    def AAstar(self, M: float) -> float:
        """
        Returns the area relation A/A*

        Parameters
        ----------
        M : float
            Mach number

        Returns
        -------
        float
            A/A*
        """
        return self.rhostarrho0 * self.rho0rho(M) / self.M_star(M)

    # normal shock
    def M2(self, M1: float) -> float:
        """
        Mach number M_2 after a normal shockwave with incoming Mach number M_1.

        Parameters
        ----------
        M1 : float
            Mach number before the shockwave

        Returns
        -------
        float
            The Mach number after the shockwave.
        """
        return np.sqrt(
            (1 + 0.5 * (self.gamma - 1) * M1**2)
            / (self.gamma * M1**2 - 0.5 * (self.gamma - 1))
        )

    def p2p1(self, M1: float) -> float:
        """
        Pressure ratio p2/p1 in a normal shockwave with incoming Mach number M1

        Parameters
        ----------
        M1 : float
            Mach number before the shockwave

        Returns
        -------
        float
            p2/p1
        """
        return 1 + 2 * self.gamma / (self.gamma + 1) * (M1**2 - 1)

    def rho2rho1(self, M1: float) -> float:
        """
        Density ratio rho2/rho1 in a normal shockwave

        Parameters
        ----------
        M1 : float
            Mach number before the shockwave

        Returns
        -------
        float
            rho2/rho1
        """
        return (self.gamma + 1) * M1**2 / (2 + (self.gamma - 1) * M1**2)

    def T2T1(self, M1: float) -> float:
        """
        Temperature ratio T2/T1 in a normal shockwave

        Parameters
        ----------
        M1 : float
            Mach number before the shockwave

        Returns
        -------
        float
            T2/T1
        """
        return self.p2p1(M1) / self.rho2rho1(M1)

    def u2u1(self, M1: float) -> float:
        """
        Velocity ratio in a normal shockwave u_2/u_1

        Parameters
        ----------
        M1 : float
            Mach number before the shockwave

        Returns
        -------
        float
            u2/u1
        """
        return 1.0 / self.rho2rho1(M1)

    def h2h1(self, M1: float) -> float:
        """
        Entalpy ratio h2/h1 in a normal shockwave.

        Parameters
        ----------
        M1 : float
            Mach number before the shockwave

        Returns
        -------
        float
            h2/h1
        """
        return self.T2T1(M1)

    def deltas(self, M1: float) -> float:
        """
        Entropy variation in a normal shockwave

        Parameters
        ----------
        M1 : float
            Mach number before the shockwave

        Returns
        -------
        float
            Delta S = S_2-S_1
        """
        return self.C_p * np.log(self.T2T1(M1)) - self.R * np.log(self.p2p1(M1))

    def p02p01(self, M1: float) -> float:
        """
        Total pressure ratio p02/p01 in a normal shockwave with incoming Mach number M1

        Parameters
        ----------
        M1 : float
            Mach number before the shockwave

        Returns
        -------
        float
            p02/p01
        """
        return np.exp(-self.deltas(M1) / self.R)

    def p02p1(self, M1: float) -> float:
        """
        Total pressure to pressure ratio p02/p1 in a normal shockwave with incoming Mach number M1

        Parameters
        ----------
        M1 : float
            Mach number before the shockwave

        Returns
        -------
        float
            p02/p1
        """
        return self.p2p1(M1) * self.p0p(self.M2(M1))

    def pitot_ratio(self, M1: float) -> float:
        """
        Ratio between the pressure measured in a Pitot tube and the static pressure in both the sub-sonic and supersonic regime.

        Parameters
        ----------
        M1 : float
            Mach number

        Returns
        -------
        float
            p_pitot/p_static
        """
        return np.piecewise(M1, [M1 <= 1, M1 > 1], [self.p0p, self.p02p1])

    # oblique shock
    def theta(self, beta: float, M1: float) -> float:
        """
        Corner angle of an oblique shockwave as a function of the wavefront angle beta and the upstream Mach number M1.

        Parameters
        ----------
        beta : float
            wavefront angle in degrees
        M1 : float
            Upstream Mach number

        Returns
        -------
        float
            theta
        """
        return np.rad2deg(
            np.arctan(
                2
                / np.tan(np.deg2rad(beta))
                * (M1**2 * (np.sin(np.deg2rad(beta))) ** 2 - 1)
                / (2 + M1**2 * (self.gamma + np.cos(2 * np.deg2rad(beta))))
            )
        )

    def theta_max(self, M1: float) -> float:
        """
        Maximum deflection angle theta achivable with a given Mach number.
        Also returns the value of beta where it occurs.

        Parameters
        ----------
        M1 : float
            Upstream Mach number.

        Returns
        -------
        tuple
            (theta_max, beta_max)
        """
        mu = self.mach_angle(M1)
        res = opt.minimize_scalar(
            lambda beta: -self.theta(beta, M1), bracket=(mu, mu / 2 + 45, 90)
        )
        beta_max = res.x
        theta_max = -res.fun
        return theta_max, beta_max

    def theta_sonic(self, M1: float) -> float:
        mu = self.mach_angle(M1)

        def _M2_oblique(beta):
            theta = self.theta(beta, M1)
            return (
                self.M2(M1 * np.sin(np.deg2rad(beta)))
                / np.sin(np.deg2rad(beta - theta))
                - 1
            )

        res = opt.root_scalar(_M2_oblique, bracket=(mu, 90))
        beta = res.root
        theta = self.theta(beta, M1)
        return theta, beta

    def beta_strong(self, theta: float, M1: float) -> float:
        """
        Wavefront angle beta corresponding to the strong shock wave given theta and M_1

        Parameters
        ----------
        theta : float
            corner angle in degrees
        M1 : _type_
            Upstream Mach number.

        Returns
        -------
        float
            beta_strong
        """
        assert theta >= 0.0
        theta_max, beta_max = self.theta_max(M1)
        if theta > theta_max:
            return np.nan
        elif theta == theta_max:
            return beta_max
        else:
            pass

    def beta_weak(self, theta: float, M1: float) -> float:
        """
        Wavefront angle beta corresponding to the weak shock wave given theta and M_1

        Parameters
        ----------
        theta : float
            corner angle in degrees
        M1 : _type_
            Upstream Mach number.

        Returns
        -------
        float
            beta_weak
        """
        assert theta >= 0.0
        theta_max, beta_max = self.theta_max(M1)
        if theta > theta_max:
            return np.nan
        elif theta == theta_max:
            return beta_max
        else:
            pass

    # expansion waves
    def mach_angle(self, M: float) -> float:
        """
        Mach angle

        Parameters
        ----------
        M : float
            Mach number

        Returns
        -------
        float
            Mach angle in degrees
        """
        return np.rad2deg(np.arcsin(1 / M))

    def prandtl_meyer(self, M: float) -> float:
        """
        Prandtl-Meyer function

        Returns
        -------
        M: float
            Mach number

        Returns
        -------
        float
            Prandtl-Meyer function in degrees
        """
        return np.rad2deg(
            np.sqrt((self.gamma + 1) / (self.gamma - 1))
            * np.arctan(np.sqrt((self.gamma - 1) / (self.gamma + 1) * (M**2 - 1)))
            - np.arctan(np.sqrt(M**2 - 1))
        )
