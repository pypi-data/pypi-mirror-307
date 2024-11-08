# -*- coding: utf-8 -*-
import os
from io import open
from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md"), "r", encoding="utf-8") as fobj:
    long_description = fobj.read()

with open(os.path.join(here, "requirements.txt"), "r", encoding="utf-8") as fobj:
    requires = fobj.readlines()
requires = [x.strip() for x in requires if x.strip()]

setup(
    name="llmhelper",
    version="0.5.2",
    description="大模型辅助函数库",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Zhou WangJie",
    maintainer="Zhou WangJie",
    license="Apache License, Version 2.0",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords=["llm", "llmhelper"],
    install_requires=requires,
    packages=find_packages(
        ".",
        exclude=[
            "django_vectorstore_index_model_demo",
            "django_vectorstore_index_model_example",
            "django_vectorstore_index_model_example.migrations",
        ],
    ),
    zip_safe=False,
    include_package_data=True,
)
