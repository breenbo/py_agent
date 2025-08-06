import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import system_prompt
from functions.get_files_info import schema_get_files_info

# setup gemini api
def setup_gemini():
    _ = load_dotenv()
    api_key= os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    return client


def use_gemini(client: genai.Client, user_prompt: str, is_verbose: bool):
    model = "gemini-2.0-flash-001"

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info
        ]
    )

    response = client.models.generate_content(model= model, 
                                              contents= messages,
                                              config = types.GenerateContentConfig(
                                              tools = [available_functions],
                                              system_instruction=system_prompt))

    if is_verbose:
        print(f"User prompt: {user_prompt}")
        print(response.text)
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    else:
        if response.function_calls == None:
            print(response.text)
        else:
            for fn in response.function_calls:
                print(f"Calling function: {fn.name}({fn.args})")

def get_user_prompt():
    if len(sys.argv) == 1:
        raise Exception

    is_verbose = False
    if len(sys.argv) == 3:
        verbose = sys.argv[2]
        is_verbose = verbose == "--verbose"

    prompt = sys.argv[1]
    return prompt, is_verbose


def main():
    print("Hello from py-agent!\n")
    client = setup_gemini()

    # prompt = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
    try:
        prompt, is_verbose = get_user_prompt()
    except:
        print("Error: no prompt available")
        sys.exit(1)
        return

    use_gemini(client, prompt, is_verbose)

if __name__ == "__main__":
    main()
