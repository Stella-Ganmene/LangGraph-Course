# Exercise 05 : The Orchestrator 

> **Duration**: 2h  
> **Difficulty**: ⭐⭐⭐⭐  
> **What you'll build**: A meta-agent that coordinates all your Day 1 agents.

---

## The Problem

Alex: *"I love what you built yesterday! But I don't want to run 3 different scripts. I want ONE assistant where I can just say what I need, and it figures out the rest."*

**Your mission**: Build an orchestrator agent that listens to Alex's request and decides which sub-agents to call, in what order, to get the job done.

---

## Part 1: Wrap Your Agents as Tools (30 min)

Take your 3 agents from Day 1 and turn them into callable tools.

### Tool 1: `find_stale_leads`
- **Wraps**: Your Exercise 01 agent
- **Input**: Number of days (default: 3)
- **Output**: List of stale leads with their details
- **Description**: "Searches the database for leads that haven't been contacted in N days. Returns lead names, emails, companies, and notes. Use this when Alex asks about forgotten or stale leads."

### Tool 2: `score_leads`
- **Wraps**: Your Exercise 02 agent
- **Input**: Optional list of lead IDs (if empty, scores all unscored leads)
- **Output**: Scored leads with categories
- **Description**: "Evaluates leads and assigns a score from 1-10 with a category (hot/warm/cold). Use this when Alex wants to know which leads to prioritize."

### Tool 3: `draft_follow_up_emails`
- **Wraps**: Your Exercise 03 agent
- **Input**: List of lead IDs to email, or "hot" to email all hot leads
- **Output**: Draft emails ready for review
- **Description**: "Generates personalized follow-up emails for specified leads. Emails require Alex's approval before sending. Use this when Alex wants to reach out to leads."

>  **Key insight**: These tools don't call the LLM directly, they run an entire LangGraph agent internally. The orchestrator doesn't know or care about the internal complexity. It just calls a tool and gets a result. This is **abstraction** at work.

---

## Part 2: Build the Orchestrator Graph (40 min)

Create a new file: `orchestrator.py`

Your orchestrator is structurally simple, it's the same ReAct pattern from Exercise 01, but with more powerful tools:

1. **State**: `MessagesState` (same as before)

2. **System prompt** for the orchestrator:
```
You are Alex's autonomous business assistant. You help manage 
his freelance consulting leads.

You have access to specialized sub-agents:
- find_stale_leads: Discovers forgotten leads
- score_leads: Evaluates and prioritizes leads  
- draft_follow_up_emails: Creates personalized outreach

When Alex gives you a task:
1. Break it down into steps
2. Use the right sub-agent(s) in the right order
3. Pass results between steps when needed
4. Provide a clear summary of everything you did

IMPORTANT: 
- Always find leads before scoring them (you can't score what you haven't found)
- Always score before emailing (only email hot leads)
- Never skip steps, if Alex says "email my stale leads", you need to find → score → draft
```

3. **Graph**: Same ReAct structure, LLM node ↔ Tool node, with conditional edges

4. **Compile** with a recursion limit and a checkpointer (for the email approval interrupt)

---

## Part 3: Test Complex Requests (30 min)

Run your orchestrator with increasingly complex requests:

### Test 1: Single Agent
```
"Who haven't I contacted this week?"
```
**Expected**: Orchestrator calls `find_stale_leads` → returns list.

### Test 2: Two-Agent Chain
```
"Score my stale leads and tell me which are worth pursuing"
```
**Expected**: Calls `find_stale_leads` → passes results to `score_leads` → returns prioritized list.

### Test 3: Full Pipeline
```
"Handle my leads: find the ones I've been neglecting, figure out which 
ones are hot, and draft follow-up emails for them"
```
**Expected**: `find_stale_leads` → `score_leads` → `draft_follow_up_emails` → pause for review.

### Test 4: Ambiguous Request
```
"I have a busy week coming up. Help me focus on what matters."
```
**Expected**: The orchestrator should interpret this as "find and prioritize leads" and call the right agents. If it doesn't, improve the system prompt.

---

## Part 4: Add a Summary Layer (20 min)

After the orchestrator completes its work, it should provide a **unified summary**, not just raw tool outputs.

Enhance the system prompt so the final response looks like:

```
 Weekly Lead Report for Alex

 Stale Leads Found: 5
   - Sarah Chen (TechCorp), 5 days, no contact
   - Marc Dubois (DataFlow), 4 days, no contact
   - Lisa Wang (StartupXYZ), 3 days, no contact
   ... 

 Scoring Results:
    Hot (3): Sarah Chen (9), Marc Dubois (8), Lisa Wang (7)
    Warm (1): Jake Smith (5)
    Cold (1): Tom Brown (2)

 Email Drafts Ready (3):
   1. Sarah Chen : "Following up on our TechCorp discussion..."
   2. Marc Dubois : "Quick update on the DataFlow integration..."
   3. Lisa Wang : "Excited to continue our StartupXYZ conversation..."

 Awaiting your approval to send.
```

---

## Success Criteria

- [ ] The orchestrator correctly chains agents in the right order
- [ ] Results from one agent flow into the next (lead IDs pass from finder to scorer)
- [ ] Email drafting still pauses for human approval (the interrupt survives the orchestration)
- [ ] Ambiguous requests are handled reasonably
- [ ] Final summary is clear and actionable

---

##  Reflection Questions

1. The orchestrator is itself an agent using the ReAct pattern. It's the **same architecture** as Exercise 01, just with more powerful tools. Does this pattern feel natural now?
2. What would happen if you gave the orchestrator a tool it shouldn't have, like `delete_all_leads`? How would you prevent misuse?
3. How many LLM calls happen in Test 3? (Count: orchestrator reasoning + each sub-agent's reasoning). Why does this matter for cost?

---
### Course 06 : Adding a brand new capability

Before starting this exercise, review the course material:  **[➤ Lecture 06: ](../00-Lectures/06-Extensibility-And-Permissions.md)**
