# Lecture 01 : What Is an AI Agent?  

> **Duration**: 20 min lecture + 10 min discussion  
> **Objective**: Understand the fundamental difference between a chatbot and an agent, and discover the ReAct pattern.

---

## The scenario That Changes Everything

Before any theory, imagine a real user making a request to an AI assistant.

They ask : *"Find my leads that haven't been contacted in 3 days and draft follow-up emails for each."*

Now observe how the assistant handles that request step by step :
1. The AI **reasons**: "I need to check the database for stale leads."
2. The AI **acts**: It queries the Supabase database.
3. The AI **observes**: "I found 3 leads without recent contact."
4. The AI **reasons again**: "Now I need to write personalized emails for each."
5. The AI **acts again**: It drafts 3 different emails based on each lead's context.

**Question for you**: Could ChatGPT do this on its own? Why or why not?    

---
To understand why this matters, we need to clarify one key distinction: chatbot vs agent.
## Chatbot vs. Agent: The Key Difference

| | Chatbot | Agent |
|---|---|---|
| **Takes initiative** | No, it waits for your input | Yes, it decides what to do next |
| **Uses tools** | No, it only generates text | Yes, it can query databases, call APIs, send emails |
| **Remembers its plan** | No, each message is independent | Yes, it tracks what it has done and what's left |
| **Makes decisions** | No, it follows a fixed script | Yes, it chooses which action to take based on context |

**The simplest way to think about it:**
- A **chatbot** is like a customer service script, it answers what you ask.
- An **agent** is like a competent employee, you give it a goal, and it figures out the steps.

---

## The ReAct Pattern : How Agents Think

The magic behind agents has a name: **ReAct** (Reasoning + Acting).

It's a loop:

```
1. REASON  → "What should I do next?"
2. ACT     → Execute a tool (database query, API call, etc.)
3. OBSERVE → "What did I get back?"
4. REPEAT  → Back to step 1 until the task is complete
```

This is exactly what you just observed in the scenario. The AI doesn't just generate text, it **thinks**, **does**, **looks at the result**, and **thinks again**.

**Real-world analogy**: Imagine you ask a colleague to book a restaurant for a team dinner.

They would:
1. *Think*: "I need to know how many people, their dietary restrictions, and a date."
2. *Act*: Check the team calendar.
3. *Observe*: "Tuesday works for everyone."
4. *Think*: "Now I need to find a restaurant that fits 8 people with one vegetarian."
5. *Act*: Search restaurants online.
6. *Observe*: "Found 3 options."
7. *Think*: "I should pick the one closest to the office."
8. *Act*: Book it and send the confirmation.

An AI agent does **exactly this**,  but with code instead of phone calls.

---

## What Is LangGraph?

You've already used **n8n** to build automations. LangGraph is similar in concept but designed specifically for AI agents.

| n8n | LangGraph |
|---|---|
| Visual workflow builder | Code-based workflow builder |
| Nodes = fixed actions | Nodes = can include AI reasoning |
| Linear or branching flows | Dynamic flows where the AI decides the next step |
| Great for simple automations | Great for complex, AI-driven decisions |

**In LangGraph, you build a "graph"**, but don't let the word scare you. A graph is simply:
- **Nodes**: Steps in your process (like boxes in a flowchart)
- **Edges**: Connections between steps (like arrows in a flowchart)
- **State**: The "memory" that travels through the process

If you've ever drawn a flowchart, you already understand graphs.

---

## What You'll Build Today

Today, you'll solve 4 real problems for **Alex**, a freelance consultant who struggles to manage his leads:

| Mini-Project | Problem | What You'll Learn |
|---|---|---|
| **Forgotten Leads** | Alex forgets to follow up with prospects | Your first agent + ReAct in action |
| **Lead Scoring** | Alex wastes time on cold leads | Conditional logic + state management |
| **Email Follow-Up** | Alex wants automated personalized emails | External APIs + human-in-the-loop |
| **Agent Rescue** | Alex's agent went haywire overnight | Debugging + observability |

Each mini-project builds on the previous one. By the end of the day, you'll have 3 working agents and the skills to fix them when they break.

---

## Key Vocabulary

| Term | Plain English |
|---|---|
| **Agent** | An AI that can reason, use tools, and act autonomously |
| **ReAct** | The think → act → observe loop that agents follow |
| **Tool** | A function the agent can call (database query, API, etc.) |
| **Graph** | A flowchart that defines the agent's possible paths |
| **Node** | One step in the graph (a box in the flowchart) |
| **Edge** | A connection between nodes (an arrow in the flowchart) |
| **State** | The shared memory that passes between nodes |

---

**Next up**: Let's get our hands dirty with LangGraph!   **[Lecture 02: LangGraph Fundamentals](02-LangGraph-Fundamentals.md)**






