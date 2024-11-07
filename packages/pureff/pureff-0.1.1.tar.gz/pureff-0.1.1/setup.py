from setuptools import setup, find_packages

# 读取项目的 README.md 文件作为长描述
with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="pureff",
    version="0.1.1", 
    description="🚀Asynchronous based full-platform download tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Johnserf-Seed",
    author_email="johnserf-seed@foxmail.com",
    license="Apache-2.0",
    url="https://github.com/Johnserf-Seed/f2",
    packages=find_packages(),
    install_requires=[
        "click==8.1.7",
        "rich==13.7.1",
        "httpx==0.27.0",
        "aiofiles==24.1.0",
        "aiosqlite==0.20.0",
        "pyyaml==6.0.1",
        "jsonpath-ng==1.6.1",
        "importlib_resources==6.4.0",
        "m3u8==3.6.0",
        "pytest==8.2.2",
        "pytest-asyncio==0.21.1",
        "browser_cookie3==0.19.1",
        "pydantic==2.6.4",
        "qrcode==7.4.2",
        "websockets>=11.0",
        "PyExecJS==1.5.1",
        "protobuf==5.27.2",
        "gmssl==3.2.2",
    ],
    python_requires=">=3.9",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Intended Audience :: Developers",
        "Intended Audience :: Customer Service",
        "License :: OSI Approved :: Apache Software License"
    ],
    entry_points={
        "console_scripts": [
            "f2 = f2.cli.cli_commands:main"
        ]
    }
)
