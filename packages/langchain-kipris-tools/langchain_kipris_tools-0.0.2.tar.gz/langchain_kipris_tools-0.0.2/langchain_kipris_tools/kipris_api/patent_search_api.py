from langchain_kipris_tools.kipris_api.abs_class import ABSKiprisAPI
from langchain_kipris_tools.kipris_api.utils import get_nested_key_value
import typing as t
import pandas as pd

class PatentSearchAPI(ABSKiprisAPI):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)        
        self.api_url = "http://plus.kipris.or.kr/kipo-api/kipi/patUtiModInfoSearchSevice/getAdvancedSearch"

    def search(self, word:str,
                invention_title:str="",
                abst_cont:str="",
                claim_scope:str="",
                ipc_number:str="",
                application_number:str="",
                open_number:str="",
                register_number:str="",
                priority_application_number:str="",
                international_application_number:str="",
                international_open_number:str="",
                application_date:str="",
                open_date:str="",
                publication_date:str="",
                register_date:str="",
                priority_application_date:str="",
                international_application_date:str="",
                international_open_date:str="",
                applicant:str="",
                inventor:str="",
                agent:str="",
                right_holder:str="",
                patent:bool=True,
                utility:bool=True,
                lastvalue:str="",
                page_no:int=1,
                num_of_rows:int=10,
                desc_sort:bool=False,
                sort_spec:str="reg_date")->pd.DataFrame:
        """_summary_

        Args:
            word (str): 자유검색 키워드 
            invention_title (str, optional): 발명의 제목에서 검색시 키워드. Defaults to "".
            abst_cont (str, optional): 발명의 개요에서 검색시 키워드. Defaults to "".
            claim_scope (str, optional): 청구범위에서 검색시 키워드. Defaults to "".
            ipc_number (str, optional): IPC번호에서 검색 출원번호. Defaults to "".
            application_number (str, optional): 출원번호에서 검색 출원번호. Defaults to "".
            open_number (str, optional): 공개번호에서 검색 공개번호. Defaults to "".
            register_number (str, optional): 등록번호에서 검색 등록번호. Defaults to "".
            priority_application_number (str, optional): 우선출원번호에서 검색 우선출원번호. Defaults to "".
            international_application_number (str, optional): 국제출원번호에서 검색 국제출원번호. Defaults to "".
            international_open_number (str, optional): 국제공개번호에서 검색 국제공개번호. Defaults to "".
            application_date (str, optional): 출원일에서 검색 출원일. Defaults to "".
            open_date (str, optional): 공개일에서 검색 공개일. Defaults to "".
            publication_date (str, optional): 공고일에서 검색 공고일. Defaults to "".
            register_date (str, optional): 등록일에서 검색 등록일. Defaults to "".
            priority_application_date (str, optional): 우선출원일에서 검색 우선출원일. Defaults to "".
            international_application_date (str, optional): 국제출원일에서 검색 국제출원일. Defaults to "".
            international_open_date (str, optional): 국제공개일에서 검색 국제공개일. Defaults to "".
            applicant (str, optional): 출원인에서 검색 출원인. Defaults to "".
            inventor (str, optional): 발명자에서 검색 발명자. Defaults to "".
            agent (str, optional): 대리인에서 검색 대리인. Defaults to "".
            right_holder (str, optional): 권리취득인에서 검색 권리취득인. Defaults to "".
            patent (bool, optional): 검색 결과에서 특허 포함 여부. Defaults to True.
            utility (bool, optional): 검색 결과에서 실용신안 포함 여부. Defaults to True.
            lastvalue (str, optional): 발명/특허의 상태 코드 검색 Defaults to "".
            page_no (int, optional): 페이지 번호. Defaults to 1.
            num_of_rows (int, optional): 페이지당 행 수. Defaults to 10.
            desc_sort (bool, optional): 내림차순 정렬. Defaults to False.
            sort_spec (str, optional): 정렬 기준. Defaults to "reg_date".

        Returns:
            pd.DataFrame: _description_
        """
        # api url https://plus.kipris.or.kr/portal/data/service/DBII_000000000000001/view.do?menuNo=200100&kppBCode=&kppMCode=&kppSCode=&subTab=SC001&entYn=N&clasKeyword=#soap_ADI_0000000000002944

        response = self.common_call(api_url=self.api_url,
                                  api_key_field="ServiceKey",
                                  word=word,
                                  invention_title=invention_title,
                                  abst_cont=abst_cont,
                                  claim_scope=claim_scope,
                                  ipc_number=ipc_number,
                                  application_number=application_number,
                                  open_number=open_number,
                                  register_number=register_number,
                                  priority_application_number=priority_application_number,
                                  international_application_number=international_application_number,
                                  international_open_number=international_open_number,
                                  application_date=application_date,
                                  open_date=open_date,
                                  publication_date=publication_date,
                                  register_date=register_date,
                                  priority_application_date=priority_application_date,
                                  international_application_date=international_application_date,
                                  international_open_date=international_open_date,
                                  applicant=applicant,
                                  inventor=inventor,
                                  agent=agent,
                                  right_holder=right_holder,
                                  patent="true" if patent else "false",
                                  utility="true" if utility else "false",
                                  page_no=str(page_no),
                                  num_of_rows=str(num_of_rows),
                                  lastvalue=str(lastvalue),
                                  desc_sort="true" if desc_sort else "false",
                                  sort_spec=str(sort_spec))
        patents = get_nested_key_value(response, "response.body.items.item")
        if patents is None:
            return pd.DataFrame()
        if isinstance(patents, t.Dict):
            patents = [patents]
        return pd.DataFrame(patents)