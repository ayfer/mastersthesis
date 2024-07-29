import argparse
import asyncio
#from curses.ascii import DEL
import sys
import time
from click import prompt
import pandas as pd
import os.path
import json
#from openai import AzureOpenAI

from loguru import logger
from typing import Dict, List
from models import get_model_handler


def load_intents(directory: str):
    intents = []
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                intents.append(json.load(file))
    return intents

def load_prompts(path: str) -> dict:
    with open(path, "r") as file:
        prompts = json.load(file)
    return prompts

def load_config(path: str) -> dict:
    with open(path, "r") as file:
        config = json.load(file)
    return config

MAX_RETRIES = 15
DELAY = 5

async def process_queries(
          df_dict: Dict[str, pd.DataFrame]
        , intents: List[str]
        , model_handler
        , temp: float=0.0
        , prompts_path: str="prompts.json"
    ) -> Dict[str, pd.DataFrame]:

    prompts = load_prompts(path=prompts_path)
    all_results: Dict[str, pd.DataFrame] = {}
    
    for category, prompt in prompts.items():

        intents = list(df_dict)
        for intent in intents:
            recognized_intents: List[str] = []
            durations: List[float] = []
            queries = df_dict[intent]['Query']
            for query in queries:
                retries = 0
                while retries < MAX_RETRIES:
                    try:
                        logger.info(f'Requesting intent recognition for "{query}" of the {intent} intent.')
                        start_time = time.monotonic()
                        recognized_intent = model_handler.get_response(prompt, intent, query, temp)
                        end_time = time.monotonic()
                        recognized_intents.append(recognized_intent)
                        durations.append(end_time - start_time)
                        logger.info(f'Prompt: {prompt}')
                        logger.info(f'Recognized intent: {recognized_intent}')
                        break  # If the request is successful, break the loop
                    except Exception as e:  # If an error occurs, log it and retry the request
                        logger.error(f'Error while requesting intent recognition: {e}')
                        retries += 1  
                        if retries < MAX_RETRIES:  
                            logger.info(f'Retrying in {DELAY} seconds...')
                            await asyncio.sleep(DELAY)  
                        else:
                            logger.error(f'Max retries reached for query "{query}". Skipping...')
                            recognized_intents.append(None) 
                            durations.append(None)  
                            break 
                
                

            #category = "_".join(category.split("_")[:2])
            if intent not in all_results.keys():
                all_results[intent] = pd.DataFrame(
                    {   'Category': category,
                        'Query': queries,
                        'Recognized Intent': recognized_intents,
                        'Duration': durations,
                    }
                    )
                
            else:
                new_df = pd.DataFrame(
                    {   'Category': category,
                        'Query': queries,
                        'Recognized Intent': recognized_intents,
                        'Duration': durations,
                    }
                    )
                
                all_results[intent] = pd.concat([all_results[intent], new_df], axis=0)


    return all_results

async def main():
    # parse the command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--intents_directory'
        , '-d'
        , required=True
        , help='The directory containing JSON intent files'
    )
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
        , help='The path to the Excel file to host the test results'
    )
    parser.add_argument(
        '--model'
        , '-m'
        , required=True
        , help='The model to be used, e.g., openai_gpt3.5, openai_gpt4, llama3'
    )
    parser.add_argument(
        '--prompts_path'
        , '-pp'
        , required=False
        , default='prompts.json'
        , help='The path to the JSON file containing the prompts'
    )
    args = parser.parse_args()

    # get the arguments
    input_filepath = args.input_filepath
    output_filepath = args.output_filepath
    sheet_names = args.sheet_names
    model_name = args.model

    config = load_config(path="config.json")
    model_config = config.get(model_name)

    if not model_config:
        logger.error(f'Model {model_name} not found in the configuration.')
        sys.exit(1)

    model_handler = get_model_handler(
        model_name=model_name,
        model_config=model_config
    )

    # logger.info(f'Reading test queries from {input_filepath}.')
    try:
        xls = pd.ExcelFile(input_filepath)
    except Exception as e:
        logger.error(f'Error reading the queries from {input_filepath}: {e}')
        sys.exit(str(e))

    if sheet_names == []:
        sheet_names = xls.sheet_names

    df_dict: Dict[str, pd.DataFrame] = {}
    for sheet_name in [s for s in xls.sheet_names if s in sheet_names]:
        try:
            df_dict[str(sheet_name)] = xls.parse(sheet_name)
        except Exception as e:
            logger.error(f'Error parsing sheet "{sheet_name}": {e}.')
            sys.exit(str(e))

    results_dict = await process_queries(
          df_dict
        , load_intents(args.intents_directory)
        , model_handler
        , prompts_path=args.prompts_path
    )
    logger.info(f'Writing test results to {output_filepath}.')
    if os.path.isfile(output_filepath):
        with pd.ExcelWriter(
              output_filepath
            , mode='a') as writer:
            for df_name, df in results_dict.items():
                try:
                    df.to_excel(
                          writer
                        , index=False
                        , sheet_name=df_name
                    )
                except ValueError:
                    sheet_names = writer.book.sheetnames
                    i = 1
                    while df_name + str(i) in sheet_names:
                        i += 1
                    df.to_excel(
                          writer
                        , index=False
                        , sheet_name=df_name + str(i)
                    )
    else:
        with pd.ExcelWriter(output_filepath) as writer:
            for df_name, df in results_dict.items():
                df.to_excel(
                      writer
                    , index=False
                    , sheet_name=df_name
                )

if __name__ == "__main__":
    asyncio.run(main())