## 使用说明

----
#### 更新日志
- v0.9 编写api接口 2017.11.13
- v0.8 增加用户头像 2017.11.12
- v0.7 增加用户评论 2017.11.10
- v0.6 增加关注用户 2017.11.10
- v0.5 增加博客文章 2017.11.10
- v0.4 增加用户资料 2017.11.09
- v0.3 增加用户角色权限 2017.11.09
- v0.2 增加用户认证功能 2017.11.08
- v0.1 基础框架 2017.11.07

----
#### API接口
- http://localhost:5000/api/v1.0/posts/

- http://localhost:5000/api/v1.0/posts/\<int:id>/

methods POST,PUT

- http://localhost:5000/api/v1.0/users/\<int:id>/posts/

- http://localhost:5000/api/v1.0/users/\<int:id>/timeline/

- http://localhost:5000/api/v1.0/comments/

- http://localhost:5000/api/v1.0/comments/\<int:id>/

- http://localhost:5000/api/v1.0/posts/\<int:id>/comments/

methods POST

