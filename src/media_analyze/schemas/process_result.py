from pydantic import BaseModel, computed_field, Json


class ProcessResult(BaseModel):
    accuracy: float
    top_class: str
    top_list: list

    @computed_field
    def top_list_count(self) -> int:
        return len(self.top_list)


class ProcessResultWithId(BaseModel):
    result_id: str
    data: Json[ProcessResult] | ProcessResult | None = None
