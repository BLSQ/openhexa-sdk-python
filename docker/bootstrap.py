#!/usr/bin/env python

import json
import os
import sys

import requests

from openhexa.sdk.pipelines import download_pipeline, import_pipeline


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def main():
    # cloud run -> need to download the code from cloud
    if "HEXA_TOKEN" not in os.environ or "HEXA_SERVER_URL" not in os.environ:
        eprint("Need token and url to download the code")
        sys.exit(1)

    access_token = os.environ["HEXA_TOKEN"]
    server_url = os.environ["HEXA_SERVER_URL"]
    run_id = os.environ["HEXA_RUN_ID"]

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
        server_url + "/pipelines/credentials2/",
        headers={"Authorization": f"Bearer {access_token}"},
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

    print("Running pipeline...")
    pipeline = import_pipeline(".")
    config = json.loads(sys.argv[1])

    pipeline(config=config)

    # clean up fuse
    if os.path.exists("/home/jovyan/.hexa_scripts/fuse_umount.py"):
        # umount at the end
        import fuse_umount  # noqa: F401, E402


if __name__ == "__main__":
    main()
