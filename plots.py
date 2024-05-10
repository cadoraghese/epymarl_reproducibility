import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import json
import os

data = []
for alg in os.listdir("results/sacred"):
    alg_path = os.path.join("results", "sacred", alg)
    for env in os.listdir(alg_path):
        env_path = os.path.join(alg_path, env)
        env_data = {
            'alg': alg,
            'env': env,
            'return_mean_steps': [],
            'return_mean_values': [],
            'test_return_mean_steps': [],
            'test_return_mean_values': []
        }
        for run in [run for run in os.listdir(env_path) if run.isnumeric()]:
            run_path = os.path.join(env_path, run)
            metrics = json.load(open(os.path.join(run_path, "metrics.json"), "r"))
            try:
                if 'lbf' in env:
                    assert np.max(np.max(metrics["return_mean"]['steps'])) > 5e6
                elif 'bpush' in env:
                    assert np.max(np.max(metrics["return_mean"]['steps'])) > 9e6
                elif 'rware' in env:
                    assert np.max(np.max(metrics["return_mean"]['steps'])) > 9e6
                elif 'mpe' in env:
                    assert np.max(np.max(metrics["return_mean"]['steps'])) > 1e6
            except AssertionError:
                print(f"Skipping {alg} {env} {run}")
                continue
            env_data['return_mean_steps'].append(metrics["return_mean"]['steps'])
            env_data['return_mean_values'].append(metrics["return_mean"]['values'])
            env_data['test_return_mean_steps'].append(metrics["test_return_mean"]['steps'])
            env_data['test_return_mean_values'].append(metrics["test_return_mean"]['values'])
        data.append(env_data)

# for entry in data:
#     plt.figure()
#     plt.title(f"{entry['alg']} {entry['env']}")
#     steps = np.mean(entry['return_mean_steps'], axis=0)
#     means = np.mean(entry['return_mean_values'], axis=0)
#     stds = np.std(entry['return_mean_values'], axis=0)
#     plt.plot(steps, means, label=f"{entry['alg']} {entry['env']}")
#     plt.fill_between(steps, means - stds, means + stds, alpha=0.3)
#
#     steps = np.mean(entry['test_return_mean_steps'], axis=0)
#     means = np.mean(entry['test_return_mean_values'], axis=0)
#     stds = np.std(entry['test_return_mean_values'], axis=0)
#     plt.plot(steps, means, label=f"{entry['alg']} {entry['env']} test", linestyle="--")
#     plt.fill_between(steps, means - stds, means + stds, alpha=0.3)

for entry in data:
    entry['return_mean_steps'] = np.mean(entry['return_mean_steps'], axis=0)
    entry['return_mean_std'] = np.std(entry['return_mean_values'], axis=0)
    entry['return_mean_values'] = np.mean(entry['return_mean_values'], axis=0)
    entry['test_return_mean_steps'] = np.mean(entry['test_return_mean_steps'], axis=0)
    entry['test_return_mean_std'] = np.std(entry['test_return_mean_values'], axis=0)
    entry['test_return_mean_values'] = np.mean(entry['test_return_mean_values'], axis=0)


def plot_env(ax, data, env, alg):
    entry = next((x for x in data if env in x['env'] and x['alg'] == alg), None)
    if not entry:
        return
    # ax.plot(entry['return_mean_steps'], entry['return_mean_values'])
    # ax.fill_between(entry['return_mean_steps'], entry['return_mean_values'] - entry['return_mean_std'], entry['return_mean_values'] + entry['return_mean_std'], alpha=0.3)
    ax.plot(entry['test_return_mean_steps'], entry['test_return_mean_values'], linestyle="-")
    ax.fill_between(entry['test_return_mean_steps'], entry['test_return_mean_values'] - entry['test_return_mean_std'], entry['test_return_mean_values'] + entry['test_return_mean_std'], alpha=0.3)


def plot_single_graph(fig_x, gsxx, data, env):
    ax1 = fig_x.add_subplot(gsxx[0, 0])
    ax2 = fig_x.add_subplot(gsxx[0, 1])
    ax3 = fig_x.add_subplot(gsxx[0, 2])
    plot_env(ax1, data, env, 'iql')
    plot_env(ax2, data, env, 'vdn')
    plot_env(ax3, data, env, 'qmix')
    return ax1, ax2, ax3


F_SIZE = 15

# LBF
lbf_data = [entry for entry in data if 'lbf' in entry['env']]
lbf_fig = plt.figure(figsize=(20, 10))
lbf_fig.suptitle("LBF", fontsize=F_SIZE)
gs0 = gridspec.GridSpec(3, 2, figure=lbf_fig)
gs00 = gs0[0].subgridspec(1, 3)
gs01 = gs0[1].subgridspec(1, 3)
gs10 = gs0[2].subgridspec(1, 3)
gs11 = gs0[3].subgridspec(1, 3)
gs20 = gs0[4].subgridspec(1, 3)
gs21 = gs0[5].subgridspec(1, 3)

ax1, ax2, ax3 = plot_single_graph(lbf_fig, gs00, lbf_data, '4p-1f')
[ax.set_ylim(0, 1) for ax in [ax1, ax2, ax3]]
ax1.set_ylabel("4p-1f", fontsize=F_SIZE)
ax1, ax2, ax3 = plot_single_graph(lbf_fig, gs01, lbf_data, '4p-2f')
[ax.set_ylim(0, 1) for ax in [ax1, ax2, ax3]]
ax1.set_ylabel("4p-2f", fontsize=F_SIZE)
ax1, ax2, ax3 = plot_single_graph(lbf_fig, gs10, lbf_data, '4p-3f')
[ax.set_ylim(0, 1) for ax in [ax1, ax2, ax3]]
ax1.set_ylabel("4p-3f", fontsize=F_SIZE)
ax1, ax2, ax3 = plot_single_graph(lbf_fig, gs11, lbf_data, '4p-4f')
[ax.set_ylim(0, 1) for ax in [ax1, ax2, ax3]]
ax1.set_ylabel("4p-4f", fontsize=F_SIZE)
ax1, ax2, ax3 = plot_single_graph(lbf_fig, gs20, lbf_data, '3p-5f')
[ax.set_ylim(0, 1) for ax in [ax1, ax2, ax3]]
ax1.set_ylabel("3p-5f", fontsize=F_SIZE)
ax1.set_xlabel("IQL", fontsize=F_SIZE)
ax2.set_xlabel("VDN", fontsize=F_SIZE)
ax3.set_xlabel("QMIX", fontsize=F_SIZE)
ax1, ax2, ax3 = plot_single_graph(lbf_fig, gs21, lbf_data, '8p-1f')
[ax.set_ylim(0, 1) for ax in [ax1, ax2, ax3]]
ax1.set_ylabel("8p-1f", fontsize=F_SIZE)
ax1.set_xlabel("IQL", fontsize=F_SIZE)
ax2.set_xlabel("VDN", fontsize=F_SIZE)
ax3.set_xlabel("QMIX", fontsize=F_SIZE)

# BPUSH
bpush_data = [entry for entry in data if 'bpush' in entry['env']]
bpush_fig = plt.figure(figsize=(20, 5))
bpush_fig.suptitle("BPUSH", fontsize=F_SIZE)
gs0 = gridspec.GridSpec(2, 2, figure=bpush_fig)
gs00 = gs0[0].subgridspec(1, 3)
gs01 = gs0[1].subgridspec(1, 3)
gs10 = gs0[2].subgridspec(1, 3)
gs11 = gs0[3].subgridspec(1, 3)

ax1, ax2, ax3 = plot_single_graph(bpush_fig, gs00, bpush_data, 'small')
[ax.set_ylim(0, 3) for ax in [ax1, ax2, ax3]]
ax1.set_ylabel("Small", fontsize=F_SIZE)
ax1, ax2, ax3 = plot_single_graph(bpush_fig, gs01, bpush_data, 'medium')
[ax.set_ylim(0, 3) for ax in [ax1, ax2, ax3]]
ax1.set_ylabel("Medium", fontsize=F_SIZE)
ax1, ax2, ax3 = plot_single_graph(bpush_fig, gs10, bpush_data, 'large')
[ax.set_ylim(0, 3) for ax in [ax1, ax2, ax3]]
ax1.set_ylabel("Large", fontsize=F_SIZE)
ax1.set_xlabel("IQL", fontsize=F_SIZE)
ax2.set_xlabel("VDN", fontsize=F_SIZE)
ax3.set_xlabel("QMIX", fontsize=F_SIZE)
ax1, ax2, ax3 = plot_single_graph(bpush_fig, gs11, bpush_data, 'tiny')
[ax.set_ylim(0, 3) for ax in [ax1, ax2, ax3]]
ax1.set_ylabel("Tiny", fontsize=F_SIZE)
ax1.set_xlabel("IQL", fontsize=F_SIZE)
ax2.set_xlabel("VDN", fontsize=F_SIZE)
ax3.set_xlabel("QMIX", fontsize=F_SIZE)

# RWARE
rware_data = [entry for entry in data if 'rware' in entry['env']]
rware_fig = plt.figure(figsize=(20, 10))
rware_fig.suptitle("RWARE", fontsize=F_SIZE)
gs0 = gridspec.GridSpec(3, 2, figure=rware_fig)
gs00 = gs0[0].subgridspec(1, 3)
gs01 = gs0[1].subgridspec(1, 3)
gs10 = gs0[2].subgridspec(1, 3)
gs11 = gs0[3].subgridspec(1, 3)
gs20 = gs0[4].subgridspec(1, 3)
gs21 = gs0[5].subgridspec(1, 3)

ax1, ax2, ax3 = plot_single_graph(rware_fig, gs00, rware_data, 'tiny-2ag')
[ax.set_ylim(0, 4) for ax in [ax1, ax2, ax3]]
ax1.set_ylabel("Tiny-2ag", fontsize=F_SIZE)
ax1, ax2, ax3 = plot_single_graph(rware_fig, gs01, rware_data, 'tiny-4ag')
[ax.set_ylim(0, 10) for ax in [ax1, ax2, ax3]]
ax1.set_ylabel("Tiny-4ag", fontsize=F_SIZE)
ax1, ax2, ax3 = plot_single_graph(rware_fig, gs10, rware_data, 'small-2ag')
[ax.set_ylim(0, 2) for ax in [ax1, ax2, ax3]]
ax1.set_ylabel("Small-2ag", fontsize=F_SIZE)
ax1, ax2, ax3 = plot_single_graph(rware_fig, gs11, rware_data, 'small-4ag')
[ax.set_ylim(0, 5) for ax in [ax1, ax2, ax3]]
ax1.set_ylabel("Small-4ag", fontsize=F_SIZE)
ax1, ax2, ax3 = plot_single_graph(rware_fig, gs20, rware_data, 'medium-4ag')
[ax.set_ylim(0, 4) for ax in [ax1, ax2, ax3]]
ax1.set_ylabel("Medium-4ag", fontsize=F_SIZE)
ax1.set_xlabel("IQL", fontsize=F_SIZE)
ax2.set_xlabel("VDN", fontsize=F_SIZE)
ax3.set_xlabel("QMIX", fontsize=F_SIZE)
ax1, ax2, ax3 = plot_single_graph(rware_fig, gs21, rware_data, 'large-4ag')
[ax.set_ylim(0, 4) for ax in [ax1, ax2, ax3]]
ax1.set_ylabel("Large-4ag", fontsize=F_SIZE)
ax1.set_xlabel("IQL", fontsize=F_SIZE)
ax2.set_xlabel("VDN", fontsize=F_SIZE)
ax3.set_xlabel("QMIX", fontsize=F_SIZE)

# MPE
mpe_data = [entry for entry in data if 'mpe' in entry['env']]
mpe_fig = plt.figure(figsize=(10, 10))
mpe_fig.suptitle("MPE", fontsize=F_SIZE)
gs0 = gridspec.GridSpec(3, 1, figure=mpe_fig)
gs00 = gs0[0].subgridspec(1, 3)
gs10 = gs0[1].subgridspec(1, 3)
gs20 = gs0[2].subgridspec(1, 3)

ax1, ax2, ax3 = plot_single_graph(mpe_fig, gs00, mpe_data, 'Spread')
[ax.set_ylim(-700, -100) for ax in [ax1, ax2, ax3]]
ax1.set_ylabel("Spread", fontsize=F_SIZE)
ax1, ax2, ax3 = plot_single_graph(mpe_fig, gs10, mpe_data, 'Tag')
[ax.set_ylim(0, 50) for ax in [ax1, ax2, ax3]]
ax1.set_ylabel("Tag (predator-prey)", fontsize=F_SIZE)
ax1, ax2, ax3 = plot_single_graph(mpe_fig, gs20, mpe_data, 'Adversary')
[ax.set_ylim(0, 20) for ax in [ax1, ax2, ax3]]
ax1.set_ylabel("Adversary", fontsize=F_SIZE)
ax1.set_xlabel("IQL", fontsize=F_SIZE)
ax2.set_xlabel("VDN", fontsize=F_SIZE)
ax3.set_xlabel("QMIX", fontsize=F_SIZE)


plt.show()
