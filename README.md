# Academic Research Paper Assistant

An intelligent assistant that helps researchers search, analyze, and synthesize academic papers using Large Language Models (LLMs). The application provides multi-agent capabilities for paper search, question answering, summarization, and future research direction generation.

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
git clone https://github.com/yourusername/research-paper-assistant.git
cd research-paper-assistant
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
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
streamlit run app.py
```

2. Open your browser and navigate to `http://localhost:8501`

3. Enter your research topic or question in the chat interface

4. Select papers of interest from the timeline view

5. Interact with the assistant through natural language queries

## Example Queries

- "Find papers about text-to-SQL"
- "What are the key findings in Paper X?"
- "Summarize the advancements in this field over the last 5 years"
- "What are potential future research directions?"
- "Generate a review paper outline"

## Project Structure

```
research-paper-assistant/
├── agents/
│   ├── __init__.py
│   ├── intent_agent.py
│   ├── search_agent.py
│   ├── qa_agent.py
│   ├── summarization_agent.py
│   └── future_works_agent.py
├── config/
│   └── config.py
├── papers/           # Downloaded papers storage
├── app.py           # Main Streamlit application
├── router.py        # Query routing logic
├── requirements.txt
└── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Streamlit](https://streamlit.io/) for the web interface framework
- [LangChain](https://python.langchain.com/) for LLM integration
- [Google Generative AI](https://ai.google.dev/) for the language model
- [Arxiv](https://arxiv.org/) for the research paper database

## Requirements

See `requirements.txt` for a full list of dependencies. Key requirements include:

```
streamlit
fastapi
langchain
google-generative-ai
faiss-cpu
pdfminer.six
```

## Development

To set up the development environment:

1. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

2. Run tests:
```bash
pytest tests/
```

3. Check code style:
```bash
flake8 .
black .
```

## Troubleshooting

### Common Issues

1. **Paper Download Failures**
   - Check your internet connection
   - Verify Arxiv API access
   - Ensure sufficient disk space

2. **Model Errors**
   - Verify Google API key is set
   - Check model quota limits
   - Ensure proper model initialization

3. **Memory Issues**
   - Reduce batch size for paper processing
   - Clear paper storage regularly
   - Monitor vector store size

### Support

For support, please:
1. Check existing issues on GitHub
2. Create a new issue with detailed reproduction steps
3. Include relevant error messages and logs
