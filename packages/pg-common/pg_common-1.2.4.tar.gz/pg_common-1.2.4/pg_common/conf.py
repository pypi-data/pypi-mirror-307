from enum import unique, Enum
from typing import Optional
from pydantic import BaseModel
from pg_common import DictValType

__all__ = ["RuntimeException", "GLOBAL_DEBUG", "SessionUser", "Context", "LangType", "GenderType", "PlatType",
           "BaseInfo", "RewardItem"]
__author__ = "baozilaji@gmail.com"


GLOBAL_DEBUG = False


class RuntimeException(Exception):
    """
      全局运行时异常
    """
    def __init__(self, name: str, msg: str):
        self.name = name
        self.msg = msg


@unique
class LangType(Enum):
    zh_CN = "zh-CN"
    en_US = "en-US"


@unique
class PlatType(Enum):
    ios = "ios"
    android = "and"
    html5 = "h5"
    windows = "win"

@unique
class GenderType(Enum):
    male = "male"
    female = "female"
    unknown = "unknown"


class RewardItem(BaseModel):
    id: int
    count: int
    expire: Optional[int] = 0
    extra: Optional[int] = 0

"""
BaseInfo对象，如果数据结构变化，依赖的模块都需要更新重启
"""
class BaseInfo(BaseModel):
    uid: int
    open_id: str
    name: Optional[str] = ''
    head_url: Optional[str] = ''
    gender: Optional[int] = 0


class SessionUser(BaseModel):
    uid: int
    open_id: str
    sessionKey: str
    last_req: int
    game: str
    channel: str
    version: int
    plat: PlatType
    lang: LangType
    info: Optional[BaseInfo] = None
    gm: Optional[str] = None
    req_cnt: Optional[int] = 0


class Context(BaseModel):
    log: dict[str, DictValType] = {}
    req: Optional[dict] = {}
    resp: Optional[dict] = {}
    path: Optional[str] = ''
    user: Optional[SessionUser] = None
