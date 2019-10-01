from pathlib import Path

from invoke import task

from ..utils import link_config


@task
def manage(ctx, cmd):
    """Runs Django manage command(s).

    :param str|list cmd:

    """
    if not isinstance(cmd, list):
        cmd = [cmd]

    for c in cmd:
        ctx.run('%s %s' % (ctx.project.name, c), pty=True)


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

    email = ctx.project.email or ''
    if email:
        command += ' --email %s --username %s' % (email, email.partition('@')[0])

    manage(ctx, command)


@task
def bootstrap(ctx):
    """Puts Django production settings file to remote."""

    link_config(
        ctx,
        title='Django',
        name_local='django.py',
        name_remote='settings_production.py',
        dir_remote_confs=Path(ctx.paths.remote.project.base) / ctx.project.name / 'settings'
    )
