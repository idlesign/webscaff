from invoke import task


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
]


@task
def configure(ctx):
    """Continues configuring using dpkg"""
    ctx.sudo('dpkg --configure -a', env={'DEBIAN_FRONTEND': 'noninteractive'})


def upgrade(ctx):
    """Initiates remote OS upgrade procedure."""
    update()
    ctx.sudo('apt-get upgrade')


@task
def update(ctx):
    """Initiates apt cache update."""
    ctx.sudo('apt-get update')


@task
def install(ctx, packages):
    """Installs packages using apt.

    :param packages:

    """
    if not isinstance(packages, list):
        packages = [packages]

    update(ctx)

    ctx.sudo(f"apt install -y {' '.join(packages)}", env={'DEBIAN_FRONTEND': 'noninteractive'})


def bootstrap(ctx):
    """Bootstraps system by installing required packages."""
    install(ctx, BOOTSTRAP_SYSTEM_PACKAGES)
