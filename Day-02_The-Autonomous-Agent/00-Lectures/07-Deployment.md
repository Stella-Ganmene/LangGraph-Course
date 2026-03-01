# Lecture 07 : Going Live: From Local Agent to Production Endpoint

> **Duration**: 15 min lecture (delivered before Exercise 07)  
> **Objective**: Understand how to expose your agent as an API that your frontend can call.

---

## The Gap Between "It Works on My Machine" and "It Works for Users"

Right now, your agent runs in a terminal. You type a message, it responds. That's great for development, but Alex's clients can't open a terminal.

We need to turn your agent into an **API endpoint**, a URL that your Lovable frontend can call.

```
Lovable Frontend                     Your Agent Backend
┌───────────────┐    HTTP POST      ┌────────────────┐
│               │ ───────────────►  │                │
│  React App    │    /api/agent     │  FastAPI +      │
│  (Lovable)    │ ◄───────────────  │  LangGraph     │
│               │    JSON response  │                │
└───────────────┘                   └────────────────┘
```

---

## FastAPI in 60 Seconds

**FastAPI** is a Python framework for building APIs. It's the simplest way to turn your agent into an endpoint.

The concept:
1. You define a **route** (URL path): `/api/agent`
2. When someone sends a request to that URL, your function runs
3. Your function calls the LangGraph agent
4. The result is sent back as JSON

That's it. Your agent logic doesn't change, you just wrap it in a web server.

---

## The Streaming Question

Agents take time to think. If your frontend sends a request and waits 30 seconds for a response, the user thinks it's broken.

Two approaches:

### Option A: Simple Request/Response
- Frontend sends request → waits → gets full response
- Simple to implement
- Bad UX for complex agent tasks (long wait, no feedback)

### Option B: Streaming
- Frontend sends request → gets incremental updates
- "Checking database..." → "Found 3 leads..." → "Scoring..." → "Done!"
- Better UX, more complex to implement
- LangGraph supports streaming natively

For this exercise, we'll start with **Option A** and discuss how to upgrade to streaming.

---

## Production Considerations

When your agent goes live, new concerns emerge:

### Authentication
Not everyone should be able to call your agent. Add an API key or JWT check.

### Rate Limiting
What if someone calls your endpoint 1,000 times per minute? Add rate limiting (e.g., 10 requests/minute per user).

### Error Responses
Your agent might fail. The API should return meaningful error messages, not Python tracebacks.

### Logging
In production, logs are your lifeline. Log every request, every agent step, every error.

### Cost Control
Every agent run costs money (LLM API calls). Track usage and set limits.

---

## The Final Architecture

Here's what your complete system looks like:

```
┌────────────────────────────────────────────────────────┐
│                    FRONTEND (Lovable)                   │
│  React app with chat interface                         │
└──────────────────────┬─────────────────────────────────┘
                       │ HTTP POST /api/agent
                       ▼
┌────────────────────────────────────────────────────────┐
│                    BACKEND (FastAPI)                    │
│  ┌──────────────────────────────────────────────────┐  │
│  │              LangGraph Orchestrator               │  │
│  │                                                    │  │
│  │   ┌──────────┐  ┌──────────┐  ┌──────────────┐  │  │
│  │   │  Lead     │  │  Lead     │  │  Email        │  │  │
│  │   │  Finder   │  │  Scorer   │  │  Drafter      │  │  │
│  │   └────┬─────┘  └────┬─────┘  └──────┬───────┘  │  │
│  │        │              │               │           │  │
│  └────────┼──────────────┼───────────────┼──────────┘  │
│           │              │               │              │
└───────────┼──────────────┼───────────────┼──────────────┘
            │              │               │
     ┌──────▼──────┐      │        ┌──────▼──────┐
     │  Supabase   │      │        │  Email API   │
     │  Database   │◄─────┘        │  (Resend)    │
     └─────────────┘               └──────────────┘
```

You built every piece of this over 2 days. Let's connect it all.

---


## Your turn

Apply what you learned here:
[Exercise 07 Going Live](../01-Exercises/07-Going-Live.md)
