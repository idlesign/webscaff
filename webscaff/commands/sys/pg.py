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
    echo(f'PostgreSQL version: {number}')
    return number


@task
def log_main(ctx):
    """Tails main PostgreSQL log."""
    version = [chunk for chunk in get_version(ctx)[:2] if int(chunk)]  # 9.4, but 10
    tail(ctx, f"/var/log/postgresql/postgresql-{'.'.join(version)}-main.log")


def dump(ctx, db_name, target_dir, binary=True):
    """Dumps DB by name into target directory."""
    sudo_pg = partial(ctx.sudo, user='postgres')

    target_path = Path(target_dir) / 'db.dump'
    fmt = '-Fc' if binary else ''

    sudo_pg(f'pg_dump {fmt} {db_name} > {target_path}')

    return target_path


def restore(ctx, db_name, source_dir):
    """Restores DB from a file."""
    sudo_pg = partial(ctx.sudo, user='postgres', warn=True)

    source_path = Path(source_dir) / 'db.dump'

    echo(f'Restoring DB dump from {source_path} ...')

    sudo_pg(f'dropdb {db_name}')
    sudo_pg(f'createdb {db_name}')
    sudo_pg(f'pg_restore --dbname {db_name} {source_path}')

    return source_path


def configure(ctx, project_name, project_user):
    """Configures PostgreSQL for the given project."""

    version_ = '.'.join(get_version(ctx)[:-1])

    path_confs = Path(f'/etc/postgresql/{version_}/main/')
    config_name = 'postgresql.conf'
    target_name = f'{project_name}.conf'

    config_linked = link_config(
        ctx,
        title='granular PG',
        name_local=config_name,
        name_remote=target_name,
        dir_remote_confs=path_confs,
    )

    if config_linked:
        # Append into main config an include line.
        append_to_file(ctx, path_confs / config_name, f"include = '{target_name}'")

    def create_db_and_user():
        sudo_pg = partial(ctx.sudo, user='postgres')

        sudo_pg(f'createdb {project_name}', warn=True)
        sudo_pg(f'createuser {project_user}')  # No password. Using Unix domain sockets.
        sudo_pg(f'psql -c "GRANT ALL PRIVILEGES ON DATABASE {project_name} TO {project_user}"')

    create_db_and_user()

    restart(ctx)
