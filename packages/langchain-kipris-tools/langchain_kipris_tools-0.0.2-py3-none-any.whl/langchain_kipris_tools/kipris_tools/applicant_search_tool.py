from langchain_kipris_tools.kipris_api.applicant_search_api import ApplicantNameSearchAPI
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
import typing as t
import pandas as pd

class Applicant_Search_Args(BaseModel):
    applicant: str = Field(..., description="Applicant name is required")
    docs_start: int = Field(1, description="Start index for documents, default is 1")
    docs_count: int = Field(10, description="Number of documents to return, default is 10, range is 1-30")
    patent: bool = Field(True, description="Include patents, default is True")
    utility: bool = Field(True, description="Include utility models, default is True")
    lastvalue:  t.Optional[str] = Field("", description="Patent registration status; leave empty for all, (A, C, F, G, I, J, R, or empty)")
    sort_spec: str = Field("AD", description="Sort field; default is AD")
    desc_sort: bool = Field(True, description="Sort in descending order; default is True, when True, sort by descending order.it mean latest date first.")


class ApplicantSearchTool(BaseTool):
    name:str = "applicant_search"
    description:str = "patent search by applicant name"
    api:ApplicantNameSearchAPI = ApplicantNameSearchAPI()
    args_schema:t.Type[BaseModel] = Applicant_Search_Args
    return_direct: bool = False

    def _run(self, applicant:str, docs_start:int=1, docs_count:int=10, patent:bool=True, utility:bool=True, lastvalue:t.Optional[str]="", sort_spec:str="AD", desc_sort:bool=True)->pd.DataFrame:
        result = self.api.search(applicant, docs_start, docs_count, patent, utility, lastvalue, sort_spec, desc_sort)
        return result.to_json()
