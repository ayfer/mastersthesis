import argparse
import asyncio
import sys
import time
import pandas as pd
import os
import json
from openai import OpenAI

from loguru import logger
from typing import Dict, List
from models import GPT35Model, GPT4Model, Llama3Model, MixtralModel

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

async def process_queries(
          df_dict: Dict[str, pd.DataFrame]
        , intents: List[str]
        , temp: float=0.0
        , model_name: str = "gpt4"
    ) -> Dict[str, pd.DataFrame]:

    config = load_config('config.json')
    model_classes = {
        "gpt3.5": lambda: GPT35Model(config["gpt3.5"]["endpoint"], config["gpt3.5"]["api_key"], config["gpt3.5"]["deployment_name"]),
        "gpt4": lambda: GPT4Model(config["gpt4"]["endpoint"], config["gpt4"]["api_key"], config["gpt4"]["deployment_name"]),
        "llama3": lambda: Llama3Model(config["llama3"]["endpoint"], config["llama3"]["api_key"]),
        "mixtral": lambda: MixtralModel(config["mixtral"]["endpoint"], config["mixtral"]["api_key"], config["mixtral"]["model_name"])
    }
    
    model = model_classes[model_name]()

    prompts = load_prompts(path="prompts.json")
    all_results: Dict[str, pd.DataFrame] = {}
    
    for category, prompt in prompts.items():
        chat_prompt = prompt
        intents_list = list(df_dict)
        for intent in intents_list:
            recognized_intents: List[str] = []
            durations: List[float] = []
            queries = df_dict[intent]['Query']
            for query in queries:
                while True:
                    try:
                        logger.info(f'Requesting intent recognition for "{query}" of the {intent} intent.')
                        start_time = time.monotonic()
                        response = model.generate(
                            chat_prompt, intentsJson=intents, input=query
                        ).to_messages()
                        
                        recognized_intent = str(response.content)  # Convert recognized_intent to a string
                        end_time = time.monotonic()
                        recognized_intents.append(recognized_intent)
                        durations.append(end_time - start_time)
                        logger.info(f'Prompt: {prompt}')
                        logger.info(f'Recognized intent: {recognized_intent}')
                        break  # If the request is successful, break the loop
                    except ValueError as e:  # Catch the ValueError
                        logger.error(f'Error while requesting intent recognition: {e}')
                        continue  # If an error occurs, continue the loop to retry the request
                

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

def load_config(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

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
        '--model_name'
        , '-m'
        , required=True
        , choices=['gpt3.5', 'gpt4', 'llama3', 'mixtral']
        , help='The name of the model to use for intent recognition'
    )
    args = parser.parse_args()

    # get the arguments
    input_filepath = args.input_filepath
    output_filepath = args.output_filepath
    sheet_names = args.sheet_names
    model_name = args.model_name

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
