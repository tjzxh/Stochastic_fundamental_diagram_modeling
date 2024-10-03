import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model
from numpy import exp, log

# unit: km, km/h
# l1 result
# ==============================================================================
#                  coef    std err          t      P>|t|      [0.025      0.975]
# ------------------------------------------------------------------------------
# const         -0.0573      0.001    -44.503      0.000      -0.060      -0.055
# x1            -0.0181      0.000    -58.979      0.000      -0.019      -0.018
# ==============================================================================
# l2 result
# ==============================================================================
#                  coef    std err          t      P>|t|      [0.025      0.975]
# ------------------------------------------------------------------------------
# const         -0.3496      0.012    -29.634      0.000      -0.373      -0.326
# x1            -0.0733      0.003    -26.032      0.000      -0.079      -0.068
# ==============================================================================
LaneID = 234
# [i, len(vs), res.x[0], res.x[1], res.x[2], res.fun]
results = np.loadtxt('./lamda_all' + str(LaneID) + '_m.txt')
# filter num > 100 and spacing < 0
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

# Robustly fit linear model with RANSAC algorithm
huber1 = linear_model.HuberRegressor().fit(log(spacing).reshape(-1, 1), l1)
huber2 = linear_model.HuberRegressor().fit(log(spacing).reshape(-1, 1), l2)
huber3 = linear_model.HuberRegressor().fit(spacing.reshape(-1, 1), l3)
print(huber1.coef_, huber1.intercept_, huber2.coef_, huber2.intercept_, huber3.coef_, huber3.intercept_)
# # # l1 = -0.01783546*ln(spacing)-0.05635338157648404
# # # l2 = -0.08117844*ln(spacing)-0.37961818136683223
# # # l3 = 0.006949186753829686
#
# plot the regression
fig, ax = plt.subplots(1, 3)
ax[0].scatter(log(spacing), l1)
ax[0].plot(log(spacing),  l1_res.predict(sm.add_constant(log(spacing))), 'r', label='Regression line')
ax[0].set_xlabel(r"ln(s) (km)")
ax[0].set_ylabel("lamda1")
ax[0].set_title('l1: ' + str(huber1.score(log(spacing).reshape(-1, 1), l1)))
ax[1].scatter(log(spacing), l2)
ax[1].plot(log(spacing), huber2.coef_[0] * log(spacing) + huber2.intercept_, 'r')
ax[1].set_xlabel("ln(spacing) (km)")
ax[1].set_ylabel("lamda2")
ax[1].set_title('l2: ' + str(huber2.score(log(spacing).reshape(-1, 1), l2)))
ax[2].scatter(spacing, l3)
ax[2].plot(spacing, huber3.predict(spacing.reshape(-1, 1)), "r")
ax[2].set_xlabel("spacing (km)")
ax[2].set_ylabel("lamda3")
ax[2].set_title('l3: ' + str(huber3.score(spacing.reshape(-1, 1), l3)))

plt.show()
