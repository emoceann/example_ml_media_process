from functools import cache

import onnxruntime as rt
import orjson
from onnxruntime import InferenceSession

from src.core.settings import get_settings

settings = get_settings()


@cache
def get_model() -> InferenceSession:
    return rt.InferenceSession(settings.PATH_TO_ML_MODEL)


@cache
def get_labels() -> dict:
    with open(settings.PATH_TO_LABELS, "r") as f:
        return orjson.loads(f.read())
