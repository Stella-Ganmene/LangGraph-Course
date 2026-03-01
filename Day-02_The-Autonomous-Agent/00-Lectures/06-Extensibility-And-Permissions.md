# Lecture 06 — Extensibility & The Permission Matrix

> **Duration**: 15 min lecture (delivered before Exercise 06)  
> **Objective**: Understand how to safely add new capabilities to an agent system.

---

## The Extensibility Test

You know your agent architecture is good when you can add a new capability **without rewriting everything**.

Today, Alex wants a new feature: "Before sending a follow-up email, check if I have a meeting slot available this week so I can propose a call."

If your architecture is well-designed, this should require:
1. Creating one new tool (calendar API)
2. Adding it to the orchestrator's toolkit
3. Updating the orchestrator's system prompt to know about it
4. Done.

No graph restructuring. No existing code changes. Just **plug in and go**.

---

## The Permission Matrix

As your agent gains more capabilities, you need a clear framework for **what it's allowed to do automatically vs. what requires approval**.

Here's a model that works:

| Action Type | Permission Level | Example |
|---|---|---|
| **Read** | 🟢 Auto-approve | Query the database, check calendar |
| **Analyze** | 🟢 Auto-approve | Score a lead, summarize data |
| **Generate** | 🟡 Show for review | Draft an email, create a report |
| **Write (internal)** | 🟡 Confirm then execute | Update a lead score in DB |
| **Write (external)** | 🔴 Require explicit approval | Send an email, book a meeting |
| **Delete** | ⛔ Block entirely | Never let an agent delete data autonomously |

**Rule of thumb**: The more **irreversible** an action is, the more **human oversight** it needs.

---

## Why This Matters

Every new tool you add to your agent is a new **surface area for mistakes**. A calendar tool that can only READ your availability is safe. A calendar tool that can BOOK meetings is powerful but risky.

Before adding any tool, ask yourself:
1. What's the **worst thing** that could happen if this tool is misused?
2. Is that outcome **reversible**?
3. Can I add a **confirmation step** for dangerous operations?

This isn't just good engineering — it's how you build AI systems that people **trust**.

---

## Cursor's Role Changes

Notice something: in Exercise 01, we told you to write code by hand. In Exercise 06, you'll use Cursor freely.

Why the shift? Because now you **understand the patterns**. When Cursor suggests a tool definition, you can evaluate:
- "Is the description clear enough?"
- "Does it have proper error handling?"
- "Should this tool have write permissions?"

You've gone from "following Cursor's suggestions" to "directing Cursor's work." That's the real skill.

---

**Now it's your turn** → Exercise 06: Add a New Power
