import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize, brute, basinhopping
from scipy.special import erf
from numpy import sqrt, pi, exp, log
from scipy.optimize import Bounds


# Be careful with the unit

# define the log-likelihood function
def loglikelihood(x):
    ll1, ll2, ll3 = x[0], x[1], x[2]
    l1, l2, l3 = ll1 / v1, ll2 / v2, ll3 / v3
    va = 0  # test the necessary of va
    H = l1 * (vs - vl) ** 2 + l2 * vs + l3 * (vs - va) ** 2
    A = (-2 * l1 * vl + l2 - 2 * l3 * va) / (2 * (l1 + l3))
    B = -A ** 2 + (l1 * vl ** 2 + l3 * va ** 2) / (l1 + l3)
    Z = (sqrt(pi) / 2) * exp(-(l1 + l3) * B) / sqrt(l1 + l3) * (erf(sqrt(l1 + l3) * (vm + A)) - erf(sqrt(l1 + l3) * A))
    logZ = log(Z)
    min_obj = np.sum(H) + np.sum(logZ)
    return min_obj


# read the random data from the text file
# [frame, subject speed, leader speed, speed difference, average speed in lane, spacing, subject class, relative class]
LaneID = 234
data = np.loadtxt("../data/homo_data_lane" + str(LaneID) + ".txt")
# train_data = data[:int(data.shape[0] * 2 / 3)]
train_data = data
vm = 120 / 3.6  # max speed (m/s)
result = []
# calculate the normalized parameters
v1, v2, v3 = 400 / 3.6 / 3.6, 50 / 3.6, 2500 / 3.6 / 3.6  # 600 / 3.6 / 3.6
# # plot the normalized data
# fig, ax = plt.subplots(1, 3, sharex='col')
# ax[0].scatter(range(train_data.shape[0]), (3.6 * train_data[:, 1] - 3.6 * train_data[:, 2]) ** 2)
# ax[1].scatter(range(train_data.shape[0]), 3.6 * train_data[:, 1])
# ax[2].scatter(range(train_data.shape[0]), (3.6 * train_data[:, 1] - 3.6 * train_data[:, 4]) ** 2)
# plt.show()
# print(v1, v2, v3)

# iterate similar spacing (units:m)
for i in np.arange(0, max(train_data[:, 5]), 0.5):
    spacing_ind = (train_data[:, 5] >= i) & (train_data[:, 5] <= i + 0.5)
    if train_data[spacing_ind].shape[0] < 100:
        continue

    vs, vl, va = train_data[spacing_ind, 1], train_data[spacing_ind, 2], 0  # train_data[spacing_ind, 4]
    # minimize the objective function
    x0 = np.array([1, 1, 1])
    bnds = Bounds([0, -np.inf, 0], [np.inf, np.inf, np.inf])
    res = minimize(loglikelihood, x0, options={'disp': True}, bounds=bnds, method='Nelder-Mead', tol=1e-6)
    # # try the global optimization
    # bounds = [(0, 10), (-10, 10), (0, 10), (0, 200 / 3.6)]
    # res = optimize.brute(loglikelihood, bounds, full_output=True, finish=optimize.fmin)
    result.append([i, len(vs), res.x[0] / v1, res.x[1] / v2, res.x[2] / v3, res.fun])
np.savetxt('lamda_all' + str(LaneID) + '_m_test.txt', np.array(result))
