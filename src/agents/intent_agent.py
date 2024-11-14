from config.config import model

class IntentAgent:
    def __init__(self):
        self.model = model
        self.prompt = """You are an intent classifier for a research paper assistant. Given a user query, classify it into one of these categories:
        
        - "search": User wants to find relevant research papers on a topic
        - "qa": User has questions about specific papers or content
        - "future_works": User wants to:
            * Generate future work ideas for a review paper
            * Create a structured review paper summary
            * Generate improvement plans from research works
            * Combine multiple papers for new research directions
            * Review paper generation
            * Synthesize multiple papers
        - "summarize": User wants to:
            * Summarize findings from multiple papers over a given timeframe
            * Extract key information from multiple papers and present it
        
        Example queries and their intents:
        "Find papers about machine learning" -> "search"
        "What does the paper say about the methodology?" -> "qa"
        "What future directions can I include in my review?" -> "future_works"
        "Can you help me write a literature review?" -> "future_works"
        "How can I combine these papers into an improvement plan?" -> "future_works"
        "What are the gaps in current research?" -> "future_works"
        "Summarize findings on neural networks from these papers" -> "summarize"
        "Extract key points from these papers" -> "summarize"
        
        Respond with just the intent category.
        
        Query: {query}"""

    
    def get_intent(self, query):
        response = self.model.generate_content(self.prompt.format(query=query))
        return response.text.strip().lower()
