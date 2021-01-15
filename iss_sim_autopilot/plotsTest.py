import matplotlib.pyplot as plt
rangeTimeList=[0.1, 0.2, 0.3]
rangeZList=[1, 2, 3.5]
currentRateZList=[1, 2, 3.5]
desiredRateZList=[1, 2, 3.5]
fig, axs = plt.subplots(3)
fig.suptitle('Stats')
axs[0].plot(rangeTimeList,rangeZList)
axs[1].plot(rangeTimeList,currentRateZList)
axs[2].plot(rangeTimeList,desiredRateZList)
plt.draw()
plt.show()