from typing import Any, Dict, List, Optional, Union,Callable
from byzerllm.utils.client.types import (    
    LLMFunctionCallResponse,
    LLMClassResponse,LLMResponse    
)
import pydantic
from byzerllm import ByzerLLM
from byzerllm.utils.client import LLMResponse
from byzerllm.utils.types import SingleOutputMeta
from byzerllm.utils.langutil import asyncfy_with_semaphore
from superanalysis.sql.generator import SQLGenerator
from loguru import logger

class LLWrapper:

    def __init__(self,llm:ByzerLLM,entry:SQLGenerator):
        self.entry = entry
        self.llm = llm
        

    def chat_oai(self,
                 conversations,
                 tools:List[Union[Callable,str]]=[], 
                 tool_choice:Optional[Union[Callable,str]]=None,
                 execute_tool:bool=False,  
                 impl_func:Optional[Callable]=None,
                 execute_impl_func:bool=False,
                 impl_func_params:Optional[Dict[str,Any]]=None,
                 func_params:Optional[Dict[str,Any]]=None,
                 response_class:Optional[Union[pydantic.BaseModel,str]] = None, 
                 response_after_chat:Optional[Union[pydantic.BaseModel,str]] = False,
                 enable_default_sys_message:bool=True,                 
                 model:Optional[str] = None,
                 role_mapping=None,llm_config:Dict[str,Any]={}
                 )->Union[List[LLMResponse],List[LLMFunctionCallResponse],List[LLMClassResponse]]:         
        res,contexts = self.entry.stream_chat_oai(conversations)
        s = "".join(res)        
        return [LLMResponse(output=s,metadata={},input="")]

    def stream_chat_oai(self,conversations, 
                        model:Optional[str]=None, 
                        role_mapping=None,
                        delta_mode=False,
                        llm_config:Dict[str,Any]={}): 
        res,contexts = self.entry.stream_chat_oai(conversations)        
        for t in res:                        
            yield (t,SingleOutputMeta(0,0))

    async def async_stream_chat_oai(self,conversations, 
                        model:Optional[str]=None, 
                        role_mapping=None,
                        delta_mode=False,
                        llm_config:Dict[str,Any]={}): 
        res,contexts = await asyncfy_with_semaphore(lambda: self.entry.stream_chat_oai(conversations))()
        for t in res:                                    
            yield (t,SingleOutputMeta(0,0))
                         

    def __getattr__(self, name):        
        return getattr(self.llm, name)