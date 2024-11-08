import pathlib

from pyoneai_ops.mlops.const import SupportedModels
from pyoneai_ops.mlops.generators.synthetic import PROFILES


def add_train_parser(parser):
    train = parser.add_parser(
        "train", prog="OpenNebula OneAIOps", help="Train ML/AI model"
    )
    train.add_argument(
        "entity",
        choices=["virtualmachine", "host"],
        help="Entity for which metrics for training will be fetched",
    )
    train.add_argument(
        "metric", help="Metric name for which model will be trained"
    )
    # NOTE: Made required as workaround until
    # https://github.com/OpenNebula/one-aiops/issues/365 is solved
    train.add_argument(
        "-p",
        "--path",
        required=True,
        type=pathlib.Path,
        help="Path to save the trained weights.",
    )
    train.add_argument(
        "-s",
        "--scenario",
        choices=list(PROFILES.keys()),
        help="VM profile name to train a model on. If not provided, the "
        "actual data from OpenNebula system will be used",
    )
    train.add_argument(
        "-m",
        "--model",
        choices=SupportedModels.keys(),
        help="A ML/AI model to use. "
        "If not passed, the default model defined in the registry "
        "will be used",
    )
    # NOTE: period is not handled here due to issue with leading dash
