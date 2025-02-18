# -*- coding: utf-8 -*-
# +
"""
simulation.py
========================
module for simulation
"""
import numpy as np
import pandas as pd
# import ray
from scipy import interpolate
from .utilities import J

# function claim
# -


def simulate_jump(model_res, θ_list, ME=None,  y_start=1,  T=100, dt=1):
    """
    Simulate temperature anomaly, emission, distorted probabilities of climate models,
    distorted probabilities of damage functions, and drift distortion.
    When ME is asigned value, it will also simulate paths for marginal value of emission

    Parameters
    ----------
    model_res : dict
        A dictionary storing solution with misspecified jump process.
        See :func:`~src.model.solve_hjb_y_jump` for detail.
    θ_list : (N,) ndarray::
        A list of matthew coefficients. Unit: celsius/gigaton of carbon.
    ME : (N,) ndarray
        Marginal value of emission as a function of y.
    y_start : float, default=1
        Initial value of y.
    T : int, default=100
        Time span of simulation.
    dt : float, default=1
        Time interval of simulation.

    Returns
    -------
    simulation_res: dict of ndarrays
        dict: {
            yt : (T,) ndarray
                Temperature anomaly trajectories.
            et : (T,) ndarray
                Emission trajectories.
            πct : (T, L) ndarray
                Trajectories for distorted probabilities of climate models.
            πdt : (T, M) ndarray
                Trajectories for distorted probabilities of damage functions.
            ht : (T,) ndarray
                Trajectories for drift distortion.
            if ME is not None, the dictionary will also include
                me_t : (T,) ndarray
                    Trajectories for marginal value of emission.
        }
    """
    y_grid = model_res["y"]
    ems = model_res["e_tilde"]
    πc = model_res["πc"]
    πd = model_res["πd"]
    h = model_res["h"]
    periods = int(T/dt)
    et = np.zeros(periods)
    yt = np.zeros(periods)
    πct = np.zeros((periods, len(θ_list)))
    πdt = np.zeros((periods, len(πd)))
    ht = np.zeros(periods)
    if ME is not None:
        me_t = np.zeros(periods)
    # interpolate
    get_πd = interpolate.interp1d(y_grid, πd)
    get_πc = interpolate.interp1d(y_grid, πc)
#     y = np.mean(θ_list)*290
    y = y_start
    for t in range(periods):
        if y > np.max(y_grid):
            break
        else:
            ems_point = np.interp(y, y_grid, ems)
            πd_list = get_πd(y)
            πc_list = get_πc(y)
            h_point = np.interp(y, y_grid, h)
            if ME is not None:
                me_point = np.interp(y, y_grid, ME)
                me_t[t] = me_point
            et[t] = ems_point
            πdt[t] = πd_list
            πct[t] = πc_list
            ht[t] = h_point
            yt[t] = y
            dy = ems_point*np.mean(θ_list)*dt
            y = dy + y
    if ME is not None:
        simulation_res = dict(yt=yt, et=et, πct=πct, πdt=πdt, ht=ht, me_t=me_t)
    else:
        simulation_res = dict(yt=yt, et=et, πct=πct, πdt=πdt, ht=ht)
    return simulation_res


def simulate_me(y_grid, e_grid, ratio_grid, θ=1.86/1000., y_start=1, T=100, dt=1):
    """
    simulate trajectories of uncertainty decomposition

    .. math::

        \\log(\\frac{ME_{new}}{ME_{baseline}})\\times 1000.

    Parameters
    ----------
    y_grid : (N, ) ndarray
        Grid of y.
    e_grid : (N, ) ndarray
        Corresponding :math:`\\tilde{e}` on the grid of y.
    ratio_grid : (N, ) ndarray::
        Corresponding :math:`\\log(\\frac{ME_{new}}{ME_{baseline}})\\times 1000` on the grid of y.
    θ : float, default=1.86/1000
        Coefficient used for simulation.
    y_start : floatsimulation
        Initial value of y.
    T : int, default=100
        Time span of simulation.
    dt : float, default=1
        Time interval of simulation. Default=1 indicates yearly simulation.

    Returns
    -------
    Et : (T, ) ndarray
        Emission trajectory.
    yt : (T, ) ndarray
        Temperature anomaly trajectories.
    ratio_t : (T, ) ndarray
        Uncertainty decomposition ratio trajectories.
    """
    periods = int(T/dt)
    Et = np.zeros(periods+1)
    yt = np.zeros(periods+1)
    ratio_t = np.zeros(periods+1)
    for i in range(periods+1):
        Et[i] = np.interp(y_start, y_grid, e_grid)
        ratio_t[i] = np.interp(y_start, y_grid, ratio_grid)
        yt[i] = y_start
        y_start = y_start + Et[i]*θ
    return Et, yt, ratio_t


def no_jump_simulation(
    model_res,
    y_start=1.1,
    T=130,
    dt=1,
):
    y = y_start
    periods = int(T / dt)
    e_tilde = model_res["e_tilde"]
    y_grid_short = model_res["y"]
    h = model_res["h"]
    πc = model_res["πc"]
    πd = model_res["πd"]
    y_bar = model_res["model_args"][4]
    θ_list = model_res["model_args"][8]
    et = np.zeros(periods)
    yt = np.zeros(periods)
    ht = np.zeros(periods)
    probt = np.zeros(periods)
    πdt = np.zeros((periods, len(πd)))
    πct = np.zeros((periods, len(πc)))

    get_d = interpolate.interp1d(y_grid_short, πd)
    get_c = interpolate.interp1d(y_grid_short, πc)
    for t in range(periods):
        if y <= y_bar:
            e_i = np.interp(y, y_grid_short, e_tilde)
            h_i = np.interp(y, y_grid_short, h)
            intensity = J(y)
            et[t] = e_i
            ht[t] = h_i
            probt[t] = intensity * dt
            yt[t] = y
            πct[t] = get_c(y)
            πdt[t] = get_d(y)
            y = y + e_i * np.mean(θ_list) * dt
        else:
            break
    yt = yt[np.nonzero(yt)]
    et = et[np.nonzero(et)]
    ht = ht[np.nonzero(ht)]
    probt = probt[:len(yt)]
    πdt = πdt[:len(yt)]
    πct = πct[:len(yt)]

    res = {
        "et": et,
        "yt": yt,
        "probt": probt,
        "πct": πct,
        "πdt": πdt,
        "ht": ht,
    }

    return res


def damage_intensity(y, y_underline):
    r1 = 1.5
    r2 = 2.5
    return r1 * (np.exp(r2/2 * (y - y_underline)**2) - 1) * (y >= y_underline)

class EvolutionState:
    DAMAGE_MODEL_NUM = 20
    DAMAGE_PROB = np.ones(20) / 20
    dt = 1/4

    def __init__(self, t, prob, damage_jump_state, damage_jump_loc, variables, y_underline, y_overline):
        self.t = t
        self.prob = prob
        self.damage_jump_state = damage_jump_state
        self.damage_jump_loc = damage_jump_loc
        self.variables = variables
        self.y_underline = y_underline
        self.y_overline = y_overline

    def set_damage(self, damage_model_num, damage_prob_fun):
        """set damage model number
        """
        self.DAMAGE_MODEL_NUM = damage_model_num
        self.DAMAGE_PROB = damage_prob_fun

    def set_time_step(self, dt):
        self.dt = dt

    def copy(self):
        return EvolutionState(self.t,
                              self.prob,
                              self.damage_jump_state,
                              self.damage_jump_loc,
                              self.variables,
                              self.y_underline,
                              self.y_overline)

    def evolve(self, θ_mean, fun_args, damage_distortion=(False, None)):

        e_fun_pre_damage, e_fun_post_damage = fun_args
        DISTORTED, damage_prob_func = damage_distortion
        [e, y, temp_anol] = self.variables
        prob_old = self.prob
        damage_loc_old = self.damage_jump_loc
        damage_state_old = self.damage_jump_state
        # Update probabilities
        temp = damage_intensity(y, self.y_underline)
        damage_jump_prob = temp * self.dt
        if damage_jump_prob > 1:
            damage_jump_prob = 1
        if DISTORTED:
            DAMAGE_PROB = np.zeros(self.DAMAGE_MODEL_NUM)
            for i in range(self.DAMAGE_MODEL_NUM):
                DAMAGE_PROB[i] = damage_prob_func[i](temp_anol)
        else:
            DAMAGE_PROB = self.DAMAGE_PROB
        # Compute variables at t+1
        if self.damage_jump_state == 'pre' and damage_jump_prob != 0:
            states_new = []
            # jump
            for i in range(self.DAMAGE_MODEL_NUM):
                e_fun = e_fun_post_damage[i]
                y_new = 2
                e_new = e_fun(y_new)
                temp_anol_new = temp_anol + e_new * θ_mean * self.dt
                prob_new = DAMAGE_PROB[i] * damage_jump_prob * prob_old
                damage_state = "post"
                damage_loc = i
                variables_new = [e_new, y_new, temp_anol_new]
                state = EvolutionState(self.t+ self.dt,
                                      prob_new,
                                      damage_state,
                                      damage_loc,
                                      variables_new,
                                      self.y_underline,
                                      self.y_overline)
                states_new.append(state)
            # no jump
            e_fun = e_fun_pre_damage
            e_new = e_fun(y)
            y_new = y + e_new * θ_mean * self.dt
            temp_anol_new = temp_anol + e_new * θ_mean * self.dt
            prob_new = (1 - damage_jump_prob) * prob_old
            damage_state = "pre"
            damage_loc = None
            variables_new = [e_new, y_new, temp_anol_new]
            state = EvolutionState(self.t+ self.dt,
                                      prob_new,
                                      damage_state,
                                      damage_loc,
                                      variables_new,
                                      self.y_underline,
                                      self.y_overline)
            states_new.append(state)
        else:
            # jump happened
            if self.damage_jump_state == "post":
                e_fun = e_fun_post_damage[damage_loc_old]
            else:
                e_fun = e_fun_pre_damage
            e_new = e_fun(y)
            y_new = y + e_new * θ_mean * self.dt
            temp_anol_new = temp_anol + e_new * θ_mean * self.dt
            prob_new = 1 * prob_old
            variables_new = [e_new, y_new, temp_anol_new]
            state = EvolutionState(self.t+ self.dt,
                                      prob_new,
                                      damage_state_old,
                                      damage_loc_old,
                                      variables_new,
                                      self.y_underline,
                                      self.y_overline)
            states_new = [state]


        return states_new


def simulate_jump_2(model_res_pre, model_res_post, y_upper, θ_list, ME=None,  y_start=1.1,  T=100, dt=1):
    """
    Simulate temperature anomaly, emission, distorted probabilities of climate models,
    distorted probabilities of damage functions, and drift distortion.
    When ME is asigned value, it will also simulate paths for marginal value of emission

    Parameters
    ----------
    model_res : dict
        A dictionary storing solution with misspecified jump process.
        See :func:`~src.model.solve_hjb_y_jump` for detail.
    θ_list : (N,) ndarray::
        A list of matthew coefficients. Unit: celsius/gigaton of carbon.
    ME : (N,) ndarray
        Marginal value of emission as a function of y.
    y_start : float, default=1
        Initial value of y.
    T : int, default=100
        Time span of simulation.
    dt : float, default=1
        Time interval of simulation.

    Returns
    -------
    simulation_res: dict of ndarrays
        dict: {
            yt : (T,) ndarray
                Temperature anomaly trajectories.
            et : (T,) ndarray
                Emission trajectories.
            πct : (T, L) ndarray
                Trajectories for distorted probabilities of climate models.
            πdt : (T, M) ndarray
                Trajectories for distorted probabilities of damage functions.
            ht : (T,) ndarray
                Trajectories for drift distortion.
            if ME is not None, the dictionary will also include
                me_t : (T,) ndarray
                    Trajectories for marginal value of emission.
        }
    """
    y_grid = model_res_pre["y"]
    ems = model_res_pre["e_tilde"]
    πc = model_res_pre["πc"]
    πd = model_res_pre["πd"]
    h = model_res_pre["h"]
    periods = int(T/dt)
    et = np.zeros(periods)
    yt = np.zeros(periods)
    πct = np.zeros((periods, len(θ_list)))
    πdt = np.zeros((periods, len(πd)))
    ht = np.zeros(periods)
    if ME is not None:
        me_t = np.zeros(periods)
    # interpolate
    get_πd = interpolate.interp1d(y_grid, πd)
    get_πc = interpolate.interp1d(y_grid, πc)
#     y = np.mean(θ_list)*290
    y = y_start
    kkkk=0
    threshold = 0
    for t in range(periods):
            if y_upper >= y:
                ems_point = np.interp(y, y_grid, ems)
                πd_list = get_πd(y)
                πc_list = get_πc(y)
                h_point = np.interp(y, y_grid, h)
                if ME is not None:
                    me_point = np.interp(y, y_grid, ME)
                    me_t[t] = me_point
                et[t] = ems_point
                πdt[t] = πd_list
                πct[t] = πc_list
                ht[t] = h_point
                yt[t] = y
                dy = ems_point*np.mean(θ_list)*dt
                y = dy + y
                K=t
            else:
                if kkkk==0:
                    threshold = K
                    y_grid = model_res_post["y"]
                    ems    = model_res_post["e_tilde"]
                    πc     = model_res_post["πc"]
                    h      = model_res_post["h"]
                    get_πc = interpolate.interp1d(y_grid, πc)
                    kkkk=1
                ems_point = np.interp(y, y_grid, ems)
                πᶜ_list = get_πᶜ(y)
                et[t] = ems_point
                πᶜt[t] = πᶜ_list
                ht[t] = h_point
                yt[t] = y
                dy = ems_point*np.mean(θ_list)*dt
                y = dy + y
                K=t
    if ME is not None:
        simulation_res = dict(yt=yt, et=et, πct=πct, πdt=πdt, ht=ht, me_t=me_t)
    else:
        simulation_res = dict(yt=yt[0:K], et=et[0:K], πct=πct[0:K], πdt=πdt[0:K], ht=ht[0:K], threshold = threshold)
    return simulation_res

def jump_once(e_short, e_long, θ, πc_func, πd_distort, 
                Y0=1.1, T=100, dt=1, Y_underline=1.5, Y_overline=2.):
    periods = int( T / dt )
    NUM_DAMAGE = len(πd_distort(Y0))
    Yt = np.zeros(periods + 1)
    Tempt = np.zeros(periods + 1)
    Et = np.zeros(periods + 1)
    Yt[0] = Y0
    JUMPED = 0
    damage_loc = np.full(periods+1, None)
    πc = πc_func(Y0) # (144, ) array
    # random draw climate parameters
    climate_loc = np.random.choice(len(θ), 1, p=πc)
    θ_j = θ[climate_loc]
    for t in range(periods):
        if Yt[t] <= Y_underline:
            e_func = e_short
            Et[t] = e_func(Yt[t])
            Yt[t+1] = Yt[t] + θ_j * Et[t] * dt
            Tempt[t+1] = Tempt[t] + θ_j * Et[t] * dt
        else:
            # jump prob
            if JUMPED == 0:
                jump_prob = damage_intensity(Yt[t], Y_underline) * dt
                JUMPED = np.random.choice(2, p=[1 - jump_prob, jump_prob])
                if JUMPED == 1:
                    # jumped
                    damage_prob = πd_distort(Yt[t])
                    damage_loc[t] = np.random.choice(NUM_DAMAGE, 1, p=damage_prob)[0]
                    e_func = e_long[damage_loc[t]]
                    Yt[t+1] = 2.
                    Et[t] = e_func(2.)
                    Tempt[t+1] = Tempt[t] + θ_j * Et[t] * dt
                else:
                    Et[t] = e_short(Yt[t])
                    Yt[t+1] = Yt[t] + θ_j * Et[t] * dt
                    Tempt[t+1] = Tempt[t] + θ_j * Et[t] * dt
                   
            else:
                # jumped
                Et[t] = e_func(Yt[t])
                Yt[t+1] = Yt[t] + θ_j * Et[t] * dt
                Tempt[t+1] = Tempt[t] + θ_j * Et[t] * dt
                damage_loc[t] =  damage_loc[t - 1]
    Et[periods] = e_func(Yt[periods])
    damage_loc[periods] = damage_loc[periods - 1]
      
    return damage_loc, climate_loc, Et, Yt, Tempt



def jump_once_theta(e_short, e_long, θ, πc_func_short, πc_func_long, πd_distort, 
                Y0=1.1, T=100, dt=1, Y_underline=1.5, Y_overline=2.):
    periods = int( T / dt )
    NUM_DAMAGE = len(πd_distort(Y0))
    Yt = np.zeros(periods + 1)
    Tempt = np.zeros(periods + 1)
    Et = np.zeros(periods + 1)
    Yt[0] = Y0
    Tempt[0] = Y0
    JUMPED = 0
    damage_loc = np.full(periods+1, None)
    climate_loc = np.full(periods + 1, None)
    for t in range(periods):
        if Yt[t] <= Y_underline:
            e_func = e_short
            Et[t] = e_func(Yt[t])
            πc_func = πc_func_short
            πc = πc_func(Yt[t])
            Yt[t+1] = Yt[t] + np.average(θ, weights=πc) * Et[t] * dt
            Tempt[t+1] = Tempt[t] + np.average(θ, weights=πc) * Et[t] * dt
        else:
            # jump prob
            if JUMPED == 0:
                jump_prob = damage_intensity(Yt[t], Y_underline) * dt
                if jump_prob > 1:
                    jump_prob = 1
                elif Yt[t] >= Y_overline:
                    jump_prob = 1
                JUMPED = np.random.choice(2, p=[1 - jump_prob, jump_prob])
                if JUMPED == 1:
                    # jumped
                    damage_prob = πd_distort(Yt[t])
                    damage_loc[t] = np.random.choice(NUM_DAMAGE, 1, p=damage_prob)[0]
                    # climate probability revealed
                    πc_func = πc_func_long[damage_loc[t]]
                    πc = πc_func(2.)
                    climate_loc[t] = np.random.choice(len(θ), 1, p=πc)[0]
                    e_func = e_long[damage_loc[t]]
                    Yt[t+1] = 2.
                    Et[t] = e_func(2.)
                    θ_j = θ[climate_loc[t]]
                    Tempt[t+1] = Tempt[t] + θ_j * Et[t] * dt
                else:
                    Et[t] = e_short(Yt[t])
                    πc_func = πc_func_short
                    πc = πc_func(Yt[t])
                    Yt[t+1] = Yt[t] + np.average(θ, weights=πc) * Et[t] * dt
                    Tempt[t+1] = Tempt[t] + np.average(θ, weights=πc) * Et[t] * dt
                   
            else:
                # jumped
                Et[t] = e_func(Yt[t])
                πc = πc_func(Yt[t])
                Yt[t+1] = Yt[t] + np.average(θ, weights=πc) * Et[t] * dt
                Tempt[t+1] = Tempt[t] + np.average(θ, weights=πc) * Et[t] * dt
                damage_loc[t] =  damage_loc[t - 1]
                climate_loc[t] = climate_loc[t - 1]
    Et[periods] = e_func(Yt[periods])
    damage_loc[periods] = damage_loc[periods - 1]
    climate_loc[periods] = climate_loc[periods - 1]
      
    return damage_loc, climate_loc, Et, Yt, Tempt
