from pydantic import BaseModel


class Installation(BaseModel):
    id: int
    node_id: str
