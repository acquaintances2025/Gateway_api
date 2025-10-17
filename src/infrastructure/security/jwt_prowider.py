import jwt

from typing import Tuple, Dict, Optional, Any
from src.config.settings import Config
from ..loggings.logger import logger



async def decode_token(token) ->  Tuple[Optional[Dict[str, Any]], bool]:
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
        return payload, True
    except jwt.ExpiredSignatureError:
        logger.warning("Срок действия токена истек")
        return None, False
    except Exception as e:
        logger.error(f"Ошибка при проверке токена: {e}")
        return None, False
