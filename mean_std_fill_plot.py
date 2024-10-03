import numpy as np
import matplotlib.pyplot as plt
from numpy import exp, log, sqrt
from sklearn.metrics import r2_score

# read the FD data from the text file [frame, flow, density, avg_speed_in_lane]
LaneID = 234
# data = np.loadtxt("./fd_instant_lane" + str(LaneID) + ".txt")
data = np.loadtxt("./fd_data_10_frame.txt")
flow, density, speed = 3600 * data[:, 1], 1000 * data[:, 2], 3.6 * data[:, 3]
# filter the valid data with density<85
valid_index = np.where(density < 85)
flow, density, speed = flow[valid_index], density[valid_index], speed[valid_index]
# calculate the mean and variance of flow relation to density
mean, var, sample_num = [], [], []
density_list = np.unique(density)
density_list.sort()
for i in density_list:
    valid_index = np.where(density == i)
    flowi, speedi = flow[valid_index], speed[valid_index]
    mean.append(np.average(flowi))
    var.append(np.var(flowi))
    sample_num.append(len(flowi))
mean, var, sample_weights = np.array(mean), np.array(var), np.array(sample_num) / np.sum(sample_num)


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


# the version for 5% probe vehicles
# L1, vm1, a1, b1 = 0.1, 36.36, 0.069, -0.335
# a2, b2 = 0.085, -0.403
# the version for 10% probe vehicles
# L1, vm1, a1, b1 = 0.1, 32.91444, 0.076, -0.330
# for 0.1 s instant FD data
# L1, vm1, a1, b1 = 0.1, 36.44563222392642, 0.07836849626568203, -0.3260000000069208
# for aggregated FD data: 10 frames, unit: km/h
# empirical 85th maximum speed: 38.387268000000006 km/h
# calibrated maximum speed: 36.59380161871782 km/h
L1, vm1, a1, b1 = 0.1, 36.34403663566313, 0.07818025386594805, -0.3260000005429407
# Transfer to unit m/s : a=3.6*a1; b=3.6*b1+3*log(10)*a
# a = 0.2826415507742512, b = 0.778818664059387
# calculate the R-squared of the fitted mean and variance
continuous_k = np.arange(0.1, 85, 0.1)
y1 = mean_q(continuous_k, L1, vm1, a1, b1) - np.sqrt(var_q(continuous_k, L1, vm1, a1, b1))
y2 = mean_q(continuous_k, L1, vm1, a1, b1) + np.sqrt(var_q(continuous_k, L1, vm1, a1, b1))
# calculate the R-squared of the stacked fitted mean and variance
mean_R = r2_score(mean, mean_q(density_list, L1, vm1, a1, b1), sample_weight=sample_weights)
var_R = r2_score(var, var_q(density_list, L1, vm1, a1, b1), sample_weight=sample_weights)
mean_var_R = r2_score(np.hstack((mean, var)),
                      np.hstack((mean_q(density_list, L1, vm1, a1, b1), var_q(density_list, L1, vm1, a1, b1))),
                      sample_weight=np.hstack((sample_weights, sample_weights)))

# mean R-squared:  0.8067820283207261
# var R-squared:  -102.77171982740057
# mean and var R-squared:  -62.6994477602667
print('mean R-squared: ', mean_R)
print('var R-squared: ', var_R)
print('mean and var R-squared: ', mean_var_R)
# plot the best fitted function
plt.rcParams['font.size'] = '30'
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams['mathtext.fontset'] = 'cm'  # cm for Cambria Math
plt.rcParams['mathtext.rm'] = 'Cambria Math'  # Set the font
plt.rcParams['mathtext.it'] = 'Cambria Math:italic'  # Set italic font
plt.rcParams['mathtext.cal'] = 'Cambria Math'  # Set calligraphy font
fig = plt.figure()
ax0 = fig.add_subplot(111)
# spec = fig.add_gridspec(2, 2)
# ax0 = fig.add_subplot(spec[:, 0])
# ax1 = fig.add_subplot(spec[0, 1])
# ax2 = fig.add_subplot(spec[1, 1])
# ax0.errorbar(density_list, mean, yerr=np.sqrt(var), fmt='o', label='I-80 data', color='black')
ax0.fill_between(continuous_k, y1, y2, alpha=.1, linewidth=0, color='red', label='Estimated std')
ax0.plot(continuous_k, (y1 + y2) / 2, linewidth=2, color='red', label='Estimated mean')
ax0.scatter(density, flow, c='b', label='I-80 data', s=30)
# ax0.plot(density_list, mean, linewidth=2, color='black', label='Empirical mean')
# # for probe vehicle data
# ax0.fill_between(continuous_k, y1, y2, alpha=.1, linewidth=0, color='red', label='Fitted std with 5% probe vehicles')
# ax0.plot(continuous_k, (y1 + y2) / 2, linewidth=2, color='red', label='Fitted mean with 5% probe vehicles')
ax0.set_xlabel("$k$ (veh/km/lane)")
ax0.set_ylabel("$Q$ (veh/h/lane)")
ax0.set_xticks(np.arange(0, 91, 10))
ax0.legend(loc="upper left", fontsize=20)
ax0.set_aspect(1 / 30)
# # plot the fitted mean and variance in ax1, ax2
# ax1.scatter(density_list, mean, c='b')
# ax1.plot(continuous_k, (y1 + y2) / 2, linewidth=2, color='red', label='Fitted mean')
# ax1.set_xlabel(r"k (veh/km)")
# ax1.set_ylabel(r"E[q] (veh/h)")
# ax1.set_xticks(np.arange(0, 101, 20))
# ax1.set_aspect(1 / 20)
# ax2.scatter(density_list, var, c='b')
# ax2.plot(continuous_k, var_q(continuous_k, L1, vm1, a1, b1), linewidth=2, color='red', label='Fitted std')
# ax2.set_xlabel(r"k (veh/km)")
# ax2.set_ylabel(r"Var[q] ($veh^2$/$h^2$)")
# ax2.set_xticks(np.arange(0, 101, 20))
# ax2.set_aspect(1 / 5000)
plt.show()
