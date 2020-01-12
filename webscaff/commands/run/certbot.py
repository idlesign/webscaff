from pathlib import Path

from . import fs
from ..sys import fs as sys_fs
from ..utils import link_config


def bootstrap(ctx):
    """Bootstraps Certbot for the project."""
    fs.create_dir(ctx, ctx.paths.remote.project.state.certbot)
    project_name = ctx.project.name

    # Link a deploy hook, to allow project user access to it.
    link_config(
        ctx,
        title='certbot hook',
        name_local=project_name + '-certbot-hook.sh',
        name_remote=project_name,
        dir_remote_confs=Path('/etc/letsencrypt/renewal-hooks/deploy/')
    )

    get_certificate(ctx)


def get_certificate(ctx):
    """Get certificates from Certbot for HTTPS using webroot plugin.

    :param ctx:

    """
    project = ctx.project
    domain = project.domain
    email = project.email or ''
    webroot = ctx.paths.remote.project.state.certbot

    if email:
        email = '--email %s' % email

    command = (
        'certbot --agree-tos --no-eff-email %s certonly --webroot -d %s -w %s' %
        (email, domain, webroot))

    ctx.sudo(command)


def dump(ctx, target_dir):
    """Dumps Certbot related stuff into a target directory."""

    sys_fs.gzip_dir(
        ctx,
        '/etc/letsencrypt',
        target_dir,
        do_sudo=True
    )


def restore(ctx, source_dir):
    """Restores Certbot related stuff from a source directory."""

    sys_fs.gzip_extract(
        ctx,
        archive=source_dir / 'certbot.tar.gz',
        target_dir='/etc/letsencrypt',
        do_sudo=True
    )
