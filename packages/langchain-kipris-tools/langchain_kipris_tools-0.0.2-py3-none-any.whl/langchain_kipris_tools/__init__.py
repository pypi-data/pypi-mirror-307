__version__ = '0.0.2'
from langchain_kipris_tools.kipris_tools import(
    ApplicantSearchTool, PatentKeywordSearchTool, PatentSearchTool 
    ) 
import os
import typing as t
from langchain_core.tools import BaseTool
class LangChainKiprisTools:
    def set_api_key(self, api_key: str):
        self.api_key = api_key
        os.environ['KIPRIS_API_KEY'] = api_key
    def get_tools(self) -> t.List[t.Type[BaseTool]]:
        tool_list = [ApplicantSearchTool(), PatentKeywordSearchTool(), PatentSearchTool()]
        return tool_list
