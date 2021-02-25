import json

'''
    Keep only the tags the have something to do with aura mls. Filter everything else out
        for example, we would keep (aura/mls, o3) but would get rid of (aura/omi, o3)
    @todo: see what the method does and remove it if it doesn't do anything useful
'''


def just_aura_mls_mission():
    raw_data_file = 'ml_data/raw_data_noNO_standardized.json'
    with open(raw_data_file) as f:
        raw_data = json.load(f)
    with open('../data/json/datasets_to_couples.json') as f:
        datasets_to_couples = json.load(f)
    aura_mls_only = {}
    for key, value in raw_data.items():
        temp_data = {}
        aura_mls_ground_truths = []
        ground_truths = value['ground_truth']
        for gt in ground_truths:
            if gt == 'ML2HCl':
                gt = 'ML2HCL'
            if "aura:mls" in (datasets_to_couples.get(gt, [])):
                if len(gt) == 0:
                    print("Key error ", gt)
                    break
                aura_mls_ground_truths.append(gt)

        for k, v in value['data'].items():
            if k.startswith("(aura/mls"):
                print(k)
                temp_data[k] = v
        aura_mls_only[key] = {
            'ground_truths': aura_mls_ground_truths,
            'data': temp_data,
        }
    print(aura_mls_only)
    with open('ml_data/raw_data_aura_mls_ONLY_noNO.json', 'w', encoding='utf-8') as f:
        json.dump(aura_mls_only, f, indent=4)

if __name__ == '__main__':
    raw_data_file = 'ml_data/raw_data_all_papers_braod.json'
    with open(raw_data_file) as f:
        raw_data = json.load(f)
    with open('../data/json/datasets_to_couples.json') as f:
        datasets_to_couples = json.load(f)
    aura_mls_only = {}
    for key, value in raw_data.items():
        temp_data = {}
        aura_mls_ground_truths = []
        ground_truths = value['ground_truth']
        for gt in ground_truths:
            if gt == 'ML2HCl':
                gt = 'ML2HCL'
            if "aura:mls" in (datasets_to_couples.get(gt, [])):
                if len(gt) == 0:
                    print("Key error ", gt)
                    break
                aura_mls_ground_truths.append(gt)

        for k, v in value['data'].items():
            mis_ins, variable = k.split(",")
            if mis_ins.startswith("(aura/mls") or mis_ins.startswith("(aura/None") or mis_ins.endswith("/mls"):
                print(k)
                temp_data[k] = v
        aura_mls_only[key] = {
            'ground_truths': aura_mls_ground_truths,
            'data': temp_data,
        }
    print(aura_mls_only)
    # with open('ml_data/raw_data_all_papers_broad_aura_mls_ONLY.json', 'w', encoding='utf-8') as f:
    #     json.dump(aura_mls_only, f, indent=4)
