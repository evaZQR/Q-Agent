import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.call import GeminiPro
from agents.call import openai_call
import importlib

# Execute a task based on the objective and five previous tasks
def execution_agent(task: str, tool) -> str:
    """
    Executes a task based on the given objective and previous context.

    Args:
        (not now use)objective (str): The objective or goal for the AI to perform the task.
        task (str): The task to be executed by the AI.
        tool (str): The tool the task need.

    Returns:
        str: The response generated by the AI for the given task.

    """
    module = importlib.import_module(f"tool.{tool}")
    cls = getattr(module, tool)
    instance = cls()
    def run_order(INPUT):
        return instance.jsonrun(INPUT)
    #context = context_agent(query=objective, top_results_num=5, results_storage = results_storage)
    #print("\n****RELEVANT CONTEXT****\n")
    #print(context)
    #print('')
    #prompt = f'Perform one task based on the following objective: {objective}.\n'
    #if context:
    #    prompt += 'Take into account these previously completed tasks:' + '\n'.join(context)
    prompt = f"now you should follow the task:\n{task}\n to make the json data"
    prompt +="your response should strictly be in the format:\n" + instance.jsonloadF
    try:
        print(openai_call(prompt))
    except Exception:
        print(GeminiPro.genai_call(prompt))
# Get the top n completed tasks for the objective
def context_agent(query: str, top_results_num: int, results_storage):
    """
    Retrieves context for a given query from an index of tasks.

    Args:
        query (str): The query or objective for retrieving context.
        top_results_num (int): The number of top results to retrieve.

    Returns:
        list: A list of tasks as context for the given query, sorted by relevance.

    """
    results = results_storage.query(query=query, top_results_num=top_results_num)
    # print("****RESULTS****")
    # print(results)
    return results
