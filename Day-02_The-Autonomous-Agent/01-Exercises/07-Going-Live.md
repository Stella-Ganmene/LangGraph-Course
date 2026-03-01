# Exercise 07 — Going Live 🚀

> **Duration**: 2h  
> **Difficulty**: ⭐⭐⭐  
> **What you'll build**: Your agent as a FastAPI endpoint, connected to your Lovable frontend.

---

## The Problem

Alex: *"This is amazing. But I'm not going to open a terminal every time I want to use my assistant. I need this in my app."*

**Your mission**: Deploy your orchestrator as a web API and connect it to the Lovable frontend so Alex can chat with his agent through a real interface.

---

## Part 1: Create the FastAPI Backend (30 min) — 🤖 Cursor ON

Create a new file: `api.py`

### What you need:

1. **A POST endpoint** at `/api/agent` that:
   - Accepts a JSON body with: `{"message": "user's request", "thread_id": "session-123"}`
   - Runs the orchestrator with the message
   - Returns the agent's response as JSON

2. **A POST endpoint** at `/api/agent/approve` that:
   - Accepts: `{"thread_id": "session-123", "action": "approve" | "reject" | "edit", "edits": "..."}`
   - Resumes the graph after a human-in-the-loop pause
   - Returns the updated response

3. **A GET endpoint** at `/api/agent/status/{thread_id}` that:
   - Returns the current state of the agent (running, paused_for_review, complete, error)
   - If paused, includes the data awaiting review (email drafts, etc.)

### Basic structure:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Alex's AI Assistant")

# Allow your Lovable frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to your domain
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/agent")
async def run_agent(request: AgentRequest):
    # Your orchestrator logic here
    pass

@app.post("/api/agent/approve")
async def approve_action(request: ApprovalRequest):
    # Resume the graph after human review
    pass

@app.get("/api/agent/status/{thread_id}")
async def get_status(thread_id: str):
    # Check agent state
    pass
```

### Test locally:
```bash
uvicorn api:app --reload --port 8000
```

Then test with curl or your browser at `http://localhost:8000/docs` (FastAPI auto-generates interactive documentation!).

---

## Part 2: Connect the Frontend (45 min) — 🤖 Cursor ON

In your **Lovable** project, create a simple chat interface that talks to your agent API.

### What you need:

1. **A chat input** where Alex types his request
2. **A message display** that shows the conversation
3. **A review panel** that appears when the agent pauses for approval:
   - Shows the email drafts
   - Buttons: "Approve", "Edit", "Reject"
4. **A status indicator**: "Thinking...", "Awaiting your review", "Done"

### The API calls:

```javascript
// Send a message to the agent
const response = await fetch("http://localhost:8000/api/agent", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ 
        message: userInput, 
        thread_id: sessionId 
    })
});

// Check if the agent needs approval
const status = await fetch(`http://localhost:8000/api/agent/status/${sessionId}`);

// Approve an action
const approval = await fetch("http://localhost:8000/api/agent/approve", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ 
        thread_id: sessionId, 
        action: "approve" 
    })
});
```

---

## Part 3: Add Production Safety (30 min)

Before considering this "production-ready," add:

### 1. Error Handling
The API should never return a Python traceback. Wrap everything in try/except and return meaningful error messages:
```json
{
    "status": "error",
    "message": "The agent encountered an issue with the database connection. Please try again.",
    "error_code": "SUPABASE_CONNECTION_ERROR"
}
```

### 2. Simple Authentication
Add an API key check. The Lovable frontend sends a key in the header:
```
Authorization: Bearer your-secret-key-here
```

### 3. Rate Limiting
Prevent abuse: maximum 10 requests per minute per thread_id.

### 4. Request Logging
Log every request with:
- Timestamp
- Thread ID
- User message
- Agent response (summary)
- Duration
- Any errors

---

## Part 4: The Grand Demo (15 min)

It's showtime! Open your Lovable frontend and run the **full pipeline** from the UI:

1. Type: *"Handle my leads for this week"*
2. Watch the agent find stale leads, score them, check the calendar, draft emails
3. Review the email drafts in your frontend
4. Approve the ones you like
5. See the confirmation that emails were sent

**Screenshot this moment.** You just built a multi-agent system with human oversight, deployed as a production API, accessible through a real frontend. In 2 days.

---

## ✅ Success Criteria

- [ ] FastAPI server runs and responds to requests
- [ ] Your Lovable frontend can send messages and display responses
- [ ] Human-in-the-loop works through the UI (pause → review → approve)
- [ ] Errors are handled gracefully (no crashes, clear messages)
- [ ] Authentication is present (API key check)
- [ ] You can run the full pipeline from the frontend

---

## 🧠 Final Reflection

Take 5 minutes. Write down:

1. **Two days ago**, I didn't know what a "graph" was in AI. **Now**, I _______________
2. The concept I'm most confident about: _______________
3. The concept I want to explore more: _______________
4. If I were to add one more feature to this agent, it would be: _______________

---

## What's Next?

You've built the foundation. Here's where you can go from here:

- **LangGraph Cloud**: Deploy your agent on LangGraph's managed platform (no server management)
- **LangSmith**: Professional observability — trace every agent run, debug in a visual UI
- **More tools**: Slack integration, Google Sheets, CRM APIs, document generation
- **More agents**: A customer support agent, a content creation agent, a data analysis agent
- **Multi-user**: Add user authentication so multiple people can have their own agent sessions

The pattern is always the same: **define a graph, add tools, compose agents**. You know this pattern now. Everything else is iteration.

---

🎉 **Congratulations! You've completed the module!**
