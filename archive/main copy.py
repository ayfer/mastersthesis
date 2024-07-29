import argparse
import asyncio
import time
import pandas as pd
import os.path
import json

from langchain_core.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_openai import AzureChatOpenAI

from loguru import logger
from typing import Dict, List

OPENAI_API_VERSION = os.getenv("OPENAI_API_VERSION")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")

def load_intents(directory: str):
    intents = []
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                intents.append(json.load(file))
    return intents

ir_prompt_template: (str) = (""""Instruction": "The task is to figure out which is the intent of the input. If no match is found, 'Unknown' is to be used as the intent name.",
    "Context": "This list of intents with examples is given:[{intentsJson}]. It is either one of these five intents or 'Unknown'",
    "Input": "The input is a string {input}.",
    "Output": "Only the intent name or 'Unknown'.",
    "Examples":

            "Input": "I want to talk to a person",
            "Output": "GetHumanAssistance"
            "Input": "Hast du Optionsempfehlungen für mich?",
            "Output": "GetOptionRecommendation"
            "Input": "Wie wird das Wetter morgen?",
            "Output": "Unknown"
            "Input":  "Is a vehicle similar to my configuration in stock?",
            "Output": "GetStockAvailability"
            "Input":"Stelle meinen MINI für 33k fertig.",
            "Output":"GetPreConfiguration"
            "Input": "Beschleunigungswerte MINI Cooper SE",
            "Output": "GetTechnicalInformation"
    """)

async def process_queries(
          df_dict: Dict[str, pd.DataFrame]
        , intents: List[str]
        , temp: float=0.0
    ) -> Dict[str, pd.DataFrame]:

    chat = AzureChatOpenAI(
        azure_deployment="gpt-35-turbo-1106",
        temperature=temp,
        cache=False
    )
    system_message_prompt = SystemMessagePromptTemplate.from_template(ir_prompt_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt]
    )
    results: Dict[str, pd.DataFrame] = {}
    intents = list(df_dict)
    for intent in intents:
        recognized_intents: List[str] = []
        durations: List[float] = []
        queries = df_dict[intent]['Query']
        for query in queries:
            logger.info(f'Requesting intent recognition for "{query}" of the {intent} intent.')
            start_time = time.monotonic()
            response = chat.invoke(
                chat_prompt.format_prompt(
                    intentsJson=intents, input=query
                ).to_messages()
            )
            recognized_intent = response.content
            end_time = time.monotonic()
            recognized_intents.append(recognized_intent)
            durations.append(end_time - start_time)
            logger.info(f'Recognized intent: {recognized_intent}')
        results[intent] = pd.DataFrame(
            { 'Query': queries
            , 'Recognized Intent': recognized_intents
            , 'Duration': durations
            }
        )
    return results

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

    logger.info(f'Reading test queries from {input_filepath}.')
    try:
        xls = pd.ExcelFile(input_filepath)
    except Exception as e:
        logger.error(f'Error reading the queries from {input_filepath}: {e}')
        exit(e)

    if sheet_names == []:
        sheet_names = xls.sheet_names

    df_dict: Dict[str, pd.DataFrame] = {}
    for sheet_name in [s for s in xls.sheet_names if s in sheet_names]:
        try:
            df_dict[sheet_name] = xls.parse(sheet_name)
        except Exception as e:
            logger.error(f'Error parsing sheet "{sheet_name}": {e}.')
            exit(e)

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