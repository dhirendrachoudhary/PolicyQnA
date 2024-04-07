import time
import psutil
from fastapi import FastAPI
from pydantic import BaseModel
from app.doc_search import load_chunk_persist_pdf, get_llm_response
from contextlib import asynccontextmanager

resource = {}
request_counter = 0

@asynccontextmanager
async def lifespan(app: FastAPI):
    resource['db'] = load_chunk_persist_pdf()
    yield
    resource['db'].client.indices.refresh(index="policy-qa")
    resource.clear()

app = FastAPI(lifespan=lifespan)

class Query(BaseModel):
    query: str

@app.post("/search")
async def search_docs(query: Query):
    start_time = time.time()
    response = get_llm_response(query.query, resource['db'])
    end_time = time.time()
    response_time = end_time - start_time
    
    # Calculate throughput
    request_processed()
    
    # Monitor resource utilization
    cpu_percent = psutil.cpu_percent(interval=None)
    memory_percent = psutil.virtual_memory().percent
    
    return {
        "answer": response[0],
        "sources": response[1],
        "response_time": response_time,
        "cpu_percent": cpu_percent,
        "memory_percent": memory_percent
    }

def request_processed():
    global request_counter
    request_counter += 1
