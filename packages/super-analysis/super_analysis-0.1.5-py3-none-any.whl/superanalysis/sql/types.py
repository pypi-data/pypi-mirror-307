from pydantic import BaseModel

class RAGConfig(BaseModel):
    schema_rag_base_url: str = ""
    schema_rag_api_key: str = "xxxx"

    context_rag_base_url: str = ""
    context_rag_api_key: str = "xxxx"

class ByzerSQLConfig(BaseModel):
    byzer_sql_url: str = ""
    data_dir: str = ""
    owner: str = ""
    result_synthesis: bool = False

class ModelConfig(BaseModel):
    llm_model: str = ""
    gen_sql_llm_model: str = ""
    sql_func_llm_model: str = ""