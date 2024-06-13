from enum import Enum


class RoleType(str, Enum):
    user = "user"
    admin = "admin"
    moderator = "moderator"
