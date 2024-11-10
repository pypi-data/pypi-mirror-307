from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import argparse
from superanalysis.sql.generator import SQLGenerator
from superanalysis.sql.types import RAGConfig, ByzerSQLConfig, ModelConfig
import byzerllm

app = FastAPI()

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    conversations: List[ChatMessage]    
    model_config: Optional[ModelConfig] = None

class ChatResponse(BaseModel):
    response: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        sql_generator = SQLGenerator(
            llm=llm,
            rag_config=rag_config,
            byzer_sql_config=byzer_sql_config,
            model_config=request.model_config
        )
        result, _ = sql_generator.stream_chat_oai(
            conversations=[{"role": msg.role, "content": msg.content} for msg in request.conversations],
            model=request.model_config.llm_model
        )
        return ChatResponse(response="".join(result))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def main():
    parser = argparse.ArgumentParser(description="SuperAnalysis API Server")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to bind the server to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind the server to")
    parser.add_argument("--schema-rag-base-url", type=str, required=True, help="Schema RAG base URL")
    parser.add_argument("--schema-rag-api-key", type=str, required=True, help="Schema RAG API key")
    parser.add_argument("--context-rag-base-url", type=str, required=True, help="Context RAG base URL")
    parser.add_argument("--context-rag-api-key", type=str, required=True, help="Context RAG API key")
    parser.add_argument("--byzer-sql-url", type=str, required=True, help="Byzer SQL URL")
    parser.add_argument("--data-dir", type=str, default="", help="Data directory")
    parser.add_argument("--owner", type=str, default="hello", help="Owner of the Byzer SQL session")
    parser.add_argument("--llm-model", type=str, required=True, help="LLM model for general use")
    parser.add_argument("--gen-sql-llm-model", type=str, required=True, help="LLM model for SQL generation")
    
    args = parser.parse_args()

    global rag_config

    rag_config = RAGConfig(
        schema_rag_base_url=args.schema_rag_base_url,
        schema_rag_api_key=args.schema_rag_api_key,
        context_rag_base_url=args.context_rag_base_url,
        context_rag_api_key=args.context_rag_api_key
    )
    global byzer_sql_config
    byzer_sql_config = ByzerSQLConfig(
        byzer_sql_url=args.byzer_sql_url,
        data_dir=args.data_dir,
        owner=args.owner
    )

    global llm
    llm = byzerllm.ByzerLLM()
    llm.setup_default_model_name(args.llm_model)

    uvicorn.run(app, host=args.host, port=args.port)

if __name__ == "__main__":
    main()