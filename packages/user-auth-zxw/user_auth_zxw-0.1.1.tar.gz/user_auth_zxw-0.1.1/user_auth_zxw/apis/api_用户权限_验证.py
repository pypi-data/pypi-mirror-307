"""
# File       : 角色.py
# Time       ：2024/8/20 下午6:09
# Author     ：xuewei zhang
# Email      ：shuiheyangguang@gmail.com
# version    ：python 3.12
# Description：
"""
from fastapi import APIRouter, Depends
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from user_auth_zxw.db.models import User, App
from user_auth_zxw.db.get_db import get_db
from user_auth_zxw.SDK_jwt.jwt import get_current_user
from user_auth_zxw.apis.schemas import 请求_验证角色_from_header, 返回_验证角色_from_header

from app_tools_zxw.Errors.api_errors import HTTPException_AppToolsSZXW, ErrorCode

router = APIRouter(prefix="/roles")


def require_role(role_name: str, app_name: str):
    """
    本函数主要作用：检查用户是否有某个角色，如果没有则返回403，如果有则返回用户信息
    使用方法：在需要检查角色的路由上加上Depends(require_role("admin", "app1"))
    使用示例：下方的get_admin_data函数
    主要流程：1. 通过jwt验证获取用户信息
            2. 通过app_name获取应用信息
            3. 判断用户是否有该角色
    :param role_name:
    :param app_name:
    :return:
    """

    async def role_checker(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
        result_app = await db.execute(select(App).filter(App.name == app_name))
        app = result_app.scalar_one_or_none()
        if app is None:
            raise HTTPException_AppToolsSZXW(
                error_code=ErrorCode.应用未找到,
                detail="应用未找到",
                http_status_code=403
            )

        if not any(role.name == role_name and role.app_id == app.id for role in user.roles):
            raise HTTPException_AppToolsSZXW(
                error_code=ErrorCode.权限不足,
                detail="权限不足",
                http_status_code=403
            )
        return user

    return role_checker


def require_roles(role_names: list[str], app_name: str):
    """
    本函数主要作用：检查用户是否有某个角色，如果没有则返回403，如果有则返回用户信息
    使用方法：在需要检查角色的路由上加上Depends(require_role("admin", "app1"))
    使用示例：下方的get_admin_data函数
    主要流程：1. 通过jwt验证获取用户信息
            2. 通过app_name获取应用信息
            3. 判断用户是否有该角色
    :param role_names:
    :param app_name:
    :return:
    """

    async def role_checker(
            user: User = Depends(get_current_user),
            db: AsyncSession = Depends(get_db)
    ):
        result_app = await db.execute(select(App).filter(App.name == app_name))
        app = result_app.scalar_one_or_none()
        if app is None:
            raise HTTPException_AppToolsSZXW(
                error_code=ErrorCode.应用未找到,
                detail="应用未找到",
                http_status_code=403
            )

        if not any(role.name in role_names and role.app_id == app.id for role in user.roles):
            raise HTTPException_AppToolsSZXW(
                error_code=ErrorCode.权限不足,
                detail="权限不足",
                http_status_code=403
            )
        return user

    return role_checker


@router.post("/role-auth/", response_model=返回_验证角色_from_header)
async def 验证角色_from_header(request: 请求_验证角色_from_header,
                               user: User = Depends(get_current_user),
                               db: AsyncSession = Depends(get_db)):
    """
    权限验证函数
    :param request: role_name,app_name
    :param user:
    :param db:
    :return:
    """
    print(user.to_payload())
    user: User = await require_role(request.role_name, request.app_name)(user, db)
    return {'status': True}


@router.get("/admin-data/")
async def demo_验证admin角色(user: User = Depends(require_role("admin", "app1"))):
    """
    权限验证函数的使用示例
    :param user:
    :return:
    """
    return {"data": "This is admin data"}
