# Exercise 06 : New Power: The Calendar Agent

> **Duration**: 2h  
> **Difficulty**: ⭐⭐⭐ (but you have the skills now!)  
> **What you'll build**: A new agent from scratch, plugged into your orchestrator.  
> **Mode**:  Full Cursor, you've earned it.

---

## The Problem

Alex: *"The follow-up emails are great, but I keep proposing meetings without checking my calendar. Last week I double-booked myself twice. Can my assistant check my availability before suggesting times?"*

**Your mission**: Build a calendar agent and plug it into the orchestrator. No hand-holding this time, you know the patterns. Apply everything you've learned.

---

## What You're Proving

This exercise is the **autonomy test**. You'll:
1. Design a new tool from scratch
2. Integrate it into the existing architecture
3. Make decisions about permissions and safety
4. Use Cursor confidently because you understand the output

If you can do this independently, you understand agent architecture.

---

## The Spec

### Option A: Real Calendar API (Cal.com or Google Calendar)

Use [Cal.com's API](https://cal.com/docs/api) (free tier available) or Google Calendar API:

**Tool 1: `check_availability`**
- Input: A date range (start, end)
- Output: List of available time slots
- Permission:  Read, auto-approve

**Tool 2: `propose_meeting`**  
- Input: Lead email, proposed time, meeting title
- Output: Meeting link/confirmation
- Permission:  Write (external), requires Alex's approval

### Option B: Mock Calendar (Simpler)

Create a mock calendar with fake data:

```python
MOCK_CALENDAR = {
    "2024-01-15": [
        {"time": "09:00-10:00", "event": "Team standup"},
        {"time": "14:00-15:30", "event": "Client call - DataFlow"},
    ],
    "2024-01-16": [
        {"time": "10:00-11:00", "event": "Dentist"},
    ],
    # Add more days...
}
```

Same tools, same logic, no API setup required.

---

## Your Tasks

### Task 1: Build the Calendar Agent (45 min)

Using the patterns from Day 1:

1. Create the tool(s) in a new file `calendar_tools.py`
2. Write clear descriptions (the orchestrator will read them!)
3. Add appropriate permission levels:
   - Reading availability = auto
   - Booking a meeting = requires confirmation
4. Add error handling (what if the API is down? what if no slots are available?)

**Use Cursor freely.** But before accepting any suggestion, ask yourself:
- Does this tool description accurately reflect what it does?
- Is there input validation?
- Is error handling present?

### Task 2: Plug Into the Orchestrator (30 min)

1. Import your new tool(s)
2. Add them to the orchestrator's toolkit
3. Update the orchestrator's system prompt to know about the calendar capability:

```
- check_availability: Checks Alex's calendar for free time slots
- propose_meeting: Suggests a meeting time to a lead (requires approval)

WORKFLOW RULE: When drafting follow-up emails, if the email suggests 
a meeting, ALWAYS check availability first. Never propose a time 
without checking.
```

### Task 3: Test the Enhanced Pipeline (30 min)

Test these scenarios:

**Scenario A: Simple availability check**
```
"Am I free tomorrow afternoon?"
```

**Scenario B: Smart email drafting**
```
"Draft a follow-up to Sarah Chen and suggest a call this week"
```
Expected: The agent should check availability BEFORE drafting the email, so it can include real available times.

**Scenario C: Full pipeline with calendar**
```
"Find my stale hot leads and propose meetings with each of them"
```
Expected: find → score → check calendar → draft emails with proposed times → pause for approval.

### Task 4: Reflect on the Architecture (15 min)

Answer these questions in a comment at the top of your code:

1. How many lines of your orchestrator code did you change to add the calendar feature? (It should be very few, mostly tool imports and prompt updates.)
2. What if Alex wanted to add a CRM note-taking agent next? How long would it take you?
3. What's the maximum number of agents you could reasonably plug into this orchestrator before it becomes hard to manage?

---

##  Success Criteria

- [ ] Calendar tool works independently (can check availability)
- [ ] Orchestrator correctly uses the calendar tool when relevant
- [ ] Email drafts include real available times (not made-up ones)
- [ ] Meeting proposals require human approval
- [ ] You added this feature without modifying existing agent code (only orchestrator config)

---

##  Bonus Challenge

If you finish early, add a **5th tool**: a meeting notes summarizer.

After a meeting, Alex pastes his notes and the agent:
1. Extracts action items
2. Updates the lead in Supabase (notes, next steps)
3. Schedules the next follow-up

This is a real-world workflow that shows how agents become genuinely useful.

---

---

**Next up**: Let's deploy this to production
**[➤ Lecture 07: Going-Live](../00-Lectures/07-Deployment.md)**

