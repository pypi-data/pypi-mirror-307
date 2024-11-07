import argparse
import os
import time
import sys
from pathlib import Path
from .context_fetcher import ContextFetcher
import requests
import json

MAX_ITERATIONS = 3


class PathEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Path):
            return str(obj)  # Convert Path to string
        return super().default(obj)


def check_invite_code() -> str:
    """
    Check if TESTFORGE_INVITE environment variable is set.
    If not, display instructions and exit.

    Returns:
        str: The invite code if it exists
    """
    invite_code = os.getenv("TESTFORGE_INVITE")
    if not invite_code:
        print("\nError: TESTFORGE_INVITE environment variable is not set.")
        print("\nPlease set your invite code using the following command:")
        if sys.platform.startswith('win'):
            print('\nset TESTFORGE_INVITE=your-invite-code')
        else:
            print('\nexport TESTFORGE_INVITE=your-invite-code')
        print("\nIf you don't have an invite code, please visit https://testforge.ai to request one.")
        sys.exit(1)
    return invite_code


def create_progress_bar(current: int, total: int, bar_length: int = 50) -> str:
    """
    Create a progress bar string.

    Args:
        current: Current progress value
        total: Total value for 100% progress
        bar_length: Length of the progress bar in characters

    Returns:
        str: The progress bar string
    """
    progress = float(current) / float(total)
    filled_length = int(bar_length * progress)
    bar = "█" * filled_length + "░" * (bar_length - filled_length)
    return bar


def countdown(seconds: int):
    """
    Display a live countdown timer with progress bar in the terminal.

    Args:
        seconds: Number of seconds to count down from
    """
    start_time = time.time()

    for elapsed in range(seconds + 1):
        remaining = seconds - elapsed
        progress_bar = create_progress_bar(elapsed, seconds, 10)
        elapsed_time = time.strftime("%M:%S", time.gmtime(elapsed))
        remaining_time = time.strftime("%M:%S", time.gmtime(remaining))

        sys.stdout.write("\r")
        sys.stdout.write(
            f"Rate limit cooldown |{progress_bar}| {elapsed_time} elapsed / {remaining_time} remaining"
        )
        sys.stdout.flush()

        if elapsed < seconds:  # Don't sleep on the last iteration
            time.sleep(1)

    # Clear the line and move to the next
    sys.stdout.write("\n")
    sys.stdout.flush()


def get_unique_filename(base_path: Path, stem: str) -> Path:
    """
    Generate a unique filename by adding a number to the prefix if the file already exists.

    Args:
        base_path: The directory path
        stem: The stem of the input file

    Returns:
        Path: A unique file path
    """
    counter = 0
    while True:
        if counter == 0:
            filename = f"test_{stem}.py"
        else:
            filename = f"test_{stem}_{counter}.py"

        output_file = base_path / filename
        if not output_file.exists():
            return output_file
        counter += 1


def generate_beta_code(generated_code, request_context, invite_code):
    """
    Sends the generated_code and request_context to the API at "api.testforge.ai/betaGen"
    and returns the generatedCode and generationProgress from the response.

    Parameters:
    generated_code (str): The generated code to be sent to the API.
    request_context (dict): A dictionary containing the request context.
    invite_code (str): The invite code for API access.

    Returns:
    dict: A dictionary containing the generatedCode and generationProgress.
    """
    url = "https://ngeyc6mnb5llual4epm565u5wu0iqlwa.lambda-url.us-west-2.on.aws/"
    data = {
        "generatedCode": generated_code,
        "requestContext": request_context,
        "inviteCode": invite_code
    }
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, data=json.dumps(data, cls=PathEncoder), headers=headers)

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 401:
        print("\nError: Invalid invite code. Please check your TESTFORGE_INVITE environment variable.")
        sys.exit(1)
    else:
        raise Exception(f"Error calling API: {response.status_code} - {response.text}")


def generate_tests(input_file: str, target_function: str, output_dir: str) -> None:
    # Check for invite code first
    invite_code = check_invite_code()

    # Create output directory if it doesn't exist
    if not output_dir:
        output_dir = Path(input_file).parent
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    print(f"Analyzing project...")
    context_fetcher = ContextFetcher(project_path='.')

    if target_function:
        request_context = context_fetcher.get_function_info(input_file, target_function)
    else:
        request_context = context_fetcher.get_file_info(input_file)

    generated_code = ""
    generation_progress = "STARTING"
    i = 0
    print(f"Generating tests...")

    while generation_progress != "DONE" and i < MAX_ITERATIONS:
        try:
            response = generate_beta_code(generated_code, request_context, invite_code)
            i += 1
            generated_code += response['generatedCode']
            generation_progress = response['generationProgress']
            if generation_progress != "DONE":
                print("Rate limit reached waiting 60s before continuing...")
                countdown(60)
            print(f"{generation_progress}")
        except Exception as e:
            print(f"Error: {e}")
            return

    # Save the generated code to a file in the output directory
    output_file = get_unique_filename(Path(output_dir), Path(input_file).stem)
    with output_file.open("w") as f:
        f.write(generated_code)

    print(f"Generated tests saved to: {output_file}")


def main():
    parser = argparse.ArgumentParser(description="TestForge CLI Tool")
    parser.add_argument("-v", "--version",
                        action="store_true", help="Show version")
    parser.add_argument("-f", "--file", type=str,
                        help="File to generate test cases for")
    parser.add_argument("-t", "--target", type=str,
                        help="Target function to generate test cases for")
    parser.add_argument("-o", "--output", type=str, default=".",
                        help="Output location for generated tests")
    args = parser.parse_args()

    if args.version:
        print("TestForge version 1.0.4")
    elif args.file:
        generate_tests(args.file, args.target, args.output)
    else:
        parser.print_help()
