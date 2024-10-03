import numpy as np
from scipy.optimize import curve_fit
from numpy import sqrt, pi, exp, log
from lmfit import Model
import matplotlib.pyplot as plt

# read the FD data from the text file [frame, flow, density, avg_speed_in_lane]
LaneID = 234
# data = np.loadtxt("./fd_instant_lane" + str(LaneID) + ".txt")
data = np.loadtxt("./fd_data_10_frame.txt")
flow, density, speed = 3600 * data[:, 1], 1000 * data[:, 2], 3.6 * data[:, 3]
# filter the valid data with density<80
valid_index = np.where(density < 85)
flow, density, speed = flow[valid_index], density[valid_index], speed[valid_index]
# instant FD : calculate the mean and variance of flow relation to density
mean, var, sample_num = [], [], []
density_list = np.unique(density)
density_list.sort()
for i in density_list:
    valid_index = np.where(density == i)
    flowi, speedi = flow[valid_index], speed[valid_index]
    mean.append(np.average(flowi))
    var.append(np.var(flowi))
    sample_num.append(len(flowi))
    # print(f"density {i} num {len(flowi)}")
# plot the mean and variance
mean, var, sample_weights = np.array(mean), np.array(var), np.array(sample_num) / np.sum(sample_num)
max_mean, max_var, max_density = np.max(mean), np.max(var), np.max(density)


def mean_q(x, vm, a, b):
    L = 0.1
    lam2 = a * log(x) + b
    lam = lam2 * x * L
    u = lam * vm
    # mean_vk = 1 / lam - u * exp(-u) / lam / (1 - exp(-u))
    mean_qk = 1 / lam2 / L - x * vm * exp(-u) / (1 - exp(-u))
    return mean_qk


def var_q(x, L, vm, a, b):
    lam2 = a * log(x) + b
    lam = lam2 * x * L
    u = lam * vm
    # var_vk = 1 / (lam ** 2) - (u ** 2) * exp(-u) / (lam ** 2) / (1 - exp(-u)) ** 2
    # var_qk = 1 / (lam2 ** 2) / (L ** 2) - (x * vm) ** 2 * exp(-u) / (1 - exp(-u)) ** 2
    var_qk = 1 / (lam2 ** 2) / (L ** 2) - (x * vm) ** 2 / (exp(u) + exp(-u) - 2)
    return var_qk


def func(x, L, vm, a, b):
    # stack the function mean_q and var_q
    mean_qi = mean_q(x, L, vm, a, b) / max_mean
    var_qi = var_q(x, L, vm, a, b) / max_var
    return np.hstack((mean_qi, var_qi))


# # curve fitting with stacked labels
# y_data = np.hstack((mean / max_mean, var / max_var))
# # try lmfit for fitting mean and var together
# mymodel = Model(func)
# mymodel.set_param_hint('L', value=0.1, min=0, max=1)
# mymodel.set_param_hint('vm', value=40, min=0, max=100)
# mymodel.set_param_hint('a', value=0.0826, min=0.072, max=0.093)
# mymodel.set_param_hint('b', value=-0.3853, min=-0.423, max=-0.348)
# weights = np.hstack((sample_weights, sample_weights * 0.05))
# result = mymodel.fit(y_data, x=density_list, weights=weights)
# print(result.fit_report())
# print(result.best_values)
# L_fit, vm_fit, a_fit, b_fit = result.best_values['L'], result.best_values['vm'], result.best_values[
#     'a'], result.best_values['b']

# curve fitting with mean
mean_model = Model(mean_q)
# mean_model.set_param_hint('L', value=0.1, min=0, max=1)
mean_model.set_param_hint('vm', value=40, min=10, max=100)
# lane 2
# mean_model.set_param_hint('a', value=0.10398907, min=0.098, max=0.133)
# mean_model.set_param_hint('b', value=-0.453818742321764, min=-0.565, max=-0.435)
# lane 3
# mean_model.set_param_hint('a', value=0.0674, min=0.054, max=0.081)
# mean_model.set_param_hint('b', value=-0.3198, min=-0.372, max=-0.268)
# lane 4
# mean_model.set_param_hint('a', value=0.1125, min=0.093, max=0.132)
# mean_model.set_param_hint('b', value=-0.5208, min=-0.593, max=-0.448)
# lane 5
# mean_model.set_param_hint('a', value=0.2, min=0.0, max=0.5)
# mean_model.set_param_hint('b', value=-0.2, min=-0.5, max=-0.0)
# lane2,3,4
mean_model.set_param_hint('a', value=0.0733, min=0.068, max=0.079)
mean_model.set_param_hint('b', value=-0.3496, min=-0.373, max=-0.326)
mean_result = mean_model.fit(mean, x=density_list, weights=sample_weights)

# curve fitting with var
var_model = Model(var_q)
var_model.set_param_hint('L', value=0.1, min=0, max=1)
var_model.set_param_hint('vm', value=40, min=10, max=100)
var_model.set_param_hint('a', value=0.07846843689723797, min=0.068, max=0.079)
var_model.set_param_hint('b', value=-0.3260000001412797, min=-0.373, max=-0.326)

var_result = var_model.fit(var, x=density_list, weights=sample_weights)
print(mean_result.fit_report())
print(var_result.fit_report())
print(mean_result.best_values)
print(var_result.best_values)
vm_mean, a_mean, b_mean = mean_result.best_values['vm'], mean_result.best_values[
    'a'], mean_result.best_values['b']
L_var, vm_var, a_var, b_var = var_result.best_values['L'], var_result.best_values['vm'], var_result.best_values['a'], \
    var_result.best_values['b']
# mean_w, var_w = 0.8, 0.2
# L_fit, vm_fit, a_fit, b_fit = mean_w * L_mean + var_w * L_var, mean_w * vm_mean + var_w * vm_var, mean_w * a_mean + var_w * a_var, mean_w * b_mean + var_w * b_var
# print(L_fit, vm_fit, a_fit, b_fit)
# plot the mean and variance of flow relation to density
fig, ax = plt.subplots(1, 2, sharex='col')
ax[0].scatter(density, flow, s=1, c='r')
ax[0].plot(density_list, mean, label='mean q-k', c='b')
# ax[0].plot(1000 * np.arange(1, 0.001), 3.600 * mean_q(np.arange(1, 0.001), L, vm, a, b), label='fit mean q-k', c='g')
continuous_density = np.arange(0.1, 94)
ax[0].plot(continuous_density, mean_q(continuous_density, vm_mean, a_mean, b_mean), label='fit mean q-k', c='g')
# ax[0].plot(density_list, mean_result.best_fit, label='fit mean q-k', c='g')
ax[0].set_xlabel('density')
ax[0].set_ylabel('flow')
ax[0].legend()
ax[1].scatter(density, flow, s=1, c='r')
ax[1].scatter(density_list, var, label='variance q-k', c='b')
ax[1].plot(continuous_density, var_q(continuous_density, L_var, vm_var, a_var, b_var), label='fit variance q-k', c='g')
# ax[1].plot(density_list, result.best_fit[8:] * max_var, label='fit variance q-k', c='g')
# ax[1].plot(density_list, var_result.best_fit, label='fit variance q-k', c='g')
ax[1].set_xlabel('density')
ax[1].set_ylabel('flow')
ax[1].legend()
plt.show()
