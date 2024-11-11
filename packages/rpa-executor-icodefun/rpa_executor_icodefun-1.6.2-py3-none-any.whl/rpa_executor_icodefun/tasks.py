import json
from pathlib import Path
from typing import Generator, TypedDict
from attr import dataclass
import yaml
import robot

from pyxxl.ctx import g
from pyxxl import PyxxlRunner

from robot.result.model import TestCase, Keyword

from .config import RpaHubConfig
from .task_io import open_task_io
from .xxl_biz_api import XXL_BIZ


@dataclass
class TaskInfo:
    suite_base_path: Path
    suite_name: str
    suite_description: str
    robot_file: str
    task_name: str
    task_description: str

    @property
    def job_id(self) -> str:
        return f"[{self.suite_name}]-[{self.task_name}]"


class TaskCollector:
    def __init__(self, config: RpaHubConfig, **kwargs):
        self.config = config

    def collect(self) -> Generator[TaskInfo, None, None]:
        base_path = Path("tasks").absolute()
        if not base_path.exists():
            pass

        for suite_path in base_path.iterdir():
            manifest_path = suite_path.joinpath("manifest.yaml")
            if (not manifest_path.exists()) or (not manifest_path.is_file()):
                print("No manifest file found")

            with open(manifest_path, "r") as f:
                try:
                    manifest = yaml.safe_load(f)
                except yaml.YAMLError as e:
                    print(f"Error loading manifest[{manifest_path}]: {e}")
                    raise e

            if (not manifest.get("name")) or (not manifest.get("tasks")):
                print("manifest not valid")

            for task in manifest.get("tasks"):
                if not task.get("name"):
                    print("task name not valid")

                print(f"Found task: {manifest.get('name')}.{task.get('name')}")
                yield TaskInfo(
                    suite_base_path=suite_path,
                    suite_name=manifest.get("name"),
                    robot_file=manifest.get("robot_file"),
                    suite_description=manifest.get("description"),
                    task_name=task.get("name"),
                    task_description=task.get("description"),
                )

    def register(self, app: PyxxlRunner, task_info: TaskInfo):
        def inner_task():
            robot_path = task_info.suite_base_path.joinpath(task_info.robot_file)
            task_id = g.xxl_run_data.logId

            with open_task_io(task_id) as io:
                if (
                    g.xxl_run_data.executorParams is not None
                    and g.xxl_run_data.executorParams != ""
                ):
                    io.input = json.loads(g.xxl_run_data.executorParams)

                visitor = ResultListener()

                robot.run(
                    str(robot_path),
                    task=task_info.task_name,
                    variable=f"TASK_ID:{task_id}",
                    # outputdir="output",
                    log=None,
                    report=None,
                    listener=visitor,
                    output=None,
                )

                output = io.output

                if not visitor.report.get("success"):
                    raise Exception(f"Task failed: {visitor.report.get('error')}")
                # TODO: log duration
                return json.dumps(output)

        app.register(name=task_info.job_id)(inner_task)


@dataclass
class ExecutionReport(TypedDict):
    success: bool
    error: str
    callStack: list[str]
    duration: int
    startTime: str


class ResultListener:
    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self):
        self.report: ExecutionReport = {
            "success": True,
            "error": None,
            "callStack": [],
            "duration": 0,
            "startTime": None,
        }

    def start_test(self, data, result: TestCase):
        self.report["startTime"] = result.start_time

    def end_test(self, data, result: TestCase):
        if result.failed:
            self.report["success"] = False
            self.report["error"] = result.message
            self.report["callStack"].append(result.name)
            self.report["duration"] = result.elapsedtime
        else:
            self.report["success"] = True
            self.report["duration"] = result.elapsedtime

    def start_keyword(self, data, result: Keyword):
        pass

    def end_keyword(self, data, result: Keyword):
        if result.failed:
            self.report["callStack"].append(result.name)

    # def end_user_keyword(self, data, result):
    #     if result.failed:
    #         self.errors.append(result.message)

    # def end_library_keyword(self, data, result):
    #     if result.failed:
    #         self.errors.append(result.message)
