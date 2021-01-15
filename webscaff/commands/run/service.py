from pathlib import Path

from invoke import task


def bootstrap(ctx):
    """Creates a systemd service file and to enable it."""

    project_name = ctx.project.name
    service_file = Path(ctx.paths.remote.configs) / f'{project_name}.service'

    ctx.sudo(f'systemctl enable --now {service_file}')


def restart(ctx):
    """Restarts project service."""
    ctx.sudo(f'systemctl restart {ctx.project.name}')


def status(ctx):
    """Returns project service status."""
    ctx.sudo(f'systemctl status {ctx.project.name}')


@task
def stop(ctx):
    """Stops project service."""
    ctx.sudo(f'systemctl stop {ctx.project.name}')
