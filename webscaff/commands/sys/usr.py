from invoke import task

from patchwork.files import append as append_to_file


def create(ctx, user):
    """Creates a user."""
    if get_id(ctx, user) is None:
        ctx.sudo('useradd -s /bin/bash %s' % user)


def add_sudoer(ctx, user):
    """Adds a user to sudoers."""
    append_to_file(ctx, '/etc/sudoers', "'%s ALL=(ALL:ALL) ALL'" % user)


def add_to_group(ctx, user, group):
    """Adds a user into a group."""
    ctx.sudo('usermod -a %s -G %s' % (user, group))


def get_id(ctx, user):
    """Returns user ID. Might be used to check whether user exists."""
    result = ctx.sudo('id -u %s' % user, warn=True).stdout.strip()
    result = int(result) if result.isdigit() else None

    return result


def whoami(ctx):
    """Returns current user name."""
    return ctx.run('whoami').stdout.strip()
