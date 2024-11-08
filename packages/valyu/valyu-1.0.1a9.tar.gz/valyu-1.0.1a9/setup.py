# setup.py

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='valyu',
    version='1.0.1a9',
    author='Valyu',
    author_email='contact@valyu.network',
    maintainer='Harvey Yorke',
    maintainer_email='harvey@valyu.network',
    description='Data is for AI what source code is for software.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://valyu.network",
    packages=find_packages(),
    install_requires=[
        'requests>=2.31.0',
        'tqdm>=4.66.4',
        'boto3==1.35.47',
        'pydantic>=2.5.2',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
