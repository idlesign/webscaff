from uuid import uuid4
from datetime import datetime
from os import makedirs
from pathlib import Path

from . import fs, dj, service, uwsgi, venv, git, certbot, pg
from ..sys import usr, apt, utils as sys_utils, fs as sys_fs
from ..utils import echo


def bootstrap(ctx):
    """Initializes a remote for your project."""

    project = ctx.project
    me = usr.whoami(ctx)

    usr.create(ctx, project.user)
    just_added = usr.add_to_group(ctx, me, project.group)

    if just_added:
        echo(' * Initial preparation is done. Please rerun the command to proceed.')
        return

    apt.bootstrap(ctx)
    fs.bootstrap(ctx)
    git.bootstrap(ctx)
    fs.upload_configs(ctx)
    venv.bootstrap(ctx)
    pg.bootstrap(ctx)
    dj.bootstrap(ctx)
    uwsgi.bootstrap(ctx)
    service.bootstrap(ctx)
    certbot.bootstrap(ctx)

    echo('* Done. Reboot now ...')

    sys_utils.reboot(ctx)


def rollout(ctx, upgrade_venv=False):
    """Updates remote files from remote repository and rolls out project.

    :param ctx:
    :param upgrade_venv: Whether to update venv using requirements file.

    """
    git.pull(ctx)

    if upgrade_venv:
        venv.upgrade(ctx)

    dj.rollout(ctx)
    uwsgi.reload_touch(ctx)


def backup(ctx):
    """Creates a project backup."""

    path_dump_local = ctx.paths.local.project.state.dumps

    makedirs(path_dump_local, exist_ok=True)

    path_dumps = Path(ctx.paths.remote.project.state.dumps)
    path_dump = path_dumps / ('%s-%s_dump' % (
        datetime.now().strftime('%Y-%m-%dT%H%M'),
        ctx.project.name
    ))

    # Create a subdirectory in dumps.
    sys_fs.mkdir(ctx, path_dump)

    try:
        dj.dump(ctx, target_dir=path_dump / 'media')
        certbot.dump(ctx, target_dir=path_dump / 'certbot')
        pg.dump(ctx, target_dir=path_dump)

        # Archive everything dumped so far.
        path_dump_arch = sys_fs.gzip_dir(ctx, path_dump, path_dump)

        try:
            # Download it to local machine.
            ctx.get(path_dump_arch, str(Path(path_dump_local) / path_dump_arch.name))

        finally:
            sys_fs.rm(ctx, path_dump_arch)

    finally:
        # Remove dumps subdir.
        sys_fs.rm(ctx, path_dump)


def restore(ctx, backup):
    """Restores project related data from a backup file."""
    backup = Path(backup).absolute()

    if not backup.exists():
        echo("Backup file doesn't exist: %s" % backup)
        return

    path_dumps = Path(ctx.paths.remote.project.state.dumps)
    path_remote_archive = path_dumps / backup.name

    echo('Uploading %s ...' % backup)

    ctx.put('%s' % backup, '%s' % path_remote_archive)
    path_remote = sys_fs.gzip_extract(ctx, path_remote_archive)

    try:
        sys_fs.rm(ctx, path_remote_archive)
        dj.restore(ctx, path_remote)
        certbot.restore(ctx, path_remote)
        pg.restore(ctx, path_remote)

    finally:
        sys_fs.rm(ctx, path_remote)


def py(ctx, filepath):
    """Run given file with Python script on remote."""

    script = Path(filepath).absolute()

    if not script.exists():
        echo("File doesn't exist: %s" % script)
        return

    path_temp = Path(ctx.paths.remote.temp)
    path_remote_script = path_temp / str(uuid4())

    ctx.put('%s' % script, '%s' % path_remote_script)

    try:
        with venv.venv_context(ctx):
            ctx.run('python %s' % path_remote_script, warn=True)

    finally:
        sys_fs.rm(ctx, path_remote_script)
