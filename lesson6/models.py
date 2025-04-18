from pydantic import BaseModel
from typing import List, Optional, Union, Dict, Any

# Input/Output models for basic math operations
class AddInput(BaseModel):
    a: int
    b: int

class AddOutput(BaseModel):
    result: int

class SqrtInput(BaseModel):
    a: int

class SqrtOutput(BaseModel):
    result: float

class SubtractInput(BaseModel):
    a: int
    b: int

class SubtractOutput(BaseModel):
    result: int

class MultiplyInput(BaseModel):
    a: int
    b: int

class MultiplyOutput(BaseModel):
    result: int

class DivideInput(BaseModel):
    a: int
    b: int

class DivideOutput(BaseModel):
    result: float

class PowerInput(BaseModel):
    a: int
    b: int

class PowerOutput(BaseModel):
    result: int

class CbrtInput(BaseModel):
    a: int

class CbrtOutput(BaseModel):
    result: float

class FactorialInput(BaseModel):
    a: int

class FactorialOutput(BaseModel):
    result: int

class LogInput(BaseModel):
    a: int

class LogOutput(BaseModel):
    result: float

class RemainderInput(BaseModel):
    a: int
    b: int

class RemainderOutput(BaseModel):
    result: int

class SinInput(BaseModel):
    a: int

class SinOutput(BaseModel):
    result: float

class CosInput(BaseModel):
    a: int

class CosOutput(BaseModel):
    result: float

class TanInput(BaseModel):
    a: int

class TanOutput(BaseModel):
    result: float

class MineInput(BaseModel):
    a: int
    b: int

class MineOutput(BaseModel):
    result: int

# Models for string and list operations
class StringsToIntsInput(BaseModel):
    string: str

class StringsToIntsOutput(BaseModel):
    ascii_values: List[int]

class ExpSumInput(BaseModel):
    int_list: List[int]

class ExpSumOutput(BaseModel):
    result: float

class FibonacciInput(BaseModel):
    n: int

class FibonacciOutput(BaseModel):
    sequence: List[int]

# Models for image and Paint operations
class TextResponse(BaseModel):
    type: str
    text: str

class CreateThumbnailInput(BaseModel):
    image_path: str

class CreateThumbnailOutput(BaseModel):
    data: bytes
    format: str

class DrawRectangleInput(BaseModel):
    x1: int
    y1: int
    x2: int
    y2: int

class DrawRectangleOutput(BaseModel):
    content: List[TextResponse]

class AddTextInput(BaseModel):
    x1: int
    y1: int
    x2: int
    y2: int
    text: str

class AddTextOutput(BaseModel):
    content: List[TextResponse]

class OpenPaintOutput(BaseModel):
    content: List[TextResponse]

class AddListInput(BaseModel):
    l: List[int]

class AddListOutput(BaseModel):
    result: int

class ToolDescription(BaseModel):
    name: str
    description: str
    input_schema: Dict[str, Any]

class AgentState(BaseModel):
    iteration: int
    last_response: Optional[Any]
    iteration_responses: List[str]
    max_iterations: int = 6

class LLMResponse(BaseModel):
    response_type: str  # "FUNCTION_CALL", "FINAL_ANSWER", "ERROR", "VERIFY"
    content: Dict[str, Any]

class ToolCall(BaseModel):
    function: str
    params: Dict[str, Any]

class ToolResult(BaseModel):
    success: bool
    result: Any
    error: Optional[str] = None

class AgentMemory(BaseModel):
    current_query: str
    tool_history: List[ToolCall]
    results_history: List[ToolResult]
    state: AgentState
