#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import numpy as np
sys.path.append(os.pardir)
import argparse
from run_boid import Boid
from alifebook_lib.visualizers import SwarmVisualizer
import time


class BoidPrey(Boid):
    def __init__(self, update_ratio=1.0, sleep_time=0.0, **kwargs):
        super().__init__(update_ratio, sleep_time, **kwargs)

        self.prey_force = kwargs['prey_force']
        self.prey_movement_step = kwargs['prey_movement_step']
        self.prey_x = np.random.rand(1, 3) * 2 - 1

    def update_vs_prey(self, dv_coh, dv_sep, dv_ali, dv_boundary):
        rel_x = self.prey_x - self.xs
        vs = self.update_vs(dv_coh, dv_sep, dv_ali, dv_boundary)
        vs += self.prey_force * (rel_x) / np.linalg.norm(rel_x, axis=1, keepdims=True)**2
        return vs

    def run(self):
        visualizer = SwarmVisualizer()
        t = 0
        while visualizer:
            dv_coh, dv_sep, dv_ali, dv_boundary = self.update_dvs()
            vs = self.update_vs_prey(dv_coh, dv_sep, dv_ali, dv_boundary)
            xs = self.update_xs(vs)
            if t % self.prey_movement_step == 0:
                self.prey_x = np.random.rand(1, 3) * 2 - 1  # reset the prey position
                visualizer.set_markers(self.prey_x) # エサの位置を表示する（Appendix参照）
            visualizer.update(xs, vs)
            if t == 0:
                time.sleep(self.sleep_time)
            t += 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='boid program of ALife book')
    parser.add_argument('--conf', type=str, help='config file')
    parser.add_argument('--sleep_time', type=float, default=0.0, help='sleep time before start; helpful for recording video')
    parser.add_argument('--update_ratio', type=float, default=1.0, help='update agent ratio (0 ~ 1)')
    args = parser.parse_args()

    # print(args.conf, args.asynch)
    dic_pars = eval(open(args.conf).read())
    boid = BoidPrey(args.update_ratio, args.sleep_time, **dic_pars)
    boid.run()
