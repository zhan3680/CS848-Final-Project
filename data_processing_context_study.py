import matplotlib.pyplot as plt

def plot(x, y, x_label):
    input = sorted([(x[i], y[i]) for i in range(len(x))])
    x_vals = [item[0] for item in input]
    y_vals = [item[1] for item in input]
    plt.figure()
    plt.plot(x_vals, y_vals)
    # plt.yscale('log')
    # plt.xticks(rotation=30, ha='right')
    plt.xlabel(x_label)
    plt.ylabel('level of matching')
    plt.show()


if __name__ == '__main__':
    level_of_matching = [0/1, 1/2, 1/3, 3/4, 3/5, 6/6, 3/7, 6/8, 8/11, 7/12, 19/21, 22/22, 14/19, 21/25, 12/15]
    level_of_matching_2 = [0*0/1, 1*1/2, 1*1/3, 3*3/4, 3*3/5, 6*6/6, 3*3/7, 6*6/8, 8*8/11, 7*7/12, 19*19/21, 22*22/22, 14*14/19, 21*21/25, 12/15]
    level_of_matching_3 = [0, 1, 1, 3, 3, 6, 3, 6, 8, 7, 19, 22, 14, 21, 12]
    first_author_hindex = [18, 9, 9, 14, 3, 4, 91, 45, 3, 4, 11, 4, 25, 35, 1]
    num_cited_references = [1, 2, 3, 4, 5, 6, 7, 8, 11, 12, 21, 22, 19, 25, 15]
    two_factor = [first_author_hindex[i]+num_cited_references[i] for i in range(len(first_author_hindex))]
    plot(num_cited_references, level_of_matching_3, "target")