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
        thought, status = check(OBJECTIVE,enriched_result)
        print('Adding new tasks to task_storage')
        new_task = task_creation_agent(
            OBJECTIVE,
            enriched_result,
            task["task_name"],
        )
        new_task = json.loads(new_task)
        new_task_thought = new_task["thought"]
        new_task_name = new_task["the new task"]

        new_task_name.update({"task_id": tasks_storage.next_task_id()})
        print('New task name:', new_task_name)
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


            
        result = execution_agent(OBJECTIVE, str(task["task_name"]), results_storage=results_storage)
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
