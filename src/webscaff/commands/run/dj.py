from pathlib import Path

from invoke import task

from .fs import create_dir
from ..sys import fs as sys_fs
from ..utils import link_config, echo


@task
def manage(ctx, cmd):
    """Runs Django manage command(s).

    :param str|list cmd:

    """
    if not isinstance(cmd, list):
        cmd = [cmd]

    project_name = ctx.project.name
    for command in cmd:
        ctx.sudo(f'{project_name} {command}', pty=True, user=project_name)


def rollout(ctx):
    """Rolls out migrations and statics."""
    migrate(ctx)
    manage(ctx, 'collectstatic --noinput')


@task
def migrate(ctx):
    """Runs Django manage command for project to launch migrations."""
    manage(ctx, 'migrate')


def create_superuser(ctx):
    """Runs Django manage command for project to create a superuser.
    Tries to get e-mail from settings, and username from e-mail.

    """
    command = 'createsuperuser'

    username = ''

    email = ctx.project.email or ''
    if email:
        username = email.partition('@')[0]
        command += f' --email {email} --username {username}'

    echo('\nCreating Django superuser %s ...' % f'[{username}]' if username else '')

    manage(ctx, command)


def bootstrap(ctx):
    """Puts Django production settings file to remote."""

    # Create media and static directories.
    dir_state = ctx.paths.remote.project.state
    create_dir(ctx, dir_state.static)
    create_dir(ctx, dir_state.media)

    link_config(
        ctx,
        title='Django',
        name_local='env_production.py',
        name_remote='env_production.py',
        dir_remote_confs=Path(ctx.paths.remote.project.base) / 'settings'
    )

    migrate(ctx)
    create_superuser(ctx)


def dump(ctx, target_dir):
    """Dumps Django related stuff into a target directory."""

    sys_fs.gzip_dir(
        ctx,
        ctx.paths.remote.project.state.media,
        target_dir,
    )


def restore(ctx, source_dir):
    """Restores Django related stuff from a source directory."""

    sys_fs.gzip_extract(
        ctx,
        archive=source_dir / 'media.tar.gz',
        target_dir=ctx.paths.remote.project.state.media
    )
