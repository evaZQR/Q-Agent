import openai
import os
from extensions.human_mode import user_input_await
import tiktoken as tiktoken
import time

import google.generativeai as genai
from google.generativeai.types import safety_types
from google.ai import generativelanguage as glm

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
openai.api_base = "http://flag.smarttrot.com/index.php/api/v1"

LLM_MODEL = os.getenv("LLM_MODEL", os.getenv("OPENAI_API_MODEL", "gpt-3.5-turbo")).lower()
OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", 0.0))
openai.api_key = OPENAI_API_KEY

def limit_tokens_from_string(string: str, model: str, limit: int) -> str:
    """Limits the string to a number of tokens (estimated)."""

    try:
        encoding = tiktoken.encoding_for_model(model)
    except:
        encoding = tiktoken.encoding_for_model('gpt2')  # Fallback for others.

    encoded = encoding.encode(string)

    return encoding.decode(encoded[:limit])


def openai_call(
    prompt: str,
    model: str = LLM_MODEL,
    temperature: float = OPENAI_TEMPERATURE,
    max_tokens: int = 100,
):
    while True:
        try:
            if model.lower().startswith("human"):
                return user_input_await(prompt)
            elif not model.lower().startswith("gpt-"):
                # Use completion API
                response = openai.Completion.create(
                    engine=model,
                    prompt=prompt,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0,
                )
                return response.choices[0].text.strip()
            else:
                # Use 4000 instead of the real limit (4097) to give a bit of wiggle room for the encoding of roles.
                # TODO: different limits for different models.

                trimmed_prompt = limit_tokens_from_string(prompt, model, 4000 - max_tokens)
                # Use chat completion API
                messages = [{"role": "system", "content": trimmed_prompt}]
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    n=1,
                    stop=None,
                )
                return response.choices[0].message.content.strip()
        except openai.error.RateLimitError:
            print(
                "   *** The OpenAI API rate limit has been exceeded. Waiting 10 seconds and trying again. ***"
            )
            time.sleep(10)  # Wait 10 seconds and try again
        except openai.error.Timeout:
            print(
                "   *** OpenAI API timeout occurred. Waiting 10 seconds and trying again. ***"
            )
            time.sleep(10)  # Wait 10 seconds and try again
        except openai.error.APIError:
            print(
                "   *** OpenAI API error occurred. Waiting 10 seconds and trying again. ***"
            )
            time.sleep(10)  # Wait 10 seconds and try again
        except openai.error.APIConnectionError:
            print(
                "   *** OpenAI API connection error occurred. Check your network settings, proxy configuration, SSL certificates, or firewall rules. Waiting 10 seconds and trying again. ***"
            )
            time.sleep(10)  # Wait 10 seconds and try again
        except openai.error.InvalidRequestError:
            print(
                "   *** OpenAI API invalid request. Check the documentation for the specific API method you are calling and make sure you are sending valid and complete parameters. Waiting 10 seconds and trying again. ***"
            )
            time.sleep(10)  # Wait 10 seconds and try again
        except openai.error.ServiceUnavailableError:
            print(
                "   *** OpenAI API service unavailable. Waiting 10 seconds and trying again. ***"
            )
            time.sleep(10)  # Wait 10 seconds and try again
        else:
            break

class GeminiPro:
    def __init__(self,
                 GOOGLE_API_KEY=""):
        self.model = genai.GenerativeModel('gemini-pro')
        self.chat = self.model.start_chat(history=[])
        self.latest_response = None
        # Or use `os.getenv('GOOGLE_API_KEY')` to fetch an environment variable.
        self.GOOGLE_API_KEY=GOOGLE_API_KEY
        genai.configure(api_key=self.GOOGLE_API_KEY)
        self.safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_NONE",
        },
        ]
        
    def genai_call(self, prompt):
        try:
            response = self.chat.send_message(prompt,safety_settings=self.safety_settings,
            generation_config=genai.types.GenerationConfig(
            # Only one candidate for now.
            candidate_count=1,
            temperature=0.0,
            max_output_tokens=1024))
            try:
                self.latest_response = response.text
            except ValueError:
                self.latest_response = response.prompt_feedback
            
            
        except:
            max_retry = 10
            for j in range(max_retry):
                try:
                    print(f"Retring: {j}/{max_retry} ")
                    response = self.chat.send_message(prompt,safety_settings=self.safety_settings,
                                            generation_config=genai.types.GenerationConfig(
                    # Only one candidate for now.
                    candidate_count=1,
                    temperature=0.0))
                    
                    try:
                        self.latest_response = response.text
                    except ValueError:
                        self.latest_response = response.prompt_feedback
                    
                except:
                    time.sleep(5)
            else:
                # raise RuntimeError("Max retry exceeded")
                self.latest_response = "I don't know."
                
        return self.latest_response
    
    def refresh_history(self):
        self.chat = self.model.start_chat(history=[])
