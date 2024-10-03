import numpy as np
import matplotlib.pyplot as plt
from numpy import exp, log, sqrt


def mean_q(x, L, vm, a, b):
    lam2 = a * log(x) + b
    lam = lam2 * x * L
    u = lam * vm
    mean_qk = 1 / lam2 / L - x * vm * exp(-u) / (1 - exp(-u))
    return mean_qk


def var_q(x, L, vm, a, b):
    lam2 = a * log(x) + b
    lam = lam2 * x * L
    u = lam * vm
    var_qk = 1 / (lam2 ** 2) / (L ** 2) - (x * vm) ** 2 / (exp(u) + exp(-u) - 2)
    return var_qk


# plot the mean and variance
# calculate the mean and variance of the fitted function
# L1, vm1, a1, b1 = 0.1, 35.90562010983311, 0.08357838144495106, -0.34800000016415733
L1, vm1, a1, b1 = 0.1, 36.44563222392642, 0.07836849626568203, -0.3260000000069208
# changing a min=0.068, max=0.079, num=10
# changing b min=-0.373, max=-0.326, num=10
# Transfer to unit m/s : a=3.6*a1; b=3.6*b1+3*log(10)*a
# list_a = [0.262 / 3.6, 0.272 / 3.6, 0.282 / 3.6, 0.292 / 3.6]  # -0.5413503937851569,
list_c = ['blue', 'lime', 'red', 'black', 'navy']
list_b = [-0.33162817, -0.32885039, -0.32607262, -0.32329484]
# norm = plt.Normalize(vmin=min(list_b), vmax=max(list_b))
continuous_k = np.arange(0.1, 94, 0.1)
plt.rcParams['font.size'] = '35'
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams['mathtext.fontset'] = 'cm'  # cm for Cambria Math
plt.rcParams['mathtext.rm'] = 'Cambria Math'  # Set the font
plt.rcParams['mathtext.it'] = 'Cambria Math:italic'  # Set italic font
plt.rcParams['mathtext.cal'] = 'Cambria Math'  # Set calligraphy font
fig, ax = plt.subplots(1, 2, sharex=True)
# for i, ai in enumerate(list_a):
for i, bi in enumerate(list_b):
    # ax[0].plot(continuous_k, mean_q(continuous_k, L1, vm1, ai, b1), c=list_c[i],
    #            label=r'$\alpha$=' + str(round(3.6 * ai, 3)),
    #            lw=2)
    ax[0].plot(continuous_k, mean_q(continuous_k, L1, vm1, a1, bi), c=list_c[i],
               label=r'$\beta$=' + str(round(3.6 * bi + 3 * log(10) * 3.6 * a1, 3)),
               lw=2)
    ax[0].set_xlabel('$k$')
    ax[0].set_ylabel('E[$Q$]')
    ax[0].set_xlim(0, 100)
    # ax[0].set_yticks(range(0, 2001,  500))

    # ax[1].plot(continuous_k, var_q(continuous_k, L1, vm1, ai, b1), c=list_c[i],
    #            label=r'$\alpha$=' + str(round(3.6 * ai, 3)),
    #            lw=2)
    ax[1].plot(continuous_k, var_q(continuous_k, L1, vm1, a1, bi), c=list_c[i],
               label=r'$\beta$=' + str(round(3.6 * bi + 3 * log(10) * 3.6 * a1, 3)),
               lw=2)
    ax[1].set_xlabel('$k$')
    ax[1].set_ylabel('Var[$Q$]')
    # ax[1].set_yticks(range(0, 800001, 200000))
ax[0].legend(fontsize=20)
ax[1].legend(fontsize=20)
plt.show()
