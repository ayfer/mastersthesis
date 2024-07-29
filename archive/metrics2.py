# %%
from sklearn.metrics import f1_score, matthews_corrcoef, accuracy_score, precision_score, recall_score
import pandas as pd
from loguru import logger
import argparse
import json


def load_categories(file_path: str) -> list:
    with open(file_path, "r") as file:
        categories = json.load(file)
    return categories.keys()

def load_labels(file_path: str) -> list:
    xls = pd.ExcelFile(file_path)
    labels = xls.sheet_names
    return labels

def calculate_f1_score(y_true, y_pred):
    return round(float(f1_score(y_true, y_pred, average='micro')), 3)

def calculate_mcc(y_true, y_pred):
    return round(float(matthews_corrcoef(y_true, y_pred)), 3)

def calculate_accuracy(y_true, y_pred):
    return round(float(accuracy_score(y_true, y_pred)), 3)

def calculate_precision(y_true, y_pred):
    return round(float(precision_score(y_true, y_pred, average='micro')), 3)

def calculate_recall(y_true, y_pred):
    return round(float(recall_score(y_true, y_pred, average='micro')), 3)

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
        , required=True
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
    labels = load_labels(input_filepath)
    output_filepath = args.output_filepath
    sheet_names = args.sheet_names
    metric = args.metric

    # logger.info(f'Reading test queries from {input_filepath}.')
    try:
        xls = pd.ExcelFile(input_filepath)
    except Exception as e:
        logger.error(f'Error reading the queries from {input_filepath}: {e}')
        exit(str(e))

    if sheet_names == []:
        sheet_names = xls.sheet_names

    for i, sheet_name in enumerate([s for s in xls.sheet_names if s in sheet_names]):
        try: 
            if i == 0:
                df = xls.parse(sheet_name)
                df["Intent"] = sheet_name
            else:
                new_df = xls.parse(sheet_name)
                new_df["Intent"] = sheet_name
                df = pd.concat([df, new_df], ignore_index=True)

        except Exception as e:
            logger.error(f'Error parsing sheet "{sheet_name}": {e}.')
            exit(str(e))

    CATEGORIES = load_categories("prompts.json")
    metrics_categories = {}

    for category in CATEGORIES:
        df_cat = df[df["Category"] == category.strip()] 
        y_true = df_cat["Intent"].apply(lambda x: x.strip()).to_list() 
        y_pred = df_cat["Recognized Intent"].apply(lambda x: x.strip()).to_list()

        if metric is None:
            metrics_categories[category] = {    
                'f1': calculate_f1_score(y_true, y_pred),
                'mcc': calculate_mcc(y_true, y_pred),
                'a': calculate_accuracy(y_true, y_pred),
                'p': calculate_precision(y_true, y_pred),
                'r': calculate_recall(y_true, y_pred)
            }
        else:
            if metric == 'f1':
                metrics_categories[category] = calculate_f1_score(y_true, y_pred)
            elif metric == 'mcc':
                metrics_categories[category] = calculate_mcc(y_true, y_pred)
            elif metric == 'a':
                metrics_categories[category] = calculate_accuracy(y_true, y_pred)
            elif metric == 'p':
                metrics_categories[category] = calculate_precision(y_true, y_pred)
            elif metric == 'r':
                metrics_categories[category] = calculate_recall(y_true, y_pred)

    #best_category = max(metrics_categories.items(), key=lambda k: k[1])
    #logger.info(f"Best category: {best_category[0]} with {metric.upper()}: {best_category[1]}")

    with open(output_filepath, "w") as file:
        json.dump(metrics_categories, file)


if __name__ == "__main__":
    main()
# %%
