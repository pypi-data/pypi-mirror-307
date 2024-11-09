import time
from pytools import AsyncUtils
from pytools import CoreUtils
from pytools import DateUtils
from pytools import HttpUtils
from pytools import JsonUtils
from pytools import LogUtils
from pytools import StreamUtils

# Sample tasks for testing
def task1():
    time.sleep(2)
    return 'task1 finished ' + DateUtils.now_str()

def task2(par1):
    time.sleep(3)
    return f'task2 finished {DateUtils.now_str()} with params {par1}'

def task3(par1, par2):
    time.sleep(1)
    return f'task3 finished {DateUtils.now_str()} with params {par1}, {par2}'

# tuples of tasks, each having a method, list of arguments
task_list = [(task1, []), (task2, [1]), (task3, [1, 2])]
# Execute tasks asynchronously
print(f'Tasks reached at {DateUtils.now_str()}')
AsyncUtils.execute_tasks_with_no_wait(task_list)
print(f'Tasks started at {DateUtils.now_str()}')