import os
from openai import OpenAI
from sqlalchemy.orm import Session
import json

from app.models import RFPSection, PreBidQuery
from app.services.relevant_sections import is_relevant_section
from app.services.gemini_client import generate_text

# client = OpenAI(api_key=os.getenv("AIzaSyBic52a-UYsBtgdY4kUg0it3Tjd7pQdbbQ"))


class PreBidQueryGeneratorAgent:

    def __init__(self, db: Session):
        self.db = db


    def generate_queries(self, rfp_id):

        sections = self.db.query(RFPSection).filter(
            RFPSection.rfp_id == rfp_id
        ).all()

        results = []

        for sec in sections:

            if not is_relevant_section(sec.section_title):
                continue

            queries = self.analyze_section(sec)

            for q in queries:

                db_obj = PreBidQuery(
                    rfp_id=rfp_id,
                    section_id=sec.section_id,
                    section_title=sec.section_title,
                    identified_issue=q["issue"],
                    suggested_query=q["query"],
                    severity=q["severity"]
                )

                self.db.add(db_obj)

                results.append(q)

        self.db.commit()

        return results


    def analyze_section(self, section):

        prompt = f"""
You are an expert bid manager.

Analyze the RFP section below.

Identify any unclear requirement or missing detail.

Generate pre-bid clarification questions.

Return JSON:

[
  {{
    "issue": "...",
    "query": "...",
    "severity": "Low/Medium/High"
  }}
]

Section Title:
{section.section_title}

Section Content:
{section.content}
"""

        # response = client.chat.completions.create(
        #     model="Gemini 3.1 Flash",
        #     messages=[
        #         {"role": "user", "content": prompt}
        #     ]
        # )

        # text = response.choices[0].message.content

        # import json

        # try:
        #     return json.loads(text)
        # except:
        #     return []

        try:
            response_text = generate_text(prompt)

            cleaned = response_text.strip()

            # Sometimes LLM adds ```json blocks
            if "```" in cleaned:
                cleaned = cleaned.split("```")[1]

            return json.loads(cleaned)

        except Exception as e:
            print("LLM parsing error:", e)
            return []