import sys

import click


def terminate(message: str, exception: Exception = None, err: bool = False, debug: bool = False):
    click.echo(message, err=err)
    if debug and exception:
        raise exception
    sys.exit(1)
