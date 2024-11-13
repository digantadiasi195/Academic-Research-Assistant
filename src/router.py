from agents import IntentAgent, SearchAgent, QAAgent, FutureWorksAgent , SummarizationAgent
import streamlit as st
class Router:
    def __init__(self):
        self.intent_agent = IntentAgent()
        self.agents = {
            "search": SearchAgent(),
            "qa": QAAgent(),
            "future_works": FutureWorksAgent(),
            "summarize": SummarizationAgent()
        }

    def route_query(self, query):
        
        intent = self.intent_agent.get_intent(query)
        agent = self.agents.get(intent)
        st.write(f"Using {intent} agent...")
        if agent:
            if intent == "search":
                ans , d = agent.solve(query)
                return ans , d
            return agent.solve(query) , None
        else:
            return "Sorry, I couldn't understand your query." , None
