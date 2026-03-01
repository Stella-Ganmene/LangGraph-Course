# Solutions — Day 2

> **For instructors only.**

---

## Exercise 05: The Orchestrator — Solution Architecture

### Wrapping Agents as Tools

```python
from langchain_core.tools import tool

@tool
def find_stale_leads(days: int = 3) -> str:
    """Searches the database for leads that haven't been contacted in N days.
    Returns a formatted list of stale leads with their details.
    Use this when Alex asks about forgotten, stale, or neglected leads.
    
    Args:
        days: Number of days without contact (default: 3)
    """
    # Run the Exercise 01 agent internally
    result = lead_finder_app.invoke({
        "messages": [{"role": "user", "content": f"Find leads not contacted in {days} days"}]
    })
    return result["messages"][-1].content


@tool
def score_leads(lead_info: str = "all unscored") -> str:
    """Evaluates leads and assigns scores from 1-10 with categories (hot/warm/cold).
    Can score all unscored leads or specific ones.
    Use when Alex wants to know which leads to prioritize.
    
    Args:
        lead_info: "all unscored" or a description of which leads to score
    """
    result = lead_scorer_app.invoke({
        "messages": [{"role": "user", "content": f"Score these leads: {lead_info}"}]
    })
    return result["messages"][-1].content


@tool
def draft_follow_up_emails(target: str = "hot leads") -> str:
    """Generates personalized follow-up emails for specified leads.
    Emails require human approval before sending.
    Use when Alex wants to reach out to leads.
    
    Args:
        target: "hot leads" or specific lead names/IDs
    """
    result = email_drafter_app.invoke({
        "messages": [{"role": "user", "content": f"Draft follow-ups for: {target}"}]
    })
    return result["messages"][-1].content
```

### Orchestrator Graph

```python
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI

ORCHESTRATOR_PROMPT = """You are Alex's autonomous business assistant.

You coordinate specialized sub-agents to manage his freelance consulting leads.

Available agents:
- find_stale_leads: Discovers leads not contacted in N days
- score_leads: Evaluates and prioritizes leads (1-10 score, hot/warm/cold)
- draft_follow_up_emails: Creates personalized emails (requires Alex's approval)

Workflow rules:
1. Find leads before scoring (can't score what you haven't found)
2. Score before emailing (only email hot leads)
3. Always provide a clear summary of actions taken

When Alex gives a general request like "handle my leads", execute the full pipeline:
find → score → draft emails for hot leads."""

llm = ChatOpenAI(model="gpt-4o-mini")
orchestrator_tools = [find_stale_leads, score_leads, draft_follow_up_emails]
llm_with_tools = llm.bind_tools(orchestrator_tools)

def orchestrator_node(state: MessagesState):
    system = {"role": "system", "content": ORCHESTRATOR_PROMPT}
    response = llm_with_tools.invoke([system] + state["messages"])
    return {"messages": [response]}

tool_node = ToolNode(orchestrator_tools)

graph = StateGraph(MessagesState)
graph.add_node("orchestrator", orchestrator_node)
graph.add_node("tools", tool_node)
graph.add_edge(START, "orchestrator")
graph.add_conditional_edges("orchestrator", tools_condition)
graph.add_edge("tools", "orchestrator")

checkpointer = MemorySaver()
app = graph.compile(checkpointer=checkpointer, recursion_limit=30)
```

---

## Exercise 06: Calendar Agent — Solution Architecture

### Calendar Tools

```python
@tool
def check_availability(start_date: str, end_date: str) -> str:
    """Checks Alex's calendar for available time slots within a date range.
    Returns a list of free slots. Read-only operation.
    
    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
    """
    # Mock implementation
    available_slots = []
    # ... query calendar API or mock data ...
    if not available_slots:
        return "No available slots found in this range."
    return f"Available slots: {available_slots}"


@tool
def propose_meeting(lead_email: str, proposed_time: str, title: str) -> str:
    """Proposes a meeting with a lead at a specific time.
    IMPORTANT: This sends an external invitation. Requires Alex's approval.
    Always check_availability first before proposing a time.
    
    Args:
        lead_email: The lead's email address
        proposed_time: Proposed meeting time in ISO format
        title: Meeting title/subject
    """
    # This should be gated behind human-in-the-loop
    return f"Meeting proposed: {title} with {lead_email} at {proposed_time}"
```

### Integration (minimal changes to orchestrator):

```python
# Add to imports
from calendar_tools import check_availability, propose_meeting

# Add to tools list
orchestrator_tools = [
    find_stale_leads, score_leads, draft_follow_up_emails,
    check_availability, propose_meeting  # NEW
]

# Add to system prompt
# ... existing prompt ...
# - check_availability: Checks Alex's calendar for free time slots
# - propose_meeting: Proposes a meeting time (requires approval)
# RULE: Always check availability before proposing meetings.
```

**Key point**: The orchestrator code changes are minimal — just tool imports and prompt updates.

---

## Exercise 07: Deployment — Solution Architecture

### FastAPI Backend

```python
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging

app = FastAPI(title="Alex's AI Assistant")
logger = logging.getLogger("agent-api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = "your-secret-key"  # In production, use env variable

class AgentRequest(BaseModel):
    message: str
    thread_id: str

class ApprovalRequest(BaseModel):
    thread_id: str
    action: str  # "approve", "reject", "edit"
    edits: str = None

async def verify_api_key(authorization: str = Header(None)):
    if not authorization or authorization != f"Bearer {API_KEY}":
        raise HTTPException(status_code=401, detail="Invalid API key")

@app.post("/api/agent")
async def run_agent(request: AgentRequest, _=Depends(verify_api_key)):
    try:
        config = {"configurable": {"thread_id": request.thread_id}}
        result = orchestrator_app.invoke(
            {"messages": [{"role": "user", "content": request.message}]},
            config
        )
        
        # Check if agent is paused for review
        snapshot = orchestrator_app.get_state(config)
        is_paused = bool(snapshot.next)
        
        return {
            "status": "awaiting_review" if is_paused else "complete",
            "response": result["messages"][-1].content,
            "thread_id": request.thread_id
        }
    except Exception as e:
        logger.error(f"Agent error: {e}")
        raise HTTPException(status_code=500, detail="Agent encountered an error")

@app.post("/api/agent/approve")
async def approve_action(request: ApprovalRequest, _=Depends(verify_api_key)):
    config = {"configurable": {"thread_id": request.thread_id}}
    
    if request.action == "reject":
        return {"status": "rejected", "message": "Action cancelled."}
    
    if request.action == "edit" and request.edits:
        orchestrator_app.update_state(config, {
            "messages": [{"role": "user", "content": request.edits}]
        })
    
    result = orchestrator_app.invoke(None, config)
    return {
        "status": "complete",
        "response": result["messages"][-1].content
    }

@app.get("/api/agent/status/{thread_id}")
async def get_status(thread_id: str, _=Depends(verify_api_key)):
    config = {"configurable": {"thread_id": thread_id}}
    try:
        snapshot = orchestrator_app.get_state(config)
        is_paused = bool(snapshot.next)
        return {
            "status": "awaiting_review" if is_paused else "idle",
            "pending_actions": list(snapshot.next) if is_paused else []
        }
    except Exception:
        return {"status": "no_session"}
```

### Run:
```bash
uvicorn api:app --reload --port 8000
```

Test at: http://localhost:8000/docs
