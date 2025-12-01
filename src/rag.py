import io
import uuid
from typing import List

import tiktoken
from fastapi import UploadFile, HTTPException
from pypdf import PdfReader
from docx import Document
from qdrant_client.http import models
from starlette.status import HTTP_400_BAD_REQUEST

from src.logger import logger
from src.settings import settings
from src.vdb import client, embedder

ENCODER = tiktoken.get_encoding("cl100k_base")
TOKENS_PER_CHUNK = 250


def _embed(text: str):
    return list(embedder.embed([text]))[0]


def _read_pdf(file_bytes: bytes) -> List[str]:
    reader = PdfReader(io.BytesIO(file_bytes))

    text = []
    for page in reader.pages:
        text.append(page.extract_text() or "")
    return text


def _read_docx(file_bytes: bytes) -> List[str]:
    # maybe too "one-liney" but we just read the paragraphs from the file, basically
    return [p.text for p in Document(io.BytesIO(file_bytes)).paragraphs]


def _text_into_chunks(contents: List[str]):
    chunks = []

    for content in contents:
        tokens = ENCODER.encode(content)
        start = 0
        while start < len(tokens):
            end = start + TOKENS_PER_CHUNK
            chunk_tokens = tokens[start:end]
            chunk_text = ENCODER.decode(chunk_tokens)
            chunks.append(chunk_text)
            start += end

    return chunks


def insert_into_vdb(file: UploadFile):
    if file.content_type == "application/pdf":
        contents = _read_pdf(file.file.read())
    elif (
        file.content_type
        == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ):
        contents = _read_docx(file.file.read())
    else:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Wrong file type")

    chunks = _text_into_chunks(contents)

    logger.debug(f"Chunks generated: {chunks}")

    client.upsert(
        settings.qdrant_main_collection_name,
        models.Batch(
            ids=[str(uuid.uuid4()) for _ in chunks],
            vectors=[_embed(chunk) for chunk in chunks],
            payloads=[{"text": chunk} for chunk in chunks],
        ),
    )


def _search_vdb(text: str):
    results = client.query_points(
        settings.qdrant_main_collection_name,
        _embed(text),
        limit=3,
        score_threshold=0.75,
    )
    text = ""
    if results.points:
        for r in results.points:
            text += r.payload.get("text", "") + "\n"
    return text


def get_rag_context(text: str):
    return _search_vdb(text)
