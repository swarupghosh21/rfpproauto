import re

def extract_sections(text):

    pattern = r"\n\d+\.?\s+[A-Z][^\n]+"  # Detect numbered headings

    matches = list(re.finditer(pattern, text))

    sections = []

    for i in range(len(matches)):

        start = matches[i].start()

        end = matches[i+1].start() if i+1 < len(matches) else len(text)

        section_title = matches[i].group().strip()

        content = text[start:end]

        sections.append({
            "title": section_title,
            "content": content
        })

    return sections