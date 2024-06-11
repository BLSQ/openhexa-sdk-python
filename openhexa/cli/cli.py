"""CLI module, with click."""

import json
import signal
from datetime import datetime
from importlib.metadata import version
from pathlib import Path
from urllib.parse import urlparse

import click

from openhexa.cli.api import (
    DockerError,
    InvalidDefinitionError,
    NoActiveWorkspaceError,
    OutputDirectoryError,
    PipelineDirectoryError,
    create_pipeline,
    create_pipeline_structure,
    delete_pipeline,
    download_pipeline_sourcecode,
    ensure_is_pipeline_dir,
    get_library_versions,
    get_pipeline,
    get_workspace,
    list_pipelines,
    run_pipeline,
    upload_pipeline,
)
from openhexa.cli.settings import settings, setup_logging
from openhexa.sdk.pipelines.exceptions import PipelineNotFound
from openhexa.sdk.pipelines.runtime import get_pipeline_metadata


def validate_url(ctx, param, value):
    """Validate URL format."""
    if value is not None:
        parsed_url = urlparse(value)
        if parsed_url.scheme in ("http", "https") and parsed_url.netloc:
            return value
        else:
            raise click.BadParameter("Invalid URL format. Please provide a valid HTTP or HTTPS URL.")


@click.group()
@click.version_option(version("openhexa.sdk"))
@click.pass_context
def app(ctx):
    """OpenHEXA CLI."""
    # ensure that ctx.obj exists and is a dict (in case `cli()` is called
    # by means other than the `if` block below)
    setup_logging()
    ctx.ensure_object(dict)

    # Check if the version is outdated and warns the user if it's the case
    ONE_HOUR = 60 * 60
    now_timestamp = int(datetime.now().timestamp())
    if settings.last_version_check is None or now_timestamp - settings.last_version_check > ONE_HOUR:
        installed_version, latest_version = get_library_versions()
        settings.last_version_check = now_timestamp
        if installed_version != latest_version or True:
            click.secho(
                "\n".join(
                    (
                        "╔════════════════════════════════════════════════════════════════════════════════════════╗",
                        f"║ 🚨 Your OpenHEXA CLI version is outdated. Please update to the latest version ({latest_version}) ║",
                        "║ $ pip install --upgrade openhexa.sdk                                                   ║",
                        "╚════════════════════════════════════════════════════════════════════════════════════════╝",
                        "",
                    )
                ),
                fg="yellow",
            )


@app.group(invoke_without_command=True)
@click.pass_context
def workspaces(ctx):
    """Manage workspaces (add workspace, remove workspace, list workspaces, activate a workspace)."""
    if ctx.invoked_subcommand is None:
        ctx.forward(workspaces_list)


@workspaces.command(name="add")
@click.argument("slug")
@click.option(
    "--token",
    prompt=True,
    hide_input=True,
    confirmation_prompt=False,
    envvar="HEXA_TOKEN",
)
def workspaces_add(slug, token):
    """Add a workspace to the configuration and activate it. The access token is required to access the workspace."""
    if slug in settings.workspaces:
        click.echo(f"Workspace {slug} already exists. We will only update its token.")
    else:
        click.echo(f"Adding workspace {slug}")
    if get_workspace(slug, token):
        settings.add_workspace(slug, token)
    else:
        _terminate(
            f"Workspace {slug} does not exist on {settings.api_url}.",
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
        click.echo(f"Current workspace: {settings.current_workspace}")
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
    click.echo(f"Creating pipeline {name}...")
    workflow_mode = None
    modes = [
        ("push", "Push the pipeline on new commits on main"),
        ("release", "Push the pipeline when a git tag is created"),
        ("manual", "Push the pipeline manually from GitHub actions"),
    ]
    if click.confirm(
        "Do you want to create a workflow to publish the pipeline to OpenHEXA from GitHub?",
        default=True,
    ):
        if settings.current_workspace is None:
            _terminate(
                "No workspace activated. Use openhexa workspaces add or openhexa workspaces activate to "
                "activate a workspace.",
                err=True,
            )

        click.echo("Select the trigger for the GitHub action:")
        for idx, (mode, text) in enumerate(modes):
            click.echo(f" {click.style(idx + 1, bold=True)}: ({click.style(mode, bold=True)}) {text}")
        mode_choice = click.prompt("Select a mode", type=click.IntRange(min=1, max=3), default=1)
        workflow_mode = modes[mode_choice - 1][0]
    try:
        pipeline_directory = create_pipeline_structure(
            name,
            Path.cwd(),
            workspace=settings.current_workspace,
            workflow_mode=workflow_mode,
        )

        if workflow_mode:
            click.echo(
                f"Github workflow created. Please add your OpenHEXA pipeline token to the secrets of your repository with the key '{click.style('OH_TOKEN', bold=True)}'."
            )
    except ValueError:
        _terminate(
            click.style(
                f"\n❌ Error while creating pipeline {name}. The directory already exists. Please choose a different name for your pipeline.",
                fg="red",
            ),
            err=True,
        )
    else:
        # Success
        click.echo("")
        click.echo(
            f"{click.style('✅ Success!', fg='green')} Your pipeline has been created in {click.style(pipeline_directory, underline=True, fg='bright_blue')}"
        )


@pipelines.command("push")
@click.argument(
    "path",
    type=click.Path(
        exists=True,
        path_type=Path,
        file_okay=False,
        dir_okay=True,
    ),
)
@click.option(
    "--name",
    "-n",
    type=str,
    help="Name of the version",
    prompt="Name of the version",
    required=True,
)
@click.option(
    "--description",
    "-d",
    default=None,
    type=str,
    help="Description of the version",
    prompt="Description of the version",
    prompt_required=False,
)
@click.option(
    "--link",
    "-l",
    type=str,
    callback=validate_url,
    help="Link to the version commit",
    prompt="Link of the version release",
    prompt_required=False,
)
@click.option("--yes", is_flag=True, help="Skip confirmation")
def pipelines_push(
    path: str,
    name: str,
    description: str = None,
    link: str = None,
    yes: bool = False,
):
    """Push a pipeline to the backend. If the pipeline already exists, it will be updated otherwise it will be created.

    PATH is the path to the pipeline file.
    """
    workspace = settings.current_workspace
    if workspace is None:
        _terminate(
            "❌ No workspace activated. Use openhexa workspaces add or openhexa workspaces activate to "
            "activate a workspace.",
            err=True,
        )

    ensure_is_pipeline_dir(path)

    try:
        pipeline = get_pipeline_metadata(path)
    except PipelineNotFound:
        _terminate(
            f"❌ No function with openhexa.sdk pipeline decorator found in {click.style(path, bold=True)}.",
            err=True,
        )
    except Exception as e:
        _terminate(f'❌ Error while importing pipeline: "{e}"', exception=e, err=True)
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
        elif not yes:
            click.confirm(
                f"Pushing pipeline {click.style(pipeline.code, bold=True)} to workspace {click.style(workspace, bold=True)} with name {click.style(name, bold=True)}?",
                True,
                abort=True,
            )

        try:
            upload_pipeline(path, name, description=description, link=link)
            click.echo(
                click.style(
                    f"✅ New version '{name}' created! You can view the pipeline in OpenHEXA on {click.style(f'{settings.public_api_url}/workspaces/{workspace}/pipelines/{pipeline.code}', fg='bright_blue', underline=True)}",
                    fg="green",
                )
            )
        except InvalidDefinitionError as e:
            _terminate(
                f'❌ Pipeline definition is invalid: "{e}"',
                err=True,
                exception=e,
            )
        except Exception as e:
            _terminate(
                f'❌ Error while importing pipeline: "{e}"',
                err=True,
                exception=e,
            )


@pipelines.command("download")
@click.argument("code", type=str)
@click.argument(
    "output",
    type=click.Path(path_type=Path),
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
        _terminate(str(e), err=True, exception=e)
    except NoActiveWorkspaceError:
        _terminate(
            "❌ No workspace activated. Use openhexa workspaces add or openhexa workspaces activate to "
            "activate a workspace.",
            err=True,
        )


@pipelines.command("delete")
@click.argument("code", type=str)
def pipelines_delete(code: str):
    """Delete a pipeline and all his versions."""
    if settings.current_workspace is None:
        _terminate(
            "❌ No workspace activated. Use openhexa workspaces add or openhexa workspaces activate to "
            "activate a workspace.",
            err=True,
        )
    else:
        pipeline = get_pipeline(code)
        if pipeline is None:
            _terminate(
                f"❌  Pipeline {click.style(code, bold=True)} does not exist in workspace {click.style(settings.current_workspace, bold=True)}"
            )

        confirmation_code = click.prompt(
            f'This will remove the pipeline "{click.style(code, bold=True)}" from the "{click.style(settings.current_workspace, bold=True)} workspace. This operation cannot be undone.\nPlease enter "{click.style(code, bold=True)}" to confirm',
            type=str,
        )

        if confirmation_code != code:
            _terminate(
                "❌ Pipeline code and confirmation are different, aborted.",
                err=True,
            )

        try:
            if delete_pipeline(pipeline["id"]):
                click.echo(
                    click.style(
                        f"✅ Pipeline {click.style(code, bold=True)} deleted.",
                        fg="green",
                    )
                )

        except Exception as e:
            _terminate(
                f'❌ Error while deleting pipeline: "{e}"',
                err=True,
                exception=e,
            )


@pipelines.command("run")
@click.argument(
    "path",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
)
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
)
@click.option("--debug", "-d", is_flag=True, help="Run the pipeline in debug mode (with debugpy)")
def pipelines_run(
    path: str,
    image: str = None,
    config_str: str = "{}",
    config_file: click.File = None,
    debug: bool = False,
):
    """Run a pipeline locally."""
    if config_str and config_file:
        _terminate("❌ You can't specify both -c and -f", err=True)
    config = None
    try:
        if config_file:
            config = json.loads(config_file.read(), strict=False)
        else:
            config = json.loads(config_str or "{}", strict=False)

        container = run_pipeline(path, config, image, debug=debug)
        # Listen to ctrl+c to stop the container
        signal.signal(signal.SIGINT, lambda _, __: container.kill())

        if debug:
            if not (Path(path) / ".vscode" / "launch.json").exists():
                click.secho("\nA launch.json is required in order to debug the pipeline", fg="red")

            click.secho("Open your pipeline directory with VSCode and start the debugging session")
            click.secho(
                "Visit the wiki for more information: https://github.com/BLSQ/openhexa/wiki/Writing-OpenHEXA-pipelines#debugging-and-troubleshooting-your-pipelines",
                fg="blue",
            )

        click.secho("\nRun logs", underline=True)
        for line in container.logs(stream=True):
            click.echo(line.decode("utf-8"))

        result = container.wait()
        click.echo()
        if result["StatusCode"] != 0:
            _terminate("❌ Error in pipeline", err=True)
        else:
            click.echo(click.style("✅ Pipeline finished successfully", fg="green"))
    except json.JSONDecodeError as e:
        _terminate(f"❌ Error while parsing JSON: {e}", err=True, exception=e)
    except PipelineDirectoryError:
        _terminate(f"❌ No pipeline found in {path}", err=True)
    except DockerError as e:
        _terminate(f"❌ Error while running pipeline: {e}", err=True, exception=e)


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
    click.echo(click.style(message, fg="red"), err=err)
    if settings.debug and exception:
        raise exception
    raise click.Abort()
