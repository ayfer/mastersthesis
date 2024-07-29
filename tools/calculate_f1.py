# %%
from sklearn.metrics import f1_score
import pandas as pd
from loguru import logger
import argparse
import json


def load_categories(file_path: str) -> list:
    with open(file_path, "r") as file:
        categories = json.load(file)
    
    return categories.keys()

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
          '--output_filepath'
        , '-o'
        , required=True
        , help='The path to the Excel file to host the test results'
    )
    args = parser.parse_args()

    # get the arguments
    input_filepath = args.input_filepath
    output_filepath = args.output_filepath
    sheet_names = args.sheet_names

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

    CATEGORIES = load_categories("prompts/prompt_eng.json")
    f1_categories = {}

    for category in CATEGORIES:
        df_cat = df[df["Category"] == category.strip()] 
        y_true = df_cat["Intent"].apply(lambda x: x.strip()).to_list() 
        y_pred = df_cat["Recognized Intent"].astype(str).apply(lambda x: x.strip()).to_list()
        f1_categories[category] = round(float(f1_score(y_true, y_pred, average='micro')), 3)

    best_category = max(f1_categories.items(), key=lambda k: k[1])
    logger.info(f"Best category: {best_category[0]} with F1-Score: {best_category[1]}")

    with open(output_filepath, "w") as file:
        json.dump(f1_categories, file)


if __name__ == "__main__":
    main()  
# %%