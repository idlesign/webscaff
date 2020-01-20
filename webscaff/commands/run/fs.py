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


def symlink_home(ctx):
    """Create a directory with project-related symlinks in user's home."""

    home_linkroot = '~/%s' % ctx.project.name

    sys_fs.mkdir(ctx, home_linkroot)

    dir_map = [
        (ctx.paths.remote.project.home, 'code'),
        (ctx.paths.remote.project.state.root, 'state'),
        (ctx.paths.remote.cache, 'cache'),
    ]

    for dir_, linkname in dir_map:
        ctx.sudo(get_symlink_command(dir_, '%s/%s' % (home_linkroot, linkname)))


def upload_configs(ctx):
    """Uploads project configuration files (under `conf` dir) to remote."""

    source = ctx.paths.local.configs + '/'  # slash is rsync semantic specific

    if Path(source).exists():
        rsync(ctx, source, ctx.paths.remote.configs, delete=True)

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
    dir_cache = ctx.paths.remote.cache
    sys_fs.rm(ctx, '%s*' % dir_cache)
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

    cache_init(ctx)
    create_environ_file(ctx)

    symlink_home(ctx)
