"""
Dummy tools used by the agents.
In a real application these would call APIs, databases, or search engines.
"""

from langchain.tools import tool


# ── Research Tools ─────────────────────────────────────────────────────────────

@tool
def search_facts(topic: str) -> str:
    """Search for key facts about a topic from the knowledge base"""
    kb = {
        "python": [
            "Created by Guido van Rossum, first released in 1991",
            "Emphasizes code readability with clean, minimal syntax",
            "Most popular language for data science, AI, and automation",
            "Supports multiple paradigms: OOP, functional, and procedural",
            "Python 3.12 brought ~60% performance improvement over 3.10",
        ],
        "javascript": [
            "Created by Brendan Eich in 10 days in 1995 at Netscape",
            "The only language natively supported by all web browsers",
            "Node.js expanded JavaScript to server-side development in 2009",
            "Most-used language on GitHub for over 10 consecutive years",
        ],
        "machine learning": [
            "Subset of AI that learns patterns from data without explicit rules",
            "Key types: supervised, unsupervised, and reinforcement learning",
            "Popular frameworks: TensorFlow, PyTorch, and scikit-learn",
            "Transformer architecture (2017) revolutionized NLP and beyond",
        ],
        "docker": [
            "Platform for building and running apps in isolated containers",
            "Containers package code + dependencies for consistent environments",
            "Released in 2013, now used by 80% of Fortune 100 companies",
            "Docker Hub hosts over 100,000 public container images",
        ],
    }
    topic_lower = topic.lower()
    for key in kb:
        if key in topic_lower or topic_lower in key:
            return "Facts about {}:\n".format(topic) + "\n".join("• " + f for f in kb[key])
    return (
        "General facts for '{}': A widely-adopted technology with active open-source "
        "community, growing developer interest, and increasing enterprise adoption.".format(topic)
    )


@tool
def get_statistics(topic: str) -> str:
    """Retrieve usage statistics and market data for a topic"""
    stats = {
        "python": (
            "48% of developers use Python (Stack Overflow 2024). "
            "#1 language 4 years in a row. 15M+ developers worldwide. "
            "400K+ packages available on PyPI."
        ),
        "javascript": (
            "65% of developers use JavaScript (Stack Overflow 2024). "
            "2.4M+ packages on npm. Used by 98.4% of all websites."
        ),
        "machine learning": (
            "ML market: $21B (2024) projected to reach $209B by 2029. "
            "70% of enterprises are actively investing in AI/ML. "
            "Demand for ML engineers grew 75% year-over-year."
        ),
        "docker": (
            "Docker has 20M+ developers. "
            "80% of Fortune 100 companies use Docker. "
            "Containers cut deployment time by up to 50%."
        ),
    }
    topic_lower = topic.lower()
    for key in stats:
        if key in topic_lower or topic_lower in key:
            return stats[key]
    return (
        "Market data for '{}': Rapidly growing adoption with increased "
        "industry investment and developer interest year over year.".format(topic)
    )


@tool
def find_examples(topic: str) -> str:
    """Find real-world use cases and company examples for a topic"""
    examples = {
        "python": (
            "Netflix uses Python for data pipelines and recommendations. "
            "Instagram's backend runs on Django (Python). "
            "NASA uses Python for data analysis and simulations. "
            "Dropbox built their desktop sync client entirely in Python."
        ),
        "javascript": (
            "React (JavaScript) powers Facebook and Instagram UIs. "
            "Node.js powers LinkedIn's mobile backend. "
            "VS Code is built with Electron (JavaScript). "
            "Next.js powers production apps at Vercel, TikTok, and Twitch."
        ),
        "machine learning": (
            "Gmail spam filter blocks 99.9% of spam using ML. "
            "Netflix saves $1B/year through ML-driven recommendations. "
            "Tesla Autopilot uses computer vision (ML) for self-driving. "
            "ChatGPT is a large language model trained with reinforcement learning."
        ),
        "docker": (
            "Spotify uses Docker for microservices deployment at scale. "
            "PayPal reduced build time from hours to minutes with Docker. "
            "Uber manages thousands of microservices in containers. "
            "GitHub Actions CI/CD pipelines run inside Docker containers."
        ),
    }
    topic_lower = topic.lower()
    for key in examples:
        if key in topic_lower or topic_lower in key:
            return examples[key]
    return (
        "Use cases for '{}': Applied in healthcare, finance, retail, "
        "and tech for automation, analytics, and operational efficiency.".format(topic)
    )


# ── Writer Tools ────────────────────────────────────────────────────────────────

@tool
def get_content_structure(content_type: str) -> str:
    """Get a structural template for a type of written content"""
    structures = {
        "article": (
            "1) Hook / Opening (2-3 sentences that grab attention)\n"
            "2) Background / Why it matters\n"
            "3) Core concepts (3-5 key points)\n"
            "4) Real-world examples\n"
            "5) Conclusion with a clear takeaway"
        ),
        "blog": (
            "1) Engaging title and personal opening\n"
            "2) Problem statement (why the reader should care)\n"
            "3) Main insights with sub-sections\n"
            "4) Actionable takeaways\n"
            "5) Conversational closing / call to action"
        ),
    }
    return structures.get(content_type.lower(), structures["article"])


@tool
def get_tone_guidelines(tone: str) -> str:
    """Get writing style guidelines for a specific tone"""
    guidelines = {
        "educational": (
            "Define terms on first use. Use analogies for complex ideas. "
            "Build from simple to complex. Include concrete examples. "
            "Summarize key points at the end."
        ),
        "professional": (
            "Use formal language. Avoid contractions. Support claims with data. "
            "Maintain objective voice. Use industry terminology appropriately."
        ),
        "casual": (
            "Write conversationally, as if talking to a friend. "
            "Contractions are fine. Keep sentences short and punchy. "
            "Use relatable, everyday examples."
        ),
    }
    return guidelines.get(tone.lower(), guidelines["educational"])


# ── Reviewer Tools ──────────────────────────────────────────────────────────────

@tool
def evaluate_structure(text: str) -> str:
    """Check whether the article has a clear introduction, body, and conclusion"""
    has_intro = any(w in text[:300].lower() for w in ["introduction", "today", "in this", "let's", "welcome"])
    has_conclusion = any(w in text[-400:].lower() for w in ["conclusion", "summary", "takeaway", "finally", "in summary", "to summarize"])
    has_examples = any(w in text.lower() for w in ["example", "for instance", "such as", "like ", "e.g."])
    has_data = any(w in text.lower() for w in ["%", "million", "billion", "survey", "report", "study"])

    results = []
    results.append("✓ Has examples" if has_examples else "✗ Missing concrete examples")
    results.append("✓ Includes data/stats" if has_data else "✗ Lacks supporting statistics")
    results.append("✓ Has a conclusion" if has_conclusion else "✗ No clear conclusion section")
    results.append("✓ Has an introduction" if has_intro else "✗ Opening could be stronger")

    return "\n".join(results)


@tool
def calculate_score(text: str) -> str:
    """Calculate a quality score for the article based on content criteria"""
    score = 4

    word_count = len(text.split())
    if word_count >= 300:
        score += 2
    elif word_count >= 150:
        score += 1
    else:
        score -= 1

    if any(w in text.lower() for w in ["example", "for instance", "such as", "e.g."]):
        score += 1

    if any(w in text.lower() for w in ["%", "million", "billion", "survey", "developers"]):
        score += 1

    if any(w in text.lower() for w in ["conclusion", "summary", "takeaway", "finally"]):
        score += 1

    if text.count("\n") >= 4:
        score += 1

    return str(min(10, max(1, score)))
