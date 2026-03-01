# Instructional Design Challenge : Autonomous AI Agents with LangGraph

## Module Overview

**Title**: From Chatbot to Autonomous Agent  
**Duration**: 2 days (14 hours)  
**Ratio**: ~80% hands-on / ~20% theory  
**Stack**: Python, LangGraph, Supabase, FastAPI, Lovable (React), Cursor IDE

---

## Pedagogical Approach: "Learn by Solving"

This module follows a **problem-first** structure. Every learning block starts with a real problem faced by "Alex," a freelance consultant struggling to manage his leads. Students solve Alex's problems one by one, and theory arrives *after* practice as formalization of what they just experienced.

The key insight: **students never feel like they're "studying." They're building.**

### The Arc

| Exercise | Alex's Problem | Skills Acquired |
|---|---|---|
| 01 | Forgets to follow up with leads | First agent, ReAct pattern, LangGraph basics |
| 02 | Wastes time on cold leads | State management, conditional edges, scoring |
| 03 | Wants automated emails | External APIs, human-in-the-loop, safety |
| 04 | Agent went haywire overnight | Debugging, observability, failure modes |
| 05 | Tired of running 3 scripts | Multi-agent orchestration, composition |
| 06 | Needs calendar checking | Extensibility, autonomous tool creation |
| 07 | Wants it in his app | Deployment, FastAPI, frontend integration |

The twist: In Exercise 05, all the mini-agents from Day 1 **come together** as tools of a single orchestrator. Students experience the reward of seeing their independent projects compose into something greater.

---

## Cursor IDE Strategy

The module uses a deliberate **"understand then accelerate"** approach:

- **Exercises 01-03**: Cursor autocomplete OFF for first implementations. Students write key code by hand to understand the mechanics. Cursor is then turned ON for enhancements.
- **Exercise 04**: Debugging, Cursor is irrelevant here (you can't autocomplete your way out of a broken agent).
- **Exercises 05-07**: Cursor fully ON. By now students understand what Cursor generates and can evaluate its suggestions critically.

This prevents the "magic problem", students can always explain *why* their code works.

---

## Addressing the Constraints

| Challenge | Solution |
|---|---|
| **Conceptual leap** (chatbot → agent) | Start with a live demo of a finished agent, then deconstruct it. Use the n8n → LangGraph analogy. |
| **Debugging complexity** | Dedicated "escape game" exercise (04) with 4 pre-broken agents. Catalog of 5 failure modes taught explicitly. |
| **The "magic" problem** | Cursor OFF for first exposure to each concept. Manual-first, accelerate-second. |
| **Safety & ethics** | Human-in-the-loop introduced naturally via "do we want AI sending emails unsupervised?" Permission matrix (read/analyze/write/delete). |
| **Cognitive load** | Never more than 2 new tools per exercise. Supabase (known) before APIs (new). Graph vocabulary mapped to n8n concepts they already know. |

---

## File Structure

```
Instructional-Design-Challenge/
├── README.md (this file)
│
├── Day-01_From-Chatbot-to-Agent/
│   ├── 00-Lectures/
│   │   ├── 01-What-Is-An-Agent.md
│   │   ├── 02-LangGraph-Fundamentals.md
│   │   ├── 03-State-And-Conditional-Logic.md
│   │   └── 04-Debugging-Agents.md
│   │
│   ├── 01-Exercises/
│   │   ├── 01-Forgotten-Leads.md
│   │   ├── 02-Lead-Scoring.md
│   │   ├── 03-Email-Follow-Up.md
│   │   ├── 04-Agent-Rescue.md
│   │   └── broken_agents/
│   │       ├── broken_agent_1.py (student - without explanation)
│   │       ├── broken_agent_2.py (student)
│   │       ├── broken_agent_3.py (student)
│   │       └── broken_agent_4.py (student)
│   │
│   └── 03-Instructors/
│       ├── Solutions/
│       │   ├── Solutions_Day1.md (instructor)
│       │   ├── broken_agent_1.py (instructor - annotated version with explanations of bugs)
│       │   ├── broken_agent_2.py (instructor)
│       │   ├── broken_agent_3.py (instructor)
│       │   └── broken_agent_4.py (instructor)
│       └── Teaching_Notes.md (instructor)
│
├── Day-02_The-Autonomous-Agent/
│   ├── 00-Lectures/
│   │   ├── 05-Multi-Agent-Architecture.md
│   │   ├── 06-Extensibility-And-Permissions.md
│   │   └── 07-Deployment.md
│   │
│   ├── 01-Exercises/
│   │   ├── 05-The-Orchestrator.md
│   │   ├── 06-New-Power.md
│   │   └── 07-Going-Live.md
│   │
│   └── 03-Instructors/
│       ├── Solutions/
│       │   └── Solutions_Day2.md (instructor)
│       └── Teaching_Notes.md (instructor)
```
