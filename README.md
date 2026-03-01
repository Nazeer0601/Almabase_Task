# AI-Powered Structured Questionnaire Answering Tool

## 📌 Overview

This project is an AI-powered system that automates answering structured questionnaires (such as security reviews, compliance forms, and vendor assessments) using reference documents as the source of truth.

The application allows users to upload questionnaires and reference documents, automatically generates answers using a Retrieval-Augmented Generation (RAG) pipeline, provides citations, and exports the completed document.

This project was developed as part of the Almabase GTM Engineering Internship assignment.

---

## 🏢 Fictional Company & Industry

### Industry
SaaS (Cloud-based Security Platform)

### Fictional Company
**SecureCloud Systems** is a cloud-based SaaS platform that provides secure data storage, identity management, and compliance solutions for enterprise clients. The company follows industry-standard security practices, encryption mechanisms, and compliance frameworks.

---

## 🎯 Features

### Core Features (Assignment Requirements)

- User authentication (Signup/Login)
- Upload structured questionnaire (PDF)
- Upload reference documents (PDF)
- Question parsing from uploaded document
- Retrieval-Augmented Generation (RAG) pipeline
- AI-generated answers using reference documents
- Citations for each generated answer
- "Not found in references" handling
- Structured review interface
- Edit answers before export
- Export completed questionnaire as document
- Persistent data storage using SQLite database

---

### Additional Features (Nice to Have Implemented)

- Confidence score for generated answers
- Evidence snippets from reference documents
- Coverage summary:
  - Total questions
  - Answered questions
  - Missing answers

---

## ⚙️ System Architecture

### Frontend
- HTML
- CSS
- JavaScript
- Flask Templates

### Backend
- Python
- Flask

### Database
- SQLite (persistent storage)

### AI Pipeline
- Sentence Transformers for embeddings
- Vector retrieval for context selection
- Retrieval-Augmented Generation (RAG)

---

## 🔄 Application Workflow

1. User signs up and logs in.
2. Uploads reference documents.
3. Uploads questionnaire document.
4. System extracts questions from the questionnaire.
5. Relevant content is retrieved from reference documents.
6. AI generates answers with citations.
7. User reviews and edits answers.
8. System exports completed questionnaire.

---

## 🧠 AI Approach

The system uses a Retrieval-Augmented Generation (RAG) pipeline:

- Reference documents are chunked and indexed.
- Semantic search retrieves relevant context.
- AI generates answers based only on retrieved evidence.
- If no relevant context exists → "Not found in references" is returned.

This ensures grounded and reliable outputs.

---

## ⚠️ Assumptions Made

- Input questionnaires follow a structured format.
- Reference documents contain relevant supporting information.
- PDFs contain extractable text.
- Simple UI prioritizes functionality over design.

---

## ⚖️ Trade-offs

- Basic UI for faster development.
- SQLite used instead of production-scale database.
- Simple PDF parsing without OCR support.
- Lightweight RAG implementation for demonstration purposes.

---

## 🚀 Future Improvements

- OCR support for scanned PDFs
- Better UI/UX design
- Role-based access control
- Version history tracking
- Improved answer validation
- Production-grade deployment configuration
- Document format support beyond PDF

---

## 💻 Local Setup Instructions

### Clone Repository
