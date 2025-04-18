import asyncio
import os
from dotenv import load_dotenv
from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters

from perception import Perception
from memory import Memory
from decision import Decision
from action import Action
from models import ToolDescription

async def main():
    # Load environment variables
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    
    # Check if API key exists
    if not api_key:
        print("Error: GEMINI_API_KEY not found in environment variables")
        return
    
    # Initialize perception component
    perception = Perception(api_key)
    memory = Memory()
    
    try:
        # Setup MCP connection
        server_params = StdioServerParameters(
            command="python",
            args=["example2-6.py"]
        )
        
        print("Connecting to MCP server...")
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                print("Initializing session...")
                await session.initialize()
                
                # Get available tools
                print("Fetching available tools...")
                tools_result = await session.list_tools()
                tools = [
                    ToolDescription(
                        name=tool.name,
                        description=getattr(tool, 'description', 'No description available'),
                        input_schema=tool.inputSchema
                    )
                    for tool in tools_result.tools
                ]
                
                # Initialize decision and action components
                decision = Decision(tools)
                action = Action(session)
                
                # Create system prompt using tool descriptions
                tools_description = decision.format_tools_description()
                perception.create_system_prompt(tools_description)

                print(perception.system_prompt)
                
                # Set initial query
                memory.memory.current_query = """Find the ASCII values of characters in INDIA and then return sum of exponentials of those values and print this sum in paint
                inside a rectangle object which is drawn in the centre of paint canvas"""
                
                print("Starting main loop...")
                # Main loop
                while memory.state.iteration < memory.state.max_iterations:
                    print(f"Iteration {memory.state.iteration + 1}/{memory.state.max_iterations}")
                    # Get context from memory
                    context = memory.get_context_for_llm()
                    
                    # Get LLM response using the system prompt and context
                    print("Generating LLM response...")
                    try:
                        llm_response = await perception.generate_with_timeout(context)
                        print(f"Response type: {llm_response.response_type}")
                        print(llm_response)
                        
                        # Process response
                        if llm_response.response_type == "FUNCTION_CALL":
                            tool_call = decision.process_llm_response(llm_response)
                            print(f"Executing tool: {tool_call.function}")
                            # Execute tool
                            result = await action.execute_tool(tool_call)
                            # Update memory
                            memory.update_state(tool_call, result)
                            
                            if not result.success:
                                print(f"Tool execution failed: {result.error}")
                                break
                        elif llm_response.response_type == "FINAL_ANSWER":
                            print(f"Final Answer: {llm_response.content.get('final_answer')}")
                            break
                        else:
                            # Error or verify
                            print(f"Agent response: {llm_response.response_type} - {llm_response.content}")
                            break
                    except TimeoutError:
                        print("LLM response timed out. Retrying or exiting...")
                        break  # Exit the loop on timeout instead of hanging
                    except Exception as e:
                        print(f"Error generating LLM response: {e}")
                        break
                        
    except Exception as e:
        print(f"Error in execution: {e}")
    finally:
        memory.reset()

if __name__ == "__main__":
    asyncio.run(main())
