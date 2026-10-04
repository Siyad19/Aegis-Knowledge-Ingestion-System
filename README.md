# Aegis Knowledge Ingestion System

This project builds a knowledge base from Aegis Series-7 HCS technical documents and uses it to answer questions with supporting evidence.

The main focus is on **extracting useful information from different documents, keeping track of where the information came from, and avoiding guesses when the data is unclear or missing.**

## Architecture

```text
Documents
   ↓
Document Processing
   ↓
Text Extraction / OCR
   ↓
Chunking
   ↓
LLM Knowledge Extraction
   ↓
Knowledge Base
   ↓
Hybrid Retrieval
   ↓
Relevant Evidence
   ↓
LLM Answer
```
## Project Goal

The goal of this project is to build a knowledge system that can read different Aegis technical documents, extract structured information with its source, retrieve relevant information for a question, and generate an answer based only on the available evidence.

The system should also handle conflicts, uncertainty, and missing information instead of guessing.

## How it works

### 1. Document Processing

The project works with different types of files such as:

* PDF
* HTML
* DOCX
* XLSX
* JSON
* Images
* PPTX

The documents are converted into a common text-based format. OCR is used where required for scanned documents and images.

### 2. Knowledge Extraction

The documents are split into smaller chunks and sent to the LLM.

The system extracts:

* **Entities** – components, sensors, alarms, etc.
* **Claims** – factual information such as pressure values.
* **Requirements** – things that must be done or checked.
* **Relationships** – connections between components.

### 3. Provenance

For every extracted piece of information, the system tries to keep its source.

For example:

```text
Filename: operator_manual.pdf
Page: 1
Source: Before starting, verify...
```

This makes it possible to show evidence along with the final answer.

### 4. Retrieval

When a question is asked, the system searches the knowledge base using a combination of:

* Keyword search
* Exact matching
* Vector similarity

The retrieval layer also gives more importance to requirements or warnings when the question is asking about something that **must** or **must not** be done.

### 5. Answer Generation

The retrieved information is given to the LLM.

The LLM is instructed to answer only from the available evidence.

The response contains:

```json
{
  "answer": "...",
  "evidence": [],
  "conflicts": [],
  "uncertainty": [],
  "gaps": []
}
```

If the available information is not enough, the system should report the gap instead of making up an answer.

## Example

**Question:**

> What must be true before starting the Hydraulic Power Unit?

**Answer:**

Before starting the HPU:

* Emergency stop circuit must be RESET.
* Isolation valve IV-21 must be OPEN.
* Hydraulic fluid level must be within the normal range.

The answer is supported by the retrieved document evidence.

## Project Structure

```text
Aegis-Knowledge-Ingestion/
│
├── prompts/
│   ├── knowledge_extraction_prompt.py
│   └── answer_question_prompt.py
│
├── processed/
│   ├── documents/
│   └── knowledge/
│
├── llm/
│   └── model.py
│
├── src/
│   │
│   ├── ingest/
│   │   ├── pdf_loader.py
│   │   ├── html_loader.py
│   │   ├── docx_loader.py
│   │   ├── xlsx_loader.py
│   │   ├── pptx_loader.py
│   │   ├── image_loader.py
│   │   ├── json_loader.py
│   │   └── ingestion_pipeline.py
│   │
│   ├── knowledge/
│   │   ├── knowledge_extraction.py
│   │   └── chunk_knowledge_extraction.py
│   │
│   ├── retrieval/
│   │   └── retriever.py
│   │
│   └── answering/
│       └── answer_question.py
│
├── app.py
├── ingest.py
├── build_knowledge.py
├── evaluate.py
├── requirements.txt
├── .env
└── README.md
```


## Implementation Steps

### 1. `ingestion.py` — Document Ingestion

**Goal:** Read all the different source files and convert them into a common format.

Steps:

1. Read documents from the dataset folders.
2. Identify the file type such as PDF, HTML, DOCX, XLSX, JSON, PPTX, or image.
3. Extract text from each document.
4. Use OCR for scanned/image-based documents when required.
5. Keep basic metadata such as filename, document ID, page number, and source location.
6. Save the processed documents in a normalized format as JSON file.

```text
Raw Documents
     ↓
Read Files
     ↓
Text / OCR Extraction
     ↓
Add Metadata
     ↓
Normalized Documents
```

`Important`: The provided dataset has already been processed using the ingestion step.

You do not need to run ingestion.py again unless you add new documents or want to re-process the existing source files.

---

### 2. `build_knowledge.py` — Knowledge Building

**Goal:** Convert the processed documents into structured knowledge.

Steps:

1. Load the normalized documents.
2. Split large documents into smaller chunks.
3. Send each chunk to the LLM.
4. Extract:

   * Entities
   * Claims
   * Requirements
   * Relationships
   * Warnings
5. Attach the original source and location to every extracted item.
6. Store all extracted information in the knowledge base.

```text
Normalized Documents
        ↓
      Chunking
        ↓
       LLM
        ↓
Knowledge Extraction
        ↓
Entities / Claims / Requirements
Relationships / Warnings
        ↓
Knowledge Base
```
`Important`: The knowledge base has already been built for the provided dataset.

You do not need to run build_knowledge.py again unless:

You add new documents.
You re-run the ingestion process.
You want to rebuild the knowledge base.

For newly added documents, run:

python build_knowledge.py

---

### 3. `retriever.py` — Evidence Retrieval

**Goal:** Find the most relevant knowledge for a user's question.

Steps:

1. Take the user's question.
2. Identify the type of question, such as a requirement or warning query.
3. Search the knowledge base using:

   * Exact matching
   * Keyword matching
   * Vector similarity
4. Give higher priority to knowledge types that match the question.
5. Rank the retrieved results.
6. Return the most relevant evidence with its provenance.

```text
User Question
      ↓
Query Intent
      ↓
Hybrid Search
      ↓
Rank Results
      ↓
Relevant Evidence
```

---

### 4. `app.py` — User Interface

**Goal:** Provide a simple interface for asking questions and viewing the grounded answer.

Steps:

1. Start the application.
2. Accept a natural-language question from the user.
3. Send the question to the retrieval layer.
4. Pass the retrieved evidence to the answer-generation layer.
5. Generate the final answer.
6. Display:

   * Answer
   * Supporting evidence
   * Source/provenance
   * Conflicts
   * Uncertainty
   * Information gaps

```text
User
 ↓
Question
 ↓
Retriever
 ↓
Evidence
 ↓
Answer Generator
 ↓
Answer + Sources
```

Run the application with:

streamlit run app.py

---


The four main components therefore have clear responsibilities:

| File                 | Main Responsibility                           |
| -------------------- | --------------------------------------------- |
| `ingestion.py`       | Read and normalize source documents           |
| `build_knowledge.py` | Extract and build structured knowledge        |
| `retriever.py`       | Find relevant evidence                        |
| `app.py`             | Accept questions and display grounded answers |


## Main Technologies

* Python
* LangChain
* LLM / Groq
* Vector Search
* OCR
* JSON

## Key Idea

The main idea of the project is:

> **Don't just give the documents to an LLM and ask questions. First build a structured knowledge layer with provenance, then retrieve the relevant evidence and generate the answer from that evidence.**

This helps the system handle technical documents, source references, conflicting information, and missing information more reliably.

## 🛠️ Installation Guide

### 1. Clone the repository

```bash
git clone https://github.com/Siyad19/Aegis-Knowledge-Ingestion-System.git
cd <project-folder>
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

### 4. Install the required packages

```bash
pip install -r requirements.txt
```

### 5. Configure the environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_api_key
```

Replace `your_api_key` with your Groq API key.

### 6. Run the application

The document ingestion and knowledge-building steps have already been completed for the provided dataset.

So, for normal usage, you only need to start the application:

```bash
streamlit run app.py
```

The application will use the existing knowledge base to retrieve evidence and answer questions.

### Adding New Documents

If you add new documents to the dataset, run the ingestion and knowledge-building steps again before starting the application:

```bash
python ingestion.py
python build_knowledge.py
streamlit run app.py
```

After adding new documents, the knowledge base needs to be rebuilt so the new information can be retrieved by the application.

