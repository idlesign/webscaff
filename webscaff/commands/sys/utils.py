from invoke import task


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
def tail(ctx, fname):
    """Tails a file to output."""
    ctx.sudo('tail -f %s' % fname)
