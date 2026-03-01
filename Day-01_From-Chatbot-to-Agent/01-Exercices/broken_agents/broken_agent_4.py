# broken_agent_4.py : "The Infinite Thinker"
# This agent has a bug. Your mission: find it and fix it.
#
# SYMPTOM: This agent started at 3 AM and is STILL running.
# CPU at 100%. No output produced.
# It was asked: "Analyze all leads and create a comprehensive report."

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
def get_all_leads() -> list[dict]:
    """Retrieves all leads from the database."""
    response = supabase.table("leads") \
        .select("*") \
        .execute()
    return response.data


@tool
def get_lead_details(lead_id: str) -> dict:
    """Gets detailed information about a specific lead.
    
    Args:
        lead_id: The UUID of the lead
    """
    response = supabase.table("leads") \
        .select("*") \
        .eq("id", lead_id) \
        .execute()
    if response.data:
        return response.data[0]
    return {"error": f"Lead {lead_id} not found"}


@tool
def get_lead_interactions(lead_id: str) -> list[dict]:
    """Gets all past interactions with a lead.
    
    Args:
        lead_id: The UUID of the lead
    """
    # BUG: This table doesn't exist! The query will fail every time.
    try:
        response = supabase.table("interactions") \
            .select("*") \
            .eq("lead_id", lead_id) \
            .execute()
        return response.data
    except Exception as e:
        # BUG: Error is returned as a string, but it's vague.
        # The LLM doesn't understand this means "table doesn't exist"
        # and tries again with different parameters.
        return {"error": str(e)}


@tool
def get_revenue_forecast(lead_ids: list[str]) -> dict:
    """Calculates revenue forecast based on lead scores and budgets.
    
    Args:
        lead_ids: List of lead UUIDs to include in forecast
    """
    # 🐛 BUG: This tool sometimes works, sometimes fails randomly
    # (simulating an unreliable external service)
    import random
    if random.random() < 0.6:  # 60% failure rate
        raise Exception("Service temporarily unavailable. Please try again.")
    
    leads = []
    for lid in lead_ids:
        response = supabase.table("leads") \
            .select("score, budget") \
            .eq("id", lid) \
            .execute()
        if response.data:
            leads.append(response.data[0])
    
    return {"forecast": "placeholder", "leads_analyzed": len(leads)}


# ---- AGENT ----

llm = ChatOpenAI(model="gpt-4o-mini")
tools = [get_all_leads, get_lead_details, get_lead_interactions, get_revenue_forecast]
llm_with_tools = llm.bind_tools(tools)

SYSTEM_PROMPT = """You are an advanced business analyst assistant.

When asked to create a comprehensive report, you must:
1. Get ALL leads from the database
2. Get DETAILED information on EACH lead individually
3. Get the INTERACTION HISTORY for each lead
4. Calculate a REVENUE FORECAST
5. Compile everything into a thorough report

Be thorough and complete. Do not skip any lead. Do not produce a partial 
report — if any data is missing, retry until you get it. 
A comprehensive report requires comprehensive data.

If a tool call fails, try again. Persistence is key."""


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

# BUG: No recursion limit!
app = graph.compile()


# ---- RUN ----
if __name__ == "__main__":
    result = app.invoke({
        "messages": [{"role": "user", "content": "Analyze all leads and create a comprehensive report"}]
    })
    print(result["messages"][-1].content)


