# #qa_agent.py 
# import os
# import streamlit as st 
# from agents import  SearchAgent
# from langchain_community.vectorstores import FAISS
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from config.config import model
# from agents.google_credentials import get_google_credentials
# # Get the credentials from the google_credentials.py file
# credentials = get_google_credentials()

            
# embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", credentials=credentials)

# class QAAgent:
#     def __init__(self):
        
#         self.model = model
#         self.prompt = """You are a research assistant answering questions about academic papers. Use the following context from papers and chat history to provide accurate, specific answers.

#         Previous conversation:
#         {chat_history}

#         Paper context:
#         {context}

#         Question: {question}

#         Guidelines:
#         1. Reference specific papers when making claims
#         2. Use direct quotes when relevant
#         3. Acknowledge if information isn't available in the provided context
#         4. Maintain academic tone and precision
#         """
#         self.papers = None
#         self.search_agent_response  = ""

#     def solve(self, query):
#         # Check if search has been performed
#         if not os.path.exists("vector_db"):
#             st.warning("No papers loaded. Performing search first...")
#             search_agent = SearchAgent()
#             self.search_agent_response , self.papers = search_agent.solve(query)
            
#         # Load vector store
#         vector_db = FAISS.load_local("vector_db", embeddings, index_name="base_and_adjacent", allow_dangerous_deserialization=True)
        
#         # Get chat history
#         chat_history = st.session_state.get("chat_history", [])
#         chat_history_text = "".join([f"{sender}: {msg}" for sender, msg in chat_history[-5:]])  # Last 5 messages
        
#         # Get relevant chunks
#         retrieved = vector_db.as_retriever().get_relevant_documents(query)
#         context = "".join([f"{doc.page_content}\n Source: {doc.metadata['source']}" for doc in retrieved])
        
#         # Generate response
#         full_prompt = self.prompt.format(
#             chat_history=chat_history_text,
#             context=context,
#             question=query
#         )
        
#         response = self.model.generate_content(str(self.search_agent_response)  + full_prompt)
#         return response.text , self.papers
############################################################################################
# import fitz  # PyMuPDF
# import streamlit as st
# import os
# from langchain_community.vectorstores import FAISS
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from src.config.config import model
# from src.agents.google_credentials import get_google_credentials

# # Get Google credentials
# credentials = get_google_credentials()
# embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", credentials=credentials)

# class QAAgent:
#     def __init__(self):
#         self.model = model
#         self.prompt_template = """You are an academic assistant answering questions from research papers.

#         Paper Extract:
#         {paper_text}

#         Question: {question}

#         Guidelines:
#         1. Provide precise, well-referenced answers.
#         2. Use direct quotes when necessary.
#         3. If information isn't available, mention it.
#         """

#     def extract_text_from_pdf(self, pdf_path):
#         """Extracts text from a PDF file."""
#         doc = fitz.open(pdf_path)
#         text = "\n".join([page.get_text() for page in doc])
#         return text[:5000]  # Limit text to avoid exceeding LLM token limits

#     def answer_question(self, paper_id, question):
#         paper_path = f"papers/{paper_id}.pdf"
#         if not os.path.exists(paper_path):
#             return "Error: Selected paper not found."

#         # Extract text from PDF
#         paper_text = self.extract_text_from_pdf(paper_path)

#         # Prepare LLM prompt
#         full_prompt = self.prompt_template.format(
#             paper_text=paper_text,
#             question=question
#         )

#         # Get LLM response
#         response = self.model.generate_content(full_prompt)
#         return response.text
############################################################################
import fitz  # PyMuPDF
import streamlit as st
import os
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from src.config.config import model
from src.agents.google_credentials import get_google_credentials

# Get Google credentials
credentials = get_google_credentials()
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", credentials=credentials)

class QAAgent:
    def __init__(self):
        self.model = model
        self.prompt_template = """You are an academic assistant answering questions from research papers.

        Paper Extract:
        {paper_text}

        Question: {question}

        Guidelines:
        1. Provide precise, well-referenced answers.
        2. Use direct quotes when necessary.
        3. If information isn't available, mention it.
        """

    def extract_text_from_pdf(self, pdf_path):
        """Extracts text from a PDF file."""
        try:
            doc = fitz.open(pdf_path)
            text = "\n".join([page.get_text() for page in doc])
            return text[:5000]  # Limit text to avoid exceeding LLM token limits
        except Exception as e:
            st.error(f"❌ Error extracting text from PDF: {str(e)}")
            return ""

    def answer_question(self, paper_path, question):
        """Handles question answering using the selected paper"""
        
        # Debugging: Print the file path received
        # st.write(f" **DEBUG:** QAAgent Received Paper Path → `{paper_path}`")

        # Ensure file exists before processing
        if not os.path.exists(paper_path):
            st.error(f"❌ **DEBUG:** QAAgent File Not Found → `{paper_path}`")
            return "Error: Selected paper not found."

        # Extract text from PDF
        paper_text = self.extract_text_from_pdf(paper_path)
        if not paper_text:
            return "Error: Unable to extract content from the selected paper."

        # Prepare LLM prompt
        full_prompt = self.prompt_template.format(
            paper_text=paper_text,
            question=question
        )

        # Get LLM response
        response = self.model.generate_content(full_prompt)
        return response.text
