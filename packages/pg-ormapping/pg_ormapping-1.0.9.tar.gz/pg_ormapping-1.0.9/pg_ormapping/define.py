from enum import Enum, unique


class GlobalRedisKey(Enum):
    """
      redis key的父类，枚举类型，方便统一命名，避免冲突
    """
    pass


@unique
class ObjectType(Enum):
    REDIS = 0
    MONGO = 1
    BOTH = 2

