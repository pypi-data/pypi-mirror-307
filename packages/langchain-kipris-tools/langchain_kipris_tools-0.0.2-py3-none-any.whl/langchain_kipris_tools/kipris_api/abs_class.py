import os
import typing as t
from langchain_kipris_tools.kipris_api.utils import get_response
from dotenv import load_dotenv
from stringcase import camelcase
load_dotenv()

class ABSKiprisAPI:
    def __init__(self, **kwargs):
        if "api_key" in kwargs:
            self.api_key = kwargs["api_key"]
        else:
            if os.getenv("KIPRIS_API_KEY") :
                self.api_key = os.getenv("KIPRIS_API_KEY")
            else:
                raise ValueError("KIPRIS_API_KEY is not set you must set KIPRIS_API_KEY in .env file or pass api_key to constructor ")

    def common_call(self,api_url:str, api_key_field = "accessKey", **params)->t.Dict:
        """
        KIPRIS API 공통 호출 서비스

        Args:
            sub_url (str): 서브 URL

        Returns:
            t.List[dict]: 응답 데이터
        """
        # url = "%s%s?"%(self.base_url, self.sub_url)
        query = ""
        for k,v in params.items():
            if v is not None and v != "":
                query += "&%s=%s"%(camelcase(k),v)
        api_key = "&%s=%s"%(api_key_field,self.api_key)
        full_url = f"{api_url}?{query[1:]}{api_key}"
        print(full_url)
        return get_response(full_url)
