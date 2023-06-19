#!/usr/bin/env python

import json
import os
import sys

import requests

from openhexa.sdk.pipelines import download_pipeline, import_pipeline


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def launch_cloud_run(config):
    # cloud run -> need to download the code from cloud
    if "HEXA_TOKEN" not in os.environ or "HEXA_SERVER_URL" not in os.environ:
        eprint("Need token and url to download the code")
        sys.exit(1)

    access_token = os.environ["HEXA_TOKEN"]
    server_url = os.environ["HEXA_SERVER_URL"]
    run_id = os.environ["HEXA_RUN_ID"]
    workspace_slug = os.environ["HEXA_WORKSPACE"]

    print("Downloading pipeline...")
    download_pipeline(
        server_url,
        access_token,
        run_id,
        ".",
    )
    print("Pipeline downloaded.")

    print("Injecting credentials...")
    r = requests.post(
        f"{server_url}/workspaces/credentials/",
        headers={"Authorization": f"Bearer {access_token}"},
        data={"workspace": workspace_slug},
        timeout=30,
    )
    r.raise_for_status()
    data = r.json()
    os.environ.update(data["env"])
    print("Credentials injected.")

    print("Mounting buckets...")
    # setup fuse for buckets
    if os.path.exists("/home/jovyan/.hexa_scripts/fuse_mount.py"):
        # import fuse mount script _after_ env variables injection
        sys.path.insert(1, "/home/jovyan/.hexa_scripts")
        import fuse_mount  # noqa: F401, E402

    if os.path.exists("/home/jovyan/.hexa_scripts/wrap_up.py"):
        # setup sample files, et co...
        os.environ["OPENHEXA_LEGACY"] = "false"

    if os.path.exists("./requirements.txt"):
        print("Installing requirements...")
        os.system("pip install -r requirements.txt")

    print("Running cloud pipeline...")
    pipeline = import_pipeline(".")

    pipeline(config=config)

    # clean up fuse
    if os.path.exists("/home/jovyan/.hexa_scripts/fuse_umount.py"):
        # umount at the end
        import fuse_umount  # noqa: F401, E402


def launch_local_run(config):
    if not os.path.exists("pipeline/pipeline.py"):
        eprint("No pipeline.py found")
        sys.exit(1)

    if os.path.exists("pipeline/requirements.txt"):
        print("Installing requirements...")
        os.system("pip install -r pipeline/requirements.txt")

    print("Running local pipeline...")
    pipeline = import_pipeline("pipeline")

    pipeline(config=config)


if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 2 else "cloudrun"
    raw_config = sys.argv[2] if len(sys.argv) > 2 else sys.argv[1]
    config = json.loads(raw_config) if raw_config else {}
    if command == "cloudrun":
        launch_cloud_run(config)
    elif command == "run":
        launch_local_run(config)
    else:
        eprint(f"Unknown command {command}")
        sys.exit(1)
