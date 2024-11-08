import json
import requests
import urllib3
import os
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Mapping of model names to Bedrock model IDs
MODEL_ID_MAPPING = {
    "claude-3-sonnet": "anthropic.claude-3-sonnet-20240229-v1:0",
    "claude-3-haiku": "anthropic.claude-3-haiku-20240307-v1:0",
    "mistral-large": "mistral.mistral-large-2402-v1:0",
    "llama3-8b": "meta.llama3-8b-instruct-v1:0",
    "llama3-70b": "meta.llama3-70b-instruct-v1:0",
}

def get_api_key():
    api_key = os.getenv("VALYU_API_KEY")
    if not api_key:
        raise ValueError("VALYU_API_KEY environment variable is not set.")
    return api_key

class ChatLLM:
    BASE_API_URL = "https://api.valyu.network"

    def __init__(self, model, api_key=None):
        self.model = model
        self.api_endpoint = f"{self.BASE_API_URL}/v1/citations"
        self.api_key = api_key or get_api_key()
        self.system_prompt = """
            You are a helpful AI assistant. 
            You will be provided with multiple pieces of context and a question. 
            You must answer the question based on the context, however you must not disclose that you have been provided with context. I.e. do not say 'Based on the context provided...' or anything similar.
        """

    def generate(self, prompt, documents):
        request_body = {
            "prompt": prompt,
            "documents": documents
        }
        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key
        }
        response = requests.post(
            self.api_endpoint,
            json=request_body,
            headers=headers,
            verify=False 
        )
        if response.status_code != 200:
            raise Exception(f"API request failed with status code {response.status_code}")

        response_data = response.json()
        if "text" not in response_data:
            raise KeyError("The response does not contain the expected 'text' field.")
        return response_data
