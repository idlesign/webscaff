from pathlib import Path

from . import fs
from ..sys import fs as sys_fs
from ..utils import link_config

LETSENCRYPT_DIR = '/etc/letsencrypt'


def bootstrap(ctx):
    """Bootstraps Certbot for the project."""
    fs.create_dir(ctx, ctx.paths.remote.project.state.certbot)
    project_name = ctx.project.name

    # Prepare directories in /etc/letsencrypt/
    ctx.sudo('certbot', warn=True)

    # Link a deploy hook, to allow project user access to it.
    link_config(
        ctx,
        title='certbot hook',
        name_local=project_name + '-certbot-hook.sh',
        name_remote=project_name,
        dir_remote_confs=Path(f'{LETSENCRYPT_DIR}/renewal-hooks/deploy/')
    )

    get_certificate(ctx)


def get_certificate(ctx):
    """Get certificates from Certbot for HTTPS using webroot plugin.

    :param ctx:

    """
    project = ctx.project
    group = ctx.project.group
    domain = project.domain
    email = project.email or ''
    webroot = ctx.paths.remote.project.state.certbot

    if email:
        email = f'--email {email}'

    command = (
        f'certbot --agree-tos --no-eff-email {email} certonly '
        f'--webroot -d {domain} -w {webroot}')

    ctx.sudo(command)

    # Set access for
    for realm in ['archive', 'live']:
        sys_fs.setfacl(
            ctx,
            path=f'{LETSENCRYPT_DIR}/{realm}/',
            acl=f'g:{group}:--x', modify=True)

        sys_fs.setfacl(
            ctx,
            path=f'{LETSENCRYPT_DIR}/{realm}/{domain}/',
            acl=f'g:{group}:r-x', modify=True)


def dump(ctx, target_dir):
    """Dumps Certbot related stuff into a target directory."""

    sys_fs.gzip_dir(
        ctx,
        LETSENCRYPT_DIR,
        target_dir,
        do_sudo=True
    )


def restore(ctx, source_dir):
    """Restores Certbot related stuff from a source directory."""

    sys_fs.gzip_extract(
        ctx,
        archive=source_dir / 'certbot.tar.gz',
        target_dir=LETSENCRYPT_DIR,
        do_sudo=True
    )
