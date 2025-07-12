import warnings

from . import VERSION
from .commands import ns
from .overrides import WebscaffConfig, WebscaffExecutor, WebscaffProgram

warnings.filterwarnings('ignore')  # filter out CryptographyDeprecationWarning and others


program = WebscaffProgram(
    name='Webscaff',
    version=VERSION,
    executor_class=WebscaffExecutor,
    config_class=WebscaffConfig,
    namespace=ns,
)
