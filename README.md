# Academic Research Paper Assistant

An intelligent assistant that helps researchers search, analyze, and synthesize academic papers using Large Language Models (LLMs). The application provides multi-agent capabilities for paper search, question answering, summarization, and future research direction generation.

![Front-End of app](src/imgs/HomePagepng.png)

![Front-End of app](src/imgs/HomePagepng.png)
## Try It Out

   **Tip:** In Streamlit website settings (by clicking on 3 dots in top right), change theme mode to "Light Mode" instead of "Dark Mode."

## Features

- **Paper Search**: Search and retrieve relevant research papers from Arxiv
- **Question Answering**: Get answers about specific papers or content with source citations
- **Summarization**: Extract key findings and trends from multiple papers
- **Future Works Generation**: Generate research directions and improvement plans
- **Interactive UI**: User-friendly Streamlit interface for paper browsing and chat

## Architecture

The application uses a multi-agent system with the following components:

- **Intent Agent**: Classifies user queries to route to appropriate specialized agents
- **Search Agent**: Retrieves and processes papers from Arxiv
- **QA Agent**: Handles specific questions about paper content
- **Summarization Agent**: Synthesizes information across multiple papers
- **Future Works Agent**: Generates research directions and review papers

## Technology Stack

- **Frontend**: Streamlit
- **Backend**: FastAPI
- **LLM Integration**: Google Generative AI
- **Vector Store**: FAISS
- **Document Processing**: LangChain
- **PDF Processing**: PDFMiner

## Installation

1. Clone the repository:
```bash
git clone https://github.com/
```

2. Create and activate a virtual environment:
```bash
conda create --name venv
conda activate venv
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
# Create .env file
GOOGLE_API_KEY=your_api_key_here
```
## Usage

1. Start the application:
```bash
cd src
streamlit run app.py
# or run  following 
# python3 -m streamlit run app.py
```

2. Open your browser and navigate to `http://localhost:8501` 

   **Tip:** In Streamlit website settings (by clicking on 3 dots in top right), change theme mode to "Light Mode" instead of "Dark Mode."
  
4. Enter your research topic or question in the chat interface

5. Select papers of interest from the timeline view

6. Interact with the assistant through natural language queries

## Example Queries

- "Find papers about text-to-SQL"
- "What are the key findings in Paper X?"
- "Summarize the advancements in this field over the last 5 years"
- "What are potential future research directions?"
- "Generate a review paper outline"

## Project Structure

```

## 🖥️ Project Structure
```bash
academic-research-assistant/
├── src/
│   ├── app.py             # Streamlit frontend
│   ├── router.py          # API routing & logic
│   ├── config/
│   │   ├── config.py      # Configuration settings
│   ├── agents/
│   │   ├── search_agent.py   # Handles search functionality
│   │   ├── qa_agent.py       # Handles Q&A system
│   │   ├── summarization_agent.py  # Summarization logic
│   ├── database/
│   │   ├── neo4j_client.py  # Graph database integration
│   ├── models/
│   │   ├── llm_manager.py   # LLM API integration
│   ├── frontend/
│   │   ├── ui.py            # UI styling & components
├── papers/                  # Downloaded research papers
├── requirements.txt          # Python dependencies
├── README.md                 # Documentation
```



## Acknowledgments

- [Streamlit](https://streamlit.io/) for the web interface framework
- [LangChain](https://python.langchain.com/) for LLM integration
- [Google Generative AI](https://ai.google.dev/) for the language model
- [Arxiv](https://arxiv.org/) for the research paper database

## Requirements

See `requirements.txt` for a full list of dependencies. Key requirements include:

```
langchain-google-genai
langchain-community
arxiv
pymupdf
faiss-cpu
pdfminer.six
google-generativeai
streamlit
fastapi
langchain
```


## 🤝 Contributing

We welcome contributions! Follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit changes (`git commit -m "Added new feature"`).
4. Push to the branch (`git push origin feature-branch`).
5. Submit a pull request.
---

## 📜 License
This project is licensed under the MIT License.

---

## 📬 Contact
For issues, suggestions, or feedback, feel free to reach out:
- GitHub Issues: [Create an Issue](https://github.com/digantadiasi195/academic-research-assistant/issues)
- Email: digantadiasi@gmail.com

Happy researching!
