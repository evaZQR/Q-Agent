#!/usr/bin/env python3
from dotenv import load_dotenv

# Load default environment variables (.env)
load_dotenv()

import os
import time
from module.task import SingleTaskListStorage
from agents.task_agent import execution_agent
from agents.generate_agent import task_creation_agent, prioritization_agent
import tiktoken as tiktoken

# default opt out of chromadb telemetry.
from chromadb.config import Settings
from module.load import load
load()

from module.storage import try_weaviate, try_pinecone, use_chroma
results_storage = try_weaviate() or try_pinecone() or use_chroma()


JOIN_EXISTING_OBJECTIVE = False
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
    while loop:
        # As long as there are tasks in the storage...
        if not tasks_storage.is_empty():
            # Print the task list
            print("\033[95m\033[1m" + "\n*****TASK LIST*****\n" + "\033[0m\033[0m")
            for t in tasks_storage.get_task_names():
                print(" • " + str(t))

            # Step 1: Pull the first incomplete task
            task = tasks_storage.popleft()
            print("\033[92m\033[1m" + "\n*****NEXT TASK*****\n" + "\033[0m\033[0m")
            print(str(task["task_name"]))

            # Send to execution function to complete the task based on the context
            result = execution_agent(OBJECTIVE, str(task["task_name"]), results_storage=results_storage)
            print("\033[93m\033[1m" + "\n*****TASK RESULT*****\n" + "\033[0m\033[0m")
            print(result)

            # Step 2: Enrich result and store in the results storage
            # This is where you should enrich the result if needed
            enriched_result = {
                "data": result
            }
            # extract the actual result from the dictionary
            # since we don't do enrichment currently
            # vector = enriched_result["data"]

            result_id = f"result_{task['task_id']}"

            results_storage.add(task, result, result_id)

            # Step 3: Create new tasks and re-prioritize task list
            # only the main instance in cooperative mode does that
            new_tasks = task_creation_agent(
                OBJECTIVE,
                enriched_result,
                task["task_name"],
                tasks_storage.get_task_names(),
            )

            print('Adding new tasks to task_storage')
            for new_task in new_tasks:
                new_task.update({"task_id": tasks_storage.next_task_id()})
                print(str(new_task))
                tasks_storage.append(new_task)

            if not JOIN_EXISTING_OBJECTIVE:
                prioritized_tasks = prioritization_agent(tasks_storage = tasks_storage)
                if prioritized_tasks:
                    tasks_storage.replace(prioritized_tasks)

            # Sleep a bit before checking the task list again
            time.sleep(5)
        else:
            print('Done.')
            loop = False


if __name__ == "__main__":
    main()
