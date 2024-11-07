import subprocess
import openai
from openai import OpenAI


def get_suggestions(changes, api_key):
    client = OpenAI(api_key=api_key)
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful developer assistant. "
                    "Your answers should be very brief."
                    "You are helping with QA work, you will be given a git diff"
                    "and you should look at all the changes made and recommend"
                    "mannual testing steps that the reviewer can use to test the"
                    "changes made and be confident that all new changes are working"
                )
            },
            {
                "role": "user",
                "content": changes
            }
        ]
    )
    return completion.choices[0].message.content


def test(a):
    return a*5


def main(api_key, branch='master'):

    # Get the diff from the current branch to master
    try:
        diff_output = subprocess.check_output(
            ['git', 'diff', branch], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        print("An error occurred while running git diff:")
        print(e.output.decode())
        return

    changes = diff_output.decode('utf-8')

    # If the diff is empty, inform the user
    if not changes.strip():
        print(f"No changes detected between the current branch and {branch}")
        return

    # Get suggestions based on the changes
    suggestions = get_suggestions(changes, api_key)

    # If suggestions were returned, print them
    if suggestions:
        print("Suggested Manual Testing Steps:\n")
        print(suggestions)
    else:
        print("Failed to generate suggestions.")
