# Solutions : Day 1

> **For instructors only.**

---

## Exercise 01: Forgotten Leads : Solution Architecture

### Tool Definition (tools.py)

```python
from langchain_core.tools import tool
from supabase import create_client
from datetime import datetime, timedelta
import os

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

@tool
def get_stale_leads(days: int) -> list[dict]:
    """Retrieves leads from the Supabase database that have not been 
    contacted in the last N days. Returns a list of lead objects with 
    their name, email, company, status, and notes.
    
    Args:
        days: Number of days without contact to consider a lead "stale"
    """
    cutoff = (datetime.now() - timedelta(days=days)).isoformat()
    response = supabase.table("leads") \
        .select("*") \
        .lt("last_contacted_at", cutoff) \
        .execute()
    return response.data
```

### Graph Definition (agent.py)

```python
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI

# 1. LLM with tools bound
llm = ChatOpenAI(model="gpt-4o-mini")
tools = [get_stale_leads]
llm_with_tools = llm.bind_tools(tools)

# 2. Agent node
def agent_node(state: MessagesState):
    system_msg = {
        "role": "system",
        "content": "You are Alex's lead management assistant. When asked about leads, "
                   "ALWAYS use the get_stale_leads tool to check the database. "
                   "Never guess or make up lead data. After retrieving leads, "
                   "generate a personalized follow-up draft for each one."
    }
    response = llm_with_tools.invoke([system_msg] + state["messages"])
    return {"messages": [response]}

# 3. Tool node
tool_node = ToolNode(tools)

# 4. Build graph
graph = StateGraph(MessagesState)
graph.add_node("agent", agent_node)
graph.add_node("tools", tool_node)

graph.add_edge(START, "agent")
graph.add_conditional_edges("agent", tools_condition)
graph.add_edge("tools", "agent")

app = graph.compile()

# 5. Run
result = app.invoke({
    "messages": [{"role": "user", "content": "Find all leads I haven't contacted in 3 days"}]
})
print(result["messages"][-1].content)
```

### Key Points for Students:
- `MessagesState` is LangGraph's built-in state that manages a list of messages
- `tools_condition` is a built-in function that checks if the LLM wants to call a tool
- `ToolNode` automatically handles tool execution and returns results as messages

---

## Exercise 02: Lead Scoring : Solution Architecture

### Additional Tools

```python
@tool
def get_unscored_leads() -> list[dict]:
    """Retrieves all leads that have not been scored yet (score is null).
    Returns lead data including budget, timeline, decision_maker status, and notes."""
    response = supabase.table("leads") \
        .select("*") \
        .is_("score", "null") \
        .execute()
    return response.data

@tool  
def update_lead_score(lead_id: str, score: int, category: str) -> str:
    """Updates a lead's score and category in the database.
    
    Args:
        lead_id: The UUID of the lead to update
        score: Score from 1-10 (MUST be in this range)
        category: One of "hot" (7-10), "warm" (4-6), "cold" (1-3)
    """
    if not 1 <= score <= 10:
        return f"ERROR: Score must be between 1 and 10. Got {score}."
    
    valid_categories = ["hot", "warm", "cold"]
    if category not in valid_categories:
        return f"ERROR: Category must be one of {valid_categories}. Got {category}."
    
    supabase.table("leads") \
        .update({"score": score, "category": category}) \
        .eq("id", lead_id) \
        .execute()
    return f"Lead {lead_id} updated: score={score}, category={category}"
```

### Expected Scoring Mistake:
The AI will almost certainly score the "budget: TBD" lead too high. The fix is adding to the system prompt:
```
IMPORTANT: "TBD", "unknown", "not sure", or empty budget = 0 budget points.
Only give budget points for SPECIFIC numbers or ranges.
```

---

## Exercise 03: Email Follow-Up : Solution Architecture

### Interrupt Implementation

```python
from langgraph.checkpoint.memory import MemorySaver

checkpointer = MemorySaver()

# Build graph with interrupt
graph = StateGraph(MessagesState)
# ... add nodes and edges ...

app = graph.compile(
    checkpointer=checkpointer,
    interrupt_before=["send_emails"]  # Pause before sending
)

# First run — will pause before send_emails
config = {"configurable": {"thread_id": "alex-session-1"}}
result = app.invoke(
    {"messages": [{"role": "user", "content": "Email my hot leads"}]},
    config
)

# Inspect the drafts in result
print("Drafts ready for review:", result)

# Resume after approval
app.invoke(None, config)  # Continues from where it paused
```

### Human Review Pattern:
To allow Alex to modify drafts, update the State between pause and resume:
```python
# After reviewing, update state to modify a draft
app.update_state(config, {
    "messages": [{"role": "user", "content": "Change the email for Sarah to be more casual"}]
})
app.invoke(None, config)
```

---

## Exercise 04: Broken Agents : Bug Details

### Case 1 (Email Spammer):
**Bug**: Edge from `send_email` → `check_leads` without updating `last_contacted_at` first.
**Fix**: Add `update_contact_date` node between `send_email` and the loop-back, plus `max_iterations=10`.

### Case 2 (Impossible Score):
**Bug**: No validation in `update_lead_score` tool + vague prompt.
**Fix**: Add `if not 1 <= score <= 10: return "Error"` + explicit prompt instructions.

### Case 3 (Ghost Leads):
**Bug**: `create_or_update_lead` tool has create capability that shouldn't be there.
**Fix**: Replace with read-only + update-score-only tools. Principle of least privilege.

### Case 4 (Infinite Loop):
**Bug**: No `recursion_limit`, no error handling on failed tool calls.
**Fix**: `graph.compile(recursion_limit=25)` + try/except in tools + fallback message.
