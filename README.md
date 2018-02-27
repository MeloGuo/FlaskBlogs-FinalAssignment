# 博客论坛
本项目是《Flask Web开发》的实践。也是我第一次接触后端的过程，在这个过程中了解了Flask框架下的后端的基本流程和内容，服务端渲染，REST架构。
并且在coding的过程中学习如何使用Git和GitHub。

## 使用说明
将项目clone到本地之后，创建一个虚拟环境：
```virtualenv venv```

然后激活虚拟环境：
```source venv/bin/activate```

在虚拟环境中，使用pip安装各种lib：
```pip install -r requirements.txt```

启动服务器:
```python manage.py runserver```

即可访问```http://127.0.0.1:5000/```

----
#### 更新日志
- v1.0 部署上线腾讯云 2017.11.20
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

- http://localhost:5000/api/v1.0/posts/\<int:id>/    [methods POST,PUT]

- http://localhost:5000/api/v1.0/users/\<int:id>/posts/

- http://localhost:5000/api/v1.0/users/\<int:id>/timeline/

- http://localhost:5000/api/v1.0/comments/

- http://localhost:5000/api/v1.0/comments/\<int:id>/

- http://localhost:5000/api/v1.0/posts/\<int:id>/comments/    [methods POST]
