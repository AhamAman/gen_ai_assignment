# OpenAI Agents — Managed Tools, Realtime API, and Voice Agents

Mastering this phase means understanding how modern production agents move beyond simple tool calling and become multimodal systems capable of:

* Web search
* File search
* Code execution
* Real-time speech conversations
* Audio streaming
* Voice synthesis
* Voice interruption handling
* Human-like conversational latency

This is the layer that powers systems similar to ChatGPT Voice, customer support voice agents, AI assistants, and real-time copilots.

---

# Table of Contents

1. Managed Tools
2. File Search Tool
3. Web Search Tool
4. Code Interpreter Tool
5. Voice Models
6. Realtime API Architecture
7. Realtime Events
8. Audio Input Pipeline
9. Audio Output Pipeline
10. Building a Voice Agent
11. Streaming Architecture
12. Interruptions and Barge-In
13. Session Management
14. Production Architecture
15. Veteran Questions

---

# Why Managed Tools Exist

Earlier agent architectures required:

```text
Developer
 ↓
Build Search
 ↓
Build Retrieval
 ↓
Build Tool Schemas
 ↓
Build Execution Layer
```

Lots of infrastructure.

Managed tools move this responsibility into the platform.

```text
Agent
 ↓
Managed Tool
 ↓
Platform Handles Complexity
```

Benefits:

* Less code
* Faster development
* Better reliability
* Native integrations
* Built-in security

---

# Managed Tools Overview

Modern OpenAI Agents can use:

```text
Agent
 ↓
--------------------------------
|              |              |
File Search   Web Search   Code Interpreter
```

Each tool is hosted and managed.

---

# File Search Tool

## Problem

LLMs cannot read large document collections directly.

Example:

```text
1000 PDFs

500 Word Docs

2000 Markdown Files
```

Too much context.

---

## Solution

File Search

```text
Documents
     ↓
Chunking
     ↓
Embedding
     ↓
Vector Store
     ↓
Retrieval
     ↓
Agent
```

---

## Mental Model

Instead of:

```text
Give model all files
```

Do:

```text
Retrieve relevant pieces
```

---

# File Search Workflow

```text
Upload Files
      ↓
Index Files
      ↓
Store Chunks
      ↓
User Query
      ↓
Retrieve Chunks
      ↓
Agent Response
```

---

# Example

User:

```text
What does our refund policy say?
```

Agent:

```text
File Search
      ↓
Retrieve Policy Section
      ↓
Answer User
```

---

# File Search Architecture

```text
User
 ↓
Agent
 ↓
File Search
 ↓
Vector Store
 ↓
Retrieved Chunks
 ↓
Response
```

---

# Web Search Tool

## Problem

Models have knowledge cutoffs.

They don't know:

* Today's news
* Live events
* Current prices
* Current documentation

---

## Solution

Web Search

```text
Question
     ↓
Search Web
     ↓
Retrieve Pages
     ↓
Summarize
     ↓
Answer
```

---

# Example

User:

```text
Latest Python release?
```

Agent:

```text
Web Search
      ↓
Read Results
      ↓
Answer
```

---

# Web Search Architecture

```text
User
 ↓
Agent
 ↓
Web Search
 ↓
Internet
 ↓
Results
 ↓
Agent
```

---

# File Search vs Web Search

| File Search        | Web Search         |
| ------------------ | ------------------ |
| Internal Knowledge | External Knowledge |
| Company Documents  | Public Internet    |
| Controlled Data    | Dynamic Data       |
| Private            | Public             |

---

# Code Interpreter Tool

One of the most powerful managed tools.

---

# Problem

LLMs are poor calculators.

Bad at:

```text
Large Math

Data Analysis

CSV Processing

Complex Statistics
```

---

# Solution

Run Real Code

```text
Agent
 ↓
Python Sandbox
 ↓
Execution
 ↓
Results
```

---

# Example

User:

```text
Analyze this CSV
```

Agent:

```text
Load CSV
 ↓
Run Python
 ↓
Generate Statistics
 ↓
Return Charts
```

---

# Code Interpreter Architecture

```text
User
 ↓
Agent
 ↓
Code Interpreter
 ↓
Python Environment
 ↓
Output
 ↓
Agent
```

---

# Why It's Powerful

Can:

* Execute Python
* Read files
* Generate charts
* Process spreadsheets
* Analyze data
* Perform calculations

---

# Voice Models

Traditional chat:

```text
Text In
 ↓
Text Out
```

Voice agents require:

```text
Audio In
 ↓
Understanding
 ↓
Reasoning
 ↓
Audio Out
```

---

# Realtime API

The Realtime API is designed for low-latency conversations.

Goal:

```text
Human-like Conversation
```

Instead of:

```text
Record Audio
 ↓
Upload
 ↓
Wait
 ↓
Receive Text
 ↓
Generate Audio
```

Realtime streams continuously.

---

# Realtime Architecture

```text
Microphone
 ↓
Audio Stream
 ↓
Realtime API
 ↓
Model
 ↓
Audio Stream
 ↓
Speaker
```

---

# Traditional Pipeline

```text
Speech
 ↓
STT
 ↓
Text
 ↓
LLM
 ↓
Text
 ↓
TTS
 ↓
Audio
```

Multiple systems.

High latency.

---

# Realtime Pipeline

```text
Speech
 ↓
Realtime Model
 ↓
Speech
```

Single integrated system.

Much faster.

---

# Realtime Session

A session represents an active conversation.

```text
Client
 ↓
WebSocket
 ↓
Realtime Session
 ↓
Model
```

State persists.

---

# Core Realtime Events

Everything is event driven.

---

## User Audio

```text
input_audio_buffer.append
```

Add microphone data.

---

## Commit Audio

```text
input_audio_buffer.commit
```

Signal:

```text
User finished speaking
```

---

## Generate Response

```text
response.create
```

Model begins responding.

---

## Audio Output

```text
response.audio.delta
```

Stream audio back.

---

# Audio Input Pipeline

Voice agent receives:

```text
Microphone
 ↓
PCM Audio
 ↓
Chunking
 ↓
Streaming
 ↓
Realtime API
```

---

# Example

```text
Mic
 ↓
20ms Audio
 ↓
20ms Audio
 ↓
20ms Audio
 ↓
Send Continuously
```

---

# Why Streaming?

Without streaming:

```text
Wait For User
 ↓
Upload Everything
```

High latency.

Streaming starts processing immediately.

---

# Audio Output Pipeline

```text
Model
 ↓
Audio Chunks
 ↓
Client
 ↓
Speaker
```

---

Example:

```text
Audio Delta 1

Audio Delta 2

Audio Delta 3
```

Played instantly.

---

# Building a Voice Agent

High-Level Flow:

```text
User Speaks
      ↓
Audio Stream
      ↓
Realtime Session
      ↓
Agent
      ↓
Tool Calls
      ↓
Response
      ↓
Audio Stream
```

---

# Voice Agent With Tools

Example:

User:

```text
What's the weather?
```

Agent:

```text
Hear Question
      ↓
Web Search Tool
      ↓
Get Weather
      ↓
Generate Speech
      ↓
Stream Voice
```

---

# Realtime Agent Architecture

```text
Mic
 ↓
Realtime API
 ↓
Agent
 ↓
----------------------
|         |          |
Search   Files    Code
Tools    Tools    Tools
 ↓
Response
 ↓
Audio Output
```

---

# Handling Interruptions (Barge-In)

Humans interrupt.

Agents must support it.

---

Example

Agent:

```text
The weather today—
```

User:

```text
Actually what about tomorrow?
```

Agent must stop speaking.

---

# Barge-In Flow

```text
Agent Speaking
      ↓
User Starts Talking
      ↓
Cancel Response
      ↓
Listen
      ↓
Respond To New Input
```

---

# Session State

Keep:

```python
session = {
    "conversation": [],
    "tool_calls": [],
    "user_preferences": {},
    "active_context": {}
}
```

---

# Voice Agent Memory

Remember:

```text
Name

Preferences

Previous Questions

Current Task
```

Across turns.

---

# Production Architecture

```text
User
 ↓
Microphone
 ↓
WebSocket
 ↓
Realtime API
 ↓
Agent
 ↓
--------------------------------
|              |              |
Web Search   File Search   Code Interpreter
 ↓
Response
 ↓
Audio Stream
 ↓
Speaker
```

---

# Latency Optimization

Target:

```text
< 500ms perceived latency
```

Techniques:

* Streaming input
* Streaming output
* Incremental generation
* Fast tool execution
* Context compression

---

# Reliability

Handle:

* Network drops
* Tool failures
* Session expiration
* Audio corruption

Recovery:

```text
Reconnect
 ↓
Restore Session
 ↓
Continue Conversation
```

---

# Security

Protect:

* Uploaded documents
* Voice recordings
* Tool access
* Session history

Use:

* Authentication
* Authorization
* Encrypted transport
* Access controls

---

# Cost Optimization

Voice systems are expensive.

Monitor:

```text
Audio Minutes

Tool Calls

Tokens

Search Requests
```

Optimize:

* Cache results
* Compress context
* Reduce unnecessary tool calls

---

# Common Mistakes

## Mistake

Treating voice like text.

### Fix

Design for streaming.

---

## Mistake

Ignoring interruptions.

### Fix

Implement barge-in handling.

---

## Mistake

Sending full audio recordings.

### Fix

Stream continuously.

---

## Mistake

No session management.

### Fix

Persistent conversation state.

---

## Mistake

Tool calls block speech.

### Fix

Stream partial responses while tools execute.

---

# Veteran Questions

* Why is streaming critical for voice UX?
* How does a realtime model differ from STT + LLM + TTS?
* When should voice agents call tools?
* How do you handle overlapping speech?
* How do you implement interruption recovery?
* How do you maintain state across long conversations?
* How do you reduce latency below 500ms?
* How do you scale thousands of concurrent voice sessions?
* How do you monitor voice quality in production?
* How would you build a customer-support voice agent architecture?

---

# Final Mental Model

```text
Realtime Voice Agent

=
Audio Input
+
Streaming
+
Realtime Model
+
Managed Tools
+
Session Memory
+
Tool Calling
+
Audio Output
+
Interrupt Handling
```

Modern voice agents are no longer:

```text
Speech → Text → LLM → Speech
```

They are continuous real-time systems that perceive, reason, use tools, and speak while the conversation is still happening.
