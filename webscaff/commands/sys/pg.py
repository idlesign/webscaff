from functools import partial
from pathlib import Path
from textwrap import dedent

from invoke import task

from .fs import tail, make_tmp_file, append_to_file
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


@task
def psql(ctx, command=None):
    """Launches psql command line utility.

    :param ctx:

    :param command: Command to execute in psql, or a filepath
        to a file containing such commands.

    """
    command = command or ''

    if command:
        command = ' -%s "%s"' % ('f' if '/' in command else 'c', command)

    ctx.sudo('psql%s' % command, user=ctx.project.user)


@task
def sizes(ctx, limit=10):
    """Launches psql command to output top n table sizes (data and indexes).

    :param ctx:
    :param int limit: Show top n tables.

    """
    command = '''
    SELECT
        name AS "Table",
        pg_size_pretty(size_data) AS "Size Data",
        pg_size_pretty(size_idx) AS "Size Indexes",
        pg_size_pretty(size_total) AS "Size Total"

    FROM (

        SELECT
            name,
            pg_table_size(path) AS size_data,
            pg_indexes_size(path) AS size_idx,
            pg_total_relation_size(path) AS size_total

        FROM (
            SELECT
              ('"' || table_schema || '"."' || table_name || '"') AS path,
              (table_schema || '.' || table_name) AS name
            FROM information_schema.tables
        ) AS tables
        ORDER BY size_total DESC

    ) AS pretty_sizes LIMIT %s;
    ''' % limit

    command = make_tmp_file(ctx, dedent(command))

    psql(ctx, command)


@task
def reindex(ctx, table):
    """Launches psql command to reindex given table.

    Useful to reclaim space from bloated indexes.

    :param ctx:

    :param str table: Table name

    """
    psql(ctx, 'REINDEX TABLE %s' % table)


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


def dump(ctx, db_name, target_dir):
    """Dumps DB by name into target directory."""
    target_path = Path(target_dir) / 'db.sql'
    ctx.run('pg_dump %s > %s' % (db_name, target_path))
    return target_path


def bootstrap(ctx):
    """Bootstraps PostgreSQL for the project."""
    version_ = '.'.join(get_version(ctx)[:-1])

    project_name = ctx.project.name
    project_user = ctx.project.user

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
