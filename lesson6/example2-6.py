# basic import 
from mcp.server.fastmcp import FastMCP, Image
from mcp.server.fastmcp.prompts import base
from mcp.types import TextContent
from mcp import types
from PIL import Image as PILImage
import math
import sys

from pywinauto.application import Application
import win32gui
import win32con
import time
from win32api import GetSystemMetrics
from models import (
    AddInput, AddOutput, AddListInput, AddListOutput,
    SubtractInput, SubtractOutput, MultiplyInput, MultiplyOutput,
    DivideInput, DivideOutput, PowerInput, PowerOutput,
    SqrtInput, SqrtOutput, CbrtInput, CbrtOutput,
    FactorialInput, FactorialOutput, LogInput, LogOutput,
    RemainderInput, RemainderOutput, SinInput, SinOutput,
    CosInput, CosOutput, TanInput, TanOutput, TextResponse,
    MineInput, MineOutput, StringsToIntsInput, StringsToIntsOutput,
    ExpSumInput, ExpSumOutput, FibonacciInput, FibonacciOutput,
    CreateThumbnailInput, CreateThumbnailOutput,
    DrawRectangleInput, DrawRectangleOutput,
    AddTextInput, AddTextOutput, OpenPaintOutput
)

# instantiate an MCP server client
mcp = FastMCP("Calculator")

# DEFINE TOOLS

#addition tool
@mcp.tool()
def add(input: AddInput) -> AddOutput:
    """Add two numbers together.
    
    Args:
        input (AddInput): Input model containing two integers to add
        
    Returns:
        AddOutput: Output model containing the sum of the two numbers
    """
    print("CALLED: add(AddInput) -> AddOutput")
    return AddOutput(result=int(input.a + input.b))

@mcp.tool()
def add_list(input: AddListInput) -> AddListOutput:
    """Calculate the sum of all numbers in a list.
    
    Args:
        input (AddListInput): Input model containing a list of integers to sum
        
    Returns:
        AddListOutput: Output model containing the sum of all numbers in the list
    """
    print("CALLED: add_list(AddListInput) -> AddListOutput")
    return AddListOutput(result=sum(input.l))

# subtraction tool
@mcp.tool()
def subtract(input: SubtractInput) -> SubtractOutput:
    """Subtract one number from another.
    
    Args:
        input (SubtractInput): Input model containing two integers to subtract
        
    Returns:
        SubtractOutput: Output model containing the difference between the two numbers
    """
    print("CALLED: subtract(a: int, b: int) -> int:")
    return SubtractOutput(result=int(input.a - input.b))

# multiplication tool
@mcp.tool()
def multiply(input: MultiplyInput) -> MultiplyOutput:
    """Multiply two numbers together.
    
    Args:
        input (MultiplyInput): Input model containing two integers to multiply
        
    Returns:
        MultiplyOutput: Output model containing the product of the two numbers
    """
    print("CALLED: multiply(a: int, b: int) -> int:")
    return MultiplyOutput(result=int(input.a * input.b))

#  division tool
@mcp.tool() 
def divide(input: DivideInput) -> DivideOutput:
    """Divide one number by another.
    
    Args:
        input (DivideInput): Input model containing two integers to divide
        
    Returns:
        DivideOutput: Output model containing the quotient of the division
    """
    print("CALLED: divide(a: int, b: int) -> float:")
    return DivideOutput(result=float(input.a / input.b))

# power tool
@mcp.tool()
def power(input: PowerInput) -> PowerOutput:
    """Calculate the power of a number.
    
    Args:
        input (PowerInput): Input model containing base and exponent integers
        
    Returns:
        PowerOutput: Output model containing the result of base raised to the exponent
    """
    print("CALLED: power(a: int, b: int) -> int:")
    return PowerOutput(result=int(input.a ** input.b))

# square root tool
@mcp.tool()
def sqrt(input: SqrtInput) -> SqrtOutput:
    """Calculate the square root of a number.
    
    Args:
        input (SqrtInput): Input model containing the number to calculate square root of
        
    Returns:
        SqrtOutput: Output model containing the square root of the input number
    """
    print("CALLED: sqrt(a: int) -> float:")
    return SqrtOutput(result=float(input.a ** 0.5))

# cube root tool
@mcp.tool()
def cbrt(input: CbrtInput) -> CbrtOutput:
    """Calculate the cube root of a number.
    
    Args:
        input (CbrtInput): Input model containing the number to calculate cube root of
        
    Returns:
        CbrtOutput: Output model containing the cube root of the input number
    """
    print("CALLED: cbrt(a: int) -> float:")
    return CbrtOutput(result=float(input.a ** (1/3)))

# factorial tool
@mcp.tool()
def factorial(input: FactorialInput) -> FactorialOutput:
    """Calculate the factorial of a number.
    
    Args:
        input (FactorialInput): Input model containing the number to calculate factorial of
        
    Returns:
        FactorialOutput: Output model containing the factorial of the input number
    """
    print("CALLED: factorial(a: int) -> int:")
    return FactorialOutput(result=int(math.factorial(input.a)))

# log tool
@mcp.tool()
def log(input: LogInput) -> LogOutput:
    """Calculate the natural logarithm of a number.
    
    Args:
        input (LogInput): Input model containing the number to calculate logarithm of
        
    Returns:
        LogOutput: Output model containing the natural logarithm of the input number
    """
    print("CALLED: log(a: int) -> float:")
    return LogOutput(result=float(math.log(input.a)))

# remainder tool
@mcp.tool()
def remainder(input: RemainderInput) -> RemainderOutput:
    """Calculate the remainder of division between two numbers.
    
    Args:
        input (RemainderInput): Input model containing dividend and divisor integers
        
    Returns:
        RemainderOutput: Output model containing the remainder of the division
    """
    print("CALLED: remainder(a: int, b: int) -> int:")
    return RemainderOutput(result=int(input.a % input.b))

# sin tool
@mcp.tool()
def sin(input: SinInput) -> SinOutput:
    """Calculate the sine of a number.
    
    Args:
        input (SinInput): Input model containing the number to calculate sine of
        
    Returns:
        SinOutput: Output model containing the sine of the input number
    """
    print("CALLED: sin(a: int) -> float:")
    return SinOutput(result=float(math.sin(input.a)))

# cos tool
@mcp.tool()
def cos(input: CosInput) -> CosOutput:
    """Calculate the cosine of a number.
    
    Args:
        input (CosInput): Input model containing the number to calculate cosine of
        
    Returns:
        CosOutput: Output model containing the cosine of the input number
    """
    print("CALLED: cos(a: int) -> float:")
    return CosOutput(result=float(math.cos(input.a)))

# tan tool
@mcp.tool()
def tan(input: TanInput) -> TanOutput:
    """Calculate the tangent of a number.
    
    Args:
        input (TanInput): Input model containing the number to calculate tangent of
        
    Returns:
        TanOutput: Output model containing the tangent of the input number
    """
    print("CALLED: tan(a: int) -> float:")
    return TanOutput(result=float(math.tan(input.a)))

# mine tool
@mcp.tool()
def mine(input: MineInput) -> MineOutput:
    """Perform a special mining calculation.
    
    Args:
        input (MineInput): Input model containing two integers for the mining calculation
        
    Returns:
        MineOutput: Output model containing the result of the mining calculation
    """
    print("CALLED: mine(a: int, b: int) -> int:")
    return MineOutput(result=int(input.a - input.b - input.b))

@mcp.tool()
def create_thumbnail(input: CreateThumbnailInput) -> CreateThumbnailOutput:
    """Create a thumbnail image from a source image.
    
    Args:
        input (CreateThumbnailInput): Input model containing the path to the source image
        
    Returns:
        CreateThumbnailOutput: Output model containing the thumbnail image data and format
    """
    print("CALLED: create_thumbnail(image_path: str) -> Image:")
    img = PILImage.open(input.image_path)
    img.thumbnail((100, 100))
    return CreateThumbnailOutput(data=img.tobytes(), format="png")

@mcp.tool()
def strings_to_chars_to_int(input: StringsToIntsInput) -> StringsToIntsOutput:
    """Convert a string to a list of ASCII values.
    
    Args:
        input (StringsToIntsInput): Input model containing the string to convert
        
    Returns:
        StringsToIntsOutput: Output model containing the list of ASCII values
    """
    print("CALLED: strings_to_chars_to_int(StringsToIntsInput) -> StringsToIntsOutput:")
    return StringsToIntsOutput(ascii_values=[int(ord(char)) for char in input.string])

@mcp.tool()
def int_list_to_exponential_sum(input: ExpSumInput) -> ExpSumOutput:
    """Calculate the sum of exponentials of numbers in a list.
    
    Args:
        input (ExpSumInput): Input model containing the list of numbers
        
    Returns:
        ExpSumOutput: Output model containing the sum of exponentials
    """
    print("CALLED: int_list_to_exponential_sum(ExpSumInput) -> ExpSumOutput:")
    return ExpSumOutput(result=sum(math.exp(i) for i in input.int_list))

@mcp.tool()
def fibonacci_numbers(input: FibonacciInput) -> FibonacciOutput:
    """Generate the first n Fibonacci numbers.
    
    Args:
        input (FibonacciInput): Input model containing the number of Fibonacci numbers to generate
        
    Returns:
        FibonacciOutput: Output model containing the sequence of Fibonacci numbers
    """
    print("CALLED: fibonacci_numbers(FibonacciInput) -> FibonacciOutput:")
    if input.n <= 0:
        return FibonacciOutput(sequence=[])
    fib_sequence = [0, 1]
    for _ in range(2, input.n):
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return FibonacciOutput(sequence=fib_sequence[:input.n])


@mcp.tool()
async def draw_rectangle(input: DrawRectangleInput) -> DrawRectangleOutput:
    """Draw a rectangle in Microsoft Paint.
    
    Args:
        input (DrawRectangleInput): Input model containing the rectangle coordinates
        
    Returns:
        DrawRectangleOutput: Output model containing the operation status message
        
    Note:
        Requires Paint to be open. Call open_paint() first if Paint is not open.
        make sure to pass x1 higher than 250
    """
    global paint_app
    try:
        if not paint_app:
            return DrawRectangleOutput(
                content=[
                    TextResponse(
                        type="text",
                        text="Paint is not open. Please call open_paint first."
                    )
                ]
            )
        
        # Get the Paint window
        paint_window = paint_app.window(class_name='MSPaintApp')
        
        # Get primary monitor width to adjust coordinates
        primary_width = GetSystemMetrics(0)
        
        # Ensure Paint window is active
        if not paint_window.has_focus():
            paint_window.set_focus()
            time.sleep(0.2)
        
        # Click on the Rectangle tool using the correct coordinates for secondary screen
        paint_window.click_input(coords=(445, 72))
        time.sleep(0.2)
        
        # Get the canvas area
        canvas = paint_window.child_window(class_name='MSPaintView')
        
        # Draw rectangle
        canvas.press_mouse_input(coords=(input.x1+primary_width, input.y1))
        canvas.move_mouse_input(coords=(input.x2+primary_width, input.y2))
        canvas.release_mouse_input(coords=(input.x2+primary_width, input.y2))
        
        return DrawRectangleOutput(
            content=[
                TextResponse(
                    type="text",
                    text=f"Rectangle drawn from ({input.x1},{input.y1}) to ({input.x2},{input.y2})"
                )
            ]
        )
    except Exception as e:
        return DrawRectangleOutput(
            content=[
                TextResponse(
                    type="text",
                    text=f"Error drawing rectangle: {str(e)}"
                )
            ]
        )

@mcp.tool()
async def add_text_in_paint(input: AddTextInput) -> AddTextOutput:
    """Draw a text box in Paint from (x1,y1) to (x2,y2), Add text in Paint
    
    Args:
        input (AddTextInput): Input model containing (x1, y1), (x2,y2), the text to add
        
    Returns:
        AddTextOutput: Output model containing the operation status message
        
    Note:
        Requires Paint to be open. Call open_paint() first if Paint is not open.
    """
    global paint_app
    try:
        if not paint_app:
            return AddTextOutput(
                content=[
                    TextResponse(
                        type="text",
                        text="Paint is not open. Please call open_paint first."
                    )
                ]
            )
        
        # Get the Paint window
        paint_window = paint_app.window(class_name='MSPaintApp')
        
        # Ensure Paint window is active
        if not paint_window.has_focus():
            paint_window.set_focus()
            time.sleep(0.5)
        
        # Get primary monitor width to adjust coordinates
        primary_width = GetSystemMetrics(0)

        # Click on the text tool
        paint_window.click_input(coords=(290, 72))
        time.sleep(0.2)
        
        # Get the canvas area
        canvas = paint_window.child_window(class_name='MSPaintView')
        
        # Click where to start typing
        # canvas.click_input(coords=(645+primary_width, 435))
        x1, y1 = input.x1, input.y1
        x2, y2 = input.x2, input.y2
        canvas.press_mouse_input(coords=(x1+primary_width, y1))
        canvas.move_mouse_input(coords=(x2+primary_width, y2))
        canvas.release_mouse_input(coords=(x2+primary_width, y2))
        # canvas.click_input(coords=(645+primary_width, 435))
        time.sleep(0.2)
        
        # Type the text passed from client
        paint_window.type_keys(input.text)
        time.sleep(0.2)
        
        # Click to exit text mode
        canvas.click_input(coords=(625+primary_width, 415))
        
        return AddTextOutput(
            content=[
                TextResponse(
                    type="text",
                    text=f"Text:'{input.text}' added successfully"
                )
            ]
        )
    except Exception as e:
        return AddTextOutput(
            content=[
                TextResponse(
                    type="text",
                    text=f"Error: {str(e)}"
                )
            ]
        )

@mcp.tool()
async def open_paint() -> OpenPaintOutput:
    """Open Microsoft Paint maximized on secondary monitor.
    
    Returns:
        OpenPaintOutput: Output model containing the operation status message
    """
    global paint_app
    try:
        paint_app = Application().start('mspaint.exe')
        time.sleep(0.2)
        
        # Get the Paint window
        paint_window = paint_app.window(class_name='MSPaintApp')
        
        # Get primary monitor width
        primary_width = GetSystemMetrics(0)
        
        # First move to secondary monitor without specifying size
        win32gui.SetWindowPos(
            paint_window.handle,
            win32con.HWND_TOP,
            primary_width + 1, 0,  # Position it on secondary monitor
            0, 0,  # Let Windows handle the size
            win32con.SWP_NOSIZE  # Don't change the size
        )
        
        # Now maximize the window
        win32gui.ShowWindow(paint_window.handle, win32con.SW_MAXIMIZE)
        time.sleep(0.2)
        
        return OpenPaintOutput(
            content=[
                TextResponse(
                    type="text",
                    text="Paint opened successfully on secondary monitor and maximized"
                )
            ]
        )
    except Exception as e:
        return OpenPaintOutput(
            content=[
                TextResponse(
                    type="text",
                    text=f"Error opening Paint: {str(e)}"
                )
            ]
        )

# DEFINE RESOURCES

# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    print("CALLED: get_greeting(name: str) -> str:")
    return f"Hello, {name}!"


# DEFINE AVAILABLE PROMPTS
@mcp.prompt()
def review_code(code: str) -> str:
    return f"Please review this code:\n\n{code}"
    print("CALLED: review_code(code: str) -> str:")


@mcp.prompt()
def debug_error(error: str) -> list[base.Message]:
    return [
        base.UserMessage("I'm seeing this error:"),
        base.UserMessage(error),
        base.AssistantMessage("I'll help debug that. What have you tried so far?"),
    ]

if __name__ == "__main__":
    # Check if running with mcp dev command
    print("STARTING")
    if len(sys.argv) > 1 and sys.argv[1] == "dev":
        mcp.run()  # Run without transport for dev server
    else:
        mcp.run(transport="stdio")  # Run with stdio for direct execution
