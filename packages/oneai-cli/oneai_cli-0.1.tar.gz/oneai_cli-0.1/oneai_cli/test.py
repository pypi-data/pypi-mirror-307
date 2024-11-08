from pyoneai import Session
from pyoneai_ops.mlops.const import SupportedModels
from pyoneai_ops.mlops.core.evaluation import (
    evaluate_on_real_data,
    evaluate_on_synthetic_data,
)
from pyoneai_ops.mlops.core.reporting import (
    prepare_markdown_report_for_real_eval,
    prepare_markdown_report_for_synth_eval,
)
from pyoneai_ops.utils import handle_missing_config
from rich.console import Console
from rich.markdown import Markdown


class EvaluationProcessor:

    def __init__(
        self,
        console: Console,
        entity: str,
        metric: str,
        period: slice,
        path: str,
        scenario: str | None,
        mse: bool,
        mae: bool,
        rmse: bool,
        mape: bool,
        r2: bool,
        nrmse: bool,
        spearmancorr: bool,
        all: bool,
        model: str | None,
    ):
        self.session = Session()
        self.console = console
        self.entity = entity
        self.metric = metric
        self.period = period
        self.path = path
        self.scenario = scenario
        self.quality_metrics = self._gather_metrics_names(
            mse=mse,
            mae=mae,
            rmse=rmse,
            mape=mape,
            r2=r2,
            nrmse=nrmse,
            spearmancorr=spearmancorr,
            all=all,
        )
        model = self._maybe_get_default_model(model)
        self.model: SupportedModels = SupportedModels.get(model)

    def _maybe_get_default_model(self, model: str | None) -> str:
        """Get the default model defined in the registry, if not specified."""
        if model is not None:
            return model
        return self.session.config.registry["default"]["prediction"]["class"]

    @handle_missing_config
    def run(self):
        with self.console.status("Evaluating ML/AI model...") as status:
            if self.scenario:
                status.update(
                    "Evaluating an AI/ML model on synthetic "
                    f"data for profile '{self.scenario}'..."
                )
                metrics_values = evaluate_on_synthetic_data(
                    session=self.session,
                    entity=self.entity,
                    metric_name=self.metric,
                    data_profile=self.scenario,
                    period=self.period,
                    model=self.model,
                    weights_path=self.path,
                    metrics=self.quality_metrics,
                )
                status.update("Preparing report...")
                report = prepare_markdown_report_for_synth_eval(
                    ml_model_name=self.model,
                    scenario_name=self.scenario,
                    metrics=metrics_values,
                )

            else:
                status.update(
                    "Evaluation an AI/ML model on real "
                    "OpenNebula Prometheus metrics..."
                )
                metrics_values = evaluate_on_real_data(
                    session=self.session,
                    entity=self.entity,
                    metric_name=self.metric,
                    period=self.period,
                    model=self.model,
                    weights_path=self.path,
                    metrics=self.quality_metrics,
                )
                status.update("Preparing report...")
                report = prepare_markdown_report_for_real_eval(
                    ml_model_name=self.model,
                    entity=self.entity,
                    metric_name=self.metric,
                    metrics=metrics_values,
                )
            self.console.print(Markdown(report))

    def _gather_metrics_names(
        self,
        mse: bool,
        mae: bool,
        r2: bool,
        mape: bool,
        rmse: bool,
        nrmse: bool,
        spearmancorr: bool,
        all: bool,
    ) -> list[str]:
        if not any([mse, mae, r2, mape, rmse, nrmse, spearmancorr, all]):
            all = True

        metrics_names = [
            "mse" if mse or all else None,
            "mae" if mae or all else None,
            "r2" if r2 or all else None,
            "mape" if mape or all else None,
            "rmse" if rmse or all else None,
            "nrmse" if nrmse or all else None,
            "spearman_correlation" if spearmancorr or all else None,
        ]
        return list(filter(None, metrics_names))
