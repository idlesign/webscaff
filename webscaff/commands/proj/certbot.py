from ..sys import fs


def bootstrap(ctx):
    """Bootstraps Certbot for the project."""
    fs.mkdir(ctx, ctx.paths.remote.project.state.certbot)
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
