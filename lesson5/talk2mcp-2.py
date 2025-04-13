import os
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
import asyncio
from google import genai
from concurrent.futures import TimeoutError
from functools import partial
import json

# Load environment variables from .env file
load_dotenv()

# Access your API key and initialize Gemini client correctly
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

max_iterations = 6
last_response = None
iteration = 0
iteration_response = []

async def generate_with_timeout(client, prompt, timeout=10):
    """Generate content with a timeout"""
    print("Starting LLM generation...")
    try:
        # Convert the synchronous generate_content call to run in a thread
        loop = asyncio.get_event_loop()
        response = await asyncio.wait_for(
            loop.run_in_executor(
                None, 
                lambda: client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt
                )
            ),
            timeout=timeout
        )
        print("LLM generation completed")
        return response
    except TimeoutError:
        print("LLM generation timed out!")
        raise
    except Exception as e:
        print(f"Error in LLM generation: {e}")
        raise

def reset_state():
    """Reset all global variables to their initial state"""
    global last_response, iteration, iteration_response
    last_response = None
    iteration = 0
    iteration_response = []

async def main():
    reset_state()  # Reset at the start of main
    print("Starting main execution...")
    try:
        # Create a single MCP server connection
        print("Establishing connection to MCP server...")
        server_params = StdioServerParameters(
            command="python",
            args=["example2-3.py"]
        )

        async with stdio_client(server_params) as (read, write):
            print("Connection established, creating session...")
            async with ClientSession(read, write) as session:
                print("Session created, initializing...")
                await session.initialize()
                
                # Get available tools
                print("Requesting tool list...")
                tools_result = await session.list_tools()
                tools = tools_result.tools
                print(f"Successfully retrieved {len(tools)} tools")

                # Create system prompt with available tools
                print("Creating system prompt...")
                print(f"Number of tools: {len(tools)}")
                
                try:
                    # First, let's inspect what a tool object looks like
                    # if tools:
                    #     print(f"First tool properties: {dir(tools[0])}")
                    #     print(f"First tool example: {tools[0]}")
                    
                    tools_description = []
                    for i, tool in enumerate(tools):
                        try:
                            # Get tool properties
                            params = tool.inputSchema
                            desc = getattr(tool, 'description', 'No description available')
                            name = getattr(tool, 'name', f'tool_{i}')
                            
                            # Format the input schema in a more readable way
                            if 'properties' in params:
                                param_details = []
                                for param_name, param_info in params['properties'].items():
                                    param_type = param_info.get('type', 'unknown')
                                    param_details.append(f"{param_name}: {param_type}")
                                params_str = ', '.join(param_details)
                            else:
                                params_str = 'no parameters'

                            tool_desc = f"{i+1}. {name}({params_str}) - {desc}"
                            tools_description.append(tool_desc)
                            print(f"Added description for tool: {tool_desc}")
                        except Exception as e:
                            print(f"Error processing tool {i}: {e}")
                            tools_description.append(f"{i+1}. Error processing tool")
                    
                    tools_description = "\n".join(tools_description)
                    print("Successfully created tools description")
                except Exception as e:
                    print(f"Error creating tools description: {e}")
                    tools_description = "Error loading tools"
                
                print("Created system prompt...")
                
                system_prompt = f"""You are a math agent solving problems in iterations. You have access to various mathematical tools.

Available tools:
{tools_description}

You must respond with EXACTLY ONE line in one of these formats (no additional text):
1. For function calls:
   FUNCTION_CALL: {{"function": "function_name", "params": {{"param1": value1, "param2": value2, ...}}}}

2. For final answers:
   FINAL_ANSWER: {{"final_answer": number}}

3. For errors or verification:
   ERROR: {{"type": "error_type", "details": "error_details"}}
   VERIFY: {{"expected": expected_value, "actual": actual_value}}

Important:
- When a function returns multiple values, you need to process all of them
- Only give FINAL_ANSWER when you have completed all necessary calculations
- Do not repeat function calls with the same parameters
- After each calculation, verify the result makes sense in context
- If a tool fails or returns unexpected results, use ERROR format
- For division operations, verify divisor is not zero before calling
- For square roots, verify input is non-negative
- For factorial, verify input is non-negative
- For logarithms, verify input is positive
- If uncertain about a result, use VERIFY format to check against expected values
- When using trigonometric functions, verify angles are in appropriate range
- If a tool returns an error, try alternative approaches or report the error

Examples:
- FUNCTION_CALL: {{"function": "add", "params": {{"a": 5, "b": 3}}}}
- FUNCTION_CALL: {{"function": "strings_to_chars_to_int", "params": {{"string": "INDIA"}}}}
- FINAL_ANSWER: {{"final_answer": 42}}
- ERROR: {{"type": "division_by_zero", "details": "Cannot divide by zero"}}
- VERIFY: {{"expected": 8, "actual": 7}}"""
                print(f"system prompt is {system_prompt}")
                query = """Find the ASCII values of characters in INDIA and then return sum of exponentials of those values and print this sum in paint
                inside a rectangle object which is drawn in the centre of paint canvas"""
                print("Starting iteration loop...")
                
                # Use global iteration variables
                global iteration, last_response
                
                while iteration < max_iterations:
                    print(f"\n--- Iteration {iteration + 1} ---")
                    if last_response is None:
                        current_query = query
                    else:
                        current_query = current_query + "\n\n" + " ".join(iteration_response)
                        current_query = current_query + "  What should I do next?"

                    # Get model's response with timeout
                    print("Preparing to generate LLM response...")
                    prompt = f"{system_prompt}\n\nQuery: {current_query}"
                    try:
                        response = await generate_with_timeout(client, prompt)
                        response_text = response.text.strip()
                        print(f"LLM Response: {response_text}")
                        
                        # Parse the response line that contains the function call
                        for line in response_text.split('\n'):
                            line = line.strip()
                            if line.startswith(("FUNCTION_CALL:", "FINAL_ANSWER:", "ERROR:", "VERIFY:")):
                                response_text = line
                                break
                        
                    except Exception as e:
                        print(f"Failed to get LLM response: {e}")
                        break

                    if response_text.startswith("FUNCTION_CALL:"):
                        try:
                            # Parse the JSON part of the response
                            json_str = response_text.replace("FUNCTION_CALL:", "").strip()
                            function_data = json.loads(json_str)
                            
                            func_name = function_data["function"]
                            params = function_data["params"]
                            
                            print(f"\nDEBUG: Function name: {func_name}")
                            print(f"DEBUG: Parameters: {params}")
                            
                            # Find the matching tool
                            tool = next((t for t in tools if t.name == func_name), None)
                            if not tool:
                                print(f"DEBUG: Available tools: {[t.name for t in tools]}")
                                raise ValueError(f"Unknown tool: {func_name}")

                            print(f"DEBUG: Found tool: {tool.name}")
                            print(f"DEBUG: Tool schema: {tool.inputSchema}")

                            # Call the tool with the parameters directly
                            result = await session.call_tool(func_name, arguments=params)
                            print(f"DEBUG: Raw result: {result}")
                            
                            # Process the result
                            if hasattr(result, 'content'):
                                print(f"DEBUG: Result has content attribute")
                                if isinstance(result.content, list):
                                    iteration_result = [
                                        item.text if hasattr(item, 'text') else str(item)
                                        for item in result.content
                                    ]
                                else:
                                    iteration_result = str(result.content)
                            else:
                                print(f"DEBUG: Result has no content attribute")
                                iteration_result = str(result)
                                
                            print(f"DEBUG: Final iteration result: {iteration_result}")
                            
                            # Format the response
                            if isinstance(iteration_result, list):
                                result_str = f"[{', '.join(map(str, iteration_result))}]"
                            else:
                                result_str = str(iteration_result)
                            
                            iteration_response.append(
                                f"In the {iteration + 1} iteration you called {func_name} with {params} parameters, "
                                f"and the function returned {result_str}."
                            )
                            last_response = iteration_result

                        except json.JSONDecodeError as e:
                            print(f"DEBUG: JSON parsing error: {e}")
                            print(f"DEBUG: Attempted to parse: {json_str}")
                            iteration_response.append(f"Error parsing function call in iteration {iteration + 1}: {str(e)}")
                            break
                        except Exception as e:
                            print(f"DEBUG: Error details: {str(e)}")
                            print(f"DEBUG: Error type: {type(e)}")
                            import traceback
                            traceback.print_exc()
                            iteration_response.append(f"Error in iteration {iteration + 1}: {str(e)}")
                            break

                    elif response_text.startswith("FINAL_ANSWER:"):
                        print("\n=== Agent Execution Complete ===")
                        try:
                            answer_data = json.loads(response_text.replace("FINAL_ANSWER:", "").strip())
                            print(f"Final Answer: {answer_data['final_answer']}")
                        except json.JSONDecodeError:
                            print("Error parsing final answer")
                        break

                    iteration += 1

    except Exception as e:
        print(f"Error in main execution: {e}")
        import traceback
        traceback.print_exc()
    finally:
        reset_state()  # Reset at the end of main

if __name__ == "__main__":
    asyncio.run(main())
    
    
