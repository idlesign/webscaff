from ..utils import collection_from_sub
from .proj.utils import bootstrap, rollout, backup
from .proj.log import stream
from .proj.uwsgi import reload_touch
from .proj.service import restart
from .sys.utils import reboot, info


ns = collection_from_sub(__file__, __name__)
ns.add_task(backup)
ns.add_task(bootstrap, name='initialize')
ns.add_task(info)
ns.add_task(reboot)
ns.add_task(reload_touch, name='reload')
ns.add_task(restart)
ns.add_task(rollout)
ns.add_task(stream, name='log')
