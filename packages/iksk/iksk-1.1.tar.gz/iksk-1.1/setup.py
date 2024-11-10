from setuptools import setup, find_packages
setup(
    name="iksk",
    version="1.1",
    packages=find_packages(),
    install_requires=[
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
    author="ice",
    author_email="light-team@foxmail.com",
    description="A encrypt and decrypt module for Python.",
    long_description=open('README.md',encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://program.ai/repo/ice/iksk/"
)