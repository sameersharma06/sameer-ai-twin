# agents/research_agent.py
from core.brain import get_response
from core.memory import log_event


def run(user_input: str) -> str:
    log_event("research_query", user_input[:100])

    # Check knowledge base first
    try:
        from knowledge.retriever import query as knowledge_query
        local_result = knowledge_query(user_input)
        if local_result and "empty" not in local_result.lower():
            return f"From your notes:\n\n{local_result}"
    except Exception:
        pass

    # Fall back to LLM
    prompt = f"""Research request: {user_input}

Provide a clear, concise summary of what you know about this topic.
Focus on practical, actionable information.
If this relates to AI, coding, or tech — be specific and technical."""

    return get_response(prompt, voice_mode=False)