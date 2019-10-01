from contextlib import contextmanager

from patchwork.files import exists


@contextmanager
def venv_context(ctx):
    """Temporarily switches into virtual environment."""

    with ctx.prefix('. %s/activate' % ctx.paths.remote.project.venv.bin):
        yield


def create(ctx, python_path):
    """Creates virtual environment using given Python interpreter path
    if not already created.

    :param ctx:
    :param str python_path: Interpreter (cmd name or full path).

    """
    project_venv = ctx.paths.remote.project.venv.root

    if exists(ctx, project_venv):
        return

    # Call as module in case `virtualenv` app is not [yet] available.
    ctx.run('%s -m venv %s' % (python_path, project_venv))
