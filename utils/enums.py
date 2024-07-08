from enum import Enum


class RoleType(str, Enum):
    user = "user"
    admin = "admin"
    moderator = "moderator"


class VoteEnum(str, Enum):
    Like = "like"
    Dislike = "dislike"
    Pass = "pass"
