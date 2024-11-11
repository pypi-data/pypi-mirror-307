"""
# File       : login.py
# Time       ：2024/8/22 19:09
# Author     ：xuewei zhang
# Email      ：shuiheyangguang@gmail.com
# version    ：python 3.12
# Description：
"""
from user_auth_zxw.SDK_jwt.jwt import create_jwt_token
from user_auth_zxw.SDK_jwt.jwt_刷新管理 import create_refresh_token

from sqlalchemy.ext.asyncio import AsyncSession

from user_auth_zxw.db.models import User
from user_auth_zxw.apis.schemas import 返回_login, Payload


async def login_user_async(user: User, db: AsyncSession) -> 返回_login:
    print("apis/api_登录注册/login.py:login_user_async: user_info=获取中")

    # 创建jwt的payload
    payload: Payload = user.to_payload()

    # 生成jwt token
    access_token = create_jwt_token(payload=payload.model_dump())
    refresh_token = create_refresh_token(user.id, db)
    await db.commit()

    return 返回_login(access_token=access_token,
                      refresh_token=refresh_token.token,
                      user_info=payload)
