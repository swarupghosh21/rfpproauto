from app.services.llm_service import ask_llm

def generate_queries(text):

    prompt = f"""
Generate clarification questions from this RFP:

{text[:4000]}
"""

    response = ask_llm(prompt)

    return response.split("\n")