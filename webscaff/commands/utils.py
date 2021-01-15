from os import environ
from pathlib import Path

from patchwork.transfers import rsync as rsync_patchwork


def echo(text):
    """Echoes the text to stdout.

    :param str text:

    """
    print(text)


def link_config(ctx, *, title, name_local, name_remote, dir_remote_confs):

    config_name = name_local
    config_local = Path(ctx.paths.local.configs) / config_name

    if config_local.exists():

        ctx.sudo(get_symlink_command(
            Path(ctx.paths.remote.configs) / config_name,
            dir_remote_confs / name_remote))

        return True

    echo(f'No {title} configuration. Expected: {config_local}')

    return False


def rsync(ctx, *args, **kwargs):
    """Ugly workaround for https://github.com/fabric/patchwork/issues/16."""
    ssh_agent = environ.get('SSH_AUTH_SOCK', None)

    if ssh_agent:
        ctx.config.run.env['SSH_AUTH_SOCK'] = ssh_agent

    return rsync_patchwork(ctx, *args, **kwargs)


def cd_sudo(cd, command):
    # https://github.com/pyinvoke/invoke/issues/459
    return f'bash -c "cd {cd} && {command}"'


def get_symlink_command(src, dest):
    """Returns a symlink command.

    :param src: Source filepath
    :param dest: Link filepath

    """
    return f'ln -sf {src} {dest}'
