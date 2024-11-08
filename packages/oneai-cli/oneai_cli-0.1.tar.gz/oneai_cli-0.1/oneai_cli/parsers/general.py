def add_version(parser) -> None:
    from .. import __version__

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="%(prog)s [{version}]".format(version=__version__),
    )
