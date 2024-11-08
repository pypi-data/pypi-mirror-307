from .conf import SessionUser, LangType, PlatType, GLOBAL_DEBUG
from .util import fernet_encrypt, base64_decode, base64_encode
try:
    from pg_objectserialization import dumps, loads
except ImportError:
    from .util import dumps, loads
import time
import requests


__all__ = ("GmUser", )
__author__ = "baozilaji@gmail.com"

class GmUser(object):
    def __init__(self, game:str, channel:str, fernet_key:str, gm:str, uid:int=-1,
                 open_id:str='gm', session_key:str='gm', version:int=0, lang:LangType=LangType.zh_CN,
                 plat:PlatType=PlatType.ios):
        self.fernet_key = fernet_key
        self.sessionUser = SessionUser(uid=uid, open_id=open_id, gm=gm, sessionKey=session_key, game=game,
                                       channel=channel, lang=lang, plat=plat, version=version,
                                       last_req=int(time.time()))
        self.token = self._build_authentication()

    def _build_authentication(self):
        return " ".join([self.sessionUser.game,
                         fernet_encrypt(self.sessionUser.json().encode(), self.fernet_key).decode()])

    def _build_header(self):
        return {"Authentication": self.token}

    def post_data(self, url:str, data:dict):
        headers = self._build_header()
        data = base64_encode(dumps(data, p=GLOBAL_DEBUG))
        resp = requests.post(url, data=data, headers=headers)
        if "Authentication" in resp.headers:
            self.token = resp.headers["Authentication"]
        out = loads(base64_decode(resp.text.encode()), p=GLOBAL_DEBUG)
        return out