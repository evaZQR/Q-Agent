import openai
openai.api_base = "http://flag.smarttrot.com/index.php/api/v1"
openai.api_key = "471fcd78-eb4d-4143-bf32-85da49f6e8cc"
prompt_after="""
\n 
"""
def openai_call_tools(
        prompt: str,
        model: str = "gpt-3.5-turbo",
        max_tokens: int = 100,
):
    response = openai.Completion.create(
        engine = model,
        prompt = prompt,
        max_tokens = max_tokens,
    )
    return response["choices"][0]["text"]