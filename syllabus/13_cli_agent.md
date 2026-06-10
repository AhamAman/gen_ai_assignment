# CLI Agent From Scratch

Building a Claude Code Style Terminal Agent

---

# What We Are Building

A coding agent that can:

* Read files
* Write files
* Edit files
* Search directories
* Execute shell commands
* Observe results
* Decide next actions
* Repeat until task completion

Examples:

```text
User:
Fix the failing tests

Agent:
→ Read project structure
→ Find test files
→ Run tests
→ Observe failures
→ Edit code
→ Run tests again
→ Verify success
→ Finish
```

This is essentially how modern coding agents operate.

---

# High-Level Architecture

```text
User
 ↓
CLI Interface
 ↓
Agent Loop
 ↓
LLM
 ↓
Tool Selection
 ↓
Tool Execution
 ↓
Observation
 ↓
LLM
 ↓
Tool Selection
 ↓
...
```

---

# Core Mental Model

A coding agent is simply:

```text
Think
 ↓
Act
 ↓
Observe
 ↓
Think Again
```

Repeated until completion.

---

# Minimal Folder Structure

```text
agent/
│
├── main.py
├── agent.py
├── tools/
│   ├── read_file.py
│   ├── write_file.py
│   ├── list_dir.py
│   └── shell.py
│
├── prompts/
│   └── system_prompt.txt
│
└── memory/
```

---

# Core Agent Loop

Everything revolves around this.

```python
while True:

    observation = gather_context()

    response = llm(observation)

    if response.action == "finish":
        break

    result = execute_tool(response)

    observation.append(result)
```

This loop is the heart of Claude Code, Cursor Agent, OpenAI Codex, and most coding agents.

---

# Agent State

The agent needs memory.

```python
state = {
    "goal": user_request,
    "history": [],
    "tool_results": [],
    "working_directory": "."
}
```

---

# Tool System

Every tool follows:

```python
tool(input)
    ↓
execute
    ↓
return output
```

Example:

```python
read_file("main.py")
```

Returns:

```python
{
    "content": "..."
}
```

---

# Tool Registry

```python
TOOLS = {
    "read_file": read_file,
    "write_file": write_file,
    "list_dir": list_dir,
    "shell": shell
}
```

---

# File Read Tool

## Purpose

Read source files.

---

## Implementation

```python
def read_file(path):

    with open(path, "r") as f:
        return f.read()
```

---

## Tool Schema

```json
{
  "name": "read_file",
  "parameters": {
    "type": "object",
    "properties": {
      "path": {
        "type": "string"
      }
    },
    "required": ["path"]
  }
}
```

---

# File Write Tool

## Purpose

Create or overwrite files.

---

## Implementation

```python
def write_file(path, content):

    with open(path, "w") as f:
        f.write(content)

    return "success"
```

---

# Directory Listing Tool

## Purpose

Explore project structure.

---

## Implementation

```python
import os

def list_dir(path="."):

    return os.listdir(path)
```

---

## Example

```text
src/
tests/
README.md
requirements.txt
```

---

# Recursive Directory Tree

Very useful for coding agents.

```python
import os

def tree(path):

    for root, dirs, files in os.walk(path):
        ...
```

---

## Example Output

```text
project/
├── src/
│   ├── app.py
│   └── db.py
│
├── tests/
│   └── test_app.py
│
└── README.md
```

---

# Shell Execution Tool

Most powerful tool.

Allows:

```text
pytest

npm test

git status

pip install

docker build
```

---

## Implementation

```python
import subprocess

def shell(command):

    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )

    return {
        "stdout": result.stdout,
        "stderr": result.stderr,
        "code": result.returncode
    }
```

---

# Example Agent Flow

User:

```text
Run tests and fix failures
```

Agent:

```text
list_dir()
```

Observes:

```text
tests/
src/
```

Agent:

```text
shell("pytest")
```

Observes:

```text
FAILED test_login
```

Agent:

```text
read_file("src/login.py")
```

Observes code.

Agent:

```text
write_file(...)
```

Edits code.

Agent:

```text
shell("pytest")
```

Observes:

```text
All tests passed
```

Agent:

```text
finish()
```

Done.

---

# Tool Calling Format

LLM outputs structured actions.

Example:

```json
{
  "tool": "read_file",
  "arguments": {
    "path": "main.py"
  }
}
```

Executor:

```python
tool = response["tool"]

args = response["arguments"]

TOOLS[tool](**args)
```

---

# Claude Code Style Architecture

Claude Code is essentially:

```text
User
 ↓
Planner
 ↓
Tool Router
 ↓
Filesystem
 ↓
Shell
 ↓
Git
 ↓
Editor
 ↓
LLM
```

---

# Planner Pattern

Separate thinking from execution.

```text
Goal
 ↓
Create Plan
 ↓
Execute Plan
 ↓
Verify
 ↓
Finish
```

---

Example Plan

```text
1. Inspect repository

2. Run tests

3. Identify failures

4. Fix code

5. Re-run tests

6. Verify success
```

---

# Observation Compression

Large projects create huge outputs.

Bad:

```text
100000 token directory tree
```

Good:

```text
Summarize results
```

Example:

```python
tree_summary = llm(tree_output)
```

---

# Context Window Management

Critical for coding agents.

Keep:

```text
Goal

Current files

Recent edits

Tool outputs
```

Drop:

```text
Old irrelevant outputs
```

---

# Diff-Based Editing

Instead of rewriting entire files.

Bad:

```text
Write entire 2000-line file
```

Good:

```text
Replace lines 42-50
```

---

Example

```text
--- old
+++ new

- return False
+ return True
```

---

# Safety Controls

Never trust the model.

---

## Allowed Commands

Whitelist.

```python
SAFE_COMMANDS = [
    "pytest",
    "ls",
    "cat",
    "git status"
]
```

---

## Dangerous Commands

Block.

```text
rm -rf /

shutdown

reboot

mkfs

chmod -R 777
```

---

# Tool Permissions

Example:

```python
ALLOW_WRITE = True

ALLOW_SHELL = False
```

User approval required.

---

# Retry System

Tool failures happen.

```python
for attempt in range(3):

    try:
        return tool()

    except:
        continue
```

---

# Error Recovery

```text
Tool Failed
     ↓
Retry
     ↓
Alternative Tool
     ↓
Ask User
     ↓
Abort
```

---

# Prevent Infinite Loops

Very important.

---

## Step Limit

```python
MAX_STEPS = 20
```

---

## Tool Call Limit

```python
MAX_TOOL_CALLS = 50
```

---

## Time Limit

```python
MAX_RUNTIME = 300
```

---

# Runaway Agent Prevention

Track:

```python
cost

token_usage

tool_calls

runtime
```

Stop if limits exceeded.

---

# Production Architecture

```text
User
 ↓
CLI
 ↓
Agent Loop
 ↓
Planner
 ↓
LLM
 ↓
Tool Router
 ↓
Filesystem Tools
 ↓
Shell Tools
 ↓
Git Tools
 ↓
Memory
 ↓
Observability
```

---

# Advanced Claude Code Features

## Multi-Step Planning

```text
Goal
 ↓
Subtasks
 ↓
Execute
 ↓
Verify
```

---

## Reflection

Agent critiques itself.

```text
Did the fix actually work?

Did tests pass?

Did I break something else?
```

---

## Verification Pass

```text
Run tests

Run linter

Run formatter

Check git diff
```

Before finishing.

---

# Veteran Questions

* Why should an agent call a shell instead of editing directly?
* How should filesystem access be sandboxed?
* How can prompt injection occur through source code files?
* When should planning be separate from execution?
* How do coding agents manage context windows?
* How do agents safely edit 100,000-line repositories?
* How do agents recover from incorrect plans?
* How do Claude Code and Cursor reduce token costs?
* How would you build a multi-agent coding system?
* How would you build a Git-aware autonomous software engineer?

---

# Final Mental Model

```text
User Goal
    ↓
Plan
    ↓
Observe
    ↓
Think
    ↓
Tool Call
    ↓
Observe
    ↓
Think
    ↓
Edit
    ↓
Verify
    ↓
Finish
```

A Claude Code–style agent is fundamentally:

```text
LLM
+
Filesystem
+
Shell
+
Planning
+
Verification
+
Safety Controls
```

wrapped inside a continuous Observe → Think → Act loop.

