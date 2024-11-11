from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn

from .task_io import get_task_io


class RpaHubKeywords:
    @keyword
    def get_task_input(self) -> str:
        builtin = BuiltIn()
        task_id = builtin.get_variable_value("TASK_ID")
        return get_task_io(task_id).input

    @keyword
    def set_task_output(self, value) -> str:
        builtin = BuiltIn()
        task_id = builtin.get_variable_value("TASK_ID")
        get_task_io(task_id).output = value
