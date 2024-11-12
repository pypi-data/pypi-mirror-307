# setup.py
from setuptools import setup, find_packages

setup(
    name="EduDesignGen",
    version="0.1.0",
    description="A library to process lesson content with customizable LLM functions",
    install_requires=[
         "requests"  # 添加非标准库依赖
    ],
    packages=find_packages(),
    python_requires='>=3.6',
)
