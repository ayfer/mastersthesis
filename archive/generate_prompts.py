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

prompt_template: (str) = ("""Given the following prompt, {category_prompt}. Do not change anything else.
                                    Prompt: {original_prompt}""")

original_prompt: (str) = ("""
Figure out which is the intent of the input.
If you cannot find a match use \"\"\"Unknown\"\"\"
Return only the intent name
""")

async def generate_new_prompt(
        temp: float=1.0
    ) -> None:

    new_prompt = {}

    with open("categories.json", "r") as file:
        CATEGORIES = json.load(file)
    
    chat = AzureChatOpenAI(
        azure_deployment="gpt-35-turbo-1106",
        temperature=temp,
        cache=False
    )

    for category, category_prompt in CATEGORIES.items():
        for i in range(3):
            system_message_prompt = SystemMessagePromptTemplate.from_template(prompt_template)
            chat_prompt = ChatPromptTemplate.from_messages(
                [system_message_prompt]
            )
            print(category, i)
            durations: List[float] = []
            start_time = time.monotonic()
            response = chat.invoke(
                chat_prompt.format_prompt(
                    original_prompt=original_prompt, category_prompt=category_prompt
                ).to_messages()
            )
            new_prompt[f"{category}_{i}"] = response.content
            end_time = time.monotonic()

            durations.append(end_time - start_time)

    with open("prompts.json", "w") as file:
        json.dump(new_prompt, file)
    

async def main():
    await generate_new_prompt()

if __name__ == "__main__":
    asyncio.run(main())