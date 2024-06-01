from typing import Any

from src.core.serializers.base import BaseSerializer
from src.media_analyze.schemas.process_result import ProcessResultWithId


class MediaSerializer(BaseSerializer):
    def serialize(self, data: Any) -> ProcessResultWithId:
        return ProcessResultWithId.model_validate(data, from_attributes=True)
