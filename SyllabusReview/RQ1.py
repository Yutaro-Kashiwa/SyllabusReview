import math
from collections import Counter

import pandas as pd

from setting import large_cat_no, start_no, end_no, fontsize
import seaborn as sns
import matplotlib.pyplot as plt


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
                words = values.replace("、", ",").replace("，", ",").split(",")  # 全角カンマを半角に置換して分割
                words_set = words_set.union(set(words))

            if col_no in large_cat_no:
                words_by_type[col_no] = words_set
                words_set = set()
        class_data["words"] = words_by_type
        classes_list_by_uni[uni_name].append(class_data)

    return classes_list_by_uni


def aggregate_words_by_category(classes_list_by_uni):
    classes_list = {}
    for uni_name in classes_list_by_uni:
        class_data = classes_list_by_uni[uni_name]
        words_by_type = {}
        for col_no in large_cat_no:
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


def plot_percentage_by_subject(bools, uni_num):
    # サブジェクトごとの割合の棒グラフ
    # 各列の合計を格納するリストを初期化
    column_sums = [0] * len(next(iter(bools.values())))
    # 各大学のデータを列ごとに加算
    for values in bools.values():
        print(values)
        for i, value in enumerate(values):
            column_sums[i] += value
    # 45で割ってパーセントに変換
    percentage_data = [(x / uni_num) * 100 for x in column_sums]

    # グラフの描画
    plt.figure(figsize=(10, 6))
    sns.barplot(x=list(range(1, len(percentage_data) + 1)), y=percentage_data)

    # ラベルとタイトル
    plt.xlabel('Column Index', fontsize=fontsize)
    plt.ylabel('Percentage (%)', fontsize=fontsize)
    # plt.title('Percentage of Each Column Value (Divided by 45)')
    plt.ylim(0, 100)
    plt.xticks(fontsize=fontsize)
    plt.yticks(fontsize=fontsize)
    # グラフを表示
    plt.savefig("outputs/percentage_by_subject.pdf")
    print("saved: percentage_by_subject.pdf")


def plot_keywords_by_subject(keywords_data):
    # データを整形して、0を除外し、長形式に変換
    long_data = []
    for uni, counts in keywords_data.items():
        for idx, count in enumerate(counts):
            if count != 0:
                long_data.append({'University': uni, 'Subject Index': idx, 'Keyword Count': count})

    # データフレームに変換
    ddd = pd.DataFrame(long_data)

    # 箱ひげ図の描画
    plt.figure(figsize=(12, 8))
    sns.boxplot(x='Subject Index', y='Keyword Count', data=ddd)
    plt.xlabel('Subjects', fontsize=fontsize)
    # 1. Software Requirements	2. Software Architecture	3. Software Design	4. Software Construction	5. Software Testing	6. Software Engineering Operations	8. Software Configuration Management	7. Software Maintenance	9. Software Engineering Management	10. Software Engineering Process	11. Software Engineering Models and Methods	12. Software Quality
    plt.ylabel('Number of Keywords', fontsize=fontsize)
    plt.xticks(fontsize=fontsize)
    plt.yticks(fontsize=fontsize)
    plt.yticks(range(0, ddd['Keyword Count'].max() + 1))  # Y軸を整数に
    plt.grid(True)
    plt.savefig("outputs/keywords_by_subject.pdf")
    print("saved: keywords_by_subject.pdf")
    pass


def plot_coverage_by_uni(bools):
    # 各大学ごとの1の割合を計算
    proportions = {uni: sum(counts) / len(counts) for uni, counts in bools.items()}

    # データフレームに変換
    ddd = pd.DataFrame(list(proportions.items()), columns=['University', 'Coverage'])
    sns.set_style('white')
    # 箱ひげ図の描画
    plt.figure(figsize=(12, 8))
    sns.violinplot(y='Coverage', data=ddd)
    plt.grid(False)
    plt.xticks(fontsize=fontsize)
    plt.yticks(fontsize=fontsize)
    plt.ylim(0, 1)
    # plt.xlabel('Proportion of 1s')
    plt.ylabel('Coverage', fontsize=fontsize)
    # plt.title('Boxplot of Proportion of 1s for Each University')
    plt.yticks([i / 10 for i in range(0, 11)])  # Y軸を0.0〜1.0の範囲で整数ステップに近い表示
    plt.grid(True)
    plt.savefig("outputs/coverage_by_uni.pdf")

    pass


# CSVファイルを読み込む
df = pd.read_csv("syllabus.csv", encoding="utf-8", header=None)
classes_list_by_uni = make_classes_list_by_uni(df)
keywords_list_by_unu = aggregate_words_by_category(classes_list_by_uni)


def make_keywords_ranking(keywords_list_by_uni, uni_num):
    keywords_list_by_uni = nayose(keywords_list_by_uni)
    keyword_counter = {}
    for uni in keywords_list_by_uni:
        keywords_by_category = keywords_list_by_uni[uni]
        for category in keywords_by_category:
            if category not in keyword_counter:
                counter = Counter(keywords_by_category[category])
            else:
                counter = keyword_counter[category]
                counter.update(keywords_by_category[category])
            keyword_counter[category] = counter

    rank = {1: [], 2: [], 3: [], 4: [], 5: []}
    for category in keyword_counter:
        counter = keyword_counter[category]
        print("-", category)
        i = 0
        for word, num in counter.most_common(5):
            i+=1
            rank[i].append(word)
            print(word)
            # print(word, f"({round(num/uni_num,2)})")

    for no in rank:
        keywords = rank[no]
        print(no,  "&", keywords[0], "&", keywords[1], "&", keywords[2], "&", keywords[3], "&", keywords[4], "&", keywords[5], "\\")

    for no in rank:
        keywords = rank[no]
        print(no, "&", keywords[6], "&", keywords[7], "&", keywords[8], "&", keywords[9], "&", keywords[10], "&", keywords[11], "\\")


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

# TODO: BUGFIX
plot_percentage_by_subject(bools, uni_num)
plot_keywords_by_subject(numbers)
plot_coverage_by_uni(bools)
