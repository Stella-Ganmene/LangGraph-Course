# Teaching Notes  Day 2: The Autonomous Agent

> **For instructors only. Do not share with students.**

---

## Overview & Pacing

| Time | Block | Type | Duration |
|---|---|---|---|
| 09:00 | Day 1 Recap + Q&A | Discussion | 20 min |
| 09:20 | Lecture 05: Multi-Agent Architecture | Lecture | 20 min |
| 09:40 | **Exercise 05: The Orchestrator** | Hands-on | 2h |
| 11:40 | Break | — | 15 min |
| 11:55 | Lecture 06: Extensibility & Permissions | Lecture | 15 min |
| 12:10 | **Exercise 06: New Power** | Hands-on | 1h10 |
| 13:20 | Lunch | — | 1h |
| 14:20 | Exercise 06 completion | Hands-on | 50 min |
| 15:10 | Lecture 07: Deployment | Lecture | 15 min |
| 15:25 | **Exercise 07: Going Live** | Hands-on | 2h |
| 17:25 | Break | — | 10 min |
| 17:35 | Grand Demo (students show their work) | Presentations | 45 min |
| 18:20 | Module Retrospective + Closing | Discussion | 20 min |

**Theory/Practice split**: ~1h10 lectures / ~6h hands-on = **~15% / 85%** 

---

## Day 1 Recap (Critical Start)

Start by asking: "Who can draw the ReAct loop on the board?" Pick a volunteer. Then ask: "Who can name the 5 failure modes from yesterday?" Pick another volunteer.

This serves two purposes:
1. Refreshes key concepts
2. Tells you who's confident and who needs support today

If the group seems uncertain, spend 10 extra minutes doing a quick live demo of a Day 1 agent to re-anchor.

---

## Exercise 05  Orchestrator: Key Teaching Moments

### The "Aha" Moment
The biggest moment of Day 2 is when students realize: "Wait, I'm using the SAME pattern as Exercise 01, but my tools are entire agents."

Reinforce this explicitly: "You already know this architecture. The only thing that changed is what the tools do internally. That's the power of abstraction."

### Common Issues:

1. **Sub-agent results not passing correctly**: Students may struggle to get the output of `find_stale_leads` to feed into `score_leads`. The key is that the orchestrator's LLM sees the tool results in the messages and decides to pass them along. If it doesn't, improve the system prompt: "When you find leads, immediately score them before doing anything else."

2. **Too many LLM calls**: In the full pipeline, there can be 8-12 LLM calls (orchestrator reasoning + each sub-agent's reasoning). Students may notice latency. This is a good teaching moment about cost and efficiency.

3. **Human-in-the-loop breaking in orchestration**: The interrupt might not propagate correctly when nested. If this happens, simplify: have the orchestrator collect drafts and pause at the orchestrator level rather than inside the sub-agent.

### If Students Are Ahead:
Ask them to add a "dry run" mode: the orchestrator explains what it WOULD do without actually doing it. This tests their understanding of the routing logic.

---

## Exercise 06 : The Autonomy Test

### Instructor Role Changes Here
In Exercises 01-04, you were actively guiding. In Exercise 06, **step back**. Let students struggle. Only intervene if they're stuck for more than 15 minutes.

This is intentional. The goal is to verify they can apply the pattern independently.

### What to Watch For:
- Do they create proper tool descriptions? (If vague → they didn't learn from Day 1)
- Do they add input validation? (If missing → remind them of the "impossible score" bug)
- Do they apply the permission matrix? (Read = auto, write = confirm?)
- Can they integrate without modifying existing code? (If they have to rewrite the orchestrator → their architecture isn't modular enough)

### Debrief:
Ask: "How many lines of code did you change in the orchestrator?" The answer should be < 10 (imports + prompt update + tool list). If it's more, discuss why and how to improve modularity.

---

## Exercise 07 : Deployment

### Keep It Simple
The FastAPI deployment can become a rabbit hole. Keep students focused on:
1. Getting the basic endpoint working
2. Getting the frontend connected
3. Getting the human-in-the-loop working through the UI

Authentication, rate limiting, and logging are "nice to have", don't let perfect be the enemy of done.

### Lovable Integration Tips:
- Students may have different Lovable setups. Provide a minimal chat component template if needed.
- The biggest issue will be CORS. Make sure they add the middleware correctly.
- If Lovable's hosting doesn't support custom backend calls, have them run the frontend locally too.

### If the Frontend Is Too Slow:
Some students might not be comfortable with React/Lovable. Offer an alternative: test with the FastAPI docs page (`/docs`) which provides an interactive UI for testing endpoints. The architecture concepts are the same.

---

## Grand Demo (45 min)

### Format:
- Each student (or pair) gets 3-5 minutes to demo their agent
- They should show: a user request → agent reasoning → tool calls → result
- Encourage them to try a request they haven't tested before (live debugging is fine!)

### What to Celebrate:
- The complete pipeline working end-to-end
- Creative additions (bonus tools, nice UI touches)
- Good error handling ("look, it didn't crash!")
- Clear explanations of architecture decisions

### Questions to Ask During Demos:
- "What happens if the API is down right now?" (Error handling)
- "What if a new intern joins, can they use your agent safely?" (Permissions)
- "What would you add if you had one more day?" (Vision)

---

## Module Retrospective (20 min)

### Run a Quick Survey:
Ask students to rate (1-5) on a piece of paper:
1. Confidence building agents from scratch
2. Confidence debugging agents
3. Confidence explaining agent architecture to someone else
4. Overall module satisfaction

### Closing Message:
"Two days ago, you didn't know what a graph, a node, or an edge was. Now you've built a multi-agent system with database integration, external APIs, human oversight, error handling, and deployment. The pattern you learned, State, Nodes, Edges, Tools, is the same pattern used by companies building production AI agents. You're not beginners anymore. Go build."

---

## Contingency: If Things Run Behind

**Priority cuts** (what to skip if time is tight):
1. Exercise 07 Part 3 (production safety), nice to have, not critical
2. Exercise 06 bonus challenge, optional enrichment
3. Exercise 07 Part 2 (frontend integration), can be replaced with FastAPI /docs UI testing
4. Grand demos can be shortened to 2 min per student

**Never cut**:
- Exercise 05 (orchestrator is the capstone)
- Exercise 06 (autonomy test proves learning)
- Reflection questions (meta-learning is what sticks)
