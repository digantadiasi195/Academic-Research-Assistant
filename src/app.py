import streamlit as st
import os
import sys
from typing import Tuple, List, Dict
from router import Router

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class AcademicResearchAssistant:
    def __init__(self):
        self.router = Router()
        self.setup_streamlit_config()
        self.initialize_session_state()

    def setup_streamlit_config(self):
        """Configures Streamlit page settings"""
        st.set_page_config(
            page_title="Academic Research Assistant",
            page_icon="📚",
            layout="wide",
            initial_sidebar_state="expanded"
        )

        # CSS
        st.markdown(
            """
            <style>
                body {
                    background-color: #f5f7fa;
                }
                .stTextInput, .stSelectbox, .stButton>button {
                    font-size: 16px !important;
                    border-radius: 8px !important;
                    padding: 10px !important;
                }
                .stButton>button {
                    background-color: #1f77b4 !important;
                    color: white !important;
                    border: none;
                }
                .paper-card {
                    background-color: #ffffff;
                    padding: 15px;
                    border-radius: 10px;
                    box-shadow: 0px 2px 4px rgba(0,0,0,0.1);
                    margin-bottom: 10px;
                    color: black;  /* Ensure text is readable */
                }
                .answer-box {
                    background-color: #e8f4f8 !important;
                    padding: 15px;
                    border-radius: 8px;
                    font-size: 16px;
                    color: black !important; /* Ensure text is visible */
                }
            </style>
            """,
            unsafe_allow_html=True
        )

    def initialize_session_state(self):
        """Initializes session state variables"""
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        if "fetched_papers" not in st.session_state:
            st.session_state.fetched_papers = []
        if "selected_paper" not in st.session_state:
            st.session_state.selected_paper = None
        if "selected_paper_title" not in st.session_state:
            st.session_state.selected_paper_title = None
        if "papers_directory" not in st.session_state:
            st.session_state.papers_directory = os.path.join(os.getcwd(), "papers") 
        if "paper_titles" not in st.session_state:
            st.session_state.paper_titles = {}  # Mapping: {title -> filename}
        if "total_searches" not in st.session_state:
            st.session_state.total_searches = 0  

    def display_welcome_section(self):
        """Displays the welcome section with key features"""
        st.title("📚 Academic Research Paper Assistant")
        # st.markdown("""
        #     Welcome to your intelligent research companion! This tool helps you:
        #     - 🔍 **Find relevant academic papers**
        #     - 📊 **Analyze research trends**
        #     - 📖 **Access paper summaries**
        #     - 📥 **Download full papers**
        # """)
        
        # Display Metrics
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(""" 
            This tool helps you:
            - 🔍 **Find relevant academic papers**
            - 📊 **Analyze research trends**
            - 📖 **Access paper summaries**
            - 📥 **Download full papers**
        """, unsafe_allow_html=True)

        with col2:
            st.markdown(
            f"""
            <div style="display: flex; justify-content: space-between;">
                <div style="width: 48%; text-align: center; padding: 15px; 
                            background-color: #222831; color: #ffffff; 
                            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2); 
                            border-radius: 10px;">
                    <h4 style="color: #eeeeee;">Papers Found</h4>
                    <h2 style="color: #00ADB5;">{len(st.session_state.fetched_papers)}</h2>
                </div>
                <div style="width: 48%; text-align: center; padding: 15px; 
                            background-color: #222831; color: #ffffff; 
                            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2); 
                            border-radius: 10px;">
                    <h4 style="color: #eeeeee;">Total Searches</h4>
                    <h2 style="color: #00ADB5;">{st.session_state.total_searches}</h2>
                </div>
            </div>
            """,
            unsafe_allow_html=True
            )

    def create_chat_interface(self) -> Tuple[str, bool]:
        """Creates the search query input interface"""
        with st.container():
            st.subheader("💬 Research Query Interface")
            
            col1, col2 = st.columns([7, 2])
            with col1:
                user_input = st.text_input(
                    "Enter your research query",
                    key="user_input",
                    placeholder="Type your research topic here...",
                    max_chars=500
                )
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)
                send_button = st.button("🔍 Search", use_container_width=True)

        return user_input, send_button

    def process_user_input(self, user_input: str):
        """Processes user input and fetches relevant papers"""
        if not user_input.strip():
            st.warning("⚠️ Please enter a valid research query.")
            return
        with st.spinner('🔍 Fetching relevant papers...'):
            response = self.router.route_query(user_input)

            # ✅ Ensure Total Searches increments properly
            st.session_state.total_searches += 1  

            if response.get("papers"):
                papers = response["papers"]
                st.session_state.fetched_papers = papers
                st.session_state.paper_titles = papers  # Store mapping correctly
            else:
                st.session_state.chat_history.append(
                    ("Assistant", "No relevant papers found. Try another query.")
                )

    def display_papers(self):
        """Displays the list of retrieved papers"""
        st.subheader("📄 Retrieved Research Papers")

        paper_titles = list(st.session_state.paper_titles.keys())

        if paper_titles:
            selected_title = st.selectbox("Select a paper for QA", paper_titles)
            st.session_state.selected_paper_title = selected_title
            selected_path = st.session_state.paper_titles[selected_title]
            st.session_state.selected_paper = selected_path

            # **Fixed: Ensure text visibility**
            st.markdown(
                f"""
                   <div class="paper-card">
                   <h4>📄 <strong style="color: black;">{selected_title}</strong></h4>
                   </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.info("🔍 No papers available. Please search first.")

    def create_question_interface(self):
        """Creates the QA interface for the selected paper"""
        if st.session_state.selected_paper:
            selected_title = st.session_state.selected_paper_title
            selected_file_path = st.session_state.selected_paper

            st.subheader(f"📝 Ask a Question on {selected_title}")
            question = st.text_input("Enter your question:")

            if st.button("🔎 Get Answer"):
                with st.spinner("Processing your question..."):
                    if os.path.exists(selected_file_path):
                        response = self.router.route_question(selected_file_path, question)
                        
                        # **Fixed: Ensure answer box is visible**
                        st.markdown(
                            f"""
                            <div class="answer-box">
                                <h4 style="color: black;">🤖 Answer:</h4>
                                <p style="color: black;">{response}</p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    else:
                        st.error(f"❌ Error: Paper not found at `{selected_file_path}`")
                        st.write("🔍 Please check if the paper exists in the `papers/` directory.")

    def run(self):
        """Runs the main application"""
        self.display_welcome_section()
        
        user_input, send_button = self.create_chat_interface()

        if user_input and send_button:
            self.process_user_input(user_input)
            st.rerun()

        self.display_papers()
        self.create_question_interface()

def main():
    app = AcademicResearchAssistant()
    app.run()

if __name__ == "__main__":
    main()
