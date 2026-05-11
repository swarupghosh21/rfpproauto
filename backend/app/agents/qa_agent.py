# from services.llm_service import ask_llm
# from services.retriever import retrieve_relevant_chunks
# from utils.prompts import QUESTIONS

# def generate_answers(chunks):
#     results = []

#     for q in QUESTIONS:
#         top_chunks = retrieve_relevant_chunks(q, chunks)

#         context = "\n\n".join(top_chunks)

#         prompt = f"""
# You are an expert RFP analyst.

# Rules:
# 1. Answer ONLY from the provided context.
# 2. If answer is not found, return: "Not specified in RFP"
# 3. Do NOT assume or infer.
# 4. Keep answer concise.

# Context:
# {context}

# Question:
# {q}

# Answer:
# """

#         answer = ask_llm(prompt)

#         results.append({
#             "question": q,
#             "answer": answer.strip(),
#             "sources": top_chunks
#         })

#     return results
# from app.services.qa_service import generate_answers

# def qa_agent(state):
#     answers = generate_answers(state["chunks"])
#     return {**state, "answers": answers}

from app.services.qa_service import generate_answers


def qa_agent(state):
    # Build answers using the vector store over chunks plus the full RFP text
    answers = generate_answers(state["vector_store"], state["text"])
    return {**state, "answers": answers}