from dataclasses import dataclass

import yaml
from pyxxl import ExecutorConfig


@dataclass
class RpaHubConfig(ExecutorConfig):
    client_secret: str = None


def load_config(path: str, debug: bool) -> RpaHubConfig:
    with open(path, "r") as f:
        yaml_config = yaml.safe_load(f)

    if yaml_config.get("xxl_admin_baseurl") is None:
        raise ValueError("xxl_admin_baseurl is required")
    if yaml_config.get("executor") is None:
        raise ValueError("executor is required")
    executor_config = yaml_config["executor"]
    executor_config.setdefault("app_name", "rpa-hub")
    if executor_config.get("host") is None:
        raise ValueError("executor host is required")
    executor_config.setdefault("port", 9999)
    executor_config.setdefault("listen_host", "")
    executor_config.setdefault("listen_port", 0)

    yaml_config.setdefault("log", {})
    yaml_config["log"].setdefault("expired_days", 7)
    yaml_config["log"].setdefault("local_dir", "logs")

    yaml_config.setdefault("max_workers", 10)

    yaml_config.setdefault("task", {})
    yaml_config["task"].setdefault("queue_length", 10)
    yaml_config["task"].setdefault("timeout", 600)

    if yaml_config.get("client_secret") is None:
        raise ValueError("client_secret is required")

    return RpaHubConfig(
        xxl_admin_baseurl=yaml_config["xxl_admin_baseurl"],
        executor_app_name=yaml_config["executor"]["app_name"],
        executor_host=yaml_config["executor"]["host"],
        executor_port=yaml_config["executor"]["port"],
        executor_listen_host=yaml_config["executor"]["listen_host"],
        executor_listen_port=yaml_config["executor"]["listen_port"],
        log_expired_days=yaml_config["log"]["expired_days"],
        log_local_dir=yaml_config["log"]["local_dir"],
        max_workers=yaml_config["max_workers"],
        task_queue_length=yaml_config["task"]["queue_length"],
        task_timeout=yaml_config["task"]["timeout"],
        debug=debug,
        client_secret=yaml_config["client_secret"],
        executor_log_path="pyxxl.log",
    )
