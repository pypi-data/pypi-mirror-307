import argparse
from service_server.api_server import ServerArgs, serve
from service_server.llm_wrapper import LLWrapper
from service_server.summary_rag import SummaryRAG
import byzerllm


def main():
    parser = argparse.ArgumentParser(description="OpenAI Serve")
    parser.add_argument(
        "--model",
        default="",
    )
    parser.add_argument("--emb_model", default="")
    parser.add_argument(
        "--ray_address",
        default="auto",
    )
    parser.add_argument("--source_dir", default=".", help="")
    parser.add_argument("--host", default="", help="")
    parser.add_argument("--port", type=int, default=8000, help="")
    parser.add_argument("--uvicorn_log_level", default="info", help="")
    parser.add_argument("--allow_credentials", action="store_true", help="")
    parser.add_argument("--allowed_origins", default=["*"], help="")
    parser.add_argument("--allowed_methods", default=["*"], help="")
    parser.add_argument("--allowed_headers", default=["*"], help="")
    parser.add_argument("--api_key", default="", help="")
    parser.add_argument("--served_model_name", default="", help="")
    parser.add_argument("--prompt_template", default="", help="")
    parser.add_argument("--ssl_keyfile", default="", help="")
    parser.add_argument("--ssl_certfile", default="", help="")
    parser.add_argument("--response_role", default="assistant", help="")
    parser.add_argument(
        "--collections", default="", help="Collection name for indexing"
    )
    parser.add_argument(
        "--base_dir",
        default="",
        help="Path where the processed text embeddings were stored",
    )

    args = parser.parse_args()

    server_args = ServerArgs(
        host=args.host,
        port=args.port,
        uvicorn_log_level=args.uvicorn_log_level,
        allow_credentials=args.allow_credentials,
        allowed_origins=args.allowed_origins,
        allowed_methods=args.allowed_methods,
        allowed_headers=args.allowed_headers,
        api_key=args.api_key,
        served_model_name=args.served_model_name or args.model,
        prompt_template=args.prompt_template,
        response_role=args.response_role,
        ssl_keyfile=args.ssl_keyfile,
        ssl_certfile=args.ssl_certfile,
    )
    byzerllm.connect_cluster(address=args.ray_address)
    llm = byzerllm.ByzerLLM()
    if not server_args.served_model_name:
        raise ValueError("served_model_name is required")
    llm.setup_default_model_name(server_args.served_model_name)
    rag = SummaryRAG(llm=llm)    
    llm_wrapper = LLWrapper(llm=llm, rag=rag)
    serve(llm=llm_wrapper, args=server_args)

if __name__ == "__main__":
    main()
