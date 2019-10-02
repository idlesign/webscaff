from invoke import task


@task
def cat(ctx, path):
    """Outputs file content."""
    ctx.sudo('cat %s' % path)


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


def gzip_dir(ctx, src, target_fname, change_dir=None, do_sudo=False):
    """GZips a directory."""
    arch_ext = '.tar.gz'

    if arch_ext not in target_fname:
        target_fname = '%s%s' % (target_fname, arch_ext)

    change_dir = change_dir or ''
    if change_dir:
        change_dir = '-C %s' % change_dir

    command = ctx.sudo if do_sudo else ctx.run
    command('tar -czf %s %s %s' % (target_fname, change_dir, src))

    return target_fname


def tail(ctx, filepath):
    """Tails a file to output."""
    # todo maybe use a more powerful tail from orchestra
    ctx.sudo('tail -f %s' % filepath)
