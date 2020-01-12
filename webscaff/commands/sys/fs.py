from pathlib import Path
from uuid import uuid4

from invoke import task
from patchwork.files import append, exists

from ..utils import echo, cd_sudo


@task
def cat(ctx, path):
    """Outputs file content."""
    ctx.sudo('cat %s' % path)


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
    fpath = '/tmp/wscf_%s' % uuid4()

    append_to_file(ctx, fpath, contents)

    return fpath


def mkdir(ctx, path):
    """Creates a directory."""
    ctx.sudo('mkdir -p %s' % path)


def chmod(ctx, path, mode):
    """Change fs object permissions."""
    ctx.sudo('chmod %s %s' % (mode, path))


def chown(ctx, path, user, group):
    """Sets owner for path contents recursively."""
    ctx.sudo('chown -R %s:%s %s' % (user, group, path))


def touch(ctx, fpath):
    """Creates a file or updates modified date if already exists."""
    ctx.run('touch %s' % fpath)


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

    ctx.sudo('setfacl -R%(mode)s "%(acl)s" %(path)s' % {
        'mode': mode,
        'acl': acl,
        'path': path
    })


def rm(ctx, target, force=True):
    """Removes target file or directory recursively."""
    ctx.sudo('rm -r%s %s' % ('f' if force else '', target))


def gzip_extract(ctx, archive, target_dir=None, do_sudo=False):
    """Extracts gzipped archive into a current directory."""

    target_dir = target_dir or archive.with_name(archive.name.replace('.tar.gz', ''))

    mkdir(ctx, target_dir)

    echo('Extract into %s ...' % target_dir)

    method = ctx.sudo if do_sudo else ctx.run
    method('tar -xzf %s -C %s' % (archive, target_dir))

    return target_dir


def gzip_dir(ctx, src, target_fname, do_sudo=False):
    """GZips a directory."""
    target_fname = str(target_fname)

    arch_ext = '.tar.gz'

    if arch_ext not in target_fname:
        target_fname = '%s%s' % (target_fname, arch_ext)

    echo('Creating %s ...' % target_fname)

    command = 'tar -czf %s *' % target_fname
    command = cd_sudo(src, command)
    method = ctx.sudo if do_sudo else ctx.run

    method(command, warn=True)

    return Path(target_fname)


@task
def tail(ctx, filepath):
    """Tails a file to output."""
    # todo maybe use a more powerful tail from orchestra
    ctx.sudo('tail -f %s' % filepath)


def swap_init(ctx):
    """Creates a swap file."""
    swap_file = '/swapfile'
    ctx.sudo('dd if=/dev/zero of=%s bs=1024 count=524288' % swap_file)
    chmod(ctx, swap_file, 600)
    ctx.sudo('mkswap %s' % swap_file)
    swap_on(ctx)


def swap_on(ctx):
    """Turns on swap."""
    swap_file = '/swapfile'
    ctx.sudo('swapon %s' % swap_file)


def swap_off(ctx):
    """Turns off swap."""
    swap_file = '/swapfile'
    ctx.sudo('swapoff %s' % swap_file)
