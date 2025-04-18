from mcp import ClientSession
from models import ToolCall, ToolResult

class Action:
    def __init__(self, session: ClientSession):
        self.session = session
    
    async def execute_tool(self, tool_call: ToolCall) -> ToolResult:
        """Execute a tool call and return the result"""
        try:
            result = await self.session.call_tool(
                tool_call.function,
                arguments=tool_call.params
            )
            print(f"tool result: {result}")
            # Process the result
            if hasattr(result, 'content'):
                if isinstance(result.content, list):
                    processed_result = [
                        item.text if hasattr(item, 'text') else str(item)
                        for item in result.content
                    ]
                else:
                    processed_result = str(result.content)
            else:
                processed_result = str(result)
            
            return ToolResult(
                success=True,
                result=processed_result
            )
            
        except Exception as e:
            return ToolResult(
                success=False,
                result=None,
                error=str(e)
            )