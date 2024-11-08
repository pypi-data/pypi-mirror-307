from . import log


def stop(server: str) -> None:
    log.info(f"Stopping {server} server...")
