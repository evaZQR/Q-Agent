from collections import deque
from typing import Dict, List
class SingleTaskListStorage:
    # 初始化一个单任务列表存储
    def __init__(self):
        # 初始化任务列表
        self.tasks = deque([])
        # 初始化任务id计数器
        self.task_id_counter = 0

    # 向任务列表中添加任务
    def append(self, task: Dict):
        # 将任务添加到任务列表中
        self.tasks.append(task)

    # 替换任务列表中的任务
    def replace(self, tasks: List[Dict]):
        # 将任务替换到任务列表中
        self.tasks = deque(tasks)

    # 从任务列表中弹出任务
    def popleft(self):
        # 从任务列表中弹出任务
        return self.tasks.popleft()

    # 判断任务列表是否为空
    def is_empty(self):
        # 判断任务列表是否为空
        return False if self.tasks else True

    # 获取任务列表中的任务名称
    def next_task_id(self):
        # 计算任务id计数器
        self.task_id_counter += 1
        # 返回任务id计数器
        return self.task_id_counter

    # 获取任务列表中的任务名称
    def get_task_names(self):
        # 返回任务列表中的任务名称
        return [t["task_name"] for t in self.tasks]
