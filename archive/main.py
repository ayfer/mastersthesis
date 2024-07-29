import os
from typing import Any, List

import langchain
import uvicorn as uvicorn
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import ValidationError
from loguru import logger

from langchain import LLMChain, PromptTemplate
from langchain.llms import AzureOpenAI
from langchain.cache import SQLiteCache, GPTCache
from langchain.chains import ConversationalRetrievalChain
from langchain.chains.conversational_retrieval.prompts import CONDENSE_QUESTION_PROMPT
from langchain.chains.question_answering import load_qa_chain
from langchain.memory import ChatMessageHistory
from langchain.schema import HumanMessage, AIMessage
from langchain.retrievers import ChatGPTPluginRetriever

from AzureOpenAI.AzureOpenAI import AzureOpenAINoParameters
from cache.GPTCache import init_gptcache_map
from models.models import DocumentMetadata, Answer, Question, ChainType
from models.charm_model import Prompt
from prompts import prompt_dict

bearer_scheme = HTTPBearer()
BEARER_TOKEN = os.getenv("BEARER_TOKEN")
assert BEARER_TOKEN is not None

def validate_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    if credentials.scheme != "Bearer" or credentials.credentials != BEARER_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    return credentials

language = 'German' # there should be a more principled way to make this specification 

def get_prompt(prompt_id: str) -> Any:
    prompt = Prompt(**prompt_dict.get(prompt_id, {'id': prompt_id}))
    template = prompt.convert_to_lc_template().replace('{language}', language)
    return(PromptTemplate.from_template(template))

def extract_metadata(source_documents: List) -> List[DocumentMetadata]:
    metadata: List[DocumentMetadata]
    try:
        metadata = [DocumentMetadata(**meta_dict)
                    for doc in source_documents
                    for meta_dict in [doc.metadata['metadata']]]
    except: # raised by older langchain versions
        metadata = []    
    return metadata

def strip_end_tokens(llm_response: str) -> str:
    return llm_response.removesuffix('<|im_end|>').removesuffix('<|im_sep|>')

def extract_chat_history(memory) -> str:
    turns = memory.messages
    chat_history: List[str] = []
    for i, turn in enumerate(turns):
        speaker: str
        if isinstance(turn, HumanMessage):
            speaker = human_prefix
        elif isinstance(turn, AIMessage):
            speaker = ai_prefix
        else:
            speaker = f'Speaker {i}'
        chat_history.append(f'{speaker}: {turn.content}')
    return '\n'.join(chat_history)

memory = ChatMessageHistory()

# memory_key: str = 'chat_history'
human_prefix: str = 'Human'
ai_prefix: str = 'AI'

# memory = ConversationBufferMemory(
#       memory_key=memory_key
#     , human_prefix=human_prefix
#     , ai_prefix=ai_prefix
#     , return_messages=False
#)

OPENAI_API_TYPE = os. getenv('OPENAI_API_TYPE', 'azure')
OPENAI_API_VERSION = os.getenv('OPENAI_API_VERSION', '2023-05-15')
OPENAI_API_BASE = os.getenv('OPENAI_API_BASE', 'https://frank-openai.openai.azure.com/')
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_COMPLETIONMODEL_DEPLOYMENTID = os.getenv('OPENAI_COMPLETIONMODEL_DEPLOYMENTID', 'gpt-35-turbo')

RETRIEVER_BEARER_TOKEN = os.getenv('RETRIEVER_BEARER_TOKEN')
RETRIEVER_URL = os.getenv("RETRIEVER_URL", "http://0.0.0.0:8000")
ANSWER_PORT = os.getenv("ANSWER_PORT", 8100)
CACHE_TYPE = os.getenv("CACHE_TYPE", "string")

retriever_top_k_default: int = 3          # should be derived from the default value of the top_k field of the retriever class
retriever = ChatGPTPluginRetriever(
      url=RETRIEVER_URL
    , bearer_token=RETRIEVER_BEARER_TOKEN
    , top_k=retriever_top_k_default
)
llm = AzureOpenAI(
      deployment_name=OPENAI_COMPLETIONMODEL_DEPLOYMENTID
    , temperature=0
    , cache=False
)
condense_question_prompt = get_prompt('condense_question_prompt')
question_generator = LLMChain(
      llm=llm
    , prompt=condense_question_prompt
)
qa_prompt = get_prompt('qa_prompt')
stuff_docs_chain = load_qa_chain(
      llm
    , chain_type='stuff'
    , prompt=qa_prompt
)
map_prompt = get_prompt('map_prompt')
reduce_prompt = get_prompt('reduce_prompt')
map_reduce_docs_chain = load_qa_chain(
      llm
    , chain_type='map_reduce'
    , question_prompt=map_prompt
    , combine_prompt=reduce_prompt
)
initial_prompt = get_prompt('initial_answer_prompt')
refine_prompt = get_prompt('refine_answer_prompt')
refine_docs_chain = load_qa_chain(
      llm
    , chain_type='refine'
    , question_prompt=initial_prompt
    , refine_prompt=refine_prompt
)
chat_history = []

if CACHE_TYPE == 'string':
    langchain.llm_cache = SQLiteCache(database_path='.cache.db')

# https://github.com/hwchase17/langchain/issues/2879
if CACHE_TYPE == 'similarity':
    langchain.llm_cache = GPTCache(init_gptcache_map)

app = FastAPI(dependencies=[Depends(validate_token)])

@app.post('/answer', response_model=Answer)
async def answer(question: Question) -> Any:
    retriever.top_k = retriever_top_k_default
    chain = ConversationalRetrievalChain(
          retriever=retriever
        , question_generator=question_generator
        , combine_docs_chain=stuff_docs_chain
        , return_generated_question=True
        , return_source_documents=True
    )
    result = chain(
        { 'question': question.question
        , 'chat_history': '\n'.join([t[0] + '\n' + t[-1] for t in chat_history])
        }
        , return_only_outputs=True
    )
    standalone_question = result['generated_question']
    chat_history.append((standalone_question, result['answer']))
    metadata: List[DocumentMetadata] = extract_metadata(result['source_documents'])
    source_documents: List[str] = [doc.page_content for doc in result['source_documents']]
    return Answer(
          answer=result['answer'].replace('\n', '')
        , metadata=metadata
        , source_documents=source_documents
    )

@app.post('/answer_with', response_model=Answer)
async def answer_with(
      question: Question
    , retriever_top_k: int = 3
    , docs_chain_type: ChainType = ChainType.stuff
    , maintain_history: bool = True
) -> Any:
    # initialization/parametrization of common components
    retriever.top_k = retriever_top_k
    condense_question_prompt = get_prompt('condense_question_prompt')
    question_generator = LLMChain(
          llm=llm
        , prompt=condense_question_prompt
    )
    qa_prompt = get_prompt('qa_prompt')
    # other setup
    match docs_chain_type:
        case ChainType.stuff:
            docs_chain = stuff_docs_chain
        case ChainType.map_reduce:
            docs_chain = map_reduce_docs_chain
        case ChainType.refine:
            docs_chain = refine_docs_chain
    chat_history = extract_chat_history(memory)
    logger.info(f'The chat history is:\n{chat_history}')
    chain = ConversationalRetrievalChain(
          retriever=retriever
        , question_generator=question_generator
        , combine_docs_chain=docs_chain
        , return_generated_question=True
        , return_source_documents=True
        )
    result = chain(
        { 'question': question.question
        , 'chat_history': memory.messages
        }
        , return_only_outputs=True
    )
    standalone_question = strip_end_tokens(result['generated_question'])
    logger.info(f'The standalone question is: "{standalone_question}"')
    # response handling
    answer = strip_end_tokens(result['answer'].replace('\n', ''))
    if maintain_history:
        memory.add_user_message(standalone_question)
        memory.add_ai_message(answer)
    metadata: List[DocumentMetadata] = extract_metadata(result['source_documents'])
    source_documents = [doc.page_content for doc in result['source_documents']]
    return Answer(
          answer=answer
        , metadata=metadata
        , source_documents=source_documents
    )

@app.post('/clear_memory')
async def clear_memory(
) -> bool:
    memory.clear()
    return True

@app.post('/retrieve_prompt', response_model=Prompt)
async def retrieve_prompt(
    prompt_id: str
) -> Any:
    prompt = Prompt(**prompt_dict.get(prompt_id, {}))
    return prompt

@app.post('/upsert_prompt')
async def upsert_prompt(
    prompt: Prompt
) -> bool:
    prompt_dict[prompt.id] = prompt.__dict__
    return True

@app.post('/predict', response_model=Answer)
async def predict(
      prompt_id: str
    , question: Question
    , max_tokens: int = 30
) -> Any:
    llm = AzureOpenAI(
          deployment_name=OPENAI_COMPLETIONMODEL_DEPLOYMENTID
        , temperature=0
        , cache=False
        , max_tokens=max_tokens
    )
    prompt = get_prompt(prompt_id)
    intent_classifier = LLMChain(
          llm=llm
        , prompt=prompt
    )
    response = intent_classifier.predict(query=question.question)
#    response = response.split('.')[0]
    return Answer(
          answer=response
        , metadata=[]
        , source_documents=[]
    )

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=ANSWER_PORT)
