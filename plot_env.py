import os
import numpy as np
import argparse
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.gridspec as gridspec
import seaborn as sns
import itertools
from scipy.io import loadmat


def moving_average(data, window=4):
    return np.convolve(data, np.ones(int(window)) / float(window), 'same')


def shaded_plot(ax, data, x_scale=1., **kwargs):
    x = np.arange(data.shape[1]) * x_scale
    mu = np.mean(data, axis=0)
    std = np.std(data, axis=0)
    ci = 1.96 * std / np.sqrt(data.shape[0])
    #    ax.fill_between(x, mu - ci, mu + ci, alpha=0.2, edgecolor="none", linewidth=0, **kwargs)
    ax.plot(x, mu, linewidth=2, **kwargs)
    ax.margins(x=0)


def add_line(name, version, ax, lc='b', ls='-', moving=1):
    data_all = []
    for i in range(1, args.n + 1):
        f = args.folder + args.env + version + '/' + name + '_' + str(i)
        try:
            data_file = loadmat(f)[args.var].flatten()
        except:
            print('Cannot read    [', f, ']')
            continue
        if args.var == 'VC_history':
            data_file = data_file[:100000]
        if args.var == 'J_history':
            data_file = data_file[:2000]
        data_all.append(data_file)
    data_all = np.array(data_all)
    if data_all.shape[0] == 0:
        print('No data    [', name, ']')
        return
    if moving > 1:
        for i in range(data_all.shape[0]):
            data_all[i, :] = moving_average(data_all[i, :], args.moving)
    x_scale = 1.
    if args.var == 'J_history':
        x_scale = 50.
    shaded_plot(ax, data_all, x_scale=x_scale, color=lc, linestyle=ls)
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
    plt.xlabel('Steps')
    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(6)
        tick.set_pad(-3)
    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(6)
        tick.set_pad(-3)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--env', default='Taxi')
    parser.add_argument('--folder', default='ql/ql/res/')
    parser.add_argument('--moving', type=int, default=1)
    parser.add_argument('--n', type=int, default=20)
    parser.add_argument('--var', default='VC_history')
    args = parser.parse_args()

    sns.set_context("paper")
    sns.set_style('darkgrid', {'legend.frameon': True})

    fig = plt.figure()
    gs = gridspec.GridSpec(1, 4)
    gs.update(wspace=0.09, hspace=0.05)

    alg_name = ['vv_ucb', 'vv_n', 'brlsvi', 'boot', 'boot_thom', 'ucb1', 'bonus', 'egreedy', 'random']
    legend = ['Ours (UCB Reward)', 'Ours (Count Reward)', 'Rand. Prior (Osband 2019)', 'Bootstr. (Osband 2016a)',
              'Thompson (D\'Eramo 2019)', 'UCB1 (Auer 2002)', 'Expl. Bonus (Strehl 2008)', r'$\epsilon$' + '-greedy',
              'Random']

    i = 0
    if args.env == 'DeepSea50':
        t = ["Zero Init.", "Optimistic Init."]
        for opt in ["", "_OPT"]:
            i += 1
            if i == 1:
                ax = fig.add_subplot(1, 2, i, title=t[i - 1])
            else:
                ax = fig.add_subplot(1, 2, i, title=t[i - 1], yticklabels=[])
            palette = itertools.cycle(sns.color_palette())
            lines = itertools.cycle(["-", "--", ":"])
            plt.tick_params(labelsize=3)
            for alg in alg_name:
                add_line(alg, opt, ax, moving=args.moving, lc=next(palette))
            if i == 1:
                if args.var == 'J_history':
                    plt.ylabel('Discounted Return')
                else:
                    plt.ylabel('States Discovered')

    else:
        t = ["Zero Init. & Short Hor.", "Zero Init. & Long Hor.", "Optimistic Init. & Short Hor.",
             "Optimistic init. & Long Hor."]
        for opt in ["", "_OPT"]:
            for hor in ["", "_LONG"]:
                i += 1
                if i == 1:
                    ax = plt.subplot(gs[i - 1], title=t[i - 1])
                else:
                    ax = plt.subplot(gs[i - 1], title=t[i - 1], yticklabels=[])
                if args.var == 'J_history' and args.env == 'GridworldSparseWall':
                    ax.set_yscale('log')
                palette = itertools.cycle(sns.color_palette())
                lines = itertools.cycle(["-", "--", ":"])
                plt.tick_params(labelsize=3)
                for alg in alg_name:
                    add_line(alg, opt + hor, ax, moving=args.moving, lc=next(palette))
                if i == 1:
                    if args.var == 'J_history':
                        plt.ylabel('Discounted Return')
                    else:
                        plt.ylabel('States Discovered')

    env_dict = {"DeepSea50": "Deep Sea", "Taxi": "Taxi", "DeepGridworld": "Deep Gridworld",
                "GridworldSparseWall": "Gridworld (Wall)", "GridworldSparseSmall": "Gridworld (Prison)",
                "GridworldSparseSimple": "Gridworld (Toy)"}

    plt.suptitle(env_dict[args.env], y=0.83, x=0.98, fontsize='x-large')

    leg = plt.legend(handles=ax.lines, labels=legend, bbox_to_anchor=(1.04, 0.8), loc='upper left')
    frame = leg.get_frame()
    frame.set_facecolor('white')

    picsize = fig.get_size_inches() / 1.3
    picsize[0] *= 3
    picsize[1] *= 0.9
    fig.set_size_inches(picsize)

    plt.savefig(args.env + '_' + args.var + ".pdf", bbox_inches='tight', pad_inches=0)
