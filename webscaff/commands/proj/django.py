from pathlib import Path

from invoke import task

from .fs import create_dir
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
        ctx.sudo('%s %s' % (project_name, command), pty=True, user=project_name)


def rollout(ctx):
    """Rolls out migrations and statics."""
    migrate(ctx)
    manage(ctx, 'collectstatic --noinput')


@task
def migrate(ctx):
    """Runs Django manage command for project to launch migrations."""
    manage(ctx, 'migrate')


@task
def create_superuser(ctx):
    """Runs Django manage command for project to create a superuser.
    Tries to get e-mail from settings, and username from e-mail.

    """
    command = 'createsuperuser'

    username = ''

    email = ctx.project.email or ''
    if email:
        username = email.partition('@')[0]
        command += ' --email %s --username %s' % (email, username)

    echo('\nCreating Django superuser %s ...' % ('[%s]' % username) if username else '')

    manage(ctx, command)


@task
def bootstrap(ctx):
    """Puts Django production settings file to remote."""

    # Create media and static directories.
    runtime_dir = ctx.paths.remote.project.runtime
    create_dir(ctx, runtime_dir.static)
    create_dir(ctx, runtime_dir.media)

    link_config(
        ctx,
        title='Django',
        name_local='django.py',
        name_remote='settings_production.py',
        dir_remote_confs=Path(ctx.paths.remote.project.base) / ctx.project.name / 'settings'
    )
