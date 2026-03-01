# Exercise 04 : Agent Rescue Mission

> **Duration**: 2h  
> **Difficulty**: ⭐⭐⭐  
> **What you'll build**: Nothing, you'll **fix** 4 broken agents.  
> **Format**: Escape game! 

---

## The Situation

Alex left his agents running overnight. He wakes up to chaos:
- 47 identical emails sent to the same prospect
- A lead scored at 15/10 (???)
- The database shows leads that don't exist
- One agent is still running since 3 AM

**Your mission**: Diagnose and fix each broken agent. For each one, you must:
1. **Read the logs** to understand what happened
2. **Identify** the failure mode (refer to Lecture 04)
3. **Fix** the code so it doesn't happen again
4. **Test** that the fix works

---

##  Case 1: The Email Spammer

**Symptom**: Lead "Sarah Chen" received 47 follow-up emails overnight.

**Files provided**: `broken_agent_1.py` (provided by your instructor)

**Your investigation**:
1. Read the code carefully. The agent is supposed to send ONE follow-up email per lead.
2. Look at the graph structure. What happens after `send_email` runs?
3. Find the bug and fix it.

**Hint**: Look at the edge that comes after the `send_email` node. Where does it go?

**Expected diagnosis**: The agent has an edge from `send_email` back to `check_leads` (creating a loop). After sending an email, it re-checks the database, finds the same lead (because `last_contacted_at` hasn't been updated yet due to a race condition), and sends another email.

**What to fix**:
- Add a `update_last_contacted` step **before** the loop-back edge
- Add a `max_iterations` limit as a safety net
- Add a duplicate-send check in the `send_email` tool

---

##  Case 2: The Impossible Score

**Symptom**: Lead "Marc Dubois" has a score of 15 out of 10.

**Files provided**: `broken_agent_2.py`

**Your investigation**:
1. Read the scoring prompt. What instructions does the AI receive?
2. Check the `update_lead_score` tool. Is there any validation?
3. Find where the system allows a score > 10.

**Expected diagnosis**: The LLM was not constrained to the 1-10 range. The prompt says "score this lead" but never says "between 1 and 10." The tool accepts any integer without validation.

**What to fix**:
- Add explicit range instructions in the prompt: "Score MUST be between 1 and 10"
- Add **code-level validation** in the tool: reject any score outside 1-10
- Return an error message to the AI so it can retry with a valid score

**Lesson**: Never trust LLM output for numerical values without validation. **Code guardrails > prompt instructions** for hard constraints.

---

##  Case 3: The Ghost Leads

**Symptom**: The database contains 3 leads that Alex never entered: "Test User", "Example Corp", and "John Doe".

**Files provided**: `broken_agent_3.py`

**Your investigation**:
1. This agent was supposed to only **read** from the database and **score** leads.
2. But it has a tool called `create_or_update_lead`. Read its description carefully.
3. Understand what happened.

**Expected diagnosis**: The tool description says "Creates a lead if it doesn't exist, or updates it if it does." When the AI tried to score leads, it hallucinated data for leads that didn't exist (common with LLMs) and the tool happily **created** them.

**What to fix**:
- **Principle of Least Privilege**: Split the tool into `read_lead` and `update_lead_score`. No create capability in a scoring agent.
- Remove any "create" functionality from tools that shouldn't create data
- Add a confirmation step for any write operation that wasn't explicitly requested

**Lesson**: Give agents the **minimum tools they need**. A scoring agent doesn't need create permissions. This is the "principle of least privilege", a security fundamental.

---

##  Case 4: The Infinite Thinker

**Symptom**: An agent started at 3 AM and is still running. CPU at 100%.

**Files provided**: `broken_agent_4.py`

**Your investigation**:
1. This agent was asked: "Analyze all leads and create a comprehensive report."
2. Look at the tool descriptions and the graph structure.
3. Find why the agent never terminates.

**Expected diagnosis**: The agent enters a loop:
1. Fetches leads → "I should analyze each one in detail"
2. Analyzes lead 1 → "I should cross-reference with other data"
3. Tries to call a non-existent tool → error → AI reasons "I should try again"
4. Retries → same error → "Let me try a different approach"
5. Calls the fetch again → starts over
6. Forever.

There is no **maximum iteration count** and no **stop condition** besides the AI deciding it's done (which it never does because it keeps hitting errors).

**What to fix**:
- Add `recursion_limit` when compiling the graph (e.g., `app = graph.compile(recursion_limit=25)`)
- Add an explicit "give up after N errors" counter in the State
- Improve error handling: when a tool fails, tell the AI clearly that the tool is unavailable (don't just pass the error silently)
- Add a fallback: "If you cannot complete the analysis, provide a partial report with what you have"

---

##  Scoring

For each case, you earn points for:
-  **Correct diagnosis** (identify the failure mode): 1 point
-  **Root cause** (explain WHY it happened): 1 point
-  **Fix implemented** (code actually works): 1 point
-  **Prevention** (the fix prevents future occurrences, not just this one): 1 point

**Target**: 12/16 or higher = you're ready for Day 2!

---

##  Takeaways

After completing all 4 cases, write down:

1. **My #1 debugging reflex will be**: _______________
2. **The most dangerous failure mode is**: _______________
3. **Every agent I build should have these 3 safety features**: 
   - _______________
   - _______________
   - _______________

---

## 🎉 Day 1 Complete!

Look at what you've accomplished today:
-  Built an agent that queries a database (Exercise 01)
-  Built an agent that reasons and writes back to a database (Exercise 02)
-  Built an agent with human oversight and an external API (Exercise 03)
-  Debugged 4 real-world agent failures (Exercise 04)

**Tomorrow**: What if all of these agents worked together, orchestrated by a single super-agent?
