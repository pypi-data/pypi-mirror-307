import atexit
from multiprocessing.util import _exit_function

from pyxxl import ExecutorConfig, PyxxlRunner

bind = ["0.0.0.0:8000"]
backlog = 512
workers = 1
timeout = 300
graceful_timeout = 2
limit_request_field_size = 8192


def when_ready(server):
    # pylint: disable=import-outside-toplevel,unused-import,no-name-in-module
    from app import xxl_handler

    atexit.unregister(_exit_function)

    config = ExecutorConfig(
        xxl_admin_baseurl="http://192.168.64.150:9970/xxl-job-admin/api/",
        executor_app_name="RPA-Hub",
        executor_host="192.168.64.132",
        debug=True,
    )

    pyxxl_app = PyxxlRunner(config, handler=xxl_handler)
    server.pyxxl_app = pyxxl_app
    pyxxl_app.run_with_daemon()
