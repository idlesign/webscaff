from pathlib import Path

from invoke import task
from patchwork.files import append as append_to_file

from ..utils import get_symlink_command, rsync, echo
from ..sys import fs as sys_fs


def symlink_entypoint(ctx):
    """Create a system-wide symlink to a project entrypoint."""
    project_name = ctx.project.name
    ctx.sudo(get_symlink_command(
        '%s/%s' % (ctx.paths.remote.project.venv.bin, project_name), '/usr/bin/%s' % project_name))


def create_environ_file(ctx, type_marker='production'):
    """Creates environment marker file for a given environment type.

    :param ctx:
    :param str type_marker:

    """
    append_to_file(ctx, ctx.paths.remote.runtime.environ, type_marker)


def symlink_home(ctx):
    """Create symlinks in user's home to a project home directory."""
    ctx.sudo(get_symlink_command(ctx.paths.remote.project.home, '~/%s' % ctx.project.name))


@task
def upload_configs(ctx):
    """Uploads project configuration files (under `conf` dir) to remote."""
    source = ctx.paths.local.configs

    if Path(source).exists():

        rsync(
            ctx, source, ctx.paths.remote.configs,
            delete=True,
            exclude=[
                ctx.paths.remote.environ_filename,
            ])

    else:
        echo('No configuration files uploaded. Expected: %s' % source)


def create_dir(ctx, path):
    """Creates a directory accessible for project user.

    :param ctx:

    :param str path: Directory path.

    """
    group = ctx.project.group
    sys_fs.mkdir(ctx, path)
    sys_fs.chown(ctx, path, ctx.project.user, group)

    # Grant project group full access.
    sys_fs.setfacl(
        ctx, path, 'g:%(group)s:rwX,d:g:%(group)s:rwX' % {'group': group},
        modify=True)


@task
def cache_init(ctx):
    """Initializes cache directory. Drops if already exists."""
    sys_fs.rm(ctx, '%s*' % ctx.paths.remote.cache)
    create_dir(ctx, ctx.paths.remote.cache)
