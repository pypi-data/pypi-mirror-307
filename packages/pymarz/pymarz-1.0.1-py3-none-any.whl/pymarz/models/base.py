import json
from enum import Enum

from dataclasses import asdict


class HttpMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


class BaseModel:
    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self, ignore_none=True):
        def dict_factory(x):
            from .proxy import ProxyTypes

            result = {}
            for k, v in x:
                if ignore_none and v is None:
                    continue
                if isinstance(v, Enum):
                    v = v.value
                elif isinstance(v, BaseModel):
                    v = v.to_dict(ignore_none=ignore_none)
                if k == "proxies" or k == "inbounds":
                    res = {}
                    for key, value in v.items():
                        if isinstance(k, ProxyTypes):
                            res[key.value] = value
                        else:
                            res[key] = value
                    result[k] = res
                else:
                    result[k] = v

            return result

        return asdict(self, dict_factory=dict_factory)
