from data_processing import statistical_test_two_groups, plot_two_groups


if __name__ == '__main__':
    plot_two_groups("final_data_authors/high_influence/high_hIndex",
                    "final_data_authors/high_influence/low_hIndex", "promotion score")
    plot_two_groups("final_data_authors/low_influence/high_hIndex",
                    "final_data_authors/low_influence/low_hIndex", "promotion score")
    plot_two_groups("final_data_authors/retracted/high_hIndex/before_retraction",
                    "final_data_authors/retracted/high_hIndex/after_retraction", "promotion score")
    plot_two_groups("final_data_authors/retracted/low_hIndex/before_retraction",
                    "final_data_authors/retracted/low_hIndex/after_retraction", "promotion score")

    plot_two_groups("final_data_authors/high_influence/high_hIndex",
                    "final_data_authors/high_influence/low_hIndex", "promotion dispersion")
    plot_two_groups("final_data_authors/low_influence/high_hIndex",
                    "final_data_authors/low_influence/low_hIndex", "promotion dispersion")
    plot_two_groups("final_data_authors/retracted/high_hIndex/before_retraction",
                    "final_data_authors/retracted/high_hIndex/after_retraction", "promotion dispersion")
    plot_two_groups("final_data_authors/retracted/low_hIndex/before_retraction",
                    "final_data_authors/retracted/low_hIndex/after_retraction", "promotion dispersion")


    statistical_test_two_groups("final_data_authors/high_influence/high_hIndex",
                                "final_data_authors/high_influence/low_hIndex", "promotion score")
    statistical_test_two_groups("final_data_authors/low_influence/high_hIndex",
                                "final_data_authors/low_influence/low_hIndex", "promotion score")
    statistical_test_two_groups("final_data_authors/retracted/high_hIndex/before_retraction",
                                "final_data_authors/retracted/high_hIndex/after_retraction", "promotion score")
    statistical_test_two_groups("final_data_authors/retracted/low_hIndex/before_retraction",
                                "final_data_authors/retracted/low_hIndex/after_retraction", "promotion score")

    statistical_test_two_groups("final_data_authors/high_influence/high_hIndex",
                                "final_data_authors/high_influence/low_hIndex", "promotion dispersion")
    statistical_test_two_groups("final_data_authors/low_influence/high_hIndex",
                                "final_data_authors/low_influence/low_hIndex", "promotion dispersion")
    statistical_test_two_groups("final_data_authors/retracted/high_hIndex/before_retraction",
                                "final_data_authors/retracted/high_hIndex/after_retraction", "promotion dispersion")
    statistical_test_two_groups("final_data_authors/retracted/low_hIndex/before_retraction",
                                "final_data_authors/retracted/low_hIndex/after_retraction", "promotion dispersion")
