# broken_agent_2.py — "The Impossible Score"
# 🐛 This agent has a bug. Your mission: find it and fix it.
#
# SYMPTOM: Lead "Marc Dubois" has a score of 15 out of 10.
# Scores should be between 1 and 10.

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from supabase import create_client

load_dotenv()

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

# ---- TOOLS ----

@tool
def get_unscored_leads() -> list[dict]:
    """Retrieves all leads that haven't been scored yet.
    Returns lead details including budget, timeline, and notes."""
    response = supabase.table("leads") \
        .select("id, name, company, budget, timeline, decision_maker, notes") \
        .is_("score", "null") \
        .execute()
    return response.data


@tool
def update_lead_score(lead_id: str, score: int, category: str) -> str:
    """Updates a lead's score and category in the database.
    
    Args:
        lead_id: The UUID of the lead
        score: The lead's score
        category: The lead's category (hot, warm, or cold)
    """
    # 🐛 BUG: No validation on score range!
    supabase.table("leads") \
        .update({"score": score, "category": category}) \
        .eq("id", lead_id) \
        .execute()
    return f"Updated lead {lead_id}: score={score}, category={category}"


# ---- AGENT ----

llm = ChatOpenAI(model="gpt-4o-mini")
tools = [get_unscored_leads, update_lead_score]
llm_with_tools = llm.bind_tools(tools)

# 🐛 BUG: The prompt doesn't specify the score range!
SYSTEM_PROMPT = """You are a lead scoring assistant.

Your job is to evaluate leads and assign them a score based on their potential value.

Consider these factors:
- Budget (higher budget = more points)
- Timeline (sooner = more points)
- Whether they are a decision maker (yes = more points)
- Engagement level from notes (more engaged = more points)

Score each lead and categorize them:
- Hot leads should be prioritized
- Warm leads can wait
- Cold leads should be archived

Be generous with scoring for leads that show enthusiasm, 
even if some details are missing — potential matters!"""


def agent_node(state: MessagesState):
    system = {"role": "system", "content": SYSTEM_PROMPT}
    response = llm_with_tools.invoke([system] + state["messages"])
    return {"messages": [response]}


tool_node = ToolNode(tools)

# ---- GRAPH ----

graph = StateGraph(MessagesState)
graph.add_node("agent", agent_node)
graph.add_node("tools", tool_node)

graph.add_edge(START, "agent")
graph.add_conditional_edges("agent", tools_condition)
graph.add_edge("tools", "agent")

app = graph.compile(recursion_limit=25)

# ---- RUN ----
if __name__ == "__main__":
    result = app.invoke({
        "messages": [{"role": "user", "content": "Score all my unscored leads"}]
    })
    print(result["messages"][-1].content)


# ============================================================
# 🐛 BUGS IN THIS FILE (for instructor reference):
#
# 1. MAIN BUG: update_lead_score has NO validation.
#    It accepts any integer — score=15, score=-3, anything.
#    The tool should reject scores outside 1-10.
#
# 2. PROMPT BUG: The system prompt never says "score from 1 to 10."
#    It just says "assign a score." The LLM has no range constraint.
#    Worse: "Be generous... potential matters!" encourages inflation.
#
# 3. CATEGORY BUG: No defined mapping between scores and categories.
#    The prompt says "hot should be prioritized" but doesn't say
#    "hot = 7-10, warm = 4-6, cold = 1-3."
#    The LLM decides on its own, inconsistently.
#
# FIXES NEEDED:
# - Add validation in update_lead_score:
#     if not 1 <= score <= 10:
#         return f"ERROR: Score must be between 1-10. Got {score}."
# - Add explicit range to prompt: "Score from 1 to 10"
# - Add explicit category rules: "hot=7-10, warm=4-6, cold=1-3"
# - Remove "be generous" — replace with explicit criteria per point
# ============================================================
