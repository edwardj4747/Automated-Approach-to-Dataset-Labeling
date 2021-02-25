import numpy as np
import copy
from matplotlib import pyplot as plt
import seaborn as sn

'''
    Given the predictions of a modoel and the ground truths, compute precision, recall, F1, papers fully correct, and
    plot some of these
'''


def pra_take_2(predicitions, y_labels, dataset_mapping, test_set_indices, debug=False):
    # return: precision, recall, F1, number of papers completely correct

    if debug:
        print(predicitions)

    inverted_dataset_mapping = {value: key for key, value in dataset_mapping.items()}
    correct, missed, extraneous = 0, 0, 0
    papers_fully_correct = 0

    correct_dict, missed_dict, extraneous_dict = {}, {}, {}

    true_labels = copy.deepcopy(y_labels)

    # Remove NON ML2xx datasets
    for key, value in true_labels.items():
        new_ground_truths = []
        for gt in value['ground_truths']:
            if gt.startswith("ML2"):
                new_ground_truths.append(gt)
        true_labels[key]['ground_truths'] = new_ground_truths

    # Main body: Check the predictions
    valid_paper_count = -1
    prediction_row_index = -1
    for paper_key, paper_value in true_labels.items():
        if len(paper_value['data']) == 0:
            continue

        valid_paper_count += 1

        if valid_paper_count in test_set_indices:
            prediction_row_index += 1
            if debug:
                print("paper_key ", paper_key, "row_index", prediction_row_index)

            ground_truths = paper_value['ground_truths']
            prediction_indices = np.where(predicitions[prediction_row_index, :] == 1)[0]
            no_extraneous_predictions = True
            for pred in prediction_indices:
                short_name = inverted_dataset_mapping[pred]
                if short_name in ground_truths:
                    correct += 1
                    ground_truths.remove(short_name)
                    correct_dict[short_name] = correct_dict.get(short_name, 0) + 1
                else:
                    extraneous += 1
                    extraneous_dict[short_name] = extraneous_dict.get(short_name, 0) + 1
                    no_extraneous_predictions = False
            missed += len(ground_truths)
            if len(ground_truths) == 0 and no_extraneous_predictions:
                papers_fully_correct += 1

            for short_name in ground_truths:
                missed_dict[short_name] = missed_dict.get(short_name, 0) + 1

    print("Correct ", correct)
    print("Missed ", missed)
    print("Extraneous ", extraneous)
    print("Papers fully corect ", papers_fully_correct)

    precision = 0 if correct == 0 and extraneous == 0 else correct / (correct + extraneous)
    recall = correct / (correct + missed)
    f1 = 0 if precision == 0 or recall == 0 else 2 * precision * recall / (precision + recall)

    print()
    print("Precision ", precision)
    print("Recall ", recall)
    print("F1 ", f1)

    print("correct ", sorted(correct_dict.items(), key=lambda x: x[1]))
    print("missed ", sorted(missed_dict.items(), key=lambda x: x[1]))
    print("extraneous ", sorted(extraneous_dict.items(), key=lambda x: x[1]))
    print("**********")

    return precision, recall, f1, papers_fully_correct, (correct, missed, extraneous)


def plot_precision_recall_f1(precision_list, recall_list, f1_list, loop_begin, loop_end, title="Untitled",
                             papers_completely_correct=None, save_plots=None, cme_list=None):

    plt.figure()
    max_f1 = max(f1_list)
    max_f1_index = f1_list.index(max_f1)

    x_labels = np.arange(loop_begin, loop_end)
    plt.plot(x_labels, precision_list, label="Precision")
    plt.plot(x_labels, recall_list, label="Recall")
    plt.plot(x_labels, f1_list, label="F1-Score")
    plt.xlabel("Max Depth")
    plt.title(title)
    plt.xticks(np.arange(loop_begin, loop_end))
    plt.annotate("Max F1: {:.2f}\nDepth={}".format(max_f1, max_f1_index), xy=(x_labels[max_f1_index], f1_list[max_f1_index]),
                 xytext=(x_labels[max_f1_index] + 1, f1_list[max_f1_index] + 0.2), arrowprops={'arrowstyle': '->'})
    plt.legend()
    if save_plots is not None:
        plt.savefig(save_plots + title + "_fig_1")

    if papers_completely_correct:
        max_papers_correct = max(papers_completely_correct)
        max_index = papers_completely_correct.index(max_papers_correct)

        plt.figure()
        plt.bar(x_labels, papers_completely_correct)
        plt.xticks(np.arange(loop_begin, loop_end))

        plt.xlabel("Max Depth")
        plt.ylabel("Papers Completely Correct")
        plt.title(title)
        plt.annotate("Max: {}\nDepth: {}".format(max_papers_correct, max_index), xy=(x_labels[max_index], papers_completely_correct[max_index]),
                     xytext=(x_labels[max_index] + 2, papers_completely_correct[max_index] - 0.1), arrowprops={'arrowstyle': '->'})
        if save_plots is not None:
            plt.savefig(save_plots + title + "_fig_2")

    if cme_list is not None:
        correct, missed, extraneous = cme_list[max_f1_index]
        matrix = np.array([[correct, extraneous], [missed, 0]])
        plot_confusion_matrix(matrix, title, save_plots)
    plt.show()


def plot_confusion_matrix(confusion_matrix, title, save_plots=""):
    plt.figure()
    sn.heatmap(confusion_matrix, annot=True, cmap='BrBG', annot_kws={'fontsize': 'large'})
    plt.xlabel("True", fontsize='large')
    plt.ylabel("Predicted", fontsize='large')
    plt.xticks([])
    plt.yticks([])
    if save_plots is not None:
        plt.savefig(save_plots + title + "_confusion_matrix")
    plt.show()


def pra_nerual_net(predicitions, y_labels):
    # predictions and y_labels are both numpy arrays of 1s and 0s of the same size

    num_rows, num_cols = predicitions.shape
    correct, missed, extraneous = 0, 0, 0
    papers_fully_correct = 0
    for r in range(num_rows):
        if all(predicitions[r, :] == y_labels[r, :]):
            papers_fully_correct += 1
        for c in range(num_cols):
            a_value = predicitions[r, c]
            b_value = y_labels[r, c]
            if a_value == 1 and b_value == 1:
                correct += 1
            elif a_value == 1 and b_value == 0:
                extraneous += 1
            elif a_value == 0 and b_value == 1:
                missed += 1


    print("Correct ", correct)
    print("Missed ", missed)
    print("Extraneous ", extraneous)
    print("Papers fully corect ", papers_fully_correct)

    precision = 0 if correct == 0 and extraneous == 0 else correct / (correct + extraneous)
    recall = correct / (correct + missed)
    f1 = 0 if precision == 0 or recall == 0 else 2 * precision * recall / (precision + recall)

    print()
    print("Precision ", precision)
    print("Recall ", recall)
    print("F1 ", f1)
    print("**********")

    return precision, recall, f1, papers_fully_correct, (correct, missed, extraneous)
