import numpy as np
import matplotlib.pyplot as plt
from numpy import log
from sklearn import linear_model

#### unit: m, m/s
# l1 result
# ==============================================================================
#                  coef    std err          t      P>|t|      [0.025      0.975]
# ------------------------------------------------------------------------------
# const          0.8796      0.012     74.521      0.000       0.856       0.903
# x1            -0.2348      0.004    -58.979      0.000      -0.243      -0.227
# ==============================================================================
# l2 result
# ==============================================================================
#                  coef    std err          t      P>|t|      [0.025      0.975]
# ------------------------------------------------------------------------------
# const          0.5645      0.030     18.777      0.000       0.505       0.624
# x1            -0.2639      0.010    -26.032      0.000      -0.284      -0.244
# ==============================================================================
plt.rcParams['font.size'] = '30'
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams['mathtext.fontset'] = 'cm'  # cm for Cambria Math
plt.rcParams['mathtext.rm'] = 'Cambria Math'  # Set the font
plt.rcParams['mathtext.it'] = 'Cambria Math:italic'  # Set italic font
plt.rcParams['mathtext.cal'] = 'Cambria Math'  # Set calligraphy font
LaneID = 234
# [i, len(vs), res.x[0], res.x[1], res.x[2], res.fun]
results = np.loadtxt('./lamda_all' + str(LaneID) + '_m.txt')
# filter num > 100 and spacing > 0
valid_ind = (results[:, 1] > 100) & (results[:, 0] > 0)
spacing, num, l1, l2, l3, fun = results[valid_ind, 0], results[valid_ind, 1], results[valid_ind, 2], results[
    valid_ind, 3], results[valid_ind, 4], results[valid_ind, 5]
mean_l3 = np.mean(l3[l3 > 0])
print(f"mean l3 {mean_l3}")
# regression of l2
# Coef interval with statsmodels
import statsmodels.api as sm

l1_res = sm.OLS(l1, sm.add_constant(log(spacing))).fit()
l2_res = sm.OLS(l2, sm.add_constant(log(spacing))).fit()
# conf_interval = lr.conf_int(alpha=0.05)
print(l1_res.summary(), l2_res.summary())
# # plot the regression with confidence interval
# pred_ols = res.get_prediction()
# iv_l = pred_ols.summary_frame()["obs_ci_lower"]
# iv_u = pred_ols.summary_frame()["obs_ci_upper"]
#
# fig, ax = plt.subplots(1, 1)
#
# ax.scatter(np.log(spacing), l2, label='data')
# ax.plot(np.log(spacing), res.fittedvalues, "r--.", label="OLS")
# ax.plot(np.log(spacing), iv_u, "r--")
# ax.plot(np.log(spacing), iv_l, "r--")
# ax.legend(loc="best")

# Robustly fit linear model with RANSAC algorithm
huber1 = linear_model.HuberRegressor().fit(log(spacing).reshape(-1, 1), l1)
huber2 = linear_model.HuberRegressor().fit(log(spacing).reshape(-1, 1), l2)
# huber3 = linear_model.HuberRegressor().fit(spacing.reshape(-1, 1), l3)
print(huber1.coef_, huber1.intercept_, huber2.coef_, huber2.intercept_)
# huber2.coef_[0] * log(spacing) + huber2.intercept_
# plot the regression
fig, ax = plt.subplots(1, 3, sharex=True)
ax[0].scatter(spacing, l1, c='b', label='Calibrated value with I-80 data')
ax[0].plot(spacing, l1_res.predict(sm.add_constant(log(spacing))), 'r', label='Regression line')
ax[0].set_xlabel("$s$ (m)")
ax[0].set_ylabel(r"$\lambda_1$")
# ax[0].set_title('l1: ' + str(huber1.score(spacing.reshape(-1, 1), l1)))
ax[1].scatter(spacing, l2, c='b', label='Calibrated value with I-80 data')
ax[1].plot(spacing, l2_res.predict(sm.add_constant(log(spacing))), 'r', label='Regression line')
ax[1].set_xlabel("$s$ (m)")
ax[1].set_ylabel(r"$\lambda_2$")
# ax[1].set_title('l2: ' + str(huber2.score(np.log(spacing).reshape(-1, 1), l2)))
ax[2].scatter(spacing, l3, c='b', label='Calibrated value with I-80 data')
# ax[2].plot(spacing, huber3.predict(spacing.reshape(-1, 1)), "r")
ax[2].set_xlabel("$s$ (m)")
ax[2].set_ylabel(r"$\lambda_3$")
# ax[2].set_title('l3: ' + str(huber3.score(spacing.reshape(-1, 1), l3)))
ax[0].legend(loc="best", fontsize=18)
ax[1].legend(loc="best", fontsize=18)
ax[2].legend(loc="best", fontsize=18)
plt.show()
