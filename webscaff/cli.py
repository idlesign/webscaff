import warnings

from . import VERSION_STR
from .commands import ns
from .overrides import WebscaffProgram, WebscaffExecutor, WebscaffConfig

warnings.filterwarnings('ignore')  # filter out CryptographyDeprecationWarning and others


program = WebscaffProgram(
    name='Webscaff',
    version=VERSION_STR,
    executor_class=WebscaffExecutor,
    config_class=WebscaffConfig,
    namespace=ns,
)
