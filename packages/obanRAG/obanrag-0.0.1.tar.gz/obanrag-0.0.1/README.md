# obanRAG

`obanRAG` is an advanced Retrieval-Augmented Generation (RAG) library that supports text, PDF, Word, and Excel files. It leverages OpenAI's GPT-4 model to answer queries based on stored documents and dynamically prioritizes documents based on user feedback.

## Features

- **Document Handling**: Supports text, PDF, Word (.docx), and Excel (.xlsx) files.
- **Hybrid Search**: Combines semantic relevance and document priority to retrieve relevant content.
- **Feedback Loop**: Adjusts document priority based on user feedback to improve future responses.
- **Cache Management**: Caches query results for faster response times to repeated queries.

## Installation

Install the package via pip:

```bash
pip install obanRAG

Prerequisites:

OpenAI API Key: You need an OpenAI API key to interact with the GPT-4 model. Set this in the environment or pass it as a parameter when initializing the library.
Register at OpenAI to get an API key.
Note: Without an API key, the library won’t function as intended since it relies on OpenAI's services for query answering.

## Usage

Initialize the System

from obanRAG import vobanRAG

# Initialize the RAG system with your OpenAI API key
rag_system = vobanRAG(api_key="your_openai_api_key")

### Adding Documents
You can add documents of various formats to the document store. Each document type has a unique function.

## Adding Plain Text
Use add_text to add raw text data to the document store.

text_data = "This is a sample text document containing valuable important information."
rag_system.add_text(text_data, title="Sample Text Document")


## Adding a PDF Documents

pdf_path = "path/to/your/document.pdf"
rag_system.add_pdf(pdf_path)


## Adding a Word Document

word_path = "path/to/your/document.docx"
rag_system.add_word(word_path)


## Adding an Excel Document

excel_path = "path/to/your/spreadsheet.xlsx"
rag_system.add_excel(excel_path)


## Querying the System

query = "What is the main topic discussed in the document?"
answer = rag_system.process_query(query)
print("Answer:", answer)


## Providing Feedback

feedback_score = int(input("Please rate the quality of the answer (1-10): "))
rag_system.feedback_loop("document_title", feedback_score)




