import pandas as pd
import os
from os.path import isfile
import statistics
from metadata import metadata
from matplotlib import pyplot as plt


def get_data_frame(path):
    df = pd.read_csv(path)
    df['citedReferences'] = df['citedReferences'].apply(lambda x: x.split('$$@$$'))

    return df


def sum_power_2(length: int):
    res = 0
    for i in range(length):
        res += 2 ** i

    return res


def promotion_effect_score(df, total_num_citations, total_num_references):
    if total_num_citations == 0:
        return 0

    res = 0
    for item in df['citedReferences']:
        res += sum_power_2(len(item))

    return res / (total_num_citations * total_num_references)


def promotion_effect_score_group(group_dir):
    res = []

    for f in os.listdir(group_dir):
        paperId = f.split('.')[0]
        full_relative_path = group_dir + "/" + f
        if isfile(full_relative_path):
            df = get_data_frame(full_relative_path)
            res.append(
                promotion_effect_score(df, metadata[paperId]["num citations"], metadata[paperId]["num references"]))

    return res


def promotion_effect_dispersion(df, total_num_references):
    paper_promotion = {}
    for item in df['citedReferences']:
        promotion_share = sum_power_2(len(item)) / len(item)
        for paper in item:
            if paper not in paper_promotion:
                paper_promotion[paper] = (promotion_share, 1)
            else:
                paper_promotion[paper][0] += promotion_share
                paper_promotion[paper][1] += 1

    # promotion_received = [paper_promotion[paper][0] / (paper_promotion[paper][1] * total_num_references) for paper in
    #                       paper_promotion.keys()]
    promotion_received = [paper_promotion[paper][0] / total_num_references for paper in paper_promotion.keys()]

    if len(promotion_received) == 0:
        return 0
    return statistics.pstdev(promotion_received)


def promotion_effect_dispersion_group(group_dir):
    res = []

    for f in os.listdir(group_dir):
        paperId = f.split('.')[0]
        full_relative_path = group_dir + "/" + f
        if isfile(full_relative_path):
            df = get_data_frame(full_relative_path)
            res.append(
                promotion_effect_dispersion(df, metadata[paperId]["num references"]))

    return res


def citation_pattern(df, total_num_citations):
    res = {}
    for item in df['citedReferences']:
        cur_num = len(item)
        if cur_num not in res:
            res[cur_num] = 1
        else:
            res[cur_num] += 1

    res[0] = total_num_citations - df.shape[0]
    return res


def citation_pattern_graph(group_dir, file_name):
    aggregated_citation_pattern_small = {}
    aggregated_citation_pattern_median = {}
    aggregated_citation_pattern_large = {}
    for f in os.listdir(group_dir):
        paperId = f.split('.')[0]
        full_relative_path = group_dir + "/" + f
        if isfile(full_relative_path):
            df = get_data_frame(full_relative_path)
            cur_citation_pattern = citation_pattern(df, metadata[paperId]["num citations"])
            for key in cur_citation_pattern:
                if key > 5:
                    key2 = 6
                    if key > 10:
                        key3 = 11
                        if key > 20:
                            key4 = 21
                        else:
                            key4 = key
                        if key4 not in aggregated_citation_pattern_large:
                            aggregated_citation_pattern_large[key4] = cur_citation_pattern[key]
                        else:
                            aggregated_citation_pattern_large[key4] += cur_citation_pattern[key]
                    else:
                        key3 = key
                    if key3 not in aggregated_citation_pattern_median:
                        aggregated_citation_pattern_median[key3] = cur_citation_pattern[key]
                    else:
                        aggregated_citation_pattern_median[key3] += cur_citation_pattern[key]
                else:
                    key2 = key
                if key2 not in aggregated_citation_pattern_small:
                    aggregated_citation_pattern_small[key2] = cur_citation_pattern[key]
                else:
                    aggregated_citation_pattern_small[key2] += cur_citation_pattern[key]

    sorted_keys_small = tuple(sorted(aggregated_citation_pattern_small.keys()))
    labels_small = [str(k) if k <= 5 else ">5" for k in sorted_keys_small]
    sizes_small = [aggregated_citation_pattern_small[k] for k in sorted_keys_small]
    plt.figure()
    plt.pie(sizes_small, labels=labels_small, startangle=90, shadow=False, explode=(0.1,)*len(labels_small),
            autopct='%1.2f%%')
    plt.savefig("{}_small".format(file_name))

    sorted_keys_median = tuple(sorted(aggregated_citation_pattern_median.keys()))
    labels_median = [str(k) if k <= 10 else ">10" for k in sorted_keys_median]
    sizes_median = [aggregated_citation_pattern_median[k] for k in sorted_keys_median]
    plt.figure()
    plt.pie(sizes_median, labels=labels_median, startangle=90, shadow=False, explode=(0.1,) * len(labels_median),
            autopct='%1.2f%%')
    plt.savefig("{}_median".format(file_name))

    sorted_keys_large = tuple(sorted(aggregated_citation_pattern_large.keys()))
    labels_large = [str(k) if k <= 20 else ">20" for k in sorted_keys_large]
    sizes_large = [aggregated_citation_pattern_large[k] for k in sorted_keys_large]
    plt.figure()
    plt.pie(sizes_large, labels=labels_large, startangle=90, shadow=False, explode=(0.1,) * len(labels_large),
            autopct='%1.2f%%')
    plt.savefig("{}_large".format(file_name))


def repetition(df):
    for i in range(1, len(df['citationName'])):
        if df['citationName'][i] == df['citationName'][i - 1]:
            print(i)

def repetition2(df):
    existing = {}
    for i in range(1, len(df['citationName'])):
        if df['citationName'][i] not in existing:
            existing[df['citationName'][i]] = [i+2]
        else:
            existing[df['citationName'][i]].append(i+2)

    for title in existing:
        if len(existing[title]) > 1:
            print("paper name: {}".format(title))
            for line_index in existing[title]:
                print("  on line {}".format(line_index))
            print("")

if __name__ == '__main__':
    df = get_data_frame("final_data/high_influence/1bb490fcd384c4bcda60cd8d1c592b266da5dbd1.csv")
    print(repetition2(df))

    # citation_pattern_graph("final_data/high_influence/backup", "high")
