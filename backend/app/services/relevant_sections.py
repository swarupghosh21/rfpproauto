def is_relevant_section(section_title):

    keywords = [
        "scope",
        "timeline",
        "payment",
        "sla",
        "integration",
        "data",
        "penalty",
        "security",
        "liability"
    ]

    title = section_title.lower()

    return any(k in title for k in keywords)