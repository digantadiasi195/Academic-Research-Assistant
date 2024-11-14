from langchain.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
import streamlit as st
from agents import SearchAgent
from config.config import model


            
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

class SummarizationAgent:
    def __init__(self):
        self.model = model
        self.prompt = """You are a research assistant tasked with synthesizing findings from multiple academic papers over time. Your goal is to create a comprehensive summary that highlights key trends, thematic developments, and methodological evolution within a given timeframe.

                        Given the following context, analyze the papers to produce a structured summary:

                        Previous conversation:
                        {chat_history}

                        Papers context:
                        {context}

                        Guidelines for timeline-based summarization:

                        Key Findings and Trends Over Time

                        Identify major discoveries and conclusions, highlighting how they have developed chronologically.
                        Note emerging trends, consensus, and any evolving contradictions across papers, especially in response to new technologies or shifts in the field.
                        Present statistical evidence and experimental results in relation to time, pointing out any measurable improvements or declines over the years.
                        Methodological Evolution

                        Compare and contrast research approaches across different time periods, emphasizing changes or advances in data collection, analysis techniques, or tools.
                        Identify and describe innovative methodological contributions and how these may have impacted research outcomes over time.
                        Theoretical Progression

                        Outline the theoretical foundations and highlight their chronological development.
                        Connect findings to existing theories, noting how interpretations or theoretical perspectives have evolved.
                        Identify theoretical advances, challenges, or shifts and their relationship to the timeline.
                        Practical Applications and Temporal Shifts

                        Discuss real-world applications over time, noting how findings have influenced industry practices or technology adoption.
                        Highlight evolving practical use cases and how implementation considerations have changed with advances in research.
                        Research Gaps and Future Directions

                        Identify limitations in studies across time periods, noting any improvement or persistent gaps.
                        Point out unexplored areas and suggest specific future research directions informed by chronological developments in the field.
                        Formatting and Style:

                        Organize the summary with clear sections that reflect the temporal progression.
                        Maintain an academic tone, using specific examples, dates, and quotes where relevant.
                        Clearly identify and label sections to enhance readability, and acknowledge any limitations in the available context.
        """
        
        self.papers = None
        self.search_agent_response = ""

    def solve(self, query):
        # Check if search has been performed
        if not os.path.exists("vector_db"):
            st.warning("No papers loaded. Performing search first...")
            search_agent = SearchAgent()
            self.search_agent_response, self.papers = search_agent.solve(query)
            
        # Load vector store
        vector_db = FAISS.load_local("vector_db", embeddings, index_name="base_and_adjacent", allow_dangerous_deserialization=True)
        
        # Get chat history
        chat_history = st.session_state.get("chat_history", [])
        chat_history_text = "\n".join([f"{sender}: {msg}" for sender, msg in chat_history[-5:]])
        
        # Get relevant chunks from all papers
        retrieved = vector_db.as_retriever(
            search_kwargs={"k": 10}  # Increase number of chunks to get broader context
        ).get_relevant_documents(query)
        
        # Organize context by paper
        context = self._organize_context(retrieved)
        
        # Generate summary
        full_prompt = self.prompt.format(
            chat_history=chat_history_text,
            context=context
        )
        
        response = self.model.generate_content(str(self.search_agent_response) + full_prompt)
        return response.text, self.papers

    def _organize_context(self, documents):
        """
        Organizes retrieved chunks by paper and creates a structured context.
        """
        # Group chunks by paper
        paper_chunks = {}
        for doc in documents:
            paper_id = doc.metadata.get('source', 'unknown')
            if paper_id not in paper_chunks:
                paper_chunks[paper_id] = []
            paper_chunks[paper_id].append(doc.page_content)

        # Create structured context
        organized_context = []
        for paper_id, chunks in paper_chunks.items():
            paper_context = f"\nPaper: {paper_id}\n"
            paper_context += "\n".join(chunks)
            organized_context.append(paper_context)

        return "\n\n".join(organized_context)