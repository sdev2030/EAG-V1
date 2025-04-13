# Lesson 5: Advanced Tool Integration and Automation

This lesson focuses on advanced tool integration and automation using the MCP (Model Control Protocol) framework. The project demonstrates how to create and use various tools for mathematical calculations, image processing, and system automation.

## Project Structure

- `main.py` - Entry point for the lesson
- `example2-3.py` - Main implementation file containing tool definitions and examples
- `talk2mcp-2.py` - Additional examples and tool usage demonstrations
- `pyproject.toml` - Project configuration and dependencies
- `.env` - Environment variables configuration
- `.python-version` - Python version specification

## Available Tools

The project implements a comprehensive set of tools for various operations:

### Mathematical Operations
- Basic arithmetic: `add`, `subtract`, `multiply`, `divide`
- Advanced math: `power`, `sqrt`, `cbrt`, `factorial`, `log`
- Trigonometry: `sin`, `cos`, `tan`
- List operations: `add_list`, `int_list_to_exponential_sum`
- Special operations: `remainder`, `mine`

### Image Processing
- `create_thumbnail` - Create image thumbnails
- `draw_rectangle` - Draw rectangles in Paint
- `add_text_in_paint` - Add text to Paint
- `open_paint` - Open Microsoft Paint

### String and Data Processing
- `strings_to_chars_to_int` - Convert strings to ASCII values
- `fibonacci_numbers` - Generate Fibonacci sequences

## Requirements

- Python >= 3.13
- Dependencies specified in `pyproject.toml`
- Windows environment (for Paint automation features)

## Getting Started

1. Ensure you have the required Python version installed
2. Install dependencies:
   ```bash
   pip install -e .
   ```
3. Configure your `.env` file with necessary environment variables
4. Run the examples:
   ```bash
   python main.py
   ```

## Features

- Mathematical tool integration
- Image processing capabilities
- System automation (Paint integration)
- String and data manipulation tools
- Error handling and debugging support

## Usage Examples

The project includes several example files demonstrating tool usage:
- `example2-3.py` - Core tool implementations
- `talk2mcp-2.py` - Advanced usage examples

## Notes

- Some features require Windows-specific libraries
- Image processing tools require PIL (Python Imaging Library)
- System automation features use pywinauto and win32gui
