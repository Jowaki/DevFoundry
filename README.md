# DevFoundry

### Autonomous Multi-Agent Software Engineering System

**DevFoundry** is a multi-agent AI software engineering platform that transforms natural-language requirements into tested, security-audited, and documented software.

Instead of relying on a single LLM to generate an entire application, DevFoundry uses a team of specialized AI agents coordinated by a **Lead Orchestrator**.

The system doesn't stop when code is generated.

It can **analyze → build → test → audit → diagnose → repair → regenerate → verify → document**.

---

## What is DevFoundry?

Give DevFoundry a requirement such as:

> "Build a REST API for a task management application with authentication, PostgreSQL, and role-based access control."

DevFoundry coordinates multiple specialized agents to turn that requirement into a complete software engineering workflow.

### The pipeline

```text
Natural Language Requirement
            │
            ▼
    Lead Orchestrator
            │
            ▼
       Architecture
            │
            ▼
      Code Generation
            │
            ▼
      Automated Testing
            │
            ▼
      Security Analysis
            │
            ▼
      Issue Classification
            │
            ├──── Critical / Unfixable ────► Report
            │
            └──── Fixable ──► Repair Loop
                              │
                              ▼
                         Regenerate Code
                              │
                              ▼
                         Run Tests Again
                              │
                              ▼
                       Security Audit Again
                              │
                              ▼
                         Final Validation
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
               Final Code          PDF Report
```

---

# Multi-Agent Architecture

DevFoundry uses specialized agents instead of asking one model to perform every task.

```text
                         ┌──────────────────┐
                         │ Lead Orchestrator│
                         └────────┬─────────┘
                                  │
             ┌────────────────────┼────────────────────┐
             │                    │                    │
             ▼                    ▼                    ▼
      Architecture             Code                 Testing
         Agent                Agent                  Agent
             │                    │                    │
             └────────────────────┼────────────────────┘
                                  │
                                  ▼
                           Security Agent
                                  │
                                  ▼
                         Issue Classification
                                  │
                                  ▼
                           Repair / Regenerate
                                  │
                                  ▼
                           Verification Loop
```

## Specialized Agents

### Architecture Agent

Responsible for translating requirements into a technical design.

Responsibilities:

* System architecture
* Component design
* Database schema
* API endpoints
* Dependencies
* Design decisions
* Scalability considerations

---

### Code Agent

Responsible for implementing the architecture.

Responsibilities:

* Generate application code
* Follow architectural decisions
* Implement APIs
* Implement business logic
* Generate project structure
* Apply coding best practices

---

### Test Agent

Responsible for validating the generated implementation.

Responsibilities:

* Generate unit tests
* Generate integration tests
* Identify edge cases
* Test failure scenarios
* Validate API behavior
* Detect regressions

---

### Security Agent

Acts as an automated security reviewer.

Checks for issues including:

* Authentication problems
* Authorization problems
* SQL injection
* Hardcoded secrets
* Unsafe input handling
* Insecure dependencies
* OWASP-style vulnerabilities
* Sensitive data exposure
* Misconfigured security controls

---

### Lead Orchestrator

The Lead Orchestrator coordinates the entire engineering workflow.

It decides:

* Which agent should run next
* What context each agent receives
* Whether the generated implementation satisfies the requirements
* Whether issues are repairable
* When code should be regenerated
* When tests should be re-run
* When security should be re-evaluated
* When the project is ready for final output

The orchestrator is effectively the **AI engineering manager** of the system.

---

# Autonomous Repair Loop

One of DevFoundry's key features is that the system doesn't simply report problems.

It attempts to **fix problems automatically**.

For example:

```text
Security Agent
      │
      ▼
SQL Injection vulnerability detected
      │
      ▼
Severity: CRITICAL
Fixable: YES
      │
      ▼
Orchestrator creates repair task
      │
      ▼
Code Agent modifies implementation
      │
      ▼
Test Agent validates modification
      │
      ▼
Security Agent re-audits
      │
      ▼
Issue resolved
```

The goal is to create a closed engineering loop rather than a one-shot generation pipeline.

---

# Issue Classification

DevFoundry classifies findings based on severity and whether they can reasonably be addressed automatically.

| Severity        | Meaning                                                 | Automatic Repair      |
| --------------- | ------------------------------------------------------- | --------------------- |
| 🔴 Critical     | Serious security, correctness, or architectural problem | Depends on confidence |
| 🟠 High         | Significant defect or risk                              | Yes                   |
| 🟡 Medium       | Important but localized issue                           | Yes                   |
| 🔵 Low          | Minor improvement                                       | Optional              |
| ⚪ Informational | Recommendation / observation                            | No                    |

Each issue can contain:

```json
{
  "severity": "medium",
  "category": "best_practice",
  "description": "Database sessions are created without explicit lifecycle management.",
  "impact": "Potential resource leakage under sustained traffic.",
  "fixable": true,
  "recommended_action": "Use dependency-managed database sessions.",
  "source_agent": "security"
}
```

The orchestrator can then determine whether the issue should enter the repair loop.

---

#  Regeneration

DevFoundry supports **issue-aware code regeneration**.

Instead of regenerating an entire application blindly, the repair agent receives:

```text
Original Requirements
        +
Architecture
        +
Current Code
        +
Test Results
        +
Security Findings
        +
Best Practice Recommendations
        ↓
     Repair Plan
        ↓
    Updated Code
```

This allows the system to make targeted improvements while preserving functionality that already works.

---

# Engineering Report

Every generation can produce a final PDF engineering report.

The report documents the entire lifecycle of the generated system.

### Report sections

```text
DevFoundry Engineering Report
│
├── Executive Summary
├── Original Requirements
├── Architecture
├── Design Decisions
├── Generated Components
├── Agent Activity
├── Test Results
├── Security Findings
├── Issue Classification
├── Automatically Applied Fixes
├── Remaining Issues
├── Best Practice Recommendations
├── Regeneration History
├── Validation Results
└── Final System Status
```

This turns the project from a **code generator** into an **AI engineering audit system**.

---

# Example Report

A generated report might contain:

```text
PROJECT: Task Management API

STATUS: PASSED WITH WARNINGS

Requirements
✓ REST API
✓ Authentication
✓ PostgreSQL
✓ Role-based access control

Architecture
✓ Layered architecture
✓ PostgreSQL persistence
✓ JWT authentication

Testing
✓ 47 tests generated
✓ 44 passed
✗ 3 failed

Security
✓ No hardcoded secrets
✓ Parameterized queries
✓ Authentication implemented

Issues
─────────────────────────────────────────
CRITICAL   0
HIGH       1
MEDIUM     3
LOW        2

Automatically Fixed
─────────────────────────────────────────
✓ Missing authorization check
✓ Database session lifecycle
✓ Input validation

Remaining
─────────────────────────────────────────
⚠ Dependency version recommendation
⚠ Additional rate limiting recommended

FINAL STATUS
PASS WITH WARNINGS
```

---

#  Technology Stack

### Backend

* Python 3.10+
* FastAPI
* LangChain
* LangGraph
* OpenAI

### Frontend

* React
* TypeScript
* WebSocket

### Testing

* pytest

### Deployment

* Render
* Vercel

### Development

* GitHub Copilot

---

# Project Structure

```text
devfoundry/
│
├── backend/
│   ├── agents/
│   │   ├── architecture.py
│   │   ├── code_generation.py
│   │   ├── testing.py
│   │   └── security.py
│   │
│   ├── orchestrator/
│   │   ├── graph.py
│   │   ├── state.py
│   │   ├── routing.py
│   │   └── repair.py
│   │
│   ├── reporting/
│   │   ├── report_generator.py
│   │   └── pdf_renderer.py
│   │
│   ├── models/
│   ├── services/
│   ├── main.py
│   └── config.py
│
├── frontend/
│   ├── components/
│   │   ├── InputSpec.tsx
│   │   ├── AgentTimeline.tsx
│   │   ├── CodeOutput.tsx
│   │   ├── IssuePanel.tsx
│   │   └── ReportViewer.tsx
│   │
│   └── src/
│
├── generated/
│   ├── projects/
│   └── reports/
│
├── tests/
│
├── .env.example
├── requirements.txt
└── README.md
```

---

# Example

Input:

```text
Build a REST API for a todo application.

Users should be able to:
- Register
- Login
- Create tasks
- Update tasks
- Delete tasks
- Mark tasks as complete
```

DevFoundry produces:

```text
1. Architecture
        ↓
2. Database Design
        ↓
3. API Specification
        ↓
4. Python/FastAPI Implementation
        ↓
5. Pytest Test Suite
        ↓
6. Security Audit
        ↓
7. Issue Classification
        ↓
8. Automatic Repair
        ↓
9. Re-testing
        ↓
10. Final Code
        ↓
11. Engineering PDF
```

---

# Design Philosophy

DevFoundry is built around one principle:

> **AI should not just generate software. It should participate in the software engineering lifecycle.**

A traditional LLM workflow looks like:

```text
Prompt → LLM → Code
```

DevFoundry aims for:

```text
Requirements
     ↓
Planning
     ↓
Architecture
     ↓
Implementation
     ↓
Testing
     ↓
Security
     ↓
Diagnosis
     ↓
Repair
     ↓
Verification
     ↓
Documentation
```

This makes the system closer to an **AI software engineering team** than a traditional code-generation tool.

---

# Current Limitations

DevFoundry is an experimental engineering project.

Generated code should always be reviewed by a human before production deployment.

LLM-generated analysis can contain:

* False positives
* False negatives
* Incorrect architectural assumptions
* Incomplete test coverage
* Incorrect security recommendations
* Unsafe automated modifications

The repair loop therefore uses validation gates rather than assuming every generated fix is correct.

---

# Roadmap

### Phase 1 — Multi-Agent Generation

* [x] Architecture Agent
* [x] Code Agent
* [x] Test Agent
* [x] Security Agent
* [ ] Lead Orchestrator

### Phase 2 — Autonomous Engineering Loop

* [ ] Issue classification
* [ ] Repair planning
* [ ] Automatic code regeneration
* [ ] Test/re-test cycle
* [ ] Security re-audit
* [ ] Regression detection

### Phase 3 — Engineering Intelligence

* [ ] PDF engineering reports
* [ ] Agent activity timeline
* [ ] Diff viewer
* [ ] Generation history
* [ ] Cost tracking
* [ ] Agent voting
* [ ] Persistent project memory

### Phase 4 — Advanced Capabilities

* [ ] Multi-language generation
* [ ] Existing repository analysis
* [ ] Pull request generation
* [ ] GitHub integration
* [ ] CI/CD integration
* [ ] Human approval gates
* [ ] Long-running autonomous engineering tasks

---

# 📈 Why This Project?

DevFoundry is designed to explore several areas of modern AI engineering:

* Agentic AI
* Multi-agent systems
* LLM orchestration
* LangGraph state management
* Prompt engineering
* Automated software testing
* AI-assisted security analysis
* Autonomous code repair
* Human-in-the-loop AI
* Real-time agent communication
* Full-stack AI applications
* AI-generated technical documentation

---

# 💡 Future Vision

The long-term goal is not simply to generate code.

The goal is to create an **AI software engineering organization in a box**.

Different agents can take on different engineering roles:

```text
              AI Engineering Manager
                       │
          ┌────────────┼────────────┐
          │            │            │
      Architect      Developer     QA
          │            │            │
          └────────────┼────────────┘
                       │
                    Security
                       │
                    Reviewer
                       │
                    Repairer
                       │
                  Documentation
```

The orchestrator coordinates the team, evaluates their work, and determines whether the system is ready to ship.

---

# Built With

Built as an exploration of **multi-agent AI, software engineering automation, and LLM orchestration**.

GitHub Copilot is used throughout development for boilerplate generation, testing assistance, debugging, refactoring, and documentation.

---

# Project Status

**Active Development **

DevFoundry is continuously evolving toward a more autonomous software engineering workflow.

---

## The Goal

**Don't just generate code.**

**Build an AI engineering team that can improve its own work.**
