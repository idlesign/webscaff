from invoke import task

from .utils import ENV_NON_INTERACTIVE


BOOTSTRAP_SYSTEM_PACKAGES = [
    'python3-dev',
    'python3-pip',
    'python3-venv',
    'python3-wheel',

    # For source builds.
    'build-essential',
    'libjpeg-dev',  # for Pillow
    'libxml2-dev', 'libxslt1-dev',  # for lxml
    'libpcre3-dev', 'libssl-dev',  # for uWSGI with SSL and routing support

    'git',
    'postgresql', 'libpq-dev',
    'certbot',

    # Utils.
    'acl',
    'mc',
    'htop',
    'net-tools',
    'ncdu',
    'screen',
]


@task
def configure(ctx):
    """Continues configuring using dpkg"""
    ctx.sudo('dpkg --configure -a', env=ENV_NON_INTERACTIVE)


@task
def upgrade(ctx, purge=False):
    """Initiates packages upgrade procedure.

    :param purge: Allows to purge unused packages.

    """
    update(ctx)
    ctx.sudo('apt upgrade')

    if purge:
        autoremove(ctx)


@task
def autoremove(ctx):
    """Removes unused packages."""
    ctx.sudo('apt autoremove')


@task
def update(ctx):
    """Initiates apt cache update."""
    ctx.sudo('apt update')


@task
def install(ctx, packages):
    """Installs packages using apt.

    :param packages:

    """
    if not isinstance(packages, list):
        packages = [packages]

    update(ctx)

    ctx.sudo(f"apt install -y {' '.join(packages)}", env=ENV_NON_INTERACTIVE)


def bootstrap(ctx):
    """Bootstraps system by installing required packages."""
    install(ctx, BOOTSTRAP_SYSTEM_PACKAGES)
