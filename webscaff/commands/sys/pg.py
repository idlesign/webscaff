from functools import partial
from pathlib import Path

from invoke import task

from .fs import tail, append_to_file
from ..utils import link_config, echo


def stop(ctx):
    """Stops PostgreSQL."""
    ctx.sudo('service postgresql stop')


@task
def restart(ctx):
    """Restarts PostgreSQL."""
    ctx.sudo('service postgresql restart')


@task
def reload(ctx):
    """Reloads PostgreSQL."""
    ctx.sudo('service postgresql reload')


def get_version(ctx):
    """Returns a list with PostgreSQL version number."""
    number = ctx.run('pg_config --version').stdout.strip()
    number = number.split(' ')[:2][-1].split('.')
    echo('PostgreSQL version: %s' % number)
    return number


@task
def log_main(ctx):
    """Tails main PostgreSQL log."""
    version = [chunk for chunk in get_version(ctx)[:2] if int(chunk)]  # 9.4, but 10
    tail(ctx, '/var/log/postgresql/postgresql-%s-main.log' % '.'.join(version))


def dump(ctx, db_name, target_dir, binary=True):
    """Dumps DB by name into target directory."""
    target_path = Path(target_dir) / 'db.' + ('dump' if binary else 'sql')
    fmt = '-Fc' if binary else ''
    ctx.run('pg_dump %s %s > %s' % (fmt, db_name, target_path))
    return target_path


def configure(ctx, project_name, project_user):
    """Configures PostgreSQL for the given project."""

    version_ = '.'.join(get_version(ctx)[:-1])

    path_confs = Path('/etc/postgresql/%s/main/' % version_)
    config_name = 'postgresql.conf'
    target_name = '%s.conf' % project_name

    config_linked = link_config(
        ctx,
        title='granular PG',
        name_local=config_name,
        name_remote=target_name,
        dir_remote_confs=path_confs,
    )

    if config_linked:
        # Append into main config an include line.
        append_to_file(ctx, path_confs / config_name, "include = '%s'" % target_name)

    def create_db_and_user():
        sudo_pg = partial(ctx.sudo, user='postgres')

        sudo_pg('createdb %s' % project_name, warn=True)
        sudo_pg('createuser %s' % project_user)  # No password. Using Unix domain sockets.
        sudo_pg('psql -c "GRANT ALL PRIVILEGES ON DATABASE %s TO %s"' % (project_name, project_user))

    create_db_and_user()

    restart(ctx)
