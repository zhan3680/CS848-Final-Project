import requests
import time
import csv
import os

S2_API_KEY = "K0YJzhxZI15eLBiS7zAUz1n1QgobRC3O4yXkPnIt"


def create_csv_file(paperId, hIndexType, retractionType, citations, target_set):
    citationCount = len(citations)

    directory_path = "final_data_authors/retracted/{}/{}/".format(hIndexType, retractionType)
    with open(os.path.join(directory_path, "{}.csv".format(paperId)), "w", encoding="UTF8", newline="", ) as f:
        writer = csv.writer(f)
        header = ["citationID", "citationName", "citedReferences"]
        writer.writerow(header)

        for i in range(len(citations)):
            citation = citations[i]
            rsp = requests.get(
                "https://api.semanticscholar.org/graph/v1/paper/{}?fields=references".format(
                    citation["paperId"]
                ),
                headers={"x-api-key": S2_API_KEY},
            )
            try:
                rsp.raise_for_status()
            except requests.exceptions.HTTPError as e:
                print("Error: " + str(e))
                citationCount -= 1
                continue

            results = rsp.json()
            if results["references"]:
                citation_reference_set = set([(r["paperId"], r["title"])
                                              for r in results["references"] if (r["paperId"] or r["title"])])
                len_citation_reference_set = len(citation_reference_set)
                if len_citation_reference_set == 0:
                    continue

                intersection = citation_reference_set.intersection(target_set)
                len_intersection = len(intersection)
                if len_intersection > 0:
                    writer.writerow(
                        [
                            citation["paperId"],
                            citation["title"],
                            "$$@$$".join([x[0] if x[0] else x[1] for x in intersection]),
                        ]
                    )

            time.sleep(0.1)
    return citationCount


def get_data(paperId, hIndexType, retraction_date):
    rsp = requests.get("https://api.semanticscholar.org/graph/v1/paper/{}?"
                       "fields=url,citations,references,"
                       "citations.publicationDate,citations.title".format(paperId),
                       headers={"x-api-key": S2_API_KEY})
    rsp.raise_for_status()
    high_influence_paper = rsp.json()
    citations_before_retraction = []
    citations_after_retraction = []
    target_set = set([(r["paperId"], r["title"])
                      for r in high_influence_paper["references"] if (r["paperId"] or r["title"])])
    len_target_set = len(target_set)
    if len_target_set == 0:
        print("1")
        exit(1)
    else:
        print("paper has {} references".format(len_target_set))

    for i in range(len(high_influence_paper["citations"])):
        citation = high_influence_paper["citations"][i]
        citation_date = citation["publicationDate"]

        if citation_date is not None:
            if citation_date < retraction_date:
                citations_before_retraction.append(citation)
            else:
                citations_after_retraction.append(citation)

    before_count = create_csv_file(paperId, hIndexType, "before_retraction", citations_before_retraction, target_set)
    after_count = create_csv_file(paperId, hIndexType, "after_retraction", citations_after_retraction, target_set)

    print(
        "There are {} citations before retraction and {} citations after retraction".format(before_count, after_count))


if __name__ == '__main__':
    get_data("35751010cf4b09552ed4c85b5a1367f96db2641f", "low_hIndex", "2020-04-22")  # YYYY-MM-DD
