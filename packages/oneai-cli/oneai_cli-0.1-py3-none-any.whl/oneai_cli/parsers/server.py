_SUPPORTED_SERVERS = ["insight", "planexecutor", "orchestrator"]


def add_start_parser(parser):
    start_parser = parser.add_parser(
        "start",
        prog="OpenNebula OneAIOps",
        help="Start one of the OneAIOps server",
    )
    start_parser.add_argument(
        "server", choices=_SUPPORTED_SERVERS, help="Server to start"
    )
    start_parser.add_argument(
        "-d",
        "--daemon",
        action="store_true",
        help="Start as a daemon process",
    )


def add_stop_parser(parser):
    stop_server = parser.add_parser(
        "stop",
        prog="OpenNebula OneAIOps",
        help="Stop one of the running OneAIOps servers",
    )
    stop_server.add_argument(
        "server", choices=_SUPPORTED_SERVERS, help="Server to stop"
    )
