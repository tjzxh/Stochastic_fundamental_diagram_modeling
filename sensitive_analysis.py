import numpy as np
import matplotlib.pyplot as plt
from numpy import sqrt, pi, exp, log
from SALib.sample import latin
from SALib.analyze import pawn, rbd_fast, hdmr


def mean_q(x, l, vm, c, b):
    lam2 = c * log(x) + b
    lam = lam2 * x * l
    u = lam * vm
    mean_qk = 1 / lam2 / l - x * vm * exp(-u) / (1 - exp(-u))
    return mean_qk


def var_q(x, l, vm, c, b):
    lam2 = c * log(x) + b
    lam = lam2 * x * l
    u = lam * vm
    var_qk = 1 / (lam2 ** 2) / (l ** 2) - (x * vm) ** 2 / (exp(u) + exp(-u) - 2)
    return var_qk


# sensitive analysis for mean_q
problem = {
    'num_vars': 4,
    'names': ['L', 'v_m', '\alpha', '\beta'],
    'bounds': [[0.05, 0.15], [30, 120], [0, 1], [-1, 0]]
}

# sample
param_values = latin.sample(problem, 2000)

# evaluate the function
x = np.linspace(1, 100, 1000)
y = np.array([mean_q(x, *params) for params in param_values])

# analyse
pawn_indices = [pawn.analyze(problem, param_values, Y) for Y in y.T]
STs = np.array([s['median'] for s in pawn_indices])
S_min = np.array([s['minimum'] for s in pawn_indices])
S_max = np.array([s['maximum'] for s in pawn_indices])
# plot all the index in one figure
continuous_k = np.arange(0.1, 94, 0.1)
plt.rcParams['font.size'] = '30'
plt.rcParams["font.family"] = "Times New Roman"
fig, ax = plt.subplots()
color_list = ['blue', 'black', 'red', 'green']
for i in range(4):
    ax.plot(x, STs[:, i], label=r'$_\mathregular{{{}}}$'.format(problem["names"][i]), color=color_list[i])
    ax.fill_between(x, S_min[:, i], S_max[:, i], color=color_list[i], alpha=0.1)
# plot subplots
# fig = plt.figure(constrained_layout=True)
# gs = fig.add_gridspec(2, 2)
#
# ax1 = fig.add_subplot(gs[0, 0])
# ax2 = fig.add_subplot(gs[0, 1])
# ax3 = fig.add_subplot(gs[1, 0])
# ax4 = fig.add_subplot(gs[1, 1])
# for i, ax in enumerate([ax1, ax2, ax3, ax4]):
#     ax.plot(x, STs[:, i],
#             label=r'S$_\mathregular{{{}}}$'.format(problem["names"][i]),
#             color='black')
#     ax.set_xlabel("x")
#     ax.set_ylabel("PAWN index")
#
#     ax.set_xlim(0, 100)
#     ax.set_ylim(0, 1)
#     ax.yaxis.set_label_position("right")
#     ax.yaxis.tick_right()
#
#     ax.legend(loc='upper right')
ax.set_xlabel("density (veh/km)")
ax.set_ylabel("PAWN index")

ax.set_xlim(0, 100)
ax.set_ylim(0, 1)
ax.yaxis.set_label_position("right")
ax.yaxis.tick_right()

ax.legend(loc='upper right')
plt.show()
