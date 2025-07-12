from patchwork.files import exists


def create(ctx, python_path, venv_dir):
    """Creates virtual environment using given Python interpreter path
    if not already created.

    :param ctx:
    :param str python_path: Interpreter (cmd name or full path).
    :param str venv_dir: Directory to create for virtual environment.

    """
    if exists(ctx, venv_dir):
        return

    # Call as module in case `virtualenv` app is not [yet] available.
    ctx.run(f'{python_path} -m venv {venv_dir}')
