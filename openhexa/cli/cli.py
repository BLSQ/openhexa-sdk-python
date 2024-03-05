"""CLI module, with click."""

import base64
import json
import sys
from importlib.metadata import version
from pathlib import Path

import click

from openhexa.cli.api import (
    APIError,
    InvalidDefinitionError,
    NoActiveWorkspaceError,
    OutputDirectoryError,
    create_pipeline,
    create_pipeline_structure,
    delete_pipeline,
    download_pipeline_sourcecode,
    ensure_is_pipeline_dir,
    ensure_pipeline_config_exists,
    get_pipeline,
    get_workspace,
    list_pipelines,
    upload_pipeline,
)
from openhexa.cli.settings import settings
from openhexa.sdk.pipelines import get_local_workspace_config
from openhexa.sdk.pipelines.exceptions import PipelineNotFound
from openhexa.sdk.pipelines.runtime import get_pipeline_metadata


@click.group()
@click.version_option(version("openhexa.sdk"))
@click.pass_context
def app(ctx):
    """OpenHEXA CLI."""
    # ensure that ctx.obj exists and is a dict (in case `cli()` is called
    # by means other than the `if` block below)
    ctx.ensure_object(dict)


@app.group(invoke_without_command=True)
@click.pass_context
def workspaces(ctx):
    """Manage workspaces (add workspace, remove workspace, list workspaces, activate a workspace)."""
    if ctx.invoked_subcommand is None:
        ctx.forward(workspaces_list)


@workspaces.command(name="add")
@click.argument("slug")
@click.option("--token", prompt=True, hide_input=True, confirmation_prompt=False, envvar="HEXA_TOKEN")
def workspaces_add(slug, token):
    """Add a workspace to the configuration and activate it. The access token is required to access the workspace."""
    if slug in settings.workspaces:
        click.echo(f"Workspace {slug} already exists. We will only update its token.")
    else:
        click.echo(f"Adding workspace {slug}")
    try:
        get_workspace(slug, token)
        settings.add_workspace(slug, token)
    except APIError as e:
        _terminate(
            f"Workspace {slug} does not exist on {settings.api_url}.",
            exception=e,
            err=True,
        )


@workspaces.command(name="activate")
@click.argument("slug")
def workspaces_activate(slug):
    """Activate a workspace that is already in the configuration. The activated workspace will be used for the 'pipelines' commands."""
    try:
        settings.activate(slug)
        click.echo(f"Current workspace set to {click.style(slug, bold=True)}")
    except ValueError:
        _terminate(
            f"Workspace {slug} does not exist on {settings.api_url}. Available workspaces:\n {', '.join(settings.workspaces.keys())}"
        )


@workspaces.command(name="list")
def workspaces_list():
    """List the workspaces in the configuration."""
    click.echo("Workspaces:")
    for slug in settings.workspaces.keys():
        click.echo(click.style(f"* {slug} (active)", bold=True) if slug == settings.current_workspace else f"* {slug}")


@workspaces.command(name="rm")
@click.argument("slug")
def workspaces_rm(slug):
    """Remove a workspace from the configuration.

    SLUG is the slug of the workspace to remove from the configuration.
    """
    if slug not in settings.workspaces:
        click.echo(f"Workspace {slug} does not exist")
        return
    click.echo(f"Removing workspace {slug}")

    settings.remove_workspace(slug)


@app.group(invoke_without_command=True)
@click.pass_context
def config(ctx):
    """Manage configuration of the CLI."""
    if ctx.invoked_subcommand is None:
        click.echo("Debug: " + ("True" if settings.debug else "False"))
        click.echo(f"Backend URL: {settings.api_url}")
        try:
            click.echo(f"Current workspace: {settings.current_workspace}")
        except KeyError:
            click.echo("No current workspace")
        click.echo("\nWorkspaces:")
        click.echo("\n".join(settings.workspaces.keys()))


@config.command(name="set_url")
@click.argument("url")
def config_set_url(url):
    """Set the URL of the backend."""
    settings.set_api_url(url)
    click.echo(f"Set backend URL to {settings.api_url}")


@app.group(invoke_without_command=True)
@click.pass_context
def pipelines(ctx):
    """Manage pipelines (list pipelines, push a pipeline to the backend)."""
    if ctx.invoked_subcommand is None:
        ctx.forward(pipelines_list)


@pipelines.command("init")
@click.argument("name", type=str)
def pipelines_init(name: str):
    """Initialize a new pipeline in a fresh directory."""
    try:
        pipeline_directory = create_pipeline_structure(name, Path.cwd())
    except ValueError:
        _terminate(
            f"Error while creating pipeline {name}. The directory already exists. Please choose a different name for your pipeline.",
            err=True,
        )
    else:
        # Success
        click.echo(f"{click.style('Success!', fg='green')} Your pipeline has been created in {pipeline_directory}")


@pipelines.command("push")
@click.argument(
    "path",
    default=".",
    type=click.Path(
        exists=True,
        path_type=Path,
        file_okay=False,
        dir_okay=True,
    ),
)
def pipelines_push(path: str, yes: bool = False):
    """Push a pipeline to the backend. If the pipeline already exists, it will be updated otherwise it will be created.

    PATH is the path to the pipeline file.
    """
    workspace = settings.current_workspace
    if workspace is None:
        _terminate(
            "No workspace activated. Use openhexa workspaces add or openhexa workspaces activate to "
            "activate a workspace.",
            err=True,
        )

    ensure_is_pipeline_dir(path)

    try:
        pipeline = get_pipeline_metadata(path)
    except PipelineNotFound:
        click.echo(
            f"No function with openhexa.sdk pipeline decorator found in {click.style(path, bold=True)}.",
            err=True,
        )
        sys.exit(1)
    except Exception as e:
        _terminate(f'Error while importing pipeline: "{e}"', exception=e, err=True)
    else:
        workspace_pipelines = list_pipelines()
        if settings.debug:
            click.echo(workspace_pipelines)

        if get_pipeline(pipeline.code) is None:
            click.echo(
                f"Pipeline {click.style(pipeline.code, bold=True)} does not exist in workspace {click.style(workspace, bold=True)}"
            )
            if not yes:
                # Ask for confirmation
                click.confirm(
                    f"Create pipeline {click.style(pipeline.code, bold=True)} in workspace {click.style(workspace, bold=True)}?",
                    True,
                    abort=True,
                )
            create_pipeline(pipeline.code, pipeline.name)

        click.echo(
            f"Pushing pipeline {click.style(pipeline.code, bold=True)} to workspace {click.style(workspace, bold=True)}"
        )

        try:
            new_version = upload_pipeline(path)
            click.echo(f"New version created: {new_version}")

            click.echo(
                f"Done! You can view the pipeline in OpenHEXA on {click.style(f'{settings.public_api_url}/workspaces/{workspace}/pipelines/{pipeline.code}', fg='bright_blue', underline=True)}"
            )
        except InvalidDefinitionError as e:
            _terminate(
                f'Pipeline definition is invalid: "{e}"',
                err=True,
                exception=e,
            )
        except Exception as e:
            _terminate(
                f'Error while importing pipeline: "{e}"',
                err=True,
                exception=e,
            )


@pipelines.command("download")
@click.argument("code", type=str)
@click.argument(
    "output",
    type=click.Path(path_type=Path),
    default=".",
)
def pipelines_download(code: str, output: Path):
    """Download a pipeline and unzip it at the output path given."""
    try:
        force_overwrite = False
        if output.exists() and output.is_dir() and any(output.iterdir()):
            force_overwrite = click.confirm(
                f"Directory {click.style(output.absolute(), bold=True)} is not empty. Overwrite the files?"
            )
        download_pipeline_sourcecode(code, output, force_overwrite)
        click.echo(f"You can find the pipeline source code in '{click.style(output.absolute(), bold=True)}'")
    except OutputDirectoryError as e:
        click.echo(
            str(e),
            err=True,
        )
        sys.exit(1)
    except NoActiveWorkspaceError:
        click.echo(
            "No workspace activated. Use openhexa workspaces add or openhexa workspaces activate to "
            "activate a workspace.",
            err=True,
        )
        sys.exit(1)


@pipelines.command("delete")
@click.argument("code", type=str)
def pipelines_delete(code: str):
    """Delete a pipeline and all his versions."""
    if settings.current_workspace is None:
        _terminate(
            "No workspace activated. Use openhexa workspaces add or openhexa workspaces activate to "
            "activate a workspace.",
            err=True,
        )
    else:
        pipeline = get_pipeline(code)
        if pipeline is None:
            click.echo(
                f"Pipeline {click.style(code, bold=True)} does not exist in workspace {click.style(settings.current_workspace, bold=True)}"
            )
            sys.exit(1)

        confirmation_code = click.prompt(
            f'This will remove the pipeline "{click.style(code, bold=True)}" from the "{click.style(settings.current_workspace, bold=True)} workspace. This operation cannot be undone.\nPlease enter "{click.style(code, bold=True)}" to confirm',
            type=str,
        )

        if confirmation_code != code:
            click.echo(
                "Pipeline code and confirmation are different, aborted.",
                err=True,
            )
            sys.exit(1)

        try:
            if delete_pipeline(pipeline["id"]):
                click.echo(f"Pipeline {click.style(code, bold=True)} deleted.")

        except Exception as e:
            _terminate(
                f'Error while deleting pipeline: "{e}"',
                err=True,
                exception=e,
            )


@pipelines.command("run")
@click.argument("path", default=".", type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path))
@click.option("-c", "config_str", type=str, help="Configuration JSON as a string")
@click.option(
    "-f",
    "config_file",
    type=click.File("r"),
    default=None,
    help="Configuration JSON file",
)
@click.option(
    "--image",
    type=str,
    help="Docker image to use",
    default="blsq/openhexa-blsq-environment:latest",
)
def pipelines_run(
    path: str,
    image: str,
    config_str: str = "{}",
    config_file: click.File = None,
):
    """Run a pipeline locally."""
    from subprocess import Popen

    path = Path(path)
    ensure_is_pipeline_dir(path)
    ensure_pipeline_config_exists(path)
    env_vars = get_local_workspace_config(path)

    # # Prepare the mount for the workspace's files
    mount_files_path = Path(env_vars["WORKSPACE_FILES_PATH"]).absolute()
    cmd = [
        "docker",
        "run",
        "--mount",
        f"type=bind,source={Path(path).absolute()},target=/home/hexa/pipeline",
        "--mount",
        f"type=bind,source={mount_files_path},target=/home/hexa/workspace",
        "--env",
        "HEXA_ENVIRONMENT=local_pipeline",
        "--env",
        f"HEXA_WORKSPACE={settings.current_workspace}",
        "--platform",
        "linux/amd64",
        "--rm",
        "--pull",
        "always",
    ]

    image = env_vars["WORKSPACE_DOCKER_IMAGE"] if env_vars.get("WORKSPACE_DOCKER_IMAGE") else image

    cmd.extend(
        [
            image,
            "pipeline",
            "run",
        ]
    )

    if config_str and config_file:
        click.echo("You can't specify both -c and -f", err=True)
        return click.Abort()

    config = config_str or "{}"
    if config_file:
        config = json.dumps(json.loads(config_file.read(), strict=False))

    cmd.extend(["--config", base64.b64encode(config.encode("utf-8")).decode("utf-8")])

    if settings.debug:
        print(" ".join(cmd))

    proc = Popen(
        cmd,
        close_fds=True,
    )
    return proc.wait()


@pipelines.command("list")
def pipelines_list():
    """List all the remote pipelines of the current workspace."""
    if settings.current_workspace is None:
        _terminate("No workspace activated", err=True)

    workspace_pipelines = list_pipelines()
    if len(workspace_pipelines) == 0:
        click.echo(f"No pipelines in workspace {settings.current_workspace}")
        return
    click.echo("Pipelines:")
    for pipeline in workspace_pipelines:
        current_version = pipeline["currentVersion"].get("number")
        if current_version is not None:
            current_version = f"v{current_version}"
        else:
            current_version = "N/A"
        click.echo(f"* {pipeline['code']} - {pipeline['name']} ({current_version})")


def _terminate(message: str, exception: Exception = None, err: bool = False):
    click.echo(message, err=err)
    if settings.debug and exception:
        raise exception
    click.Abort()
