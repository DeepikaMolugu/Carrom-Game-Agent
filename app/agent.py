# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import re
import json
import logging
from typing import Any, Optional
from pydantic import BaseModel, Field

from google.adk.agents import LlmAgent
from google.adk.apps import App
from google.adk.models import Gemini
from google.adk.tools import AgentTool
from google.adk.workflow import Workflow, Edge, node
from google.adk.agents.context import Context
from google.adk.events import RequestInput, Event
from google.adk.tools import McpToolset
from mcp.client.stdio import StdioServerParameters
import sys

from app.config import config

logger = logging.getLogger("carrom_agent")

# Define Game State Schema
class CarromGameState(BaseModel):
    player_turn: str = "Player 1"
    score_p1: int = 0
    score_p2: int = 0
    board_state: str = "9 White pieces, 9 Black pieces, 1 Red Queen, 1 Striker"
    last_shot_result: str = ""
    audit_logs: list[str] = Field(default_factory=list)
    moves_history: list[str] = Field(default_factory=list)

# Specialized sub-agent: Referee Agent
referee_agent = LlmAgent(
    name="referee_agent",
    model=Gemini(model=config.model),
    instruction=(
        "You are the Carrom Referee. Your job is to enforce rules, determine turns, "
        "and calculate scoring. Carrom rules:\n"
        "- Scoring: White piece = 10 pts, Black piece = 5 pts, Queen (Red) = 25 pts.\n"
        "- If a player pockets their own color piece, they retain the turn.\n"
        "- Pocketing the Queen requires backing it by pocketing another piece on the same or next shot.\n"
        "- Output a clear description of the new score, who gets the next turn, and board state updates."
    )
)

# Specialized sub-agent: Strategy Coach Agent
coach_agent = LlmAgent(
    name="coach_agent",
    model=Gemini(model=config.model),
    instruction=(
        "You are the Carrom Strategy Coach. Your job is to suggest shot angles, "
        "striker placement (horizontal baseline coordinate x from -1 to 1), "
        "shot power (from 0 to 100), and recommended pocket targets. "
        "Provide detailed physics-based advice (elastic collisions, board friction) "
        "to help the player win."
    )
)

# Multi-Agent Orchestrator Agent
mcp_toolset = McpToolset(
    connection_params=StdioServerParameters(
        command=sys.executable,
        args=[os.path.join(os.path.dirname(__file__), "mcp_server.py")]
    )
)

orchestrator_agent = LlmAgent(
    name="orchestrator_agent",
    model=Gemini(model=config.model),
    instruction=(
        "You are the Carrom Game Master. You receive user move requests, queries about rules, "
        "and shot advisory requests. You delegate to your sub-agents:\n"
        "- For shot outcome, rules, or score validation, use referee_agent.\n"
        "- For shot recommendations, angle planning, or game strategy, use coach_agent.\n"
        "- Use your tools to retrieve or update the game state, and to get carrom rules as needed.\n"
        "- If a player requests a 'custom rule waiver' or 'cheat shot', respond that this requires human approval "
        "and output 'NEEDS_APPROVAL' as the final instruction."
    ),
    tools=[
        AgentTool(agent=referee_agent),
        AgentTool(agent=coach_agent),
        mcp_toolset
    ]
)

# Security node: Input validation, scrubbing, and audit log
@node(name="security_checkpoint", rerun_on_resume=True)
def security_checkpoint(ctx: Context, node_input: Any) -> Any:
    # 1. PII Scrubbing
    input_str = str(node_input)
    email_regex = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    phone_regex = r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b"
    
    clean_input = re.sub(email_regex, "[EMAIL_REDACTED]", input_str)
    clean_input = re.sub(phone_regex, "[PHONE_REDACTED]", clean_input)
    
    # 2. Prompt Injection Detection
    injection_keywords = ["ignore previous instructions", "system prompt", "override rules", "bypass security"]
    is_injection = any(kw in clean_input.lower() for kw in injection_keywords)
    
    # 3. Domain-Specific Rule: Validate input size & coordinates if provided
    coord_violation = False
    if "striker" in clean_input.lower() and "coordinate" in clean_input.lower():
        matches = re.findall(r"[-+]?\d*\.\d+|\d+", clean_input)
        for val in matches:
            try:
                f_val = float(val)
                if abs(f_val) > 1000.0:  # Arbitrary max bound to prevent exploit coordinates
                    coord_violation = True
            except ValueError:
                pass

    # Audit Logging in JSON
    audit_event = {
        "event": "security_check",
        "pii_detected": clean_input != input_str,
        "injection_detected": is_injection,
        "coordinate_violation": coord_violation,
        "severity": "CRITICAL" if (is_injection or coord_violation) else "INFO"
    }
    
    if ctx.state is None:
        ctx.state = CarromGameState()
    
    ctx.state.audit_logs.append(json.dumps(audit_event))
    
    if is_injection or coord_violation:
        ctx.route = "denied"
        return "Security block: Input contains prompt injection or invalid move coordinates."
        
    ctx.route = "approved"
    return clean_input

# Orchestrator Node wrapper that handles routing
@node(name="orchestrator_node", rerun_on_resume=True)
async def orchestrator_node(ctx: Context, node_input: Any) -> Any:
    # Run the orchestrator agent
    res = await ctx.run_node(orchestrator_agent, node_input=node_input)
    
    # If the response indicates needs approval, route to human approval
    if "NEEDS_APPROVAL" in str(res):
        ctx.route = "needs_approval"
    else:
        ctx.route = "done"
        
    return res

# Human-in-the-loop Node
@node(name="human_approval_checkpoint", rerun_on_resume=True)
def human_approval_checkpoint(ctx: Context, node_input: Any) -> Any:
    interrupt_id = "p2_rule_waiver_approval"
    
    # Check if we have received the human response
    if interrupt_id in ctx.resume_inputs:
        response = ctx.resume_inputs[interrupt_id]
        audit_event = {
            "event": "human_approval_response",
            "decision": response,
            "severity": "INFO"
        }
        ctx.state.audit_logs.append(json.dumps(audit_event))
        
        if str(response).lower() in ["yes", "approved", "y"]:
            ctx.route = "approved"
            return f"Player 2 approved the request. Continuing play."
        else:
            ctx.route = "denied"
            return "Player 2 rejected the custom rule waiver request."
            
    # Request Input from the opponent player
    ctx.route = "needs_approval"
    return RequestInput(
        interrupt_id=interrupt_id,
        message="A custom rule waiver / cheat shot was requested by Player 1. Player 2, do you approve? (yes/no)",
        response_schema=str
    )

# Final formatting node
@node(name="final_output", rerun_on_resume=True)
def final_output(ctx: Context, node_input: Any) -> Any:
    if ctx.state is None:
        ctx.state = CarromGameState()
    
    summary = str(node_input)
    ctx.state.last_shot_result = summary
    ctx.state.moves_history.append(summary)
    
    return {
        "output": summary,
        "player_turn": ctx.state.player_turn,
        "score": {
            "Player 1": ctx.state.score_p1,
            "Player 2": ctx.state.score_p2
        },
        "board_state": ctx.state.board_state
    }

# Connect Workflow Graph
carrom_workflow = Workflow(
    name="carrom_workflow",
    state_schema=CarromGameState,
    edges=[
        # START -> Security
        ("START", security_checkpoint),
        
        # Security routing
        (security_checkpoint, {
            "approved": orchestrator_node,
            "denied": final_output
        }),
        
        # Orchestrator routing
        (orchestrator_node, {
            "needs_approval": human_approval_checkpoint,
            "done": final_output
        }),
        
        # Human approval routing
        (human_approval_checkpoint, {
            "approved": orchestrator_node,
            "denied": final_output
        })
    ]
)

# Export the application
app = App(
    root_agent=carrom_workflow,
    name="app"
)
