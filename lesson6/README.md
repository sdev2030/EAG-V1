# Math Agent with Tool Usage

This project implements a mathematical agent that can solve complex problems by sequentially using various tools. The agent follows a perception-memory-decision-action loop to solve mathematical problems.

## Project Structure

- **main.py**: Entry point for the application that initializes the components and runs the main loop
- **perception.py**: Handles interactions with the LLM (using Gemini API) to generate responses
- **memory.py**: Manages the agent's state and context across iterations
- **decision.py**: Processes LLM responses and validates tool calls
- **action.py**: Executes tool calls and processes their results
- **models.py**: Contains Pydantic models for all inputs, outputs, and internal structures
- **example2-6.py**: Implements various mathematical and utility tools using FastMCP

## Tools Available

The agent has access to a wide range of mathematical tools:

1. Basic arithmetic: add, subtract, multiply, divide
2. Advanced operations: power, sqrt, cbrt, factorial, log, remainder
3. Trigonometric functions: sin, cos, tan
4. List operations: add_list, int_list_to_exponential_sum
5. String operations: strings_to_chars_to_int
6. Sequence generation: fibonacci_numbers
7. Visual tools: create_thumbnail, open_paint, draw_rectangle, add_text_in_paint

## Architecture

The system follows a modular architecture with four main components:

1. **Perception**: Interacts with the LLM to generate responses based on queries and context
2. **Memory**: Maintains the state of the agent, including iteration count and history
3. **Decision**: Validates and processes LLM responses to create executable tool calls
4. **Action**: Executes tool calls and processes their results

## Installation

1. Create a virtual environment: `python -m venv .venv`
2. Activate the environment: 
   - Windows: `.venv\Scripts\activate`
   - Unix/macOS: `source .venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt` (or use the provided `pyproject.toml`)
4. Create a `.env` file with your Gemini API key: `GEMINI_API_KEY=your_api_key_here`

## Usage

Run the application with:

```bash
python main.py
```

The agent will attempt to solve the problem by iteratively using tools based on the LLM's guidance.

## Example Query

The default query is:
"Find the ASCII values of characters in INDIA and then return sum of exponentials of those values"

The agent will:
1. Convert "INDIA" to ASCII values using `strings_to_chars_to_int`
2. Calculate the sum of exponentials of these values using `int_list_to_exponential_sum`
3. Return the final answer

## Development

- `pyproject.toml`: Defines project dependencies
- `.python-version`: Specifies the Python version for the project
