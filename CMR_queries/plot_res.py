from matplotlib import pyplot as plt
import numpy as np
import matplotlib
import datetime

# AUra/omu collection. Run one was with a bad state of CMR
run_one = np.array([55, 66, 89, 117, 161, 175, 176, 177, 189])
run_two = np.array([90, 100, 109, 131, 159, 175, 176, 177, 189])
run_two_usage = np.array([99, 113, 124, 159, 164, 170, 186, 187, 189])

run_two_missed = [380, 370, 361, 339, 311, 295, 294, 293, 281]
run_two_extraneous = [281, 480, 708, 864, 1056, 1186, 1368, 1502, 1606]

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

plt.ylabel('Num Correct')
plt.xlabel("Top-N")
plt.title("Different CMR Versions")
plt.savefig('omi results with diff cmr')
plt.show()

plt.bar(x, run_two, color='g')
plt.xticks([1,2,3,4,5,6,7,8,9])
plt.title("Datasets Correctly Predicted")
plt.xlabel("Top-n")
plt.ylabel("Number of Datasets")
plt.savefig("Omi Correct Datasets")
plt.show()

plt.bar(x, run_two_missed, color='r')
plt.xticks([1,2,3,4,5,6,7,8,9])
plt.title("Datasets Not Predicted")
plt.xlabel("Top-n")
plt.ylabel("Number of Datasets")
plt.savefig("Omi Not Predicted Datasets")
plt.show()

plt.bar(x, run_two_extraneous, color='b')
plt.xticks([1,2,3,4,5,6,7,8,9])
plt.title("Datasets Predicted that Should Not Have Been")
plt.xlabel("Top-n")
plt.ylabel("Number of Datasets")
plt.savefig("Omi extraneous Datasets")
plt.show()

# Plot the three on the same graph
ax = plt.subplot(111)
ax.bar(x-0.2, run_two, width=0.2, color='g', align='center', label='Correct')
ax.bar(x, run_two_missed, width=0.2, color='r', align='center', label='Missed')
ax.bar(x+0.2, run_two_extraneous, width=0.2, color='b', align='center', label='Extra')

plt.ylabel('Num Correct')
plt.xlabel("Top-N")
plt.title("Full Results")
plt.legend()
plt.savefig('omi results cme')
plt.show()