import requests
import time
import csv

S2_API_KEY = "K0YJzhxZI15eLBiS7zAUz1n1QgobRC3O4yXkPnIt"


def get_data(paperType, hIndexType, paperId):
    rsp = requests.get('https://api.semanticscholar.org/graph/v1/paper/{}?fields=url,citations,references'.format(
        paperId), headers={'x-api-key': S2_API_KEY})
    rsp.raise_for_status()
    high_influence_paper = rsp.json()
    print("{} paper ID: {}".format(paperType, high_influence_paper['paperId']))
    print("{} paper url: {}".format(paperType, high_influence_paper['url']))
    print("{} paper citations: {}".format(paperType, len(high_influence_paper['citations'])))
    target_set = set([(r['paperId'], r['title']) for r in high_influence_paper['references'] if (r['paperId'] or r['title'])])
    len_target_set = len(target_set)
    if len_target_set == 0:
        print('1')
        exit(1)
    else:
        print("{} paper has {} references".format(paperType, len_target_set))

    with open('final_data_authors/{}/{}/{}.csv'.format(paperType, hIndexType, paperId), 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        header = ["citationID", "citationName", "citedReferences"]
        writer.writerow(header)
        for i in range(len(high_influence_paper['citations'])):
            citation = high_influence_paper['citations'][i]
            rsp = requests.get(
                'https://api.semanticscholar.org/graph/v1/paper/{}?fields=references'.format(citation['paperId']),
                headers={'x-api-key': S2_API_KEY})
            try:
                rsp.raise_for_status()
            except requests.exceptions.HTTPError as e:
                print("Error: " + str(e))
                continue

            results = rsp.json()
            if results['references']:
                citation_reference_set = set([(r['paperId'], r['title']) for r in results['references'] if (r['paperId'] or r['title'])])
                len_citation_reference_set = len(citation_reference_set)
                if len_citation_reference_set == 0:
                    continue
                # else:
                #     print("citation {} of high influence paper has {} references".format(i, len_citation_reference_set))

                intersection = citation_reference_set.intersection(target_set)
                len_intersection = len(intersection)
                if len_intersection > 0:
                    # print('')
                    # print(citation['title'])
                    # print("{} common citations:".format(len_intersection))
                    # for item in intersection:
                    #     print("  {}".format(item[0]))
                    #     print("  {}".format(item[1]))
                    writer.writerow([citation['paperId'], citation['title'], "$$@$$".join([x[0] if x[0] else x[1] for x in intersection])])
                # else:
                #     print("No common citations.")

            time.sleep(0.1)


if __name__ == '__main__':
    get_data("low_influence", "high_hIndex", "946eb33942e2c89287edf9bf1e7946e1309d4367")

