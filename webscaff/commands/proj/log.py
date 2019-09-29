from invoke import task


@task
def stream(ctx):
    """Outputs project service log."""
    ctx.sudo('journalctl -fu %s' % ctx.project.name)