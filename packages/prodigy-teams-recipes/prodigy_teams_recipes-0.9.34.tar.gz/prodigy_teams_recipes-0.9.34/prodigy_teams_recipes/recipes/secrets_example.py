import os
from typing import List, Literal, Optional

from prodigy.types import RecipeSettingsType
from prodigy_teams_recipes_sdk import (
    Dataset,
    IntProps,
    ListProps,
    Secret,
    props,
    task_recipe,
)


@task_recipe(
    title="Secrets Example",
    description="Annotate 'hello world'",
    field_props={
        "dataset": props.dataset_choice,
        "n_examples": IntProps(title="Number of examples to generate", min=1),
        "secrets": ListProps(
            name="secrets",
            title="Secrets",
            description="Add secrets as Environment Variables for this task.",
            exists=True,
        ),
    },
)
def secrets_example(
    *,
    dataset: Dataset[Literal["text"]],
    n_examples: int = 100,
    secrets: Optional[List[Secret]] = None,
) -> RecipeSettingsType:

    # Access Secrets directly using `Secret.get_secret_value`
    # if secrets:
    #     for secret in secrets:
    #         print(secret.name, secret.get_secret_value("MY_ENV_VAR_KEY"))

    # Access Secrets as normal Environment Variables
    secret_val = os.getenv("MY_SECRET")
    print("Value of MY_SECRET from Environment Variable", secret_val)

    stream = ({"text": f"hello world {i}"} for i in range(n_examples))
    return {
        "dataset": dataset.name if isinstance(dataset, Dataset) else dataset,
        "stream": stream,
        "view_id": "text",
    }
