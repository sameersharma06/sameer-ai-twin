# agents/router.py — LangGraph multi-agent router
from langgraph.graph import StateGraph, END
from typing import TypedDict


class AgentState(TypedDict):
    input: str
    output: str
    agent_used: str


def detect_intent(text: str) -> str:
    text = text.lower()

    task_words = [
        "task", "todo", "tasks", "deadline", "add task",
        "complete", "mark done", "what are my", "show tasks"
    ]
    brain_words = [
        "what should i", "what to do", "i have time",
        "free time", "next step", "what's next",
        "i don't know", "help me decide", "motivation",
        "focus on", "prioritize", "should i build",
        "what should i build", "where to start",
        "i am stuck", "feeling lost", "guide me"
    ]
    research_words = [
    "what is", "explain", "research", "find", "search",
    "tell me about", "what do my notes", "how does", "summarize",
    "how do i", "how do you", "what are", "describe",
    "what do i know", "what do i have", "do i have notes",
    "what have i learned", "what do my notes say"
    ]
    coding_words = [
        "code", "write a function", "debug", "fix this error",
        "function", "script", "implement", "class", "import error",
        "syntax", "write a class", "write a script"
    ]
    automation_words = [
        "open", "launch", "automate", "notify",
        "remind", "close app", "start app"
    ]

    if any(w in text for w in task_words):
        return "task"
    if any(w in text for w in brain_words):
        return "brain"
    if any(w in text for w in automation_words):
        return "automation"
    if any(w in text for w in coding_words):
        return "coding"
    if any(w in text for w in research_words):
        return "research"
    return "brain"


def route_node(state: AgentState) -> str:
    return detect_intent(state["input"])


def task_node(state: AgentState) -> AgentState:
    from agents.task_agent import run
    state["output"] = run(state["input"])
    state["agent_used"] = "TaskAgent"
    return state


def research_node(state: AgentState) -> AgentState:
    from agents.research_agent import run
    state["output"] = run(state["input"])
    state["agent_used"] = "ResearchAgent"
    return state


def coding_node(state: AgentState) -> AgentState:
    from agents.coding_agent import run
    state["output"] = run(state["input"])
    state["agent_used"] = "CodingAgent"
    return state


def automation_node(state: AgentState) -> AgentState:
    from agents.automation_agent import run
    state["output"] = run(state["input"])
    state["agent_used"] = "AutomationAgent"
    return state


def brain_node(state: AgentState) -> AgentState:
    from core.brain import get_response
    state["output"] = get_response(state["input"])
    state["agent_used"] = "Brain"
    return state


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("task", task_node)
    graph.add_node("research", research_node)
    graph.add_node("coding", coding_node)
    graph.add_node("automation", automation_node)
    graph.add_node("brain", brain_node)

    graph.set_conditional_entry_point(
        route_node,
        {
            "task": "task",
            "research": "research",
            "coding": "coding",
            "automation": "automation",
            "brain": "brain"
        }
    )

    graph.add_edge("task", END)
    graph.add_edge("research", END)
    graph.add_edge("coding", END)
    graph.add_edge("automation", END)
    graph.add_edge("brain", END)

    return graph.compile()


# Build once at import time
agent_graph = build_graph()


def run_agents(user_input: str) -> tuple[str, str]:
    """
    Returns (response, agent_name)
    """
    result = agent_graph.invoke({
        "input": user_input,
        "output": "",
        "agent_used": ""
    })
    return result["output"], result["agent_used"]