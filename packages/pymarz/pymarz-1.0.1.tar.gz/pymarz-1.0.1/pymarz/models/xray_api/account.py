from enum import Enum


class XTLSFlows(str, Enum):
    NONE = ''
    VISION = 'xtls-rprx-vision'

class ShadowsocksMethods(str, Enum):
    AES_128_GCM = 'aes-128-gcm'
    AES_256_GCM = 'aes-256-gcm'
    CHACHA20_POLY1305 = 'chacha20-ietf-poly1305'

