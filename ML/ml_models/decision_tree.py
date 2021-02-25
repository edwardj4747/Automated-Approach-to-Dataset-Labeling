import json

from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split, cross_val_score
import numpy as np
from ml_model_utils import precision_recall_analysis

print("Starting")
# Load in the data
X = np.load('../ml_ready_data/one_hot_2068_features_strict_160_papers.npy')
y_9 = np.load('../ml_ready_data/ML2xx_num_datasets_9_papers_160.npy')
y_23 = np.load('../ml_ready_data/ML2xx_num_datasets_23_papers_160.npy')

y = y_9

# Declare some useful properties
num_papers, num_features = X.shape
train_percentage = 0.8
print(num_papers, num_features)

# Train/Test splits. Can't Use sklearn train_test_split bc later on we will need to know which rows (papers) are in which set
# X_train, X_test, y_train, y_test = train_test_split(X, y_9, test_size=0.2, random_state=1)
np.random.seed(1)
permutation = np.random.permutation(num_papers)
print(permutation)

# Determine the split for training and testing
upper_bound = int(num_papers * train_percentage)
training_indices = permutation[:upper_bound]
testing_indices = permutation[upper_bound:]

print("training ", training_indices)
print("testing ", sorted(testing_indices))


X_train = X[training_indices, :]
X_test = X[testing_indices, :]

y_train = y[training_indices, :]
y_test = y[testing_indices, :]

print(X_train.shape, y_train.shape)
print(X_test.shape, y_test.shape)




dtc = DecisionTreeClassifier(max_depth=7)
dtc.fit(X_train, y_train)

print(dtc.score(X_train, y_train))
print(dtc.score(X_test, y_test))

predictions = dtc.predict(X_test)
print(predictions)

# print("****")
# print(y_test)

with open('../ml_data/raw_data_aura_mls_ONLY_noNO.json') as f:
    input_data = json.load(f)

with open('../ml_ready_data/9_dataset_mapping_threshold_10.json') as f:
    dataset_mapping = json.load(f)

# precision_recall_analysis(predictions, input_data, dataset_mapping, testing_indices)

# look at the training
# precision_recall_analysis(dtc.predict(X_train), input_data, dataset_mapping, training_indices)