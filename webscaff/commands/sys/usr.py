from .fs import append_to_file


def create(ctx, user):
    """Creates a user."""
    if get_id(ctx, user) is None:
        ctx.sudo(f'useradd -s /bin/bash {user}')


def add_sudoer(ctx, user):
    """Adds a user to sudoers."""
    append_to_file(ctx, '/etc/sudoers', f"'{user} ALL=(ALL:ALL) ALL'")


def add_to_group(ctx, user, group):
    """Adds a user into a group.

    Returns ``True`` if is just added (not already was there).

    :rtype: bool

    """
    result = ctx.sudo(f'adduser {user} {group}').stdout.strip()
    return 'Adding' in result


def get_id(ctx, user):
    """Returns user ID. Might be used to check whether user exists."""
    result = ctx.sudo(f'id -u {user}', warn=True).stdout.strip()
    result = int(result) if result.isdigit() else None

    return result


def whoami(ctx):
    """Returns current user name."""
    return ctx.run('whoami').stdout.strip()
