import numpy as np

y = np.load('Mar3_ML2xx_num_datasets_11_papers_344.npy')

num_papers, _ = y.shape
test_percentage = 0.2

# the first x papers are training. Going alphabetically should actually probably not be that terrible
test_train_split = int(test_percentage * num_papers)
print("Test train split index is ", test_train_split)


# X_test = X[:test_train_split, :]
y_test = y[:test_train_split]

# X_train = X[test_train_split:, :]
# y_train = y[test_train_split:, :]
y_train = y[test_train_split:]

print(np.sum(y_train, axis=0))
print(np.sum(y_test, axis=0))