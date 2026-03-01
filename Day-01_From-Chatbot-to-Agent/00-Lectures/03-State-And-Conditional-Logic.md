# Lecture 03 : State Management & Conditional Logic

> **Duration**: 15 min lecture (delivered just-in-time before Exercise 02)  
> **Objective**: Understand how to make agents that take different paths based on what they discover.

---

## The State Grows With Your Agent

In Exercise 01, your State was simple, a user request and some leads. Now we need to **enrich** it.

Think of it this way: Alex's assistant now needs to remember not just *what* leads exist, but *how good* they are. The State becomes a richer notepad:

```
State (before):
{
    "user_request": "...",
    "leads_found": [...]
}

State (after - enriched):
{
    "user_request": "...",
    "leads_found": [...],
    "lead_scores": {"lead_1": 8, "lead_2": 3, "lead_3": 9},
    "hot_leads": [...],
    "cold_leads": [...]
}
```

**Key insight** : Every time you add a capability to your agent, you extend the State. The State is your agent's growing memory.

---

## Conditional Edges : The Agent Makes Choices

Until now, our graph was basically linear. Now we introduce **branching**, the agent takes different paths depending on what it finds.

```
                    ┌──────────────────┐
                    │  Score the lead  │
                    └────────┬─────────┘
                             ▼
                    ┌──────────────────┐
                    │   Score > 7 ?    │
                    └───┬──────────┬───┘
                        │          │
                   YES  │          │  NO
                        ▼          ▼
              ┌──────────────┐  ┌──────────────┐
              │  "Hot lead"  │  │  "Cold lead" │
              │  → prioritize│  │  → archive   │
              └──────────────┘  └──────────────┘
```

In LangGraph, this is a **conditional edge**: a function that looks at the State and returns the name of the next node to execute.

**Real-world analogy** : It's like a mail sorter. Letters arrive, someone reads the address, and sends them down different conveyor belts based on the destination. The letters (State) carry the information; the sorter (conditional edge) makes the routing decision.

---

## The Difference Between AI Decisions and Code Decisions

There are **two ways** an agent can make decisions:

### 1. The LLM Decides (tool calling)
The AI model itself chooses what to do next. This is flexible but unpredictable.
```
User: "Handle this lead"
AI thinks: "I should check the database first" → calls tool
AI thinks: "Score looks good, let me draft an email" → calls another tool
```

### 2. Your Code Decides (conditional edge)
You write a function that checks the State and routes accordingly. This is predictable and reliable.
```python
# You decide the rule, not the AI
if state["lead_score"] > 7:
    return "hot_lead_path"
else:
    return "cold_lead_path"
```

**Best practice**: Use LLM decisions for *creative, ambiguous* tasks (like writing an email). Use code decisions for *critical business logic* (like whether a lead is qualified). Don't let the AI make decisions that should be rules.

---

## When Agents Go Wrong: A Preview

Here's something that will happen to you today: your agent will **score a lead incorrectly**.

Why? Because the LLM might:
- Ignore important information in the lead's profile
- Hallucinate details that don't exist
- Weight factors differently than you'd expect

This is **normal** and **expected**. It's not a bug in your code, it's the nature of AI reasoning. In Exercise 02, you'll encounter this firsthand, and we'll discuss how to handle it.

The lesson: **never blindly trust agent outputs on important decisions**. Always build in checkpoints.

---

**Next up**: Alex has too many leads. Let's help him prioritize → 
**[Exercise 02: Lead-Scoring](../01-Exercices/02-Lead-Scoring.md)**
