from setuptools import setup, find_packages
with open('README.md') as f:
    LONG_DESCRIPTION = f.read()


setup(
    name='pureff',
    version='0.1',
    description='f2 without log',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        # 依赖列表
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
)
