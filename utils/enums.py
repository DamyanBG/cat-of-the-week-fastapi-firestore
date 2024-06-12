from enum import Enum


class RoleType(str, Enum):
    voter = "voter"
    participant = "participant"
    admin = "admin"
    moderator = "moderator"
