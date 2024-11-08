from . import console, log


def start(server: str, background: bool = False) -> None:
    if background:
        _start_background(server)
    else:
        _start_foreground(server)


def _start_foreground(server: str) -> None:
    console.log(f"Starting {server} server as the foreground service...")
    match server:
        case "insight":
            from pyoneai_ops.insight import start_insight_server

            start_insight_server()
        case "planexecutor":
            from pyoneai_ops.orchestrator.plan_executor import (
                start_plan_executor_server,
            )

            start_plan_executor_server()
        case "orchestrator":
            from pyoneai_ops.orchestrator.scheduler import (
                start_scheduler_server,
            )

            start_scheduler_server()
        case "_":
            raise KeyError(f"Server '{server}' is not supported.")


def _start_background(server: str) -> None:
    console.log(f"Starting {server} server as the background service...")
    raise NotImplementedError("Background service is not implemented yet.")
