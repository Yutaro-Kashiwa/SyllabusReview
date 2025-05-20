import pandas as pd

# CSVファイルを読み込む
df = pd.read_csv("syllabus.csv", encoding="utf-8")
df = df.iloc[1:].reset_index(drop=True)
# 各列ごとの単語リスト（重複なし）を作成
column_words = {}

for col in df.columns:
    unique_words = set()

    for values in df[col].dropna():  # NaN値を除外
        values = str(values)
        words = values.replace("、", ",").replace("，", ",").split(",")  # 全角カンマを半角に置換して分割
        unique_words.update(word.strip() for word in words)  # 前後の空白を削除

    column_words[col] = list(unique_words)

# 新しいDataFrameを作成（ヘッダーを維持）
output_df = pd.DataFrame.from_dict(column_words, orient="index").transpose()
output_df = output_df.iloc[:, 10:]
# CSVファイルに書き出し（ヘッダーを残す）
output_df.to_csv("column_unique_words.csv", index=False, encoding="utf-8")

