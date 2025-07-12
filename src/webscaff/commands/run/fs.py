from pathlib import Path

from invoke import task

from ..sys import fs as sys_fs
from ..utils import get_symlink_command, rsync, echo


def create_environ_file(ctx, type_marker='production'):
    """Creates environment marker file for a given environment type.

    :param ctx:
    :param str type_marker:

    """
    sys_fs.append_to_file(ctx, ctx.paths.remote.project.state.environ, type_marker)


def linksdir_get(ctx):
    """Get project links dir in user's home."""
    return f'~/{ctx.project.name}'


def linksdir_create(ctx):
    """Create project links dir in user's home."""
    sys_fs.mkdir(ctx, linksdir_get(ctx), sudo=False)


def symlink_home(ctx):
    """Create a directory with project-related symlinks in user's home."""

    home_linkroot = linksdir_get(ctx)

    dir_map = [
        (ctx.paths.remote.project.home, 'code'),
        (ctx.paths.remote.project.state.root, 'state'),
        (ctx.paths.remote.cache, 'cache'),
    ]

    for dir_, linkname in dir_map:
        ctx.sudo(get_symlink_command(dir_, f'{home_linkroot}/{linkname}'))


def upload_configs(ctx):
    """Uploads project configuration files (under `conf` dir) to remote."""

    source = ctx.paths.local.configs + '/'  # slash is rsync semantic specific

    if Path(source).exists():
        rsync(ctx, source, ctx.paths.remote.configs, delete=True)

    else:
        echo(f'No configuration files uploaded. Expected: {source}')


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
        ctx, path, f'g:{group}:rwX,d:g:{group}:rwX,m:rwx',
        modify=True)


@task
def cache_init(ctx, drop=False):
    """Initializes cache directory.

    :param ctx:
    :param drop: If True - drops if already exists. Otherwise - empties.

    """
    dir_cache = ctx.paths.remote.cache
    command = '%s*' if drop else '%s/*'
    sys_fs.rm(ctx, command % dir_cache)
    create_dir(ctx, dir_cache)


def bootstrap(ctx):
    """Bootstraps filesystem for the project."""

    project = ctx.paths.remote.project
    dir_state = project.state

    dirs = [
        project.home,
        dir_state.root,
        dir_state.dumps,
        dir_state.static,
        dir_state.media,
    ]

    for dir_ in dirs:
        create_dir(ctx, dir_)

    cache_init(ctx, drop=True)
    create_environ_file(ctx)

    symlink_home(ctx)
