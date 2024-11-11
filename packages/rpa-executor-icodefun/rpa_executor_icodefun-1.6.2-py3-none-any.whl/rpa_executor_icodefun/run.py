from pyxxl import PyxxlRunner, JobHandler

import argparse
import os

from .config import load_config
from .tasks import TaskCollector
from .xxl_biz_api import XXL_BIZ


def run_cli():
    parser = argparse.ArgumentParser(
        description="这是用于启动iCodeFun RPA executor的命令行工具"
    )

    parser.add_argument(
        "mode", type=str, help="启动模式", choices=["dev", "prod"], default="dev"
    )
    parser.add_argument("--config_path", type=str, help="指定配置文件路径")

    args = parser.parse_args()

    config_path = args.config_path

    if config_path is None:
        config_path = "config.yaml"

    if not os.path.exists(config_path):
        raise ValueError(f"配置文件{config_path}不存在")

    config = load_config(config_path, args.mode == "dev")

    collector = TaskCollector(config)

    xxl_handler = JobHandler()

    pyxxl_app = PyxxlRunner(config, handler=xxl_handler)
    biz_api = XXL_BIZ(config)

    tasks = collector.collect()
    biz_api.all_jobs_registry([task.job_id for task in tasks])
    for task_info in tasks:
        collector.register(pyxxl_app, task_info)

    if config.debug:
        pyxxl_app.run_executor()
    else:
        pyxxl_app.run_with_daemon()


if __name__ == "__main__":
    run_cli()
