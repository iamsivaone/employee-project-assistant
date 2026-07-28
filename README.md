# 🤖 Employee Project Assistant

A multi-agent AI assistant designed to help employees query project details, search internal documentation using Retrieval-Augmented Generation (RAG), and manage role-based access control (RBAC) securely.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [System Architecture](#system-architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Environment Variables](#environment-variables)
  - [Option 1: Running with Docker Compose (Recommended)](#option-1-running-with-docker-compose-recommended)
  - [Option 2: Running Locally (Manual Setup)](#option-2-running-locally-manual-setup)
- [Usage Guide](#usage-guide)
  - [Streamlit Interface](#streamlit-interface)
  - [Admin Permission Matrix](#admin-permission-matrix)
  - [Document Ingestion](#document-ingestion)
- [API Reference](#api-reference)
- [Database Schema & Initial Seed](#database-schema--initial-seed)

---

## 🌟 Overview

The **Employee Project Assistant** combines FastAPI, LangChain/LangGraph, PostgreSQL, ChromaDB, and Streamlit into a cohesive enterprise solution. It allows employees to interact naturally with project repositories and documents while ensuring strict runtime authorization checks so user privacy and access control are never bypassed.

---

## ✨ Key Features

- **🤖 Multi-Agent Orchestration**:
  - **Supervisor Agent**: Central router enforcing runtime security and delegating requests to specialized sub-agents.
  - **Project Information Agent**: Queries relational metadata (deadlines, statuses, descriptions).
  - **Document RAG Agent**: Searches semantic embeddings of uploaded PDFs, Word documents, and text files.
- **🔒 Runtime RBAC Authorization**:
  - Every user query triggers a mandatory `check_project_access` tool evaluation before accessing sensitive data or document stores.
- **⚡ Real-Time Streaming UI**:
  - Interactive Streamlit frontend featuring Server-Sent Events (SSE) streaming responses and real-time agent execution inspection windows.
- **📄 Multi-Format Ingestion**:
  - Supports uploading `.pdf`, `.docx`, and `.txt` files into ChromaDB for vector retrieval.
- **🛡️ Admin Access Control Dashboard**:
  - Live access toggle matrix for project administrators to update employee permissions dynamically.

---

## 🏗️ System Architecture

```mermaid
graph TD
    User([👤 User / Browser]) <--> Streamlit[🖥️ Streamlit Frontend :8502]
    Streamlit <--> API[🚀 FastAPI Backend :8001]
    
    subgraph Multi-Agent System
        API --> Supervisor[🤖 Supervisor Agent]
        Supervisor -->|1. Enforce RBAC| AccessTool[🔒 Access Check Tool]
        AccessTool <--> Postgres[(🐘 PostgreSQL Database)]
        
        Supervisor -->|2. Query Metadata| ProjectAgent[📊 Project Info Agent]
        ProjectAgent <--> Postgres
        
        Supervisor -->|3. Query Docs| RAGAgent[📚 RAG Document Agent]
        RAGAgent <--> Chroma[(🔍 ChromaDB Vector Store)]
    end
```

---

## 🛠️ Tech Stack

- **Framework & Core**: Python 3.12+, FastAPI, Uvicorn
- **AI & Orchestration**: LangChain, LangGraph, Google Gemini API / Groq
- **Database & Vector Search**: PostgreSQL 16 (Relational Store), ChromaDB (Vector Store)
- **Document Parsing**: PyPDF, `python-docx`
- **Frontend**: Streamlit
- **Environment & Package Management**: `uv`, Docker, Docker Compose

---

## 📁 Project Structure

```text
employee-assistant/
├── app/
│   ├── agents/            # Multi-agent implementations (Supervisor, RAG, Project)
│   ├── api/               # FastAPI route handlers (chat, access, admin, upload, etc.)
│   ├── database/          # Database connection setup, models, and seeding scripts
│   ├── models/            # Pydantic schemas and data models
│   ├── prompts/           # System prompts for agents
│   ├── repositories/      # Data access layer for DB operations
│   ├── services/          # LLM initialization and core business logic
│   ├── tools/             # Agent tools (access check, document retrieval, project DB tools)
│   └── main.py            # FastAPI entry point
├── database/              # SQL initialization scripts
├── uploads/               # Staging folder for uploaded documents
├── chroma_db/             # Local persistent Chroma vector store
├── docker-compose.yml     # Multi-container service setup
├── Dockerfile             # Container definition
├── pyproject.toml         # Project dependencies and metadata
├── requirements.txt       # Alternative dependency lock file
└── streamlit_app.py       # Streamlit user interface
```

---

## 🚀 Getting Started

### Prerequisites

- **Docker & Docker Compose** (Recommended) or **Python 3.12+** & **`uv`**
- Google Gemini API Key (`GOOGLE_API_KEY`) or Groq API Key (`GROQ_API_KEY`)

---

### Environment Variables

Create a `.env` file in the root directory (or use `.env.docker` for Docker setups):

```env
# AI Models Configuration
GOOGLE_API_KEY=your_google_api_key_here
GROQ_API_KEY=your_groq_api_key_here

# Relational Database URL
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/employee_db_local

# ChromaDB Configuration
CHROMA_DB_PATH=./chroma_db
CHROMA_HOST=chromadb
CHROMA_PORT=8000
```

---

### Option 1: Running with Docker Compose (Recommended)

To build and start all containers (PostgreSQL, ChromaDB, FastAPI API, and Streamlit UI) in one command:

```bash
docker-compose up --build
```

Access the services:
- **Streamlit Web UI**: [http://localhost:8502](http://localhost:8502)
- **FastAPI API Documentation**: [http://localhost:8001/docs](http://localhost:8001/docs)

---

### Option 2: Running Locally (Manual Setup)

1. **Install Dependencies**:
   ```bash
   uv sync
   ```

2. **Start Database Services**:
   Ensure PostgreSQL is running on port `5432` with database `employee_db_local`.

3. **Seed Database**:
   ```bash
   uv run python -m app.database.seed
   ```

4. **Start Backend Server**:
   ```bash
   uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

5. **Start Streamlit App**:
   ```bash
   uv run streamlit run streamlit_app.py
   ```

---

## 💡 Usage Guide

### Streamlit Interface

1. Open [http://localhost:8502](http://localhost:8502) in your web browser.
2. Select your user role from the **Login As** sidebar selectbox (e.g. `Admin`, `Employee A`, `Employee B`).
3. Select an assigned project from the **Project** dropdown.
4. Type natural language queries into the chat bar, such as:
   - *"What is the status and deadline of Project Alpha?"*
   - *"How does authentication work according to our documentation?"*

### Admin Permission Matrix

1. Switch user to **Admin**.
2. Scroll to the **Permission Management** section.
3. Toggle access controls for any user and project pair.
4. Click **Save** to update authorization rules in real time.

### Document Ingestion

1. Log in as **Admin**.
2. Use the **Upload** sidebar widget to upload `.pdf`, `.docx`, or `.txt` files.
3. The server processes, splits, and embeds documents directly into ChromaDB for vector retrieval.

---

## 🔌 API Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Operational health check |
| `GET` | `/users` | List all system users |
| `GET` | `/projects` | List all available projects |
| `POST` | `/chat/stream/` | Stream chat responses with real-time agent execution tokens |
| `POST` | `/upload/` | Upload and vectorize documentation files |
| `GET` | `/access/check` | Check permission for user and project |
| `GET` | `/admin/get-permissions` | Retrieve global permissions matrix |
| `POST` | `/admin/update-permission` | Grant or revoke user project access |

---

## 📊 Database Schema & Initial Seed

The database initializes automatically on seed execution with sample records:

- **Users**: Admin, Employee A, Employee B
- **Projects**:
  - `Project Alpha` (Employee Portal using AI)
  - `Project Beta` (Healthcare Chatbot)
- **Initial Permissions**:
  - `Employee A`: Access granted to `Project Alpha`, denied for `Project Beta`
  - `Employee B`: Access granted to `Project Beta`