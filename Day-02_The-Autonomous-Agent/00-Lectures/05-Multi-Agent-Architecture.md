# Lecture 05 — The Orchestrator: Multi-Agent Architecture

> **Duration**: 20 min lecture  
> **Objective**: Understand how a single "manager" agent can coordinate multiple specialized agents.

---

## Where We Are

Yesterday, you built 3 independent agents:
1. 🔍 **Lead Finder** — detects stale leads in Supabase
2. 📊 **Lead Scorer** — evaluates and categorizes leads
3. ✉️ **Email Drafter** — writes and sends follow-ups with human approval

Each one works great. But Alex still has to **manually decide** which one to launch and when. That's not really autonomous, is it?

---

## The Multi-Agent Idea

What if there was a **4th agent** — a manager — whose only job is to:
1. Listen to Alex's request
2. Figure out which agent(s) to call
3. Chain them together in the right order
4. Return a unified result

```
Alex: "Handle my leads for this week"

Orchestrator thinks:
  1. First, I need to find stale leads       → calls Lead Finder
  2. Then, score the ones I found             → calls Lead Scorer  
  3. Finally, draft emails for hot leads      → calls Email Drafter
  
Alex gets: "Found 5 stale leads. Scored them. 
            3 are hot — here are your email drafts for review."
```

This is **multi-agent architecture**: specialized agents coordinated by an orchestrator.

---

## Real-World Analogy

Think of a company:
- The **CEO** (orchestrator) doesn't write code, design marketing, or handle sales
- They decide **who** needs to do **what** and in **what order**
- Each department (agent) is specialized and works independently
- The CEO coordinates the workflow and reports back to the board (Alex)

```
                    ┌─────────────────┐
                    │   Orchestrator   │
                    │   (the CEO)      │
                    └────┬───┬───┬────┘
                         │   │   │
              ┌──────────┘   │   └──────────┐
              ▼              ▼              ▼
        ┌──────────┐  ┌──────────┐  ┌──────────┐
        │  Lead     │  │  Lead     │  │  Email    │
        │  Finder   │  │  Scorer   │  │  Drafter  │
        └──────────┘  └──────────┘  └──────────┘
```

---

## How It Works in LangGraph

The elegant part: your existing agents become **tools** of the orchestrator.

Remember tools? They're just functions with descriptions that the AI can choose to call. Your mini-agents are functions. So you can wrap them as tools:

```
Tool: find_stale_leads
Description: "Runs the lead finder agent. Searches the database for 
             leads not contacted in N days. Returns a list of stale leads."

Tool: score_leads  
Description: "Runs the lead scoring agent. Takes a list of leads, 
             scores them 1-10, and categorizes as hot/warm/cold."

Tool: draft_follow_ups
Description: "Runs the email drafter agent. Takes hot leads and 
             generates personalized follow-up emails. Requires human 
             approval before sending."
```

The orchestrator's graph is simple — it's the same ReAct pattern you already know:

```
[Orchestrator LLM] ←→ [Tool: find_leads | score_leads | draft_emails]
```

The LLM decides which "sub-agent tool" to call, in which order, based on Alex's request. You don't hardcode the sequence.

---

## The Power of Composition

This pattern is powerful because:

1. **Each agent can be tested independently** — if scoring breaks, you fix the scorer, not the whole system
2. **Adding new capabilities is easy** — just add a new agent as a new tool
3. **The orchestrator adapts** — ask it something new and it figures out the right combination
4. **It scales** — 3 agents today, 10 tomorrow, same pattern

---

## What Makes a Good Orchestrator?

A good orchestrator needs:
- **Clear tool descriptions** — so it knows what each sub-agent can do
- **Access to shared State** — so it can pass results from one agent to the next
- **A good system prompt** — that defines its role and decision-making rules
- **Guardrails** — so it doesn't call agents unnecessarily or in wrong combinations

---

**Now it's your turn** → Exercise 05: Build the Orchestrator
