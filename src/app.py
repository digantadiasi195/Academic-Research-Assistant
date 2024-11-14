import streamlit as st
import os
import sys
from typing import Tuple, List, Dict, Optional
from router import Router

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class AcademicResearchAssistant:
    def __init__(self):
      
        self.router = Router()
        self.setup_streamlit_config()
        self.initialize_session_state()

    def setup_streamlit_config(self):
    
        st.set_page_config(
            page_title="Academic Research Assistant",
            page_icon="📚",
            layout="wide",
            initial_sidebar_state="expanded",
            menu_items={
                'Get Help': 'https://github.com/yourusername/academic-research-assistant',
                'Report a bug': "https://github.com/yourusername/academic-research-assistant/issues",
                'About': "# Academic Research Assistant v1.0\nYour intelligent research companion."
            }
        )

        # Custom CSS to enhance the UI
        st.markdown("""
            <style>
            .stApp {
                background: linear-gradient(to bottom right, #f5f7fa, #eef2f7);
            }
            .stButton>button {
                background-color: #1f4287;
                color: white;
                border-radius: 5px;
                padding: 0.5rem 1rem;
            }
            .stProgress .st-bo {
                background-color: #1f4287;
            }
            .chat-message {
                padding: 10px;
                border-radius: 5px;
                margin: 5px 0;
                animation: fadeIn 0.5s ease-in;
            }
            .user-message {
                background-color: #e6f3ff;
            }
            .bot-message {
                background-color: #f0f2f6;
            }
            @keyframes fadeIn {
                from {opacity: 0;}
                to {opacity: 1;}
            }
            .paper-card {
                background-color: white;
                padding: 1.5rem;
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                margin-bottom: 1rem;
            }
            .paper-title {
                color: #1f4287;
                font-size: 1.1rem;
                font-weight: bold;
                margin-bottom: 0.5rem;
            }
            .paper-metadata {
                font-size: 0.9rem;
                color: #666;
                margin-bottom: 0.5rem;
            }
            .paper-abstract {
                font-size: 0.95rem;
                line-height: 1.5;
                margin-top: 1rem;
                padding-left: 1rem;
                border-left: 3px solid #1f4287;
            }
            .download-button {
                background-color: #4CAF50;
                color: white;
                padding: 0.5rem 1rem;
                border-radius: 5px;
                text-decoration: none;
                display: inline-block;
                margin-top: 1rem;
            }
            .metric-card {
                background-color: white;
                padding: 1rem;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.05);
                text-align: center;
            }
            </style>
        """, unsafe_allow_html=True)

    def initialize_session_state(self):
       
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        if "fetched_papers" not in st.session_state:
            st.session_state.fetched_papers = []
        if "search_count" not in st.session_state:
            st.session_state.search_count = 0
        if "total_searches" not in st.session_state:
            st.session_state.total_searches = 0

    def display_welcome_message(self):

        st.title("📚 Academic Research Paper Assistant")
        
        # Create three columns for metrics
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        
        with col1:
            st.markdown("""
            Welcome to your intelligent research companion! This tool helps you:
            - 🔍 Find relevant academic papers
            - 📊 Analyze research trends
            - 📖 Access paper summaries
            - 📥 Download full papers
            """)
        
        # Display metrics in cards
        with col3:
            st.markdown("""
                <div class="metric-card">
                    <h3>Papers Found</h3>
                    <h2>{}</h2>
                </div>
            """.format(len(st.session_state.fetched_papers)), unsafe_allow_html=True)
            
        with col4:
            st.markdown("""
                <div class="metric-card">
                    <h3>Total Searches</h3>
                    <h2>{}</h2>
                </div>
            """.format(st.session_state.total_searches), unsafe_allow_html=True)
      
        

    def create_chat_interface(self) -> Tuple[str, bool]:
       
        with st.container():
            st.write("### 💬 Research Query Interface")
            
            # Create columns for better layout
            col1, col2 = st.columns([4, 1])
            
            with col1:
                user_input = st.text_input(
                    "Enter your research query (e.g., 'Recent advances in quantum computing')",
                    key="user_input",
                    placeholder="Type your research question here...",
                    max_chars=500
                )
            
            col3, col4, col5 = st.columns([2, 1, 1])
            with col3:
                send_button = st.button("🔍 Search ", use_container_width=True)
            with col4:
                clear_button = st.button("🗑️ Clear History", use_container_width=True)
            
            if clear_button:
                st.session_state.chat_history = []
                st.session_state.fetched_papers = []
                st.session_state.search_count = 0
                st.session_state.total_searches = 0
                st.rerun()
                
        return user_input, send_button

    def process_user_input(self, user_input: str):
        
        with st.spinner('🔍 Working on response...'):
            # Update search metrics
            st.session_state.search_count = len(st.session_state.fetched_papers)
            st.session_state.total_searches += 1
            
            try:
                # Get response from router
                response, papers = self.router.route_query(user_input)
                
                # Update papers in session state
                if papers:
                    unique_papers = {paper['paper_number']: paper for paper in papers}
                    st.session_state.fetched_papers = list(unique_papers.values())
                
                # Add bot response and use message to chat history
                if response:
                    st.session_state.chat_history.append(("Bot", response))
                    st.session_state.chat_history.append(("User", user_input))
                else:
                    st.session_state.chat_history.append(
                        ("Bot", "I couldn't find relevant papers for your query. Please try rephrasing or use more specific terms.")
                    )
            except Exception as e:
                st.session_state.chat_history.append(
                    ("Bot", f"An error occurred while processing your request: {str(e)}")
                )
                st.error("There was an error processing your request. Please try again.")

    def display_chat_history(self):
        """Display the chat history with user and bot messages"""
        for sender, message in reversed(st.session_state.chat_history):
            if sender == "User":
                st.markdown(
                    "<div class='chat-message user-message'>"
                    f"<strong>👤 You:</strong> {message}"
                    "</div>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    "<div class='chat-message bot-message'>"
                    f"<strong>🤖 Assistant:</strong> {message[0]}"
                    "</div>",
                    unsafe_allow_html=True
                )

    def display_papers(self):
        """Display the list of fetched papers with download links"""
        st.write("### 📄 Retrieved Research Papers")
        if st.session_state.fetched_papers:
            for paper in st.session_state.fetched_papers:
                with st.expander(f"📑 {paper.get('title', 'Untitled Paper')}"):
                    st.markdown(
                        "<div class='paper-card'>"
                        f"<div class='paper-title'>{paper.get('title', '').replace('\n', ' ').strip()}</div>"
                        f"<div class='paper-metadata'>Year: {paper.get('year', 'N/A')} | Paper ID: {paper.get('paper_number', 'N/A')}</div>"
                        f"""{'<div class="paper-abstract">' + paper.get('abstract', '') + '</div>' if paper.get('abstract') else ''}"""
                        "</div>",
                        unsafe_allow_html=True
                    )
                    
                    download_link = paper.get('link')
                    if download_link:
                        st.markdown(f"[📥 Download PDF]({download_link})")
                    else:
                        st.warning("⚠️ No download link available")
        else:
            st.info("🔍 No papers fetched yet. Start by entering a research query above!")

    def run(self):
        """Main method to run the application"""
        self.display_welcome_message()
        

        user_input, send_button = self.create_chat_interface()

        st.markdown("### 💬 Chat History")
        self.display_chat_history()
        

        if user_input and send_button:
            self.process_user_input(user_input)
            st.rerun()
        
        st.markdown("---")
        self.display_papers()

def main():

    app = AcademicResearchAssistant()
    app.run()

if __name__ == "__main__":
    main()