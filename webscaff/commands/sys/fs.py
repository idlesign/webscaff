from pathlib import Path
from uuid import uuid4
from invoke import task
from patchwork.files import append, exists

from ..utils import echo, cd_sudo


@task
def cat(ctx, path, printout=True):
    """Outputs file content.

    :param ctx:
    :param path: Filepath to read.
    :param printout: Whether to print to console.

    """
    return ctx.sudo(f'cat {path}', hide=not printout).stdout


def append_to_file(ctx, filepath, contents):
    """Add contents to a file.

    :param ctx:
    :param str filepath:
    :param str contents:

    """
    if not exists(ctx, filepath):
        touch(ctx, filepath)
    append(ctx, filepath, contents)


def make_tmp_file(ctx, contents):
    """Makes a temporary file with the given content.
    Returns filepath.

    :param ctx:

    :param str contents:

    :rtype: str

    """
    fpath = f'/tmp/wscf_{uuid4()}'

    append_to_file(ctx, fpath, contents)

    return fpath


def mkdir(ctx, path):
    """Creates a directory."""
    ctx.sudo(f'mkdir -p {path}')


def chmod(ctx, path, mode):
    """Change fs object permissions."""
    ctx.sudo(f'chmod {mode} {path}')


def chown(ctx, path, user, group):
    """Sets owner for path contents recursively."""
    ctx.sudo(f'chown -R {user}:{group} {path}')


def touch(ctx, fpath):
    """Creates a file or updates modified date if already exists."""
    ctx.run(f'touch {fpath}')


def setfacl(ctx, path, acl, modify=False):
    """Sets/modifies ACL for a directory/file.

    :param ctx:
    :param path:
    :param acl:
        * u:www-data:--x
        * u::rwX,g::-,o::-,u:idlesign:rwx
        * u::rwx,g::---,o::---,u:idlesign:r-x
    :param modify: Modify or set.

    """
    mode = 'm' if modify else ' --set'
    ctx.sudo(f'setfacl -R{mode} "{acl}" {path}')


def rm(ctx, target, force=True):
    """Removes target file or directory recursively."""
    opt = 'f' if force else ''
    ctx.sudo(f'rm -r{opt} {target}')


def gzip_extract(ctx, archive, target_dir=None, do_sudo=False):
    """Extracts gzipped archive into a current directory."""

    target_dir = target_dir or archive.with_name(archive.name.replace('.tar.gz', ''))

    mkdir(ctx, target_dir)

    echo(f'Extract into {target_dir} ...')

    method = ctx.sudo if do_sudo else ctx.run
    method(f'tar -xzf {archive} -C {target_dir}')

    return target_dir


def gzip_dir(ctx, src, target_fname, do_sudo=False):
    """GZips a directory."""
    target_fname = str(target_fname)

    arch_ext = '.tar.gz'

    if arch_ext not in target_fname:
        target_fname = f'{target_fname}{arch_ext}'

    echo(f'Creating {target_fname} ...')

    command = f'tar -czf {target_fname} *'
    command = cd_sudo(src, command)
    method = ctx.sudo if do_sudo else ctx.run

    method(command, warn=True)

    return Path(target_fname)


@task
def tail(ctx, filepath):
    """Tails a file to output."""
    # todo maybe use a more powerful tail from orchestra
    ctx.sudo(f'tail -f {filepath}')


def swap_init(ctx):
    """Creates a swap file."""
    swap_file = '/swapfile'
    ctx.sudo(f'dd if=/dev/zero of={swap_file} bs=1024 count=524288')
    chmod(ctx, swap_file, 600)
    ctx.sudo(f'mkswap {swap_file}')
    swap_on(ctx)


def swap_on(ctx):
    """Turns on swap."""
    swap_file = '/swapfile'
    ctx.sudo(f'swapon {swap_file}')


def swap_off(ctx):
    """Turns off swap."""
    swap_file = '/swapfile'
    ctx.sudo(f'swapoff {swap_file}')
