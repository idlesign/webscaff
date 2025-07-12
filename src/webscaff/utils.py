from importlib import import_module
from pathlib import Path

from invoke import Collection, task


class WebscaffCollection(Collection):

    def register_task(self, task_func, name=None):
        self.add_task(task(task_func), name=name)


def collection_from_sub(filepath, name):
    """Task gatherer.

    :param filepath:
    :param name:

    """
    dir_base = Path(filepath).parent
    ns = WebscaffCollection()

    def contribute(items):

        for item in items:
            module = import_module(f'.{item.stem}', name)
            ns.add_collection(module)

    dir_packages = [path.parent for path in dir_base.glob('*/__init__.py')]
    contribute(dir_packages)

    submodules = [path for path in dir_base.glob('*.py') if not path.stem.startswith('_')]
    contribute(submodules)

    return ns
