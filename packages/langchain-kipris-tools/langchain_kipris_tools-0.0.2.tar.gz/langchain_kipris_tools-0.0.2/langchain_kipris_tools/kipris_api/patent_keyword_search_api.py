from langchain_kipris_tools.kipris_api.abs_class import ABSKiprisAPI
from langchain_kipris_tools.kipris_api.utils import get_nested_key_value
import typing as t
import pandas as pd

class PatentSearchAPI(ABSKiprisAPI):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_url = "http://plus.kipris.or.kr/openapi/rest/patUtiModInfoSearchSevice/freeSearchInfo"

    def search(self, query:str, patent:bool=True,
                utility:bool=True,
                lastvalue:str="",
                docs_start:int=1,
                docs_count:int=10,
                desc_sort:bool=False,
                sort_spec:str="reg_date")->pd.DataFrame:
        """
        KIPRIS API 검색 서비스

        Args:
            query (str): 검색어
            patent (bool): 특허 여부
            utility (bool): 특허 여부
            lastvalue (str): 특허 상태값
            docs_start (int, optional): 시작 번호. Defaults to 1.
            docs_count (int, optional): 검색결과 표시 수량. Defaults to 10.
            desc_sort (bool, optional): 내림차순 여부. Defaults to False.
            sort_spec (str, optional): 정렬 기준. Defaults to "AD".
        """
        # api url https://plus.kipris.or.kr/portal/data/service/DBII_000000000000001/view.do?menuNo=200100&kppBCode=&kppMCode=&kppSCode=&subTab=SC001&entYn=N&clasKeyword=#soap_ADI_0000000000010162

        response = self.common_call(api_url= self.api_url, word=query,
                                  patent="true" if patent else "false",
                                  utility="true" if utility else "false",
                                  docs_start=str(docs_start),
                                  docs_count=str(docs_count),
                                  lastvalue=str(lastvalue),
                                  desc_sort="true" if desc_sort else "false",
                                  sort_spec=str(sort_spec))
        patents = get_nested_key_value(response, "response.body.items.PatentUtilityInfo")
        if patents is None:
            return pd.DataFrame()
        if isinstance(patents, t.Dict):
            patents = [patents]
        return pd.DataFrame(patents)