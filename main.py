import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import system_prompt
from functions.call_functions import call_functions
from functions.get_file_content import schema_get_file_content
from functions.get_files_info import schema_get_files_info
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file

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
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file
        ]
    )

    for i in range(0,10):
        response = client.models.generate_content(model= model, 
                                                  contents= messages,
                                                  config = types.GenerateContentConfig(
                                                  tools = [available_functions],
                                                  system_instruction=system_prompt))

        if response.text is not None:
            print(response.text)

        if response.candidates is not None:
            for candidate in response.candidates:
                if candidate.content:
                    messages.append(candidate.content)

        response_text = ""

        if is_verbose:
            response_text += f"User prompt: {user_prompt}\n"
            response_text += f"Prompt tokens: {response.usage_metadata.prompt_token_count}\n"
            response_text += f"Response tokens: {response.usage_metadata.candidates_token_count}\n"

        if response.function_calls == None:
            response_text = response.text
        else:
            for fn in response.function_calls:
                print(f"Calling function: {fn.name}({fn.args})\n")
                res = call_functions(fn, is_verbose)
                messages.append(types.Content(parts = res.parts, role="tool"))


                if res.parts[0].function_response.response is None:
                    raise Exception("Something broken")
                else:
                    response_text += f"-> {res.parts[0].function_response.response}"

        # print(response_text)


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
