# Exercise 01 : The Forgotten Leads

> **Duration**: 1h30  
> **Difficulty**: ⭐ (your first agent!)  
> **What you'll build**: An agent that finds leads Alex forgot to follow up with.

---

## The Problem

Alex is a freelance consultant. He stores his leads in a Supabase table but keeps forgetting to follow up. Leads go cold because nobody contacts them after the first call.

**Your mission**: Build an AI agent that checks Alex's database, finds leads that haven't been contacted in over 3 days, and generates a follow-up draft for each.

---

## Setup (15 min)

### Step 1: Prepare the Supabase Table

In your Supabase project, create a table called `leads` with the following columns:

| Column | Type | Description |
|---|---|---|
| `id` | uuid (primary key) | Auto-generated |
| `name` | text | Lead's full name |
| `email` | text | Lead's email address |
| `company` | text | Lead's company name |
| `status` | text | "new", "contacted", "qualified", "lost" |
| `notes` | text | Free-form notes about the lead |
| `last_contacted_at` | timestamptz | When Alex last reached out |
| `created_at` | timestamptz | Auto-generated |

### Step 2: Insert Sample Data

Insert at least 6 leads, make sure **3 of them** have a `last_contacted_at` date older than 3 days, and **3 of them** were contacted recently.

>  **Tip**: Use realistic data! Give leads different companies, different notes. The more realistic, the better your agent's responses will be.

### Step 3: Set Up Your Project

Create a new Python project in **Cursor** with the following structure:

```
alex-agent/
├── agent.py          ← Your LangGraph agent
├── tools.py          ← Your Supabase tool functions
├── .env              ← Your API keys (never commit this!)
└── requirements.txt  ← Dependencies
```

Install the required packages:
```
langchain
langgraph
langchain-openai   (or langchain-anthropic if using Claude)
supabase
python-dotenv
```

---

## Part 1: Build the Tool (20 min) : No Cursor Autocomplete

> ⚠️ **Important**: For this first exercise, write the tool **by hand**. Turn off Cursor's autocomplete. You need to understand what every line does before we let AI help us.

**In `tools.py`**, create a function called `get_stale_leads` that:

1. Connects to your Supabase database using the credentials from `.env`
2. Queries the `leads` table for leads where `last_contacted_at` is older than N days
3. Returns the results as a list of dictionaries

**Then**, wrap this function as a LangGraph tool with:
- A clear **name**: `get_stale_leads`
- A clear **description**: Explain what it does, what parameter it takes, and what it returns
- A clear **input schema**: It takes one integer parameter, the number of days

> **Think about it**: Why does the description matter so much? Because the AI reads it to decide whether to use this tool. A vague description = an AI that doesn't know when to use your tool.

---

## Part 2: Build the Graph (30 min) :  Still No Cursor

**In `agent.py`**, build a LangGraph graph with:

1. **A State** with these fields:
   - `messages`: the conversation history (list)

2. **A node** called `agent` that:
   - Sends the messages to the LLM along with the available tools
   - The LLM decides whether to call a tool or respond directly

3. **A node** called `tools` that:
   - Executes whatever tool the LLM decided to call
   - Returns the result back to the messages

4. **A conditional edge** after the `agent` node:
   - If the LLM wants to use a tool → go to the `tools` node
   - If the LLM is ready to respond → go to `END`

5. **An edge** from `tools` back to `agent` (so the AI can reason about the tool's result)

**Test your agent** with this request:
```
"Find all leads that haven't been contacted in 3 days"
```

---

## Part 3: Make It Useful (15 min) : Cursor ON

Now turn Cursor's autocomplete back on. Use it to:

1. **Enhance the system prompt**: Tell the AI it's Alex's assistant, specialized in lead management. It should be proactive and concise.

2. **Improve the output**: The agent should not just list leads, it should generate a **brief follow-up message draft** for each stale lead, personalized based on the lead's `notes` and `company`.

3. **Test with different queries**:
   - "Any leads I should follow up with?"
   - "Show me leads from the last week that went cold"
   - "Who haven't I talked to recently?"

---

##  Success Criteria

Your agent works if:
- [ ] It correctly identifies leads older than 3 days without contact
- [ ] It generates personalized follow-up drafts (not generic templates)
- [ ] It handles the case where **no stale leads exist** (doesn't crash or hallucinate)
- [ ] You can explain what each node in your graph does

---

##  Reflection Questions

Before moving on, answer these for yourself:

1. When you typed the user query, **how did the AI decide** to use `get_stale_leads` instead of just answering from memory?
2. What would happen if your tool **description** was just "Gets leads"? Would the AI use it correctly?
3. Look at the messages in your State after the agent runs. Can you see the **ReAct loop** (Reason → Act → Observe → Reason)?

---

---

## Ready to go further?

In Exercise 01, you built your first agent that can find Alex’s forgotten leads.  
You now have a working ReAct loop with a real database tool behind it.

Before we make the agent smarter, we need to understand **how it keeps track of information** and **how it decides what to do next**.

That’s exactly what you’ll learn in the next lecture.

<div align="center">

**[➤ Lecture 03: State And Conditional Logic](../Lectures/03-State-And-Conditional-Logic.md)**

</div>
