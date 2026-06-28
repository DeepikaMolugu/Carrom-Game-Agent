# carrom-game-agent

Simple ReAct agent
Agent generated with `agents-cli` version `0.5.0`

## Problem Statement

Creating an engaging, pure HTML5 Carrom game while demonstrating the power of a Multi-Agent architecture. The goal of this project is to show how autonomous agents (such as a Referee, a Strategy Coach, and an Orchestrator) can govern rules, provide intelligent gameplay advice, and maintain security guardrails in a real-time web application using the ADK 2.0 framework and the Model Context Protocol (MCP).


## Project Structure

```
carrom-game-agent/
├── app/         # Core agent code
│   ├── agent.py               # Main agent logic
│   ├── agent_runtime_app.py    # Agent Runtime application logic
│   └── app_utils/             # App utilities and helpers
├── tests/                     # Unit, integration, and load tests
├── GEMINI.md                  # AI-assisted development guide
└── pyproject.toml             # Project dependencies
```

> 💡 **Tip:** Use [Gemini CLI](https://github.com/google-gemini/gemini-cli) for AI-assisted development - project context is pre-configured in `GEMINI.md`.

## Requirements

Before you begin, ensure you have:
- **uv**: Python package manager (used for all dependency management in this project) - [Install](https://docs.astral.sh/uv/getting-started/installation/) ([add packages](https://docs.astral.sh/uv/concepts/dependencies/) with `uv add <package>`)
- **agents-cli**: Agents CLI - Install with `uv tool install google-agents-cli`
- **Google Cloud SDK**: For GCP services - [Install](https://cloud.google.com/sdk/docs/install)


## Quick Start

Install `agents-cli` and its skills if not already installed:

```bash
uvx google-agents-cli setup
```

Install required packages:

```bash
agents-cli install
```

Test the agent with a local web server:

```bash
agents-cli playground
```

You can also use features from the [ADK](https://adk.dev/) CLI with `uv run adk`.

## Commands

| Command              | Description                                                                                 |
| -------------------- | ------------------------------------------------------------------------------------------- |
| `agents-cli install` | Install dependencies using uv                                                         |
| `agents-cli playground` | Launch local development environment                                                  |
| `agents-cli lint`    | Run code quality checks                                                               |
| `agents-cli eval`    | Evaluate agent behavior (generate, grade, analyze, and more — see `agents-cli eval --help`) |
| `uv run pytest tests/unit tests/integration` | Run unit and integration tests                                                        |
| `agents-cli deploy`  | Deploy agent to Agent Runtime                                                                |
| `agents-cli publish gemini-enterprise` | Register deployed agent to Gemini Enterprise                    |

## 🛠️ Project Management

| Command | What It Does |
|---------|--------------|
| `agents-cli scaffold enhance` | Add CI/CD pipelines and Terraform infrastructure |
| `agents-cli infra cicd` | One-command setup of entire CI/CD pipeline + infrastructure |
| `agents-cli scaffold upgrade` | Auto-upgrade to latest version while preserving customizations |

---

## Development

Edit your agent logic in `app/agent.py` and test with `agents-cli playground` - it auto-reloads on save.

## Deployment

```bash
gcloud config set project <your-project-id>
agents-cli deploy
```

To add CI/CD and Terraform, run `agents-cli scaffold enhance`.
To set up your production infrastructure, run `agents-cli infra cicd`.

## Observability

Built-in telemetry exports to Cloud Trace, BigQuery, and Cloud Logging.

## Version Control (GitHub)

To push this project to a new repository on GitHub, open your terminal and follow these steps:

1. Navigate to your project folder:
   ```bash
   cd "C:\Users\deepi\AI Agents\adk-workspace\carrom-game-agent"
   ```
2. Initialize git and commit your files:
   ```bash
   git init
   git add .
   git commit -m "Initial commit of Carrom Game Agent"
   ```
3. Create a new empty repository on GitHub.
4. Link the remote and push your code:
   ```bash
   git remote add origin https://github.com/DeepikaMolugu/Carrom-Game-Agent.git
   git branch -M main
   git push -u origin main
   ```

## Assets

### Workflow Architecture Diagram
![Carrom Agent Architecture Diagram](assets/architecture_diagram.png)

### Cover Banner
![Carrom Game Cover Banner](assets/cover_page_banner.png)

## Demo Script

If you'd like to present this project, check out the [Demo Script](DEMO_SCRIPT.txt) for a guided walkthrough of the architecture and a live demonstration of the multi-agent workflow.
