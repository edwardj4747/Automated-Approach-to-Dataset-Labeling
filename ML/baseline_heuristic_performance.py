import json
from ast import literal_eval
from collections import Counter

'''
    See how well two simple dataset prediction heuristics perform
        1. If a sentence has (aura/mls, science keyword), predicted ML2Science_keyword dataset
            ie: (aura/mls, co) -> predict ML2CO
        2. If a paper does not have any sentences with all of mission, instrument, and variable, look at the sentences
            with two of mission, instrument, and science keyword
                Perform a commutative property-like hueristic. 
                ie: if (aura/mls, None) and (None/mls, o3) appear, predict ML2O3
'''


def commutative(data):
    missions_instrument_key = "(aura/mls"

    science_keywords_found = []
    found_aura_mls = False
    for key in data['data']:
        science_keyword = key.split(",")[1][:-1]
        if science_keyword != 'None':
            science_keywords_found.append(science_keyword)
        if key.startswith(missions_instrument_key):
            found_aura_mls = True

    if found_aura_mls:
        predictions = []
        # make prediction ML2xx for all science Keywords
        for sk in science_keywords_found:
            prediction = "ML2" + sk.upper()
            print(paper, "Prediction ", prediction)
            predictions.append(prediction)

        return predictions
    return []


def check_correctness_of_prediction(ground_truths, correct_predictions, extraneous_predictions):
    if prediction in ground_truths:
        correct_predictions += 1
        ground_truths.remove(prediction)
    else:
        print("Extraneous key is ", paper)
        extraneous_predictions += 1
    return correct_predictions, extraneous_predictions


if __name__ == '__main__':
    with open('ml_data/raw_data_aura_mls_ONLY_noNO.json') as f:
        raw_data = json.load(f)

    with open('ml_data/papers_with_broad_sentences.json') as f:
        papers_with_no_sentences = json.load(f)

    correct_predictions = 0
    missed_predictions = 0
    extraneous_predictions = 0
    missed_dataset_counts = {}

    for paper, paper_value in raw_data.items():
        ground_truths = paper_value['ground_truths']
        if len(paper_value['data']) == 0:
            print("No extracted sentences. Applying commutative Property Heuristic")
            predictions = commutative(papers_with_no_sentences[paper])
            for pred in predictions:
                correct_predictions, extraneous_predictions = check_correctness_of_prediction(ground_truths, correct_predictions, extraneous_predictions)
        else:
            for k, v in paper_value['data'].items():
                mis_ins, science_keyword = k.split(",")
                science_keyword = science_keyword[:-1]
                split = mis_ins.split("/")
                mis = split[0][1:]
                ins = split[1]
                # print(mis, ins, science_keyword)
                if mis == 'aura' and ins == 'mls':
                    prediction = 'ML2' + science_keyword.upper()
                    print("Prediction ", prediction)
                    correct_predictions, extraneous_predictions = check_correctness_of_prediction(ground_truths, correct_predictions, extraneous_predictions)
                else:
                    print("No prediction")
        missed_predictions += len(ground_truths)
        # keep track of the datasets that were missed
        for mp in ground_truths:
            missed_dataset_counts[mp] = missed_dataset_counts.get(mp, 0) + 1

        print("-------")

    print("Correct ", correct_predictions)
    print("Missed ", missed_predictions)
    print("Extraneous ", extraneous_predictions)

    counter = Counter(missed_dataset_counts)
    print("Most common missed datasets ", counter.most_common())

    missed_ML2 = 0
    missed_others = 0
    for paper, paper_value in missed_dataset_counts.items():
        if paper.startswith("ML2"):
            missed_ML2 += paper_value
        else:
            missed_others += paper_value
    print("missed ML2xx ", missed_ML2)
    print("missed others ", missed_others)