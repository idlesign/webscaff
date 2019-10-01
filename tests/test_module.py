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
    assert config.user_webserver == 'www-data'
    assert config.dir_conf == 'conf'

    project = config.project
    assert project.name == 'testme'
    assert project.user == 'testme'
    assert project.group == 'testme'
    assert project.repo == 'https://repome'
    assert not project.repo_slim
    assert project.domain == ''
    assert project.email == ''

    paths = config.paths

    paths_remote = paths.remote
    assert paths_remote.temp == '/tmp'
    assert paths_remote.cache == '/tmp/cache_testme'
    assert paths_remote.projects == '/srv'
    assert paths_remote.configs == '/srv/testme/conf'
    assert paths_remote.repo == '/srv/testme'

    assert paths_remote.project.home == '/srv/testme'
    assert paths_remote.project.base == '/srv/testme/testme'
    assert paths_remote.project.venv.root == '/srv/testme/venv'
    assert paths_remote.project.venv.bin == '/srv/testme/venv/bin'

    remote_runtime = paths_remote.project.runtime
    assert remote_runtime.certbot == '/srv/testme/runtime/certbot'
    assert remote_runtime.spool == '/srv/testme/runtime/spool'
    assert remote_runtime.reloader == '/srv/testme/runtime/reloader'
    assert remote_runtime.environ == '/srv/testme/runtime/environ'

    paths_local = paths.local
    assert paths_local.configs.endswith('/conf')
    assert paths_local.project.home.endswith('tests')
    assert paths_local.project.base.endswith('tests/testme')
