import RQ1, RQ2
from plot import plot_classes_by_uni
import pandas as pd
import pandas as pd
import numpy as np
from scipy.stats import mannwhitneyu
from cliffs_delta import cliffs_delta as cliffs_d
import pingouin as pg


def perform_statistical_analysis(classes_list_by_uni_domestic, classes_list_by_uni_foreign):
    """
    Perform Mann-Whitney U-tests and calculate Cliff's delta for comparing
    domestic and foreign university class counts using established libraries.
    """
    print("Statistical Analysis Results")
    print("=" * 50)

    # Extract class counts for each group
    domestic_counts = [len(classes) for classes in classes_list_by_uni_domestic.values()]
    foreign_counts = [len(classes) for classes in classes_list_by_uni_foreign.values()]

    print(f"Domestic universities: {len(domestic_counts)} universities")
    print(f"Foreign universities: {len(foreign_counts)} universities")
    print(f"Domestic class counts - Mean: {np.mean(domestic_counts):.2f}, Median: {np.median(domestic_counts):.2f}")
    print(f"Foreign class counts - Mean: {np.mean(foreign_counts):.2f}, Median: {np.median(foreign_counts):.2f}")
    print()

    if len(domestic_counts) > 0 and len(foreign_counts) > 0:
        # Method 1: Using scipy for Mann-Whitney U
        statistic, p_value = mannwhitneyu(domestic_counts, foreign_counts,
                                          alternative='two-sided')

        print("Mann-Whitney U-test Results (scipy):")
        print(f"U-statistic: {statistic}")
        print(f"p-value: {p_value:.6f}")

        # Method 2: Using pingouin for comprehensive analysis
        # Create dataframe for pingouin
        data_df = pd.DataFrame({
            'values': domestic_counts + foreign_counts,
            'group': ['domestic'] * len(domestic_counts) + ['foreign'] * len(foreign_counts)
        })

        # Mann-Whitney U using pingouin
        mwu_result = pg.mwu(domestic_counts, foreign_counts, alternative='two-sided')
        print("\nMann-Whitney U-test Results (pingouin):")
        print(mwu_result)

        # Interpret p-value
        alpha = 0.01
        if p_value < alpha:
            significance = f"statistically significant (p < {alpha})"
        else:
            significance = f"not statistically significant (p >= {alpha})"
        print(f"\nResult: {significance}")
        print()

        # Cliff's delta using the cliffs_delta library
        delta = cliffs_d(domestic_counts, foreign_counts)

        print("Cliff's Delta Results (cliffs_delta library):")
        print(f"Cliff's delta: {delta}")
        print()

        # Summary statistics using pingouin
        print("Descriptive Statistics (pingouin):")
        print("-" * 40)
        desc_stats = pg.describe(data_df, by='group')
        print(desc_stats)

    else:
        print("Error: One or both groups have no data for statistical analysis")
        return None

    return {
        'domestic_counts': domestic_counts,
        'foreign_counts': foreign_counts,
        'mann_whitney_u': statistic,
        'p_value': p_value,
        'cliffs_delta': delta,
        'effect_size': effect_size,
        'mwu_pingouin': mwu_result,
        'descriptive_stats': desc_stats
    }

if __name__ == "__main__":
    df_domestic = pd.read_csv("syllabus.csv", encoding="utf-8", header=None)
    classes_list_by_uni_domestic = RQ1.make_classes_list_by_uni(df_domestic)

    df_foreign = pd.read_csv("syllabus_foreign.csv", encoding="utf-8", header=0)
    classes_list_by_uni_foreign = RQ2.make_classes_list_by_uni(df_foreign)

    results = perform_statistical_analysis(classes_list_by_uni_domestic, classes_list_by_uni_foreign)

    plot_classes_by_uni(classes_list_by_uni_domestic, classes_list_by_uni_foreign)