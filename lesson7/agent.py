import asyncio
import time
import os
import datetime
from perception import extract_perception
from memory import MemoryManager, MemoryItem
from decision import generate_plan
from action import execute_tool
from example7 import index_url
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
 # use this to connect to running server

import shutil
import sys

def log(stage: str, msg: str):
    now = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{now}] [{stage}] {msg}",  file=sys.stderr, flush=True)

max_steps = 3

async def main(user_input: str):
    try:
        print("[agent] Starting agent...")
        print(f"[agent] Current working directory: {os.getcwd()}")
        
        server_params = StdioServerParameters(
            command="python",
            args=["example7.py"],
            cwd="/home/sn/EAG-V1/lesson7"
        )

        try:
            async with stdio_client(server_params) as (read, write):
                print("Connection established, creating session...")
                try:
                    async with ClientSession(read, write) as session:
                        print("[agent] Session created, initializing...")
 
                        try:
                            await session.initialize()
                            print("[agent] MCP session initialized")

                            # Your reasoning, planning, perception etc. would go here
                            tools = await session.list_tools()
                            print("Available tools:", [t.name for t in tools.tools])

                            # Get available tools
                            print("Requesting tool list...")
                            tools_result = await session.list_tools()
                            tools = tools_result.tools
                            tool_descriptions = "\n".join(
                                f"- {tool.name}: {getattr(tool, 'description', 'No description')}" 
                                for tool in tools
                            )

                            log("agent", f"{len(tools)} tools loaded")

                            memory = MemoryManager()
                            session_id = f"session-{int(time.time())}"
                            query = user_input  # Store original intent
                            step = 0

                            while step < max_steps:
                                log("loop", f"Step {step + 1} started")

                                perception = extract_perception(user_input)
                                log("perception", f"Intent: {perception.intent}, Tool hint: {perception.tool_hint}")

                                retrieved = memory.retrieve(query=user_input, top_k=3, session_filter=session_id)
                                log("memory", f"Retrieved {len(retrieved)} relevant memories")

                                plan = generate_plan(perception, retrieved, tool_descriptions=tool_descriptions)
                                log("plan", f"Plan generated: {plan}")

                                if plan.startswith("FINAL_ANSWER:"):
                                    log("agent", f"✅ FINAL RESULT: {plan}")
                                    break

                                try:
                                    result = await execute_tool(session, tools, plan)
                                    log("tool", f"{result.tool_name} returned: {result.result}")

                                    memory.add(MemoryItem(
                                        text=f"Tool call: {result.tool_name} with {result.arguments}, got: {result.result}",
                                        type="tool_output",
                                        tool_name=result.tool_name,
                                        user_query=user_input,
                                        tags=[result.tool_name],
                                        session_id=session_id
                                    ))

                                    user_input = f"Original task: {query}\nPrevious output: {result.result}\nWhat should I do next?"

                                except Exception as e:
                                    log("error", f"Tool execution failed: {e}")
                                    break

                                step += 1
                        except Exception as e:
                            print(f"[agent] Session initialization error: {str(e)}")
                except Exception as e:
                    print(f"[agent] Session creation error: {str(e)}")
        except Exception as e:
            print(f"[agent] Connection error: {str(e)}")
    except Exception as e:
        print(f"[agent] Overall error: {str(e)}")

    log("agent", "Agent session complete.")

#if __name__ == "__main__":
#    query = input("🧑 What do you want to solve today? → ")
#    asyncio.run(main(query))


# Find the ASCII values of characters in INDIA and then return sum of exponentials of those values.
# How much Anmol singh paid for his DLF apartment via Capbridge? 
# What do you know about Don Tapscott and Anthony Williams?
# What is the relationship between Gensol and Go-Auto?


# --- Additions for server functionality below ---

from flask import Flask, request, jsonify
from flask_cors import CORS
import threading

app = Flask(__name__)
CORS(app)

def find_url_for_query(query):
    """
    Synchronous wrapper to run the agent and extract a URL from the result.
    This is a placeholder: you should adapt the logic to extract the URL from the agent's output.
    """
    import asyncio

    # This function will capture the FINAL_ANSWER from the agent's plan
    result_holder = {}

    async def run_agent_and_capture(query):
        # You may want to adapt this to parse the plan for a URL
        # For now, we just print and return the last plan
        nonlocal result_holder
        # You may want to refactor main() to return the plan instead of printing
        # For now, we capture stdout
        import io, sys, re
        old_stdout = sys.stdout
        sys.stdout = mystdout = io.StringIO()
        await main(query)
        sys.stdout = old_stdout
        output = mystdout.getvalue()
        # Try to extract a URL from FINAL_ANSWER or output
        url_match = re.search(r'(https?://[^\s\'"<>]+)', output)
        if url_match:
            url = url_match.group(1).rstrip('.,);:!?\'"')
            result_holder['url'] = url
        else:
            result_holder['url'] = None

    asyncio.run(run_agent_and_capture(query))
    return result_holder['url']

@app.route('/search', methods=['POST'])
def search():
    log("flask", "Received /search request")
    data = request.get_json()
    query = data.get('query', '')
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    url = find_url_for_query(query)
    return jsonify({'url': url})

@app.route('/index', methods=['POST'])
def index():
    data = request.get_json()
    url = data.get('url', '')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    try:
        # Call your index_url function here
        result = index_url(url)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def run_flask():
    app.run(port=5000)

if __name__ == "__main__":
    # If run as main, start both the agent CLI and the Flask server in parallel
    threading.Thread(target=run_flask, daemon=True).start()
    query = input("🧑 What do you want to solve today? → ")
    asyncio.run(main(query))