import os
import json
from .evaluation import evaluate_code

def main():
    """
    The main game loop for AI Coder.
    """
    print("Welcome to AI Coder!")
    print("Your journey to becoming an AI expert starts now.")

    # Load tasks
    tasks = []
    task_files = sorted(os.listdir("ai_coder/tasks"))
    for task_file in task_files:
        with open(os.path.join("ai_coder/tasks", task_file)) as f:
            tasks.append(json.load(f))

    # Game loop
    for task in tasks:
        print(f"\n--- New Task: {task['title']} ---")
        print(task['description'])

        while True:
            print("Enter your code. Press Ctrl-D or type 'EOF' on a new line when you're done.")
            lines = []
            while True:
                try:
                    line = input()
                    if line == "EOF":
                        break
                    lines.append(line)
                except EOFError:
                    break
            player_code = "\n".join(lines)

            if not player_code:
                print("\nExiting game.")
                return

            stdout, stderr, returncode = evaluate_code(player_code)

            if returncode != 0:
                print(f"Error executing your code:\n{stderr}")
                print("Please try again.")
                continue

            if stdout == task["expected_output"]:
                print("Correct! You've completed the task.")
                break
            else:
                print(f"Incorrect. Expected:\n{task['expected_output']}\nGot:\n{stdout}")
                print("Please try again.")


    print("\nCongratulations, you've completed all available tasks!")

if __name__ == "__main__":
    main()