import os
import shutil

import click

from finter.framework_model.submission.config import get_model_info
from finter.framework_model.submission.helper_poetry import get_docker_file_content
from finter.framework_model.submission.helper_submission import submit_model
from finter.framework_model.validation import ValidationHelper


@click.group()
def finter():
    """Finter CLI - A tool for submitting models with specific configurations."""
    pass


@finter.command()
@click.option(
    "--universe",
    required=True,
    type=click.Choice(
        [
            "kr_stock",
            "us_etf",
            "us_stock",
            "vn_stock",
            "vn_stock_deprecated",
            "id_stock",
            "crypto_spot_binance",
        ],
        case_sensitive=False,
    ),
    help="The name of the universe (required).",
)
@click.option(
    "--gpu", required=False, is_flag=True, help="Whether to use GPU machine (optional)."
)
@click.option(
    "--image-tag",
    required=False,
    type=click.Choice(["2.1.0-gpu"], case_sensitive=False),
    help="Choose the SageMaker image tag (only applicable if GPU is true).",
)
@click.option(
    "--machine",
    required=False,
    type=click.Choice(["g4dn.2xlarge"], case_sensitive=False),
    help="Choose the machine type (only applicable if GPU is true).",
)
@click.option(
    "--poetry-path",
    required=False,
    type=str,
    help="Path to the directory containing the Poetry 'pyproject.toml' and 'poetry.lock' files to be copied to the current working directory (Optional). This option is not needed if these files already exist in the current workspace. If submitting for GPU tasks, specify only the additional packages required for the SageMaker image.",
)
@click.option(
    "--custom-docker-file",
    required=False,
    is_flag=True,
    help="Whether to use custom docker file (optional). If not provided, an appropriate Dockerfile will be generated.",
)
@click.option(
    "--start",
    required=False,
    type=int,
    help="Start date for submission in YYYYMMDD format (optional). If not provided, the system will automatically calculate the start date during submission.",
)
@click.option(
    "--staging",
    required=False,
    is_flag=True,
    help="Whether to use staging environment (optional).",
)
def submit(
    universe,
    gpu,
    image_tag,
    machine,
    poetry_path,
    custom_docker_file,
    start,
    staging,
):
    current_dir = os.getcwd()
    click.echo(f"Current working directory: {current_dir}")

    model_alias = os.path.basename(current_dir)
    click.echo(f"Model alias: {model_alias}")

    model_files = [
        f for f in os.listdir(current_dir) if f in ["am.py", "pm.py", "ffd.py"]
    ]

    if len(model_files) != 1:
        click.echo(
            "Error: Exactly one model file (am.py, pm.py, ffd.py) must exist.",
            err=True,
        )
        return

    model_file = model_files[0]

    model_type = {"am.py": "alpha", "pm.py": "portfolio", "ffd.py": "flexible_fund"}[
        model_file
    ]

    click.echo(f"Model type: {model_type}")

    if poetry_path:
        click.echo(f"Copying Poetry files from {poetry_path} to current directory...")
        poetry_source_file = os.path.join(poetry_path, "pyproject.toml")
        poetry_source_lock = os.path.join(poetry_path, "poetry.lock")

        if not os.path.exists(poetry_source_file) or not os.path.exists(
            poetry_source_lock
        ):
            click.echo(
                f"Error: 'pyproject.toml' or 'poetry.lock' file not found in {poetry_path}",
                err=True,
            )
            return

        try:
            shutil.copy2(poetry_source_file, current_dir)
            shutil.copy2(poetry_source_lock, current_dir)
            click.echo("Poetry files copied successfully")
        except Exception as e:
            click.echo(f"Error copying Poetry files: {e}", err=True)
            return

    poetry_file = os.path.join(current_dir, "pyproject.toml")
    poetry_lock_file = os.path.join(current_dir, "poetry.lock")

    if not os.path.exists(poetry_file) or not os.path.exists(poetry_lock_file):
        click.echo(
            "Error: 'pyproject.toml' or 'poetry.lock' file not found. Please ensure both exist in the current directory.",
            err=True,
        )
        return

    if gpu:
        if not image_tag or not machine:
            click.echo(
                "Error: Both image_tag and machine must be specified when GPU is true.",
                err=True,
            )
            return

        image = f"sagemaker-distribution:{image_tag}"
        docker_file_content = get_docker_file_content(gpu, image)
        click.echo(
            f"Submitting model: {model_alias}, using GPU with image: {image} and machine: {machine}."
        )
    else:
        if image_tag or machine:
            click.echo(
                "Warning: Image and machine options are ignored when GPU is not used."
            )
        docker_file_content = get_docker_file_content(gpu)
        click.echo(f"Submitting model: {model_alias}")

    docker_file = os.path.join(current_dir, "Dockerfile")

    if custom_docker_file:
        if not os.path.exists(docker_file):
            click.echo(
                "Error: 'Dockerfile' file not found. Please ensure it exists in the current directory.",
                err=True,
            )
            return
    else:
        with open(docker_file, "w") as file:
            file.write(docker_file_content)

        click.echo(f"Dockerfile saved to {docker_file}")

    model_info = get_model_info(universe, model_type)

    model_info["gpu"] = gpu
    if start:
        model_info["start"] = start

    validator = ValidationHelper(model_path=current_dir, model_info=model_info)
    validator.validate()

    submit_result = submit_model(
        model_info=model_info,
        output_directory=current_dir,
        docker_submit=True,  # docker_submit=False is deprecated
        staging=staging,
        model_nickname=model_alias,
    )

    click.echo(
        "Validation URL: "
        + click.style(submit_result.s3_url, fg="blue", underline=True)
    )


if __name__ == "__main__":
    finter()
