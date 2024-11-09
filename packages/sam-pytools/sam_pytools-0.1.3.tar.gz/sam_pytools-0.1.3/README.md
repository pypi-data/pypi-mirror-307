# PY Tools

`sam_pytools` is a collection of Python utilities that provide commonly used functions for handling dates, HTTP requests, JSON manipulation, logging, and more.
These tools help streamline various tasks in Python projects.


### Installation

`pip install samPytools`

#### Available Modules
    GlobalValues: Manages global values like home and log directories.
    CoreUtils: Contains utility methods for general operations 
    like downloading images, decoding bytes, generating unique IDs, etc.
    DateUtils: Provides date manipulation functions, 
    including time difference calculations and interval additions.
    HttpUtils: Offers HTTP helper methods for GET and POST requests.
    JsonUtils: Contains JSON helper functions, like converting dictionaries to objects.
    LogUtils: Manages logging and error handling.
    AsyncUtils: Enables asynchronous execution of given tasks with asyncio or ThreadPoolExecutor.


`pip install sam_pytools`

#### Special features

For easier and clean error tracing

`LogUtils.getErrorMessage()` is the one that can make life easier

Another is AsyncUtils
```
    from sam_tools import AsyncUtils

      def task1():
          time.sleep(2)
          return 'task1 finished ' + DateUtils.now_str()
      
      def task2(par1):
          time.sleep(3)
          return f'task2 finished {DateUtils.now_str()}, received params => {par1}'
      
      def task3(par1, par2):
          time.sleep(1)
          return f'task3 finished {DateUtils.now_str()}, received params => {par1},{par2}'

      task_list = [(task1, []), (task2, [1]), (task3, [1, 2])]
      #Execute tasks asynchronously
      print(f'Tasks reached at {DateUtils.now_str()}')
      AsyncUtils.execute_tasks_with_no_wait(task_list)
      print(f'Tasks started at {DateUtils.now_str()}')
```


#### General about pip

If you want to reset your testing virtual environment

`pip freeze | xargs pip uninstall -y`

then to install your requirements

`pip install -r requirements.txt`