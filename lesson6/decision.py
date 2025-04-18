from models import LLMResponse, ToolCall, ToolDescription
from typing import List, Optional

class Decision:
    def __init__(self, tools: List[ToolDescription]):
        self.tools = {tool.name: tool for tool in tools}
    
    def validate_tool_call(self, tool_call: ToolCall) -> Optional[str]:
        """Validate if a tool call is valid based on tool descriptions"""
        if tool_call.function not in self.tools:
            return f"Unknown tool: {tool_call.function}"
            
        tool = self.tools[tool_call.function]
        # Validate parameters against schema
        required_params = {
            k for k, v in tool.input_schema.get("properties", {}).items()
            if "required" in tool.input_schema and k in tool.input_schema["required"]
        }
        
        if not all(param in tool_call.params for param in required_params):
            return f"Missing required parameters: {required_params - set(tool_call.params.keys())}"
        
        return None
    
    def process_llm_response(self, response: LLMResponse) -> Optional[ToolCall]:
        """Process LLM response and return tool call if valid"""
        if response.response_type == "FUNCTION_CALL":
            # Extract function name and parameters
            if "function" not in response.content:
                raise ValueError("Function call must contain 'function' field")
            if "params" not in response.content:
                # For functions without parameters, provide an empty params object
                tool_call = ToolCall(
                    function=response.content["function"],
                    params={}
                )
            else:
                tool_call = ToolCall(**response.content)
            
            error = self.validate_tool_call(tool_call)
            if error:
                raise ValueError(error)
            return tool_call
        elif response.response_type == "FINAL_ANSWER":
            # Verify final answer format
            if "final_answer" not in response.content:
                raise ValueError("Final answer must contain 'final_answer' field")
            return None
        elif response.response_type == "ERROR":
            # Just log the error and return None, let main.py handle it
            print(f"LLM reported an error: {response.content.get('type')}: {response.content.get('details')}")
            return None
        elif response.response_type == "VERIFY":
            # Verify the verification format
            if "expected" not in response.content or "actual" not in response.content:
                raise ValueError("Verification must contain 'expected' and 'actual' fields")
            return None
        else:
            raise ValueError(f"Unknown response type: {response.response_type}")
    
    def format_tools_description(self) -> str:
        """Format tool descriptions for the system prompt"""
        tools_description = []
        for i, (name, tool) in enumerate(self.tools.items()):
            try:
                # Format the input schema in a readable way
                if 'properties' in tool.input_schema:
                    param_details = []
                    for param_name, param_info in tool.input_schema['properties'].items():
                        param_type = param_info.get('type', 'unknown')
                        param_details.append(f"{param_name}: {param_type}")
                    params_str = ', '.join(param_details)
                else:
                    params_str = 'no parameters'

                tool_desc = f"{i+1}. {name}({params_str}) - {tool.description}"
                tools_description.append(tool_desc)
            except Exception as e:
                tools_description.append(f"{i+1}. Error processing tool {name}")
        
        return "\n".join(tools_description)