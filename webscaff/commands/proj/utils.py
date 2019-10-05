from pathlib import Path

from invoke import task
from patchwork.files import exists

from . import fs, django, service, uwsgi
from ..sys import usr, apt, git, venv, pip, pg, utils as sys_utils, certbot


@task
def bootstrap(ctx):
    """Initializes a remote for your project."""

    project = ctx.project
    project_home = ctx.paths.remote.project.home
    me = usr.whoami(ctx)

    usr.create(ctx, project.user)
    usr.add_to_group(ctx, me, project.group)

    apt.bootstrap(ctx)

    fs.create_dir(ctx, project_home)
    fs.symlink_home(ctx)

    if not exists(ctx, Path(ctx.paths.remote.repo) / '.git'):
        git.clone(
            ctx,
            path_base=project_home,
            repo_url=project.repo,
            dir_target=project.name if project.repo_slim else '.')

    venv.create(ctx, ctx.python)

    with ctx.cd(ctx.paths.remote.project.base):
        pip.install(ctx, package='.', editable=True)
        pip.install(ctx, from_req=True)

    fs.symlink_entypoint(ctx)

    fs.upload_configs(ctx)
    fs.create_environ_file(ctx)

    pg.bootstrap(ctx)

    django.bootstrap(ctx)
    django.migrate(ctx)
    django.create_superuser(ctx)

    uwsgi.bootstrap(ctx)

    service.bootstrap(ctx)

    certbot.bootstrap(ctx)
    certbot.get_certificate(ctx)

    sys_utils.reboot(ctx)


@task
def rollout(ctx):
    """Updates remote files from remote repository and rolls out project."""
    git.pull(ctx, ctx.paths.remote.repo)
    django.rollout(ctx)
    uwsgi.reload_touch()


@task
def backup(ctx):
    """Creates a project backup."""
    # todo implement
    raise NotImplementedError
