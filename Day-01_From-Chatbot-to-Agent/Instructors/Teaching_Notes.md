# Teaching Notes — Day 1: From Chatbot to Agent

> **For instructors only. Do not share with students.**

---

## Overview & Pacing

| Time | Block | Type | Duration |
|---|---|---|---|
| 09:00 | Welcome + Live Demo | Lecture/Demo | 30 min |
| 09:30 | Lecture 01: What Is an Agent | Lecture | 20 min |
| 09:50 | Lecture 02: LangGraph Fundamentals | Lecture | 15 min |
| 10:05 | **Exercise 01: Forgotten Leads** | Hands-on | 1h30 |
| 11:35 | Break | — | 15 min |
| 11:50 | Lecture 03: State & Conditional Logic | Lecture | 15 min |
| 12:05 | **Exercise 02: Lead Scoring** | Hands-on | 1h15 |
| 13:20 | Lunch | — | 1h |
| 14:20 | Exercise 02 wrap-up + debrief | Discussion | 15 min |
| 14:35 | **Exercise 03: Email Follow-Up** | Hands-on | 2h |
| 16:35 | Break | — | 15 min |
| 16:50 | Lecture 04: Debugging Agents | Lecture | 20 min |
| 17:10 | **Exercise 04: Agent Rescue** | Hands-on | 1h30 |
| 18:40 | Day 1 Retrospective | Discussion | 20 min |

**Theory/Practice split**: ~1h30 lectures / ~6h15 hands-on = **~20% / 80%**

---

## Opening Demo (Critical : Sets the Tone)

**Prepare beforehand**: Have a fully working agent running locally that does the complete CRM flow (fetch leads → score → draft email → show for approval → send).

**How to run it**:
1. Open a terminal, run the agent
2. Type: "Find my stale leads, score them, and draft follow-up emails for the hot ones"
3. Let students watch the agent reason, call tools, and produce results
4. When it pauses for approval, show the drafted emails and approve one

**After the demo, ask**: "What just happened? How many steps did the AI take? Did I tell it which steps to take?"

This creates the "aha" moment that carries the rest of the day.

---

## Exercise 01 : Common Pitfalls & How to Help

### Expected Issues:
1. **Supabase connection errors**: Most common issue. Verify `.env` file has correct URL and anon key. RLS policies might block the query — help students add a simple SELECT policy.

2. **Tool not being called**: The AI ignores the tool and tries to answer from memory. Fix: improve the system prompt to explicitly say "You MUST use the get_stale_leads tool to check the database. Never guess."

3. **Import confusion**: Students mix up `langchain` vs `langgraph` imports. Provide a clear import cheat sheet on the board.

### The "No Cursor" Rule:
Students will resist turning off autocomplete. Explain: "In 30 minutes, I'll let you turn it back on. But right now, you need to understand what every line does. Trust the process."

If a student is really stuck after 15 min, allow them to use Cursor for the tool definition only, but make them explain each line to you.

---

## Exercise 02 : The Intentional Mistake

### Setup:
Design your sample data so that at least one lead will be scored incorrectly. For example:
- Lead with `budget: "TBD"` and `notes: "Very enthusiastic on the call"` → The AI will likely score high (8-9) despite no confirmed budget
- Lead with `budget: "€50k"` but `timeline: "maybe next year"` and `decision_maker: false` → Should be warm, AI might score hot

### Debrief the Mistake:
After students find incorrect scores, lead a 5-min discussion:
- "How many of you found a wrong score?" (most hands should go up)
- "This is NOT a bug. This is the nature of LLM reasoning. They make plausible mistakes."
- "This is why Exercise 03 adds human review, and why it matters."

---

## Exercise 03 : Human-in-the-Loop

### Key Teaching Moment:
Before students start, pose the ethical question: "If this agent sends a bad email to a real client, who is responsible? Alex? The AI? You, the developer?"

Let them discuss for 2-3 minutes. There's no right answer, the point is to create awareness.

### Technical Note on `interrupt_before`:
Students will struggle with the checkpoint/interrupt mechanism. Walk through the concept on the board:

```
Graph runs → reaches send_emails → STOPS
State is saved to checkpointer
You inspect the State, modify if needed
You call graph.invoke(None, config) → graph RESUMES from where it stopped
```

Show this live with a simple example before they attempt it.

### If Time Runs Short:
Exercise 03 can be shortened by skipping Part 4 (guardrails). The core learning (human-in-the-loop) is in Parts 1-3.

---

## Exercise 04 : Agent Rescue

### Preparation:
You MUST prepare the 4 broken agent files in advance. Place them in the `03-Instructors/Solutions/` folder.

### Facilitation Tips:
- Run it as a **timed challenge**: 25 min per case, with a 5-min group debrief after each
- Encourage **pair work**, debugging is better with two brains
- After each case, ask ONE student to explain their diagnosis to the group
- Keep a scoreboard on the whiteboard for engagement

### If Students Finish Early:
Ask them to add **unit tests** for the fix. Can they write a test that would have caught the bug?

---

## Day 1 Retrospective (20 min)

Ask three questions:
1. "What's the one thing you understood today that was confusing this morning?"
2. "What concept are you still unsure about?"
3. "On a scale of 1-5, how confident are you building an agent from scratch?"

Use the answers to adjust Day 2 pacing. If confidence is low, spend more time on the Day 2 warmup.

---

## Key Vocabulary to Reinforce Throughout the Day

Write these on the board and point to them whenever they come up:
- **ReAct**: Reason → Act → Observe → Repeat
- **State**: The agent's memory (dictionary that travels through the graph)
- **Tool**: A function the AI can decide to call
- **Conditional Edge**: A fork in the graph based on a condition
- **Human-in-the-Loop**: Pausing the agent for human approval
- **Recursion Limit**: Maximum number of loops to prevent infinite runs
