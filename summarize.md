# 从写项目学到的技术总结以及细节

## jwt 验证

- 引入 flask_jwt_extended
- 指定哪个字段作为生成token的依据（选取的依据必须是字符串类型的）
- 每次使用时校验对象
- 统一的错误处理
- 记录那些接口需要token

本次使用双重token（access token, refresh token）
access token 很存活时间短，refresh token 存活时间长 
access token 过期后使用 通过 refresh token 验证的接口获取新的access token
短时的 access token 更具有安全性

## 头像管理

### 为了优化用户体验，前端直接上传图片即可。因此，图片大多偏大尺寸不一。所以要统一一下

- 将传来的图片缩放裁剪至 80x80 ,利用第三方服务存储原图片和处理过的图片

## 第二次模块优化

按照数据库的表来分