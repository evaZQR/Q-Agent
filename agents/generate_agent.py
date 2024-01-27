import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.call import openai_call
from typing import Dict, List
import json
import importlib
import os
OBJECTIVE = os.getenv("OBJECTIVE", "")
import re

def task_creation_agent(
        objective: str, result: Dict, task_description: str
):
    prompt = f"""
You are to use the result from an execution agent to create a new tasks with the following objective: {objective}.
The last completed task has the result: \n{result["data"]}
This result was based on this task description: {task_description}.\n"""

    prompt += "Based on the result, return a task to be completed in order to meet the objective.\n "
    prompt += "The task you propose must be solvable by one of the following tools. Note that before using this tool, you must have the required input data, which can be obtained from previous tasks or judged by yourself. The following is a description of all tools:\n"
    
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
    Return only one task in your response. The result must strictly be in the format:
    {
        "thought": Why do you generate this task.
        "the new task": A simple discription of the new task you generate.
    }
    """

    #print(f'\n*****TASK CREATION AGENT PROMPT****\n{prompt}\n')
    #raise ValueError("EVAstop")
    max_try = 5
    while max_try > 0:
        try:
            response = openai_call(prompt, max_tokens=2000)
            response = json.loads(response)
            new_task = response["the new task"]
            new_task_thought = response["thought"]
            break
        except:
            max_try -= 1
            print(f'\033[31m****TASK CREATION AGENT ERROR****\033[0m\n{response}\nwe will try again for {max_try} times\n')
            continue
            
    print(f'\n\033[32m****TASK CREATION AGENT RESPONSE****\033[0m\n{response}\n')
    task_name = re.sub(r'[^\w\s_]+', '', new_task).strip()
    out = {"task_name": task_name, "task_thought": new_task_thought}
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
    response = openai_call(prompt, max_tokens=2000)
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