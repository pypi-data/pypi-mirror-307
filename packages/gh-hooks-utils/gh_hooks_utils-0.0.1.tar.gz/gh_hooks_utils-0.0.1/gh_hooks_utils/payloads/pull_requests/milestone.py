from pydantic import BaseModel

from .milestone_state_enum import MilestoneStateEnum
from .user import User


class Milestone(BaseModel):
    url: str
    html_url: str
    labels_url: str
    id: int
    node_id: str
    number: int
    state: MilestoneStateEnum
    title: str
    description: str | None
    create: User
    open_issues: int
    closed_issues: int
    created_at: str
    updated_at: str
    closed_at: str | None
    due_on: str | None
