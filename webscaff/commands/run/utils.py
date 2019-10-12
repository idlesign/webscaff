from invoke import task

from . import fs, django, service, uwsgi, venv, git, certbot, pg
from ..sys import usr, apt, utils as sys_utils
from ..utils import echo


@task
def bootstrap(ctx):
    """Initializes a remote for your project."""

    project = ctx.project
    me = usr.whoami(ctx)

    usr.create(ctx, project.user)
    just_added = usr.add_to_group(ctx, me, project.group)

    if just_added:
        echo(' * Initial preparation is done. Please rerun the command to proceed.')
        return

    apt.bootstrap(ctx)
    fs.bootstrap(ctx)
    git.bootstrap(ctx)
    venv.bootstrap(ctx)
    pg.bootstrap(ctx)
    django.bootstrap(ctx)
    uwsgi.bootstrap(ctx)
    service.bootstrap(ctx)
    certbot.bootstrap(ctx)

    echo('* Done. Reboot now ...')

    sys_utils.reboot(ctx)


@task
def rollout(ctx):
    """Updates remote files from remote repository and rolls out project."""
    git.pull(ctx)
    django.rollout(ctx)
    uwsgi.reload_touch()


@task
def backup(ctx):
    """Creates a project backup."""
    # todo implement
    raise NotImplementedError
