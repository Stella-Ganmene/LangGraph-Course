# broken_agent_3.py — "The Ghost Leads"
# 🐛 This agent has a bug. Your mission: find it and fix it.
#
# SYMPTOM: The database now contains 3 leads that Alex never entered:
#   - "Test User" at "Example Corp"
#   - "John Doe" at "Acme Inc"  
#   - "Jane Sample" at "Demo LLC"
# This agent was only supposed to READ and SCORE leads.

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from supabase import create_client
from datetime import datetime

load_dotenv()

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

# ---- TOOLS ----

@tool
def get_all_leads() -> list[dict]:
    """Retrieves all leads from the database with their details."""
    response = supabase.table("leads") \
        .select("*") \
        .execute()
    return response.data


# 🐛 BUG: This tool can CREATE leads — but this agent should only READ and SCORE!
@tool
def create_or_update_lead(
    name: str, 
    email: str, 
    company: str, 
    score: int = None, 
    category: str = None,
    notes: str = None
) -> str:
    """Creates a new lead if it doesn't exist, or updates an existing lead.
    Use this to save lead information and scores to the database.
    
    Args:
        name: Lead's full name
        email: Lead's email address
        company: Lead's company name
        score: Optional score (1-10)
        category: Optional category (hot, warm, cold)
        notes: Optional notes about the lead
    """
    # Check if lead exists
    existing = supabase.table("leads") \
        .select("id") \
        .eq("email", email) \
        .execute()
    
    lead_data = {
        "name": name,
        "email": email,
        "company": company,
        "notes": notes,
        "last_contacted_at": datetime.now().isoformat()
    }
    
    if score is not None:
        lead_data["score"] = score
    if category is not None:
        lead_data["category"] = category
    
    if existing.data:
        # Update existing lead
        supabase.table("leads") \
            .update(lead_data) \
            .eq("id", existing.data[0]["id"]) \
            .execute()
        return f"Updated lead: {name} ({email})"
    else:
        # 🐛 Creates a NEW lead — this should never happen in a scoring agent!
        supabase.table("leads") \
            .insert(lead_data) \
            .execute()
        return f"Created new lead: {name} ({email})"


# ---- AGENT ----

llm = ChatOpenAI(model="gpt-4o-mini")
tools = [get_all_leads, create_or_update_lead]
llm_with_tools = llm.bind_tools(tools)

SYSTEM_PROMPT = """You are a lead scoring assistant.

Your job is to analyze all leads in the database and make sure each one 
has a proper score and category.

For each lead:
1. Read their information
2. Evaluate their potential (budget, timeline, engagement)
3. Assign a score from 1-10 and a category (hot/warm/cold)
4. Save the results

Make sure every lead in the system is properly scored and categorized.
If you notice any leads that seem incomplete, fill in reasonable defaults."""


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
        "messages": [{"role": "user", "content": "Score and organize all my leads"}]
    })
    print(result["messages"][-1].content)


# ============================================================
# 🐛 BUGS IN THIS FILE (for instructor reference):
#
# 1. MAIN BUG — PRINCIPLE OF LEAST PRIVILEGE VIOLATION:
#    The tool `create_or_update_lead` can CREATE new leads.
#    A scoring agent should NEVER have create permissions.
#    
#    What happened: The LLM hallucinated lead data. When it tried
#    to "score" leads like "Test User" or "John Doe" (which don't
#    exist), the tool created them instead of returning an error.
#
# 2. PROMPT BUG: "fill in reasonable defaults" encourages the LLM
#    to invent data when information is missing.
#
# 3. TOOL DESIGN BUG: Combining create + update in one tool is 
#    dangerous. The agent can't distinguish between "update existing"
#    and "accidentally create new."
#
# FIXES NEEDED:
# - Split into two separate tools:
#     - get_all_leads (read-only)
#     - update_lead_score(lead_id, score, category) (update only, no create)
# - The update tool should require a lead_id (not email lookup)
#   and return an error if the lead doesn't exist
# - Remove "fill in reasonable defaults" from the prompt
# - Add: "Only score leads that already exist. Never create new leads."
# ============================================================
