#src/router.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.agents.intent_agent import IntentAgent
from src.agents.search_agent import SearchAgent
from src.agents.qa_agent import QAAgent
from src.agents.future_works_agent import FutureWorksAgent
from src.agents.summarization_agent import SummarizationAgent
import os
import streamlit as st

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

class QuestionRequest(BaseModel):
    paper_path: str 
    question: str

class Router:
    def __init__(self):
        self.intent_agent = IntentAgent()
        self.qa_agent = QAAgent()
        self.agents = {
            "search": SearchAgent(),
            "qa": self.qa_agent,
            "future_works": FutureWorksAgent(),
            "summarize": SummarizationAgent()
        }
        self.retrieved_papers = {}  

    def route_query(self, query):
        intent = self.intent_agent.get_intent(query)
        agent = self.agents.get(intent)

        if agent:
            if intent == "search":
                response, papers = agent.solve(query)

                # Store papers correctly as {title: full_path}
                self.retrieved_papers = {
                    paper["title"]: os.path.abspath(f"papers/{paper['paper_number']}.pdf")
                    for paper in papers
                }

                return {"response": response, "papers": self.retrieved_papers}
            return {"response": agent.solve(query)}
        else:
            return {"response": "Sorry, I couldn't understand your query."}

    def route_question(self, paper_path, question):
        """Pass full paper path to QA system"""
        return self.qa_agent.answer_question(paper_path, question)

    def get_papers(self):
        return {"papers": self.retrieved_papers}

router = Router()

@app.post("/query")
def query_research_papers(request: QueryRequest):
    """API endpoint to handle research queries."""
    return router.route_query(request.query)

@app.post("/ask_question")
def ask_question(request: QuestionRequest):
    """API endpoint to ask questions about a selected paper."""
    if not request.paper_path or not request.question:
        raise HTTPException(status_code=400, detail="Missing paper path or question.")
    
    answer = router.route_question(request.paper_path, request.question)
    return {"answer": answer}

@app.get("/get_papers")
def get_retrieved_papers():
    """API endpoint to get the list of retrieved papers."""
    return router.get_papers()
