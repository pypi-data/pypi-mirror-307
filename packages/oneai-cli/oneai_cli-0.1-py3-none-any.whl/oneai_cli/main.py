import argparse as ap
from os import path

from pyexpat import model

from . import console
from .parsers.general import add_version
from .parsers.server import add_start_parser, add_stop_parser
from .parsers.test import add_eval_parser
from .parsers.train import add_train_parser
from .utils import _handle_period_arg

_PROGRAM_NAME: str = "OpenNebula OneAIOps CLI"


def main():
    parser = ap.ArgumentParser(
        prog=_PROGRAM_NAME,
        add_help=True,
        description="OneAIOps CLI",
    )
    add_version(parser)
    subparsers = parser.add_subparsers(
        dest="command", help="Supported commands"
    )
    add_start_parser(subparsers)
    add_stop_parser(subparsers)
    add_train_parser(subparsers)
    add_eval_parser(subparsers)

    # NOTE: workaround as we cannot pass period starting with negative values
    # due to leading dash which is interpreted as argument
    arguments, unknown = parser.parse_known_args()
    match arguments.command:
        case "start":
            from .start import start

            start(server=arguments.server, background=arguments.daemon)
        case "stop":
            from .stop import stop

            stop(server=arguments.server)
        case "train":
            from .train import TrainProcessor

            TrainProcessor(
                console=console,
                entity=arguments.entity,
                metric=arguments.metric,
                period=_handle_period_arg(unknown),
                path=arguments.path,
                scenario=arguments.scenario,
                model=arguments.model,
            ).run()
        case "test":
            from .test import EvaluationProcessor

            EvaluationProcessor(
                console=console,
                entity=arguments.entity,
                metric=arguments.metric,
                period=_handle_period_arg(unknown),
                scenario=arguments.scenario,
                mse=arguments.mse,
                mae=arguments.mae,
                r2=arguments.r2,
                rmse=arguments.rmse,
                nrmse=arguments.nrmse,
                mape=arguments.mape,
                spearmancorr=arguments.spearmancorr,
                all=arguments.all,
                path=arguments.path,
                model=arguments.model,
            ).run()
