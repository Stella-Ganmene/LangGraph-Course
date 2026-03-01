# broken_agent_1.py : "The Email Spammer"
# This agent has a bug. Your mission: find it and fix it.
#
# SYMPTOM: Lead "Sarah Chen" received 47 identical follow-up emails overnight.
# The agent was supposed to send ONE email per stale lead.

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from supabase import create_client
from datetime import datetime, timedelta

load_dotenv()

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

# ---- TOOLS ----

@tool
def get_stale_leads(days: int = 3) -> list[dict]:
    """Retrieves leads not contacted in the last N days.
    
    Args:
        days: Number of days without contact to consider stale
    """
    cutoff = (datetime.now() - timedelta(days=days)).isoformat()
    response = supabase.table("leads") \
        .select("id, name, email, company, notes, last_contacted_at") \
        .lt("last_contacted_at", cutoff) \
        .execute()
    return response.data


@tool
def send_follow_up_email(lead_email: str, subject: str, body: str) -> str:
    """Sends a follow-up email to a lead.
    
    Args:
        lead_email: The recipient's email address
        subject: Email subject line
        body: Email body content
    """
    # Simulated send (in real code, this calls an email API)
    print(f"📧 SENDING EMAIL to {lead_email}: {subject}")
    return f"Email sent successfully to {lead_email} at {datetime.now().isoformat()}"


# ---- AGENT ----

llm = ChatOpenAI(model="gpt-4o-mini")
tools = [get_stale_leads, send_follow_up_email]
llm_with_tools = llm.bind_tools(tools)

SYSTEM_PROMPT = """You are Alex's lead management assistant. 

Your job:
1. Find leads that haven't been contacted recently
2. Send a personalized follow-up email to each one
3. Make sure every stale lead gets exactly one email

After sending emails, check if there are any remaining stale leads 
that still need follow-up."""


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
        "messages": [{"role": "user", "content": "Send follow-up emails to all my stale leads"}]
    })
    print(result["messages"][-1].content)


