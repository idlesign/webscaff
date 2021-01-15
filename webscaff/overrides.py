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

        def init_state_dirs(state_root):

            state = paths.state

            if paths.state.root:
                state_root = Path(paths.state.root)

            else:
                paths.state.root = str(state_root)

            # Set defaults for runtime subdirectories.
            for state_dir_name in state._config.keys():

                if state_dir_name == 'root':
                    continue

                if getattr(state, state_dir_name, None) is None:
                    setattr(state, state_dir_name, str(state_root / state_dir_name))

        project_name = self.project.name

        if not self.project.user:
            self.project.user = project_name

        if not self.project.group:
            self.project.group = self.project.user

        # Remote paths:
        paths = self.paths.remote.project

        if not paths.home:
            paths.home = f'{self.paths.remote.projects}/{project_name}'

        home_remote = Path(paths.home)

        if not paths.base:
            paths.base = str(home_remote / project_name)

        if not self.paths.remote.repo:
            self.paths.remote.repo = paths.home

        if not paths.venv.root:
            paths.venv.root = str(home_remote / 'venv')

        if not paths.venv.bin:
            paths.venv.bin = str(Path(paths.venv.root) / 'bin')

        if not self.paths.remote.cache:
            self.paths.remote.cache = str(Path('/var/cache') / project_name)

        # Initialize remote state dirs.
        init_state_dirs(state_root=Path('/var/lib') / project_name)

        # Local paths:
        paths = self.paths.local.project

        if not paths.base:
            paths.base = str(Path(paths.home) / project_name)

        # Initialize local state dirs.
        init_state_dirs(state_root=Path(paths.home) / 'state')

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

            'dir_conf': 'conf',

            'project': {
                'name': None,
                'user': None,
                'group': None,
                'repo': None,  # url
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
                        'state': {
                            'root': None,  # State directory root
                            'dumps': None,  # Dumps (DB, etc.) directory
                            'static': None,  # Django static directory
                            'media': None,  # Django media directory
                            'certbot': None,  # Certbot webroot dir
                            'spool': None,  # uWSGI spooler dir
                            'reloader': None,  # uWSGI touch reload file
                            'maintenance': None,  # uWSGI maintenance trigger file
                            'environ': None,  # Project environ type file
                            'bootstrap': None,  # Boostrap stage log file
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
                        'state': {
                            'root': None,
                            'dumps': None,
                        }
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
