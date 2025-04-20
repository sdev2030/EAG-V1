import asyncio
import json
from google import genai
from pydantic import BaseModel
from typing import Optional
from models import LLMResponse, AgentState

class Perception:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.system_prompt = None
    
    def create_system_prompt(self, tools_description: str, user_preference: str):
        """Create the system prompt using tool descriptions"""
        self.system_prompt = f"""You are a math agent solving problems in iterations. You have access to various mathematical tools.

REASONING PROCESS:
1. ALWAYS think step-by-step before making any function calls
2. Break down complex problems into simpler sub-problems
3. For each step, explicitly state your reasoning BEFORE selecting a tool
4. After each function call, verify the result makes sense by checking:
   - Is the output within expected ranges?
   - Does it match simple mental calculations?
   - Are units and dimensions consistent?
5. If a verification fails, reconsider your approach and try again
6. Tag each reasoning step with [REASONING] and each verification step with [VERIFICATION]

{tools_description}

You must respond with EXACTLY ONE line in one of these formats (no additional text):
1. For function calls:
   FUNCTION_CALL: {{"function": "function_name", "params": {{"input": {{EXACT_FIELD_NAMES_FROM_MODEL: values}}}}}}
   Or for functions without input parameters:
   FUNCTION_CALL: {{"function": "function_name", "params": {{}}}}

2. For final answers:
   FINAL_ANSWER: {{"final_answer": 42}}

3. For errors or verification:
   ERROR: {{"type": "error_type", "details": "error_details"}}
   VERIFY: {{"expected": expected_value, "actual": actual_value}}

CRITICAL:
- You MUST use the EXACT field names from the tool descriptions
- For example, if a tool requires "int_list", you must use "int_list" not "numbers" or other variations
- Some tools like "open_paint" don't take any parameters, use empty params for them
- Always perform self-verification checks after each computation
- If uncertain about a result, recalculate or use alternative methods to confirm

IMPORTANT JSON FORMATTING RULES:
- Always use double quotes for property names and string values
- Arrays use square brackets: [1, 2, 3]
- Boolean values are lowercase: true, false
- No trailing commas

CRITICAL TOOL USAGE:
- Use exact field names from tool descriptions
- For open_paint use: FUNCTION_CALL: {{"function": "open_paint", "params": {{}}}}
- If a tool fails, report the error and try an alternative approach
- {user_preference}

Examples:
- FUNCTION_CALL: {{"function": "add", "params": {{"input": {{"a": 5, "b": 3}}}}}}
- FUNCTION_CALL: {{"function": "strings_to_chars_to_int", "params": {{"input": {{"string": "INDIA"}}}}}}
- FUNCTION_CALL: {{"function": "int_list_to_exponential_sum", "params": {{"input": {{"int_list": [1, 2, 3, 4, 5]}}}}}}
- FUNCTION_CALL: {{"function": "open_paint", "params": {{}}}}
- FUNCTION_CALL: {{"function": "draw_rectangle", "params": {{"input": {{"x1": 100, "y1": 100, "x2": 200, "y2": 200}}}}}}
- FUNCTION_CALL: {{"function": "add_text_in_paint", "params": {{"input": {{"text": "Hello World!"}}}}}}
- FINAL_ANSWER: {{"final_answer": 42}}
- ERROR: {{"type": "tool_execution_error", "details": "Error message here"}}"""
    
    async def generate_with_timeout(self, user_query: str, timeout: int = 10) -> LLMResponse:
        """Generate content with a timeout using Gemini"""
        if not self.system_prompt:
            raise ValueError("System prompt not initialized")
            
        prompt = f"{self.system_prompt}\n\nQuery: {user_query}"
        
        try:
            loop = asyncio.get_event_loop()
            response = await asyncio.wait_for(
                loop.run_in_executor(
                    None,
                    lambda: self.client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=prompt
                    )
                ),
                timeout=timeout
            )
            
            # Parse the response into structured format
            response_text = response.text.strip()
            print(f"Raw LLM response: {response_text}")  # Add debugging
            
            # Parse response type and content
            for line in response_text.split('\n'):
                line = line.strip()
                if line.startswith(("FUNCTION_CALL:", "FINAL_ANSWER:", "ERROR:", "VERIFY:")):
                    response_type, content = line.split(':', 1)
                    content = content.strip()
                    try:
                        parsed_content = json.loads(content)
                        return LLMResponse(
                            response_type=response_type,
                            content=parsed_content
                        )
                    except json.JSONDecodeError as e:
                        print(f"JSON parsing error: {e}")
                        print(f"Content that failed to parse: {content}")
                        raise ValueError(f"Invalid JSON in LLM response: {e}")
            
            raise ValueError("No valid response format found")
            
        except asyncio.TimeoutError:
            raise TimeoutError("LLM generation timed out")