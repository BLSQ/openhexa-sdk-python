"""CLI module, with click."""

import base64
import json
import sys
from importlib.metadata import version
from pathlib import Path

import click
import stringcase

from openhexa.cli.api import (
    InvalidDefinitionError,
    create_pipeline,
    delete_pipeline,
    ensure_is_pipeline_dir,
    ensure_pipeline_config_exists,
    get_pipeline,
    get_skeleton_dir,
    get_workspace,
    is_debug,
    list_pipelines,
    open_config,
    save_config,
    upload_pipeline,
)
from openhexa.sdk.pipelines import get_local_workspace_config, import_pipeline


@click.group()
@click.option("--debug/--no-debug", default=False, envvar="DEBUG")
@click.version_option(version("openhexa.sdk"))
@click.pass_context
def app(ctx, debug):
    """OpenHEXA CLI."""
    # ensure that ctx.obj exists and is a dict (in case `cli()` is called
    # by means other than the `if` block below)
    ctx.ensure_object(dict)

    user_config = open_config()
    user_config.set("openhexa", "debug", str(debug))
    save_config(user_config)


@app.group(invoke_without_command=True)
@click.pass_context
def workspaces(ctx):
    """Manage workspaces (add workspace, remove workspace, list workspaces, activate a workspace)."""
    if ctx.invoked_subcommand is None:
        ctx.forward(workspaces_list)


@workspaces.command(name="add")
@click.argument("slug")
@click.option("--token", prompt=True, hide_input=True, confirmation_prompt=False)
def workspaces_add(slug, token):
    """Add a workspace to the configuration and activate it. The access token is required to access the workspace."""
    user_config = open_config()
    if slug in user_config["workspaces"]:
        click.echo(f"Workspace {slug} already exists. We will only update its token.")
    else:
        click.echo(f"Adding workspace {slug}")
    try:
        get_workspace(user_config, slug, token)
    except Exception as e:
        click.echo(
            f"Error while getting workspace '{slug}' on {user_config['openhexa']['url']}. Check the slug of the workspace and the access token.",
            err=True,
        )
        if is_debug(user_config):
            raise e
        return click.Abort()

    user_config["workspaces"].update({slug: token})
    user_config["openhexa"].update({"current_workspace": slug})

    save_config(user_config)


@workspaces.command(name="activate")
@click.argument("slug")
def workspaces_activate(slug):
    """Activate a workspace that is already in the configuration. The activated workspace will be used for the 'pipelines' commands."""
    user_config = open_config()
    if slug not in user_config["workspaces"]:
        click.echo(f"Workspace {slug} does not exist on {user_config['openhexa']['url']}. Available workspaces:")
        click.echo(", ".join(user_config["workspaces"].keys()))
        return click.Abort()
    click.echo(f"Activating workspace {slug}")
    user_config["openhexa"].update({"current_workspace": slug})

    save_config(user_config)


@workspaces.command(name="list")
def workspaces_list():
    """List the workspaces in the configuration."""
    user_config = open_config()

    click.echo("Workspaces:")
    for slug in user_config["workspaces"]:
        click.echo(
            click.style(f"* {slug} (active)", bold=True)
            if slug == user_config["openhexa"]["current_workspace"]
            else f"* {slug}"
        )

    save_config(user_config)


@workspaces.command(name="rm")
@click.argument("slug")
def workspaces_rm(slug):
    """Remove a workspace from the configuration.

    SLUG is the slug of the workspace to remove from the configuration.
    """
    user_config = open_config()
    if slug not in user_config["workspaces"]:
        click.echo(f"Workspace {slug} does not exist")
        return
    click.echo(f"Removing workspace {slug}")

    del user_config["workspaces"][slug]
    if f"pipelines.{slug}" in user_config.sections():
        del user_config[f"pipelines.{slug}"]

    if user_config["openhexa"]["current_workspace"] == slug:
        user_config["openhexa"].update({"current_workspace": ""})

    save_config(user_config)


@app.group(invoke_without_command=True)
@click.pass_context
def config(ctx):
    """Manage configuration of the CLI."""
    if ctx.invoked_subcommand is None:
        user_config = open_config()
        click.echo("Debug: " + ("True" if is_debug(user_config) else "False"))
        click.echo(f"Backend URL: {user_config['openhexa']['url']}")
        try:
            click.echo(f"Current workspace: {user_config['openhexa']['current_workspace']}")
        except KeyError:
            click.echo("No current workspace")
        click.echo("\nWorkspaces:")
        click.echo("\n".join(user_config["workspaces"].keys()))


@config.command(name="set_url")
@click.argument("url")
def config_set_url(url):
    """Set the URL of the backend."""
    user_config = open_config()
    user_config["openhexa"].update({"url": url})
    save_config(user_config)
    click.echo(f"Set backend URL to {user_config['openhexa']['url']}")


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
    new_pipeline_directory_name = stringcase.snakecase(name.lower())
    new_pipeline_path = Path.cwd() / Path(new_pipeline_directory_name)
    if new_pipeline_path.exists():
        click.echo(
            f"There is already a {name} directory in the current directory. Please choose a new name "
            f"for your pipeline.",
            err=True,
        )
        sys.exit(1)

    # Load samples
    sample_directory_path = get_skeleton_dir()
    with open(sample_directory_path / Path(".gitignore")) as sample_ignore_file:
        sample_ignore_content = sample_ignore_file.read()
    with open(sample_directory_path / Path("pipeline.py")) as sample_pipeline_file:
        sample_pipeline_content = (
            sample_pipeline_file.read()
            .replace("skeleton-pipeline-code", stringcase.spinalcase(name.lower()))
            .replace("skeleton_pipeline_name", stringcase.snakecase(name.lower()))
            .replace("Skeleton pipeline name", name)
        )
    with open(sample_directory_path / Path("workspace.yaml")) as sample_workspace_file:
        sample_workspace_content = sample_workspace_file.read()

    # Create directory
    new_pipeline_path.mkdir(exist_ok=False)
    (new_pipeline_path / "workspace").mkdir(exist_ok=False)
    with open(new_pipeline_path / ".gitignore", "w") as ignore_file:
        ignore_file.write(sample_ignore_content)
    with open(new_pipeline_path / "pipeline.py", "w") as pipeline_file:
        pipeline_file.write(sample_pipeline_content)
    with open(new_pipeline_path / "workspace.yaml", "w") as workspace_file:
        workspace_file.write(sample_workspace_content)

    # Success
    click.echo(
        f"{click.style('Success!', fg='green')} Your pipeline has been created in "
        f"the {new_pipeline_directory_name}/ directory"
    )
    click.echo(
        f"Run it using {click.style(f'cd {new_pipeline_directory_name}', fg='cyan')} && "
        f"{click.style('python pipeline.py', fg='cyan')}"
    )


@pipelines.command("push")
@click.argument("path", default=".", type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option("--yes", is_flag=True, default=False, help="Do not ask for confirmation")
def pipelines_push(path: str, yes: bool = False):
    """Push a pipeline to the backend. If the pipeline already exists, it will be updated otherwise it will be created.

    PATH is the path to the pipeline file.
    """
    user_config = open_config()
    try:
        workspace = user_config["openhexa"]["current_workspace"]
    except KeyError:
        click.echo(
            "No workspace activated. Use openhexa workspaces add or openhexa workspaces activate to "
            "activate a workspace.",
            err=True,
        )
        sys.exit(1)

    ensure_is_pipeline_dir(path)
    ensure_pipeline_config_exists(Path(path))

    try:
        pipeline = import_pipeline(path)
    except Exception as e:
        click.echo(f'Error while importing pipeline: "{e}"', err=True)
        if is_debug(user_config):
            raise e
        sys.exit(1)
    else:
        workspace_pipelines = list_pipelines(user_config)
        if is_debug(user_config):
            click.echo(workspace_pipelines)

        if get_pipeline(user_config, pipeline.code) is None:
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
            create_pipeline(user_config, pipeline.code, pipeline.name)

        click.echo(
            f"Pushing pipeline {click.style(pipeline.code, bold=True)} to workspace {click.style(workspace, bold=True)}"
        )

        try:
            new_version = upload_pipeline(user_config, path)
            click.echo(f"New version created: {new_version}")

            url = f"{user_config['openhexa']['url']}/workspaces/{workspace}/pipelines/{pipeline.code}".replace(
                "api", "app"
            )
            click.echo(
                f"Done! You can view the pipeline in OpenHEXA on {click.style(url, fg='bright_blue', underline=True)}"
            )
        except InvalidDefinitionError as e:
            _terminate(
                f'Pipeline definition is invalid: "{e}"',
                err=True,
                exception=e,
                debug=is_debug(user_config),
            )
        except Exception as e:
            _terminate(
                f'Error while importing pipeline: "{e}"',
                err=True,
                exception=e,
                debug=is_debug(user_config),
            )


@pipelines.command("delete")
@click.argument("code", type=str)
def pipelines_delete(code: str):
    """Delete a pipeline and all his versions."""
    user_config = open_config()
    try:
        workspace = user_config["openhexa"]["current_workspace"]
    except KeyError:
        click.echo(
            "No workspace activated. Use openhexa workspaces add or openhexa workspaces activate to "
            "activate a workspace.",
            err=True,
        )
        sys.exit(1)
    else:
        pipeline = get_pipeline(user_config, code)
        if pipeline is None:
            click.echo(
                f"Pipeline {click.style(code, bold=True)} does not exist in workspace {click.style(workspace, bold=True)}"
            )
            sys.exit(1)

        confirmation_code = click.prompt(
            f'This will remove the pipeline "{click.style(code, bold=True)}" from the "{click.style(workspace, bold=True)} workspace. This operation cannot be undone.\nPlease enter "{click.style(code, bold=True)}" to confirm',
            type=str,
        )

        if confirmation_code != code:
            click.echo(
                "Pipeline code and confirmation are different, aborted.",
                err=True,
            )
            sys.exit(1)

        try:
            if delete_pipeline(user_config, pipeline["id"]):
                click.echo(f"Pipeline {click.style(code, bold=True)} deleted.")

        except Exception as e:
            _terminate(
                f'Error while deleting pipeline: "{e}"',
                err=True,
                exception=e,
                debug=is_debug(user_config),
            )


@pipelines.command("run")
@click.argument("path", default=".", type=click.Path(exists=True, file_okay=False, dir_okay=True))
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
    user_config = open_config()
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
        f"HEXA_WORKSPACE={user_config['openhexa']['current_workspace']}",
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

    if is_debug(user_config):
        print(" ".join(cmd))

    proc = Popen(
        cmd,
        close_fds=True,
    )
    return proc.wait()


@pipelines.command("list")
def pipelines_list():
    """List all the remote pipelines of the current workspace."""
    user_config = open_config()
    workspace = user_config["openhexa"]["current_workspace"]

    if workspace == "":
        click.echo("No workspace activated", err=True)
        sys.exit(1)

    workspace_pipelines = list_pipelines(user_config)
    if len(workspace_pipelines) == 0:
        click.echo(f"No pipelines in workspace {workspace}")
        return
    click.echo("Pipelines:")
    for pipeline in workspace_pipelines:
        current_version = pipeline["currentVersion"].get("number")
        if current_version is not None:
            current_version = f"v{current_version}"
        else:
            current_version = "N/A"
        click.echo(f"* {pipeline['code']} - {pipeline['name']} ({current_version})")


def _terminate(message: str, exception: Exception = None, err: bool = False, debug: bool = False):
    click.echo(message, err=err)
    if debug and exception:
        raise exception
    sys.exit(1)
