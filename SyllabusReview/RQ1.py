import math

import pandas as pd

from setting import large_cat_no, start_no, end_no

# CSVファイルを読み込む
df = pd.read_csv("syllabus.csv", encoding="utf-8",header=None)

col = df.iloc[1]
df = df.iloc[2:].reset_index(drop=True)
df.columns = col

df = df[df["対象"].isna()]
# 各列ごとの単語リスト（重複なし）を作成
column_words = {}
stop = []
col_no = -1

classes_list_by_uni = {}

for index, row in df.iterrows():
    class_data = {}
    uni_name = row[2]
    class_name = row[4]
    class_data["uni_name"] = uni_name
    class_data["class_name"] = class_name
    words_set = set()
    words_by_type = {}

    if uni_name is not classes_list_by_uni:
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

def find_replacement(df, target_string):
    for index, row in df.iterrows():
        if target_string in row[1:].values:
            return row[0]
    return None

nayose_df = pd.read_csv("nayose.csv", encoding="utf-8", header=None)

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

percentage = {}
numbers = {}
for uni_name in classes_list:
    bools = []
    keywords = []
    for type_no in classes_list[uni_name]:
        keywords_num = len(classes_list[uni_name][type_no])
        if keywords_num > 0:
            bools.append(True)
        else:
            bools.append(False)
        keywords.append(keywords_num)


    percentage[uni_name] = bools
    numbers[uni_name] = keywords

# NaNキーを除外した新しい辞書を作成
percentage = {k: v for k, v in percentage.items() if not isinstance(k, float) or not math.isnan(k)}
numbers = {k: v for k, v in numbers.items() if not isinstance(k, float) or not math.isnan(k)}
print(percentage)
print(numbers)


# 各インデックス位置のTrueの数をカウント
true_counts = [0] * 12
for values in percentage.values():
    for i, value in enumerate(values):
        if value:
            true_counts[i] += 1


import matplotlib.pyplot as plt
# 棒グラフの描画
plt.figure(figsize=(10, 6))
plt.bar(range(12), true_counts, color='skyblue')
plt.xlabel('Index')
plt.ylabel('Count of True')
plt.title('Count of True values at each index')
plt.xticks(range(12))
plt.grid(axis='y')
plt.show()
