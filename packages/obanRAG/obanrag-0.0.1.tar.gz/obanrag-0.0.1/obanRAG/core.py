import openai
import pymupdf  # Use pymupdf for PDF processing
import pandas as pd
from docx import Document as DocxDocument
from collections import defaultdict
import os
from openai import OpenAI

# Set up OpenAI API key
API_KEY = "your_openai_api_key"

# create an OpenAI client using the API key
client = OpenAI(api_key=API_KEY)

class vobanRAG:
    def __init__(self):
        # Document storage, caching, and feedback tracking
        self.documents = []
        self.document_titles = []
        self.cache = {}
        self.feedback_scores = defaultdict(list)  # Stores feedback scores for each document
        self.document_priority = defaultdict(float)  # Tracks priority score for each document
    
    def add_text(self, text, title="Text Document"):
        """Adds plain text directly to the document store with a title."""
        self.documents.append(text)
        self.document_titles.append(title)
        self.document_priority[title] = 5.0  # Initialize priority with a neutral score

    def add_pdf(self, pdf_path):
        """Extracts text from a PDF file using pymupdf and adds it to the document store."""
        try:
            text = ""
            with pymupdf.open(pdf_path) as pdf:
                for page in pdf:
                    text += page.get_text()
            self.add_text(text, title=pdf_path)
            print(f"Text from PDF '{pdf_path}' added successfully.")
        except Exception as e:
            print(f"Failed to process PDF '{pdf_path}': {e}")

    def add_word(self, word_path):
        """Extracts text from a Word (.docx) file and adds it to the document store."""
        try:
            doc = DocxDocument(word_path)
            text = "\n".join([para.text for para in doc.paragraphs])
            self.add_text(text, title=word_path)
            print(f"Text from Word document '{word_path}' added successfully.")
        except Exception as e:
            print(f"Failed to process Word document '{word_path}': {e}")
    
    def add_excel(self, excel_path):
        """Extracts text from an Excel file and adds it to the document store."""
        try:
            df = pd.read_excel(excel_path)
            text = df.to_string()
            self.add_text(text, title=excel_path)
            print(f"Text from Excel file '{excel_path}' added successfully.")
        except Exception as e:
            print(f"Failed to process Excel file '{excel_path}': {e}")
    
    def caching(self, query, result):
        """Stores the result of a query in the cache."""
        self.cache[query] = result
        
    def gpt4_compare_similarity(self, query, doc):
        """Uses GPT-4 to compare the relevance of a document to a query."""
        prompt = f"Consider the query:\n'{query}'\nHow relevant is the following document to this query?\n'{doc}'\nAnswer with a relevance score from 1 (not relevant) to 10 (highly relevant). Only provide the numerical score."
    
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=10,
                temperature=0
            )
            score_text = response.choices[0].message.content.strip().split()[0]
            score = int(score_text)
            return score
        except ValueError as ve:
            print(f"Error parsing score: {ve}")
            return 0
        except Exception as e:
            print(f"Error in GPT-4 similarity scoring: {e}")
            return 0

    def gpt4_answer_query(self, question, context):
        """Generates an answer using GPT-4 based on the provided context."""
        prompt = f"Answer the question: '{question}' based on the following context:\n{context}"
        
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100,
                temperature=0.5
            )
            answer = response.choices[0].message.content.strip()
            return answer
        except Exception as e:
            print(f"Error in GPT-4 answer generation: {e}")
            return "Error generating answer"
    
    def hybrid_search(self, query, top_k=5):
        """Performs hybrid search using semantic relevance and priority adjustment."""
        scored_results = []
        for idx, doc in enumerate(self.documents):
            title = self.document_titles[idx]
            base_score = self.gpt4_compare_similarity(query, doc)
            adjusted_score = base_score * self.document_priority[title]  # Adjust score based on document priority
            scored_results.append((doc, title, adjusted_score))
    
        # Sort documents by adjusted score (high to low) and select top_k
        scored_results = sorted(scored_results, key=lambda x: x[2], reverse=True)[:top_k]
        return [doc for doc, title, score in scored_results]
    
    def guardrails(self, response):
        """Ensures the response is safe and appropriate."""
        if any(word in response.lower() for word in ["inappropriate", "offensive"]):
            return "The response is not suitable."
        return response

    def feedback_loop(self, doc_title, feedback_score):
        """Stores feedback and dynamically adjusts document priority."""
        self.feedback_scores[doc_title].append(feedback_score)
        
        # Calculate the updated average score
        avg_score = sum(self.feedback_scores[doc_title]) / len(self.feedback_scores[doc_title])
        
        # Update document priority based on feedback
        if avg_score >= 7:
            self.document_priority[doc_title] = min(10, self.document_priority[doc_title] * 1.1)  # Cap at 10
            print(f"Document '{doc_title}' received high feedback (Average Score: {avg_score}). It will be prioritized.")
        else:
            self.document_priority[doc_title] = max(1, self.document_priority[doc_title] * 0.9)  # Floor at 1
            print(f"Document '{doc_title}' received low feedback (Average Score: {avg_score}). It will be deprioritized.")
    
    def evals(self):
        """Evaluates overall performance based on feedback trends and adjusts system behavior accordingly."""
        avg_priority = sum(self.document_priority.values()) / len(self.document_priority)
        print(f"Current average document priority: {avg_priority}")

    def process_query(self, query):
        """Main query processing function."""
        # Check cache first
        if query in self.cache:
            print("Retrieved result from cache.")
            return self.cache[query]
        
        # Perform hybrid search to retrieve top documents
        search_results = self.hybrid_search(query)
        
        # Use the most relevant document for answering
        context = search_results[0] if search_results else "No relevant document found."
        answer = self.gpt4_answer_query(query, context)
        
        # Cache the result and return answer
        self.caching(query, answer)
        return answer

# Example usage
rag_system = vobanRAG()

# Add a PDF document
rag_system.add_pdf("document.pdf")

# Add a Word document
rag_system.add_word("document.docx")

# Add an Excel document
rag_system.add_excel("document.xlsx")

# Ask a query
query = input("Enter your query: ")
print("Query:", query)
answer = rag_system.process_query(query)
print("Answer:", answer)

# Collect feedback score from the user
try:
    feedback_score = int(input("Please rate the quality of the answer (1-10): "))
    if 1 <= feedback_score <= 10:
        rag_system.feedback_loop("document.pdf", feedback_score)
        print("Feedback submitted. Thank you!")
    else:
        print("Invalid feedback score. Please enter a number between 1 and 10.")
except ValueError:
    print("Invalid input. Please enter an integer between 1 and 10.")

# Display overall evaluation
rag_system.evals()
