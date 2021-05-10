""" Tennesse Eastman Process (TEP) Simulation

Main file used to start the TEP simulation program

Takes the following arguments:
TODO: add these arguments
"""
__author__ = "Hussein Saafan"

import argparse

from controllers import Controller


parser = argparse.ArgumentParser()
cli_group = parser.add_argument_group()

# Parser arguments
parser.add_argument('-g', '--gui',
                    help='run the program with a gui',
                    action='store_true'
                    )

cli_group.add_argument('-p', '--path',
                       help='change the default settings directory',
                       type=str,
                       default='./settings'
                       )
cli_group.add_argument('-t', '--time',
                       help='the time to simulate in hours',
                       type=float,
                       default=24)
cli_group.add_argument('-dt', '--step',
                       help='the time step to use when simulating in hours',
                       type=float,
                       default=0.1)
cli_group.add_argument('-s', '--seed',
                       help='the seed to use for the simulation',
                       type=int,
                       default=None)

args = parser.parse_args()


controller = Controller(use_gui=args.gui,
                        seed=args.seed,
                        time=args.time,
                        time_step=args.step,
                        path=args.path)
