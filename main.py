import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse

load_dotenv()
# Set up argument parser to accept user prompt from command line
parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

user_prompt = args.user_prompt

# Retrieve the Gemini API key from environment variables
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in the environment variables.")

# Initialize the Gemini API client
client = genai.Client(api_key=api_key)


# Create a list of messages with the user prompt
messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]


# Generate content using the Gemini API
response = client.models.generate_content(
    model='gemini-2.5-flash', contents=messages
    )


#checl if response contains usage metadata
if response.usage_metadata is None:
    raise ValueError("Response does not contain usage metadata.")


#extract prompt and response tokens from usage metadata
prompt_tokens = response.usage_metadata.prompt_token_count
response_tokens = response.usage_metadata.candidates_token_count


# Verbose output
if args.verbose:
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {response_tokens}")
    
           
#print the response text
print(response.text)


def main():
    pass
    


if __name__ == "__main__":
    main()
