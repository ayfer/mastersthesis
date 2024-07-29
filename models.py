from openai import AzureOpenAI, OpenAI
import google.generativeai as genai
import requests
import json

class GeminiModelHandler:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
    
    def get_response(self, prompt, intents, query, temp):
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt.format(input=query, intentsJson=json.dumps(intents)))
        genai.types.GenerationConfig(temperature=temp)
        return response.text

class OpenAIModelHandler:
    def __init__(self, api_key, endpoint, model_name):
        self.client = AzureOpenAI(
        api_key=api_key,  
        api_version="2024-02-01",
        azure_endpoint= endpoint
    )   
        self.model_name = model_name

    def get_response(self, prompt, intents, query, temp):
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": prompt.format(input=query, intentsJson=json.dumps(intents))},
                {"role": "user", "content": query}
            ],
            temperature=temp,
        )
        return response.choices[0].message.content
    
class MistralModelHandler:
    def __init__(self, api_key, endpoint, model_name):
        self.client = OpenAI(
        api_key = api_key,
        base_url = endpoint
    )
        self.model_name = model_name
    
    def get_response(self, prompt, intents, query, temp):
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "user", "content": query},
                {"role": "assistant", "content": prompt.format(input=query, intentsJson=json.dumps(intents))}
            ],
            temperature=temp,
        )
        return response.choices[0].message.content

class LlamaModelHandler:
    def __init__(self, api_key, endpoint):
        self.api_key = api_key
        self.endpoint = endpoint

    def get_headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def get_response(self, prompt, intents, query, temp):
        payload = {
            "messages": [
                {"role": "system", "content": prompt.format(input=query, intentsJson=json.dumps(intents))},
                {"role": "user", "content": query}
            ],
            "temperature": temp
        }

        try:
            url = f'{self.endpoint}/v1/chat/completions'
            response = requests.post(url=url, headers=self.get_headers(), json=payload)
            response = response.json()
            return response['choices'][0]['message']['content'].strip()
        except requests.exceptions.RequestException as e:
            print("Request failed:", e)

def get_model_handler(model_name, model_config):
    if "openai" in model_name:
        return OpenAIModelHandler(
            api_key=model_config["api_key"],
            endpoint=model_config["endpoint"],
            model_name=model_config["model_name"]
        )
    elif "mistral" in model_name:
        return MistralModelHandler(
            api_key=model_config["api_key"],
            endpoint=model_config["endpoint"],
            model_name=model_config["model_name"]
        )
    elif "llama" in model_name:
        return LlamaModelHandler(
            api_key=model_config["api_key"],
            endpoint=model_config["endpoint"]
        )
    elif "gemini" in model_name:
        return GeminiModelHandler(
            api_key=model_config["api_key"]
        )
    else:
        raise ValueError(f"Unsupported model: {model_name}")
