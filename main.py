""" Main Module """
__author__ = "Hussein Saafan"
from math import ceil

import materials
import flowsheet


def main(time: float, time_step: float, seed: int = None,
         flowsheet_file: str = "flowsheet.yaml",
         init_file: str = "init.yaml"):
    MATS = materials.import_materials()
    FS = flowsheet.FlowSheet(MATS, flowsheet_file)
    FS.seed = seed
    time = ceil(time * 3600 / time_step)
    for h in range(time):
        FS.step(h)
        data = FS.output()
    pass


if __name__ == "__main__":
    time = 24
    time_step = 0.1
    seed = 4651207995
    main(time, time_step, seed)
