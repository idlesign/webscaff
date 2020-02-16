import pytest


from webscaff.overrides import WebscaffConfig


def test_defaults():

    config = WebscaffConfig()

    with pytest.raises(ValueError):
        config.check_required()

    config.project.name = 'testme'
    config.project.repo = 'https://repome'

    config.check_required()
    config.contribute_missing()


    assert config.forward_agent
    assert config.tasks['collection_name'] == 'wscaffs'
    assert config.python == 'python3'
    assert config.dir_conf == 'conf'

    project = config.project
    assert project.name == 'testme'
    assert project.user == 'testme'
    assert project.group == 'testme'
    assert project.repo == 'https://repome'
    assert project.domain == ''
    assert project.email == ''

    paths = config.paths

    paths_remote = paths.remote
    assert paths_remote.temp == '/tmp'
    assert paths_remote.cache == '/var/cache/testme'
    assert paths_remote.projects == '/srv'
    assert paths_remote.configs == '/srv/testme/conf'
    assert paths_remote.repo == '/srv/testme'

    assert paths_remote.project.home == '/srv/testme'
    assert paths_remote.project.base == '/srv/testme/testme'
    assert paths_remote.project.venv.root == '/srv/testme/venv'
    assert paths_remote.project.venv.bin == '/srv/testme/venv/bin'

    remote_state = paths_remote.project.state
    assert remote_state.static == '/var/lib/testme/static'
    assert remote_state.media == '/var/lib/testme/media'
    assert remote_state.certbot == '/var/lib/testme/certbot'
    assert remote_state.spool == '/var/lib/testme/spool'
    assert remote_state.reloader == '/var/lib/testme/reloader'
    assert remote_state.environ == '/var/lib/testme/environ'

    paths_local = paths.local
    assert paths_local.configs.endswith('/tests/conf')
    assert paths_local.project.home.endswith('/tests')
    assert paths_local.project.base.endswith('/tests/testme')
    assert paths_local.project.state.root.endswith('/tests/state')
    assert paths_local.project.state.dumps.endswith('/tests/state/dumps')
