# Claude Skills Mastery Guide

Skills are one of the most powerful abstractions emerging in agent ecosystems.

Most developers initially build:

```text
Prompts

Tools

Agents
```

Eventually they discover a problem:

```text
Same workflows
Repeated everywhere
```

Examples:

```text
Code Review

Architecture Review

PR Analysis

Bug Investigation

RAG Evaluation

Security Audit
```

The logic gets copied repeatedly.

Skills solve this.

---

# Table of Contents

1. Why Skills Exist
2. What Is A Skill
3. Skills vs Prompts
4. Skills vs Tools
5. Skills vs Agents
6. Skill Architecture
7. Skill Components
8. Input Contracts
9. Output Contracts
10. Skill Composition
11. Skill Packaging
12. Skill Distribution
13. Skill Marketplaces
14. Enterprise Skills
15. Production Architecture
16. Veteran Questions

---

# Why Skills Exist

Imagine building:

```text
Code Review Agent

PR Review Agent

Security Agent

Refactoring Agent
```

Every one contains:

```text
Code Analysis

Best Practices

Review Logic
```

Repeated.

---

# Problem

Without skills:

```text
Prompt
 ↓
Copy
 ↓
Paste
 ↓
Modify
 ↓
Repeat
```

Knowledge fragments.

---

# Solution

Encapsulate capability.

```text
Skill
=
Reusable Expertise
```

---

# What Is A Skill?

A skill is:

```text
Instructions
+
Knowledge
+
Workflow
+
Input Contract
+
Output Contract
```

packaged into a reusable unit.

---

# Mental Model

Tool

```text
Can Do Something
```

Example:

```text
Read File
```

---

Skill

```text
Knows How To Solve Something
```

Example:

```text
Perform Senior Code Review
```

---

# Human Analogy

Tool:

```text
Hammer
```

---

Skill:

```text
Carpentry
```

---

# Skills vs Prompts

Prompt:

```text
One-time instruction
```

---

Skill:

```text
Reusable capability
```

---

Prompt

```text
Review this code.
```

---

Skill

```text
Code Review Specialist
```

usable everywhere.

---

# Skills vs Tools

Tool

```text
Action
```

Example:

```text
Search GitHub
```

---

Skill

```text
Expertise
```

Example:

```text
Analyze GitHub Repository
```

which may use multiple tools.

---

# Skills vs Agents

Agent

```text
Decision Maker
```

---

Skill

```text
Capability Module
```

---

Architecture

```text
Agent
 ↓
Uses Skills
 ↓
Uses Tools
```

---

# Skill Architecture

High-level:

```text
Input
 ↓
Skill
 ↓
Output
```

Internally:

```text
Input
 ↓
Instructions
 ↓
Knowledge
 ↓
Workflow
 ↓
Output
```

---

# Components of a Skill

Every production skill should contain:

```text
Name

Description

Instructions

Input Schema

Output Schema

Examples

Constraints
```

---

# Example Skill

## Name

```text
Architecture Reviewer
```

---

## Purpose

Review system design documents.

---

## Inputs

```text
Architecture Document
```

---

## Outputs

```text
Findings

Risks

Recommendations
```

---

# Input Contracts

Most important concept.

---

Bad

```text
Give me something.
```

---

Good

```json
{
  "architecture_document": "..."
}
```

Explicit.

---

# Why Input Contracts Matter

Benefits:

```text
Validation

Predictability

Automation

Reuse
```

---

# Output Contracts

Skills should return structured outputs.

---

Bad

```text
Large wall of text
```

---

Good

```json
{
  "strengths": [],
  "risks": [],
  "recommendations": []
}
```

---

Benefits:

```text
Machine Readable

Composable

Reliable
```

---

# Skill Execution Flow

```text
Input
 ↓
Validate
 ↓
Execute Skill
 ↓
Generate Output
 ↓
Validate Output
```

---

# Skill Composition

Skills can call other skills.

---

Example

```text
Architecture Skill
      ↓
------------------
|                |

Security      Scalability
Skill         Skill
```

---

Architecture

```text
Master Skill
 ↓
Sub Skills
 ↓
Combined Result
```

---

# Example

System Design Review

Uses:

```text
Architecture Review

Security Review

Performance Review

Cost Review
```

Skills.

---

# Skill Packaging

Goal:

```text
Portable Capability
```

---

Skill Package

```text
skill/
│
├── skill.yaml
├── instructions.md
├── examples/
├── schemas/
└── assets/
```

---

# Skill Manifest

Contains:

```text
Name

Version

Description

Inputs

Outputs
```

---

Example

```yaml
name: code-review

version: 1.0.0

description: Senior engineering review skill
```

---

# Versioning Skills

Treat skills like software.

---

Example

```text
v1.0

v1.1

v2.0
```

---

Allows:

```text
Improvements

Compatibility

Rollback
```

---

# Distributing Skills

Once packaged:

```text
Developer
 ↓
Publish Skill
 ↓
Community
```

---

# Distribution Models

---

## Internal

Enterprise only.

```text
Company Skills
```

---

Examples:

```text
Security Review

Compliance Review

Legal Review
```

---

## Public

Community usage.

Examples:

```text
Code Review Skill

RAG Evaluation Skill

Architecture Review Skill
```

---

# Skill Registry

Equivalent of:

```text
npm

PyPI

Docker Hub
```

for AI capabilities.

---

Architecture

```text
Skill Author
      ↓
Registry
      ↓
Consumers
```

---

# Skill Discovery

Agent asks:

```text
What skills are available?
```

Registry returns:

```text
Architecture Reviewer

PR Reviewer

Security Auditor

Research Analyst
```

---

# AI Ecosystem Vision

Future:

```text
Agents
 ↓
Install Skills
 ↓
Gain Capabilities
```

Just like:

```text
Developers
 ↓
Install Packages
 ↓
Gain Features
```

---

# Enterprise Skill Architecture

```text
Agent
 ↓
---------------------------------
|               |              |

Code Skill   Security Skill  Compliance Skill
```

Shared across company.

---

Benefits:

```text
Consistency

Reuse

Governance

Quality
```

---

# Skill Lifecycle

```text
Create
 ↓
Package
 ↓
Test
 ↓
Publish
 ↓
Install
 ↓
Use
 ↓
Update
```

---

# Testing Skills

Skills should be evaluated.

---

Input:

```text
Known Example
```

Expected:

```text
Known Output
```

---

Track:

```text
Accuracy

Consistency

Latency

Cost
```

---

# Production Architecture

```text
User
 ↓
Agent
 ↓
Skill Registry
 ↓
Selected Skill
 ↓
Tools
 ↓
Output
```

---

# Skills + MCP

Powerful combination.

---

Architecture

```text
Skill
 ↓
Uses MCP Tools
 ↓
External Systems
```

---

Example

```text
GitHub Review Skill
```

Uses:

```text
GitHub MCP Server
```

---

# Skills + Agents

Agent becomes orchestrator.

---

Architecture

```text
Agent
 ↓
Choose Skill
 ↓
Execute Skill
 ↓
Return Result
```

---

Instead of:

```text
Agent
 ↓
Solve Everything
```

---

# Common Mistakes

---

## Mistake

Treating prompts as skills.

### Fix

Add contracts and structure.

---

## Mistake

Huge monolithic skills.

### Fix

Small focused capabilities.

---

## Mistake

No schemas.

### Fix

Explicit inputs and outputs.

---

## Mistake

No versioning.

### Fix

Semantic versions.

---

## Mistake

Duplicated skills.

### Fix

Central skill registry.

---

# Veteran Questions

* When should something be a tool versus a skill?
* When should a skill become an agent?
* How should skills be versioned?
* How should skills be evaluated?
* How do enterprises govern skills?
* How should skill dependencies work?
* How do skills compose together?
* How should skills be distributed publicly?
* How would you build an npm for AI skills?
* How would you design a company-wide skill ecosystem?

---

# Final Mental Model

```text
Tools
=
Actions

Skills
=
Expertise

Agents
=
Decision Makers
```

Architecture:

```text
User
 ↓
Agent
 ↓
Skill
 ↓
Tools
 ↓
Result
```

The biggest lesson:

```text
Prompts are reusable text.

Skills are reusable intelligence.
```

Just as software engineering evolved from scripts to reusable packages, Agentic AI is evolving from prompts to reusable skills that can be shared, installed, versioned, and distributed across the AI ecosystem.
