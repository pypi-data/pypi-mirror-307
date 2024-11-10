from typing import Optional, Dict, Any, List
from openai import OpenAI
import json
from .types import RAGConfig, ByzerSQLConfig, ModelConfig
from byzerllm.utils.client import code_utils
import byzerllm
import requests
from loguru import logger
import traceback
from byzerllm.utils.nontext import TagExtractor


class SQLGenerator:

    @byzerllm.prompt()
    def gen_context(self, conversations: List[Dict[str, str]]) -> str:
        """
        对话内容：
        {% for msg in conversations %}
        <{{ msg.role }}>: {{ msg.content }}
        {% endfor %}

        根据提供的对话内容，理解用户最后的问题，然后提取可能会用到的 Byzer-SQL 相关的知识。
        """

    @byzerllm.prompt()
    def gen_sql(
        self,
        conversations: List[Dict[str, str]],
        context: str,
        schema: str,
        model: str = "deepseek_chat",
    ) -> str:
        """
        相关知识：
        {{ context }}

        Schema信息：
        {{ schema }}

        对话内容：
        {% for msg in conversations %}
        <{{ msg.role }}>: {{ msg.content }}
        {% endfor %}

        模型UDF函数：
        {{ model }}

        根据提供的相关知识以及对话内容，理解用户最后的问题，然后根据看到的schema 信息，生成 Byzer-SQL 语句。
        Byzer-SQL 首先需要用 load 语法加载 schema 中的路径映射成表格，然后根据表格的信息生成对应的 Byzer-SQL 语句。

        特别需要关注的是:
        1. 用户的很多需求是要对表格的文本内容做自然语言处理，你需要使用 Byzer-SQL 中的大模型辅助函数来完成这个需求。
        2. 使用 `llm_result` 函数处理 LLM 模型函数的响应,`llm_result` 函数得到的是一段文本，虽然我们要求模型函数只输出特定的文本，但考虑到大模型会有一些额外的字符输出，不会只是输出我们要求的文字，所以通过 `like` 来进行匹配。
        3. 注意 Byzer-SQL 的语法，比如select 语句最后一定需要有 as <table_name>。
        3. 输出的 Byzer-SQL 语句务必使用 <_byzer_sql_></_byzer_sql_> 标签包裹起来。
        """

    @byzerllm.prompt()
    def fetch_schema(self, context: str) -> str:
        """
        下面是一些基础知识，包括名词术语等等：
        {{ context }}

        当理解对话内容的时候，需要参考上面的基础知识，然后更好的理解对应的表格schema信息是不是有用。
        """
    
    @byzerllm.prompt()
    def result_synthesis(self, conversations: List[Dict[str, str]], result: str) -> str:
        """
        对话内容：
        {% for msg in conversations %}
        <{{ msg.role }}>: {{ msg.content }}
        {% endfor %}

        系统返回的数据：
        {{ result }}

        根据提供的对话内容以及系统返回的数据，对数据使用自然语言进行表述，要友好、简洁、准确。
        """

    def __init__(
        self,
        llm: byzerllm.ByzerLLM,
        rag_config: RAGConfig,
        byzer_sql_config: ByzerSQLConfig,
        model_config: ModelConfig,
    ) -> None:
        self.llm = llm
        self.schema_rag_client = OpenAI(
            api_key=rag_config.schema_rag_api_key,
            base_url=rag_config.schema_rag_base_url,
        )
        self.context_rag_client = OpenAI(
            api_key=rag_config.context_rag_api_key,
            base_url=rag_config.context_rag_base_url,
        )
        self.byzer_sql_url = byzer_sql_config.byzer_sql_url
        self.byzer_sql_config = byzer_sql_config
        self.llm_model = byzerllm.ByzerLLM()
        self.llm_model.setup_default_model_name(model_config.llm_model)
        self.gen_sql_llm_model = byzerllm.ByzerLLM()
        self.gen_sql_llm_model.setup_default_model_name(model_config.gen_sql_llm_model)
        self.model_config = model_config


    def stream_chat_oai(
        self,
        conversations,
        model: Optional[str] = None,
        role_mapping=None,
        delta_mode=False,
        llm_config: Dict[str, Any] = {},
    ):
        try:
            v, c = self._stream_chat_oai(
                conversations=conversations,
                model=model,
                role_mapping=role_mapping,
                delta_mode=delta_mode,
                llm_config=llm_config,
            )
        except Exception as e:
            error_msg = f"Error in stream_chat_oai: {e}\n{traceback.format_exc()}"
            logger.error(error_msg)
            v, c = [str(e)], []

        return v, c

    def _stream_chat_oai(
        self,
        conversations,
        model: Optional[str] = None,
        role_mapping=None,
        delta_mode=False,
        llm_config: Dict[str, Any] = {},
    ):
        logger.info(f"Starting stream_chat_oai with model: {model}")
        logger.debug(f"Conversations: {conversations}")
        logger.debug(f"LLM Config: {llm_config}")

        if not model:
            model = self.llm_model.default_model_name
        logger.info(f"Using model: {model}")

        query = conversations[-1]["content"]

        if (
            "使用四到五个字直接返回这句话的简要主题，不要解释、不要标点、不要语气词、不要多余文本，不要加粗，如果没有主题"
            in query
            or "简要总结一下对话内容，用作后续的上下文提示 prompt，控制在 200 字以内"
            in query
        ):
            chunks = self.llm.stream_chat_oai(
                conversations=conversations,
                model=model,
                role_mapping=role_mapping,
                llm_config=llm_config,
                delta_mode=True,
            )
            return (chunk[0] for chunk in chunks), []

        logger.info("Fetching context from context RAG client")
        context_query = self.gen_context.prompt(conversations=conversations)
        context_response = self.context_rag_client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": json.dumps(
                        {"query": context_query, "only_contexts": True},
                        ensure_ascii=False,
                    ),
                }
            ],
            model=model,
        )

        context = context_response.choices[0].message.content
        new_context = ""
        for msg in context.split("\n"):
            if msg.strip():
                v = json.loads(msg)
                new_context += v["source_code"]
        logger.info(f"context {new_context[0:100]}...")
        logger.info("Context retrieved successfully")

        logger.info("Fetching schemas from schema RAG client")
        schema_query = self.fetch_schema.prompt(context=new_context)

        response = self.schema_rag_client.chat.completions.create(
            messages=conversations[0:-1]
            + [
                {
                    "role": "user",
                    "content": json.dumps(
                        {"query": schema_query, "only_contexts": True},
                        ensure_ascii=False,
                    ),
                }
            ],
            model=model,
        )        

        schema_str = response.choices[0].message.content
        logger.debug(f"Schema RAG response: {schema_str}")
        logger.info("Schema retrieved successfully")

        logger.info("Generating SQL string")
        sql_str = self.gen_sql.with_llm(self.gen_sql_llm_model).run(
            conversations=conversations,
            context=new_context,
            schema=schema_str,
            model=self.model_config.sql_func_llm_model,
        )

        logger.info("SQL string generated")
        logger.debug(f"Generated SQL string: {sql_str}")

        # Extract SQL code from tags
        tag_extractor = TagExtractor(sql_str)
        extracted_tags = tag_extractor.extract()
        sql = extracted_tags.content[0].content
        logger.info(f"Extracted SQL: {sql}")

        if not self.byzer_sql_url:
            return (item for item in [sql]), []

        logger.info(f"Sending SQL to Byzer SQL URL: {self.byzer_sql_url}")
        try:
            response = requests.post(
                self.byzer_sql_url,
                data={
                    "sql": sql,
                    "owner": self.byzer_sql_config.owner or "hello",
                    "sessionPerUser": True,
                    "sessionPerRequest": True,
                    "includeSchema": True,
                },
            )
            response.raise_for_status()
            result = response.content.decode("utf-8")
            logger.info("SQL execution result decoded")
            logger.debug(f"SQL execution result: {result}")
            if self.byzer_sql_config.result_synthesis:
                synthesized_result = self.result_synthesis.with_llm(self.llm_model).run(
                    conversations=conversations,
                    result=result,
                )
                return (item for item in [synthesized_result]), []
            else:
                return (item for item in [result]), []
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send SQL to Byzer SQL URL: {e}")
            if hasattr(e.response, "content"):
                error_content = e.response.content.decode("utf-8")
                logger.error(f"Server response: {error_content}")
            else:
                logger.error("No server response available")
            raise Exception(f"Byzer SQL request failed: {str(e)}") from e
