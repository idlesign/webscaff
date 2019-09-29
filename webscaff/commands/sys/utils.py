from invoke import task

from .fs import chmod


@task
def reboot(ctx):
    """Reboots remote immediately."""
    ctx.sudo('shutdown -r now')


def set_locale(ctx, locale='ru_RU'):
    """Generates and sets given UTF-8 locale.

    Default: ru_Ru

    """
    ctx.sudo('locale-gen "%s.UTF-8"' % locale)
    ctx.sudo('dpkg-reconfigure locales')
    ctx.sudo('update-locale LC_ALL=%(locale)s.UTF-8 LANG=%(locale)s.UTF-8' % {'locale': locale})


@task
def info(ctx):
    """Prints out remote system information, including kernel info and timezone."""
    ctx.run('uname -a')
    ctx.run('cat /etc/timezone')
    ctx.run('uptime')
    ctx.run('df -h')


@task
def shutdown(ctx):
    """Turns the remote off immediately."""
    ctx.sudo('shutdown now')


@task
def swap_init(ctx):
    """Creates a swap file."""
    swap_file = '/swapfile'
    ctx.sudo('dd if=/dev/zero of=%s bs=1024 count=524288' % swap_file)
    chmod(ctx, swap_file, 600)
    ctx.sudo('mkswap %s' % swap_file)
    swap_on()


@task
def swap_on(ctx):
    """Turns on swap."""
    swap_file = '/swapfile'
    ctx.sudo('swapon %s' % swap_file)


@task
def swap_off(ctx):
    """Turns off swap."""
    swap_file = '/swapfile'
    ctx.sudo('swapoff %s' % swap_file)


@task
def tail(ctx, fname):
    """Tails a file to output."""
    ctx.sudo('tail -f %s' % fname)
