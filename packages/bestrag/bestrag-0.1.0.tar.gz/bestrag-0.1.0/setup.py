from setuptools import setup, find_packages

setup(
    name="bestrag",
    version="0.1.0",
    description="BestRAG (Best Retrieval Augmented by Qdrant) is a library that provides "
                "functionality for storing and searching document embeddings in a Qdrant vector database.",
    author="samadpls",
    author_email="abdulsamadsid1@gmail.com",
    url="https://github.com/samadpls/bestrag",
    packages=find_packages(),
    install_requires=[
        "fastembed==0.4.1",
        "streamlit",
        "pytest",
        "flake8",
        "PyPDF2",
        "qdrant-client",
        "onnxruntime==1.19.2",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
