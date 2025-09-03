"""CLI module, with click."""

import functools
import json
import signal
import urllib
from datetime import datetime
from importlib.metadata import version
from pathlib import Path
from urllib.parse import urlparse

import click

from openhexa.cli.api import (
    DockerError,
    GraphQLError,
    InvalidDefinitionError,
    NoActiveWorkspaceError,
    OpenHexaClient,
    OutputDirectoryError,
    PipelineDirectoryError,
    create_pipeline,
    create_pipeline_structure,
    create_pipeline_template_version,
    delete_pipeline,
    download_pipeline_sourcecode,
    ensure_is_pipeline_dir,
    get_library_versions,
    get_pipeline_from_code,
    get_pipelines_pages,
    get_workspace,
    run_pipeline,
    upload_pipeline,
)
from openhexa.cli.settings import settings, setup_logging
from openhexa.sdk.pipelines.exceptions import PipelineNotFound
from openhexa.sdk.pipelines.runtime import get_pipeline


def handle_ssl_errors(func):
    """Handle SSL certificate verification errors in CLI commands."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except GraphQLError as e:
            if "SSL certificate verification failed" in str(e):
                click.echo(click.style(str(e), fg="red"), err=True)
                raise click.Abort()
            raise

    return wrapper


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
@handle_ssl_errors
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
        click.echo("SSL Verification: " + ("True" if settings.verify_ssl else "False"))
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


def propose_to_create_template_version(workspace, pipeline_version, yes):
    """Propose to create a new version of the template if the pipeline is based on a template."""
    pipeline = pipeline_version["pipeline"]
    if pipeline["template"] and pipeline["permissions"]["createTemplateVersion"]["isAllowed"]:
        if not yes and not click.confirm(
            f"The template {click.style(pipeline['template']['name'], bold=True)} is based on this pipeline, do you want to publish a new version of the template as well?",
            True,
        ):
            # Return early when the user do not want to create a template version
            return
        changelog = (
            ""
            if yes
            else click.prompt(
                f"{click.style('Changelog', bold=True)} (optional)", type=str, default="", show_default=False
            )
        )
        try:
            template = create_pipeline_template_version(workspace, pipeline["id"], pipeline_version["id"], changelog)
            template_code_url = urllib.parse.quote(template["code"])
            click.echo(
                click.style(
                    f"✅ New version '{template['currentVersion']['versionNumber']}' of the template '{template['name']}' created! You can view the new template version in OpenHEXA on {click.style(f'{settings.public_api_url}/workspaces/{workspace}/templates/{template_code_url}/versions', fg='bright_blue', underline=True)}",
                    fg="green",
                )
            )
        except Exception as e:
            _terminate(
                f'❌ Error while creating template version: "{e}"',
                err=True,
                exception=e,
            )


def select_pipeline(workspace_pipelines, number_of_pages: int, pipeline):
    """Select a pipeline from the list of workspace pipelines or select creating a new one or select a pipeline from a code."""
    create_new_pipeline = f"Create a new {click.style(pipeline.name, bold=True)} pipeline"
    enter_pipeline_code = f"Insert a {click.style('pipeline code', italic=True)}"
    cancel = "Cancel"

    def _generate_choices():
        """Generate the list of choices for the user."""
        return (
            [
                f"{click.style(p['name'], bold=True)} (code: {click.style(p['code'], italic=True)})"
                for p in workspace_pipelines
            ]
            + [create_new_pipeline]
            + ([enter_pipeline_code] if number_of_pages > 1 else [])
            + [cancel]
        )

    def _handle_user_selection(choices):
        """Handle the user's selection from the list of choices."""
        click.echo("Which pipeline do you want to update?")
        for index, choice in enumerate(choices, start=1):
            click.echo(f"[{index}] {choice}")

        choice_idx = (
            click.prompt(
                "Select an option",
                type=click.IntRange(1, len(choices)),
                default=1,
            )
            - 1
        )

        if choices[choice_idx] == create_new_pipeline:
            return None
        elif choices[choice_idx] == enter_pipeline_code:
            return _handle_enter_pipeline_code()
        elif choices[choice_idx] == cancel:
            raise click.Abort()
        else:
            return workspace_pipelines[choice_idx]

    def _handle_enter_pipeline_code():
        """Handle the case where the user wants to enter a pipeline code."""
        pipeline_code = click.prompt(enter_pipeline_code)
        selected_pipeline = get_pipeline_from_code(pipeline_code)
        if selected_pipeline:
            return selected_pipeline
        else:
            click.echo(f"Pipeline with code {click.style(pipeline_code, italic=True)} not found. Please try again.")
            return _handle_enter_pipeline_code()

    return _handle_user_selection(_generate_choices())


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
    "--code",
    "-c",
    type=str,
    help="Code of the pipeline",
    prompt="Code of the pipeline",
    prompt_required=False,
)
@click.option(
    "--name",
    "-n",
    default=None,
    type=str,
    help="Name of the version",
    prompt="Name of the version",
    prompt_required=False,
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
@handle_ssl_errors
def pipelines_push(
    path: str,
    code: str = None,
    name: str = None,
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
    if yes and not code:
        _terminate("❌ You must provide a pipeline code (using -c or --code) when using the --yes flag.", err=True)

    ensure_is_pipeline_dir(path)

    try:
        pipeline = get_pipeline(path)
    except PipelineNotFound:
        _terminate(
            f"❌ No function with openhexa.sdk pipeline decorator found in {click.style(path, bold=True)}.",
            err=True,
        )
    except Exception as e:
        _terminate(f'❌ Error while importing pipeline: "{e}"', exception=e, err=True)
    else:
        pipeline_pages = get_pipelines_pages(name=pipeline.name)
        workspace_pipelines = pipeline_pages["items"]
        number_of_pages = pipeline_pages["totalPages"]
        if settings.debug:
            click.echo(workspace_pipelines)

        if code:
            selected_pipeline = get_pipeline_from_code(code) or _terminate(
                f"❌ Pipeline with code '{code}' not found.", err=True
            )
        elif yes:
            selected_pipeline = workspace_pipelines[0] if workspace_pipelines else None
        else:
            selected_pipeline = select_pipeline(workspace_pipelines, number_of_pages, pipeline)

        if not yes:
            name_text = f" with name {click.style(name, bold=True)}" if name else ""
            confirmation_message = (
                f"Pushing pipeline {click.style(pipeline.name, bold=True)} "
                f"to workspace {click.style(workspace, bold=True)}{name_text} ?"
            )
            click.confirm(confirmation_message, default=True, abort=True)

        selected_pipeline = selected_pipeline or create_pipeline(pipeline.name)
        uploaded_pipeline_version = None
        try:
            uploaded_pipeline_version = upload_pipeline(
                selected_pipeline["code"], path, name, description=description, link=link
            )
            version_url = click.style(
                f"{settings.public_api_url}/workspaces/{workspace}/pipelines/{selected_pipeline['code']}",
                fg="bright_blue",
                underline=True,
            )
            click.echo(
                click.style(
                    f"✅ New version '{uploaded_pipeline_version['versionName']}' created! You can view the pipeline in OpenHEXA on {version_url}",
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
        propose_to_create_template_version(workspace, uploaded_pipeline_version, yes)


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
        pipeline = get_pipeline_from_code(code)
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
@handle_ssl_errors
def pipelines_list():
    """List all the remote pipelines of the current workspace."""
    if settings.current_workspace is None:
        _terminate("No workspace activated", err=True)

    with OpenHexaClient() as client:
        workspace_pipelines = client.pipelines(workspace_slug=settings.current_workspace).items
    if len(workspace_pipelines) == 0:
        click.echo(f"No pipelines in workspace {settings.current_workspace}")
        return
    click.echo("Pipelines:")
    for pipeline in workspace_pipelines:
        if pipeline.type == "zipFile":
            current_version = f"v{pipeline.current_version.version_number}" if pipeline.current_version else "N/A"
        else:
            current_version = "Jupyter notebook"
        click.echo(f"* {pipeline.code} - {pipeline.name} ({current_version})")


def _terminate(message: str, exception: Exception = None, err: bool = False):
    click.echo(click.style(message, fg="red"), err=err)
    if settings.debug and exception:
        raise exception
    raise click.Abort()
