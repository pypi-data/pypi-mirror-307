from pydantic import BaseModel

from .merge_method_enum import MergeMethodEnum
from .user import User


class AutoMerge(BaseModel):
    enabled_by: User
    merge_method: MergeMethodEnum
    commit_title: str
    commit_message: str
