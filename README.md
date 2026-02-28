# AI-Powered Command-Line Agent

An intelligent command-line agent built in Python that leverages the Google Gemini API to execute dynamic tasks. This agent can read files, list directories, execute Python code, write files, and intelligently call functions based on natural language commands.

## Features

- **Natural Language Interface**: Communicate with the agent using plain English commands
- **File Operations**: Read, write, and manage files within the working directory
- **Directory Management**: List and explore directory contents
- **Python Execution**: Safely execute Python scripts with sandboxed execution
- **Dynamic Tool Calling**: Use Gemini's function-calling capabilities to execute tasks intelligently
- **Verbose Mode**: Optional detailed logging for debugging and transparency
- **Security**: All operations are restricted to a designated working directory for safety

## How It Works

The agent operates on a continuous loop that:

1. **Accepts User Input**: Takes natural language commands from the user
2. **Sends to Gemini**: Forwards the request to Google's Gemini 2.5 Flash model
3. **Tool Selection**: Gemini analyzes the request and decides which tools to use
4. **Function Execution**: The agent executes the selected tools (file read, directory list, code execution, etc.)
5. **Response Generation**: Gemini synthesizes the results and provides a natural language response
6. **Loop Continuation**: The process repeats until the user exits

The agent uses predefined tool schemas that Gemini can call, including:
- `read_file`: Read the contents of a file
- `list_directory`: List files and folders in a directory
- `execute_python`: Run Python code safely
- `write_file`: Create or modify files

## Installation

### Prerequisites

- Python 3.7 or higher
- `uv` package manager (recommended) or `pip`

### Steps

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd aiagent
   ```

2. **Create a virtual environment**:
   ```bash
   uv venv
   ```

3. **Activate the virtual environment**:
   - On macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```
   - On Windows:
     ```bash
     .venv\Scripts\activate
     ```

4. **Install dependencies**:
   ```bash
   uv pip install -r requirements.txt
   ```

## Setup

### Environment Configuration

1. **Create a `.env` file** in the project root directory:
   ```bash
   touch .env
   ```

2. **Add your Gemini API key** to the `.env` file:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

   **How to obtain a Gemini API key**:
   - Visit [Google AI Studio](https://aistudio.google.com)
   - Sign in with your Google account
   - Click on "Get API key" in the left sidebar
   - Create a new API key and copy it
   - Paste it into your `.env` file

3. **Protect your `.env` file** by adding it to `.gitignore`:
   ```
   echo ".env" >> .gitignore
   ```
   
   ⚠️ **Important**: Never commit your `.env` file to version control. Your API key is sensitive and should be kept private.

## Usage

### Basic Commands

Run the agent with a command:

```bash
uv run main.py "your command here"
```

### Examples

**List files in the root directory**:
```bash
uv run main.py "what files are in the root?"
```

**Execute a Python file**:
```bash
uv run main.py "run tests.py"
```

**Execute with verbose output**:
```bash
uv run main.py "run tests.py" --verbose
```

### Verbose Mode

The `--verbose` flag enables detailed logging that shows:
- The exact requests sent to Gemini
- Tool selection and invocation details
- Raw API responses
- Step-by-step execution flow

This is useful for debugging and understanding how the agent processes your commands.

```bash
uv run main.py "command" --verbose
```

## Project Structure

```
aiagent/
├── main.py                 # Main agent loop and entry point
├── tool_schemas.py         # Tool definitions for Gemini
├── function_handlers.py    # Implementation of tool functions
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not committed)
├── .gitignore             # Git ignore file
├── calculator/            # Working directory for safe execution
│   ├── __init__.py
│   └── tests.py           # Example test file
└── README.md              # This file
```

## Security

All file operations and code execution are **restricted to the `./calculator` working directory**. This sandboxing prevents accidental or malicious operations outside the intended scope:

- File reads are limited to `./calculator/`
- File writes create/modify files only in `./calculator/`
- Python execution runs within the `./calculator/` context
- Directory listings show only contents of `./calculator/`

**Do not run untrusted code** through this agent, as it has access to execute arbitrary Python within its working directory.

## Future Improvements

- [ ] Add support for more complex data types and structured outputs
- [ ] Implement conversation memory for multi-turn interactions
- [ ] Add rate limiting and API quota management
- [ ] Support for custom tool definitions
- [ ] Web interface for easier interaction
- [ ] Integration with other AI models
- [ ] Enhanced error handling and recovery
- [ ] Logging to persistent storage
- [ ] Unit tests and integration tests
- [ ] Docker containerization for isolated execution

## License

This project is part of a Boot.dev guided project and is provided as educational material.

