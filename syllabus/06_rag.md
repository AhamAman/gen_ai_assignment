# 📚 RAG (Retrieval Augmented Generation) Mastery Checklist

> From Basic RAG → Enterprise Knowledge Systems → Production AI Search Platforms

Master document ingestion, parsing, chunking, embeddings, indexing, retrieval, reranking, context construction, evaluation, and production-grade RAG architectures.

---

# 📚 Table of Contents

```text
Part 0  : Why RAG Exists
Part 1  : Complete RAG Architecture
Part 2  : RAG Lifecycle
Part 3  : Document Ingestion
Part 4  : Document Parsing
Part 5  : Chunking Fundamentals
Part 6  : Fixed Size Chunking
Part 7  : Recursive Chunking
Part 8  : Semantic Chunking
Part 9  : Agentic Chunking
Part 10 : Chunking Strategy Selection
Part 11 : Embedding Fundamentals
Part 12 : Embedding Model Selection
Part 13 : Indexing Pipeline Design
Part 14 : Vector Databases
Part 15 : Metadata Design
Part 16 : Query Pipeline Design
Part 17 : Retrieval Strategies
Part 18 : Hybrid Search
Part 19 : Reranking
Part 20 : Context Construction
Part 21 : RAG Prompt Engineering
Part 22 : RAG Evaluation
Part 23 : RAG Optimization
Part 24 : Advanced RAG Architectures
Part 25 : Production RAG Systems
Part 26 : Real Projects
Part 27 : Senior RAG Engineer Mastery
```

---

# Part 0 — Why RAG Exists

## Problem

LLMs have:

```text
Knowledge Cutoff
Hallucinations
No Access To Private Data
```

---

## Example

Question:

```text
What does our company handbook say about PTO?
```

LLM cannot know.

---

## Solution

```text
Question
 ↓
Retrieve Documents
 ↓
Inject Context
 ↓
LLM Answers
```

---

## First Principles

RAG =

```text
Retrieval
+
Generation
```

---

# Part 1 — Complete RAG Architecture

```text
Documents
      ↓
Parsing
      ↓
Chunking
      ↓
Embeddings
      ↓
Vector DB
==================
User Question
      ↓
Embedding
      ↓
Retrieval
      ↓
Reranking
      ↓
Context Building
      ↓
LLM
      ↓
Answer
```

---

# Part 2 — RAG Lifecycle

## Two Pipelines

### Indexing Pipeline

Runs once.

### Query Pipeline

Runs per request.

---

## Understand

```text
Indexing Cost
≠
Query Cost
```

---

# Part 3 — Document Ingestion

## Sources

### PDFs

### Word Documents

### Markdown

### HTML

### Wikis

### Databases

### APIs

### Notion

### Confluence

---

## Exercises

* [ ] Build ingestion pipeline

---

# Part 4 — Document Parsing

## PDF Parsing

Challenges:

```text
Headers
Footers
Tables
Images
Columns
OCR
```

---

## Tools

### PyMuPDF

### PDFPlumber

### Unstructured

### Docling

### LlamaParse

---

## Markdown Parsing

Preserve:

```text
Headings
Lists
Code Blocks
```

---

## HTML Parsing

Preserve:

```text
Title
Sections
Hierarchy
```

---

## Exercises

* [ ] Parse PDF
* [ ] Parse Markdown
* [ ] Parse HTML

---

## Veteran Questions

* Why is document parsing often harder than retrieval?

---

# Part 5 — Chunking Fundamentals

## Why Chunk?

Cannot embed:

```text
Entire Document
```

---

Need:

```text
Document
 ↓
Chunks
```

---

## Goals

* Preserve Meaning
* Improve Retrieval
* Fit Context Window

---

# Part 6 — Fixed Size Chunking

## Method

```text
Every 500 Tokens
```

Example:

```text
Chunk 1
Chunk 2
Chunk 3
```

---

## Pros

* Simple
* Fast

---

## Cons

* Breaks Context
* Breaks Sentences

---

## Use Cases

* Logs
* Large Raw Text

---

## Exercises

* [ ] Compare chunk sizes

---

# Part 7 — Recursive Chunking

## Strategy

Split by:

```text
Paragraph
 ↓
Sentence
 ↓
Words
```

Until chunk size reached.

---

## Benefits

Preserves structure.

---

## Most Common

Production default.

---

## Exercises

* [ ] Build recursive splitter

---

# Part 8 — Semantic Chunking

## Idea

Split based on meaning.

---

## Example

Keep:

```text
Entire Topic
```

together.

---

## Process

```text
Sentence Embeddings
 ↓
Similarity
 ↓
Boundary Detection
```

---

## Benefits

Better retrieval.

---

## Costs

Slower indexing.

---

## Exercises

* [ ] Compare semantic vs recursive

---

# Part 9 — Agentic Chunking

## Advanced

LLM decides:

```text
Where To Split
```

---

## Benefits

Highest quality.

---

## Drawbacks

Expensive.

---

# Part 10 — Chunking Strategy Selection

## PDF Knowledge Base

```text
Recursive
```

---

## Research Papers

```text
Semantic
```

---

## Legal Documents

```text
Semantic
+
Metadata
```

---

## Codebases

```text
Structure Aware Chunking
```

---

## Exercises

* [ ] Choose strategy for 5 domains

---

# Part 11 — Embedding Fundamentals

## Purpose

Convert text to vectors.

---

```text
Text
 ↓
Embedding Model
 ↓
Vector
```

---

## Similar Meaning

```text
Nearby Vectors
```

---

# Part 12 — Embedding Model Selection

## Metrics

### Quality

### Speed

### Cost

### Vector Size

---

## Popular Models

### BGE

### E5

### Nomic

### Jina

### GTE

### OpenAI Embeddings

### Gemini Embeddings

---

## Decision Guide

### Local RAG

```text
BGE
Nomic
E5
```

---

### Enterprise RAG

```text
BGE Large
Jina
OpenAI
```

---

## Exercises

* [ ] Benchmark embeddings

---

## Veteran Questions

* Why shouldn't chat models generate embeddings?

---

# Part 13 — Indexing Pipeline Design

## Pipeline

```text
Document
 ↓
Parser
 ↓
Cleaner
 ↓
Chunker
 ↓
Metadata
 ↓
Embeddings
 ↓
Vector DB
```

---

## Metadata

### Source

### Page

### Section

### Author

### Timestamp

---

# Part 14 — Vector Databases

## Local

### FAISS

### Chroma

---

## Production

### Qdrant

### Weaviate

### Pinecone

### Milvus

---

## Exercises

* [ ] Build vector database

---

# Part 15 — Metadata Design

## Store

```text
Document ID
Page
Section
URL
Timestamp
Tags
```

---

## Benefits

Improved filtering.

---

# Part 16 — Query Pipeline Design

## Flow

```text
Question
 ↓
Query Rewrite
 ↓
Embedding
 ↓
Search
 ↓
Rerank
 ↓
Context Build
 ↓
LLM
```

---

# Part 17 — Retrieval Strategies

## Similarity Search

### Cosine Similarity

### Dot Product

---

## MMR

Maximum Marginal Relevance

---

## Multi Query Retrieval

Generate:

```text
Multiple Queries
```

---

## Exercises

* [ ] Compare retrieval strategies

---

# Part 18 — Hybrid Search

## Combine

```text
Keyword Search
+
Vector Search
```

---

## Why?

Vector search misses exact matches.

---

## Tools

### BM25

### Elasticsearch

### OpenSearch

---

## Exercises

* [ ] Build hybrid retrieval

---

# Part 19 — Reranking

## Problem

Top retrieved docs aren't always best.

---

## Solution

Reranker

---

## Examples

### BGE Reranker

### Cohere Rerank

### Cross Encoders

---

## Pipeline

```text
Retrieve 50
 ↓
Rerank
 ↓
Keep Top 5
```

---

## Exercises

* [ ] Add reranking

---

# Part 20 — Context Construction

## Question

How many chunks should be sent?

---

## Context Builder

```text
Top Chunks
+
Metadata
+
Question
```

---

## Ordering Matters

---

# Part 21 — RAG Prompt Engineering

## Prompt Template

```text
Context
Question
Instructions
```

---

## Hallucination Prevention

```text
Answer only from provided context.
```

---

# Part 22 — RAG Evaluation

## Metrics

### Recall

### Precision

### Faithfulness

### Groundedness

### Answer Relevance

---

## Tools

### Ragas

### DeepEval

---

## Exercises

* [ ] Evaluate RAG

---

# Part 23 — RAG Optimization

## Improve

### Parsing

### Chunking

### Embeddings

### Retrieval

### Reranking

---

## Reality

Most gains come before the LLM.

---

# Part 24 — Advanced RAG Architectures

## Parent Child Retrieval

---

## Graph RAG

---

## Agentic RAG

---

## Multi-Hop RAG

---

## Knowledge Graph RAG

---

## Exercises

* [ ] Build GraphRAG prototype

---

# Part 25 — Production RAG Systems

## Components

```text
Parser
Chunker
Embedding Service
Vector DB
Retriever
Reranker
LLM
Monitoring
```

---

## Infrastructure

### Redis

### PostgreSQL

### Qdrant

### FastAPI

---

# Part 26 — Real Projects

## Beginner

* PDF Question Answering
* Company FAQ Bot

---

## Intermediate

* Research Assistant
* Legal Document Search

---

## Advanced

* Enterprise Knowledge Assistant
* Multi-Source RAG Platform
* GraphRAG System

---

# Part 27 — Senior RAG Engineer Mastery

## Can Explain

* Parsing
* Chunking
* Embeddings
* Retrieval
* Reranking
* Evaluation

---

## Can Build

* Production RAG Systems
* Enterprise Search
* Hybrid Search
* Agentic RAG

---

## Can Design

* Knowledge Platforms
* Enterprise AI Search
* Multi-Tenant RAG Systems
* Large Scale Retrieval Infrastructure

---

# Common RAG Mistakes

## Mistake 1

Using fixed chunking everywhere.

Fix:

```text
Choose chunking based on document type.
```

---

## Mistake 2

Ignoring metadata.

Fix:

```text
Metadata-aware retrieval.
```

---

## Mistake 3

No reranking.

Fix:

```text
Retriever + Reranker.
```

---

## Mistake 4

Using chat models as embeddings.

Fix:

```text
Dedicated embedding models.
```

---

## Mistake 5

Optimizing prompts first.

Fix:

```text
Fix retrieval first.
```

---

# Final Mastery Checklist

## Beginner

* [ ] Parse PDFs
* [ ] Chunk documents
* [ ] Generate embeddings
* [ ] Build vector search

## Intermediate

* [ ] Hybrid search
* [ ] Metadata filtering
* [ ] Reranking
* [ ] Evaluation

## Advanced

* [ ] GraphRAG
* [ ] Agentic RAG
* [ ] Multi-hop retrieval

## Expert

* [ ] Enterprise RAG architecture
* [ ] Knowledge platforms
* [ ] Large-scale retrieval systems
* [ ] Retrieval infrastructure design

```
```
