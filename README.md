# Just a RAG — V1

A small **Retrieval-Augmented Generation (RAG)** project built from scratch for learning.

The goal of this project is to understand how RAG works internally by building each part step by step instead of jumping directly into a framework.

## What is RAG?

**RAG (Retrieval-Augmented Generation)** is a technique where an AI system retrieves relevant information from a collection of documents and then gives that information to an LLM to generate an answer.

Instead of asking an LLM:

```text
"Answer this question using what you know."
```

we do:

```text
User Question
      ↓
Search our documents
      ↓
Find relevant information
      ↓
Give the information to the LLM
      ↓
Generate an answer
```

This allows the AI to answer questions using **our own data**.

---

## V1 Goal

The first version of this project is intentionally simple.

We are starting with:

* `.txt` documents
* Python
* Basic file loading
* Document chunking
* Embeddings
* Vector similarity search
* Simple retrieval

Later, an LLM will be added to generate answers from the retrieved information.

---

## Project Structure

```text
simple-rag/
│
├── documents/
│   ├── python.txt
│   ├── rag.txt
│   └── ai.txt
│
├── main.py
├── requirements.txt
└── README.md
```

### `documents/`

Contains the knowledge that our RAG system will use.

For example:

```text
documents/
├── python.txt
├── machine_learning.txt
└── rag.txt
```

---

## Loading Documents

The first step is reading our documents into Python.

Example:

```python
from pathlib import Path

DOCUMENTS_PATH = Path("documents")


def load_documents():
    documents = []

    for fp in DOCUMENTS_PATH.glob("*.txt"):
        text = fp.read_text(encoding="utf-8")

        documents.append({
            "filename": fp.name,
            "text": text
        })

    return documents
```

If we have:

```text
documents/python.txt
```

the function converts it into something like:

```python
{
    "filename": "python.txt",
    "text": "Python is a programming language..."
}
```

All documents are then stored in a list:

```python
[
    {
        "filename": "python.txt",
        "text": "..."
    },
    {
        "filename": "rag.txt",
        "text": "..."
    }
]
```

---

## Why Are We Doing This?

An LLM cannot automatically know the contents of our private documents.

We therefore need a pipeline that takes our documents and makes them searchable.

The complete system will eventually look like:

```text
              DOCUMENT INGESTION
                     │
                     ▼
              Load Documents
                     │
                     ▼
              Split into Chunks
                     │
                     ▼
                Create Embeddings
                     │
                     ▼
              Store in Vector DB
                     │
                     │
                     ▼
              USER QUESTION
                     │
                     ▼
            Create Query Embedding
                     │
                     ▼
              Similarity Search
                     │
                     ▼
             Relevant Chunks
                     │
                     ▼
                   LLM
                     │
                     ▼
               Final Answer
```

---

## Learning Roadmap

This project will be developed incrementally.

### V1.1 — Load Documents

Read `.txt` files from the `documents/` directory.

```text
TXT files
   ↓
Python list
```

### V1.2 — Chunk Documents

Large documents need to be divided into smaller pieces.

```text
Document
   ↓
Chunk 1
Chunk 2
Chunk 3
...
```

### V1.3 — Create Embeddings

Convert each chunk into a numerical vector.

```text
"Python is a programming language."
             ↓
       [0.12, -0.43, 0.82, ...]
```

The vector represents the **meaning** of the text.

### V1.4 — Similarity Search

When the user asks a question, we convert the question into an embedding and find the chunks with the most similar vectors.

```text
Question
   ↓
Embedding
   ↓
Similarity Search
   ↓
Top relevant chunks
```

### V1.5 — Add an LLM

Finally, provide the retrieved chunks to an LLM:

```text
Question
   +
Relevant Documents
   ↓
LLM
   ↓
Answer
```

---

## The Main Idea

The most important concept to understand is:

> **RAG separates knowledge retrieval from answer generation.**

The vector search system answers:

```text
"What information is relevant?"
```

The LLM answers:

```text
"How should I explain that information?"
```

---

## Current Status

**Version:** V1 — Document Loading

Currently implemented:

* [x] Project structure
* [x] Documents directory
* [x] `.txt` document discovery
* [x] Reading documents
* [x] Storing filename + text
* [x] Document chunking
* [x] LLM generation

Coming next:

* [ ] Embeddings
* [ ] Vector search
* [ ] Retrieval
* [ ] Complete RAG pipeline

---

## Running the Project

Make sure Python is installed.

Then run:

```bash
python main.py
```

The program will read all `.txt` files inside:

```text
documents/
```

and print their contents.

---

## Why Build This From Scratch?

The purpose of this project is **learning**.

Instead of immediately using a large RAG framework, we are building the fundamental pieces ourselves so that we understand:

* What a document is
* What a chunk is
* What an embedding is
* How vector similarity works
* How retrieval works
* How retrieved context is passed to an LLM
* How the complete RAG pipeline fits together

Once the fundamentals are understood, frameworks such as LangChain or LlamaIndex become much easier to understand.

---

## Final Architecture

The final simple RAG will look approximately like this:

```text
                    ┌──────────────┐
                    │  Documents   │
                    │   (.txt)     │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │   Chunking   │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  Embeddings  │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │ Vector Store │
                    └──────┬───────┘
                           │
                           │
                     User Question
                           │
                           ▼
                    ┌──────────────┐
                    │   Retrieval  │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │ Relevant     │
                    │   Chunks     │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │     LLM      │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │    Answer    │
                    └──────────────┘
```

This repository is primarily a **learning project for understanding RAG fundamentals**.
