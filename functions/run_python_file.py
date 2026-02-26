import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    try:
        # Get absolute paths
        working_directory = os.path.abspath(working_directory)
        absolute_file_path = os.path.abspath(
            os.path.join(working_directory, file_path)
        )

        # Check if file is outside working directory
        if os.path.commonpath([working_directory, absolute_file_path]) != working_directory:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # Check that it exists and is a regular file
        if not os.path.isfile(absolute_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        # Check file extension
        if not absolute_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        # Build command
        command = ["python", absolute_file_path]
        if args:
            command.extend(args)

        # Run subprocess
        result = subprocess.run(
            command,
            cwd=working_directory,
            capture_output=True,
            text=True,
            timeout=30
        )

        output = ""

        if result.returncode != 0:
            output += f"Process exited with code {result.returncode}\n"

        if not result.stdout and not result.stderr:
            output += "No output produced"
        else:
            if result.stdout:
                output += f"STDOUT: {result.stdout}"
            if result.stderr:
                output += f"STDERR: {result.stderr}"

        return output.strip()

    except Exception as e:
        return f"Error: executing Python file: {e}"