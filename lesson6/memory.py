from models import AgentState, ToolCall, ToolResult, AgentMemory
from typing import Optional

class Memory:
    def __init__(self):
        self.state = AgentState(
            iteration=0,
            last_response=None,
            iteration_responses=[],
            max_iterations=6
        )
        self.memory = AgentMemory(
            current_query="",
            tool_history=[],
            results_history=[],
            state=self.state
        )
    
    def update_state(self, tool_call: Optional[ToolCall] = None, tool_result: Optional[ToolResult] = None):
        if tool_call:
            self.memory.tool_history.append(tool_call)
        if tool_result:
            self.memory.results_history.append(tool_result)
            self.state.last_response = tool_result.result
            self.state.iteration_responses.append(
                f"In the {self.state.iteration + 1} iteration you called {tool_call.function} "
                f"with {tool_call.params} parameters, and the function returned {tool_result.result}."
            )
        self.state.iteration += 1
    
    def reset(self):
        self.__init__()
    
    def get_context_for_llm(self) -> str:
        if not self.state.iteration_responses:
            return self.memory.current_query
        return (
            f"{self.memory.current_query}\n\n"
            f"{' '.join(self.state.iteration_responses)}\n"
            f"What should I do next?"
        )