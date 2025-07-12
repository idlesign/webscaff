from .run.log import stream
from .run.service import restart, status
from .run.utils import rollout, cfg
from .run.uwsgi import reload_touch, on_503, off_503
from .sys.utils import reboot, info
from ..utils import collection_from_sub


ns = collection_from_sub(__file__, __name__)

ns.register_task(info)
ns.register_task(on_503, name='off')
ns.register_task(off_503, name='on')
ns.register_task(reload_touch, name='reload')
ns.register_task(restart)
ns.register_task(rollout)
ns.register_task(status)
ns.register_task(cfg)
ns.register_task(stream, name='log')
