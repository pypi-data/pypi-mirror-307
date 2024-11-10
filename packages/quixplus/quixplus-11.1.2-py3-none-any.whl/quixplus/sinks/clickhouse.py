import logging
from typing import Any, Dict, List, Tuple

from quixstreams.models import HeaderValue
from quixstreams.sinks.base.batch import BatchingSink, SinkBatch
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)

class CLickhouseSink:
    pass
