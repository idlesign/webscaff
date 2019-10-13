from pathlib import Path

from invoke import task


def bootstrap(ctx):
    """Creates a systemd service file and to enable it."""

    project_name = ctx.project.name
    service_file = Path(ctx.paths.remote.configs) / ('%s.service' % project_name)

    ctx.sudo('systemctl enable --now %s' % service_file)


def restart(ctx):
    """Restarts project service."""
    ctx.sudo('systemctl restart %s' % ctx.project.name)


def status(ctx):
    """Returns project service status."""
    ctx.sudo('systemctl status %s' % ctx.project.name)


@task
def stop(ctx):
    """Stops project service."""
    ctx.sudo('systemctl stop %s' % ctx.project.name)
