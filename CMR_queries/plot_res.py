from matplotlib import pyplot as plt
import numpy as np
import matplotlib
import datetime

run_one = np.array([55, 66, 89, 117, 161, 175, 176, 177, 189])
run_two = np.array([90, 100, 109, 131, 159, 175, 176, 177, 189])
run_two_usage = np.array([99, 113, 124, 159, 164, 170, 186, 187, 189])

run_one = [55, 66, 89, 117, 161, 175, 176, 177, 189]
run_two = [90, 100, 109, 131, 159, 175, 176, 177, 189]
run_two_usage = [99, 113, 124, 159, 164, 170, 186, 187, 189]

x = np.arange(1, 10)
print(x)

y = run_one
z = run_two
k = run_two_usage

ax = plt.subplot(111)
ax.bar(x-0.2, y, width=0.2, color='b', align='center')
ax.bar(x, z, width=0.2, color='g', align='center')
ax.bar(x+0.2, k, width=0.2, color='r', align='center')

plt.savefig('omi results with diff cmr')
plt.ylabel('Num Correct')
plt.xlabel("Top-N")
plt.title("Different CMR Versions")
plt.show()