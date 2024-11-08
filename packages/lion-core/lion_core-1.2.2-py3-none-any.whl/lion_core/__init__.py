import logging

from dotenv import load_dotenv
from lion_service import iModel

from .protocols.operatives.step import Step
from .session import Branch
from .settings import Settings
from .version import __version__

load_dotenv()


__all__ = [
    "Settings",
    "__version__",
    "iModel",
    "Branch",
    "Step",
]

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
