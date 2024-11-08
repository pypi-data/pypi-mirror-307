from pyoneai.session import Session
from pyoneai_ops.mlops.const import SupportedModels
from pyoneai_ops.mlops.core.training import (
    train_model_on_real,
    train_model_on_syntehtic,
)
from pyoneai_ops.utils import handle_missing_config

from . import console, log


class TrainProcessor:

    def __init__(
        self,
        console,
        entity: str,
        metric: str,
        period: str,
        path: str,
        scenario: str | None,
        model: str | None,
    ):
        self.session = Session()
        self.console = console
        self.entity = entity
        self.metric = metric
        self.period = period
        self.path = path
        self.scenario = scenario
        model = self._maybe_get_default_model(model)
        self.model: SupportedModels = SupportedModels.get(model)

    def _maybe_get_default_model(self, model: str | None) -> str:
        """Get the default model defined in the registry, if not specified."""
        if model is not None:
            return model
        return self.session.config.registry["default"]["prediction"]["class"]

    @handle_missing_config
    def run(self):

        with self.console.status("Training the model...") as status:
            self.console.log("Session created.")

            status.update("Prepare model...")
            if self.scenario:
                status.update(
                    f"Training a model: {self.model.name} on the "
                    f"synthetic data from profile '{self.scenario}'..."
                )
                train_model_on_syntehtic(
                    session=self.session,
                    entity=self.entity,
                    metric_name=self.metric,
                    period=self.period,
                    scenario=self.scenario,
                    model=self.model,
                    path=self.path,
                )
            else:
                status.update(
                    f"Training a model: {self.model.name} on real "
                    "OpenNebula Prometheus metrics..."
                )
                train_model_on_real(
                    session=self.session,
                    entity=self.entity,
                    metric_name=self.metric,
                    period=self.period,
                    model=self.model,
                    path=self.path,
                )
