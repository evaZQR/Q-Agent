import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.call import openai_call
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
