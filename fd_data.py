import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# read text file into pandas DataFrame and create header with names
# Column 1:	Vehicle ID
# Column 2:	Frame ID
# Column 3:	Lane ID
# Column 4:	LocalY
# Column 5:	Mean Speed
# Column 6:	Mean Acceleration
# Column 7:	Vehicle length
# Column 8:	Vehicle Class ID
# Column 9:	Follower ID
# Column 10: Leader ID
# df = pd.read_csv("D:/Reconstructed_I80/reconstructed_NGSIM.txt", sep='\s+', header=None,
#                  names=["VehID", "FrameID", "LaneID", "LocalY", "MeanSpeed", "MeanAcc",
#                         "Vehlen", "VehClass", "FollowerID", "LeaderID"])
# # calculate density and flow in fixed spatial interval and instants
# # get all vehicles where LaneID=2 and localY before on-ramp
# min_y, max_y, ft_to_m = 800 - 100 / 0.3048, 800, 0.3048
# LaneID = 234
# # filter lane 2,3,4
# df = df[(df.LaneID == 2) | (df.LaneID == 3) | (df.LaneID == 4)]
# df = df[(df.LocalY >= min_y * ft_to_m) & (df.LocalY <= max_y * ft_to_m)]
# fd_data = []
# all_frame = df.FrameID.unique()
frame, interval = 0, 10
# # iterate over the ascending FrameID for 10 steps (10 frames)
# while frame < max(all_frame):
#     # get all data for this frame
#     df_frame = df[(df.FrameID >= frame) & (df.FrameID < frame + interval)]
#     # calculate only when there are all ClassVeh 2 vehicles
#     vehClass = df_frame.VehClass.to_numpy()
#     if len(df_frame) == 0:
#         frame += interval
#         continue
#     # get density and all the speeds
#     density = len(df_frame) / ((max_y - min_y) * ft_to_m) / 3 / interval
#     speeds = df_frame.MeanSpeed.to_numpy()
#     avg_speed_in_lane = np.average(speeds)
#     flow = density * avg_speed_in_lane
#     fd_data.append([frame, flow, density, avg_speed_in_lane])
#     frame += interval
# # save the data into a text file
# print(len(fd_data))
# fd_data = np.array(fd_data)
# np.savetxt("fd_data_" + str(interval) + "_frame.txt", fd_data)
# plot the data
fd_data = np.loadtxt("fd_data_" + str(interval) + "_frame.txt")
flow, density, speed = 3600 * fd_data[:, 1], 1000 * fd_data[:, 2], 3.6 * fd_data[:, 3]
# filter the valid data with density<85
valid_index = np.where(density < 85)
flow, density, speed = flow[valid_index], density[valid_index], speed[valid_index]
plt.rcParams['font.size'] = '30'
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams['mathtext.fontset'] = 'cm'  # cm for Cambria Math
plt.rcParams['mathtext.rm'] = 'Cambria Math'  # Set the font
plt.rcParams['mathtext.it'] = 'Cambria Math:italic'  # Set italic font
plt.rcParams['mathtext.cal'] = 'Cambria Math'  # Set calligraphy font
fig = plt.figure()
spec = fig.add_gridspec(2, 2)
ax0 = fig.add_subplot(spec[:, 0])
ax1 = fig.add_subplot(spec[0, 1])
ax2 = fig.add_subplot(spec[1, 1])
ax0.scatter(density, flow, c='b')
ax0.set_xlabel("$k$ (veh/km/lane)")
ax0.set_ylabel("$Q$ (veh/h/lane)")
ax0.set_xticks(np.arange(0, 91, 10))
ax0.set_aspect(1 / 20)
# plot the mean flow in ax1 and variance in ax2
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
ax1.scatter(density_list, mean, c='b')
ax1.set_xlabel("$k$ (veh/km/lane)")
ax1.set_ylabel("E[$Q$]")
ax1.set_xticks(np.arange(0, 91, 30))
ax1.set_aspect(1 / 20)
ax2.scatter(density_list, var, c='b')
ax2.set_xlabel("$k$ (veh/km/lane)")
ax2.set_ylabel("Var[$Q$]")
ax2.set_xticks(np.arange(0, 91, 30))
ax2.set_aspect(1 / 1650)
# print the total number of data points
# print(len(fd_data))
plt.show()
