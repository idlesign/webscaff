from invoke import task

from . import fs


@task
def bootstrap(ctx):
    """Bootstraps Certbot for the project."""
    fs.mkdir(ctx, ctx.paths.remote.project.runtime.certbot)


def get_certificate(ctx):
    """Get certificates from Certbot for HTTPS using webroot plugin.

    :param ctx:

    """
    project = ctx.project
    domain = project.domain
    email = project.email or ''
    webroot = ctx.paths.remote.project.runtime.certbot

    if email:
        email = '--email %s' % email

    command = (
        'certbot --agree-tos --no-eff-email %s certonly --webroot -d %s -w %s' %
        (email, domain, webroot))

    ctx.sudo(command)
