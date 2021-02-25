import json
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
import numpy as np
from ml_model_utils import pra_take_2, plot_precision_recall_f1
from enum import Enum

'''
    Build and evaluate different decision trees and random forest ML models
'''


class ClassifierType(Enum):
    DECISION_TREE = 0,
    RANDOM_FOREST = 1


classifier_type = ClassifierType.DECISION_TREE
title_value = classifier_type.name + " Doc2Vec CORPUS VS 32 trained broad Thresholded"
# title_value = classifier_type.name + " Doc2Vec Broad VS 32 Thresholded E50"
rf_num_trees = 10

if classifier_type == ClassifierType.RANDOM_FOREST:
    title_value += " " + str(rf_num_trees) + " Trees"

save_location = "C:/Users/edwar/Desktop/Publishing Internship/Progress Reports/W5 ML algo exploration/"
# save_location = None

correct_title = input("Is the title for the figures correct?\n{}\n".format(title_value))
if correct_title != "yes":
    exit(1)


# with open('../ml_data/raw_data_aura_mls_ONLY_noNO.json') as f:
#     input_dictionary = json.load(f)

with open('../ml_data/raw_data_all_papers_broad_aura_mls_ONLY.json') as f:
    input_dictionary = json.load(f)

with open('../ml_ready_data/9_dataset_mapping_threshold_10.json') as f:
    dataset_mapping = json.load(f)

# with open('../ml_ready_data/23_dataset_mapping.json') as f:
#     dataset_mapping = json.load(f)


# Load in the data
X = np.load('../ml_ready_data/doc2vec_ALL_CORPUS_broad_234_papers_VS_32_epochs_100.npy')
y_9 = np.load('../ml_ready_data/ML2xx_num_datasets_9_papers_234.npy')
y_23 = np.load('../ml_ready_data/ML2xx_num_datasets_23_papers_234.npy')

y = y_9

# Declare some useful properties
num_papers, num_features = X.shape
test_percentage = 0.2


# the first 30 papers are training. Going alphabetically should actually probably not be that terrible
test_train_split = int(test_percentage * num_papers)
print("Test train split index is ", test_train_split)


# debug_value = 9  # raw_data[5] has no data
# X_test = X[:debug_value, :]
# y_test = y[:debug_value, :]
#
#
# X_train = X[10:, :]
# y_train = y[10:, :]


X_test = X[:test_train_split, :]
y_test = y[:test_train_split, :]


X_train = X[test_train_split:, :]
y_train = y[test_train_split:, :]

print(X_train.shape, y_train.shape, X_test.shape, y_test.shape)



precision_list = []
recall_list = []
f1_list = []
totally_correct_list = []
cme_list = []  # correct, missed, extraneous

loop_begin = 1
loop_end = 22

for md in range(loop_begin, loop_end):
    print("md is ", md)
    if classifier_type == ClassifierType.DECISION_TREE:
        clf = DecisionTreeClassifier(random_state=1, max_depth=md)
    elif classifier_type == ClassifierType.RANDOM_FOREST:
        clf = RandomForestClassifier(random_state=1, max_depth=md, n_estimators=rf_num_trees)

    clf.fit(X_train, y_train)
    # print(list(clf.tree_.feature))


    import graphviz
    dot_data = tree.export_graphviz(clf, filled=True, rounded=True)
    graph = graphviz.Source(dot_data)
    graph.render(title_value + "_decision_tree")





    print(clf.score(X_train, y_train))
    print(clf.score(X_test, y_test))

    predictions = clf.predict(X_test)

    precision, recall, f1, totally_correct, cme = pra_take_2(predictions, input_dictionary, dataset_mapping,
                                                        range(0, test_train_split))

    precision_list.append(precision)
    recall_list.append(recall)
    f1_list.append(f1)
    totally_correct_list.append(totally_correct)
    cme_list.append(cme)


plot_precision_recall_f1(precision_list, recall_list, f1_list, loop_begin, loop_end, title=title_value, papers_completely_correct=totally_correct_list,
                         save_plots=save_location, cme_list=cme_list)






