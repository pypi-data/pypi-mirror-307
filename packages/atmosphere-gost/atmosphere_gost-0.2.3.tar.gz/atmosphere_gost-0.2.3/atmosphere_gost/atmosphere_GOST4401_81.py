# -*- coding: utf-8 -*-
from math import log10, sqrt, pi
from typing import NoReturn


class StandardAtmosphere:
    """ Реализация модели стандартной атмосферы, ГОСТ 4401-81 """
    
    # Параметры на высоте среднего уровня моря
    ac = 340.294  # скорость звука, м/с
    gc = 9.80665  # ускорение свободного падения, м/с2
    Hpc = 8434.5  # масштаб высоты по давлению, м
    lc = 66.328e-9  # средняя длина свободного пробега частиц воздуха
    Mc = 28.964420  # молярная масса, кг/кмоль  (NB! размерность)
    nc = 25.471e+24  # концентрация частиц
    pc = 101325.0  # давление
    Tc = 288.15  # температура
    vc = 458.94  # средняя скорость частиц воздуха, м/с
    gammac = 12.013  # удельный вес, Н/м3
    nuc = 14.607e-6  # кинематическая вязкость, м2/с
    muc = 17.894e-6  # динамическая вязкость, Па*с
    lambdac = 25.343e-3  # теплопроводность, Вт/(м*К)
    omc = 6.9193e+9  # частота соударений частиц воздуха (#TODO: NB! проверить значение)
    rhoc = 1.2250  # плотность, кг/м3
    
    Na = 602.257e24  # постоянная Авогадро, 1/кмоль (NB! размерность)
    Rgas = 8314.32  # универсальная газовая постоянная, Дж / (К*кмоль) (NB! размерность)
    R = 287.05287  # удельная газовая постоянная, Дж / (кг*К)
    S = 110.4  # температура в законе динамической вязкости Сазерленда, К
    betaS = 1.458e-6  # коэффициент из закона Сазерленда, кг / (с*м*К^0.5)
    sigma = 0.365e-9  # эффективный диаметр молекул воздуха при столкновении, м
    
    
    def __init__(self):
        # Подготавливаем опорные величины для расчёта атмосферы
        # NB! Давление на всех промежутках рассчитывается по цепочке
        # исходя из значения на уровне моря, которое задано
        self.base = (
            # H[м]  T[K]    beta[-]  p[Pa]
            [-2000,  301.15,  -0.0065, None],
            [0,      self.Tc, -0.0065, self.pc],
            [11000,  216.65,  +0,      None],
            [20000,  216.65,  +0.001,  None],
            [32000,  228.65,  +0.0028, None],
            [47000,  270.65,  +0,      None],
            [51000,  270.65,  -0.0028, None],
            [71000,  214.65,  -0.002,  None],
            [85000,  186.65,  +0,      None],
        )
        self._prepare_base()

    
    def _prepare_base(self) -> NoReturn:
        """ Прямое вычисление величин опорного давления """
        for i in range(2, len(self.base)):
            self._update_pbase_at_pos(i)
        self._update_pbase_at_pos(0, is_base_prev=False)
    
    
    def _update_pbase_at_pos(self,
                            i: int,
                            is_base_prev : bool = True) -> NoReturn:
        """ Прямой расчёт опорного давления для строки i таблицы self.base """
        ib = i - 1 if is_base_prev else i + 1
        Hb, Tb, beta, pb = self.base[ib]
        H = self.base[i][0]
        T = self._get_T(Tb, beta, H, Hb)
        p = self._get_p(T, Tb, pb, beta, H, Hb)
        self.base[i][-1] = p

    
    def convert_heihgt(self, h: float, to : str = 'H') -> float:
        """ Конвертирует высоты """
        r = 6356767
        if to == 'H':  # геометрическая в геопотенциальную
            return r * h / (r + h)
        elif to == 'h':  # геопотенциальная в геометрическую
            return r * h / (r - h)
        raise ValueError(f'to={to}, но допустимы только типы конвертации H (геом. в геопот.) и h (геопот. в геом.)')
        
    
    def _get_base_params(self, H: float) -> tuple[float, float, float, float]:
        """
        Возвращает опорные параметры на заданной геопотенциальной высоте
        
        Parameters
        ----------
        H : float
            Геопотенциальная высота.

        Raises
        ------
        ValueError
            Задана неподдерживаемое значение -2км > H > 94км.

        Returns
        -------
        tuple[float, float, float, float]
            Опорные параметры для расчёта атмосферы H[м], T[K], beta[-], p[Pa]

        """
        if H < self.base[0][0] or H > 94000:
            msg = f'H={H}: реализован расчёт температуры лишь для геопотенциальных высот от -2000м до 94000м'
            raise ValueError(msg)

        for base in self.base[::-1]:
            if H >= base[0]: return base

    
    def get_state_at(self, h: float) -> tuple[float, float, float]:
        """
        Состояние воздуха на заданной высоте

        Parameters
        ----------
        h : float
            Геометрическая высота.

        Returns
        -------
        tuple[float, float, float]
            p[Па], T[К], rho[кг/м3].

        """
        H = self.convert_heihgt(h, to='H')
        Hb, Tb, beta, pb = self._get_base_params(H)
            
        T = self._get_T(Tb, beta, H, Hb)
        p = self._get_p(T, Tb, pb, beta, H, Hb)
        
        return p, T, self.rho(p, T)
    
    
    
    def _get_T(self, Tb: float, beta: float, H: float, Hb: float) -> float:
        """
        Температура на заданной геопотенциальной высоте

        Parameters
        ----------
        Tb : float
            Опорная температура [K].
        beta : float
            Градиент температуры по геопотенциальной высоте.
        H : float
            Геопотенциальная высота [м].
        Hb : float
            Опорная геопотенциальная высота [м].

        Returns
        -------
        float
            Температура [К].

        """
        return Tb + beta * (H - Hb)
    
    def _get_p(self, T: float, Tb: float, pb: float,
               beta: float, H: float, Hb: float) -> float:
        """
        Давление на заданной геопотенциальной высоте и при данной температуре

        Parameters
        ----------
        T : float
            Текущая температура [К].
        Tb : float
            Опорная температура [К].
        pb : float
            Опорное давление [Па].
        beta : float
            Градиент температуры по геопотенциальной высоте.
        H : float
            Геопотенциальная высота [м].
        Hb : float
            Опорная геопотенциальная высота [м].

        Returns
        -------
        float
            Давление [Па].

        """
        if beta != 0:
            lgp = log10(pb) - self.gc / (beta * self.R) * log10(T/Tb)
        else:
            lgp = log10(pb) - 0.434294 * self.gc / (self.R * T) * (H - Hb)
        return 10**lgp

    
    def rho(self, p: float, T: float) -> float:
        """
        Плотность из уравнения состояния

        Parameters
        ----------
        p : float
            Давление [Па].
        T : float
            Температура [К].

        Returns
        -------
        float
            Плотность [кг/м3].

        """
        return p / (self.R * T)
    
    
    def mean_free_path(self, h: float) -> float:
        """
        Средняя длина свободного пробега молекул воздуха

        Parameters
        ----------
        h : float
            Геометрическая высота [м].

        Returns
        -------
        float
            Средняя длина свободного пробега молекул воздуха [м].

        """
        p_Pa, T_K, *_ = self.get_state_at(h)
        coef = self.Rgas / (sqrt(2) * pi * self.Na * self.sigma**2)
        return coef * T_K / p_Pa
    
    
    def viscosity(self, h: float) -> float:
        """
        Динамическая вязкость (двухпараметрическая формула Сазерленда ГОСТ, С.178)

        Parameters
        ----------
        h : float
            Геометрическая высота [м].
        
        Raises
        ------
        ValueError
            Выход за область применимости расчётной формулы h<90км.

        Returns
        -------
        float
            Динамическая вязкость [Па*с].

        """
        if h > 90000:
            raise ValueError("h={h:.2f}м, область применимости расчётных формул для динамической вязкости (h<90км).")
        _, T_K, *_ = self.get_state_at(h)

        return self.viscosity_sutherland(T_K)
    
    
    def viscosity_sutherland(self, T_K: float) -> float:
        """
        Формула Сазерленда ГОСТ, С.178
        
        Parameters
        ----------
        T_K : float
            Абсолютная температура [К].
        
        Returns
        -------
        float
            Динамическая вязкость [Па*с].
        """
        return  self.betaS / (T_K + self.S) * T_K**1.5
    
    
    def heat_conductivity(self, h: float) -> float:
        """
        Коэффициент теплопроводности (империческая формула ГОСТ, С. 179)

        Parameters
        ----------
        h : float
            Геометрическая высота [м].

        Raises
        ------
        ValueError
            Выход за область применимости расчётной формулы (h<90км).

        Returns
        -------
        float
            Коэффициент теплопроводности [Вт/(м*К)].

        """
        if h > 90000:
            raise ValueError("h={h:.2f}м, область применимости расчётных формул для теплопроводности: h < 90000м.")
        _, T_K, *_ = self.get_state_at(h)
        return self.heat_conductivity_at_T(T_K)
    
    
    def heat_conductivity_at_T(self, T_K: float) -> float:
        """
        Коэффициент теплопроводности (империческая формула ГОСТ, С. 179)

        Parameters
        ----------
        T_K : float
            Абсолютная температура [К].

        Returns
        -------
        float
            Коэффициент теплопроводности [Вт/(м*К)].

        """
        lam  = 2.648151e-3 * T_K**1.5
        lam /= T_K + 245.4 * 10**(-12/T_K)
        return lam

    
    def get_all(self, h: float) -> tuple[float, float, float, float, float, float]:
        """
        Все доступные параметры атмосферы

        Parameters
        ----------
        h : float
            Геометрическая высота.

        Returns
        -------
        tuple[float, float, float, float, float, float]
            p[Па], T[К], rho[кг/м3], mu[Па*с], lam[Вт/(м*К)], mfp[м].

        """
        p, T, rho = self.get_state_at(h)
        mu = self.viscosity(h)
        lam = self.heat_conductivity(h)
        mfp = self.mean_free_path(h)
        return p, T, rho, mu, lam, mfp
        
    
sa = StandardAtmosphere()


#%% Testing
if __name__ == '__main__':
    import numpy as np
    import matplotlib.pyplot as plt
    
    hh = np.linspace(0, 94000, 95)
    pp, TT, rhos = np.array(list(map(sa.get_state_at, hh))).T
    plt.plot(hh, pp)
    plt.xlim([-2000, 100000])
    plt.gca().set_yscale('log')
    
    plt.xlabel('Высота над средним уровнем моря, м')
    plt.ylabel('Давление, Па')
    
    plt.show()

