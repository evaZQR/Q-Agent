import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.call import GeminiPro
from agents.call import openai_call
from typing import Dict, List
import json
import importlib
import os
OBJECTIVE = os.getenv("OBJECTIVE", "")
import re

def task_creation_agent(
        objective: str, result: Dict
):
    prompt = f"""
You are to use the result from an execution agent to create a new tasks with the following objective: {objective}.
The last completed tasks has the result: \n{result}"""

    prompt += "Based on the result, return a task to be completed in order to meet the objective.\n "
    prompt += "You should not ask user for help and do the all things by yourself"
    prompt += "The task you propose must be solvable by one of the following tools. Note that before using this tool, you must have the required input data, which can be obtained from previous tasks or judged by yourself. The following is a description of all tools:\n"
    
    task_descriptions = []
    module_files = [f for f in os.listdir("./tool") if f.endswith(".py") and not f.endswith("_no.py")]
    tools = []
    for module in module_files:
        module_name = os.path.splitext(module)[0]
        tools.append(module_name)
        module = importlib.import_module(f"tool.{module_name}")
        cls = getattr(module, module_name)
        if cls:
            instance = cls()
            task_descriptions.append(instance.description)
    task_descriptions = "\n".join(task_descriptions)
    prompt += task_descriptions
    prompt += """
    Return only one task in your response. The result must strictly be in the format:
    {
        "thought": Why do you generate this task.
        "Tool": The Tool you use.
        "the new task": A simple discription of the new task you generate. The discription should be clear and short.
    }
    """

    #print(f'\n*****TASK CREATION AGENT PROMPT****\n{prompt}\n')
    #raise ValueError("EVAstop")
    max_try = 5
    while max_try > 0:
        try:
            try:  
                response = openai_call(prompt, max_tokens=2000)
            except NameError:
                response = GeminiPro.genai_call(prompt, max_tokens=2000)
     
            response = json.loads(response)
            new_task = response["the new task"]
            new_task_thought = response["thought"]
            new_task_tool = response["Tool"]
            tool_is_found = False
            for tool in tools:
                if new_task_tool .lower() == tool.lower() or new_task_tool in tool or tool in new_task_tool:
                    new_task_tool = tool
                    tool_is_found = True
                    break
            if tool_is_found is False: raise ValueError("connot find")
            break
        except:
            max_try -= 1
            print(f'\033[31m****TASK CREATION AGENT ERROR****\033[0m\n{response}\nwe will try again for {max_try} times\n')
            continue
            
    print(f'\n\033[32m****TASK CREATION AGENT RESPONSE****\033[0m\n{response}\n')
    task_name = re.sub(r'[^\w\s_]+', '', new_task).strip()
    out = {"task_name": task_name, "task_thought": new_task_thought,"task_tool":new_task_tool}
    return out


def prioritization_agent(tasks_storage):
    task_names = tasks_storage.get_task_names()
    bullet_string = '\n'

    prompt = f"""
You are tasked with prioritizing the following tasks: {bullet_string + bullet_string.join(task_names)}
Consider the ultimate objective of your team: {OBJECTIVE}.
Tasks should be sorted from highest to lowest priority, where higher-priority tasks are those that act as pre-requisites or are more essential for meeting the objective.
Do not remove any tasks. Return the ranked tasks as a numbered list in the format:

#. First task
#. Second task

The entries must be consecutively numbered, starting with 1. The number of each entry must be followed by a period.
Do not include any headers before your ranked list or follow your list with any other output."""

    #print(f'\n****TASK PRIORITIZATION AGENT PROMPT****\n{prompt}\n')
    try:  
        response = openai_call(prompt, max_tokens=2000)
    except NameError:
        response = GeminiPro.genai_call(prompt, max_tokens=2000)
     
    #print(f'\n****TASK PRIORITIZATION AGENT RESPONSE****\n{response}\n')
    if not response:
        print('Received empty response from priotritization agent. Keeping task list unchanged.')
        return
    new_tasks = response.split("\n") if "\n" in response else [response]
    new_tasks_list = []
    for task_string in new_tasks:
        task_parts = task_string.strip().split(".", 1)
        if len(task_parts) == 2:
            task_id = ''.join(s for s in task_parts[0] if s.isnumeric())
            task_name = re.sub(r'[^\w\s_]+', '', task_parts[1]).strip()
            if task_name.strip():
                new_tasks_list.append({"task_id": task_id, "task_name": task_name})

    return new_tasks_list

if __name__ == '__main__':
    task_creation_agent("no",{"data": 0},"no")
