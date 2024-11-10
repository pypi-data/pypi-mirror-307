import pytest
from langchain_kipris_tools.tools.patent_search_tool import PatentSearchTool, Patent_Search_Args

def test_patent_search_class():
    search_tool = PatentSearchTool()
    print(search_tool.args_schema)
    print(search_tool.name)
    print(search_tool.description)

def test_patent_search_args():
    args = Patent_Search_Args(word="이차전지")
    print(args)

def test_patent_search_tool():
    search_tool = PatentSearchTool()
    params = Patent_Search_Args(word="이차전지", applicant="현대자동차").model_dump()
    print(params)
    result = search_tool.run(tool_input=params)
    print(result)
    if not result.empty :
        assert True
    else:
        pytest.fail("result is empty")