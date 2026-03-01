# Lecture 02 : LangGraph Fundamentals

> **Duration**: 15 min lecture (delivered just-in-time before Exercise 01)  
> **Objective**: Understand the 3 building blocks of LangGraph: State, Nodes, and Edges.

---

## The Three Building Blocks

Every LangGraph agent is built from exactly **3 ingredients**:

### 1. State, The Agent's Notepad

The State is a dictionary that travels through the entire graph. Every node can **read** from it and **write** to it.

Think of it like a clipboard that gets passed from person to person in an office. Each person reads what's on it, does their job, and writes their results back on the clipboard before passing it along.

```
State = {
    "user_request": "Find my stale leads",
    "leads_found": [],           ← filled by the database node
    "drafts_generated": [],      ← filled by the AI node
    "actions_taken": []           ← filled by the action node
}
```

**Key rule**: The State is how nodes communicate. If a node doesn't write to the State, the next node won't know what happened.

### 2. Nodes, The Workers

Each node is a function that:
1. Receives the current State
2. Does something (AI reasoning, database query, API call)
3. Returns an updated State

```
[Analyze Request] → [Query Database] → [Generate Response]
     node 1              node 2              node 3
```

### 3. Edges, The Arrows

Edges connect nodes and define **which node runs next**. There are two types:

- **Normal edge**: Always goes to the same next node (a straight arrow)
- **Conditional edge**: The AI decides which node to go to next (a fork in the road)

```
                         ┌─ "needs data" → [Query DB]
[Analyze Request] ──────┤
                         └─ "ready to respond" → [Generate Response]
```



This is the power of LangGraph, the AI itself decides the path through the graph.

---

## Your First Graph: A Visual Blueprint

Before writing any code, let's draw the graph we'll build in Exercise 01:

```
    ┌──────────────┐
    │    START      │
    └──────┬───────┘
           ▼
    ┌──────────────┐
    │  AI Reasons   │ ◄──────────────┐
    │  (LLM node)   │                │
    └──────┬───────┘                │
           ▼                        │
     ┌─────────────┐               │
     │  Decision:   │               │
     │  use tool?   │               │
     └──┬───────┬──┘               │
        │       │                   │
    yes │       │ no                │
        ▼       ▼                   │
  ┌──────────┐  ┌──────────┐       │
  │ Run Tool │  │   END    │       │
  │(Supabase)│  └──────────┘       │
  └────┬─────┘                     │
       │                           │
       └───────────────────────────┘
       (result goes back to AI)
```

**Read this diagram out loud:**
1. The AI receives the user's request and **reasons** about it.
2. If it decides it needs data → it runs a **tool** (like a Supabase query).
3. The tool result goes back to the AI, which **reasons again** with the new information.
4. When the AI has enough information → it produces a **final response** and stops.

This is the ReAct loop, implemented as a graph. You'll see this pattern in every agent you build.

---

## The Anatomy of a LangGraph Tool

A "tool" is just a Python function with a description that tells the AI what it does:

```
Tool: get_stale_leads
Description: "Retrieves leads from the database that haven't 
             been contacted in the last N days"
Input: number of days (integer)
Output: list of leads with their details
```

The AI reads the description and **decides on its own** whether to use the tool. You don't hardcode "use this tool" the AI figures it out from context.

This is why good tool descriptions matter: a vague description = an AI that doesn't know when to use the tool.

---

## Important Concept: Why Graphs, Not Chains?

You might wonder: why not just chain functions together in a line?

**Chain** (fixed sequence):
```
Step 1 → Step 2 → Step 3 → Done
```

**Graph** (dynamic, AI-driven):
```
Step 1 → Decision → Step 2a or Step 2b → Back to Decision → Step 3 → Done
```

A chain always does the same thing. A graph lets the AI **adapt** based on what it discovers. That's what makes it an agent instead of a script.

---

**Now it's your turn** → Exercise 01: **[Exercise 01: The Forgotten Leads](../Exercices/01-Forgotten-Leads.md)**
