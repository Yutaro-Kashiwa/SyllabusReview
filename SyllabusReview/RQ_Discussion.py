import RQ1, RQ2
from plot import plot_classes_by_uni
import pandas as pd

if __name__ == "__main__":
    df_domestic = pd.read_csv("syllabus.csv", encoding="utf-8", header=None)
    classes_list_by_uni_domestic = RQ1.make_classes_list_by_uni(df_domestic)

    df_foreign = pd.read_csv("syllabus_foreign.csv", encoding="utf-8", header=0)
    classes_list_by_uni_foreign = RQ2.make_classes_list_by_uni(df_foreign)


    plot_classes_by_uni(classes_list_by_uni_domestic, classes_list_by_uni_foreign)