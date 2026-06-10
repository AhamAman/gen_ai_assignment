# Claude API 101 — Advanced Claude-Specific Primitives

This phase focuses on the capabilities that made Claude popular among engineers building document intelligence systems, coding assistants, research systems, and enterprise AI applications.

Unlike many introductory LLM guides, this document focuses on the unique primitives Claude introduced or popularized:

* Massive context windows
* Native document understanding
* PDF ingestion
* Inline citations
* Prompt caching
* Extended thinking
* Structured outputs
* Tool usage
* Message batching
* Manual prompt orchestration

These features dramatically affect architecture, cost, latency, and product design.

---

# Table of Contents

1. Long Context Windows
2. Why Long Context Works
3. Native PDF Understanding
4. Inline Citations
5. Prompt Caching
6. Prompt Cache Internals
7. Measuring Cache Savings
8. Manual Prompt Chaining
9. Extended Thinking
10. Structured Outputs
11. Structured Tool Use
12. Message Batches
13. Large Scale Processing
14. Architecture Patterns
15. Veteran Questions

---

# Long Context Windows

One of Claude's most famous features.

---

## Traditional LLM Problem

Earlier models:

```text id="j3pc9z"
Document
   ↓
Chunk
   ↓
Embed
   ↓
Retrieve
   ↓
LLM
```

Everything required chunking.

---

## Claude Approach

Large context enables:

```text id="mh98g7"
Entire Document
       ↓
Claude
```

or

```text id="w2hh4u"
Entire Codebase
       ↓
Claude
```

or

```text id="7k2rq8"
Many Documents
       ↓
Claude
```

---

# Why This Matters

Traditional RAG:

```text id="g4qu5j"
Chunk A

Chunk B

Chunk C
```

Model only sees fragments.

---

Claude:

```text id="9jclw7"
Whole Document
```

Allows reasoning across:

* Chapters
* Sections
* Tables
* References
* Cross-document relationships

---

# What Makes Long Context Possible?

Many beginners think:

```text id="wpy8v5"
Just increase token limit
```

Not enough.

---

# Attention Problem

Transformers use attention.

Basic attention cost:

O(n^2)

---

As context grows:

```text id="d8qv1x"
10k tokens

100k tokens

200k tokens
```

Computation explodes.

---

# Long Context Innovations

Modern systems use:

```text id="fyjdxz"
Attention Optimizations

Memory Optimizations

Sparse Attention

KV Cache Improvements

Training Strategies
```

to make large windows practical.

---

# Architectural Impact

Traditional:

```text id="tm4px4"
Docs
 ↓
Chunk
 ↓
Retrieve
 ↓
Answer
```

Claude:

```text id="o9pr0h"
Docs
 ↓
Direct Reasoning
```

Fewer moving pieces.

---

# Native PDF Understanding

One of Claude's most useful capabilities.

---

# Traditional PDF Pipeline

Old approach:

```text id="jfc24r"
PDF
 ↓
OCR
 ↓
Extract Text
 ↓
Cleanup
 ↓
LLM
```

Many failure points.

---

# Claude Approach

```text id="v7g0y4"
PDF
 ↓
Claude
```

Send document directly.

---

# Why This Matters

PDFs contain:

```text id="c8bx8x"
Tables

Charts

Headers

Footnotes

Formatting
```

Raw text extraction often loses this structure.

---

# Native Document Workflow

```text id="zywqot"
PDF Upload
      ↓
Claude
      ↓
Document Understanding
      ↓
Answer
```

---

# Example Use Cases

* Contracts
* Research papers
* Financial reports
* SEC filings
* Technical manuals

---

# Inline Citations

A major feature for enterprise and research systems.

---

# Problem

Normal LLM:

```text id="g58x5f"
Answer

But where did it come from?
```

Unknown.

---

# Claude Citation Flow

```text id="aev1d6"
Document
 ↓
Question
 ↓
Answer
 ↓
Citation References
```

---

# Example

```text id="7s8ej8"
Revenue increased by 18%.

Source:
Page 14
Paragraph 3
```

---

# Why Important?

Enterprise users ask:

```text id="7bpbpz"
Show me proof.
```

Citations provide traceability.

---

# Architecture

```text id="6rwdhf"
Document
 ↓
Model
 ↓
Answer
 +
Source Locations
```

---

# Prompt Caching

One of Claude's most valuable production features.

---

# Problem

Many prompts repeat.

Example:

```text id="49uc8m"
100-page handbook

same system prompt

same instructions
```

Repeated every request.

Expensive.

---

# Without Caching

Request 1:

```text id="g4rr1a"
System Prompt
+
Documents
+
Question
```

Request 2:

```text id="jkwx85"
System Prompt
+
Documents
+
Question
```

Pay repeatedly.

---

# With Caching

First request:

```text id="jh4g6x"
Store Prefix
```

Later requests:

```text id="ypk4zs"
Reuse Cached Prefix
```

Only process new tokens.

---

# Cache Architecture

```text id="m2a6vt"
Prompt
 ├── Cached Prefix
 └── Dynamic Suffix
```

---

Example

```text id="l91p3w"
System Prompt
Large Document
```

cached

while

```text id="v7f50t"
User Question
```

changes.

---

# Prompt Cache Internals

Think of:

```text id="dnjg7u"
Prompt
```

as

```text id="2i5i93"
Static Region

+

Dynamic Region
```

---

Static:

```text id="7llpkv"
Instructions

Knowledge Base

Policies
```

---

Dynamic:

```text id="wph60x"
Current User Query
```

---

# Measuring Cost Savings

Suppose:

```text id="3x7iqq"
100,000 token document
```

Question:

```text id="st7z6f"
What does section 3 say?
```

Without cache:

```text id="rygr7v"
100k tokens every request
```

---

10 requests:

```text id="4qxk17"
1,000,000 tokens processed
```

---

With cache:

```text id="hf0pd4"
100k once

+

small query each request
```

Massive savings.

---

# Manual Prompt Chaining

Sometimes better than agents.

---

# Pattern

```text id="a4zmjl"
Prompt A
 ↓
Output
 ↓
Prompt B
 ↓
Output
 ↓
Prompt C
```

---

# Example

Research Workflow

```text id="2f5htk"
Summarize
 ↓
Extract Insights
 ↓
Generate Report
```

---

# Why Use It?

Advantages:

```text id="u85kn8"
Predictable

Cheap

Debuggable
```

Compared to agents.

---

# Extended Thinking

Claude provides reasoning-focused modes.

---

# Standard Generation

```text id="l16cy4"
Question
 ↓
Answer
```

---

# Extended Thinking

```text id="dphbrs"
Question
 ↓
Reason Longer
 ↓
Answer
```

---

# When To Use

Good:

* Complex reasoning
* Research
* Planning
* Math
* Multi-step decisions

---

Bad:

* Simple chat
* FAQs
* Classification
* Extraction

---

# Tradeoff

| Normal  | Extended Thinking |
| ------- | ----------------- |
| Faster  | Slower            |
| Cheaper | More Expensive    |
| Simpler | Better Reasoning  |

---

# Structured Outputs

Production systems should not parse text.

---

Bad:

```text id="0sqxhn"
Name: John

Age: 30
```

Fragile.

---

Good:

```json id="0cfqko"
{
  "name": "John",
  "age": 30
}
```

---

# Output Schema

Define:

```json id="uxyljf"
{
  "type":"object",
  "properties":{
    "name":{"type":"string"},
    "age":{"type":"integer"}
  }
}
```

---

Benefits:

* Validation
* Reliability
* Automation

---

# Structured Tool Use

Tools should be schema-driven.

---

Example

```json id="3wdttd"
{
  "tool":"weather",
  "arguments":{
    "city":"Pune"
  }
}
```

---

# Tool Execution Flow

```text id="5e6v24"
Agent
 ↓
Tool Schema
 ↓
Tool Call
 ↓
Validation
 ↓
Execution
```

---

# Message Batches

Useful for bulk processing.

---

# Problem

Need to process:

```text id="v10zlr"
10,000 documents
```

Sending individually:

```text id="4jq9hc"
10,000 API Calls
```

Inefficient.

---

# Batch Architecture

```text id="q3p0r6"
Documents
      ↓
Batch Request
      ↓
Processing Queue
      ↓
Results
```

---

# Example Use Cases

* Classification
* Summarization
* Extraction
* Sentiment Analysis
* Large document pipelines

---

# Batch Benefits

```text id="vl2lui"
Higher Throughput

Lower Overhead

Better Cost Efficiency
```

---

# Enterprise Architecture

```text id="4vz9b5"
Documents
 ↓
Claude
 ↓
-------------------------
|           |           |

Caching   Citations   Structured Output
```

---

# Claude Design Philosophy

Claude historically focused heavily on:

```text id="9hslc6"
Documents

Reasoning

Long Context

Enterprise Workflows

Reliable Outputs
```

rather than purely chatbot interactions.

---

# Common Mistakes

---

## Mistake

Chunking everything automatically.

### Fix

Try long-context reasoning first.

---

## Mistake

Ignoring prompt caching.

### Fix

Cache static context.

---

## Mistake

Using extended thinking everywhere.

### Fix

Use only when reasoning complexity justifies it.

---

## Mistake

Parsing text outputs.

### Fix

Use schemas.

---

## Mistake

Building agents unnecessarily.

### Fix

Use prompt chains when possible.

---

# Veteran Questions

* When does long context outperform RAG?
* When does RAG outperform long context?
* How should cache boundaries be designed?
* What prompt regions should never be cached?
* How do citations improve enterprise trust?
* When should prompt chaining replace agents?
* How do you measure cache ROI?
* How do long-context models handle attention efficiently?
* What workflows benefit most from message batching?
* How would you design a 1-million-document processing pipeline?

---

# Final Mental Model

```text id="v6j5oz"
Claude Enterprise Workflow

=
Long Context
+
Document Understanding
+
Native PDFs
+
Citations
+
Prompt Caching
+
Structured Outputs
+
Tool Usage
+
Batch Processing
+
Reasoning Modes
```

The biggest architectural lesson is:

```text id="a0l89o"
Before building RAG,
before building agents,
before building orchestration,

ask:

Can the model simply reason over the entire context directly?
```

Many Claude-powered systems became dramatically simpler because the answer was often **yes**.
