import os
from langchain_core.messages import HumanMessage
from langchain_openai import AzureChatOpenAI

OPENAI_API_VERSION = os.getenv("OPENAI_API_VERSION")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")

model = AzureChatOpenAI(
    azure_deployment="gpt-35-turbo-1106",
)

message = HumanMessage(
    content="Translate this sentence from English to German. I love programming."
)
print(model([message]).content)