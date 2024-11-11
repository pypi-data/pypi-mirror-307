# 常用函数包

-
    1. 项目根目录下必须包含config.py文件

- 支付接口编写规范：
  支付服务_代码规范.py

# 更细说明

- 0.0.6.5 : 
  - 去掉地址中冗余地址../api/...
  - tags优化
- 0.0.6.6 :
  - 新增:add_new_role函数, 新增app name, 用户权限
- 0.0.6.7 : 
- - 新增:delete_role函数, 解除用户权限(只解除关联, 不删除role表)
- 0.0.6.8 : 
- - 新增:require_roles函数, 批量验证权限
- 0.0.6.9 : 
- - bug fix : 注册登录 import add_new_role
- 0.0.7 : 
- - bug fix : add new role
- 0.0.7.1:
- - 新增api: /register-or-login-phone/   手机号注册或登录
- 0.0.7.2:
- - 取消get_current_user的print(token)
- 0.0.7.3:
- - 上传vue前端页面
- 0.0.7.4:
- - 优化configs.py导入
- 0.0.8: 新增:批量删除用户角色(delete_roles)
- 0.0.9: 表结构User新增字段:referer_id,referer,invitees , 手机号注册登录新增相应字段.  对应功能: 增加邀请人信息
- 0.1.0: 修改: jwt验证失败, 弹出401 HTTPException_AppToolsSZXW异常
- 0.1.1: 支持多线程任务，集成修改: 短信验证码验证，redis存储与验证
