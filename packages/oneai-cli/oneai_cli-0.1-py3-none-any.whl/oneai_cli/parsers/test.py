__all__ = [
    "add_eval_subparser",
]
from pyoneai_ops.mlops.const import SupportedModels
from pyoneai_ops.mlops.generators.synthetic import PROFILES


def add_eval_parser(parser):
    test = parser.add_parser(
        "test", prog="OpenNebula OneAIOps", help="Evaluate ML/AI model"
    )
    test.add_argument(
        "entity",
        choices=["virtualmachine", "host"],
        help="Entity for which metrics for training will be fetched",
    )
    test.add_argument(
        "metric", help="Metric name for which model will be trained"
    )
    test.add_argument(
        "-s",
        "--scenario",
        choices=list(PROFILES.keys()),
        help="VM profile name to train a model on. If not provided, the "
        "actual data from OpenNebula system will be used",
    )
    test.add_argument(
        "--mse",
        action="store_true",
        help="Use Mean Squared Error for evaluation",
    )
    test.add_argument(
        "--mae",
        action="store_true",
        help="Use Mean Absolute Error for evaluation",
    )
    test.add_argument(
        "--r2", action="store_true", help="Use R2 Score for evaluation"
    )
    test.add_argument(
        "--mape",
        action="store_true",
        help="Use Mean Absolute Percentage Error for evaluation",
    )
    test.add_argument(
        "--rmse",
        action="store_true",
        help="Use Root Mean Squared Error for evaluation",
    )
    test.add_argument(
        "--nrmse",
        action="store_true",
        help="Use Normalized Root Mean Squared Error for evaluation",
    )
    test.add_argument(
        "--spearmancorr",
        action="store_true",
        help="Use Spearman Correlation " "for evaluation",
    )
    test.add_argument(
        "--all", action="store_true", help="Use all evaluation metrics"
    )
    test.add_argument(
        "-m",
        "--model",
        choices=SupportedModels.keys(),
        help="A ML/AI model to use. "
        "If not provided, the default model defined in the registry "
        "will be used",
    )
    test.add_argument(
        "-p", "--path", type=str, help="Path to load model weights (if needed)"
    )
