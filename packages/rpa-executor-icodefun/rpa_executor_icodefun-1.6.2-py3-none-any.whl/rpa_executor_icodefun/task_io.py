_task_io: dict = {}

class TaskIo:
    def __init__(self, task_id: int):
        self.task_id = task_id
        self.input = None
        self.output = None

    def __enter__(self):
        _task_io[self.task_id] = self
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        _task_io.pop(self.task_id)


def open_task_io(task_id: int) -> TaskIo:
    return TaskIo(task_id)


def get_task_io(task_id: int) -> TaskIo:
    return _task_io.get(task_id)
