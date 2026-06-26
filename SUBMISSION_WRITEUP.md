# Carrom Multi-Agent Game
**A next-generation AI-powered Carrom Game powered by ADK 2.0 and MCP.**

![Carrom Game Cover Banner](/C:/Users/deepi/.gemini/antigravity-ide/brain/7383ed22-9bed-43ab-a8e0-8f3b6e67ff68/carrom_game_banner_1782478069784.png)

## Overview
This project is an advanced, purely browser-based HTML5 Carrom game integrated with a highly sophisticated **Multi-Agent Workflow**. We built a dynamic, 60fps physics-enabled game interface that operates in sync with intelligent agent nodes to govern, coach, and secure the playing experience.

## Technical Architecture

![Carrom Agent Architecture Diagram](/C:/Users/deepi/.gemini/antigravity-ide/brain/7383ed22-9bed-43ab-a8e0-8f3b6e67ff68/carrom_agent_architecture_1782477923163.png)

### 1. Multi-Agent Orchestration (ADK 2.0)
The backend leverages the **ADK 2.0 Workflow** framework, organizing language models into a specialized hierarchy:
* **Orchestrator Agent**: Acts as the Game Master, receiving incoming player chat requests and delegating them to sub-agents.
* **Referee Agent**: Expert in Carrom mechanics, enforcing scoring rules (White=10, Black=5, Queen=25) and turn-retention logic.
* **Strategy Coach Agent**: Advises players on optimal striker placement, power, and shot angles based on the current board state.

### 2. Model Context Protocol (MCP) Integration
To seamlessly bridge the live game state with the LLM context, we implemented an **MCP Server** via `FastMCP`.
* Tools such as `get_game_state`, `get_carrom_rules`, and `update_game_state` allow the Orchestrator to pull realtime JSON context regarding piece counts, scores, and turns directly from the application layer over the `stdio` transport using `McpToolset`.

### 3. Security Checkpoints & Human-in-the-Loop (HITL)
Robust safety guardrails are integrated natively into the ADK node graph:
* **Security Checkpoint**: Intercepts every incoming query to scrub PII (emails/phones), block malicious prompt injections, and validate numerical boundaries for game coordinates.
* **Human Approval Node (HITL)**: If a player requests a "custom rule waiver" or a "cheat shot", the Orchestrator triggers an interrupt. The workflow pauses execution and requests explicit approval from the opponent (Player 2) before allowing the move to proceed.

### 4. Pure HTML5 Canvas Engine
The frontend is built without heavy game engines, emphasizing zero dependencies and high performance:
* Custom Rigid-Body 2D Physics handling elastic collisions, momentum transfer, and friction.
* Dynamic Web Audio API integration for velocity-dependent wooden strike sounds.
* Slingshot click-and-drag controls.

## How to Play
1. **Play the Game:** Open [index.html](file:///c:/Users/deepi/AI%20Agents/adk-workspace/carrom-game-agent/index.html) in your browser.
2. **Interact with the Agents:** Run `uv run agents-cli interact` in your terminal to chat with the Game Master, ask for coaching, or request rule waivers!
