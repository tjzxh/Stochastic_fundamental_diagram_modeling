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
df = pd.read_csv("C:/Users/Administrator/Desktop/data_and_results/data/reconstructed_NGSIM.txt", sep='\s+', header=None,
                 names=["VehID", "FrameID", "LaneID", "LocalY", "MeanSpeed", "MeanAcc",
                        "Vehlen", "VehClass", "FollowerID", "LeaderID"])
# calculate the maximum speed
speeds = 3.6 * df.MeanSpeed.to_numpy()
point_y = 85
point_x = np.percentile(speeds, point_y)
print("Maximum speed: {} km/h".format(point_x))
# plot the cumulative distribution of the speeds
import matplotlib.pyplot as plt

plt.rcParams['font.size'] = '30'
plt.rcParams["font.family"] = "Times New Roman"
# sort the data in ascending order
x = np.sort(speeds)
N = len(speeds)
# get the cdf values of y
y = 100 * np.arange(N) / N
# plotting
fig, ax = plt.subplots(1)
plt.xlabel('Velocity (km/h)')
plt.ylabel('Empirical cumulative distribution (%)')
ax.boxplot(x)
# ax.plot(x, y, color='b', linewidth=3)
# ax.scatter(point_x, point_y, color='r', s=200)
# plt.xlim(0, 30 * 3.6)
# ax.set_aspect(1 / 1)
# plt.ylim(0, 100)
plt.show()

# # calculate the proportion of auto (VehClass=2) in the data
# print("Proportion of autos: {}%".format(100 * len(df[df.VehClass == 2]) / len(df)))  # 95.2%

# # filter the data
# all_data = np.array([])
# # get all vehicles where LaneID=2,3,4,5
# LaneID = 2345
# # iterate over the LaneID and the FrameID
# for lane in [2, 3, 4, 5]:
#     df_lane = df[df.LaneID == lane]
#     for frame in df.FrameID.unique():
#         # get all data for this frame and sort by LocalY
#         df_frame = df_lane[df_lane.FrameID == frame].sort_values(by=['LocalY'])
#         # calculate only when there are more than 2 vehicles
#         if len(df_frame) <= 2:
#             continue
#         # get all the speeds, lengths, localY and vehicle class
#         speeds = df_frame.MeanSpeed.to_numpy()
#         lengths = df_frame.Vehlen.to_numpy()
#         localY = df_frame.LocalY.to_numpy()
#         vehClass = df_frame.VehClass.to_numpy()
#         # get the average speed of the vehicles in this frame and this lane
#         avg_speed_in_lane = np.average(speeds)
#         # get the subject speed and leader speed
#         subject_speed = speeds[:-1]
#         leader_speed = speeds[1:]
#         # get the spacing between the vehicles
#         spacing = np.diff(localY) - lengths[1:]
#         # get the subject vehicle class and relative class
#         subject_class = vehClass[:-1]
#         relative_class = np.diff(vehClass)
#         # [frame, subject speed, leader speed, speed difference, average speed in lane, spacing, subject class, relative class]
#         data = np.column_stack(
#             (np.full(len(subject_speed), frame), subject_speed, leader_speed, subject_speed - leader_speed,
#              np.full(len(subject_speed), avg_speed_in_lane), spacing, subject_class, relative_class))
#         # stack the data
#         all_data = np.vstack((all_data, data)) if all_data.size else data
#
# # filter the data for homogeneous: append only for auto vehicles (classID=2 and relative class=0)
# homo_index = (all_data[:, 6] == 2) & (all_data[:, 7] == 0)
# homo_data = all_data[homo_index]
# # shuffle the data beforehand
# np.random.shuffle(homo_data)
# np.random.shuffle(all_data)
# # save the data into a text file
# np.savetxt("all_data_lane" + str(LaneID) + ".txt", all_data)
# np.savetxt("homo_data_lane" + str(LaneID) + ".txt", homo_data)
# print("Done! There are total {} data points and {} homo data points.".format(all_data.shape[0], homo_data.shape[0]))

# calculate the average DHW
# all_data = np.loadtxt("../data/all_data_lane234.txt")
# dis = all_data[:, 5]
# avg_dis = np.average(dis)
# print("Average spacing: {} m".format(avg_dis))
# speeds = all_data[:, 1]
# point_y = 85
# point_x = np.percentile(speeds, point_y)
# print("Maximum speed: {} km/h".format(3.6 * point_x))
