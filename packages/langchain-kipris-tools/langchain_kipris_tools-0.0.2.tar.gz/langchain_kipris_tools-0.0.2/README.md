# langchain_kipris_tools

plus.kipris.or.kr 에서 제공하는 api_key를 이용하여 특허를 검색하는 langchain tool 구현체입니다.
api_key는 본인의 키를 사용해야 합니다.
가입은 plus.kipris.or.kr/portal/main.do 에서 가입 후 사용 가능합니다.

사용 예제

```python
import os
os.environ["KIPRIS_API_KEY"] = ''

from langchain_kipris_tools import LangChainKiprisTools
kipristools = LangChainKiprisTools()
tools = kipristools.get_tools()
```

제공하는 api 목록

| 순번 | api 명칭                     | 설명             | 참조 url                                                                                                       |
| - | ---------------------------- | ---------------- | -------------------------------------------------------------------------------------------------------------- |
|  1| patent_search_tool           | 특허 전체 검색   | [link](https://plus.kipris.or.kr/portal/popup/DBII_000000000000001/SC002/ADI_0000000000002944/apiDescriptionSearch.do) |
|  2| patent_keyword_search_tool   | 특허 키워드 검색 | [link](https://plus.kipris.or.kr/portal/popup/DBII_000000000000001/SC002/ADI_0000000000010162/apiDescriptionSearch.do) |
|  3| patent_applicant_search_tool | 특허 출원인 검색 | [link](https://plus.kipris.or.kr/portal/popup/DBII_000000000000001/SC002/ADI_0000000000015118/apiDescriptionSearch.do) |
