from setuptools import setup, find_packages

setup(
    name="obanRAG",  # Name of your package
    version="0.0.1",  # Version number
    packages=find_packages(),
    install_requires=[
        "openai",
        "pymupdf",
        "pandas",
        "python-docx"
    ],
    description="An advanced Retrieval-Augmented Generation system supporting PDF, Word, and Excel documents with feedback-based prioritization.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="volkanobn@gmail.com",
    classifiers=[
    "Development Status :: 4 - Beta",  # Adjust based on project maturity
    "Intended Audience :: End Users/Desktop",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.7")
