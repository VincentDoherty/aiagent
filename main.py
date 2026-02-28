import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from prompts import system_prompt
from functions.call_function import available_functions, call_function

def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set in the environment variables.")

    client = genai.Client(api_key=api_key)

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    for _ in range(20):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt,
            ),
        )

        if not response.candidates:
            print("No candidates returned by the model.")
            sys.exit(1)

        # Optional: verbose token info per model call
        if args.verbose:
            if response.usage_metadata is None:
                raise ValueError("Response does not contain usage metadata.")
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        # Add all candidates to history
        for candidate in response.candidates:
            if candidate.content is not None:
                messages.append(candidate.content)

        function_calls = response.function_calls
        
        if function_calls:
            for fc in function_calls:
                print(f"Calling function: {fc.name}({fc.args})")

        # Final answer case
        if not function_calls:
            if response.text:
                print(response.text)
            break

        # Execute function calls and collect parts
        function_responses = []
        for function_call_obj in function_calls:
            function_call_result = call_function(function_call_obj.name, function_call_obj.args)

            if not function_call_result.parts:
                raise Exception("Function call result has empty parts list.")

            function_response = function_call_result.parts[0].function_response
            if function_response is None:
                raise Exception("Function response is None.")

            if function_response.response is None:
                raise Exception("Function response contains no result.")

            function_responses.append(function_call_result.parts[0])

            if args.verbose:
                print(f"-> {function_response.response.get('result')}")

        # Append tool results for next iteration
        messages.append(types.Content(role="user", parts=function_responses))

    else:
        print("Error: Maximum number of iterations reached without final response.")
        sys.exit(1)

if __name__ == "__main__":
    main()