# Gradient Ascent
### Autonomous SDLC Orchestration Engine
![Language](https://img.shields.io/badge/Language-Python-blue) ![Platform](https://img.shields.io/badge/Platform-Web_%7C_SDK-green) ![License](https://img.shields.io/badge/License-MIT-orange) ![Status](https://img.shields.io/badge/Status-Hackathon-red)

---
### 🔗 Quick Links
- [⚡ The Translation Gap](#-the-translation-gap) - [⚙️ Architecture](#️-architecture-the-three-phase-pipeline) - [📦 Installation Steps](#-getting-started)
- [📐 Usage Example](#-usage--sdk-integration) - [✨ Features](#technical-features) - [🛠️ Tech Stack Decisions](#️-tech-stack-decisions) - [📂 Project Structure](#-project-structure)
---

Gradient Ascent is an **autonomous software development lifecycle (SDLC) pipeline** that bridges the gap between disconnected product requirements, manual QA cycles, and vulnerable code. 

It parses natural language PRDs, generates adversarial test matrices, executes Python source code in a self-healing AST sandbox, and pushes verified artifacts directly to Jira.

> **"Subjective Development in. Deterministic Engineering out."**
> Gradient Ascent treats the SDLC not as a series of human hand-offs, but as a continuous, verifiable computational graph.

---

## What Problem Does Gradient Ascent Solve?

In modern software development, Product Managers draft requirements in ambiguous text, QA engineers manually translate those into tests, and Developers write code based on subjective interpretations of both. 

This translation gap leads to **"Silent Failures"**—critical logical oversights, unhandled edge cases, and security vulnerabilities (like `eval()` risks) that bypass static review. Gradient Ascent completely automates this translation layer, guaranteeing that the code executing in production is cryptographically traced back to the original business requirement.

<p align="right">(<a href="#gradient-ascent">back to top</a>)</p>

---

### ⚡ The Translation Gap

| Metric | Traditional SDLC | Gradient Ascent Workflow |
| :--- | :--- | :--- |
| **Requirements** | Static PDFs, ambiguous text | **Structured Epics & Health Checks** |
| **QA Generation** | Manual, subjective interpretation | **Adversarial Edge-Case Matrix** |
| **Traceability** | Often lost between PM and QA | **100% Unbroken `[REF-ID]` Custody** |
| **Security Scanning**| Fragile Regex (bypassed easily) | **Native AST Structural Mapping** |
| **Bug Resolution** | Fails CI/CD pipeline, manual fix | **Autonomous Self-Healing Sandbox** |

---

## ⚙️ Architecture: The Three-Phase Pipeline

Gradient Ascent is powered by a multi-agent orchestrated routing core. It splits the SDLC into three distinct execution phases, entirely removing the human bottleneck between requirements and Jira tickets.

~~~ mermaid
flowchart TD
    subgraph Phase 1: Ingestion
        A[Raw PRD] --> B[DocumentParser]
        B --> C[PM Agent]
        C --> D[Structured Epics & Health Check]
    end

    subgraph Phase 2: Translation
        D --> E[QA Agent]
        E --> F[Adversarial Matrix]
        F --> G[100% Traceability Vectors]
    end

    subgraph Phase 3: Execution
        G --> H[AST Sandbox Engine]
        I[Source Code] --> H
        H --> J{Sandbox Assertions}
        J -- Fail --> K[Self-Healing Loop]
        K --> H
        J -- Pass --> L[Production Ready Refactor]
    end

    L --> M[Push to Jira API]
    D -.-> M
    G -.-> M
~~~

<p align="right">(<a href="#gradient-ascent">back to top</a>)</p>

---

## ✨Technical Features

### 🧠 The Agents
- **PM Agent (Requirements Audit):** Parses raw PDFs/MDs, injects heuristic `[REF]` tags, and automatically runs a **PRD Health Check** to flag architectural blind spots before code is written.
- **QA Agent (Adversarial Matrices):** Generates exhaustive Positive, Negative, and Edge-Case test vectors based strictly on extracted business logic, maintaining an unbroken chain of custody to the original PRD.
- **Dev Agent (AST Engine):** Deconstructs Python source code into an Abstract Syntax Tree to map logical boundaries and scan for hardcoded secrets or command injections, rendering the topography as a dynamic Mermaid.js flowchart.

### 🛡️ The Routing Core & Sandbox
- **Multi-Model Failover Shield:** Driven by `litellm`, the engine dynamically routes between `gemini-3.1-flash-lite`, Groq's ultra-fast `llama-3.3-70b`, and stable fallbacks to ensure 99.9% uptime during API congestion.
- **Autonomous Self-Healing:** Code is executed in an ephemeral `subprocess` sandbox. If assertions fail, the engine captures the `pytest` traceback and iteratively rewrites the logic up to 3 times to achieve a passing state.
- **Native Jira Integration:** Automatically formats Epics, Matrix Tables, and AST Bug Reports into Atlassian Document Format (ADF) and pushes them via REST API to active Scrum boards.

<p align="right">(<a href="#gradient-ascent">back to top</a>)</p>

---

## 📐 Usage & SDK Integration

Gradient Ascent features a dual-use architecture. You can run the interactive Streamlit Dashboard (`app.py`), or import it natively into your CI/CD pipeline via the SDK.

### 💻 Headless SDK Example

```python
from ai_qa_sdk import GradientAscent

# 1. Initialize Engine
sdk = GradientAscent()

# 2. Audit Requirements (Phase 1)
requirements = sdk.audit_requirements("path/to/prd.pdf")
print(requirements.health_check.blind_spots)

# 3. Generate Traceability Matrix (Phase 2)
matrix = sdk.generate_matrix(requirements)

# 4. AST Verification & Self-Healing (Phase 3)
source_code = """
def process_payment(amount):
    return eval("amount * 1.05") # Vulnerable
"""

reports = sdk.verify_source_code(source_code, context=str(requirements))

for report in reports:
    if report.is_healed:
        print("Bug Patched. Refactored Source:\n", report.refactored_source)
```

<p align="right">(<a href="#gradient-ascent">back to top</a>)</p>

---

## 🛠️ Tech Stack Decisions

- **Why AST over Regex:** Traditional static analysis uses string matching, which is easily bypassed by multi-line strings or aliases (`exec = eval`). Gradient Ascent maps the actual Python Abstract Syntax Tree (`ast.walk`), making vulnerability detection deterministic and immune to syntactic obfuscation.
- **Why Multi-Model Routing:** Relying on a single LLM provider in an autonomous loop is a single point of failure. The `resilient_completion` core leverages Google Gemini for massive context windows (PRD ingestion) but instantly fails over to Groq's LPU-accelerated Llama 3.3 if rate limits are hit.
- **Why Streamlit:** Allowed for the rapid development of a premium, reactive command center that handles file uploads, chat histories, dynamic dataframes, and custom HTML/JS (Mermaid) injections without building a massive React frontend.

---

## ⚠️ Technical Trade-offs (Known & Intentional)

- **Sandbox Security Boundary:** The current execution sandbox relies on Python's `tempfile` and `subprocess` modules. While isolated locally, true production deployment requires containerization (e.g., Docker/gVisor) to safely execute highly untrusted external code.
- **Language Lock-in:** The AST static analyzer is currently hardcoded for Python (`ast` module). Expanding to Java/C++ would require integrating multi-language parsers like Tree-sitter.
- **Context Window Limits:** Extremely large codebases might exceed standard API context windows, requiring future implementation of RAG-based chunking for the Dev Agent.

<p align="right">(<a href="#gradient-ascent">back to top</a>)</p>

---

### 📂 Project Structure

```text
/
├── app.py                  # 🖥️ The Streamlit Command Center (UI)
├── ai_qa_sdk/              # 📦 The Portable Python Library
│   ├── pm/
│   │   ├── parser.py       # Heuristic Tagging & Document Parsing
│   │   └── extractor.py    # PM Agent (Epics & Health Checks)
│   ├── qa/
│   │   └── generator.py    # QA Agent (Traceability Matrices)
│   └── dev/
│       └── unit_tester.py  # AST Engine, Sandbox & Self-Healing
├── .env                    # 🔑 API & Failover Configuration
└── requirements.txt        
```

<p align="right">(<a href="#gradient-ascent">back to top</a>)</p>

---

## 🚀 Getting Started

**Prerequisites**
- Python 3.9+
- API Keys for Google Gemini and Groq.

**Installation**
1. Clone the repository.
2. Install dependencies:
   `pip install -r requirements.txt`
3. Create a `.env` file in the root directory:
   ```env
   GEMINI_API_KEY=your_key_here
   GROQ_API_KEY=your_key_here
   ```
4. Launch the Dashboard:
   `streamlit run app.py`

---

## 👨‍💻 Author(s)

- Ameetesh Awadh
- Arnav Srivastava
- Harkeerat Singh
- Nishant Sharma
- Anuj Kumar
<!-- Built by **Ameetesh** B.Tech Undergraduate (South Asian University)  
Focused on Systems Engineering, SDLC Automation, and LLM Orchestration. -->

---

## License

MIT.
<p align="right">(<a href="#gradient-ascent">back to top</a>)</p>