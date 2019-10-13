from invoke import task

from . import fs, dj, service, uwsgi, venv, git, certbot, pg
from ..sys import usr, apt, utils as sys_utils
from ..utils import echo


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
    fs.upload_configs(ctx)
    venv.bootstrap(ctx)
    pg.bootstrap(ctx)
    dj.bootstrap(ctx)
    uwsgi.bootstrap(ctx)
    service.bootstrap(ctx)
    certbot.bootstrap(ctx)

    echo('* Done. Reboot now ...')

    sys_utils.reboot(ctx)


def rollout(ctx):
    """Updates remote files from remote repository and rolls out project."""
    git.pull(ctx)
    dj.rollout(ctx)
    uwsgi.reload_touch(ctx)


def backup(ctx):
    """Creates a project backup."""
    # todo implement
    raise NotImplementedError
