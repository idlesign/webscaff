from textwrap import dedent

from invoke import task

from ..sys import pg as sys_pg, fs


def bootstrap(ctx):
    """Bootstraps PostgreSQL for the project."""

    sys_pg.configure(
        ctx,
        project_name=ctx.project.name,
        project_user=ctx.project.user)


def dump(ctx, target_dir):
    """Dumps project Database into a target directory."""
    sys_pg.dump(ctx, ctx.project.name, target_dir=target_dir)


def restore(ctx, source_dir):
    """Restores project Database from a backup directory."""
    sys_pg.restore(ctx, ctx.project.name, source_dir=source_dir)


@task
def psql(ctx, command=None):
    """Launches psql command line utility.

    :param ctx:

    :param command: Command to execute in psql, or a filepath
        to a file containing such commands.

    """
    command = command or ''

    if command:
        opt = 'f' if '/' in command else 'c'
        command = f' -{opt} "{command}"'

    ctx.sudo(f'psql{command}', user=ctx.project.user)


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

    command = fs.make_tmp_file(ctx, dedent(command))

    psql(ctx, command)


@task
def reindex(ctx, table):
    """Launches psql command to reindex given table.

    Useful to reclaim space from bloated indexes.

    :param ctx:

    :param str table: Table name

    """
    psql(ctx, f'REINDEX TABLE {table}')
