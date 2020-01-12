import os

import pytest
from invoke.context import Context
from invoke.executor import Executor


if not os.getcwd().endswith('tests'):
    # To run both from package root and tests/ subdir.
    os.chdir('tests/')


context_commands = []


class CommandResult:

    def __init__(self, command):
        self.command = command

    stdout = 'tstout'
    ok = True


class MockContext(Context):

    def _run(self, runner, command, **kwargs):
        context_commands.append(command)
        return CommandResult(command)

    def _sudo(self, runner, command, **kwargs):
        context_commands.append(command)
        return CommandResult(command)

    def cd(self, path):
        context_commands.append('cd %s' % path)
        return super().cd(path)

    def put(self, what, where):
        context_commands.append('put %s %s' % (what, where))


class MockExecutor(Executor):

    def expand_calls(self, calls):
        for call in calls:
            call.make_context = lambda config: MockContext(config)
        return super().expand_calls(calls)


@pytest.fixture
def run_command_mock(monkeypatch):

    monkeypatch.chdir('../demo')
    monkeypatch.setattr('webscaff.overrides.WebscaffExecutor', MockExecutor)

    from webscaff.cli import program

    def run_command_mock_(command, *args):
        try:
            program.run(['webscaff', command] + list(args), exit=False)
            commands = list(context_commands)
            return commands
        finally:
            context_commands.clear()

    return run_command_mock_
