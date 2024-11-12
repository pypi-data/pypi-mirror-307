from scipy import optimize
from scipy.integrate import quad
from scipy.interpolate import PchipInterpolator
from scipy.signal import savgol_filter
import numpy as np
import ray
from cosmoTransitions import transitionFinder, tunneling1D, pathDeformation

from .potential import PotentialWrapper


class FOPTFinder:
    def __init__(
        self,
        potential: PotentialWrapper,
        Tmax,
        g_star,
        Mp,
        initialized=False,
        parallel=False,
        criterion_value=None,
        Tnuc=None,
        num_points=100,
        window_length=19,
    ):
        self.potential = potential
        self.Tmax = Tmax
        self.criterion_value = criterion_value
        self.Tnuc = Tnuc
        self.num_points = num_points
        self.window_length = window_length
        self.g_star = g_star
        self.Mp = Mp

        # Initialization
        self.dST_dT_vec = None
        self.dST_dT_Tn = None

        # - Find all transitions
        if not initialized:
            self.potential.getPhases()
            self.potential.findAllTransitions()

        # - Find critical temperature
        tc_trans_result = self.potential.calcTcTrans()
        if tc_trans_result and len(tc_trans_result) > 0:
            self.Tcrit = tc_trans_result[0].get("Tcrit")
            print(f"Tcrit = {self.Tcrit}")
        else:
            self.Tcrit = None
            raise ValueError("No Tc found")

        # - Find T0
        self.T0 = self.potential.findT0()

        # Define start phase
        start_idx = transitionFinder.getStartPhase(
            self.potential.phases, self.potential.Vtot
        )
        self.start_phase = self.potential.phases[start_idx]

        # Find actions for T_domain
        self.T_domain = np.logspace(
            np.log10(self.T0), np.log10(self.Tcrit), num=self.num_points
        )
        self.S_vec = self.findActions(self.T_domain, parallel)
        self.S_over_T_fn = PchipInterpolator(self.T_domain, self.S_vec / self.T_domain)

        # To find Tnuc
        self.findDR()
        self.findHubbleTemp()
        self.findDPdT()
        self.findP()

    def findTnuc(self, g_star=None, Mp=None):
        if self.Tnuc:
            return self.Tnuc
        if self.criterion_value is not None:
            try:
                PT_result = transitionFinder.tunnelFromPhase(
                    self.potential.phases,
                    self.start_phase,
                    self.potential.Vtot,
                    self.potential.gradV,
                    Tmax=self.Tmax,
                    nuclCriterion=lambda S, T: S / (T + 1e-100) - self.criterion_value,
                )
                self.Tnuc = PT_result.get("Tnuc")
                if self.Tnuc is None or not np.isfinite(self.Tnuc):
                    raise ValueError("No Tnuc found")
            except Exception as e:
                print(e)
                self.Tnuc = None
        else:
            Tmin = self.T0

            def is_P_one(T):
                return np.log10(self.P_fn(self.Tcrit - T))

            params = dict(
                xtol=1e-10,
                rtol=1e-10,
                maxiter=1000,
            )

            sol = optimize.root_scalar(
                is_P_one, bracket=[0, self.Tcrit - Tmin], method="brentq", **params
            )
            T_root = sol.root
            self.Tnuc_err = np.abs(self.P_fn(self.Tcrit - T_root) - 1)
            self.Tnuc = self.Tcrit - T_root
            self.dST_dT_Tn = self.dST_dT(self.Tnuc)

    def create_action_finder(self):
        return ActionFinder(
            potential=self.potential, start_phase=self.start_phase
        )

    def findActions(self, T_vec, parallel=False):
        finders = [self.create_action_finder() for _ in range(len(T_vec))]
        if parallel:
            actions = ray.get(
                [finder.findAction.remote(T) for finder, T in zip(finders, T_vec)]
            )
        else:
            actions = [finder.findAction(T) for finder, T in zip(finders, T_vec)]
        return np.array(actions)

    def gradST(self):
        if self.dST_dT_vec and self.dST_dT_Tn:
            pass
        else:
            dST_dT = self.S_over_T_fn.derivative()
            dST_dT_vec = dST_dT(self.T_domain)

            self.dST_dT = dST_dT
            self.dST_dT_vec = dST_dT_vec

            # For smoothing
            smoothed_data = savgol_filter(
                dST_dT_vec, self.window_length, 2, mode="mirror"
            )
            smoothed_data[-self.window_length :] = dST_dT_vec[-self.window_length :]
            self.smoothed_dST_dT_vec = smoothed_data

    def findBetas(self, smoothing=True):
        if self.dST_dT_vec is None:
            self.gradST()
        if self.smoothing:
            return self.smoothed_dST_dT_vec * self.T_domain
        else:
            return self.dST_dT_vec * self.T_domain

    def report(self):
        if self.Tnuc is None:
            raise ValueError("Tnuc not found")
        if self.Tcrit is None:
            raise ValueError("Tcrit not found")
        if self.dST_dT_Tn is None:
            raise ValueError("dST_dT_Tn not found")
        action_finder = ActionFinder(self.potential, self.start_phase)
        action = action_finder.findAction(self.Tnuc)
        return {
            "T0": self.T0,
            "Tnuc": self.Tnuc,
            "Tcrit": self.Tcrit,
            "S/Tnuc": action / self.Tnuc,
            "alpha": self.potential.alpha(self.Tnuc, self.g_star),
            "beta": self.dST_dT_Tn * self.Tnuc,
        }

    def findDR(self):
        if len(self.S_vec) < 3:
            raise ValueError("Not enough actions to spline")
        result = np.zeros(len(self.T_domain))
        for i, (S, T) in enumerate(zip(self.S_vec, self.T_domain)):
            result[i] = np.exp(-S / T) * T**4 * (S / (T * 2 * np.pi)) ** 1.5
        self.DR_vec = result

    def findHubbleTemp(self):
        self.Hubble_vec = (
            np.pi / (3 * self.Mp) * np.sqrt(self.g_star / 10) * self.T_domain**2
        )

    def findDPdT(self):
        self.dPdT_vec = self.DR_vec / (self.T_domain * self.Hubble_vec**4)

    def findP(self):
        if self.dPdT_vec[0] > 0:
            print("Warning: dPdT[0] is not zero")
            idx_zero = np.where(self.dPdT_vec <= 0)[0][0]
            T_finite = self.T_domain[0 : idx_zero]
            y_finite = self.dPdT_vec[0 : idx_zero]
        else:
            y_temp = self.dPdT_vec[1:]
            idx_zero = np.where(y_temp <= 0)[0][0]
            T_finite = self.T_domain[1 : idx_zero + 1]
            y_finite = self.dPdT_vec[1 : idx_zero + 1]

        self.log_dPdT_fn = PchipInterpolator(T_finite, np.log(y_finite))

        def integral(t):
            if t >= T_finite[-1]:
                return 0
            return quad(lambda t: np.exp(self.log_dPdT_fn(t)), t, T_finite[-1])[0]

        self.P_fn = integral


#@ray.remote
class ActionFinder:
    def __init__(self, potential, start_phase):
        self.potential = potential
        self.start_phase = start_phase
        self.outdict = {}

    def findAction(self, T: float, phitol=1e-8, overlap_angle=45.0):
        if T in self.outdict:
            return self.outdict[T]["action"]

        try:
            def fmin(x):
                return optimize.fmin(
                    self.potential.Vtot, x, args=(T,), xtol=phitol, ftol=np.inf, disp=False
                )

            x0 = fmin(self.start_phase.valAt(T))
            V0 = self.potential.Vtot(x0, T)

            tunnel_list = []
            for key, p in self.potential.phases.items():
                if key == self.start_phase.key:
                    continue
                if p.T[0] > T or p.T[-1] < T:
                    continue
                x1 = fmin(p.valAt(T))
                V1 = self.potential.Vtot(x1, T)
                if V1 >= V0:
                    continue
                tdict = dict(
                    low_vev=x1,
                    high_vev=x0,
                    Tnuc=T,
                    low_phase=key,
                    high_phase=self.start_phase.key,
                )
                tunnel_list.append(tdict)

            # Check for overlap
            if overlap_angle > 0.0:
                excluded = []
                cos_overlap = np.cos(np.deg2rad(overlap_angle))
                for i in range(1, len(tunnel_list)):
                    for j in range(i):
                        xi = tunnel_list[i]["low_vev"]
                        xj = tunnel_list[j]["low_vev"]
                        xi2 = np.sum((xi - x0) ** 2)
                        xj2 = np.sum((xj - x0) ** 2)
                        dotij = np.sum((xj - x0) * (xi - x0))
                        if dotij >= np.sqrt(xi2 * xj2) * cos_overlap:
                            excluded.append(i if xi2 > xj2 else j)
                for i in sorted(excluded)[::-1]:
                    del tunnel_list[i]

            def V_(x, T=T):
                return self.potential.Vtot(x, T)

            def dV_(x, T=T):
                return self.potential.gradV(x, T)

            lowest_action = np.inf
            for tdict in tunnel_list:
                x1 = tdict["low_vev"]
                try:
                    tobj = pathDeformation.fullTunneling([x1, x0], V_, dV_, callback_data=T)
                    tdict["instanton"] = tobj
                    tdict["action"] = tobj.action
                    tdict["trantype"] = 1
                except tunneling1D.PotentialError as err:
                    if err.args[1] == "no barrier":
                        tdict["trantype"] = 0
                        tdict["action"] = 0.0
                    elif err.args[1] == "stable, not metastable":
                        tdict["trantype"] = 0
                        tdict["action"] = 0.0
                    else:
                        print("Unexpected error message.")
                        raise
                if tdict["action"] <= lowest_action:
                    lowest_action = tdict["action"]
            if lowest_action == np.inf:
                lowest_action = 0.0
            return lowest_action
        except Exception as e:
            return 0
