_tasks={}
def register(name,task):
    _tasks[name]=task
def unregister(name):
    try:
        del _tasks[name]
    except KeyError:
        pass
def tasks():
    return _tasks
def stop(name):
    task=_tasks.get(name)
    if not task:
        return False
    task.cancel()
    del _tasks[name]
    return True