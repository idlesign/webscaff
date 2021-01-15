from invoke import task

from ..utils import echo


@task
def reboot(ctx):
    """Reboots remote immediately."""
    ctx.sudo('shutdown -r now')


def set_locale(ctx, locale='ru_RU'):
    """Generates and sets given UTF-8 locale.

    Default: ru_Ru

    """
    ctx.sudo(f'locale-gen "{locale}.UTF-8"')
    ctx.sudo('dpkg-reconfigure locales')
    ctx.sudo(f'update-locale LC_ALL={locale}.UTF-8 LANG={locale}.UTF-8')


def info(ctx):
    """Prints out remote system information, including kernel info and timezone."""
    ctx.run('who')
    echo('')
    ctx.run('uname -a')
    echo('')
    ctx.run('cat /etc/timezone')
    echo('')
    ctx.run('uptime')
    echo('')
    ctx.run('df -h')
    echo('')
    ctx.sudo('journalctl --disk-usage')


@task
def shutdown(ctx):
    """Turns the remote off immediately."""
    ctx.sudo('shutdown now')
