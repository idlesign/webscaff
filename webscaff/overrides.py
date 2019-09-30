from pathlib import Path

from fabric.main import Fab, Executor, Config
from invoke.config import merge_dicts


class WebscaffExecutor(Executor):
    """Custom webscaff executor."""


class WebscaffConfig(Config):

    prefix = 'wscaff'

    def check_required(self):
        project = self.project

        for setting_name in ('name', 'repo'):
            if not getattr(project, setting_name):
                raise ValueError("Please provide a value for 'project.%s' setting." % setting_name)

    def contribute_missing(self):

        project_name = self.project.name

        if not self.project.user:
            self.project.user = project_name

        if not self.project.group:
            self.project.group = self.project.user

        # Remote paths:
        paths = self.paths.remote.project

        if not paths.home:
            paths.home = '%s/%s' % (self.paths.remote.projects, project_name)

        home_remote = Path(paths.home)

        if not paths.base:
            paths.base = str(home_remote / project_name)

        if not self.paths.remote.repo:
            self.paths.remote.repo = paths.base if self.project.repo_slim else paths.home

        if not paths.venv.root:
            paths.venv.root = str(home_remote / 'venv')

        if not paths.venv.bin:
            paths.venv.bin = str(Path(paths.venv.root) / 'bin')

        if not self.paths.remote.cache:
            self.paths.remote.cache = '%s/cache_%s' % (self.paths.remote.temp, project_name)

        remote_runtime = paths.runtime
        remote_runtime_dir = home_remote / 'runtime'

        if not remote_runtime.certbot:
            remote_runtime.certbot = str(remote_runtime_dir / 'certbot')

        if not remote_runtime.spool:
            remote_runtime.spool = str(remote_runtime_dir / 'spool')

        if not remote_runtime.reloader:
            remote_runtime.reloader = str(remote_runtime_dir / 'reloader')

        if not remote_runtime.maintenance:
            remote_runtime.maintenance = str(remote_runtime_dir / 'maintenance')

        if not remote_runtime.environ:
            remote_runtime.environ = str(remote_runtime_dir / 'environ')

        # Local paths:
        paths = self.paths.local.project

        if not paths.base:
            paths.base = str(Path(paths.home) / project_name)

        # Local and remote configs:
        self.paths.local.configs = str(Path(self.paths.local.project.home) / self.dir_conf)
        self.paths.remote.configs = str(home_remote / self.dir_conf)

    @staticmethod
    def global_defaults():
        defaults = Config.global_defaults()

        ours = {
            'forward_agent': True,  # Transparently access private VCS repos, etc.

            'tasks': {'collection_name': 'wscaffs'},

            'python': 'python3',

            'user_webserver': 'www-data',
            'dir_conf': 'conf',

            'project': {
                'name': None,
                'user': None,
                'group': None,
                'repo': None,  # url
                'repo_slim': False,  # slim if no conf/ dir and etc.
                'domain': '',
                'email': '',
            },

            'paths': {
                'remote': {
                    'temp': '/tmp',
                    'cache': None,
                    'projects': '/srv',
                    'configs': None,
                    'repo': None,

                    'project': {
                        'home': None,
                        'base': None,
                        'runtime': {
                            'certbot': None,  # Certbot webroot dir
                            'spool': None,  # uWSGI spooler dir
                            'reloader': None,  # uWSGI touch reload file
                            'maintenance': None,  # uWSGI maintenance trigger file
                            'environ': None,  # Project environ type file
                        },
                        'venv': {
                            'root': None,
                            'bin': None,
                        },
                    },
                },
                'local': {
                    'configs': None,
                    'project': {
                        'home': str(Path.cwd()),
                        'base': None,
                    }
                }
            }

        }
        merge_dicts(defaults, ours)

        return defaults


class WebscaffProgram(Fab):

    def execute(self):
        hosts = self.core[0].args.hosts

        if not hosts.value:
            # Load hosts from config if not passed via command -H argument
            remotes = self.config.remotes
            hosts.value = ','.join(remotes) if isinstance(remotes, list) else remotes

        super().execute()

    def parse_collection(self):
        super().parse_collection()
        # Load configuration from working directory,
        # but get tasks from webscaff package.
        self.config.set_project_location(str(Path.cwd()))
        self.config.load_project()

    def update_config(self):
        super().update_config()

        config = self.config
        config.check_required()
        config.contribute_missing()
