from config import model
from langchain.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
from agents import  SearchAgent
import streamlit as st

            
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

class FutureWorksAgent:
    def __init__(self):
        self.model = model
        self.prompt = """Analyze the research context and provide targeted insights based on the specific task type.
        
        Previous conversation:
        {chat_history}
        
        Current research context:
        {context}
        
        Task Type Detection:
        1. Review Paper Future Work:
           If the query involves generating future work for a review paper:
           - Identify emerging trends and unexplored areas
           - Suggest potential research questions
           - Outline methodology gaps
           - Propose innovative approaches
        
        2. Structured Review Summary:
           If the query involves creating a review paper summary:
           - Synthesize key findings across papers
           - Identify major research themes
           - Highlight methodological approaches
           - Present conflicting results or debates
           - Suggest future research opportunities
        
        3. Improvement Plan:
           If the query involves generating an improvement plan:
           - Analyze existing solutions and their limitations
           - Identify potential enhancements
           - Suggest novel technical contributions
           - Propose validation approaches
           - Outline implementation steps
        
        4. Research Direction Synthesis:
           If the query involves combining multiple papers:
           - Identify common themes and patterns
           - Highlight complementary approaches
           - Suggest novel combinations of methods
           - Propose new research directions
           - Outline potential experimental designs
        
        Format Guidelines:
        - Begin with identifying the specific task type
        - Provide structured, section-wise response
        - Include specific examples from papers
        - List concrete action items or suggestions
        - Acknowledge limitations and assumptions
        - Suggest validation approaches
        
        Note: Focus on providing actionable, specific suggestions rather than general statements.
        Consider both theoretical advances and practical implementations.
        """
        
        self.papers = None
        self.search_agent_response  = ""

    def solve(self, query):
        # Check if search has been performed
        if not os.path.exists("vdb_chunks"):
            st.warning("No papers loaded. Performing search first...")
            search_agent = SearchAgent()
            self.search_agent_response , self.papers = search_agent.solve(query)
            
        # Load vector store
        vdb_chunks = FAISS.load_local("vdb_chunks", embeddings, index_name="base_and_adjacent", allow_dangerous_deserialization=True)
        
        # Get chat history
        chat_history = st.session_state.get("chat_history", [])
        chat_history_text = "".join([f"{sender}: {msg}" for sender, msg in chat_history[-5:]])
        
        # Get relevant chunks
        retrieved = vdb_chunks.as_retriever().get_relevant_documents(query)
        context = "".join([f"{doc.page_content}\n Source: {doc.metadata['source']}" for doc in retrieved])
        
        # Generate response
        full_prompt = self.prompt.format(
            chat_history=chat_history_text,
            context=context
        )
        response = self.model.generate_content(str(self.search_agent_response) + full_prompt)
        return response.text , self.papers