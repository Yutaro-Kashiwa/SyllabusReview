import math

import pandas as pd

from RQ1 import separate, make_keywords_ranking, normalize_and_summarize_keywords, aggregate_words_by_category, \
    calculate_cover_number
from plot import plot_percentage_by_subject, plot_coverage_by_uni
from setting import large_cat_no, large_cat_no_foreign


def make_classes_list_by_uni(df):
    # col = df.iloc[1]
    # df = df.iloc[2:].reset_index(drop=True)
    # df.columns = col
    df = df[df["対象"].isna()]
    # 各列ごとの単語リスト（重複なし）を作
    classes_list_by_uni = {}

    for index, row in df.iterrows():
        class_data = {}
        uni_name = row[2]
        class_name = row[4]
        class_data["uni_name"] = uni_name
        class_data["class_name"] = class_name
        words_set = set()
        words_by_type = {}
        if not uni_name in classes_list_by_uni:
            classes_list_by_uni[uni_name] = []
        for col_no in range(10, 22):
            values = str(row[col_no])
            if values == 'nan':
                pass
            else:
                words = separate(values)
                words_set = words_set.union(set(words))

            if col_no in large_cat_no_foreign:
                words_by_type[col_no] = words_set
                words_set = set()
        class_data["words"] = words_by_type
        classes_list_by_uni[uni_name].append(class_data)

    return classes_list_by_uni


if __name__ == "__main__":
    df = pd.read_csv("syllabus_foreign.csv", encoding="utf-8", header=0)

    classes_list_by_uni = make_classes_list_by_uni(df)
    calculate_cover_number(classes_list_by_uni)

    keywords_list_by_unu = aggregate_words_by_category(classes_list_by_uni, large_cat_no_foreign)

    bools, numbers = normalize_and_summarize_keywords(keywords_list_by_unu)

    # print(bools)
    # NaNキーを除外した新しい辞書を作成
    bools = {k: v for k, v in bools.items() if not isinstance(k, float) or not math.isnan(k)}
    numbers = {k: v for k, v in numbers.items() if not isinstance(k, float) or not math.isnan(k)}
    uni_num = len(bools)
    make_keywords_ranking(keywords_list_by_unu, uni_num)

    sub_num = 12
    import seaborn as sns

    plot_percentage_by_subject(bools, uni_num, "_foreign")
    # plot_keywords_by_subject(numbers, "foreign")
    plot_coverage_by_uni(bools, "_foreign", color=sns.color_palette(n_colors=2)[1])