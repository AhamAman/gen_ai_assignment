# Agentic Workflows — Core Concepts Mastery Guide

Mastering Agentic Workflows means understanding how LLMs evolve from simple prompt-response systems into autonomous systems capable of reasoning, planning, using tools, recovering from failures, and operating safely in production environments.

---

# Table of Contents

1. Chain vs Agent
2. Perceive → Decide → Act Loop
3. Tools and JSON Schemas
4. Sequential Tool Calls
5. Parallel Tool Calls
6. Guardrails
7. Safe Tool Evaluation
8. Retries
9. Error Recovery
10. Preventing Infinite Loops
11. Runaway Agent Prevention
12. Production Architecture
13. Veteran Questions

---

# 1. Chain vs Agent

The most fundamental distinction in Agentic AI.

---

## Chain

A chain follows a predetermined workflow.

```text
User Query
     ↓
Retrieve Documents
     ↓
Summarize
     ↓
Generate Answer
     ↓
Return
```

The LLM does not decide what happens next.

The developer defines the flow.

### Example

```python
def chain(user_query):
    docs = retrieve(user_query)
    summary = summarize(docs)
    answer = generate(summary)

    return answer
```

Execution path is fixed:

```text
A → B → C → D
```

### Characteristics

* Deterministic
* Predictable
* Cheap
* Easy to debug
* Limited flexibility

### Typical Use Cases

* RAG Pipelines
* ETL Workflows
* Report Generation
* Data Processing
* Document Summarization

---

## Agent

An agent decides dynamically.

It chooses:

* Whether to use tools
* Which tool to use
* How many tools to use
* When to stop

### Example Flow

```text
User Question
      ↓
Agent Thinks
      ↓
Need Information?
      ↓
Tool Call
      ↓
Observe Result
      ↓
Think Again
      ↓
Finish
```

### Example

```python
while True:

    observation = gather_context()

    decision = llm(observation)

    if decision.action == "finish":
        return decision.answer

    result = execute_tool(decision.tool)

    observation.append(result)
```

### Characteristics

* Dynamic
* Flexible
* Non-deterministic
* More expensive
* Harder to debug

---

# Chain vs Agent Summary

| Chain                | Agent             |
| -------------------- | ----------------- |
| Fixed Workflow       | Dynamic Workflow  |
| Deterministic        | Non-deterministic |
| Fast                 | Slower            |
| Cheap                | Expensive         |
| Easy Debugging       | Hard Debugging    |
| Developer Controlled | Model Controlled  |

---

# 2. Perceive → Decide → Act Loop

The core architecture of every agent.

```text
Observe
   ↓
Reason
   ↓
Decide
   ↓
Act
   ↓
Observe New State
   ↓
Repeat
```

---

## Perceive

Gather information from:

* User input
* Memory
* Databases
* Previous tool outputs
* External APIs

Example:

```python
observation = {
    "user": query,
    "history": messages,
    "tool_results": tool_outputs
}
```

---

## Decide

The model reasons.

Questions include:

```text
What do I know?

What am I missing?

Should I call a tool?

Should I stop?
```

Example:

```python
decision = llm(observation)
```

---

## Act

Execute the selected action.

```python
tool_result = execute_tool(decision.tool)
```

Examples:

* Search
* Database Query
* Calculator
* Weather API
* Email Sender

---

## Loop

Tool results become new observations.

```python
while not finished:

    observe()

    decide()

    act()
```

---

# 3. Tools and JSON Schemas

Tools should expose a machine-readable contract.

---

## Example Tool Definition

```json
{
  "name": "get_weather",
  "description": "Get weather for a city",
  "parameters": {
    "type": "object",
    "properties": {
      "city": {
        "type": "string"
      }
    },
    "required": ["city"]
  }
}
```

---

## Model Output

```json
{
  "tool": "get_weather",
  "arguments": {
    "city": "Pune"
  }
}
```

---

## Execution

```python
weather("Pune")
```

---

## Result

```json
{
  "temperature": 34,
  "condition": "Sunny"
}
```

---

## Why JSON Schema?

* Validation
* Safety
* Type checking
* Structured execution
* Tool interoperability

---

# 4. Sequential Tool Calls

One tool depends on the previous tool.

---

## Example

```text
Search Customer
      ↓
Get Customer ID
      ↓
Get Orders
      ↓
Generate Report
```

---

## Code

```python
customer = search_customer()

orders = get_orders(customer.id)

report = generate_report(orders)
```

---

## Dependency Graph

```text
A
↓
B
↓
C
```

Cannot parallelize.

---

# 5. Parallel Tool Calls

Independent tasks executed simultaneously.

---

## Example

Need:

* Weather
* News
* Stock Price

No dependency exists.

---

## Sequential

```python
weather()

news()

stocks()
```

Runtime:

```text
1s + 1s + 1s = 3s
```

---

## Parallel

```python
await asyncio.gather(
    weather(),
    news(),
    stocks()
)
```

Runtime:

```text
~1 second
```

---

## Graph

```text
        Agent
          |
    ------|------
    |     |     |
 Weather News Stocks
```

---

# Parallel vs Sequential

| Sequential         | Parallel     |
| ------------------ | ------------ |
| Dependencies Exist | Independent  |
| Slower             | Faster       |
| Ordered            | Concurrent   |
| Simpler            | More Complex |

---

# 6. Guardrails

Guardrails keep agents safe.

---

## Input Guardrails

Validate user requests.

```text
User Input
     ↓
Safety Check
     ↓
Agent
```

Examples:

* Prompt injection detection
* PII detection
* Jailbreak prevention

---

## Output Guardrails

Validate model outputs.

```python
answer = llm()

validate(answer)
```

Examples:

* JSON validation
* Content moderation
* Policy checks

---

## Tool Guardrails

Validate tool execution.

Example:

```python
if tool == "transfer_money":
    require_human_approval()
```

---

# 7. Safe Tool Evaluation

Never trust tool calls generated by the model.

---

## Tool Whitelist

```python
ALLOWED_TOOLS = {
    "search",
    "calculator",
    "weather"
}

if tool_name not in ALLOWED_TOOLS:
    reject()
```

---

## Parameter Validation

Bad:

```json
{
  "amount": -1000000
}
```

Reject invalid inputs.

---

## Validation Libraries

* Pydantic
* JSON Schema
* Zod
* Marshmallow

---

# 8. Retries

External systems fail.

Examples:

* Timeouts
* Rate limits
* Temporary outages

---

## Retry Pattern

```python
for attempt in range(3):

    try:
        return tool()

    except:
        continue
```

---

## Exponential Backoff

```text
1 second

2 seconds

4 seconds

8 seconds
```

Avoid overwhelming services.

---

# 9. Error Recovery

Agents should recover intelligently.

---

## Recovery Flow

```text
Failure
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

## Example

Search API fails.

Agent can:

1. Retry
2. Use backup search
3. Ask user for clarification
4. Stop gracefully

---

# 10. Preventing Infinite Loops

One of the most common production failures.

---

## Bad Loop

```text
Search
 ↓
Search
 ↓
Search
 ↓
Search
 ↓
Forever
```

---

## Why It Happens

Agent keeps thinking:

```text
I need more information.
```

---

## Solution: Max Iterations

```python
MAX_STEPS = 10

for step in range(MAX_STEPS):

    run_agent_step()

raise AgentStopped()
```

---

## Solution: Duplicate Detection

Track previous actions.

```python
if action == previous_action:
    stop()
```

---

# 11. Runaway Agent Prevention

Runaway agents waste tokens and money.

---

## Time Budget

```python
MAX_RUNTIME = 60
```

Stop after one minute.

---

## Cost Budget

```python
MAX_TOKENS = 100000
```

Stop if exceeded.

---

## Tool Budget

```python
MAX_TOOL_CALLS = 20
```

Limit external actions.

---

## Recursion Depth

```python
MAX_DEPTH = 5
```

Prevent nested-agent explosions.

---

# 12. Production Architecture

A real-world agent system.

```text
User
 ↓
API Gateway
 ↓
Agent Orchestrator
 ↓
Planner
 ↓
Tool Router
 ↓
Tool Layer
 ├── Search
 ├── Database
 ├── APIs
 └── Internal Systems
 ↓
Memory Layer
 ↓
Observability
 ↓
Final Response
```

---

# Production Requirements

## Monitoring

Track:

* Latency
* Tool calls
* Failures
* Costs
* Token usage

---

## Reliability

* Retries
* Circuit breakers
* Fallback tools
* Timeouts

---

## Security

* Tool whitelists
* Permission systems
* Secret management
* Audit logs

---

## Cost Controls

* Token budgets
* Tool budgets
* Early stopping
* Caching

---

# Veteran Questions

## Chain vs Agent

* Why should this be an agent instead of a workflow?
* What decision is the model actually making?

---

## Tool Design

* Can this tool be abused?
* How should parameters be validated?
* What permissions are required?

---

## Reliability

* What happens if every tool fails?
* What happens if the model hallucinates tool arguments?

---

## Architecture

* When should planning be separated from execution?
* When should multiple agents collaborate?
* When does an agent become too autonomous?

---

## Production

* How do we measure agent success?
* How do we prevent cost explosions?
* How do we safely deploy self-improving agents?

---

# Final Mental Model

```text
Observe
   ↓
Reason
   ↓
Decide
   ↓
Act
   ↓
Validate
   ↓
Recover
   ↓
Repeat
   ↓
Stop
```

A production-grade agent is not merely an LLM with tools.

It is a controlled system with:

* Planning
* Tooling
* Validation
* Recovery
* Monitoring
* Security
* Cost Controls
* Loop Prevention

That combination is what transforms a chatbot into a reliable autonomous system.
