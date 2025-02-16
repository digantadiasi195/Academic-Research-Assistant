# Academic Research Paper Assistant

An intelligent assistant that helps researchers search, analyze, and synthesize academic papers using Large Language Models (LLMs). The application offers multi-agent capabilities for paper search, question answering, summarization, and future research direction generation.

<div align="center">
  <img src="src/imgs/HomePagepng.png" alt="Front-End of App" width="600" />
</div>

<div align="center">
  <img src="src/imgs/Q1.png" alt="Search paper of App" width="300" />
  <img src="src/imgs/Q3.png" alt="Query of App" width="300" />
</div>

---

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Example Queries](#example-queries)
- [Project Structure](#project-structure)
- [Acknowledgments](#acknowledgments)
- [Requirements](#requirements)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## Features

- **Paper Search**: Retrieve relevant research papers from Arxiv.
- **Question Answering**: Get detailed answers about paper content with source citations.
- **Summarization**: Extract key insights and trends from multiple papers.
- **Future Works Generation**: Generate potential research directions and improvement plans.
- **Interactive UI**: User-friendly interface built with Streamlit for paper browsing and chatting.

---

## Architecture

The application employs a multi-agent system that includes:

- **Intent Agent**: Classifies user queries to direct them to the appropriate specialized agents.
- **Search Agent**: Retrieves and processes research papers from Arxiv.
- **QA Agent**: Handles specific questions related to paper content.
- **Summarization Agent**: Synthesizes key findings from multiple papers.
- **Future Works Agent**: Proposes future research directions and outlines for review papers.

---

## Technology Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Backend**: [FastAPI](https://fastapi.tiangolo.com/)
- **LLM Integration**: [Google Generative AI](https://ai.google.dev/)
- **Vector Store**: FAISS
- **Document Processing**: [LangChain](https://python.langchain.com/)
- **PDF Processing**: PDFMiner

---

## Installation

To set up the project locally, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/academic-research-assistant.git
