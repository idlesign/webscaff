from .fs import upload_configs
from .utils import bootstrap, backup, restore, py
from ...utils import collection_from_sub

ns = collection_from_sub(__file__, __name__)
ns.register_task(bootstrap, name='initialize')
ns.register_task(backup)
ns.register_task(py)
ns.register_task(restore)
ns.register_task(upload_configs, name='upconf')
