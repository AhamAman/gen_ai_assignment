# Claude Agent SDK Mastery Guide

Building Production Agents with Claude

This phase covers how to move from simple Claude API calls to fully autonomous agents capable of:

* Tool usage
* Multi-turn conversations
* Stateful workflows
* Agent loops
* Tool orchestration
* Long-context reasoning
* Production deployment

The goal is to understand how real Claude-powered agents are built in production.

---

# Table of Contents

1. Why Agent SDKs Exist
2. Claude Agent Architecture
3. SDK Setup
4. Defining Tools
5. Writing Effective System Prompts
6. Single Tool Agent
7. Multi-Tool Agent
8. Full End-to-End Agent
9. Multi-Turn Conversations
10. Conversation Memory
11. Agent Loops
12. Tool Orchestration
13. Model Selection
14. Claude vs OpenAI for Agents
15. Production Architecture
16. Veteran Questions

---

# Why Agent SDKs Exist

Without an SDK:

```text id="i3y0o5"
LLM Calls

Tool Parsing

JSON Validation

Conversation State

Retries

Error Recovery

Agent Loops

Logging
```

must all be built manually.

---

# Traditional Agent

```text id="w6mq1v"
User
 ↓
Custom Loop
 ↓
Claude API
 ↓
Tool Calls
 ↓
State
 ↓
Response
```

Lots of boilerplate.

---

# SDK Approach

```text id="n8iijz"
User
 ↓
Agent
 ↓
Claude SDK
 ↓
Tools
 ↓
Response
```

Framework handles orchestration.

---

# Claude Agent Architecture

A Claude agent consists of:

```text id="0iixuj"
Agent
├── Model
├── System Prompt
├── Tools
├── State
├── Memory
└── Execution Loop
```

---

# Mental Model

Think of an agent as:

```text id="9tx3ln"
Brain
+
Capabilities
+
Memory
+
Instructions
```

---

# SDK Setup

Typical setup:

```bash id="g6bnw6"
pip install anthropic
```

---

Environment:

```bash id="rdh9g8"
ANTHROPIC_API_KEY=...
```

---

# Basic Client

```python id="gux5l7"
from anthropic import Anthropic

client = Anthropic()
```

Everything starts here.

---

# Defining Tools

Tools are capabilities.

Without tools:

```text id="yiczh5"
Claude
 ↓
Text Only
```

With tools:

```text id="v5k81d"
Claude
 ↓
Can Act
```

---

# Example Tool

```python id="0ucx9x"
def get_weather(city):

    return weather_api(city)
```

---

# Tool Schema

```json id="hpn6ek"
{
  "name": "get_weather",
  "description": "Get weather",
  "input_schema": {
    "type": "object",
    "properties": {
      "city": {
        "type": "string"
      }
    }
  }
}
```

---

# Tool Flow

```text id="08wccu"
User
 ↓
Claude
 ↓
Tool Call
 ↓
Tool Result
 ↓
Claude
 ↓
Answer
```

---

# Writing System Prompts

System prompts are the most important part of agent behavior.

---

# Bad Prompt

```text id="6if4uj"
Help the user.
```

Too vague.

---

# Better Prompt

```text id="7wxrqm"
You are a senior software engineer.

Responsibilities:

- Analyze code
- Use tools when necessary
- Verify all assumptions
- Explain reasoning clearly

Never invent tool results.
Always use tools when factual information is required.
```

---

# System Prompt Components

Good prompts define:

```text id="qqyzcw"
Identity

Responsibilities

Constraints

Tool Usage Rules

Output Style

Failure Handling
```

---

# Single Tool Agent

Architecture:

```text id="vbrq4t"
User
 ↓
Claude
 ↓
Weather Tool
 ↓
Response
```

---

Example:

```text id="hjlwm9"
What's weather in Pune?
```

Claude:

```text id="k54p9e"
Need weather tool.
```

Calls tool.

Gets result.

Responds.

---

# Multi-Tool Agent

Most real agents use multiple tools.

---

Architecture:

```text id="4l6mje"
Agent
 ↓
---------------------
|         |         |

Search   Weather   DB
```

---

Examples:

* Search
* Calculator
* Database
* CRM
* File Search

---

# Tool Selection

Claude decides:

```text id="sp8m40"
Do I know this?

Need Tool?

Which Tool?

Need More Tools?

Can I Answer?
```

---

# Full End-to-End Agent

Example:

User:

```text id="gn2a6l"
Find failing tests and fix them
```

---

Flow:

```text id="c6h78u"
Read Files
 ↓
Run Tests
 ↓
Inspect Errors
 ↓
Modify Code
 ↓
Run Tests Again
 ↓
Verify
 ↓
Finish
```

---

Architecture:

```text id="7lr6gv"
User
 ↓
Claude
 ↓
Filesystem Tools
 ↓
Shell Tools
 ↓
Verification
 ↓
Response
```

---

# Multi-Turn Conversations

Agents become useful when they remember context.

---

Without Memory

```text id="ew2myd"
Turn 1

Forgot

Turn 2
```

Bad experience.

---

With Memory

```text id="vsz8zt"
Turn 1
 ↓
Stored
 ↓
Turn 2
 ↓
Context Available
```

---

# Conversation Structure

```python id="rvyrgm"
messages = [

    user,

    assistant,

    user,

    assistant
]
```

Sent every turn.

---

# Multi-Turn Flow

```text id="jtbmnd"
User:
Build API

Assistant:
Creates plan

User:
Add authentication

Assistant:
Uses previous plan
```

Context persists.

---

# Conversation Memory

Memory stores:

```text id="n7pz80"
Goals

Plans

Tool Results

Preferences

Progress
```

---

# Agent Loops

Real agents don't stop after one tool.

---

Architecture:

```text id="i2zl1e"
Observe
 ↓
Think
 ↓
Tool
 ↓
Observe
 ↓
Think
 ↓
Tool
 ↓
Finish
```

---

Pseudo Code

```python id="ofh7jv"
while True:

    response = claude()

    if response.finished:
        break

    execute_tool()
```

---

# Tool Orchestration

Tools often depend on one another.

---

Example

```text id="xf2rkg"
Search Customer
 ↓
Get Customer ID
 ↓
Load Orders
 ↓
Generate Report
```

Sequential.

---

# Parallel Tool Calls

Possible when independent.

```text id="f9nm7u"
Weather

Stocks

News
```

Can execute simultaneously.

---

Architecture

```text id="8zj8yz"
Agent
 ↓
-------------
|     |     |

A     B     C
```

---

# Choosing the Right Claude Model

This is often overlooked.

---

# Fast Tasks

Examples:

```text id="p13ndg"
Classification

Extraction

Tagging

Routing
```

Use smaller models.

---

# General Agents

Examples:

```text id="t9v06r"
Business Automation

Customer Support

Workflows
```

Use balanced models.

---

# Heavy Reasoning

Examples:

```text id="l6l3ke"
Research

Code Analysis

Planning

Long Context
```

Use flagship models.

---

# Model Selection Framework

```text id="7jcl1t"
Cheap
 ↓
Fast
 ↓
Balanced
 ↓
Reasoning Heavy
 ↓
Flagship
```

Match model to task complexity.

---

# Claude Strengths for Agents

Historically strong at:

```text id="mw1ej6"
Long Context

Document Understanding

Code Analysis

Instruction Following

Enterprise Workflows
```

---

# Claude Weaknesses

Potential tradeoffs:

```text id="s6c1zk"
Cost

Latency

Longer Responses
```

Depending on model choice.

---

# Claude vs OpenAI for Agentic Workloads

Important architectural discussion.

---

# Claude Strengths

```text id="h0vxh0"
Huge Context

Document Workflows

PDF Analysis

Long Reasoning Chains

Research Tasks
```

---

# OpenAI Strengths

```text id="smwh1o"
Realtime Voice

Managed Tools

Agent SDK

Multimodal Ecosystem

Production Agent Infrastructure
```

---

# Claude-Oriented Architecture

```text id="l8c1r0"
Large Documents
 ↓
Claude
 ↓
Reasoning
```

Often simpler.

---

# OpenAI-Oriented Architecture

```text id="p8c7r3"
Agent
 ↓
Tools
 ↓
Realtime
 ↓
Voice
 ↓
Multi-Agent
```

Very strong ecosystem.

---

# Practical Guidance

Use Claude when:

```text id="4wz93u"
Documents dominate

Research dominates

Context dominates
```

---

Use OpenAI when:

```text id="r70mxw"
Voice dominates

Realtime matters

Managed tooling matters

Complex agent ecosystems matter
```

---

Many production systems use both.

---

Architecture:

```text id="wn4lk8"
Voice
 ↓
OpenAI

Documents
 ↓
Claude

Application Layer
 ↓
User
```

---

# Production Architecture

```text id="7sv11v"
User
 ↓
API Layer
 ↓
Agent
 ↓
Memory
 ↓
Tool Router
 ↓
-------------------------
|          |            |

Search    Database    Files
```

---

# Reliability

Add:

```text id="uxc2lo"
Retries

Timeouts

Fallbacks

Validation
```

to every tool.

---

# Observability

Track:

```text id="dj8wfx"
Latency

Tokens

Tool Calls

Failures

Costs
```

---

# Common Mistakes

## Mistake

One giant tool.

### Fix

Small focused tools.

---

## Mistake

Weak system prompts.

### Fix

Explicit behavior rules.

---

## Mistake

No memory.

### Fix

Conversation state.

---

## Mistake

Using largest model everywhere.

### Fix

Match model to task.

---

## Mistake

Ignoring tool validation.

### Fix

Schema validation.

---

# Veteran Questions

* When should a tool be a tool versus another agent?
* How much conversation history should be retained?
* When should memory be summarized?
* How should large tool outputs be compressed?
* How do long-context agents compare to RAG systems?
* How should tool permissions be enforced?
* How do you prevent infinite tool loops?
* How do you coordinate multiple specialized agents?
* When should Claude and OpenAI be combined?
* How would you build a production software engineering agent?

---

# Final Mental Model

```text id="r1rqit"
Claude Agent

=
Claude Model
+
System Prompt
+
Tools
+
Conversation Memory
+
Agent Loop
+
Tool Orchestration
+
State Management
```

The biggest lesson:

```text id="bsgmzg"
A good agent is rarely about the model.

It is usually about:

Tool Design
+
Prompt Design
+
Memory Design
+
Workflow Design
```

Those four components determine most of an agent's real-world performance.
