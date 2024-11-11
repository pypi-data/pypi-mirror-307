from setuptools import setup, find_packages

setup(
    name="langchain_kipris_tools",  # 패키지 이름
    version="0.0.2",           # 패키지 버전
    author="jaeho. kang",
    author_email="greennuri@gmail.com",
    description="kipris api tools for langchain",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/greennuri/langchain_kipris_tools",  # 패키지 URL (옵션)
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",      # Python 버전 요구 사항
    install_requires=[            # 의존 패키지
        "langchain",
        "requests",
        "xmltodict",
        "pandas",
        "stringcase",
        "python-dotenv",
    ],
)