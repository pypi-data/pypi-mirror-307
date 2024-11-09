from .app import *
from .assets import *
from .input import *
from .events import *
from .entity import *
from .object import *
from .gameworld import *
from .resource import *

import os, platform, blackforge.version as ver
if "BLACKFORGE_NO_PROMT" not in os.environ:
    print(
        f"BlackForge {ver.BLACKFORGE_MAJOR}.{ver.BLACKFORGE_MINOR}.{ver.BLACKFORGE_PATCH} | Random Quote Here..."
    )