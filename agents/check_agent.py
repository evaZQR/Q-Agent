import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.call import openai_call
import importlib
import json
"""
the check agent will check if the work can be done, or it is all ready done.
input: Objective, enriched_result
output: "Done","Unable","Continue"
"""
def check(OBJECTIVE, enriched_result):
    prompt = f""""
Now you are an assistant, and you need to use the Objective of the task, your completed tasks, 
and your existing tools to determine whether your current task has been completed and can be completed.
If it has been completed, return "Done" in "status".
If it cannot be completed, return "Unable" in "status".
If it can be completed but not, return "Continue" in "status". 
Regardless of what is returned, the reason needs to be explained in "thought"."""
    prompt += f"\nObjective: {OBJECTIVE}\nCompleted tasks: {enriched_result}\n"
    prompt += "The following is the description of all tools you can use:\n"
    task_descriptions = []
    module_files = [f for f in os.listdir("./tool") if f.endswith(".py") and not f.endswith("_no.py")]
    for module in module_files:
        module_name = os.path.splitext(module)[0]
        module = importlib.import_module(f"tool.{module_name}")
        cls = getattr(module, module_name)
        if cls:
            instance = cls()
            task_descriptions.append(instance.description)
    task_descriptions = "\n".join(task_descriptions)
    prompt += task_descriptions
    prompt += """
    Your response must strictly be in the format:
    {
        "thought": Why do you confirm this status.
        "status": "Done" or "Unable" or "Continue"
    }
    """
    max_try = 5
    while max_try > 0:
        try:
            response = openai_call(prompt, max_tokens=2000)
            response = json.loads(response)
            confirm = response["status"]
            if confirm == "Done" or confirm.startswith("D"):
                return "Done",response["thought"]
            elif confirm == "Unable" or confirm.startswith("U"):
                return "Unable",response["thought"]
            elif confirm == "Continue" or confirm.startswith("C"):
                return "Continue",response["thought"]
            else:
                raise ValueError(f"Unknown status: {confirm}")
        except:
            max_try -= 1
            print(f'\033[31m****CHECK AGENT ERROR****\033[0m\n{response}\nwe will try again for {max_try} times\n')
            continue
