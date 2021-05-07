""" Main Module """
__author__ = "Hussein Saafan"

from mvc import Model, View, Controller


def main(time: float, time_step: float, seed: int = None):
    view = View()
    model = Model()
    controller = Controller()
    controller.connect_model(model)
    controller.connect_view(view)
    model.set_seed(seed)
    model.set_time(time, time_step)
    pass


if __name__ == "__main__":
    time = 24
    time_step = 0.1
    seed = 4651207995
    main(time, time_step, seed)
