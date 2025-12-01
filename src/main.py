import json

import requests
from src.logger import logger
from fastapi import FastAPI, UploadFile
from starlette.status import HTTP_202_ACCEPTED, HTTP_200_OK


from src.rag import insert_into_vdb, get_rag_context
from src.settings import settings

app = FastAPI()


@app.post("/add-rag-doc", status_code=HTTP_202_ACCEPTED, description="This endpoint allows upload of WORD and PDF docs.")
def add_rag_doc(file: UploadFile):
    insert_into_vdb(file)
    return "success"


@app.post("/chat", status_code=HTTP_200_OK)
def chat(prompt: str):
    prompt = (
        f"""PROMPT: {prompt} \n CONTEXT:\n {get_rag_context(prompt)} \n MAX 50 WORDS"""
    )
    logger.debug(f"sending prompt: `{prompt}` to local model")

    body = {"model": "gemma3:4b", "prompt": prompt, "stream": False}
    response = requests.post(url=settings.llm_host, json=body).text
    model_response = json.loads(response).get("response", "")
    return model_response
