from mcp.server.fastmcp import FastMCP
import json

# Initialize the MCP Server
mcp = FastMCP("CarromServer")

# Simulate a simple backend store for game states (for demo purposes)
game_db = {
    "current_game": {
        "player_turn": "Player 1",
        "score_p1": 0,
        "score_p2": 0,
        "board_state": "9 White pieces, 9 Black pieces, 1 Red Queen, 1 Striker",
        "last_shot_result": ""
    }
}

@mcp.tool()
def get_game_state() -> str:
    """Retrieves the current Carrom game state."""
    return json.dumps(game_db["current_game"])

@mcp.tool()
def get_carrom_rules() -> str:
    """Provides the official Carrom rules."""
    return (
        "Carrom rules:\n"
        "- Scoring: White piece = 10 pts, Black piece = 5 pts, Queen (Red) = 25 pts.\n"
        "- If a player pockets their own color piece, they retain the turn.\n"
        "- Pocketing the Queen requires backing it by pocketing another piece on the same or next shot."
    )

@mcp.tool()
def update_game_state(player_turn: str, score_p1: int, score_p2: int, board_state: str, last_shot_result: str) -> str:
    """Updates the game state."""
    game_db["current_game"] = {
        "player_turn": player_turn,
        "score_p1": score_p1,
        "score_p2": score_p2,
        "board_state": board_state,
        "last_shot_result": last_shot_result
    }
    return f"Game state updated successfully."

if __name__ == "__main__":
    # Start the MCP server using stdio transport
    mcp.run()
