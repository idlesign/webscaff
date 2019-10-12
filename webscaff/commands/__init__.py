from .run.log import stream
from .run.service import restart, status
from .run.utils import bootstrap, rollout, backup
from .run.uwsgi import reload_touch, maintenance_on, maintenance_off
from .sys.utils import reboot, info
from ..utils import collection_from_sub

ns = collection_from_sub(__file__, __name__)
ns.add_task(backup)
ns.add_task(bootstrap, name='initialize')
ns.add_task(info)
ns.add_task(maintenance_on, name='off')
ns.add_task(maintenance_off, name='on')
ns.add_task(reboot)
ns.add_task(reload_touch, name='reload')
ns.add_task(restart)
ns.add_task(rollout)
ns.add_task(status)
ns.add_task(stream, name='log')
