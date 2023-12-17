from collections import deque
import os
from os.path import isfile, isdir
import requests
from metadata import metadata
from data_processing import get_data_frame, promotion_effect_score, promotion_effect_dispersion

S2_API_KEY = "K0YJzhxZI15eLBiS7zAUz1n1QgobRC3O4yXkPnIt"


def find_scores_by_publication_year(group_dir):
    queue = deque([group_dir])
    promotionEffectScores = {}
    promotionEffectDispersionScores = {}

    while len(queue) > 0:
        cur_dir = queue.popleft()
        for f in os.listdir(cur_dir):
            full_relative_path = cur_dir + "/" + f
            if isfile(full_relative_path):
                if f.endswith(".csv"):
                    paperId = f.split('.')[0]
                    rsp = requests.get(
                        'https://api.semanticscholar.org/graph/v1/paper/{}?fields=year'.format(
                            paperId), headers={'x-api-key': S2_API_KEY})
                    rsp.raise_for_status()
                    paper = rsp.json()
                    df = get_data_frame(full_relative_path)
                    published_year = paper['year']
                    promotionEffectScore = promotion_effect_score(df, metadata[paperId]["num citations"], metadata[paperId]["num references"])
                    promotionDispersionScore = promotion_effect_dispersion(df, metadata[paperId]["num references"])

                    if published_year not in promotionEffectScores:
                        promotionEffectScores[published_year] = [promotionEffectScore]
                    else:
                        promotionEffectScores[published_year].append(promotionEffectScore)

                    if published_year not in promotionEffectDispersionScores:
                        promotionEffectDispersionScores[published_year] = [promotionDispersionScore]
                    else:
                        promotionEffectDispersionScores[published_year].append(promotionDispersionScore)

            elif isdir(full_relative_path):
                queue.append(full_relative_path)

    for k, v in promotionEffectScores.items():
        promotionEffectScores[k] = sum(v) / float(len(v))

    for k, v in promotionEffectDispersionScores.items():
        promotionEffectDispersionScores[k] = sum(v) / float(len(v))

    return sorted(promotionEffectScores.items()), sorted(promotionEffectDispersionScores.items())


if __name__ == '__main__':
    promotionEffectScores, promotionEffectDispersionScores = find_scores_by_publication_year("final_data/high_influence")
    print(promotionEffectDispersionScores)