from langchain_kipris_tools.kipris_api.patent_keyword_search_api import PatentSearchAPI
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
import typing as t
import pandas as pd

class Patent_Keyword_Search_Args(BaseModel):
    query: str = Field("", description="Search query, default is an empty string. if this is empty, then i should ask user to input query.")
    patent: bool = Field(True, description="Include patents, default is True")
    utility: bool = Field(True, description="Include utility, default is True")
    lastvalue:  t.Optional[str] = Field("", description="Patent registration status; (전체:공백입력, 공개:A, 취하:C, 소멸:F, 포기:G, 무효:I, 거절:J, 등록:R)")
    docs_start: int = Field(1, description="Start index for documents, default is 0")
    docs_count: int = Field(10, description="Number of documents to return, default is 10")
    desc_sort: bool = Field(True, description="Sort in descending order, default is True")
    sort_spec: str = Field("AD", description="Field to sort by; default is 'AD'(PD-공고일자, AD-출원일자, GD-등록일자, OPD-공개일자, FD-국제출원일자, FOD-국제공개일자, RD-우선권주장일자)")


class PatentKeywordSearchTool(BaseTool):
    name:str = "patent_keyword_search"
    description:str = "patent search by keyword"
    api:PatentSearchAPI = PatentSearchAPI()
    args_schema:t.Type[BaseModel] = Patent_Keyword_Search_Args
    return_direct: bool = False

    def _run(self, query:str, patent:bool=True, utility:bool=True, lastvalue:t.Optional[str]="", docs_start:int=0, docs_count:int=10, desc_sort:bool=True, sort_spec:str="AD")->pd.DataFrame:
        result = self.api.search(query, patent=patent, utility=utility, lastvalue=lastvalue, docs_start=docs_start, docs_count=docs_count, sort_spec=sort_spec, desc_sort=desc_sort)
        return result
