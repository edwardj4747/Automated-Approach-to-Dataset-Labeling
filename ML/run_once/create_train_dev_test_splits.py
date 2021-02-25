import json
import random


def read_json_file(file_name):
    with open('../ml_data/' + file_name + '.json', encoding='utf-8') as f:
        return json.load(f)

if __name__ == '__main__':
    ground_truths = read_json_file('ground_truths')
    threshold = 4
    ground_truths_less_than_four = [gt for gt in ground_truths.keys() if len(ground_truths[gt]) <= threshold]

    print("len gt ", len(ground_truths))
    print("len gtltt ", len(ground_truths_less_than_four))

    train_percentage = 0.8
    dev_percentage = 0.1
    test_percentage = 0.1

    random.seed(1)

    print(ground_truths_less_than_four)
    random.shuffle(ground_truths_less_than_four)
    print(ground_truths_less_than_four)

    t1 = int(train_percentage * len(ground_truths_less_than_four))
    t2 = int(dev_percentage * len(ground_truths_less_than_four))
    print("T1 ", t1, "t2 ", t2)
    train = ground_truths_less_than_four[:t1]
    dev = ground_truths_less_than_four[t1:t1+t2]
    test = ground_truths_less_than_four[t1+t2:]

    splits = {
        "train": train,
        "dev": dev,
        "test": test
    }

    with open('../ml_data/train_test_split.json', 'w', encoding='utf-8') as f:
        json.dump(splits, f, indent=4)