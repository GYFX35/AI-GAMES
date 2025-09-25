import subprocess

def evaluate_code(code: str) -> tuple[str, str, int]:
    """
    Executes a string of Python code and captures its output.

    Args:
        code: The Python code to execute.

    Returns:
        A tuple containing stdout, stderr, and the return code.
    """
    try:
        process = subprocess.run(
            ['python', '-c', code],
            capture_output=True,
            text=True,
            timeout=5  # Add a timeout for safety
        )
        return process.stdout, process.stderr, process.returncode
    except subprocess.TimeoutExpired:
        return "", "Error: Code execution timed out.", 1