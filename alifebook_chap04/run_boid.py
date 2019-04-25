#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.pardir)
import argparse
import numpy as np
from alifebook_lib.visualizers import SwarmVisualizer
import time


class Boid:
    def __init__(self, update_ratio=1.0, sleep_time=0.0, **kwargs):
        self.sleep_time = sleep_time
        self.update_ratio = update_ratio
        # シミュレーションパラメータ
        self.n_agent = kwargs['n_agent']
        # 速度の上限/下限
        self.min_vel = kwargs['min_vel']
        self.max_vel = kwargs['max_vel']
        # 境界で働く力（0にすると自由境界）
        self.boundary_force = kwargs['boundary_force']

        self.par_dynamics = {}
        # 力の強さ、働く距離, 働く角度をそれぞれ設定
        force_kinds = ['cohesion', 'separation', 'alignment']
        par_kinds = ['force', 'distance', 'angle']
        for k in force_kinds:
            for p in par_kinds:
                key = '%s_%s' % (k, p)
                self.par_dynamics[key] = kwargs[key]
        self.init_values()

    def init_values(self):
        # 位置と速度
        self.xs = np.random.rand(self.n_agent, 3) * 2 - 1
        self.vs = (np.random.rand(self.n_agent, 3) * 2 - 1) * self.min_vel
        # cohesion, separation, alignmentの３つの力を代入する変数
        self.dv_coh = np.zeros((self.n_agent, 3))
        self.dv_sep = np.zeros((self.n_agent, 3))
        self.dv_ali = np.zeros((self.n_agent, 3))
        # 境界で働く力を代入する変数
        self.dv_boundary = np.zeros((self.n_agent, 3))

    def _mask(self, distance, angle, kind):
        mask_dist = (distance < self.par_dynamics[kind + '_distance'])
        mask_angle = (angle < self.par_dynamics[kind + '_angle'])
        return mask_dist & mask_angle

    def update_dv_coh(self, x_this, x_that, distance, angle, n_th):
        coh_agents_x = x_that[self._mask(distance, angle, 'cohesion')]

        self.dv_coh[n_th] = 0.0
        if len(coh_agents_x) > 0:
            x_avg = np.average(coh_agents_x, axis=0)
            self.dv_coh[n_th] =\
                self.par_dynamics['cohesion_force'] * (x_avg - x_this)

    def update_dv_sep(self, x_this, x_that, distance, angle, n_th):
        sep_agents_x = x_that[self._mask(distance, angle, 'separation')]

        self.dv_sep[n_th] = 0.0
        if len(sep_agents_x) > 0:
            x_sum = np.sum(x_this - sep_agents_x, axis=0)
            self.dv_sep[n_th] =\
                self.par_dynamics['separation_force'] * x_sum

    def update_dv_ali(self, v_this, v_that, distance, angle, n_th):
        ali_agents_v = v_that[self._mask(distance, angle, 'alignment')]

        self.dv_ali[n_th] = 0.0
        if len(ali_agents_v) > 0:
            v_avg = np.average(ali_agents_v, axis=0)
            self.dv_ali[n_th] =\
                self.par_dynamics['alignment_force'] * (v_avg - v_this)

    def calc_dv_boundary(self, x):
        dist_center = np.linalg.norm(x)  # 原点からの距離
        if dist_center <= 1:
            return 0.0
        rel_dist_bou = (dist_center - 1) / dist_center
        return -1 * self.boundary_force * x * rel_dist_bou

    def update_dv_bou(self, x_this, n_th):
        self.dv_boundary[n_th] = self.calc_dv_boundary(x_this)

    @staticmethod
    def calc_dist_angle(x_this, x_that, v_this):
        # 個体間の距離と角度
        rel_vec = x_that - x_this
        distance = np.linalg.norm(rel_vec, axis=1)
        norm = np.linalg.norm(v_this) * np.linalg.norm(rel_vec, axis=1)
        angle = np.arccos(np.dot(v_this, rel_vec.T) / norm)
        return distance, angle

    def update_dvs(self):
        """加速度のアップデート"""
        update_agents = np.random.choice(self.n_agent,
            int(self.update_ratio * self.n_agent), replace=False)
        for i in update_agents:
            # ここで計算する個体の位置と速度
            x_this = self.xs[i]
            v_this = self.vs[i]
            # それ以外の個体の位置と速度の配列
            x_that = np.delete(self.xs, i, axis=0)
            v_that = np.delete(self.vs, i, axis=0)
            distance, angle = self.calc_dist_angle(x_this, x_that, v_this)

            self.update_dv_coh(x_this, x_that, distance, angle, i)
            self.update_dv_sep(x_this, x_that, distance, angle, i)
            self.update_dv_ali(v_this, v_that, distance, angle, i)
            self.update_dv_bou(x_this, i)
        return self.dv_coh, self.dv_sep, self.dv_ali, self.dv_boundary

    def update_vs(self, dv_coh, dv_sep, dv_ali, dv_boundary):
        """速度のアップデートと上限/下限のチェック"""
        self.vs += dv_coh + dv_sep + dv_ali + dv_boundary
        # 上限・下限を設定
        v_abs = np.linalg.norm(self.vs, axis=1)
        norm_vs = self.vs / v_abs.reshape(-1, 1)
        mask_min = v_abs < self.min_vel
        mask_max = v_abs > self.max_vel
        self.vs[mask_min] = self.min_vel * norm_vs[mask_min]
        self.vs[mask_max] = self.max_vel * norm_vs[mask_max]
        return self.vs

    def update_xs(self, vs):
        self.xs += vs
        return self.xs

    def run(self):
        # visualizerの初期化 (Appendix参照)
        visualizer = SwarmVisualizer()
        t = 0
        while visualizer:
            dv_coh, dv_sep, dv_ali, dv_boundary = self.update_dvs()
            vs = self.update_vs(dv_coh, dv_sep, dv_ali, dv_boundary)
            xs = self.update_xs(vs)
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
    boid = Boid(args.update_ratio, args.sleep_time, **dic_pars)
    boid.run()
