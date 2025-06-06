import pandas as pd

from setting import large_cat_no

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
unique_words = set()
for col in df.columns:
    col_no += 1
    if col_no <= 10:
        continue

    for values in df[col].dropna():  # NaN値を除外
        values = str(values)
        words = values.replace("、", ",").replace("，", ",").split(",")  # 全角カンマを半角に置換して分割
        unique_words.update(word.strip() for word in words)  # 前後の空白を削除

    if (col_no-10) in large_cat_no:
        column_words[col] = sorted(list(unique_words))
        unique_words = set()

# 新しいDataFrameを作成（ヘッダーを維持）
output_df = pd.DataFrame.from_dict(column_words, orient="index").transpose()
# CSVファイルに書き出し（ヘッダーを残す）
output_df.to_csv("column_unique_words.csv", index=False, encoding="utf-8")

