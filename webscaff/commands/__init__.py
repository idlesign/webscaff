from invoke import task

from .run.log import stream
from .run.service import restart, status
from .run.utils import bootstrap, rollout, backup
from .run.uwsgi import reload_touch, on_503, off_503
from .sys.utils import reboot, info
from ..utils import collection_from_sub

ns = collection_from_sub(__file__, __name__)


def register_task(task_func, name=None):
    ns.add_task(task(task_func), name=name)


register_task(backup)
register_task(bootstrap, name='initialize')
register_task(info)
register_task(on_503, name='off')
register_task(off_503, name='on')
register_task(reboot)
register_task(reload_touch, name='reload')
register_task(restart)
register_task(rollout)
register_task(status)
register_task(stream, name='log')
