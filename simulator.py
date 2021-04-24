""" Tennessee Eastman process simulation

Simulating the Tennessee Eastman [1]_ process with Python

Classes
-------
StateVar: class
    State variable storage
TEP: class
    The process simulator class

References
----------
.. [1] J. J. Downs and E. F. Vogel, “A plant-wide industrial process control
        problem,” Computers & Chemical Engineering, vol. 17, no. 3,
        pp. 245–255, 1993.
"""
__author__ = "Hussein Saafan"

import numpy as np


class StateVar:
    """ State variable storage

    Special class for storage of variables for ease of differentiation,
    integration and properties of variables such as limits and units.

    Attributes
    ----------
    base_value: float
        The initial value of the variable
    value: float
        The current value of the variable
    prev_vals: numpy.ndarray
        An array containing some previous values of the variable
    num_prev_vals: int
        The number of previous values to store
    units: str
        The units of the variable
    desc: str
        A short description of the variable
    low_limit: float
        The lower control limit
    high_limit: float
        The higher control limit
    """
    base_value = None
    value = None
    prev_vals = None
    num_prev_vals = 3
    units = None
    desc = None
    low_limit = None
    high_limit = None

    def __init__(self, base_value, units, desc):
        self.base_value = base_value
        self.value = base_value
        self.units = units
        self.desc = desc
        self.prev_vals = np.zeros((self.num_prev_vals))

    def __repr__(self):
        return(f"{self.value:{10}.{5}} {self.units:{10}} [{self.desc}]")

    def __str__(self):
        return(self.__repr__())

    def limit(self, low_limit, high_limit, pct_limit=None):
        self.low_limit = low_limit
        self.high_limit = high_limit
        if pct_limit is not None:
            val = (pct_limit / 100) * (high_limit - low_limit)
            self.value = val
            self.base_value = val
        return

    def set_num_prev_vals(self, number):
        self.num_prev_vals = number
        self.prev_vals = np.zeros((number))
        return

    def set_value_as_pct_limit(self, pct_limit):
        val = (pct_limit / 100) * (self.high_limit - self.low_limit)
        self.set_value(val)
        return

    def set_value(self, value):
        self.prev_vals = np.roll(self.prev_vals, 1)
        self.prev_vals[0] = self.value
        self.value = val
        return


class TEP:

    state = None

    def __init__(self):
        self._initialize_state()

    def _initialize_state(self):
        XMV01 = StateVar(0, 'kg/h', 'D Feed Flow (Stream 2)')
        XMV01.limit(0, 5811, 63.053)
        XMV02 = StateVar(0, 'kg/h', 'E Feed Flow (Stream 3)')
        XMV02.limit(0, 8354, 53.980)
        XMV03 = StateVar(0, 'kscmh', 'A Feed Flow (Stream 1)')
        XMV03.limit(0, 1.017, 24.644)        
        XMV04 = StateVar(0, 'kscmh', 'A and C Feed Flow (Stream 4)')
        XMV04.limit(0, 15.25, 61.302)
        XMV05 = StateVar(0, '%', 'Compressor Recycle Valve')
        XMV05.limit(0, 100, 22.210)
        XMV06 = StateVar(0, '%', 'Purge Valve (Stream 9)')
        XMV06.limit(0, 100, 40.064)
        XMV07 = StateVar(0, 'm**3/h', 'Separator Pot Liquid Flow (Stream 10)')
        XMV07.limit(0, 65.71, 38.100)
        XMV08 = StateVar(0, 'm**3/h', 'Stripper Liquid Product Flow (Stream 11)')
        XMV08.limit(0, 49.10, 46.534)
        XMV09 = StateVar(0, '%', 'Stripper Steam Valve')
        XMV09.limit(0, 100, 47.446)
        XMV10 = StateVar(0, 'm**3/h', 'Reactor Cooling Water Flow')
        XMV10.limit(0, 227.1, 41.106)
        XMV11 = StateVar(0, 'm**3/h', 'Condenser Cooling Water Flow')
        XMV11.limit(0, 272.6, 18.114)
        XMV12 = StateVar(0, 'rpm', 'Agitator Speed')
        XMV12.limit(150, 250, 50.000)

        XMEAS01 = StateVar(0.25052, 'kscmh', 'A Feed (Stream 1)')
        XMEAS02 = StateVar(3664.0, 'kg/h', 'D Feed (Stream 2)')
        XMEAS03 = StateVar(4509.3, 'kg/h', 'E Feed (Stream 3)')
        XMEAS04 = StateVar(9.3477, 'kscmh', 'A and C Feed (Stream 4)')
        XMEAS05 = StateVar(26.902, 'kscmh', 'Recycle Flow (Stream 8)')
        XMEAS06 = StateVar(42.339, 'kscmh', 'Reactor Feed Rate (Stream 6)')
        XMEAS07 = StateVar(2705.0, 'kPag', 'Reactor Pressure')
        XMEAS08 = StateVar(75.000, '%', 'Reactor Level')
        XMEAS08.limit(0, 100)
        XMEAS09 = StateVar(120.40, 'C', 'Reactor Temperature')
        XMEAS10 = StateVar(0.33712, 'kscmh', 'Purge Rate (Stream 9)')
        XMEAS11 = StateVar(80.109, 'C', 'Product Separator Temperature')
        XMEAS12 = StateVar(50.000, '%', 'Product Separator Level')
        XMEAS12.limit(0, 100)
        XMEAS13 = StateVar(2633.7, 'kPag', 'Product Separator Pressure')
        XMEAS14 = StateVar(25.160, 'm**3/h', 'Product Separator Underflow (Stream 10)')
        XMEAS15 = StateVar(50.000, '%', 'Stripper Level')
        XMEAS15.limit(0, 100)
        XMEAS16 = StateVar(3102.2, 'kPag', 'Stripper Pressure')
        XMEAS17 = StateVar(22.949, 'm**3/h', 'Stripper Underflow (Stream 11)')
        XMEAS18 = StateVar(65.731, 'C', 'Stripper Temperature')
        XMEAS19 = StateVar(230.31, 'kg/h', 'Stripper Steam Flow')
        XMEAS20 = StateVar(341.43, 'kW', 'Compressor Work')
        XMEAS21 = StateVar(94.599, 'C', 'Reactor Cooling Water Outlet Temperature')
        XMEAS22 = StateVar(77.297, 'C', 'Seperator Cooling Water Outlet Temperature')
        XMEAS23 = StateVar(32.188, 'mol%', 'Component A (Stream 6)')
        XMEAS23.limit(0, 100)
        XMEAS24 = StateVar(8.8933, 'mol%', 'Component B (Stream 6)')
        XMEAS24.limit(0, 100)
        XMEAS25 = StateVar(26.383, 'mol%', 'Component C (Stream 6)')
        XMEAS25.limit(0, 100)
        XMEAS26 = StateVar(6.8820, 'mol%', 'Component D (Stream 6)')
        XMEAS26.limit(0, 100)
        XMEAS27 = StateVar(18.776, 'mol%', 'Component E (Stream 6)')
        XMEAS27.limit(0, 100)
        XMEAS28 = StateVar(1.6567, 'mol%', 'Component F (Stream 6)')
        XMEAS28.limit(0, 100)
        XMEAS29 = StateVar(32.958, 'mol%', 'Component A (Stream 9)')
        XMEAS29.limit(0, 100)
        XMEAS30 = StateVar(13.823, 'mol%', 'Component B (Stream 9)')
        XMEAS30.limit(0, 100)
        XMEAS31 = StateVar(23.978, 'mol%', 'Component C (Stream 9)')
        XMEAS31.limit(0, 100)
        XMEAS32 = StateVar(1.2565, 'mol%', 'Component D (Stream 9)')
        XMEAS32.limit(0, 100)
        XMEAS33 = StateVar(18.579, 'mol%', 'Component E (Stream 9)')
        XMEAS33.limit(0, 100)
        XMEAS34 = StateVar(2.2633, 'mol%', 'Component F (Stream 9)')
        XMEAS34.limit(0, 100)
        XMEAS35 = StateVar(4.8436, 'mol%', 'Component G (Stream 9)')
        XMEAS35.limit(0, 100)
        XMEAS36 = StateVar(2.2986, 'mol%', 'Component H (Stream 9)')
        XMEAS36.limit(0, 100)
        XMEAS37 = StateVar(0.01787, 'mol%', 'Component D (Stream 11)')
        XMEAS37.limit(0, 100)
        XMEAS38 = StateVar(0.83570, 'mol%', 'Component E (Stream 11)')
        XMEAS38.limit(0, 100)
        XMEAS39 = StateVar(0.09858, 'mol%', 'Component F (Stream 11)')
        XMEAS39.limit(0, 100)
        XMEAS40 = StateVar(53.724, 'mol%', 'Component G (Stream 11)')
        XMEAS40.limit(0, 100)
        XMEAS41 = StateVar(43.828, 'mol%', 'Component H (Stream 11)')
        XMEAS41.limit(0, 100)

        self.state = {
            "XMV01": XMV01,
            "XMV02": XMV02,
            "XMV03": XMV03,
            "XMV04": XMV04,
            "XMV05": XMV05,
            "XMV06": XMV06,
            "XMV07": XMV07,
            "XMV08": XMV08,
            "XMV09": XMV09,
            "XMV10": XMV10,
            "XMV11": XMV11,
            "XMV12": XMV12,
            "XMEAS01": XMEAS01,
            "XMEAS02": XMEAS02,
            "XMEAS03": XMEAS03,
            "XMEAS04": XMEAS04,
            "XMEAS05": XMEAS05,
            "XMEAS06": XMEAS06,
            "XMEAS07": XMEAS07,
            "XMEAS08": XMEAS08,
            "XMEAS09": XMEAS09,
            "XMEAS10": XMEAS10,
            "XMEAS11": XMEAS11,
            "XMEAS12": XMEAS12,
            "XMEAS13": XMEAS13,
            "XMEAS14": XMEAS14,
            "XMEAS15": XMEAS15,
            "XMEAS16": XMEAS16,
            "XMEAS17": XMEAS17,
            "XMEAS18": XMEAS18,
            "XMEAS19": XMEAS19,
            "XMEAS20": XMEAS20,
            "XMEAS21": XMEAS21,
            "XMEAS22": XMEAS22,
            "XMEAS23": XMEAS23,
            "XMEAS24": XMEAS24,
            "XMEAS25": XMEAS25,
            "XMEAS26": XMEAS26,
            "XMEAS27": XMEAS27,
            "XMEAS28": XMEAS28,
            "XMEAS29": XMEAS29,
            "XMEAS30": XMEAS30,
            "XMEAS31": XMEAS31,
            "XMEAS32": XMEAS32,
            "XMEAS33": XMEAS33,
            "XMEAS34": XMEAS34,
            "XMEAS35": XMEAS35,
            "XMEAS36": XMEAS36,
            "XMEAS37": XMEAS37,
            "XMEAS38": XMEAS38,
            "XMEAS39": XMEAS39,
            "XMEAS40": XMEAS40,
            "XMEAS41": XMEAS41
        }

        return

    def print_state(self):
        for key, val in self.state.items():
            print(f"{key:{10}}: {val}")

    def _simulate_step(self):
        return

    def simulate(self, time, time_step):
        step_arr = np.arange(start=0, stop=time, step=time_step)

        for step in step_arr:
            self._simulate_step(time_step)
        return


if __name__ == "__main__":
    process = TEP()
    process.print_state()
