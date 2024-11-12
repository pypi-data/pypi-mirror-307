from pydantic import BaseModel

from .enterprise import Enterprise
from .installation import Installation
from .organization import Organization
from .pull_request import PullRequest
from .pull_request_action_enum import PullRequestActionEnum
from .repository import Repository
from .user import User


class PullRequestEvent(BaseModel):
    action: PullRequestActionEnum
    enterprise: Enterprise | None = None
    installation: Installation | None = None
    number: int
    organization: Organization | None = None
    pull_request: PullRequest
    repository: Repository
    sender: User
