from .utils import bootstrap, backup, restore
from ...utils import collection_from_sub


ns = collection_from_sub(__file__, __name__)
ns.register_task(bootstrap, name='initialize')
ns.register_task(backup)
ns.register_task(restore)
