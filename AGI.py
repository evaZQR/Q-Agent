#!/usr/bin/env python3
from dotenv import load_dotenv
import json

# Load default environment variables (.env)
load_dotenv()

import os
import time
from module.task import SingleTaskListStorage
from agents.task_agent import execution_agent
from agents.generate_agent import task_creation_agent, prioritization_agent
from agents.check_agent import check
import tiktoken as tiktoken

# default opt out of chromadb telemetry.
from chromadb.config import Settings
from module.load import load
load()

from module.storage import try_weaviate, try_pinecone, use_chroma
results_storage = try_weaviate() or try_pinecone() or use_chroma()


JOIN_EXISTING_OBJECTIVE = True
INITIAL_TASK = os.getenv("INITIAL_TASK", os.getenv("FIRST_TASK", ""))
OBJECTIVE = os.getenv("OBJECTIVE", "")
# Initialize tasks storage
tasks_storage = SingleTaskListStorage()
# Add the initial task if starting new objective
if not JOIN_EXISTING_OBJECTIVE:
    initial_task = {
        "task_id": tasks_storage.next_task_id(),
        "task_name": INITIAL_TASK
    }
    tasks_storage.append(initial_task)

def main():
    loop = True
    enriched_result = "you have done nothing"
    while loop:
        # As long as there are tasks in the storage...
        #if not tasks_storage.is_empty():
        status ,thought = check(OBJECTIVE,enriched_result)

        if status == "Done":
            ans = "Q-Agent have completed the objective\n"
            ans += "The result is:\n" + enriched_result
            print(ans)
            loop = False
            break
        elif status == "Unable":
            ans = "Q-Agent cannot do the objective\nbecause:"+ thought
            print(ans)
            loop = False
            break
        else:
            print("\ntest:"+thought+"\n\n")
        print('Adding new tasks to task_storage')
        new_task = task_creation_agent(
            OBJECTIVE,
            enriched_result,
        )
        new_task_thought = new_task["task_thought"]
        new_task_name = new_task["task_name"]
        new_task_tool = new_task["task_tool"]

        new_task.update({"task_id": tasks_storage.next_task_id()})
        print('New task name:', new_task_name)
        print('New task thought:', new_task_thought)
        tasks_storage.append(new_task)


        if not JOIN_EXISTING_OBJECTIVE:
            prioritized_tasks = prioritization_agent(tasks_storage = tasks_storage)
            if prioritized_tasks:
                tasks_storage.replace(prioritized_tasks)
            
        print("\033[95m\033[1m" + "\n*****TASK LIST*****\n" + "\033[0m\033[0m")
        for t in tasks_storage.get_task_names():
            print(" • " + str(t))


        task = tasks_storage.popleft()
        print("\033[92m\033[1m" + "\n*****NEXT TASK*****\n" + "\033[0m\033[0m")
        print(str(task["task_name"]))


            
        result = execution_agent(OBJECTIVE, new_task_tool)
        raise ValueError("Q-Agent testing edge!!! you get the wrong .")
        print("\033[93m\033[1m" + "\n*****TASK RESULT*****\n" + "\033[0m\033[0m")
        print(result)

            
        enriched_result = {
            "data": result
        }
            

        result_id = f"result_{task['task_id']}"
        results_storage.add(task, result, result_id)

            

        # Sleep a bit before checking the task list again
        time.sleep(5)


if __name__ == "__main__":
    main()
