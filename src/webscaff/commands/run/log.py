from invoke import task


def stream(ctx):
    """Outputs project service log."""
    ctx.sudo(f'journalctl -fu {ctx.project.name}')
