from pathlib import Path

from setuptools import setup, find_packages


# 读取 README.md 内容
long_description = (Path(__file__).parent / 'docs/api_reference.md').read_text(encoding='utf-8')

setup(
    name="my_mini_sklearn",           # 库的名称，发布到 PyPI 后用户将用这个名字安装
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "matplotlib"
    ],
    long_description=long_description,  # 添加 long_description 字段
    long_description_content_type="text/markdown",  # 告诉 PyPI 使用 Markdown 格式
    description="A mini machine learning library similar to scikit-learn",
    author="zhao-geyi",
    author_email="3050945076@qq.com",
    url="https://gitee.com/zhao-geyi/mini_sklearn1/tree/mini_sklearn",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
