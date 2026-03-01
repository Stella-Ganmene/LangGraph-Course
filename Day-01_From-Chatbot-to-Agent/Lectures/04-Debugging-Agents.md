# Lecture 04 : When Agents Fail: A Debugging Guide

> **Duration**: 20 min lecture (delivered before Exercise 04)  
> **Objective**: Learn the 5 most common ways agents break and how to diagnose them.

---

## Agents Fail Differently Than Normal Code

When a regular Python script fails, you get an error message with a line number. You fix it and move on.

When an agent fails, it's often **silent**. The agent doesn't crash, it just does the wrong thing. It might:
- Query the database 50 times in a row for no reason
- Send the same email to the same person 12 times
- Confidently give you an answer based on data it made up
- Run forever without producing a result

This makes debugging agents one of the **most important skills** you'll learn today.

---

## The 5 Failure Modes of AI Agents

###  Failure 1: The Infinite Loop

**What happens**: The agent keeps calling the same tool over and over, never reaching a conclusion.

**Why it happens**: The AI reasons "I need more information" → calls a tool → gets a result → reasons "I still need more information" → calls the same tool again → forever.

**How to spot it**: Your agent runs for minutes without responding. Logs show the same tool being called repeatedly.

**How to fix it**:
- Set a **maximum number of iterations** (e.g., max 10 tool calls)
- Add a **stop condition** in your graph
- Improve the tool description so the AI knows when it has enough data

---

###  Failure 2: Tool Hallucination

**What happens**: The AI tries to call a tool that doesn't exist, or passes wrong parameters.

**Why it happens**: The LLM "imagines" a tool based on its training data. It might try to call `search_google()` even though you only gave it `query_supabase()`.

**How to spot it**: Error messages about unknown functions or invalid parameters.

**How to fix it**:
- Make your tool descriptions **very explicit** about what each tool does and doesn't do
- Validate tool inputs before executing them
- Give the AI a clear list of available tools in the system prompt

---

###  Failure 3: Reasoning Hallucination

**What happens**: The agent makes confident but wrong conclusions from the data.

**Why it happens**: The LLM interprets data creatively. A lead with "budget: TBD" might get scored as high-budget because the AI assumes "they'll figure it out."

**How to spot it**: Results that look plausible but are factually wrong when you check the source data.

**How to fix it**:
- Add **explicit scoring criteria** in your prompts (not just "score this lead")
- Log the AI's reasoning at each step so you can trace where it went wrong
- For critical decisions, use **code-based rules** instead of AI judgment

---

###  Failure 4: State Corruption

**What happens**: The State gets overwritten or lost between nodes, so the agent "forgets" what it did.

**Why it happens**: A node writes to the wrong key, or two nodes overwrite each other's data.

**How to spot it**: The agent repeats actions it already did, or produces results that ignore previous steps.

**How to fix it**:
- **Log the State after every node**, this is your #1 debugging tool
- Use descriptive, unique key names in your State
- Make sure nodes **add** to the State (append) rather than **replace** it

---

###  Failure 5: External Service Timeout

**What happens**: An API call or database query takes too long or fails, and the agent doesn't handle it.

**Why it happens**: External services are unreliable. Supabase might be slow, an API might return an error, a rate limit might be hit.

**How to spot it**: The agent hangs or crashes with a network error.

**How to fix it**:
- Always wrap tool calls in **try/except** blocks
- Set **timeouts** on all external calls
- Implement **retry logic** (try again once or twice before giving up)
- Have a **fallback behavior** ("If I can't reach the API, tell the user instead of crashing")

---

## The Debugging Mindset

When your agent does something unexpected, follow this checklist:

```
1. CHECK THE LOGS   → What did the agent actually do? (step by step)
2. CHECK THE STATE  → What data did it have at each step?
3. CHECK THE TOOLS  → Did the tools return what you expected?
4. CHECK THE PROMPT → Did the AI have clear enough instructions?
5. CHECK THE EDGES  → Did the graph route to the right nodes?
```

**Golden rule**: Never guess. Always look at the logs first.

---

## Adding Observability To Your Agent

"Observability" is a fancy word for **being able to see what your agent is doing**. It means adding logging at key points:

```
[2026-01-15 10:23:01] Node: analyze_request → Received user query
[2026-01-15 10:23:02] Node: analyze_request → Decision: need to query database
[2026-01-15 10:23:02] Tool: get_stale_leads(days=3) → Called
[2026-01-15 10:23:03] Tool: get_stale_leads → Returned 3 leads
[2026-01-15 10:23:03] State update: leads_found = [lead_1, lead_2, lead_3]
[2026-01-15 10:23:04] Node: generate_response → Drafting emails for 3 leads
[2026-01-15 10:23:06] → Agent complete. 3 drafts generated.
```

With logs like these, when something goes wrong, you can **replay the agent's thought process** and find exactly where it went off track.

---

**Now it's your turn**  Exercise 04: **[Exercise 04: Agent Rescue Mission (fixing broken agents!)](../Exercices/04-Agent-Rescue.md)**
