import seaborn as sns
import matplotlib.pyplot as plt

from setting import fontsize
import pandas as pd


def plot_percentage_by_subject(bools, uni_num, suffix=""):
    # サブジェクトごとの割合の棒グラフ
    # 各列の合計を格納するリストを初期化
    column_sums = [0] * len(next(iter(bools.values())))
    # 各大学のデータを列ごとに加算
    for values in bools.values():
        for i, value in enumerate(values):
            column_sums[i] += value
    # 45で割ってパーセントに変換
    percentage_data = [(x / uni_num) * 100 for x in column_sums]

    # plt.rcParams['font.family'] = 'IPAexGothic'

    # グラフの描画
    sns.set(style="darkgrid")
    # sns.set(style="ticks", color_codes=True)
    plt.figure(figsize=(10, 6))
    barplot = sns.barplot(x=list(range(1, len(percentage_data) + 1)), y=percentage_data, color='skyblue')

    barplot.set_xticklabels(['Requirement','Architecture ','Design','Construction','Testing','Operation','Maintenance',
                             'Configuration','Management','Process','Models','Quality'],
                            rotation=90, fontsize=fontsize-5,)

    # ラベルとタイトル
    # plt.xlabel('Column Index', fontsize=fontsize)
    plt.ylabel('Percentage (%)', fontsize=fontsize)
    # plt.title('Percentage of Each Column Value (Divided by 45)')
    plt.ylim(0, 100)
    plt.xticks(fontsize=fontsize)
    plt.yticks(fontsize=fontsize)
    plt.tight_layout()
    # グラフを表示
    plt.savefig(f"outputs/percentage_by_subject{suffix}.pdf")
    print("saved: percentage_by_subject.pdf")


def plot_keywords_by_subject(keywords_data, suffix=""):
    # データを整形して、0を除外し、長形式に変換
    long_data = []
    for uni, counts in keywords_data.items():
        for idx, count in enumerate(counts):
            if count != 0:
                long_data.append({'University': uni, 'Subject Index': idx, 'Keyword Count': count})

    # データフレームに変換
    ddd = pd.DataFrame(long_data)
    sns.set(style="darkgrid")

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
    plt.savefig(f"outputs/keywords_by_subject_{suffix}.pdf")
    print("saved: keywords_by_subject.pdf")
    pass


def plot_coverage_by_uni(bools, suffix="", color=None):
    # 各大学ごとの1の割合を計算
    proportions = {uni: sum(counts) / len(counts) for uni, counts in bools.items()}
    print(proportions)
    # データフレームに変換
    ddd = pd.DataFrame(list(proportions.items()), columns=['University', 'Coverage'])


    print("median coverage", ddd['Coverage'].median())
    print("q1", ddd['Coverage'].quantile(0.25))
    print("q3", ddd['Coverage'].quantile(0.75))
    print("all classes", len(ddd))
    print("less than 50%",len(ddd[ddd['Coverage'] < 0.50]))
    print("per of 50%",len(ddd[ddd['Coverage'] < 0.50])/len(ddd))
    print("min", ddd['Coverage'].quantile(0))

    sns.set(style="darkgrid")
    # 箱ひげ図の描画
    plt.figure(figsize=(12, 8))
    sns.violinplot(y='Coverage', data=ddd, color=color)
    plt.grid(False)
    plt.xticks(fontsize=fontsize)
    plt.yticks(fontsize=fontsize)
    plt.ylim(0, 1)
    # plt.xlabel('Proportion of 1s')
    plt.ylabel('Coverage', fontsize=fontsize)
    # plt.title('Boxplot of Proportion of 1s for Each University')
    plt.yticks([i / 10 for i in range(0, 11)])  # Y軸を0.0〜1.0の範囲で整数ステップに近い表示
    plt.grid(True)
    plt.savefig(f"outputs/coverage_by_uni_{suffix}.pdf")

    pass


def plot_classes_by_uni(classes_list_by_uni_domestic, classes_list_by_uni_foreign):
    # 各大学の授業数をリストに変換
    sns.set(style="darkgrid")
    class_counts_domestic = [len(classes) for classes in classes_list_by_uni_domestic.values()]
    class_counts_foreign = [len(classes) for classes in classes_list_by_uni_foreign.values()]

    dd1 = pd.DataFrame(class_counts_domestic, columns=['classes'])
    dd1['domestic/foreign'] = 'Domestic'
    dd2 = pd.DataFrame(class_counts_foreign, columns=['classes'])
    dd2['domestic/foreign'] = 'Foreign'

    print("Domestic")
    print("median classes", dd1['classes'].median())
    print("q1", dd1['classes'].quantile(0.25))
    print("q3", dd1['classes'].quantile(0.75))
    print("Foreign")
    print("median classes", dd2['classes'].median())
    print("q1", dd2['classes'].quantile(0.25))
    print("q3", dd2['classes'].quantile(0.75))




    dd = pd.concat([dd1, dd2])
    # バイオリンプロットの作成
    plt.figure(figsize=(10, 6))
    sns.violinplot(data=dd,  y='classes', hue='domestic/foreign', split=True, inner="box")
    plt.xticks(fontsize=fontsize)
    plt.yticks(fontsize=fontsize)
    plt.ylabel('Number of Classes', fontsize=fontsize)
    # plt.xticks(range(len(classes_list_by_uni)), classes_list_by_uni.keys())
    plt.grid(True)
    plt.savefig(f"outputs/classes_comparison.pdf")

    # プロットの表示
    plt.show()

