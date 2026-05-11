# from app.utils.prompts import QUESTIONS
# from app.services.llm_service import ask_llm

# def generate_answers(chunks):

#     results = []

#     for q in QUESTIONS:
#         context = "\n".join(chunks[:3])

#         prompt = f"""
# Answer ONLY from context. If not found say 'Not specified in RFP'

# Context:
# {context}

# Question:
# {q}
# """

#         answer = ask_llm(prompt)

#         results.append({
#             "question": q,
#             "answer": answer
#         })

#     return results

from app.services.llm_service import ask_llm
from app.services.retriever_rfp import retrieve_chunks
from app.services.retriever_questions import retrieve_questions


def generate_answers(vector_store, text):
    """
    Generate answers for detected questions.

    - `text` is the full RFP text, used to detect which questions apply.
    - `vector_store` is the FAISS-backed store over RFP chunks, used
      to retrieve the most relevant chunks per question.
    """
    # Use the raw RFP text to find the most relevant questions
    questions = retrieve_questions(text)

    results = []

    for q in questions:
        # For each question, retrieve the most relevant chunks from the store
        relevant_chunks = retrieve_chunks(q, vector_store)
        context = "\n".join(relevant_chunks)

        prompt = f"""
Answer ONLY from context.
If not found say "Not specified in RFP"

Context:
{context}

Question:
{q}
"""

        answer = ask_llm(prompt)

        results.append(
            {
                "question": q,
                "answer": answer,
                "sources": relevant_chunks,
            }
        )

    return results