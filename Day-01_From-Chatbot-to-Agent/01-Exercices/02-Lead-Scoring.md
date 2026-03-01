# Exercise 02 : The Lead Scorer 

> **Duration**: 1h30  
> **Difficulty**: ⭐⭐  
> **What you'll build**: An agent that scores and categorizes leads automatically.

---

## The Problem

Alex just told you: *"I spent 2 hours last week on a call with someone who turned out to have zero budget. I need a way to know which leads are worth my time BEFORE I call them."*

**Your mission**: Build an agent that reads lead information from Supabase, scores each lead (1-10) based on criteria, and categorizes them as "hot", "warm", or "cold."

---

## Setup (5 min)

### Add Columns to Your Leads Table

Add these columns to your existing `leads` table:

| Column | Type | Default |
|---|---|---|
| `budget` | text | null |
| `timeline` | text | null |
| `decision_maker` | boolean | false |
| `score` | integer | null |
| `category` | text | null |

Update your sample leads with realistic data:
- Some leads should have clear budgets ("€10k-20k"), some vague ("TBD"), some empty
- Some have tight timelines ("next month"), some are far out ("maybe next year")
- Mix of decision makers and non-decision makers

---

## Part 1: Build the Scoring Tool (20 min) : By Hand

Create **two new tools** in `tools.py`:

### Tool 1: `get_unscored_leads`
- Queries Supabase for leads where `score` is null
- Returns the lead data including budget, timeline, decision_maker, and notes

### Tool 2: `update_lead_score`
- Takes a lead ID, a score (integer 1-10), and a category ("hot", "warm", "cold")
- Updates the lead in Supabase
- Returns a confirmation message

>  **Think about it**: Why are we making the "write" operation a separate tool? Because later, we'll want to add a safety check before writing to the database. Keeping reads and writes separate is a good design pattern.

---

## Part 2: Enrich Your Graph (30 min) : By Hand First

Extend your agent from Exercise 01:

1. **Add the new tools** to the agent's toolkit

2. **Update the system prompt** with scoring criteria:

```
Score leads from 1 to 10 based on these criteria:
- Budget: Clear budget (3 pts), Vague budget (1 pt), No budget (0 pts)
- Timeline: Within 3 months (3 pts), 3-6 months (2 pts), 6+ months or unclear (0 pts)
- Decision maker: Yes (2 pts), No (0 pts)  
- Engagement (from notes): Active/responsive (2 pts), Passive (1 pt), Unresponsive (0 pts)

Categories:
- Hot: Score 7-10
- Warm: Score 4-6
- Cold: Score 1-3
```

3. **Add a conditional edge** for the scoring path:
   - After scoring, if the lead is "hot" → log it as priority
   - If "cold" → suggest archiving it

4. **Test with**: `"Score all my unscored leads and tell me who I should focus on"`

---

## Part 3: Catch the Agent's Mistakes (20 min)

**This is intentional.** Run your agent and carefully check the scores it gives.

You'll likely notice at least one questionable score. For example:
- A lead with "budget: TBD" scored as 8/10
- A lead with "timeline: next year" scored as 7/10
- A lead with no notes scored highly because the AI "assumed" positive intent

**Your task**:
1. **Identify** at least one incorrect score
2. **Explain** why the AI made that mistake (check the reasoning in the messages)
3. **Fix it** by improving your system prompt to be more explicit about edge cases

> **Key lesson**: AI agents make plausible-sounding mistakes. If you don't check, you won't notice. This is why **human oversight** matters, we'll build this properly in Exercise 03.

---

## Part 4: Use Cursor to Improve (15 min), Cursor ON

Now use Cursor to:

1. Add **logging** to your tools, print what the agent is doing at each step:
   ```
   [TOOL] get_unscored_leads → Found 4 leads
   [TOOL] update_lead_score → Updated lead "John" to score 8 (hot)
   ```

2. Add a **summary function** that, after all leads are scored, produces a formatted output:
   ```
    Hot leads (3): Alice (9), Bob (8), Carol (7)
    Warm leads (1): Dave (5)
    Cold leads (2): Eve (2), Frank (1)
   ```

---

##  Success Criteria

Your agent works if:
- [ ] It correctly fetches unscored leads from Supabase
- [ ] It scores each lead based on the defined criteria
- [ ] It writes the scores back to Supabase
- [ ] You found and fixed at least one scoring mistake
- [ ] You can explain why the AI made that mistake

---

##  Reflection Questions

1. Your scoring criteria are in the **system prompt** (AI interpretation). Could some of them be in **code** instead (deterministic rules)? Which ones and why?
2. What happens if Alex adds a new lead while the agent is running? Does your agent handle this?
3. The agent wrote directly to the database without asking Alex. Is that OK for scoring? What about deleting leads?

---

**Next up**: Alex wants to send follow-up emails automatically → **[Exercice 03: Email-Follow-Up](03-Email-Follow-Up.md)**
