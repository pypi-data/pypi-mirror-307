import dataclasses
import shutil
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import httpx
import prodigy.recipes.train
import prodigy_teams_recipes_sdk.prodigy_teams_pam_sdk.models as pam_models
import srsly
from cloudpathlib import AnyPath, CloudPath
from prodigy.errors import RecipeError
from prodigy.util import msg
from prodigy_teams_recipes_sdk import (
    BlankModel,
    BoolProps,
    FloatProps,
    InputDataset,
    IntProps,
    ListProps,
    Model,
    OptionalProps,
    TextProps,
)
from prodigy_teams_recipes_sdk import __version__ as pt_recipes_sdk_version
from prodigy_teams_recipes_sdk import action_recipe, resolve_remote_path, teams_type
from prodigy_teams_recipes_sdk.prodigy_teams_pam_sdk.errors import ProdigyTeamsError
from prodigy_teams_recipes_sdk.prodigy_teams_pam_sdk.recipe_client import (
    Settings,
    get_pam_client,
)

# TODO: allow custom config


@teams_type(
    title="Training data",
    description="Annotated data for the different components to train",
    field_props={
        # fmt: off
        "training": ListProps(title="Training datasets", exists=True, min=1),
        "evaluation": ListProps(title="Optional datasets to evaluate on", description="If no datasets are provided, a portion of the training data (defined as the eval split) is held back for evaluation", exists=True, min=0),
        # fmt: on
    },
)
@dataclasses.dataclass
class ComponentData:
    training: List[InputDataset]
    evaluation: Optional[List[InputDataset]] = None

    def load(self) -> Tuple[List[str], List[str]]:
        return (
            [str(d.name) for d in self.training],
            [str(d.name) for d in self.evaluation]
            if self.evaluation is not None
            else [],
        )


@teams_type(
    field_props={
        # fmt: off
        "ner": OptionalProps(title="Named Entity Recognizer datasets", optional_title="Train a Named Entity Recognizer"),
        "spancat": OptionalProps(title="Span Categorizer datasets", optional_title="Train a Span Categorizer"),
        "textcat": OptionalProps(title="Text Classifier (exclusive categories) datasets", optional_title="Train a Text Classifier (exclusive categories)"),
        "textcat_multilabel": OptionalProps(title="Text Classifier (non-exclusive categories) datasets", optional_title="Train a Text Classifier (non-exclusive categories)"),
        "tagger": OptionalProps(title="Part-of-speech Tagger datasets", optional_title="Train a Part-of-speech Tagger"),
        "parser": OptionalProps(title="Dependency Parser datasets", optional_title="Train a Dependency Parser"),
        "senter": OptionalProps(title="Sentence Segmenter datasets", optional_title="Train a Sentence Segmenter"),
        "coref": OptionalProps(title="Coreference Resolution datasets", optional_title="Train a Coreference Resolution component"),
        # fmt: on
    }
)
@dataclasses.dataclass
class Data:
    ner: Optional[ComponentData] = None
    spancat: Optional[ComponentData] = None
    textcat: Optional[ComponentData] = None
    textcat_multilabel: Optional[ComponentData] = None
    tagger: Optional[ComponentData] = None
    parser: Optional[ComponentData] = None
    senter: Optional[ComponentData] = None
    coref: Optional[ComponentData] = None

    def load(self) -> Dict[str, Tuple[List[str], List[str]]]:
        pipes = {}
        for field in dataclasses.fields(self):
            value = getattr(self, field.name)
            if value is not None:
                pipes[field.name] = value.load()
        return pipes


@teams_type(
    title="Train Curve mode",
    field_props={
        # fmt: off
        "n_samples": IntProps(title="Number of samples to take", description="For example, 4 samples to train with 25, 50 and 100%", min=1, step=1),
        "show_plot": BoolProps(title="Show a visual plot of the curve in the logs"),
        # fmt: on
    },
)
class TrainCurve:
    n_samples: int = 1
    show_plot: bool = False


@teams_type(
    title="Register Model",
    field_props={
        "name": TextProps(
            title="Model Name",
            description="Name to register model with in Prodigy Teams.",
        ),
        "path": TextProps(title="Model Path", description="Path to upload model to."),
        "version": TextProps(
            title="Model Version", description="Semantic version to save model as"
        ),
        "asset_kind": TextProps(
            title="Asset Kind",
            description="Kind of asset to register model as. Defaults to 'model'.",
        ),
    },
)
class ModelRegistrationSettings:
    name: str
    path: str
    version: str = "0.1.0"
    asset_kind: str = "model"


COMPONENTS = [f.name for f in dataclasses.fields(Data)]


@action_recipe(
    title="Train a spaCy pipeline",
    description="Train a spaCy model with one or more components on annotated data",
    field_props={
        # fmt: off
        "base_model": TextProps(
            title="Base model", description="Base model to use for training. If not provided, a blank model will be used."
        ),
        "eval_split": FloatProps(title="Portion of examples to split off for evaluation", description="This is applied if no dedicated evaluation datasets are provided for a component.", min=0.0, max=1.0, step=0.05),
        "label_stats": BoolProps(title="Show per-label scores", description="Will output an additional table for each component with scores for the individual labels"),
        "verbose": BoolProps(title="Enable verbose logging"),
        "train_curve": OptionalProps(title="Train curve", description="Train with different portions of the data to simulate how the model improves with more data", optional_title="Enable train curve diagnostics"),
        "output": OptionalProps(title="Model to Register", description="Register model with Prodigy Teams", optional_title="Enable model registration"),
        "config_overrides": ListProps(title="Config overrides", description="Override config values for training", exists=False, min=0),
        # fmt: on
    },
    cli_names={
        **{f"data.{c}.training": f"{c}.train" for c in COMPONENTS},
        **{f"data.{c}.evaluation": f"{c}.eval" for c in COMPONENTS},
        "base-model-model": "base-model",
        "base-model-blank.lang": "lang",
    },
)
def train(
    *,
    data: Data,
    base_model: Union[BlankModel, Model] = BlankModel("en"),
    eval_split: float = 0.2,
    label_stats: bool = False,
    verbose: bool = False,
    train_curve: Optional[TrainCurve] = None,
    output: Optional[ModelRegistrationSettings] = None,
    config_overrides: Optional[List[str]] = None,
) -> None:
    """
    Train a spaCy pipeline from one or more datasets for different components
    or run training diagnostics to check if more annotations improve the model.
    """
    config_overrides_dict = _parse_config_overrides(config_overrides or [])
    prodigy.recipes.train.set_log_level(verbose=verbose)
    pipes = data.load()
    if not pipes:
        raise RecipeError("No components to train")
    elif train_curve is not None and train_curve.n_samples > 1:
        prodigy.recipes.train._train_curve(
            pipes,
            eval_split=eval_split,
            n_samples=train_curve.n_samples,
            show_plot=train_curve.show_plot,
            overrides=config_overrides_dict,
        )
    else:

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_dir = Path(tmp_dir)
            if isinstance(base_model, BlankModel):
                train_config = prodigy.recipes.train._prodigy_config(
                    pipes,
                    None,
                    lang=base_model.lang,
                    eval_split=eval_split,
                    verbose=verbose,
                )
            elif isinstance(base_model, Model):
                base_nlp = base_model.load(download_to=tmp_dir / "__base_model__")
                base_nlp.lang
                train_config = prodigy.recipes.train._prodigy_config(
                    pipes,
                    None,
                    lang=base_nlp.vocab.lang,
                    eval_split=eval_split,
                    base_model=str(base_nlp.path),
                    verbose=verbose,
                )
            else:
                raise TypeError(f"Unexpected type for base_model: {base_model}")

            prodigy.recipes.train._train(
                train_config,
                output_dir=tmp_dir,
                overrides=config_overrides_dict,
                gpu_id=-1,
                show_label_stats=label_stats,
            )

            if output is not None:
                msg.info("Starting Model Registration")
                _register_model(output, tmp_dir)


def _register_model(model_registration: ModelRegistrationSettings, base_dir: Path):
    cfg = Settings()
    if not cfg.validate():
        raise ValueError("Invalid Prodigy Teams Client Settings.", cfg)
    assert cfg.broker_id

    pam_client = get_pam_client(cfg.pam_host, cfg.pam_token)
    msg.info(f"Uploading model to {model_registration.path}")

    resolved_path = resolve_remote_path(
        pam_client, model_registration.path, cfg.broker_id
    )
    dest = AnyPath(resolved_path)

    if isinstance(dest, CloudPath):
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.upload_from(base_dir / "model-best", force_overwrite_to_cloud=True)
    else:
        assert isinstance(dest, Path)
        shutil.copytree(base_dir / "model-best", dest, dirs_exist_ok=True)

    msg.good(f"Uploaded model to {model_registration.path}")
    body = pam_models.AssetCreating(
        broker_id=cfg.broker_id,
        name=model_registration.name,
        version=model_registration.version,
        path=model_registration.path,
        kind=model_registration.asset_kind,
        meta={
            "prodigy_teams_recipes_sdk_version": pt_recipes_sdk_version,
        },
    )
    try:
        pam_client.asset.create(body)
    except ProdigyTeamsError as e:
        msg.fail("Failed to register new Asset with Prodigy Teams.", e, exits=1)
    except httpx.HTTPStatusError as e:
        msg.fail(
            "Unexpected error when registering new Asset with Prodigy Teams.",
            e,
            exits=1,
        )
    else:
        msg.good(
            f"Asset {model_registration.name} successfully registered with Prodigy Teams"
        )


def _parse_config_overrides(overrides: List[str]) -> Dict[str, str]:
    config_overrides = {}
    for arg in overrides:
        if "=" not in arg:
            raise RecipeError(
                "Error parsing Config Overrides. Each override must be in the form of key=value\n\n"
                "e.g. training.max_epochs=10."
            )
        else:
            key, value = arg.split("=", 1)
            config_overrides[key] = _parse_override(value)
    return config_overrides


def _parse_override(value: Any) -> Any:
    # Just like we do in the config, we're calling json.loads on the
    # values. But since they come from the CLI, it'd be unintuitive to
    # explicitly mark strings with escaped quotes. So we're working
    # around that here by falling back to a string if parsing fails.
    # TODO: improve logic to handle simple types like list of strings?
    try:
        return srsly.json_loads(value)
    except ValueError:
        return str(value)
