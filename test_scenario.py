import asyncio
from google.adk.agents.context import Context
from app.agent import carrom_workflow
from google.adk.events import RequestInput

async def test_run():
    print("--- Test Scenario: Requesting Rule Waiver ---")
    prompt = "Player 1 requests a custom rule waiver to pocket the Queen without covering it."
    print(f"Input: {prompt}\n")
    
    ctx = Context()
    interrupt_id = None
    
    print("Running workflow...")
    async for event in carrom_workflow.run(ctx=ctx, node_input=prompt):
        print(event)
        if isinstance(event, RequestInput):
            interrupt_id = event.interrupt_id
            print(f"\n[!] Human-in-the-loop Triggered: {event.message}")
            break

    if interrupt_id:
        print("\nSending 'yes' to approve the waiver...")
        ctx.resume_inputs = {interrupt_id: "yes"}
        # Continue execution with the injected input
        async for event in carrom_workflow.run(ctx=ctx, node_input=prompt):
            print(event)

if __name__ == "__main__":
    asyncio.run(test_run())
