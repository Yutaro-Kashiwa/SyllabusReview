import math
from collections import Counter

import pandas as pd
import statistics

from plot import plot_percentage_by_subject, plot_coverage_by_uni, plot_classes_by_uni
from setting import large_cat_no, start_no, end_no


def separate(values):
    return values.replace("、", ",").replace("，", ",").split(",")  # 全角カンマを半角に置換して分割



def make_classes_list_by_uni(df):
    col = df.iloc[1]
    df = df.iloc[2:].reset_index(drop=True)
    df.columns = col

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
        for col_no in range(start_no, end_no):
            values = str(row[col_no])
            if values == 'nan':
                pass
            else:
                words = separate(values)
                words_set = words_set.union(set(words))

            if col_no in large_cat_no:
                words_by_type[col_no] = words_set
                words_set = set()
        class_data["words"] = words_by_type
        classes_list_by_uni[uni_name].append(class_data)

    return classes_list_by_uni


def aggregate_words_by_category(classes_list_by_uni, cat):
    classes_list = {}
    for uni_name in classes_list_by_uni:
        class_data = classes_list_by_uni[uni_name]
        words_by_type = {}
        for col_no in cat:
            words_by_type[col_no] = set()
        for data in class_data:
            for idx in data["words"]:
                words_by_type[idx] = words_by_type[idx].union(data["words"][idx])
        classes_list[uni_name] = words_by_type
    return classes_list


def find_replacement(df, target_string):
    for index, row in df.iterrows():
        if target_string in row[1:].values:
            return row[0]
    return None


nayose_df = pd.read_csv("nayose.csv", encoding="utf-8", header=None)


def nayose(classes_list):
    for uni_name in classes_list:

        words_by_type = classes_list[uni_name]
        for type_no in words_by_type:
            new_words = set()
            words = words_by_type[type_no]
            for word in words:
                # 値2が含まれる行を抽出
                replacement = find_replacement(nayose_df, word)
                if replacement is not None:
                    new_words.add(replacement)
                else:
                    new_words.add(word)
            words_by_type[type_no] = new_words
        classes_list[uni_name] = words_by_type
    return classes_list


def normalize_and_summarize_keywords(keywords_list_by_uni):
    keywords_list_by_uni = nayose(keywords_list_by_uni)

    percentage = {}
    numbers = {}
    for uni_name in keywords_list_by_uni:
        # print(uni_name)
        bools = []
        freq = []
        for type_no in keywords_list_by_uni[uni_name]:
            # print("  ", type_no)
            # print("    ", keywords_list_by_uni[uni_name][type_no])
            keywords_num = len(keywords_list_by_uni[uni_name][type_no])
            if keywords_num > 0:
                bools.append(1)
            else:
                bools.append(0)
            freq.append(keywords_num)

        percentage[uni_name] = bools
        numbers[uni_name] = freq
    return percentage, numbers








def make_keywords_ranking(keywords_list_by_uni, uni_num):
    keywords_list_by_uni = nayose(keywords_list_by_uni)
    keyword_counter = {}
    for uni in keywords_list_by_uni:
        keywords_by_category = keywords_list_by_uni[uni]
        # print(uni)
        for category in keywords_by_category:
            print("  -", category, keywords_by_category[category])
            if category not in keyword_counter:
                counter = Counter(keywords_by_category[category])
            else:
                counter = keyword_counter[category]
                counter.update(keywords_by_category[category])
            keyword_counter[category] = counter

    rank = {1: [], 2: [], 3: [], 4: [], 5: []}
    for category in keyword_counter:
        counter = keyword_counter[category]
        # print("-", category)
        i = 0
        for word, num in counter.most_common(5):
            i+=1
            rank[i].append(word)
            # print(word)
            # print(word, f"({round(num/uni_num,2)})")

    for no in rank:
        keywords = rank[no]
        print(no,  "&", keywords[0], "&", keywords[1], "&", keywords[2], "&", keywords[3], "&", keywords[4], "&", keywords[5], "\\\\")
    print("")
    for no in rank:
        keywords = rank[no]
        print(keywords)
        print(no, "&", keywords[6], "&", keywords[7], "&", keywords[8], "&", keywords[9], "&", keywords[10], "&", keywords[11], "\\\\")
def calculate_cover_number(classes_list_by_uni):
    numbers = []
    for uni in classes_list_by_uni:
        d = classes_list_by_uni[uni]
        for category in d:
            i = 0
            for no in category['words']:
                if len(category['words'][no])>0:
                    i += 1
            numbers.append(i)
    print("Median of cover number: ", statistics.median(numbers))


if __name__ == "__main__":
    # CSVファイルを読み込む
    df = pd.read_csv("syllabus.csv", encoding="utf-8", header=None)
    classes_list_by_uni = make_classes_list_by_uni(df)

    calculate_cover_number(classes_list_by_uni)

    keywords_list_by_unu = aggregate_words_by_category(classes_list_by_uni, large_cat_no)

    bools, numbers = normalize_and_summarize_keywords(keywords_list_by_unu)

    # print(bools)
    # NaNキーを除外した新しい辞書を作成
    bools = {k: v for k, v in bools.items() if not isinstance(k, float) or not math.isnan(k)}
    numbers = {k: v for k, v in numbers.items() if not isinstance(k, float) or not math.isnan(k)}
    uni_num = len(bools)
    make_keywords_ranking(keywords_list_by_unu, uni_num)

    sub_num = 12
    print(bools)
    print(numbers)


    plot_percentage_by_subject(bools, uni_num)
    # plot_keywords_by_subject(numbers)
    plot_coverage_by_uni(bools)
