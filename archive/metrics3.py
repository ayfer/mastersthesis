import numpy as np
import pandas as pd
import argparse
import json
from collections import defaultdict
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score, accuracy_score, matthews_corrcoef

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
          '--input_filepath'
        , '-i'
        , required=True
        , help='The path to the Excel file containing the test queries'
    )
    parser.add_argument(
          '--sheet_names'
        , '-s'
        , nargs='+'
        , required=False
        , default=[]
        , help='The name(s) of the sheet(s) hosting the queries to be tested'
    )
    parser.add_argument(
          '--output_filepath'
        , '-o'
        , required=False
        , help='The path to the file to host the test results'
    )
    parser.add_argument(
          '--metric'
        , '-m'
        , required=False
        , choices=['f1', 'mcc', 'a', 'p', 'r', None]
        , help='The metric to be calculated: "f1" for F1-Score, "mcc" for Matthews Correlation Coefficient, "a" for Accuracy, "p" for Precision, "r" for Recall. If not specified, all metrics will be calculated.'
    )
    args = parser.parse_args()

    # get the arguments
    input_filepath = args.input_filepath
    output_filepath = args.output_filepath
    sheet_names = args.sheet_names
    metric = args.metric

    xls = pd.ExcelFile(input_filepath)
    true_labels = xls.sheet_names
    print(true_labels)

    results = defaultdict(lambda: defaultdict(dict))
    category_totals = defaultdict(lambda: [0, 0, 0, 0])  # TP, TN, FP, FN
    f1_scores = {}

    for sheet in true_labels:
        df = xls.parse(sheet)
        df['Recognized Intent'] = df['Recognized Intent'].str.strip()
        df['Category'] = df['Category'].astype(str)

        for category, group in df.groupby('Category'):
            true_labels_category = group['Recognized Intent'] == sheet
            tp = true_labels_category.sum()
            fp = (~true_labels_category & group['Recognized Intent'].isin(true_labels)).sum()
            fn = (~true_labels_category & ~group['Recognized Intent'].isin(true_labels)).sum()
            tn = len(group) - tp - fp - fn

            results[sheet][category] = (tp, tn, fp, fn)
            category_totals[category][0] += tp
            category_totals[category][1] += tn
            category_totals[category][2] += fp
            category_totals[category][3] += fn

    # Calculate F1 scores for each category
    for category in category_totals:
        tp, tn, fp, fn = category_totals[category]
        precision = tp / (tp + fp) if tp + fp > 0 else 0
        recall = tp / (tp + fn) if tp + fn > 0 else 0
        f1_scores[category] = 2 * (precision * recall) / (precision + recall) if precision + recall > 0 else 0
        print(f'Total - Category: {category}, TP: {tp}, TN: {tn}, FP: {fp}, FN: {fn}, F1: {f1_scores[category]:.2f}')

    # Calculate macro-average metrics
    all_precisions = []
    all_recalls = []
    all_f1s = []
    for category in category_totals:
        tp, tn, fp, fn = category_totals[category]
        precision = tp / (tp + fp) if tp + fp > 0 else 0
        recall = tp / (tp + fn) if tp + fn > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if precision + recall > 0 else 0
        all_precisions.append(precision)
        all_recalls.append(recall)
        all_f1s.append(f1)

    macro_avg_precision = np.mean(all_precisions)
    macro_avg_recall = np.mean(all_recalls)
    macro_avg_f1 = np.mean(all_f1s)

    print(f'Macro Average Precision: {macro_avg_precision:.2f}')
    print(f'Macro Average Recall: {macro_avg_recall:.2f}')
    print(f'Macro Average F1: {macro_avg_f1:.2f}')

    if output_filepath:
        with open(output_filepath, "w") as file:
            json.dump({
                'results': results,
                'category_totals': category_totals,
                'f1_scores': f1_scores,
                'macro_avg_precision': macro_avg_precision,
                'macro_avg_recall': macro_avg_recall,
                'macro_avg_f1': macro_avg_f1
            }, file)

if __name__ == "__main__":
    main()
