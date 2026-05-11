from app.services.parser import parse_pdf

def intake_agent(state):
    text = parse_pdf(f"uploads/{state['filename']}")
    return {**state, "text": text}