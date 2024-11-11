# -*- coding: utf-8 -*-
from atmosphere_gost import sa
from math import isclose

###############################################################################
#------------------( Тестовая выборка из таблиц ГОСТ 4401-81 )----------------# 
###############################################################################
example_data = {
# h_geom[м]:  (  T[К],      p[Па], rho[кг/м3],    mfp[м],  mu[Па*с], lam[Вт/(м*К)] )
      -1150: (295.626, 1.15927e+5, 1.36609e+0, 5.9477e-8, 1.8252e-5, 2.5929e-2),
       1650: (277.428, 8.30155e+4, 1.04243e-0, 7.7944e-8, 1.7372e-5, 2.4495e-2),
       6950: (243.024, 4.13947e+4, 5.93381e-1, 1.3693e-7, 1.5629e-5, 2.1713e-2),
      15450: (216.650, 1.12859e+4, 1.81475e-1, 4.4773e-7, 1.4216e-5, 1.9518e-2),
      26300: (222.842, 2.09072e+3, 3.26842e-2, 2.4860e-6, 1.4554e-5, 2.0038e-2),
      39000: (247.584, 3.28820e+2, 4.62672e-3, 1.7561e-5, 1.5866e-5, 2.2087e-2),
      49200: (270.650, 8.81183e+1, 1.13422e-3, 7.1637e-5, 1.7037e-5, 2.3954e-2),
      62400: (240.428, 1.57858e+1, 2.28728e-4, 3.5523e-4, 1.5493e-5, 2.1500e-2),
      79200: (200.199, 1.20301e+0, 2.09336e-5, 3.8814e-3, 1.3297e-5, 1.8121e-2),
}


def test_get_state_at():
    """ Проверяет расчёт параметров состояния газа на нескольких геометрических высотах """
    for h, data in example_data.items():
        T, p, rho, *_ = data
        ph, Th, rhoh = sa.get_state_at(h)
        assert isclose(T, Th, abs_tol=1e-3), f'h={h} --> T_calc={Th:.3f} vs T_table={T}'
        assert isclose(p, ph, rel_tol=1e-5), f'h={h} --> p_calc={ph:.5e} vs p_table={p:.5e}'
        assert isclose(rho, rhoh, rel_tol=1e-5), f'h={h} --> rho_calc={rhoh:.5e} vs rho_table={rho:.5e}'


def test_mean_free_path():
    """ Проверяет расчёт длины свободного пробега """
    for h, data in example_data.items():
        _, _, _, mfp, *_ = data
        mfph = sa.mean_free_path(h)
        assert isclose(mfp, mfph, rel_tol=1e-4), f'h={h} --> mfp_calc={mfph:.5e} vs mfp_table={mfp:.5e}'


def test_viscosity():
    """ Проверка расчёта динамической вязкости """
    for h, data in example_data.items():
        _, _, _, _, mu, *_ = data
        muh = sa.viscosity(h)
        assert isclose(mu, muh, rel_tol=1e-4), f'h={h} --> mfp_calc={muh:.5e} vs mfp_table={mu:.5e}'


def test_heat_conductivity():
    """ Проверка расчёта теплопроводности """
    for h, data in example_data.items():
        _, _, _, _, _, lam, *_ = data
        lamh = sa.heat_conductivity(h)
        assert isclose(lam, lamh, rel_tol=1e-4), f'h={h} --> mfp_calc={lamh:.5e} vs mfp_table={lam:.5e}'
