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


class BoidHunter(Boid):
    def __init__(self, update_ratio=1.0, sleep_time=0.0, **kwargs):
        super().__init__(update_ratio, sleep_time, **kwargs)

        self.n_hunter = kwargs['n_hunter']
        self.hunter_force = kwargs['hunter_force']
        self.hunter_n_closest = kwargs['hunter_n_closest']
        self.escape_force = kwargs['escape_force']

        self.hunter_xs = np.random.rand(self.n_hunter, 3) * 2 - 1
        self.hunter_vs = np.zeros((self.n_hunter, 3))

    def update_vs_w_hunter(self, dv_coh, dv_sep, dv_ali, dv_boundary):
        vs = self.update_vs(dv_coh, dv_sep, dv_ali, dv_boundary)

        for i in range(self.n_hunter):
            rel_x = self.hunter_xs[i] - self.xs
            vs += -1 * self.escape_force * (rel_x) / np.linalg.norm(rel_x, axis=1, keepdims=True)**2
        return vs

    def calc_hunter_vs(self):
        for i in range(self.n_hunter):
            rel_xs = self.xs - self.hunter_xs[i]
            rel_dists = np.linalg.norm(rel_xs, axis=1)
            mask_field = rel_dists.argsort()[:self.hunter_n_closest]
            rel_x_mean = rel_xs[mask_field].mean(axis=0)
            # Hunter velはcumulativeにしない（獲物に向かって素早い方向転換したいので）。
            self.hunter_vs[i] = self.hunter_force * rel_x_mean / np.linalg.norm(rel_x_mean)
        return self.hunter_vs

    def check_hunter_pos(self):
        if self.n_hunter == 1:
            return

        MIN_DIST = 0.15
        for i in range(self.n_hunter):
            rel_xs = np.delete(self.hunter_xs, i, axis=0) - self.hunter_xs[i]
            rel_dists = np.linalg.norm(rel_xs, axis=1)
            if (rel_dists < MIN_DIST).any():
                self.hunter_xs[i] = np.random.rand(1, 3) * 2 - 1  # reset pos


    def run(self):
        visualizer = SwarmVisualizer()
        t = 0
        while visualizer:
            dv_coh, dv_sep, dv_ali, dv_boundary = self.update_dvs()
            vs = self.update_vs_w_hunter(dv_coh, dv_sep, dv_ali, dv_boundary)
            xs = self.update_xs(vs)
            current_vs = self.calc_hunter_vs()
            self.hunter_xs += current_vs
            self.check_hunter_pos()
            visualizer.update(xs, vs)
            visualizer.set_markers(self.hunter_xs)
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
    boid = BoidHunter(args.update_ratio, args.sleep_time, **dic_pars)
    boid.run()
