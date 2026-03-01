# Exercise 03 : The Email Follow-Up

> **Duration**: 2h  
> **Difficulty**: ⭐⭐⭐  
> **What you'll build**: An agent that drafts and sends personalized emails,  but asks Alex first.

---

## The Problem

Alex is excited. "My leads are scored! Now I want the agent to **send follow-up emails** to hot leads automatically."

You could build that. But should you?

Imagine the agent sends a badly worded email to Alex's biggest prospect. Or sends 5 emails to the same person. Or promises a discount Alex never offered.

**Your mission**: Build an agent that drafts personalized emails, shows them to Alex for approval, and only sends after human confirmation.

---

## The Big Idea : Human-in-the-Loop

Not everything should be automated. The smartest agents know **when to ask for permission**.

Here's our new graph:

```
[Get Hot Leads] → [Draft Email] → [PAUSE: Show to Alex] → [Send Email]
                                          │
                                    Alex says "no"
                                          │
                                          ▼
                                   [Revise Draft]
                                          │
                                          ▼
                                  [PAUSE: Show again]
```

The key node here is **PAUSE**, the agent stops, presents its work, and waits for human input before continuing.

---

## Setup (10 min)

### Option A: Real Email API (Resend)

Sign up for a free account at [resend.com](https://resend.com) and get an API key. Free tier allows 100 emails/day, perfect for testing.

### Option B: Mock Email API (Simpler)

If you prefer, create a mock function that **prints** the email instead of sending it. This is fine for learning, the concepts are the same.

```python
# Mock version : replace with real API later
def send_email(to, subject, body):
    print(f" Would send to: {to}")
    print(f"   Subject: {subject}")
    print(f"   Body: {body}")
    return {"status": "sent", "to": to}
```

---

## Part 1: Build the Email Tool (20 min) : By Hand

Create a new tool in `tools.py`:

### Tool: `send_follow_up_email`
- **Inputs**: lead email, subject line, email body
- **Action**: Sends the email via your chosen API (or mock)
- **Output**: Confirmation with timestamp

>  **Important**: This tool **writes to the outside world**. Sending an email is irreversible. This is fundamentally different from reading a database. Keep this distinction in mind, it matters.

---

## Part 2: Build the Human-in-the-Loop Graph (40 min)

This is the most architecturally interesting exercise so far. Your graph needs a new concept: **interruption**.

### The Flow:

1. **Node: `get_hot_leads`** : Fetch leads with score ≥ 7 from Supabase

2. **Node: `draft_emails`** : The LLM generates a personalized email for each hot lead, using their name, company, notes, and context

3. ** Interrupt: `human_review`**  The graph **pauses**. It displays the drafted emails to Alex and waits for input:
   - "approve" → continue to sending
   - "edit" → Alex modifies the draft, then continue
   - "reject" → skip this email

4. **Node: `send_emails`** : Send only the approved emails

5. **Node: `log_activity`** : Update Supabase: set `last_contacted_at` to now, add a note about the follow-up

### How to Implement the Interrupt:

LangGraph has a built-in mechanism for this: **`interrupt_before`**. When the graph reaches a node marked with `interrupt_before`, it stops and returns the current State. You can then:
1. Inspect the State (show the drafts to Alex)
2. Modify the State if needed (Alex edits a draft)
3. Resume the graph (it continues from where it paused)

**Hint**: When adding the `send_emails` node to your graph, configure it with:
```python
graph.add_node("send_emails", send_emails_node)
# The interrupt happens BEFORE this node runs
```

And compile the graph with:
```python
app = graph.compile(checkpointer=checkpointer, interrupt_before=["send_emails"])
```

---

## Part 3: Test the Safety Net (30 min)

Run your agent and test these scenarios:

### Scenario A: Happy Path
1. Ask: "Send follow-up emails to all hot leads"
2. The agent drafts emails → pauses for review
3. Approve all emails → they get sent
4. Check Supabase: `last_contacted_at` should be updated

### Scenario B: Alex Rejects One
1. Same request
2. Agent drafts 3 emails → pauses
3. Reject one email, approve the other 2
4. Verify: only 2 emails sent, rejected lead unchanged in DB

### Scenario C: The Bad Draft
1. Same request
2. Agent drafts an email that's too aggressive or promises something wrong
3. Edit the draft manually → approve
4. Verify: the modified version was sent, not the original

---

## Part 4: Add Guardrails (20 min) : Cursor ON

Use Cursor to add these safety features:

1. **Rate limiting**: The agent should never send more than 5 emails in one run
2. **Duplicate detection**: Before sending, check if this lead was already emailed in the last 24 hours
3. **Content validation**: Before pausing for review, the agent checks that:
   - The email has a subject line
   - The body mentions the lead's name
   - The email doesn't contain placeholder text like "[INSERT NAME]"

---

##  Success Criteria

Your agent works if:
- [ ] It drafts personalized emails (not copy-paste templates)
- [ ] It **pauses** before sending and shows you the drafts
- [ ] You can approve, reject, or edit individual emails
- [ ] Only approved emails get sent
- [ ] Supabase is updated after sending (last_contacted_at)
- [ ] Duplicate protection works

---

##  Reflection Questions

1. What would happen if we **removed** the human-in-the-loop? What's the worst-case scenario?
2. Are there operations in Exercise 02 (lead scoring) that should ALSO have had human review? Why or why not?
3. Where would you draw the line between "auto-approve" and "require human review" in a real business?

---
<div align="center">

# **Perfect!** 

Your agent now generates personalized emails 

**Next challenge**: Agents break in production. Learn to debug, monitor, and rescue them...

**[➤ Lecture 04: Debugging Agents](../00-Lectures/04-Debugging-Agents.md)**

</div>
