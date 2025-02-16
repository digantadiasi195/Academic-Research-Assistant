import requests
import os
import urllib.request as libreq
import xml.etree.ElementTree as ET
from langchain_community.document_loaders import PDFMinerLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import ArxivLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from src.config.config import model
from src.agents.google_credentials import get_google_credentials

# Ensure the "papers" directory exists
os.makedirs("papers", exist_ok=True)

# Load credentials
credentials = get_google_credentials()

# Initialize Google Embeddings
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", credentials=credentials)

# Initialize FAISS Index
index = faiss.IndexFlatL2(len(embeddings.embed_query("dummy query")))

# Text Splitter for processing documents
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=700,
    chunk_overlap=0,
    length_function=len
)

class SearchAgent:
    def __init__(self):
        self.model = model
        self.prompt_template = """You are an assistant designed to extract research topics or titles from user queries. 
        When a user asks about a specific topic, identify the central subject of their query and provide a concise, clear title 
        or topic related to that area of research. If the query refers to a particular research paper, extract the title, author(s), 
        and publication year.

        Examples:
        - "Recent advancements in text-to-SQL models" → "Text-to-SQL Models"
        - "What does the paper 'Deep Learning for NLP by John Doe, 2022' discuss?" → "'Deep Learning for NLP' (John Doe, 2022)"
        """

    def solve(self, task):
        """Fetches relevant research papers using semantic retrieval from ArXiv API."""
        print(f"🔎 Searching for information on: {task}")

        # Generate search query
        response = model.generate_content(self.prompt_template + task)
        search_query = response.text.strip()

        # Convert query to ArXiv API format
        formatted_query = "%20".join(search_query.split())

        # Query ArXiv API
        arxiv_url = f"http://export.arxiv.org/api/query?search_query=all:{formatted_query}&sortBy=relevance&sortOrder=descending&start=0&max_results=5"
        with libreq.urlopen(arxiv_url) as url:
            xml_response = url.read()

        # Parse XML response
        root = ET.fromstring(xml_response)
        ns = {'atom': 'http://www.w3.org/2005/Atom'}

        papers = []
        for entry in root.findall('atom:entry', ns):
            paper_info = {
                "title": entry.find('atom:title', ns).text,
                "link": entry.find('atom:id', ns).text.replace("abs", "pdf"),
                "year": entry.find('atom:published', ns).text[:4]  # Extract year
            }
            papers.append(paper_info)

        # Ensure relevant papers are retrieved
        if not papers:
            return "No relevant papers found.", []

        downloaded_papers = []
        
        def download_paper(url):
            """Downloads the PDF from the given URL and saves it locally."""
            paper_number = os.path.basename(url).replace(".pdf", "")
            pdf_path = f"papers/{paper_number}.pdf"
            
            try:
                res = requests.get(url, timeout=10)
                with open(pdf_path, 'wb') as f:
                    f.write(res.content)
                return paper_number
            except Exception as e:
                print(f"❌ Failed to download {url}: {e}")
                return None

        # Download all papers
        for paper in papers:
            paper_number = download_paper(paper['link'])
            if paper_number:
                downloaded_papers.append(paper_number)
                paper['paper_number'] = paper_number

        # Setup FAISS vector database
        vector_db = FAISS(
            embedding_function=embeddings,
            index=index,
            docstore=InMemoryDocstore(),
            index_to_docstore_id={}
        )

        # Process papers for FAISS indexing
        for pdf_number in downloaded_papers:
            docs = PDFMinerLoader(f"papers/{pdf_number}.pdf").load()
            split_docs = text_splitter.split_documents(docs)
            vector_db.add_documents(split_docs)

        # Save FAISS index
        vector_db.save_local("vector_db", index_name="base_and_adjacent")

        return f"✅ {len(papers)} relevant papers found.", papers
