from sklearn.metrics import confusion_matrix, accuracy_score, ConfusionMatrixDisplay
import pandas as pd
import matplotlib.pyplot as plt
from loguru import logger
import argparse
import json
import os


def load_categories(file_path: str) -> list:
    with open(file_path, "r") as file:
        categories = json.load(file)
    
    return list(categories.keys())

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
        , help='The name(s) of the sheet(s) hosting the queries to be testet'
    )
    parser.add_argument(
          '--output_directory'
        , '-o'
        , required=True
        , help='The directory to host the confusion matrix images'
    )
    args = parser.parse_args()

    # get the arguments
    input_filepath = args.input_filepath
    output_directory = args.output_directory
    sheet_names = args.sheet_names

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

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

    overall_y_true = []
    overall_y_pred = []

    for category in CATEGORIES:
        df_cat = df[df["Category"] == category.strip()]
        y_true = df_cat["Intent"].apply(lambda x: x.strip()).to_list()
        y_pred = df_cat["Recognized Intent"].apply(lambda x: x.strip()).to_list()
        
        overall_y_true.extend(y_true)
        overall_y_pred.extend(y_pred)
        
        cm = confusion_matrix(y_true, y_pred, labels=df_cat["Intent"].unique(), normalize='true')
        fig, ax = plt.subplots(figsize=(5, 5))
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=df_cat["Intent"].unique())

        accuracy = accuracy_score(y_true, y_pred) 
        
        disp.plot(cmap=plt.cm.Greys, ax=ax, colorbar=False)
        plt.title(f'Accuracy({category})={accuracy:.3f}', fontsize=10)
        plt.xlabel('Recognized Intent', fontsize=10)  
        plt.ylabel('Intent', fontsize=10) 
        plt.xticks(rotation=45, ha='right', fontsize=8)  
        plt.yticks(fontsize=8)
        plt.tight_layout()
        plt.savefig(os.path.join(output_directory, f'confusion_matrix_{category}.png'))
        plt.close()

    # Gesamt-Konfusionsmatrix erstellen
    overall_cm = confusion_matrix(overall_y_true, overall_y_pred, labels=df["Intent"].unique(), normalize='true')
    fig, ax = plt.subplots(figsize=(5, 5))
    overall_disp = ConfusionMatrixDisplay(confusion_matrix=overall_cm, display_labels=df["Intent"].unique())

    overall_disp.plot(cmap=plt.cm.Greys, ax=ax, colorbar=False)
    plt.title('Overall Confusion Matrix', fontsize=10)
    plt.xlabel('Recognized Intent', fontsize=10)  
    plt.ylabel('Intent', fontsize=10) 
    plt.xticks(rotation=45, ha='right', fontsize=8)  
    plt.yticks(fontsize=8)
    plt.tight_layout()
    plt.savefig(os.path.join(output_directory, 'overall_confusion_matrix.png'))
    plt.close()

    logger.info(f"Confusion matrices saved in {output_directory}")


if __name__ == "__main__":
    main()
    plt.close('all')
