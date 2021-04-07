import json
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
import numpy as np
from ML.ml_models.ml_model_utils import plot_precision_recall_f1, pra_single_dataset_classifier
from enum import Enum
import graphviz
from joblib import dump

'''
    Build and evaluate different decision trees and random forest ML models
'''


class ClassifierType(Enum):
    DECISION_TREE = 0,
    RANDOM_FOREST = 1


class RunningMode(Enum):
    SINGLE = 0,
    MULTIPLE = 1


# Load in the dataset mapping
with open('../ml_ready_data/author_keywords/Mar5_combined_13_dataset_mapping_threshold_10.json') as f:
    dataset_mapping = json.load(f)

# with open('../ml_data/raw_data_aura_mls_ONLY_noNO.json') as f:
#     input_dictionary = json.load(f)

with open('../ml_ready_data/author_keywords/344author_keywords_attempt_d1_mn4_tr6_MERGED.json') as f:
    input_dictionary = json.load(f)

# with open('../z_keyword_sentence_improvement_attempts/data/344author_keywords_attempt_d1_mn4_tr6_M.json') as f:
#     input_dictionary = json.load(f)

# Load in the data
X = np.load('../ml_ready_data/author_keywords/Mar3_tfidf_344_papers_30_words.npy')
# y_9 = np.load('../ml_ready_data/ML2xx_num_datasets_9_papers_234.npy')
# y_23 = np.load('../ml_ready_data/ML2xx_num_datasets_23_papers_234.npy')
y_all = np.load('../ml_ready_data/author_keywords/Mar5_ML2xxPlusCombined_num_datasets_13_papers_344.npy')

# with open('../ml_ready_data/23_dataset_mapping.json') as f:
#     dataset_mapping = json.load(f)


save_pdf_visualization = False
save_best_model = True
classifier_type = ClassifierType.DECISION_TREE
# classifier_for = 'ML2O3'  # only for when doing a single classifier
save_location = "C:/Users/edwar/Desktop/Publishing Internship/Progress Reports/W8 Trees Take 2/17_datasets/"
    # save_location = None

for key, value in dataset_mapping.items():
    classifier_for = key
    classifier_index = value

     # @todo: change y labels for this and raw_data to make OMTO3 and OMTO3d the same
    if classifier_for != "OMTO3" and classifier_for != "UARH":
        continue
    save_pdf_visualization = True

    title_value = classifier_type.name + " TF-IDF 30 Keywords-" + classifier_for + " classifier"
    # title_value = classifier_type.name + " Doc2Vec Broad VS 32 Thresholded E50"

    rf_num_trees = 5

    if classifier_type == ClassifierType.RANDOM_FOREST:
        title_value += " " + str(rf_num_trees) + " Trees"

    # correct_title = input("Is the title for the figures correct?\n{}\n".format(title_value))
    # if correct_title != "yes":
    #     exit(1)


    y = y_all[:, classifier_index]  # create models one dataset at a time

    # Declare some useful properties
    num_papers, num_features = X.shape
    test_percentage = 0.2




    # the first x papers are training. Going alphabetically should actually probably not be that terrible
    test_train_split = int(test_percentage * num_papers)
    print("Test train split index is ", test_train_split)

    # calculate dataset number of occurrences
    # print(np.sum(y_11, axis=0))
    # print(np.sum(y_11[test_train_split:, :], axis=0))
    # print(np.sum(y_11[:test_train_split, :], axis=0))
    # exit()


    X_test = X[:test_train_split, :]
    # y_test = y[:test_train_split, :]
    y_test = y[:test_train_split]


    X_train = X[test_train_split:, :]
    # y_train = y[test_train_split:, :]
    y_train = y[test_train_split:]



    # print("Train test distribution ", classifier_for)
    # print(np.sum(y_train))
    # print(np.sum(y_test))

    print(X_train.shape, y_train.shape, X_test.shape, y_test.shape)

    precision_list = []
    recall_list = []
    f1_list = []
    totally_correct_list = []
    cme_list = []  # correct, missed, extraneous

    loop_begin = 1
    loop_end = 7
    min_leaf_samples = int(np.sum(y_train) * 0.15)

    best_model = None
    best_f1 = 0
    best_model_props = ''

    for md in range(loop_begin, loop_end):
        print("md is ", md)
        if classifier_type == ClassifierType.DECISION_TREE:
            # clf = DecisionTreeClassifier(random_state=1, max_depth=md)
            clf = DecisionTreeClassifier(random_state=1, max_depth=md, max_leaf_nodes=8, min_samples_split=15, min_samples_leaf=min_leaf_samples)
        elif classifier_type == ClassifierType.RANDOM_FOREST:
            clf = RandomForestClassifier(random_state=1, max_depth=md, n_estimators=rf_num_trees, max_leaf_nodes=8, min_samples_split=15, min_samples_leaf=min_leaf_samples)

        clf.fit(X_train, y_train)
        # print(list(clf.tree_.feature))

        if save_pdf_visualization:
            dot_data = tree.export_graphviz(clf, filled=True, rounded=True)
            graph = graphviz.Source(dot_data)
            graph.render(save_location + title_value + "_md" + str(md) + "_decision_tree")


        print(clf.score(X_train, y_train))
        print(clf.score(X_test, y_test))

        predictions = clf.predict(X_test)

        # precision, recall, f1, totally_correct, cme = pra_take_2(predictions, input_dictionary, dataset_mapping, range(0, test_train_split))
        precision, recall, f1, totally_correct, cme = pra_single_dataset_classifier(predictions, input_dictionary, range(0, test_train_split), classifier_for=classifier_for)

        precision_list.append(precision)
        recall_list.append(recall)
        f1_list.append(f1)
        totally_correct_list.append(totally_correct)
        cme_list.append(cme)

        if f1 > best_f1:
            best_model = clf
            best_f1 = f1
            best_model_props = f'_md{md}_ms_{min_leaf_samples}_'

    plot_precision_recall_f1(precision_list, recall_list, f1_list, loop_begin, loop_end, title=title_value, papers_completely_correct=totally_correct_list,
                             save_plots=save_location, cme_list=cme_list)

    if save_best_model:
        dump(best_model, 'classifier_models/' + title_value + best_model_props + ".joblib")





