import argparse
import byzerllm
from byzerllm.utils.client import ByzerLLM
from superanalysis.serve.api_server import serve, ServerArgs
from superanalysis.sql.types import RAGConfig, ByzerSQLConfig, ModelConfig
from superanalysis.sql.generator import SQLGenerator
from superanalysis.serve.llm_wrapper import LLWrapper


def main():
    parser = argparse.ArgumentParser(description="ByzerLLM API Server")
    parser.add_argument("--ray-address", type=str, default="auto", help="ray address")
    parser.add_argument(
        "--host", type=str, default="0.0.0.0", help="Host to bind the server to"
    )
    parser.add_argument(
        "--port", type=int, default=8000, help="Port to bind the server to"
    )
    parser.add_argument(
        "--uvicorn-log-level", type=str, default="info", help="Uvicorn log level"
    )
    parser.add_argument(
        "--allow-credentials", action="store_true", help="Allow credentials"
    )
    parser.add_argument(
        "--allowed-origins", type=str, nargs="+", default=["*"], help="Allowed origins"
    )
    parser.add_argument(
        "--allowed-methods", type=str, nargs="+", default=["*"], help="Allowed methods"
    )
    parser.add_argument(
        "--allowed-headers", type=str, nargs="+", default=["*"], help="Allowed headers"
    )
    parser.add_argument(
        "--api-key", type=str, default="", help="API key for authentication"
    )
    parser.add_argument(
        "--served-model-name",
        type=str,
        required=True,
        help="Name of the model to be served",
    )
    parser.add_argument(
        "--prompt-template", type=str, default="", help="Prompt template"
    )
    parser.add_argument(
        "--response-role", type=str, default="assistant", help="Response role"
    )
    parser.add_argument("--ssl-keyfile", type=str, default="", help="SSL key file")
    parser.add_argument(
        "--ssl-certfile", type=str, default="", help="SSL certificate file"
    )

    # Add new arguments for RAGConfig
    parser.add_argument(
        "--schema-rag-base-url", type=str, default="", help="RAG base URL"
    )
    parser.add_argument(
        "--schema-rag-api-key", type=str, default="xxxx", help="RAG API key"
    )

    parser.add_argument(
        "--context-rag-base-url", type=str, default="", help="RAG base URL"
    )
    parser.add_argument(
        "--context-rag-api-key", type=str, default="xxxx", help="RAG API key"
    )

    # Add new argument for ByzerSQLConfig
    parser.add_argument("--byzer-sql-url", type=str, default="", help="Byzer SQL URL")
    parser.add_argument("--data-dir", type=str, default="", help="Data directory")
    parser.add_argument(
        "--owner", type=str, default="hello", help="Owner of the Byzer SQL session"
    )
    parser.add_argument(
        "--llm-model", type=str, default="", help="LLM model for general use"
    )
    parser.add_argument(
        "--gen-sql-llm-model", type=str, default="", help="LLM model for SQL generation"
    )
    parser.add_argument(
        "--sql-func-llm-model", type=str, default="", help="LLM model for SQL functions"
    )

    parser.add_argument(
        "--result-synthesis", action="store_true", help="Enable result synthesis"
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
        served_model_name=args.served_model_name,
        prompt_template=args.prompt_template,
        response_role=args.response_role,
        ssl_keyfile=args.ssl_keyfile,
        ssl_certfile=args.ssl_certfile,
    )

    # Create RAGConfig instance
    rag_config = RAGConfig(
        schema_rag_base_url=args.schema_rag_base_url,
        schema_rag_api_key=args.schema_rag_api_key,
        context_rag_base_url=args.context_rag_base_url,
        context_rag_api_key=args.context_rag_api_key,
    )

    # Create ByzerSQLConfig instance
    byzer_sql_config = ByzerSQLConfig(
        byzer_sql_url=args.byzer_sql_url,
        data_dir=args.data_dir,
        owner=args.owner,
        result_synthesis=args.result_synthesis,
    )

    model_config = ModelConfig(
        llm_model=args.llm_model or args.served_model_name,
        gen_sql_llm_model=args.gen_sql_llm_model or args.served_model_name,
        sql_func_llm_model=args.sql_func_llm_model or args.served_model_name,
    )

    byzerllm.connect_cluster(address=args.ray_address)
    llm = ByzerLLM()
    llm.setup_default_model_name(args.served_model_name)
    llm = byzerllm.ByzerLLM()
    if not server_args.served_model_name:
        raise ValueError("served_model_name is required")
    llm.setup_default_model_name(server_args.served_model_name)

    print("RAG Config: ", rag_config)
    print("Model Config: ", model_config)
    rag = SQLGenerator(
        llm=llm,
        rag_config=rag_config,
        byzer_sql_config=byzer_sql_config,
        model_config=model_config,
    )
    llm_wrapper = LLWrapper(llm=llm, entry=rag)
    serve(llm_wrapper, server_args)


if __name__ == "__main__":
    main()
