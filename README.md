# Broccoli-RAG

## Etymology
GitHub auto-suggested `broccoli-something`, I suggested `RAG`. Boom, `Broccoli-RAG`.

## General Info
Broccoli-RAG is a small and very simple example of how to implement RAG functionality using vector database and local LLM model.
It is just a showcase of the general idea, it skips a lot of important stuff.

It uses:
- **Python**, duh
- **FastAPI**, for our backend's API
- **OLlama**, for local LLM model
- **Qdrant**, as vector database
- **Tiktoken**, for 
- **Docker**, so we can do everything out of the box, no need for manual installation of each component

## Requirements

You need to have docker (with compose plugin) installed.

Also, if you want to use GPU for local LLM, you might need to tweak around with your GPU settings in WSL/Linux, but it should work out of the box. 
The GPU setup of docker compose looks like this:
```yaml
    deploy: { }
    runtime: nvidia
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
```

Also `(Also count so far: 2)`, you need to have the ability to run the makefile (`apt install make` ;))

## Usage
To use this beautiful project, you just need to run:
```bash
make up
```
That's it. It should install all the required containers, start them and install the relevant LLM model. In our case it's `gemma3:4b`

Then you can navigate to `http://localhost:8080/docs`.

There are two endpoints:
- `/add-rag-doc` - it allows a WORD or PDF document and adds it to the Vector DB
- `/chat` - It returns a model response to the given prompt using RAG and Local LLM model